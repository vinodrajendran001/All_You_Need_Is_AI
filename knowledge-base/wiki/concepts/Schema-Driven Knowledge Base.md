---
type: concept
created: 2026-05-08
updated: 2026-05-08
tags:
  - concept
  - schema
  - workflow
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
status: active
---

# Schema-Driven Knowledge Base

## Definition

A schema-driven knowledge base uses an instruction file to define the directory structure, note types, naming conventions, workflows, and maintenance rules that the LLM must follow.

## Why it matters

Without a schema, the model behaves like a generic assistant. With a schema, it behaves like a disciplined maintainer that updates the right pages, preserves consistency, and keeps the wiki navigable.

## Current synthesis

- The schema is the operational contract between human and LLM.
- It encodes how ingests happen, how durable answers get filed, and how the wiki gets linted.
- In this workspace, the root `CLAUDE.md` file is the schema and `knowledge-base/` is the maintained surface it governs.
- The schema should evolve as the vault grows, especially when new page types or workflows prove useful.

## Open questions

- Which metadata fields will become most useful once the number of sources grows?
- When should the schema introduce stronger constraints for tags, aliases, or citation formats?

## Related pages

- [[Persistent Wiki]]
- [[Ingest Query Lint Loop]]
- [[AI Knowledge Base Overview]]
- [[Andrej Karpathy - LLM Wiki]]
- [[knowledge-base/wiki/index|Knowledge Base Index]]
