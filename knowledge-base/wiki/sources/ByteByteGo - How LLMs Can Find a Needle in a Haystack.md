---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-16-bytebytego-needle-haystack-retrieval
source_title: "How LLMs Can Find a Needle in a Haystack"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-llms-can-find-a-needle-in-a-haystack
tags: [source/summary, retrieval, vector-search, ann]
source_ids: [src-2026-09-16-bytebytego-needle-haystack-retrieval]
status: active
---

# ByteByteGo - How LLMs Can Find a Needle in a Haystack

## Summary

This retrieval tutorial separates vector proximity from usable evidence. It covers semantic chunking,
embedding compatibility, exact flat search, IVF and HNSW approximate indexes, metadata filtering,
version rules, hybrid lexical/vector retrieval, reranking, and abstention when the nearest passages
still do not answer the question.

## Key claims

- Flat search performs roughly O(n) distance comparisons and returns exact neighbors under a metric,
  not necessarily factually suitable evidence.
- In an illustrative million-passage IVF index with 1,000 groups, probing 10 groups examines about
  10,000 passages before overhead and imbalance.
- HNSW's `M`, `ef_construction`, and `ef_search` independently control connectivity, build effort,
  and query effort; requested result count is not search breadth.
- Version metadata prevents obsolete and current policies from being retrieved together.
- A practical pipeline can retrieve 30 candidates, then rerank to a smaller evidence set.

## Why it matters

ANN recall and answer relevance are separate measurements. Every collection has a nearest vector, so
retrieval needs filters, reranking, provenance, and an explicit no-answer path.

## Tensions and caveats

All numbers are educational examples. The article reports no measured latency, recall, corpus quality,
index maintenance cost, or downstream answer accuracy.

## Raw capture

- [[2026-09-16 ByteByteGo - How LLMs Can Find a Needle in a Haystack]]

## Affected pages

- [[Approximate Nearest-Neighbor Search]]
- [[Retrieval-Augmented Generation]]
- [[ByteByteGo]]

## Related pages

- [[Embedding Model Selection]]
- [[Search-Augmented Language Models]]

