---
type: overview
created: 2026-05-08
updated: 2026-05-08
tags:
  - overview
  - ai
  - knowledge-base
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
status: active
---

# AI Knowledge Base Overview

## Scope

This wiki is the persistent knowledge layer for the `All_You_Need_Is_AI` vault. It is meant to accumulate sources, syntheses, and durable answers about AI instead of rediscovering them from scratch on every query.

## Current picture

The workspace now implements Karpathy's three-layer pattern:

- Raw sources live under `knowledge-base/raw/`.
- Curated wiki pages live under `knowledge-base/wiki/`.
- The operating schema lives in the root [[CLAUDE]] note.

The first source in the system is [[Andrej Karpathy - LLM Wiki]], which establishes the baseline operating model for future ingests.

## Key pages

- [[knowledge-base/wiki/index|Knowledge Base Index]] - main entry point into the wiki
- [[Persistent Wiki]] - the central idea behind the whole system
- [[Schema-Driven Knowledge Base]] - how the schema keeps maintenance disciplined
- [[Ingest Query Lint Loop]] - the repeating maintenance cycle
- [[Index and Log]] - control files that help the LLM navigate the vault

## Gaps

- Existing notes elsewhere in the workspace have not yet been ingested into this structure.
- The `queries/`, `syntheses/`, and `lint/` folders are ready but intentionally empty until real work accumulates there.
- No search tooling has been added yet because the index is enough at the current scale.

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Obsidian]]
