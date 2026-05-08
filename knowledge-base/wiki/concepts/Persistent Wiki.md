---
type: concept
created: 2026-05-08
updated: 2026-05-08
tags:
  - concept
  - wiki
  - llm
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
status: active
---

# Persistent Wiki

## Definition

A persistent wiki is an interlinked markdown layer that the LLM updates over time so that synthesis, cross-references, and contradictions accumulate instead of being recomputed from raw sources for every question.

## Why it matters

It changes the value of the system from "good retrieval at query time" to "continuously improving compiled knowledge." The wiki becomes the durable working memory of the vault.

## Current synthesis

- The wiki sits between raw sources and downstream questions.
- Each ingest should strengthen or revise existing pages instead of producing isolated summaries.
- Good query answers can become durable pages, which means exploration compounds too.
- Maintenance cost stays low because the LLM can update many related files in one pass.

## Open questions

- When should a new idea extend an existing concept page versus creating a fresh one?
- What review cadence keeps the wiki coherent as the number of sources grows?

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[AI Knowledge Base Overview]]
- [[Schema-Driven Knowledge Base]]
- [[Ingest Query Lint Loop]]
- [[Index and Log]]
- [[Obsidian]]
