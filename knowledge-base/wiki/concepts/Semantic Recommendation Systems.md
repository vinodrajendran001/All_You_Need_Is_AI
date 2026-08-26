---
type: concept
created: 2026-08-12
updated: 2026-08-26
tags:
  - concept
  - recommendation-systems
  - retrieval
  - embeddings
source_ids:
  - src-2026-08-12-bytebytego-semantic-feed-retrieval
  - src-2026-05-21-bytebytego-batch
  - src-2026-07-28-bytebytego-delivery-llm-search
status: active
---

# Semantic Recommendation Systems

## Definition

Semantic recommendation systems retrieve or generate candidate items using representations of content meaning and user interests rather than relying only on historical engagement or collaborative behavior.

## Why it matters

Behavioral engagement is scalable but easy to game and weak during cold start. Semantic models can connect users and items before interaction history exists, retrieve long-tail content, and encode topic relationships that surface matching cannot capture.

## Current synthesis

### Shared two-stage shape

Large feeds usually separate:

1. **retrieval**, which cheaply narrows an enormous corpus;
2. **ranking**, which spends more compute on the survivors.

Semantic retrieval changes candidate generation but does not remove ranking, integrity, diversity, or policy objectives.

### Three production architectures

[[ByteByteGo - How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies]] compares:

- **Unified dual-encoder retrieval:** LinkedIn maps member and post representations into one embedding space and uses nearest-neighbor search.
- **Specialized ranking funnel:** Meta progressively applies more expensive models while keeping objectives separately tunable.
- **Generative retrieval:** YouTube PLUM generates content-derived semantic IDs, reducing reliance on a large item embedding table while introducing invalid-ID and catalog-update problems.

### Representation is part of the model

Structured features must be encoded in forms the model can use. Raw popularity counts may be meaningless tokens; ranked buckets, temporal sequences, and model-legible metadata can substantially change retrieval quality.

### Proxy replacement is not objective alignment

Moving from engagement to semantics reduces one class of gaming but does not make relevance equal quality. Semantic systems can amplify stereotypes during cold start, reward topic-shaped bait, or consolidate several failure modes into one model.

## Three production answers to the same question

[[ByteByteGo - Three LLM Search Architectures for Delivery Platforms]] is a useful control on this page's enthusiasm, because it shows three large marketplaces adding LLMs to search and arriving at three different architectures — none of which replaces the retrieval stack:

- **DoorDash** constrains LLM query parsing to its existing taxonomy, so the model resolves ambiguity but cannot invent categories the catalog does not have.
- **Instacart** pairs cached contextual query rewriting for head traffic with online handling for the long tail, spending model calls only where caching cannot reach.
- **Uber Eats** fine-tunes LLM embeddings and serves them through two-tower ANN retrieval — the dual-encoder shape described above, with the encoder upgraded rather than the architecture replaced.

The durable pattern is **LLM augmentation under product constraints**: use the model where it resolves ambiguity or representation mismatch, keep deterministic catalogs and rankers, and let traffic distribution, latency budget, and available training data pick the design. That there is no single right answer here is the finding, not a gap in the reporting. See [[DoorDash]] and [[Retrieval-Augmented Generation]].

## Open questions

- How should semantic relevance be balanced against quality, novelty, diversity, integrity, and creator fairness?
- When does one unified retriever outperform a redundant family of specialist systems operationally?
- How can generative recommenders guarantee valid, fresh, and policy-compliant item IDs?
- Which cold-start inferences are useful personalization versus unjustified stereotyping?

## Related pages

- [[ML Systems at Scale]]
- [[Retrieval-Augmented Generation]]
- [[Model Routing]]
- [[Model Factory]]
- [[ByteByteGo]]
- [[ByteByteGo - How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies]]
- [[ByteByteGo - Three LLM Search Architectures for Delivery Platforms]]
- [[DoorDash]]
