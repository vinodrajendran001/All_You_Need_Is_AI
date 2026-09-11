---
type: concept
created: 2026-09-11
updated: 2026-09-11
tags:
  - concept
  - topic/gpu
  - topic/inference
  - topic/serving
source_ids:
  - src-2026-09-08-cohere-megakernel-serving
status: active
---

# Megakernels

## Definition

A serving technique that collapses an entire model forward pass — in current practice, one decode step —
into a **single persistent GPU kernel launch**. Rather than the driver scheduling thousands of
threadblocks across hundreds of kernels, the megakernel launches **one threadblock per SM**, keeps it
resident for the whole step, and has it interpret a **task list** held in global memory. Dependencies
between tasks become **explicit counters** instead of kernel boundaries.

This is a scheduling change, not a fusion trick. Kernel fusion merges adjacent operations to avoid a
round trip through memory; a megakernel replaces the scheduler.

## Why it matters

Batch-1 decode is bandwidth-bound and spends a large fraction of its time not moving weights. The
technique attacks four distinct sources of that waste, and the middle two are the ones fusion cannot
reach:

1. **Launch and synchronisation overhead** — the expected and least interesting win.
2. **Wave quantisation.** A GPU with 132 SMs running 200 tiles needs two waves for 1.5 waves of work. A
   megakernel can backfill the partial wave with unrelated tasks, so the waste is recoverable rather than
   structural.
3. **False dependencies.** A kernel boundary forces all-or-nothing ordering. With per-task counters, the
   O-projection for one KV group can start the moment *that group's* attention lands.
4. **Weight prefetch.** Weights are immutable, so weight tiles can begin streaming before activation
   dependencies resolve — in code, the prefetch call sits above the input-barrier wait.

Measured on Cohere's **North Mini Code** (30B total, 3.3B active), decode streams **6.6 GB of weights per
step** plus ~0.5 GB of KV cache at 8K; an H100 at **3.35 TB/s** therefore caps decode at about **470
tok/s**. vLLM reaches **185 tok/s (39% of speed-of-light)**; the megakernel reaches **292 tok/s (62%),
a 1.58× speedup at batch 1**. End-to-end across benchmarks the range is **1.25×–1.41×** (AIME 2025 1.41×,
SciCode 1.37×, MMLU-Pro CS 1.33×, LiveCodeBench v6 1.28×, GPQA 1.25×), holding to **256K context** with
accuracy preserved — SciCode 38.9% ± 1.6% against 38.2% over 7 runs.

## Current synthesis

**The lineage.** Hazy Research's "Look Ma, No Bubbles!" demonstrated the approach on Llama-3.2-1B,
reaching 78% of H100 bandwidth at batch 1, and contributed the task-interpreter pattern, counter-based
synchronisation and cross-task overlap. [[Cohere - North Mini Code Megakernel Serving Engine]] claims the
first *fully fledged serving system* built around one, as opposed to a compiler that auto-generates
megakernels or a batch-size-1 demonstration. Its departures: heavy `wgmma` tensor-core use even at batch
1, and abandoning shared-memory paging because the bookkeeping was complex, buggy and high-overhead.

**One ABI for every operation.** Cohere's design fixes **3 warpgroups / 12 warps** for all tasks:
warpgroup 0 splits into a controller (prefetching task descriptors into a shared-memory ring), a
producer, a storer and one idle warp; the remaining 8 warps are consumers. Roles are compile-time tags
resolved with `if constexpr`, and workers synchronise on a named barrier that deliberately excludes the
controller so it can run ahead. A task is a **32-int32 descriptor** whose field 0 is the opcode, with
**16 opcodes in four groups**: dense GEMMs, attention, MoE routing, MoE GEMMs.

**Barriers are O(1) in fan-in.** They are plain global-memory counters manipulated with `atomicAdd`,
`fence.proxy.async` and `__threadfence()`, spun on with `__nanosleep(20)`. Cost does not grow with
fan-in or fan-out, which is what makes fine-grained dependency graphs affordable at all.

**Porting is a four-step recipe and step 3 is the hard one** — opcode definition, kernel body, **barrier
accounting**, scheduling.

**Scheduling is tuned, not derived, and the obvious optimisation is wrong.** Placement is mostly static
round-robin (`task k → SM k mod 132`) with a hand-tuned wave order
(`qkv → router → top-k → route setup → MoE gather → attention → MoE up/down → O-proj → RMSNorm`). Ablated
at batch 1/2/4: tuned gives **291/423/553 tok/s**; interleaving loses **3/4/4%**; attention-first loses
**19/14/8%**. And **dependency-affinity placement — co-locating dependent tasks on the same SM — made it
1–2% slower.** The authors state that a complete causal model "remains open." Dynamic work stealing is
used only for the irregular work (attention and MoE) via drain-claimer tasks; earlier greedy
topology-aware and brute-force schedulers gave ~10% on a dense model and did not transfer to MoE.

**Model architecture determines how much the technique buys.** North Mini Code uses **parallel
transformer layers** — attention and MoE computed from the same normalised input and rejoined by a fused
residual add plus RMSNorm — which guarantees independent work is always available to backfill with. This
is the software-side analogue of the tile-geometry coupling in
[[Accelerator Software Externalization]]: a model design choice made for other reasons decides how well
an implementation technique works.

**Real traffic benefits more than synthetic traffic, which inverts a benchmarking convention.** With
real expert distributions the speedup is **1.32× at batch 8 against 1.14× under uniform routing**,
because real requests concentrate on the same experts, leaving sparser MoE work and therefore more
bubbles to fill. **Synthetic uniform routing understates megakernel speedup on real traffic** — a
warning that belongs with the normalisation caveats in [[Serving Benchmarks and Goodput]].

## Open questions

- Reported maximum batch size is 8, described as a configuration rather than architectural limit.
  Production serving runs far above that, and at higher batch sizes arithmetic intensity rises and the
  bandwidth bound that motivates the technique weakens.
- Decode only, with no mixed prefill/decode support — a component of a serving system rather than a
  serving system in the sense continuous-batching engines mean.
- The schedule was found by tuning with no causal model. A different model, or the same model on
  different hardware, plausibly requires the search to be redone.
- Why dependency-affinity placement *hurts* is unexplained, and it is the single clearest indicator of
  how immature megakernel scheduling theory is.
- Whether shared-memory paging is intrinsically not worth it, or was merely hard in this implementation,
  is left open.
- The 1.58× headline is against vLLM at batch 1, which is not vLLM's operating point; the end-to-end
  1.25×–1.41× band is the more meaningful and notably narrower comparison.

## Related pages

- [[GPU Kernel Optimization]]
- [[GPU Execution Model]]
- [[Inference Serving Engines]]
- [[LLM Inference]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Mixture of Experts]]
- [[KV Cache]]
- [[AI-Generated Kernels]]
- [[Serving Benchmarks and Goodput]]
- [[Accelerator Software Externalization]]
- [[Cohere - North Mini Code Megakernel Serving Engine]]
