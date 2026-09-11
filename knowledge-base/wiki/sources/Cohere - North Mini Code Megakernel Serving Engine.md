---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-08-cohere-megakernel-serving
source_title: "Cohere's North Mini Code Megakernel Serving Engine"
source_author: Cohere
source_url: https://cohere.com/blog/megakernels
tags:
  - source/summary
  - gpu
  - inference
  - serving
source_ids:
  - src-2026-09-08-cohere-megakernel-serving
status: active
---

# Cohere - North Mini Code Megakernel Serving Engine

## Summary

An engineering report on what the authors claim is the **first fully fledged serving system built around
a decode megakernel** — prior work being either compilers that auto-generate megakernels or batch-size-1
research demonstrations. The technique is to collapse an entire decode step into **one persistent kernel
launch**: one threadblock per SM, resident for the whole step, pulling work from a task list in global
memory, with inter-task dependencies expressed as **explicit counters** rather than kernel boundaries.

The measured result for **North Mini Code**, a 30B model with 3.3B active parameters: the megakernel
reaches **292 tok/s at batch 1, which is 62% of the hardware's speed-of-light against vLLM's 185 tok/s
(39%)** — a **1.58× speedup**. End-to-end on real benchmarks it is **1.25×–1.41×**, holding to **256K
context with no measurable accuracy loss**.

The article's value is in the parts that are not the speedup: a complete ABI, a scheduler ablation that
contradicts the intuitive design, and an honest admission that a causal model of why the tuned schedule
wins "remains open."

## Key claims

**The speed-of-light calculation sets the target.** At BF16 the model streams **6.6 GB of weights per
decode step** plus roughly 0.5 GB of KV cache at 8K context; an H100 at **3.35 TB/s** therefore caps
decode at about **470 tok/s**. Everything above is a percentage of that ceiling.

**A megakernel is a scheduling change, not a fusion trick.** A GPU has ~100–150 SMs; the megakernel
launches exactly one threadblock per SM and keeps it resident, so "instead of the GPU driver scheduling
thousands of threadblocks across hundreds of kernels, the kernel itself interprets a task list."

**Four independent sources of speedup**, and the second is the least obvious:

1. **Reduced launch and synchronisation overhead** — the expected win.
2. **Wave quantisation.** "200 tiles on 132 SMs means two waves for 1.5 waves of work." Because the
   megakernel can backfill the partial wave with unrelated tasks, the waste is recoverable. North Mini
   Code amplifies this: it uses **parallel transformer layers**, where attention and MoE are computed from
   the same normalised input and rejoined by a fused residual add plus RMSNorm, so there is always
   independent work available to backfill with.
3. **Dropping false dependencies.** Kernel boundaries force all-or-nothing ordering; with per-task
   counters, the O-projection for a KV group can start as soon as *that group's* attention lands.
4. **Weight prefetch.** Weights are immutable, so weight tiles can stream before activation dependencies
   resolve — visible in the code as `prefetch_weight_tiles` sitting above `wait_input_bars`.

**It builds explicitly on Hazy Research's "Look Ma, No Bubbles!"** (Llama-3.2-1B at 78% of H100 bandwidth
at batch 1), borrowing the task-interpreter pattern, counter-based synchronisation, and cross-task
overlap. Two deliberate departures: **heavy `wgmma` tensor-core use even at batch 1**, and **abandoning
shared-memory paging** because "the bookkeeping was complex, buggy, and had high overhead."

**One ABI for every operation — exactly 3 warpgroups, 12 warps.** Warpgroup 0 splits into a controller
(warp 0, prefetching task descriptors into a shared-memory ring), a producer (warp 1), a storer (warp 2),
and an idle warp 3; the other 8 warps are consumers. Roles are compile-time tags resolved with
`if constexpr`, and workers synchronise on a named barrier `worker_sync` that deliberately excludes the
controller so it can run ahead.

**A task is a 32-int32 descriptor whose field 0 is the opcode**, with **16 opcodes in four groups**:
dense GEMMs, attention, MoE routing, and MoE GEMMs.

**Barriers are plain global-memory counters and their cost does not grow with fan-in.** The mechanism is
`atomicAdd` with `fence.proxy.async` and `__threadfence()`, spun on with `__nanosleep(20)` — **O(1)
regardless of fan-in or fan-out**, which is what makes fine-grained dependency graphs affordable.

**Porting is a four-step recipe and step 3 is the hard one.** The steps are opcode definition, kernel
body, barrier accounting, and scheduling; the authors state plainly that **"the hard part is step 3."**

