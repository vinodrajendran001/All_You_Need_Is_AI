---
type: concept
created: 2026-09-11
updated: 2026-10-23
tags:
  - concept
  - hardware
  - inference
source_ids:
  - src-2026-09-07-semianalysis-tpu-inferencex
  - src-2026-10-21-simpson-torchtpu
status: active
---

# Accelerator Software Externalization

## Definition

The work required to make an accelerator usable by people who did not design it — and, more importantly,
by models that were not designed for it. Externalization is the gap between a chip that is competitive on
a specification sheet and one that serves a given model well: a framework integration, a compiler path, a
kernel library, a tuned schedule per model family, and model architectures whose dimensions happen to
suit the hardware's tile geometry.

The phrase comes from Google's effort to make TPUs available outside Google, documented in
[[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]], but the concept is vendor-independent.
It names why a credible second source of inference silicon is not a procurement decision.

## Why it matters

The benchmark numbers are the least durable part of the story. The same TPUv7 Ironwood hardware is
**50–96% better per dollar than B200/B300** at one operating point, **8–25% better** when normalised on
end-to-end response time, and **roughly 30% worse** against a disaggregated GB300 NVL72 in the middle of
the curve. Which number is true depends on the normalisation axis, and any single figure quoted without
it is misleading.

What does not change with normalisation is the cost of getting there. Bringing up a single model
(Qwen3.5 397B in FP8) produced dozens of kernel- and memory-level changes, each worth single-digit to
low-double-digit percentages: combining two all-gathers saved ~80 µs per layer (4.64 ms per forward pass
across 58 layers); moving ReduceScatter to SparseCore with double buffering gave 4.1–14.2%, but not
always, so a VMEM-derived threshold keeps small collectives on TensorCore; a packed sort key took a kernel
from 106.6 µs to 21.7 µs; compact recurrent-state allocation reclaimed ~76 GiB of HBM and 18% throughput;
splitting RPA v3 block size into fetch-16k and compute-4k took decode from 64.9k to 96.3k tok/s (+49%) on
an inverted-U curve — and shipped as an environment variable because the tuned-parameter table could only
hold one block size.

That last detail is the concept in miniature. A 49% win existed, was found, and was not expressible in
the configuration system, so it is not automatically available to anyone else.

## Current synthesis

**The software stack is being rebuilt, and the compiler is the fixed point.** vLLM's TPU support has gone
through three stages: PyTorch/XLA with lazy tensors → a `tpu-inference` backend using JAX with
**TorchAX** → **TorchTPU**, a native PyTorch `PrivateUse1` device. Throughout, **XLA remains the
compiler** — not Inductor, not Triton — and Pallas kernels carry over. TorchTPU was in private beta with
open-sourcing expected around mid-October at the PyTorch Conference. **Update 2026-10-23: it shipped.**
[[Ebba Simpson - Introducing TorchTPU]] is the PyTorch blog announcement, dated 2026-10-21, and it
confirms the architecture SemiAnalysis described while adding that TorchTPU **drops the JAX runtime
dependency** entirely — so the TorchAX middle stage of that lineage is retired rather than layered over.
The section below replaces the vault's earlier reading of TorchTPU as an unverified roadmap item.

**Hardware tile geometry now constrains model architecture.** This is the most consequential and least
obvious finding. The TPU matrix unit was **128×128 (16,384 MACs/cycle) through v5** and is **256×256
(65,536 MACs/cycle) from v6e**. Consequently **Llama 3 8B's head dimension of 128 caps attention matmuls
at 50% MXU utilisation, and a head dimension of 64 caps them at 25%.** gpt-oss ships at 64; DeepSeek MLA
splits 128+64=192. Head dimension is normally chosen for modelling reasons; on a 256×256 MXU it becomes a
hardware-utilisation decision.

**Hence "TPUs are picky," and bring-up cost correlates poorly with model popularity.** A widely used
model with awkward dimensions is expensive to support; an obscure one with friendly dimensions is cheap.
Architectural hyperparameters increasingly have to be chosen with a target accelerator's tile geometry in
mind, which is hardware constraining models rather than the reverse.

**The same coupling appears on the software side.** [[Megakernels]] shows a model's use of *parallel
transformer layers* — chosen for unrelated reasons — determining how effectively wave quantisation can be
backfilled. In both cases an implementation technique's payoff is decided by an architecture decision
made years earlier for other reasons.

**Interconnect is being redesigned around the new workload.** ICI went from a 2D torus (v2/v3) to a 3D
torus from v4/v5p — 4×4×4 = 64 chips per rack, twisted torus, Optical Circuit Switches rewiring around
failures in seconds and scaling to the **9,216-chip Ironwood superpod at 42.5 FP8 exaflops**. **TPUv8i
"Boardfly" replaces the torus with a high-radix dragonfly-style fabric**, cutting network diameter by
more than 50% (~16 hops to ~7 at 1,024–1,152 chips), doubling ICI bandwidth to **19.2 Tb/s**, and
tripling on-chip SRAM to **384 MB** — sized specifically to hold reasoning and agentic KV cache on-chip.
Google has split training and inference architectures for the first time (8t versus 8i), and the target
workload is named explicitly: multi-turn, long context, high prefix reuse, sub-agent bursts.

That is the first instance in this vault of **agent workloads driving a hardware design decision** rather
than a serving-software one.

