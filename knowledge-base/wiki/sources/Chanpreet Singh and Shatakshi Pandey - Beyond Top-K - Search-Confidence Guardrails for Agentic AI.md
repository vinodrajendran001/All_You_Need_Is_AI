---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-16-opensearch-beyond-top-k
source_title: "Beyond Top-K: Building search-confidence guardrails for agentic AI with OpenSearch"
source_author: Chanpreet Singh and Shatakshi Pandey
source_url: https://opensearch.org/blog/beyond-top-k-building-search-confidence-guardrails-for-agentic-ai-with-opensearch/
tags: [source/summary, rag, retrieval, abstention, guardrails, ai-agents]
source_ids:
  - src-2026-10-16-opensearch-beyond-top-k
status: active
---

# Chanpreet Singh and Shatakshi Pandey - Beyond Top-K - Search-Confidence Guardrails for Agentic AI

## Summary

An OpenSearch project blog post by Chanpreet Singh and Shatakshi Pandey, published 16 October 2026.
Its argument is that an agent acting on retrieval results needs a signal for "none of what I
retrieved is good enough to act on", and that Top-K retrieval does not supply one. Better retrieval,
meaning hybrid search, Reciprocal Rank Fusion (RRF), cross-encoder reranking, or OpenSearch's own
agentic search, improves ranking or query generation. It does not tell the agent when to stop.

The proposal is a *confidence layer* in the agent's orchestration code, between retrieval and
action. It has three steps. **Quantify** a composite confidence from five signals. **Threshold** it
by query type and action intent. **Abstain** on a graduated ladder: act, caveat, clarify, escalate,
or hard abstain. The authors call the post "a conceptual deep dive with illustrative code". Every
weight, threshold, and example outcome is a starting point or computed from mocked scores, not a
measurement.

## Key claims

**Raw retrieval scores are not a trust signal.** The post gives three reasons:

- Scales differ across methods. BM25 scores are "theoretically unbounded and in practice commonly
  fall in the 0 to 15 range", while L2 distance for vector search sits between 0 and 1.
- Scores are not comparable across queries. A BM25 score of 8.5 on one query does not mean the same
  relevance as 8.5 on another.
- There is no "I don't know" signal. For vector (k-NN) queries, Top-K returns K results by
  construction. For BM25, an irrelevant query returns no hits or very low scores, and "a
  low-but-nonzero score is easy to mistake for a usable answer".

The motivating case is hypothetical. An internal knowledge agent asked "how to rotate API keys in
production" treats the top-ranked document as ground truth, follows a deprecated 2022 runbook, and
causes a production incident.

**Better ranking does not supply confidence.** Min-max normalization rescales scores against the
returned candidate set, so a high top score means a document is "the best of that set", not that it
is relevant. With a single hybrid clause the top hit is always 1.0. The gap to the second hit
depends on how many hits came back: two hits might score `[1.0, 0.001]`, a gap of 0.999, while
three might score `[1.0, 0.5, 0.001]`, a gap of 0.5. RRF discards score information entirely. A
cross-encoder logit "is designed for ordering, not calibrated confidence". Agentic search plans and
runs a query well but still returns whatever that query matches.

**Quantify: five signals, three of them from outside the retrieval scores.**

| Signal | Weight | Source of the signal |
| --- | --- | --- |
| Score magnitude (top normalized score) | 0.35 | Retrieval scores; weak on its own under min-max |
| Score gap (first minus second) | 0.25 | Retrieval scores; compare only within one technique |
| Result coherence | 0.20 | Agent layer, for example embedding agreement among top hits |
| Freshness | 0.10 | An indexed field such as a `last_updated` timestamp |
| Source authority | 0.10 | An index-time field (`source_type` or `authority`) or a metadata-aware reranker |

"The weights above are a starting point; tune them against a judged query set for your corpus".
For non-hybrid queries, `script_score` can also fold authority and freshness into ranking.

**Threshold: the boundary depends on what the agent is about to do.**

| Query type | Intent | Threshold |
| --- | --- | --- |
| Factual lookup | read only | 0.75 |
| Factual lookup | execute action | 0.90 |
| Exploratory | read only | 0.50 |
| Exploratory | execute action | 0.70 |
| Troubleshooting | execute action | 0.85 |

Unlisted combinations default to 0.75 in the sample code. The authors tell readers to derive the
values empirically. Sweep candidate thresholds over a judged query set and choose one per cell, for
example by maximizing F1 or by holding false acts under a target rate. Revisit the values as the
corpus and traffic shift, or derive the boundary from each result set's score distribution.

