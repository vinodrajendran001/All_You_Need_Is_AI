---
type: concept
created: 2026-09-03
updated: 2026-09-11
tags:
  - concept
  - rag
  - retrieval
  - embeddings
source_ids:
  - src-2026-09-02-bytebytego-rag-embedding-model
  - src-2026-09-09-bytebytego-model-routing
  - src-2026-09-08-raji-cosine-similarity-safety
status: active
---

# Embedding Model Selection

## Definition

The embedding model is the component that turns documents and queries into vectors. Because retrieval compares
those vectors, the embedding model — not the generator — determines **what the language model ever gets to
see**. [[ByteByteGo - Why Your RAG System Is Only as Good as Its Translator Model]] calls it the "translator"
and states the consequence plainly: **"A better language model cannot repair bad retrieval."**

## Why it matters

The vault's [[Retrieval-Augmented Generation]] page is organised by **architecture** — classic, graph and
agentic tiers. This page covers the layer beneath all three: whatever the architecture, retrieval quality is
bounded by the geometry of the embedding space. Agentic RAG's ability to reformulate and re-query is a real
advantage, but it cannot find a passage that no phrasing of the query brings close.

The selection decision also behaves unlike other component choices, because it is **not swappable**. See
below.

## Where embedding similarity and relevance diverge

Seven characteristic failure modes, each a case where surface similarity and semantic relevance come apart:

1. **Similar subject, different question** — the topic matches, the information need does not.
2. **Same words, different entity.**
3. **Negation** — "you can delete this" and "you cannot delete this" embed close together.
4. **Versions and dates.**
5. **Numerical identifiers** — a 30-day policy and a 60-day policy look nearly identical.
6. **Domain-specific meanings** of ordinary words.
7. **Multi-part questions**, where one vector must stand for several information needs.

Numbers three and five deserve separate weight. Both retrieve a document that is **topically perfect and
factually inverted**, so the generator produces a confident, fluent, wrong answer rather than an obviously
empty one. They are also the failures most likely to be caught by lexical matching, which strengthens the case
for hybrid retrieval already noted on [[Retrieval-Augmented Generation]] and [[Direct Corpus Interaction]].

A plausible unifying reading is that embeddings encode **topic** far more strongly than they encode
**logical operators and identifiers**, and most of the seven are consequences of that one property.

## Selection criteria are mostly not about semantics

Domain vocabulary, language support, dimension count, maximum input length, inference speed, and deployment
mode. Only the first is about meaning; the rest are systems constraints. Maximum input length in particular
couples the embedding choice to the chunking strategy, so the two cannot be decided independently.

## Migration is a one-way door

Every embedding model defines **its own vector space**. Queries embedded by a new model cannot be compared
against vectors written by an old one, so adopting a better embedding model requires **re-embedding the entire
corpus**. The recommended pattern is **blue-green**: build the new index alongside the old, cut over, retain
rollback.

This is why embedding selection is a **schema decision rather than a component choice**, and why treating it
as swappable is how teams end up unable to adopt a better model later. The practical mitigation is provenance:
record model name, version, dimension, query-versus-passage format, normalization, chunking version, and
creation time. An index without these cannot be safely reasoned about once the people who built it move on —
the same argument [[Schema-Driven Knowledge Base]] makes for structured knowledge generally.

## Matryoshka embeddings, and their limit

Matryoshka embeddings are trained so that **prefixes** of the vector are independently useful, typically at
256, 512, 1024 and full dimensions. Three storage designs follow: store only the short vector; store the full
vector with a short-vector search index; or two-stage retrieval that shortlists on the prefix and re-ranks on
the full vector.

The limit is worth stating explicitly because the truncation trick is easy to mistake for portability:
**Matryoshka gives flexibility within one model's space only.** It does nothing for cross-model
incompatibility, and the migration cost above is unchanged.

## Embeddings determine intent reliably and difficulty unreliably

[[ByteByteGo - How Smart Model Routing Can Cut LLM Costs by 10X]] flags a limit on semantic routing worth generalising: embedding the request and
comparing it against clusters of past requests "is helpful for determining intent. However, it is not
always reliable for determining difficulty because two requests can look similar in wording but differ in
reasoning requirements."

That is a statement about what the embedding space encodes. Surface form and topic are captured;
computational depth is not, because nothing in the training objective makes reasoning difficulty a
geometric property. Selecting a better embedding model does not fix this — it is a category limit, not a
quality one. See [[Model Routing]].

## The embedding model version is a security parameter

[[Amine Raji - Cosine Similarity Is Not a Safety Property]] adds a selection criterion that has nothing to do with retrieval quality. Because
**"cosine similarity measures an angle"** with "no notion of truth, authority or provenance", the
retriever offers no integrity guarantee, and the defences that do work are calibrated against the specific
embedding model in use.

Three consequences for model selection.

**Thresholds are model properties.** The ingestion-time poisoning detectors that took attack success from
95% to 20% — nearest-neighbour similarity above **0.85**, batch pairwise similarity above **0.90** — are
explicitly stated to be **"properties of your embedding model, not of your data."** The prescription is to
baseline your own corpus and set the threshold at mean + 2 standard deviations.

**Pinning the version becomes a control.** An embedding model upgrade invalidates every calibrated
threshold simultaneously, so a routine dependency bump is a security event.

**Distance metric defaults are a trap.** ChromaDB's default is **squared L2, not cosine**; cosine must be
requested with `metadata={"hnsw:space": "cosine"}`. An application built on the default is not measuring
what its authors believe.

And the stored vectors are not inert. Vec2Text recovered **92% of 32-token inputs exactly**, and ALGEN
reduced inversion to a one-step linear map needing roughly 1,000 aligned pairs, with **no tested defence
effective** — so the choice of embedding model also determines what a compromised store discloses. See
[[Embedding Inversion]] and [[Retrieval Poisoning]].

## Open questions

- The source is an explainer with **no benchmarks** and names no models, so none of the seven failure modes is
  quantified and no selection is empirically grounded.
- Re-ranking is the cheaper first response to several of these failures and is not discussed at all. When is
  a better re-ranker preferable to a better embedding model?
- When is a migration worth its cost? The source gives the mechanism and not the threshold.
- Are the seven modes independent failures or one failure — topic dominance — seen seven ways?
- Do the identifier and negation failures survive in current large embedding models, or are they artifacts of
  smaller ones?

## Related pages

- [[ByteByteGo - Why Your RAG System Is Only as Good as Its Translator Model]]
- [[Retrieval-Augmented Generation]]
- [[Search-Augmented Language Models]]
- [[Direct Corpus Interaction]]
- [[Semantic Recommendation Systems]]
- [[Graph Engineering]]
- [[Agent Memory]]
- [[Context Engineering]]
- [[Schema-Driven Knowledge Base]]
- [[Model Quantization and Efficiency]]
- [[ByteByteGo - How Smart Model Routing Can Cut LLM Costs by 10X]]
- [[Model Routing]]
- [[ByteByteGo]]
- [[Amine Raji - Cosine Similarity Is Not a Safety Property]]
- [[Embedding Inversion]]
- [[Retrieval Poisoning]]
- [[Amine Raji]]