**Ironwood's own particulars.** Two separate compute dies joined by a die-to-die link, each an
independent logical device, breaking the MegaCore convention; 2 TensorCores and 4 third-generation
SparseCores per chip; roughly **6× Trillium's HBM capacity**; the **first TPU with native FP8** and no
native FP4 (which arrives with TPUv8i). Anthropic has committed to **over one million TPUs** — about 400k
purchased directly, 600k rented via GCP — surpassing DeepMind's own usage by 2029.

**The roadmap is largely catching up to GPU serving practice**: speculative decoding and MTP,
prefill-decode disaggregation via TPU-Sync (zero-copy through native PJRTBuffer descriptors), KV cache
offloading to DRAM, Mooncake Store P2P pooling, AgentX.

## The framework-level bill, itemized — and portability still is not performance

The SemiAnalysis material above measures externalization in per-model kernel tuning.
[[Ebba Simpson - Introducing TorchTPU]] measures it one layer up, and the itemization is the useful
part: before any PyTorch user can reach a TPU, someone has to supply a C++ `PrivateUse1` dispatcher
backend with TPU storage behind `at::Tensor`, a real eager mode (Strict, Debug, and a DeferAndFuse mode
that accumulates ops to a materialization point), a `torch.compile` entry point that lowers a Dynamo FX
graph to a single StableHLO program, collectives at the Process Group level, kernel-authoring DSLs, and
a dynamic-shape story. That list, not the benchmark table, is what a second source of silicon owes a
framework.

Coverage is reported first-party and without a stated pass criterion: **~450 ATen ops**, the **5,000
most-downloaded Hugging Face models**, a validation corpus of **4,917 models across 500+ architecture
families**, **Tier 1 pass rate 98% (4,821/4,917)**, **Tier 2 numerical parity with GPU 97% (638/657)**,
and bounded dynamism correct on **834/839** models, reported as 99%.

The post is candid that none of this is speed. Its own FLUX sequence prices the gap: **11.49s per step
(0.26 samples/s) baseline → 9.95s with DeferAndFuse (1.15x) → 6.52s with SimpleFSDP (1.76x) → 5.55s
with a Pallas SplashAttention kernel (2.07x) → 3.02s under full `torch.compile` (3.80x) → 2.78s
(1.08 samples/s) after peephole rewriting**. A straight `.to("tpu")` port buys the first row. The
remaining **4.1x** is hand work, and the post recommends "pursuing an optimal approach based on Pallas
kernels" and TPU-specific stacks such as vLLM-TorchTPU, SGLang-TorchTPU, or TorchTitan-TorchTPU for peak
production performance. Hardware generation, batch size, and baseline implementation are not fully
stated for that ladder.

Two first-party figures with **no stated workload, hardware, or baseline** deserve to be carried as
unverified: DeferAndFuse is said to be **"50% or more faster"** than Strict Eager, and **Skinny
Collectives** — the mechanism that isolates collectives into separate modules to avoid cross-rank graph
inconsistency — are said to cost **30-40% end-to-end**. The second is the more interesting number,
because it is a *correctness* workaround whose price is paid in throughput.

And the externalization story does not uniformly end in a win. On **Qwen3 MoE 235B across 64 TPU v7**
(local batch 16, sequence length 4096, 94 decoder layers in one scan loop), the TorchTitan/PyTorch path
reports **1,828 TPS** against **1,937 TPS** for JAX/MaxText on the same hardware — the externalized
framework roughly **6% behind** the vendor's native one. **DLRM v2 on 32 TPU v7x** at **18.3 ms** step
latency is described as **100% parity** with a JAX baseline, which is a stronger word than a single
latency figure supports. Both results are first-party.

## Open questions

- The results come from an Official Preview on one model. Google was presumably involved in tuning, and
  the NVIDIA configurations may not have received equivalent attention.
- TTFT is materially worse on TPU (mean 5.41s against 3.75s on B200 and 2.40s on B300) — which matters
  most for exactly the interactive agentic workloads TPUv8i is being designed for.
- TorchTPU's portability claims were unverified at the time of the SemiAnalysis report; it was then
  unreleased. **Revised 2026-10-23:** it is released, and the coverage claims are now *stated* rather
  than absent — but they remain first-party, with no published pass criterion and no evidence that any
  of the 5,000 supported models runs unchanged in production. Portability is now documented; it is
  still not independently verified.
- The announcement's own roadmap — bounded dynamism, FP8/FP4, reinforcement-learning integration,
  dynamic kernels — is **6-12 months** of future work, so parts of the externalization story described
  as shipped are descriptions of intent.
- Several of the features exist to work around the port rather than to make it fast: `@spmd_safe` is
  described as brittle if the code is actually MPMD, Skinny Collectives trade 30-40% end-to-end for
  rank consistency, and FlexAttention was unsupported in one TorchTitan example and replaced with
  vanilla scaled dot-product attention. How much of a framework's surface silently changes semantics
  on a second-source accelerator?
- No general theory exists for how much of the per-model tuning transfers to the next model. The
  evidence so far suggests not much.
- If tile geometry constrains architecture, the equilibrium is unclear: do model designers converge on
  hardware-friendly dimensions, do accelerators become more flexible, or does the ecosystem fragment by
  target?

## Related pages

- [[AI Accelerator Architecture]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[Prefill-Decode Disaggregation]]
- [[GPU Kernel Optimization]]
- [[Megakernels]]
- [[KV Cache]]
- [[Linear Attention and Recurrent Memory]]
- [[ML Systems at Scale]]
- [[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]]
- [[Ebba Simpson - Introducing TorchTPU]]
- [[PyTorch]]
- [[Distributed Training Parallelism]]
- [[Meta]]
- [[Google Cloud]]
