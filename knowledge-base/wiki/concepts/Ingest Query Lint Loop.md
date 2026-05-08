---
type: concept
created: 2026-05-08
updated: 2026-05-08
tags:
  - concept
  - workflow
  - maintenance
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
status: active
---

# Ingest Query Lint Loop

## Definition

The core operating loop of the knowledge base is threefold: ingest new sources, answer questions against the maintained wiki, and periodically lint the wiki for coherence and gaps.

## Why it matters

This loop turns the knowledge base into a living system rather than a pile of notes. It gives the LLM recurring responsibilities and makes knowledge maintenance explicit.

## Current synthesis

- **Ingest** converts a new source into a raw capture, a source page, and a set of updates across concept and entity pages.
- **Query** reads the index first, follows the current wiki graph, and can file durable outputs back into the vault.
- **Lint** checks for broken links, stale claims, missing pages, weak summaries, and research gaps.
- The loop compounds value because every pass improves future passes.

## Open questions

- How often should lint passes happen in practice for this vault?
- Which user prompts should automatically result in a filed query note or synthesis page?

## Related pages

- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Persistent Wiki]]
- [[Andrej Karpathy - LLM Wiki]]
- [[AI Knowledge Base Overview]]
