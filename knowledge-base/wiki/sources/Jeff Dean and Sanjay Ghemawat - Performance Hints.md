---
type: source-summary
created: 2026-08-07
updated: 2026-08-26
source_id: src-2026-08-07-dean-ghemawat-performance-hints
source_title: Performance Hints
source_author: Jeff Dean and Sanjay Ghemawat
source_url: https://abseil.io/fast/hints.html
tags:
  - source/summary
  - performance
  - systems
  - c-plus-plus
source_ids:
  - src-2026-08-07-dean-ghemawat-performance-hints
status: active
---

# Jeff Dean and Sanjay Ghemawat - Performance Hints

## Summary

Jeff Dean and Sanjay Ghemawat present a large, example-driven guide to performance engineering within a single binary. The source combines back-of-the-envelope estimation, profiling, API design, algorithmic changes, memory representation, allocation reduction, avoided work, code-size control, parallelism, synchronization, Protocol Buffers, and C++-specific container guidance. Its recurring rule is to choose a faster design when it does not materially damage clarity, then measure representative behavior before accepting complexity.

The examples are grounded in concrete Google change lists and emphasize that significant gains often come from structural changes—better algorithms, bulk APIs, compact layouts, fewer allocations, fast paths, or moved work—rather than isolated instruction-level tuning.

## Key claims

- Ignoring performance during initial design can create flat profiles where cost is distributed throughout the system and difficult to repair later.
- Rough operation-cost estimates can eliminate bad designs before implementation.
- Profiling and stable microbenchmarks are essential, but microbenchmarks must be checked against end-to-end behavior.
- Algorithmic complexity and avoiding unnecessary work generally outrank micro-optimization.
- Compact, contiguous data structures improve memory footprint, cache locality, allocator pressure, and bandwidth use.
- Bulk APIs amortize boundary crossings, locks, allocations, and repeated checks.
- Code size affects compile time, binary size, instruction-cache pressure, and branch prediction.
- Parallelism helps only when spare compute exists and memory bandwidth or contention does not become the bottleneck.

## Why it matters

The source seeds [[Software Performance Engineering]] as a bridge between algorithm design and hardware-aware execution. It also broadens [[SIMD]] from a standalone primitive into one option among measurement-led improvements in memory layout, batching, code size, and synchronization.

## Tensions / open questions

- Many examples are C++- and Google-infrastructure-specific even when the principles generalize.
- Historical operation-cost tables are intentionally approximate and need recalibration for current hardware.
- Local microbenchmark gains can worsen system-level latency, memory use, fairness, or maintenance cost.
- Several techniques trade API simplicity, portability, or safety for speed and should remain behind well-tested encapsulation boundaries.
- The guide excludes distributed-system and ML-hardware performance, both major areas for this vault.

## Affected pages

- [[Abseil]]
- [[SIMD]]
- [[Software Performance Engineering]]

## Citations

- Raw capture: [[2026-08-07 Jeff Dean and Sanjay Ghemawat - Performance Hints]]
- Canonical URL: https://abseil.io/fast/hints.html

## Raw capture

- [[2026-08-07 Jeff Dean and Sanjay Ghemawat - Performance Hints]]

## Related pages

- [[Abseil]]
- [[AI Accelerator Architecture]]
- [[LLM Inference]]
- [[GPU Execution Model]]
- [[ML Systems at Scale]]

