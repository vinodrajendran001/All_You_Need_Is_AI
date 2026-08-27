---
type: source-summary
created: 2026-08-12
updated: 2026-08-26
source_id: src-2026-08-12-bytebytego-semantic-feed-retrieval
source_title: How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-to-fight-clickbait-meta-linkedin
tags:
  - source/summary
  - recommendation-systems
  - semantic-retrieval
source_ids:
  - src-2026-08-12-bytebytego-semantic-feed-retrieval
status: active
---

# ByteByteGo - How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies

## Summary

ByteByteGo compares three large-scale attempts to reduce engagement bait by changing feed retrieval from behavioral proxies toward semantic relevance. LinkedIn consolidates multiple candidate sources into one language-model dual encoder; Meta keeps a staged funnel of specialized models and a multi-objective value function; YouTube's PLUM generates semantic item identifiers rather than querying a conventional embedding index.

The shared system shape remains retrieval followed by more expensive ranking. Semantic models reduce dependence on historical engagement and improve cold start, but they do not remove manipulation, ranking objectives, serving constraints, or the need for post-retrieval integrity controls.

## Key claims

- Engagement is a cheap relevance proxy but can be optimized directly by low-value bait.
- Dual encoders precompute item embeddings and retrieve candidates through nearest-neighbor search against a user embedding.
- LinkedIn represents structured profile, activity, and popularity features as model-legible text; bucketing raw counts improves their usefulness.
- Meta favors a multi-stage funnel so positive, negative, diversity, integrity, and creator objectives remain separately tunable.
- YouTube's PLUM tokenizes videos into semantic IDs and generates likely next-item IDs with a language model, trading index storage for invalid-ID risk.
- Semantic pretraining helps most when behavioral history is sparse, while potentially projecting stereotypes onto new users.
- Semantic retrieval weakens engagement bait but can itself be gamed through content engineered around desirable topics.

## Why it matters

The comparison seeds [[Semantic Recommendation Systems]] and extends [[ML Systems at Scale]] with three distinct production architectures: unified vector retrieval, specialized ranking funnels, and generative retrieval. It also demonstrates that feature representation and serving design can matter as much as the base model.

## Tensions / open questions

- The source synthesizes company reports rather than presenting a controlled cross-platform comparison.
- Metrics, latency, and architecture descriptions differ in scope and are not directly comparable.
- Semantic relevance is not identical to quality, truth, diversity, or user welfare.
- Generative retrieval must handle nonexistent identifiers and catalog updates.
- Consolidated systems simplify maintenance but can create larger rollback and correlated-failure domains.

## Affected pages

- [[ByteByteGo]]
- [[ML Systems at Scale]]
- [[Semantic Recommendation Systems]]

## Citations

- Raw capture: [[2026-08-12 ByteByteGo - How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies]]
- Canonical URL: https://blog.bytebytego.com/p/how-to-fight-clickbait-meta-linkedin

## Raw capture

- [[2026-08-12 ByteByteGo - How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies]]

## Related pages

- [[ByteByteGo]]
- [[Retrieval-Augmented Generation]]
- [[Model Factory]]
- [[Model Routing]]
- [[Small Language Models]]

