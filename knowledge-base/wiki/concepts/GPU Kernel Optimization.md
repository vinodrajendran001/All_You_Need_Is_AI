---
type: concept
created: 2026-08-26
updated: 2026-08-26
tags:
  - concept
  - gpu
  - kernels
  - performance-engineering
  - cuda
source_ids:
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-07-03-fergus-finn-cuda-kernel
  - src-2026-04-20-moonshotai-flashkda-v1
status: active
---

# GPU Kernel Optimization

## Definition

**Kernel optimization** is the engineering of individual GPU programs so that they approach the hardware's achievable limit rather than its nominal one. It sits between [[GPU Execution Model]] (how a kernel runs at all) and [[Inference Serving Engines]] (how many requests are scheduled across kernels), and it is governed throughout by [[Arithmetic Intensity and the Roofline Model]]: a kernel is only worth optimizing along the axis it is actually bound by.

## Why it matters

Model architecture sets what must be computed; kernels set what it costs. Most of the inference gains of the last several years came not from new mathematics but from re-expressing the same mathematics to move fewer bytes — FlashAttention being the canonical case, where an algebraically identical attention computation became several times faster purely by avoiding materialization of the attention matrix in high-bandwidth memory.

This page exists because the vault previously discussed attention, quantization, and serving without naming the kernel-level lineage underneath them.

## The optimization ladder

[[Wafer - AI Performance Engineering Resources]] orders kernel work as a dependency chain rather than a menu, and the ordering is the useful part:

1. **Memory access shape first.** Coalescing, shared-memory tiling, and bank conflicts, taught through matrix transpose and parallel reduction. At this stage the lesson is that occupancy is a poor proxy for performance and measured hardware behavior is the real guide.
2. **Algorithmic primitives that avoid materialization.** Decoupled look-back scan (one pass over memory) and online softmax (numerically stable without storing intermediates). Online softmax is the direct precursor of FlashAttention.
3. **Register tiling and matmul.** Building a matmul from naive CUDA through shared-memory and register tiling until it approaches cuBLAS, then reading layouts, PTX, and machine code to explain the remaining gap.
4. **Tensor cores and low precision.** FP8 (E4M3/E5M2) and shared-scale MX formats defined by OCP specifications, executed through vendor libraries with explicit scaling control. See [[Model Quantization and Efficiency]].
5. **Asynchrony and specialized hardware paths.** The Tensor Memory Accelerator, thread-block clusters, and producer-consumer pipelines on Hopper; tensor memory and `tcgen05` matrix instructions on Blackwell.

### The FlashAttention lineage

The clearest illustration of the ladder is the attention kernel line, which the vault had not previously recorded:

| Version | Contribution |
| --- | --- |
| FlashAttention | IO-aware exact attention; tiling and recomputation instead of a materialized N×N matrix |
| FlashAttention-2 | Better work partitioning and parallelism across warps and blocks |
| FlashAttention-3 | Asynchronous data movement overlapped with tensor-core execution on Hopper |
| FlashAttention-4 | A Blackwell-specific schedule |

Each step is a scheduling and data-movement change, not a change to the attention function. This is the strongest available evidence for the vault's recurring claim that **inference progress is mostly memory-movement engineering**; see [[Arithmetic Intensity and the Roofline Model]]. [[MoonshotAI - FlashKDA v1 Deep Dive]] is the vault's worked example of the same discipline applied to a linear-attention variant, where bf16 persisted state with fp32 updates was needed to make the theoretical efficiency real.

## Programming models

Writing kernels directly in CUDA C++ is only one option, and the choice of abstraction is itself a performance decision:

- **Triton** — a blocked-program language and compiler; the programmer describes tiles, the compiler handles intra-tile scheduling.
- **CUTLASS and CuTe** — a layout algebra plus collective/kernel structure, giving explicit control over tiling, copies, and matrix-multiply atoms without writing raw PTX.
- **CUDA Tile IR** — NVIDIA's newer compiler-owned tile abstraction.
- **Pallas** — the JAX kernel model, targeting both GPU and TPU backends.
- **ROCm Composable Kernel, AITER, and HipKittens** — the AMD equivalents; HipKittens is a tile abstraction in the same spirit as CUTLASS.
- **NKI** — the tile-level model for AWS NeuronCore hardware.

The recurring shape across all of them is *tiles as the unit of reasoning*, which is what the memory hierarchy rewards.

## Measurement is part of the work

The source treats profiling and correctness as inseparable from optimization rather than as a following step: Nsight Systems for system and CPU-GPU timelines, Nsight Compute for kernel metrics and roofline analysis, Compute Sanitizer for memory, race, initialization, and synchronization errors, and documented GEMM measurement methodology for reproducible benchmarking. A faster kernel that is not verified correct is not a result — the same standard [[Benchmark Optimization]] argues for at the model level.

## Open questions

- How much of the kernel ladder survives as compilers absorb it? Triton and CUDA Tile exist precisely to make step 3 unnecessary, yet the fastest kernels are still hand-written.
- Do tile abstractions genuinely port across vendors, or does each backend leak enough that a "portable" kernel is rewritten in practice?
- FP8 and MX formats are specified openly, but scaling strategy is where accuracy is won or lost — how much of that is transferable between models?
- When does a kernel stop being worth hand-optimizing because the workload has moved to a different bottleneck, such as collectives or scheduling?
- Can [[AI-Generated Kernels]] climb this ladder, or only its first rungs?

## Related pages

- [[Wafer - AI Performance Engineering Resources]]
- [[GPU Execution Model]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[AI Accelerator Architecture]]
- [[AI-Generated Kernels]]
- [[Model Quantization and Efficiency]]
- [[Transformer Architecture]]
- [[MoonshotAI - FlashKDA v1 Deep Dive]]
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]]
- [[Inference Serving Engines]]
