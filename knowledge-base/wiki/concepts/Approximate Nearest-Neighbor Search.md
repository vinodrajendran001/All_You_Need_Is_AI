---
type: concept
created: 2026-09-18
updated: 2026-11-27
tags: [concept, retrieval, vector-search, ann]
source_ids:
  - src-2026-09-16-bytebytego-needle-haystack-retrieval
  - src-2026-11-23-alphasignal-e-means-rag
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

## Building an IVF index is a clustering job, and its cost sets how often it is rebuilt

The IVF bullet above leaves the build step implicit. The groups an IVF index probes are clusters,
each represented by a centroid, and the centroids come from k-means over the stored embeddings.
[[Alpha Signal - RAG Gets a 70-Year Upgrade with Meta's e-means Algorithm]] puts a price on that step.
RAG corpora reach millions of chunks with embeddings of up to **3,072** values, split into "tens of
thousands of clusters", and Lloyd's k-means makes **20-25** full passes over every vector. Teams
therefore postpone rebuilds. Appended vectors are then assigned to centroids that no longer describe
the corpus, clusters grow lopsided, and the newsletter says latency rises and recall falls. This
failure belongs to the index-recall layer above, not to evidence relevance: every document can be
current while the partition over them is stale.

The relayed remedy is **e-means**, credited to researchers at Meta FAIR and École nationale des
ponts et chaussées and shipped in Faiss 1.16.0. It is mini-batch k-means with centroids updated as
exponential moving averages, batch and step sizes set by derived rules, and empty clusters revived
by splitting large ones. Across **24** benchmarks it reportedly beats a Lloyd baseline in roughly
**one-tenth the passes**, and runs **10-45X** faster than Flash-KMeans on GPUs and **8-15X** faster
than Faiss on CPUs. On an H100 with **10 million** vectors and **65,536** clusters, 25 epochs of
plain PyTorch Lloyd take **142 to 155 seconds** and Flash-KMeans **14 to 22 seconds**. No absolute
e-means time is given. Reclustering leaves the embeddings and query-time search untouched, so a
cheaper build makes regular IVF rebuilds practical. The same centroid-first search also appears
inside attention, where Latent Sparse Attention clusters cached keys ([[Sparse Attention]]).

Three limits matter here. The clustering "accuracy" metric is unnamed, and no recall or latency is
reported for indexes built this way, so faster rebuilds are not yet shown to improve ANN recall.
The method applies to cluster-based indexes. HNSW builds a proximity graph rather than k-means
centroids, so in the vault's reading the HNSW controls above are unaffected. Finally, it rebuilds
static snapshots rather than handling streaming updates, and managed vector databases that hide
clustering inside the storage engine cannot adopt it.

## Open questions

- How should ANN recall targets change for high-risk or versioned corpora?
- When should metadata filters run before graph traversal versus after candidate generation?
- How should index rebuild cost and update freshness enter retrieval benchmarks? The e-means relay
  above prices the clustering side of a rebuild but measures no recall or latency for the rebuilt
  index, so the benchmark side remains open.
- How fast do IVF centroids drift on a changing corpus, and at what point does drift justify a
  rebuild?
- Which abstention test distinguishes "nearest available" from "evidence sufficient to answer"? [[Retrieval-Augmented Generation]] records one proposal: a composite of score shape and metadata checked against a stakes-keyed threshold, with illustrative rather than measured outcomes.

## Related pages

- [[ByteByteGo - How LLMs Can Find a Needle in a Haystack]]
- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Search-Augmented Language Models]]
- [[Serving Benchmarks and Goodput]]
- [[Alpha Signal - RAG Gets a 70-Year Upgrade with Meta's e-means Algorithm]]
- [[Meta]]
- [[Sparse Attention]]
