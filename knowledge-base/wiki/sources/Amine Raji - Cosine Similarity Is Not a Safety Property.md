---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-08-raji-cosine-similarity-safety
source_title: "Cosine Similarity Is Not a Safety Property"
source_author: Amine Raji
source_url: https://aminrj.com/posts/cosine-similarity-is-not-a-safety-property/
tags:
  - source/summary
  - security
  - rag
  - embeddings
source_ids:
  - src-2026-09-08-raji-cosine-similarity-safety
status: active
---

# Amine Raji - Cosine Similarity Is Not a Safety Property

## Summary

An attack-and-defence study of vector stores, built on one observation stated in the title and unpacked
in a sentence: **"Cosine similarity measures an angle. It has no notion of truth, authority or
provenance."** The consequence is that "Revenue was $8.3M" and "Revenue was $24.7M" occupy nearly
identical positions in embedding space — a retriever cannot prefer the true one, because truth is not a
geometric property.

Raji demonstrates two independent consequences. **Retrieval poisoning**: crafted documents win retrieval
and steer the generated answer, reproducible without gradients or white-box access. **Embedding
inversion**: a stolen vector store is not a metadata leak but a partial document leak, because published
attacks recover substantial text from stored vectors alone.

The defence section is the most useful part, because it rests on a structural argument rather than a
list of mitigations: **"The attacker's requirement is also their signature."** A poison document must be
similar to the target query and mutually reinforcing with its siblings, and both requirements are
measurable at ingestion time.

All measurements are March 2026, ChromaDB with `all-MiniLM-L6-v2` (384 dimensions) and
Qwen2.5-7B-Instruct at temperature 0.1. The author labels them "a lab reading, not a base rate."

## Key claims

**ChromaDB's default distance is squared L2, not cosine**, and cosine must be requested explicitly with
`metadata={"hnsw:space": "cosine"}`. Raji flags this because "the default is squared L2, not cosine" and
the difference silently changes what "similarity" means in an application built on the default.

**PoisonedRAG (Zou, Geng, Wang and Jia, USENIX Security 2025) injected five crafted texts into a corpus
of 2.6 million and drove attacker-chosen answers above 90% success**, using gradient optimisation
against the embedding model.

**The cheap version works nearly as well.** Vocabulary engineering — reusing query terminology, adding
plausible specifics, and writing three mutually corroborating fake documents (a CFO correction, a
restatement notice, board minutes) — reached **95% success against an undefended pipeline**. No
gradients, no white-box access. Raji states the base immediately: "twenty runs against a small seeded
corpus with one embedding model and one generation model. That is a lab reading, not a base rate."

**Corroboration works by crowding, not by outranking.** Three fake documents "crowd out the single true
document in a top-3 retrieval" — and critically, "in my own measurements the legitimate document was
often retrieved *and still lost*." Retrieval quality is not the defence people assume it is.

**An attack needs two conditions, and they are separable.** The *retrieval condition* (the poison must
be retrieved) and the *generation condition* (the model must prefer it once retrieved). Defences that
only address one leave the other intact.

**Architecture matters more than retrieval tuning — and in an uncomfortable direction.** Citing Korn's
"Architecture Matters" (May 2026): success spread **nearly 58 points across four architectures, from
81.9% against vanilla RAG down to 24.4% against recursive**, and "most of the strongest variant's
advantage came from adversarial framing rather than retrieval optimisation."

**Two ingestion-time detectors took poisoning from 95% to 20%.** Flag a new document whose
nearest-neighbour similarity to existing content exceeds **0.85**; flag a batch whose pairwise internal
similarity exceeds **0.90**. Both follow from the attacker's own requirements. The residual 20% is where
an attacker who understands both thresholds balances between them.

**The thresholds are model properties, not data properties.** Raji is emphatic: **"These thresholds are
properties of your embedding model, not of your data."** The prescription is to baseline your own corpus
and set the threshold at mean + 2 standard deviations, and to **pin the embedding model version**,
because a model upgrade invalidates every calibrated threshold at once. A table walks 0.95 → 0.75,
trading catch rate against false-flag volume.

