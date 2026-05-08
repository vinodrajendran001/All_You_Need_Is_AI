---
type: concept
created: 2026-05-08
updated: 2026-05-08
tags:
  - concept
  - navigation
  - maintenance
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
status: active
---

# Index and Log

## Definition

`index.md` is the content-oriented catalog of the wiki, while `log.md` is the append-only operational timeline of what changed and when.

## Why it matters

Together they give both the human and the LLM lightweight navigation and memory without requiring dedicated retrieval infrastructure at small scale.

## Current synthesis

- The index is the first file to read when routing a question through the wiki.
- The log preserves chronology, which helps reconstruct recent ingests, queries, and maintenance passes.
- Keeping both files current makes the wiki legible even as it grows.
- This vault uses them as explicit control surfaces rather than passive notes.

## Open questions

- At what scale should index maintenance become partially automated with Dataview or custom tooling?
- What level of detail in log entries best balances traceability with readability?

## Related pages

- [[knowledge-base/wiki/index|Knowledge Base Index]]
- [[knowledge-base/wiki/log|Knowledge Base Log]]
- [[Ingest Query Lint Loop]]
- [[Persistent Wiki]]
- [[Andrej Karpathy - LLM Wiki]]
