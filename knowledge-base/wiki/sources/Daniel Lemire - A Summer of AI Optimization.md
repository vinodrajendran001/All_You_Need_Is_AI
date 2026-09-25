---
type: source-summary
created: 2026-09-25
updated: 2026-09-25
source_id: src-2026-09-22-lemire-summer-ai-optimization
source_title: "A summer of AI optimization"
source_author: Daniel Lemire
source_url: https://lemire.me/blog/2026/09/22/a-summer-of-ai-optimization/
tags: [source/summary, performance-engineering, ai-assisted-development]
source_ids: [src-2026-09-22-lemire-summer-ai-optimization]
status: active
---

# Daniel Lemire - A Summer of AI Optimization

## Summary

Daniel Lemire reports a burst of AI-assisted optimization across six mature open-source libraries.
The durable result is not a novel optimization technique but a lower cost of trying, measuring, and
discarding known techniques in codebases where each remaining gain had previously required days.

## Key claims

- On one Intel Xeon Gold 6548N, ada URL throughput rose from **0.54 to 1.28 GB/s** after roughly 550
  flat commits and then six weeks of work, reaching about **15 million URLs/s/core**.
- Reported gains include roaring iterators at **4.5-5.9x**, fast_float at **+43% to +70%** on two
  files, simdutf ASCII validation at **83 to 160 GB/s**, and CRoaring cardinality at **4.9x**.
- simdjson serialization improved **1.6x-2.1x** on two files while instructions per byte on one fell
  from **6.1 to 3.1**.
- Lemire says the techniques were already known; AI made more optimization experiments affordable.

## Why it matters

AI coding tools can change the search economics of performance engineering even when they contribute
no new systems idea. The unit of evidence remains a benchmarked commit on a named workload.

## Tensions and caveats

This is the maintainer's own reconstruction on one CPU. Results are library- and dataset-specific,
there is no control group or cost accounting, and Lemire says he cannot isolate how much AI caused
each gain. He also discloses advising perfloop, which contributed to one library.

## Raw capture

- [[2026-09-22 Daniel Lemire - A Summer of AI Optimization]]

## Affected pages

- [[Software Performance Engineering]]
- [[GPU Kernel Optimization]]

## Related pages

- [[AI-Generated Kernels]]
- [[Serving Benchmarks and Goodput]]
- [[SIMD]]