**Access-controlled retrieval is the only complete defence, and only because it is structural.**
Filtering at query time on classification metadata
(`where={"classification": {"$in": user_permitted_classifications}}`) "does not depend on detecting
anything." Without it, **twenty out of twenty** natural-language queries returned confidential content to
an unauthorised user. And the warning that generalises furthest: **"Partial implementation of this
control is worse than none, because it manufactures confidence."**

**Stored embeddings leak their text.** Morris, Kuleshov, Shmatikov and Rush, "Text Embeddings Reveal
(Almost) As Much As Text" (EMNLP 2023), introduced Vec2Text, which **recovered 92% of 32-token inputs
exactly**. Chen, Lent and Bjerva (ACL 2024) extended inversion to multilingual embeddings.

**ALGEN made inversion cheap, and cost is the contribution.** Chen, Xu and Bjerva (February 2025) learn a
one-step linear map into a decoder's space: **a single aligned pair already gives partial success and
roughly 1,000 pairs reach optimum**, with ROUGE-L up to ~46 in the cross-encoder setting against a
low-fifties monolingual upper bound, and cosine similarity around 0.95. "No tested defence was
effective." Raji's reading: **"ALGEN's contribution is *cost*."** LAGO (May 2025) adds a further 10–20%
ROUGE-L with as few as ten samples per language.

**The action is a reclassification, and it is free.** "Reclassify vector store compromise in your threat
model. It is not a metadata leak. It is a partial document leak." Doing it before an incident costs
nothing; doing it after "is an incident report." Per-tenant vector encryption (IronCore Cloaked AI is
named) is the paid follow-on.

**This is a named OWASP category**, LLM08:2025 Vector and Embedding Weaknesses.

## Why it matters

The vault's [[Retrieval-Augmented Generation]] material has treated retrieval quality as an accuracy
problem. This source establishes that it is also an integrity problem with a distinct threat model, and
supplies the two concepts the vault was missing — [[Retrieval Poisoning]] and [[Embedding Inversion]].

The strongest durable idea is **"the attacker's requirement is also their signature."** That is a
detection strategy derived from the attack's information-theoretic needs rather than from observed
samples, which is why it generalises past the specific poisoning technique demonstrated. It is worth
holding onto as a pattern for defending other learned components.

**"Partial implementation of this control is worse than none, because it manufactures confidence"** is
the second. It is a claim about organisational belief rather than about software, and it applies directly
to guardrails generally — compare the 67 silently no-op'ing checks reported in
[[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]].

Finally, this is the third source in this batch to find a **security surface created by an efficiency
mechanism**: routing instructions can be prompt-injected, retrieval can be poisoned, and stored vectors
leak. The common shape is that a component built as an internal optimisation turns out to accept
untrusted input.

## Tensions / open questions

- The 95% and the 20% both come from twenty runs on a small seeded corpus, one embedding model, one
  generator. Raji says so plainly, but the numbers are quotable in a way the caveat is not.
- The detection thresholds are explicitly model-dependent and require per-corpus baselining, so the
  95% → 20% reduction is not a portable result — it is a demonstration that baselined thresholds *can*
  work.
- The residual 20% is where an attacker "balances between the two" constraints. The source does not show
  that balancing is hard, only that the naive attack fails.
- Legitimate content can be self-similar: a compliance corpus of near-identical policy restatements
  would trip the 0.90 batch threshold constantly. The false-positive economics are tabulated but not
  measured on a real corpus.
- Inversion results are reported on short inputs (Vec2Text at 32 tokens). How much of a long chunked
  document is recoverable in practice is not established here.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Retrieval Poisoning]]
- [[Embedding Inversion]]
- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Agent Security and Governance]]
- [[Amine Raji]]

## Related pages

- [[Semantic Recommendation Systems]]
- [[Agent Observability]]
- [[Reasoning Trace Privacy]]
- [[Defensive Deception for Open Models]]
- [[Model Routing]]

## Citations

- Raw capture: [[2026-09-08 Amine Raji - Cosine Similarity Is Not a Safety Property]]
- Source: <https://aminrj.com/posts/cosine-similarity-is-not-a-safety-property/>
