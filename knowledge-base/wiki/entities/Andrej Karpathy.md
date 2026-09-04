---
type: entity
created: 2026-05-08
updated: 2026-09-04
entity_kind: person
tags:
  - entity
  - author
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-09-02-meta-organizational-second-brain
status: active
---

# Andrej Karpathy

## What it is

Author of the `LLM Wiki` gist that seeded this workspace's knowledge-base structure.

## Why it matters here

His gist defines the operating pattern used here: immutable raw sources, an LLM-maintained wiki, a schema file to enforce discipline, and recurring ingest/query/lint workflows.

## Notes

- Frames the wiki as a compounding artifact rather than a one-shot retrieval layer.
- Explicitly positions Obsidian as the browsing and graph-view environment for the maintained wiki.
- Suggests that good answers and analyses should be filed back into the wiki instead of dying in chat history.
- The vault's `knowledge-base/` layout, root `CLAUDE.md`, and emphasis on `index.md` plus `log.md` all descend directly from this operating model.
- His framing is important not because every implementation detail must match the gist, but because it defines the maintenance mindset: update the knowledge artifact itself, not just the current answer.

## The LLM Wiki idea, built at industrial scale

[[Meta - An Organizational Second Brain]] explicitly cites Karpathy's **LLM Wiki** proposal as prior art,
alongside Google's Open Knowledge Format, for a production deployment of 200+ structured knowledge files backing
a compliance-domain expert agent. This vault is itself an instance of the same proposal, so the citation is the
first outside evidence that the idea generalises past a personal knowledge base into an organisational one.

What the industrial version adds to Karpathy's sketch is the maintenance machinery: bidirectional
`depends_on`/`referenced_by` declarations, deterministic routing indexes rather than embedding similarity, a
pass/fail linter, and blind regression replay — plus the claim that the whole thing improves **without model
retraining**, which is the strongest form of Karpathy's original argument that the knowledge belongs in text
rather than in weights. See [[Institutional Knowledge Agents]].

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Ingest Query Lint Loop]]
- [[AI Knowledge Base Overview]]
- [[Obsidian]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
