---
type: entity
created: 2026-09-11
updated: 2026-09-11
entity_kind: person
tags:
  - entity
  - topic/security
  - topic/rag
  - topic/embeddings
source_ids:
  - src-2026-09-08-raji-cosine-similarity-safety
status: active
---

# Amine Raji

## What it is

Security researcher and practitioner writing at aminrj.com on the security properties of AI systems, with
an emphasis on running his own measurements and labelling their limits.

## Why it matters here

Raji established both of the vault's vector-store security concepts — [[Retrieval Poisoning]] and
[[Embedding Inversion]] — from a single observation: **cosine similarity measures an angle, and has no
notion of truth, authority or provenance.**

The defensive contribution is the more durable one, and it is structural rather than empirical: **the
attacker's requirement is also their signature.** A poison document must be similar to the target query,
and a corroborating set must be mutually similar, so both are measurable at ingestion. That reasoning —
deriving a detector from what the attack needs rather than from observed samples — is a pattern worth
reusing wherever a learned component accepts untrusted input.

His second reusable line is about controls rather than software: **"Partial implementation of this control
is worse than none, because it manufactures confidence."** It applies directly to the silently dead
guardrails recorded under [[Agent Observability]].

## Notes

- Measurements are March 2026 on ChromaDB with `all-MiniLM-L6-v2` (384-dim) and Qwen2.5-7B-Instruct at
  temperature 0.1, and he explicitly labels the 95% attack-success figure "a lab reading, not a base
  rate" from twenty runs.
- Flags that **ChromaDB's default distance is squared L2, not cosine**, which silently changes what
  "similarity" means in applications built on the default.
- Reports that the legitimate document was often retrieved **and still lost**, which is the finding that
  defeats "improve your retriever" as a defence.
- Emphasises that detection thresholds are properties of the embedding model rather than of the data,
  and that pinning the model version is therefore a security control.
- Argues the free action is a threat-model reclassification: vector store compromise is partial document
  disclosure, not metadata leakage.

## Related pages

- [[Retrieval Poisoning]]
- [[Embedding Inversion]]
- [[Retrieval-Augmented Generation]]
- [[Embedding Model Selection]]
- [[Agent Security and Governance]]
- [[Amine Raji - Cosine Similarity Is Not a Safety Property]]
