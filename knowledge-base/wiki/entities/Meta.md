---
type: entity
created: 2026-09-04
updated: 2026-09-04
entity_kind: organization
tags:
  - entity
  - organization
  - ai-lab
  - agents
  - knowledge-management
source_ids:
  - src-2026-09-02-meta-organizational-second-brain
status: active
---

# Meta

## What it is

Technology company operating at very large scale, publisher of the Llama open-weight model family, and — in this
vault's only directly ingested Meta source — an operator of internal domain-expert agents.

## Why it matters here

Meta enters this vault not through a model release but through an **internal deployment report**:
[[Meta - An Organizational Second Brain]] describes a compliance-domain expert agent built on 200+ structured
knowledge files, improved by compiling expert feedback into text under regression tests rather than by retraining.
It anchors [[Institutional Knowledge Agents]].

The reason it matters more than a typical engineering-blog post is the position it stakes out: **"Keep the
complexity in text files, not in model weights or opaque embeddings. Every improvement is a text edit a domain
expert can review in 30 seconds."** That is an argument about governance as much as capability, and it comes from
an organisation with the resources to fine-tune instead.

It also gives this vault a mirror. The described architecture — declared frontmatter dependencies, deterministic
routing indexes, an append-only improvement record, a deterministic linter — converges independently on the shape
described in [[Schema-Driven Knowledge Base]], [[Persistent Wiki]], [[Index and Log]], and
[[Ingest Query Lint Loop]]. The divergences are the useful part: Meta's loop adds blind regression replay and an
**independent adversarial reviewer** that sees only diffs and not the rationale.

## Notes

- The source positions itself as a production instance of ideas already circulating, explicitly citing
  **Karpathy's LLM Wiki** proposal (see [[Andrej Karpathy]]) and **Google's Open Knowledge Format** as prior art.
- Reported results after three two-week sprints — "useful almost all the time," days reduced to minutes, "zero
  regressions" — are **entirely qualitative, with no denominators, baselines, or task counts.** Read as a design
  report, not as evidence of effectiveness.
- The one quantitative figure, roughly **80% fewer tokens per turn** from progressive disclosure, is unattributed
  across several simultaneous changes.
- Meta appears elsewhere in this vault only indirectly, through Llama in the open-weight model discussions.

## Related pages

- [[Meta - An Organizational Second Brain]]
- [[Institutional Knowledge Agents]]
- [[Schema-Driven Knowledge Base]]
- [[Persistent Wiki]]
- [[Retrieval-Augmented Generation]]
- [[Agent Memory]]
- [[Continual Learning for Agents]]
- [[LLM-as-a-Judge]]
- [[Andrej Karpathy]]
- [[AI Knowledge Base Overview]]