In recent OpenSearch versions, `min_score` applies to hybrid queries after normalization, so the
floor can be enforced at query time. It stops applying when a `sort` clause is added, and older
clusters do not support it, so in those cases the threshold has to live in the orchestration layer.

**Abstain: a ladder keyed to the margin.** The margin is confidence minus threshold.

| Margin | Response |
| --- | --- |
| 0 or more | Act |
| above -0.05 | Caveat: answer and flag the uncertainty |
| above -0.15 | Clarify: ask a narrowing question |
| above -0.25 | Escalate: route to a human |
| lower | Hard abstain |

The authors assert, without measuring it, that the ladder "prevents cascading hallucinations at the
source, because the agent stops before building further reasoning on a weak retrieval".

**The worked example is mocked.** A property-management assistant searches four indexes (leases,
work orders, properties, tenants) and is run on five queries. Its confidence values are "computed
from mocked retrieval scores":

- A lookup of a lease's early termination clause acts, at confidence 0.85 and margin +0.10.
- A bulk suspension of tenants who defaulted on rent escalates to a leasing manager.
- Auto-closing resolved HVAC tickets answers, but flags the 4 of 12 tickets with pending follow-ups.
- A vague request to send renewal offers asks which occupancy level and area were meant.
- A restaurant question hard-abstains as off-domain.

The unguarded column shows what an agent without the layer would do, by construction of the
example rather than by observation.

## Why it matters

[[Retrieval-Augmented Generation]] recorded that its failure-mode source gave no guidance on
retrieval thresholds. That left open which retrieval-time signal could flag a result set as
insufficient. This post proposes one: score shape plus indexed metadata, not the model's own
confidence. Freshness is aimed directly at the retired-policy failure that page already describes.

[[LLM Application Resilience]] gets a graded version of its *needs review* third state. The ladder
is keyed to a margin computed outside the model, and the threshold rises with the stakes of the
action, not only with the type of question.

## Tensions / open questions

- **Nothing is measured.** The weights, thresholds, ladder cut points, and all five example
  outcomes are illustrative. The post does not test whether the composite score separates queries
  that should act from those that should abstain.
- **The composite is not a probability.** It mixes a technique-dependent magnitude, which is always
  1.0 for a single-clause min-max top hit, with a gap whose size depends on the hit count. Weighting
  them 0.35 and 0.25 does not make 0.75 a calibrated confidence. The authors' own remedy is tuning
  against a judged query set.
- **Three signals are only as good as the metadata.** Authority has to be populated at index time.
  A missing or wrong `last_updated` field defeats the deprecated-runbook defense.
- **Query type and intent must be classified first, and the post does not say how.** Misreading an
  executing action as a read lowers the bar, for example from 0.90 to 0.75 for a factual lookup.
- **Vendor framing.** It is an OpenSearch project post built around OpenSearch primitives, although
  it places the confidence and abstention logic in the agent's orchestration layer, outside OpenSearch.
- **Version-dependent features.** z-score normalization is available on self-managed OpenSearch,
  while managed offerings such as Amazon OpenSearch Serverless support min-max and L2. The
  normalization processor dates from OpenSearch 2.10. Agentic search has been generally available
  since 3.2, and Amazon OpenSearch Service supports it from 3.3. Post-normalization `min_score` was
  added after the first hybrid query release.

## Affected pages

- [[Retrieval-Augmented Generation]]
- [[LLM Application Resilience]]

## Raw capture

- [[Beyond Top-K Building search-confidence guardrails for agentic AI with OpenSearch]]

## Citations

- Canonical URL:
  https://opensearch.org/blog/beyond-top-k-building-search-confidence-guardrails-for-agentic-ai-with-opensearch/
  (email tracking parameters removed).
- Published 16 October 2026; authors from the clipping's frontmatter. The code blocks are the
  post's illustrative snippets and none were run during this ingest.

## Related pages

- [[Retrieval-Augmented Generation]]
- [[LLM Application Resilience]]
- [[ByteByteGo - Why Do LLMs Lie]]
- [[Approximate Nearest-Neighbor Search]]
- [[Search-Augmented Language Models]]
- [[LLM-as-a-Judge]]
- [[Agent Security and Governance]]
- [[Institutional Knowledge Agents]]
- [[AI Knowledge Base Overview]]
