---
type: concept
created: 2026-09-18
updated: 2026-09-18
tags: [concept, retrieval, vector-search, ann]
source_ids:
  - src-2026-09-16-bytebytego-needle-haystack-retrieval
status: active
---

# Approximate Nearest-Neighbor Search

## Definition

Approximate nearest-neighbor (ANN) search reduces the number of vector comparisons needed to retrieve
similar items from a large collection, accepting a tunable risk of missing the exact nearest vectors.

## Why it matters

Flat search scales roughly linearly with collection size. ANN indexes make retrieval practical at
scale, but introduce a second quality boundary: index recall can fail before the generator sees any
evidence. The nearest vector can also be irrelevant, obsolete, or contradictory even when search is
mathematically exact.

## Current synthesis

[[ByteByteGo - How LLMs Can Find a Needle in a Haystack]] contrasts two common families:

- **IVF** clusters vectors and probes selected groups. More probes improve recall at higher cost.
- **HNSW** navigates a multilayer proximity graph. `M` controls connectivity, `ef_construction`
  controls build effort, and `ef_search` controls query breadth.

ANN tuning and evidence tuning are different. Search recall asks whether the index recovered the
neighbors the metric defines. Evidence relevance asks whether those neighbors are current, complete,
authorized, and sufficient for the user's question. Metadata filters, stable identifiers, active
version rules, hybrid lexical/vector retrieval, reranking, and abstention operate after or around the
index to close that gap.

The source's million-document IVF and 30-candidate reranking examples are explanatory, not benchmark
results. They establish the mechanics but not a recommended operating point.

## Open questions

- How should ANN recall targets change for high-risk or versioned corpora?
- When should metadata filters run before graph traversal versus after candidate generation?
- How should index rebuild cost and update freshness enter retrieval benchmarks?
- Which abstention test distinguishes "nearest available" from "evidence sufficient to answer"?

## Related pages

- [[ByteByteGo - How LLMs Can Find a Needle in a Haystack]]
- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Search-Augmented Language Models]]
- [[Serving Benchmarks and Goodput]]

