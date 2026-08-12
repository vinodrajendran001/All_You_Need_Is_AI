---
type: concept
created: 2026-08-12
updated: 2026-08-12
tags:
  - concept
  - recommendation-systems
  - retrieval
  - embeddings
source_ids:
  - src-2026-08-12-bytebytego-semantic-feed-retrieval
  - src-2026-05-21-bytebytego-batch
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

