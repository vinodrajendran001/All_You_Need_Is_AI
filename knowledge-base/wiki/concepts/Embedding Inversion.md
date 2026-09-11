---
type: concept
created: 2026-09-11
updated: 2026-09-11
tags:
  - concept
  - topic/security
  - topic/embeddings
source_ids:
  - src-2026-09-08-raji-cosine-similarity-safety
status: active
---

# Embedding Inversion

## Definition

Recovering the original text from a stored embedding vector. The practical consequence is a
reclassification: a compromised vector store is **not a metadata leak, it is a partial document leak**.
Organisations that treat embeddings as an opaque numeric derivative — and therefore as lower-sensitivity
than the documents they came from — are holding a threat model that the published attacks have already
invalidated.

## Why it matters

The reclassification is free and the timing is the whole argument. Changing a threat-model entry before
an incident costs nothing; doing it afterwards is an incident report.

Vector stores are routinely given weaker controls than document stores: replicated to analytics
environments, shared across tenants, backed up with looser retention, and excluded from
data-classification reviews on the grounds that they contain "just numbers." Every one of those decisions
assumes inversion is impractical. It is not, and the cost of the attack has fallen by roughly three
orders of magnitude in two years.

This is the second attack surface on the same store documented in
[[Amine Raji - Cosine Similarity Is Not a Safety Property]], and it runs in the opposite direction from
[[Retrieval Poisoning]]: poisoning inserts text to be retrieved, inversion extracts text that was already
stored.

## Current synthesis

**The feasibility result (2023).** Morris, Kuleshov, Shmatikov and Rush, *Text Embeddings Reveal (Almost)
As Much As Text* (EMNLP 2023), introduced **Vec2Text**, which **recovered 92% of 32-token inputs
exactly**. Chen, Lent and Bjerva (ACL 2024) extended inversion to the multilingual setting.

**The cost result (2025), which is the one that changes decisions.** **ALGEN** (Chen, Xu and Bjerva,
February 2025) learns a **one-step linear map** from the target embedding space into a decoder's space.
**A single aligned pair already gives partial success, and roughly 1,000 pairs reach optimum.** Reported
quality is ROUGE-L up to ~46 in the cross-encoder setting against a low-fifties monolingual upper bound,
with cosine similarity around 0.95, and **no tested defence was effective**. Raji's reading is the right
emphasis: **ALGEN's contribution is *cost*** — not that inversion became possible, but that it became
cheap enough to assume. **LAGO** (May 2025) adds a further 10–20% ROUGE-L with as few as ten samples per
language.

**What follows operationally.** First, the free move: reclassify vector store compromise as partial
document disclosure, and let retention, replication, access review and breach-notification policy follow
from that classification rather than from "numeric derivative." Second, the paid move: evaluate
per-tenant vector encryption — IronCore's Cloaked AI is the named example — which is the only control
that addresses the stored representation itself rather than the perimeter around it.

**The structural control does double duty.** Access-controlled retrieval, filtering at query time on
classification metadata, is the only complete defence against cross-tenant leakage through the query
interface, and it is also the primary structural defence against poisoning. It does not, however, protect
a store that has already been exfiltrated — that is what encryption is for.

Catalogued with poisoning under OWASP **LLM08:2025 Vector and Embedding Weaknesses**.

## Open questions

- Published results are on short inputs — Vec2Text at 32 tokens. How much of a long chunked document is
  recoverable in practice is not established.
- "No tested defence was effective" is a claim about the defences tested as of early 2025, not a proof of
  impossibility. Noise injection, dimensionality reduction and quantisation are obvious candidates whose
  cost in retrieval quality is unmeasured here.
- Per-tenant vector encryption trades against approximate-nearest-neighbour performance; that cost is
  named as a thing to evaluate rather than quantified.
- The interaction with [[Model Quantization and Efficiency]] is unexplored: whether a heavily quantised
  or rotated embedding is meaningfully harder to invert.
- Nothing addresses inversion of *embeddings in transit* to a hosted embedding provider, which is a
  different exposure from a compromised store.

## Related pages

- [[Retrieval Poisoning]]
- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Agent Security and Governance]]
- [[Reasoning Trace Privacy]]
- [[Model Quantization and Efficiency]]
- [[Amine Raji - Cosine Similarity Is Not a Safety Property]]
