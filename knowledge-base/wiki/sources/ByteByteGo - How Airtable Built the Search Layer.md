---
type: source-summary
source_id: src-2026-05-28-bytebytego-airtable-search
source_title: "How Airtable Built the Search Layer Behind Their AI Features"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-airtable-built-the-search-layer
created: 2026-05-29
updated: 2026-05-29
tags:
  - source-summary
  - vector-search
  - system-design
  - ai-infrastructure
status: active
---

# ByteByteGo - How Airtable Built the Search Layer

## Overview

This source distills Airtable's public account of the semantic search layer behind Omni and linked-record recommendations. The durable lesson is workload fit: tenant isolation, a heavily skewed hot/cold access pattern, and strict latency targets determined the partitioning model, the ANN index choice, and the memory policy more than generic vector-database feature comparisons did.

## Durable claims

1. Airtable's AI features use semantic retrieval over customer bases that can exceed 500K rows, retrieving only the most relevant rows before handing them to downstream AI features.
2. Embeddings are roughly 10x the size of the source data, which makes a dedicated vector database economically and operationally necessary.
3. Airtable chose one partition per base in Milvus because physical isolation simplifies permission boundaries and makes customer deletion a partition-drop operation, despite the operational overhead of many partitions.
4. Milvus bookkeeping degraded when a collection approached 100K partitions, so Airtable introduced hierarchical capping: 400 collections per cluster and 1,000 partitions per collection.
5. HNSW beat IVF-SQ8 and DiskANN for Airtable's workload because the product required p99 latency below 500 ms and recall above 99%.
6. Vector indexes sit on a three-way tradeoff between memory, latency, and recall; HNSW spends memory to buy latency and recall, IVF-SQ8 saves memory by accepting more approximation error, and DiskANN saves RAM by paying extra latency.
7. Airtable exploits the fact that about 75% of bases are idle in a given week by unloading cold partitions from memory and reloading them on demand.
8. Airtable self-hosts Milvus for privacy and operational control, while keeping authorization in the application layer after vector retrieval rather than inside the vector database.

## Affected pages

- [[ML Systems at Scale]]
- [[Retrieval-Augmented Generation]]
- [[Search-Augmented Language Models]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
- [[index|Knowledge Base Index]]
- [[log|Knowledge Base Log]]

## Raw capture

- `knowledge-base/raw/sources/How Airtable Built the Search Layer Behind Their AI Features.md`

## Related pages

- [[ByteByteGo]]
- [[ML Systems at Scale]]
- [[Retrieval-Augmented Generation]]
- [[Search-Augmented Language Models]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[AI Knowledge Base Overview]]