**The scheduler ablation contradicts the obvious design.** Scheduling is mostly static round-robin
(`task k → SM k mod 132`) with a hand-tuned wave order:
`qkv → router → top-k → route setup → MoE gather → attention → MoE up/down → O-proj → RMSNorm`. At
batches 1/2/4 the tuned order gives **291/423/553 tok/s**; interleaving loses **3/4/4%**; putting
attention first loses **19/14/8%**. And the intuitively correct optimisation fails: **dependency-affinity
placement — putting dependent tasks on the same SM — slowed it by 1–2%.** The authors say a complete
causal model "remains open."

**Dynamic work stealing is used only where the work is irregular** — attention and MoE — via `*_DRAIN`
claimer tasks. Earlier greedy topology-aware and brute-force schedulers gave ~10% on a dense model but
"did not transfer to MoE."

**Real traffic benefits more than synthetic traffic, for a counterintuitive reason.** With real expert
distributions the speedup is **1.32× at batch 8 versus 1.14× under uniform routing**, because real
requests concentrate on the same experts, leaving sparser MoE work and therefore more bubbles for the
megakernel to fill. The conclusion is worth keeping: **"synthetic uniform routing therefore understates
megakernel speedup on real traffic."**

**End-to-end results across benchmarks**: AIME 2025 **1.41×**, LiveCodeBench v6 1.28×, GPQA 1.25×,
MMLU-Pro CS 1.33×, SciCode 1.37×. Accuracy is preserved — SciCode **38.9% ± 1.6% against vLLM's 38.2%**
over 7 runs.

**Serving integration is a two-thread design**: a Python control-plane thread and a native C++ decode
thread that take turns via park/resume.

**The stated limitations are substantial**: no mixed prefill/decode, a maximum batch size of 8 (a
configuration limit, not an architectural one), and decode only.

## Why it matters

The vault's [[GPU Kernel Optimization]] material has treated kernels as the unit of optimisation. This
source moves the unit up a level: the kernel *is* the program, and the interesting object becomes the
task graph and its schedule. That is a different discipline, and it is why [[Megakernels]] is worth a
page of its own rather than a section under kernel fusion.

Two findings are more broadly instructive than the speedup itself.

First, **dependency-affinity placement made things slower.** The obvious optimisation — co-locate
producer and consumer to exploit locality — is wrong here, and the authors do not have a theory for why.
That is a useful marker for how immature megakernel scheduling is: the working schedule was found by
tuning, not derived.

Second, **the real-traffic result inverts a standard benchmarking assumption.** Uniform synthetic routing
is the conventional way to benchmark an MoE serving path, and it systematically *understates* this
technique because it removes the load imbalance the megakernel is good at absorbing. Anyone benchmarking
MoE serving with synthetic traffic is measuring the wrong distribution — a point that belongs alongside
the normalisation warnings in [[Serving Benchmarks and Goodput]].

The **parallel transformer layer** interaction is also a genuine architecture/implementation coupling:
the model's structure, chosen for other reasons, is what makes backfilling effective. It is the
software-side analogue of the tile-geometry constraint documented in
[[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]].

## Tensions / open questions

- Batch size 8 is the ceiling reported, and production serving runs far above that. The authors call it a
  configuration limit; nothing here demonstrates the technique holds at higher batch sizes, where
  arithmetic intensity rises and the memory-bandwidth bound that motivates the work weakens.
- Decode only, with no mixed prefill/decode support — so this is a component of a serving system, not yet
  a serving system in the sense continuous-batching engines mean.
- The scheduler is hand-tuned with no causal model, and the authors say so. A different model, or the same
  model on a different GPU, plausibly needs the tuning redone.
- The 1.58× is against vLLM at batch 1, which is not vLLM's operating point. The end-to-end 1.25×–1.41×
  range is the more meaningful comparison and is notably narrower.
- Accuracy parity is shown on SciCode over 7 runs (38.9% ± 1.6% vs 38.2%) — reassuring, but a single
  benchmark with overlapping error bars.
- Shared-memory paging was abandoned as buggy and high-overhead. Whether that is a property of the
  technique or of this implementation is left open.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Megakernels]]
- [[GPU Kernel Optimization]]
- [[GPU Execution Model]]
- [[Inference Serving Engines]]
- [[LLM Inference]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Serving Benchmarks and Goodput]]
- [[Cohere]]

## Related pages

- [[Mixture of Experts]]
- [[KV Cache]]
- [[AI-Generated Kernels]]
- [[Software Performance Engineering]]
- [[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]]

## Citations

- Raw capture: [[2026-09-08 Cohere - North Mini Code Megakernel Serving Engine]]
- Source: <https://cohere.com/blog/megakernels>
