---
type: concept
created: 2026-08-03
updated: 2026-08-07
tags: [concept, hardware, performance]
source_ids:
  - src-2026-07-22-mitchell-hashimoto-simd
  - src-2026-08-07-dean-ghemawat-performance-hints
status: active
---

# SIMD

Single instruction, multiple data (SIMD) executes one arithmetic instruction across several independent values held in vector lanes. It is the CPU-side counterpart to the data parallelism that makes GPUs effective, and it matters whenever a workload repeatedly transforms arrays, pixels, embeddings, or numerical state.

## Current synthesis

- A practical SIMD loop has five parts: broadcast scalar inputs, process vector-sized blocks, apply vector operations, reduce vector accumulators, then handle the scalar tail.
- Compilers may auto-vectorize, but loop-carried dependencies, aliasing, control flow, and missed target flags can prevent it. Inspecting generated assembly or vectorization reports is therefore part of performance engineering.
- Lane-count speedups are ceilings, not guarantees: memory bandwidth, reductions, packing, and scalar remainder work can dominate.
- [[Jeff Dean and Sanjay Ghemawat - Performance Hints]] places SIMD inside a broader optimization hierarchy: first improve algorithms, avoid work, compact data, reduce allocations, and measure the hot path; then vectorize regular operations when data movement can sustain it.

## Related pages

- [[Mitchell Hashimoto - Everyone Should Know SIMD]]
- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
- [[LLM Inference]]
- [[Software Performance Engineering]]
- [[Jeff Dean and Sanjay Ghemawat - Performance Hints]]
