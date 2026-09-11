---
type: concept
created: 2026-09-11
updated: 2026-09-11
tags:
  - concept
  - hardware
  - inference
source_ids:
  - src-2026-09-07-semianalysis-tpu-inferencex
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
open-sourcing expected around mid-October at the PyTorch Conference.

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

## Open questions

- The results come from an Official Preview on one model. Google was presumably involved in tuning, and
  the NVIDIA configurations may not have received equivalent attention.
- TTFT is materially worse on TPU (mean 5.41s against 3.75s on B200 and 2.40s on B300) — which matters
  most for exactly the interactive agentic workloads TPUv8i is being designed for.
- TorchTPU's portability claims were unverified at the time of writing; it was unreleased.
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
