---
type: entity
created: 2026-05-08
updated: 2026-06-02
entity_kind: person
tags:
  - entity
  - author
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
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

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Ingest Query Lint Loop]]
- [[AI Knowledge Base Overview]]
- [[Obsidian]]
