---
type: concept
created: 2026-08-03
updated: 2026-09-04
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
- Compilers may auto-vectorize, but loop-carried dependencies, aliasing, control flow, and missed target flags
  can prevent it. Inspecting generated assembly or vectorization reports is therefore part of performance
  engineering rather than an optional extra — vectorization is **conditional, not automatic**.
- Lane-count speedups are ceilings, not guarantees: memory bandwidth, reductions, packing, and scalar remainder
  work can dominate. [[Mitchell Hashimoto - Everyone Should Know SIMD]] reports a **fivefold speedup on one
  workload** after explicit SIMD-oriented restructuring — well short of the nominal lane count, and offered as a
  single case rather than a rate to expect.
- [[Jeff Dean and Sanjay Ghemawat - Performance Hints]] places SIMD inside a broader optimization hierarchy:
  first improve algorithms, avoid work, compact data, reduce allocations, and measure the hot path; then
  vectorize regular operations when data movement can sustain it. Vectorizing before the memory layout can feed
  the execution units buys nothing, which is why SIMD sits **near the end** of that ordering rather than at the
  start.

## Open questions

- **When is hand-written SIMD worth its portability cost?** Both sources treat intrinsics as a hot-path-only
  tool, but neither offers a threshold, and the readability and cross-architecture costs are real.
- **How much of the CPU-side work around LLM inference is actually vectorizable?** The vault has no measurement,
  and the sources are general-purpose rather than ML-specific.
- **What replaces assembly inspection as compilers improve?** The advice to read generated code assumes the
  compiler cannot be trusted to report its own decisions; whether vectorization reports are now sufficient is
  untested here.

## Related pages

- [[Mitchell Hashimoto - Everyone Should Know SIMD]]
- [[Jeff Dean and Sanjay Ghemawat - Performance Hints]]
- [[Software Performance Engineering]]
- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
- [[GPU Kernel Optimization]]
- [[LLM Inference]]
