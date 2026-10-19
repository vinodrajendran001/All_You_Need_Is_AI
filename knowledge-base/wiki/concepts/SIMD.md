---
type: concept
created: 2026-08-03
updated: 2026-10-19
tags:
  - concept
  - hardware
  - performance
source_ids:
  - src-2026-07-22-mitchell-hashimoto-simd
  - src-2026-08-07-dean-ghemawat-performance-hints
status: active
---

# SIMD

## Definition

Single instruction, multiple data (SIMD) executes one arithmetic instruction across several independent values
held in vector lanes. It is the CPU-side counterpart to the data parallelism that makes GPUs effective, and it
matters whenever a workload repeatedly transforms arrays, pixels, embeddings, or numerical state.

## Why it matters

SIMD is where this vault's hardware material meets its software-performance material. The same data-parallel
argument that motivates [[GPU Execution Model]] and [[AI Accelerator Architecture]] applies one level down, on
the CPU that runs the tokenizer, the sampler, the retrieval preprocessing, and everything else around an
accelerator. For LLM systems specifically, the CPU-side work that surrounds inference is often where latency
accumulates unnoticed, and it is usually the code least likely to have been vectorized.

It is also the vault's clearest case of a technique whose headline number is a **ceiling rather than an
expectation**. Lane counts of 4, 8, or 16 describe what the instruction set offers, not what a workload will
realize, and the gap between the two is the whole discipline.

## Current synthesis

- A practical SIMD loop has five parts: broadcast scalar inputs, process vector-sized blocks, apply vector
  operations, reduce vector accumulators, then handle the scalar tail.
- Compilers can auto-vectorize simple, regular loops without complex control flow, but
  [[Mitchell Hashimoto - Everyone Should Know SIMD]] calls them "severely limited" and advises compiling the
  optimized scalar version and checking what the compiler produces before writing SIMD by hand.
  [[Jeff Dean and Sanjay Ghemawat - Performance Hints]] adds one enabling move: copying small amounts of data
  into local variables can let the compiler assume no aliasing, which may improve auto-vectorization.
  Vectorization is **conditional, not automatic**.
- Lane-count speedups are ceilings, not guarantees. Hashimoto's Ghostty loop could improve throughput by up to
  **8x** with AVX2, but measured end to end on an AVX2 Intel desktop it was "more like a **5x** speedup", the rest
  lost to "the other stuff around the SIMD code". It is a single case rather than a rate to expect, and the
  essay does not break down which surrounding work cost the difference.
- [[Jeff Dean and Sanjay Ghemawat - Performance Hints]] places SIMD inside a broader optimization hierarchy:
  first improve algorithms, avoid work, compact data, reduce allocations, and measure the hot path; then
  vectorize regular operations when data movement can sustain it. Vectorizing before the memory layout can feed
  the execution units buys nothing, which is why SIMD sits **near the end** of that ordering rather than at the
  start.

## Open questions

- **When is explicit SIMD worth its readability cost?** Hashimoto avoids CPU-specific intrinsics in favor of
  portable generic vectors, and wants vectorization explicit so that an unrelated change or compiler update
  cannot quietly turn a loop back into scalar code. Dean and Ghemawat place SIMD after algorithmic and
  data-layout work. Neither offers a threshold for when a loop matters enough.
- **How much of the CPU-side work around LLM inference is actually vectorizable?** The vault has no measurement,
  and the sources are general-purpose rather than ML-specific.
- **How should a team catch silent de-vectorization?** Hashimoto's argument for explicit code assumes the
  compiler's choices can regress unnoticed; the vault has no evidence on which checks (benchmarks,
  generated-code inspection, or compiler reports) catch that regression in practice.

## Related pages

- [[Mitchell Hashimoto - Everyone Should Know SIMD]]
- [[Jeff Dean and Sanjay Ghemawat - Performance Hints]]
- [[Software Performance Engineering]]
- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
- [[GPU Kernel Optimization]]
- [[LLM Inference]]
