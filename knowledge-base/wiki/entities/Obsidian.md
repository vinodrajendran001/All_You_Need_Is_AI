---
type: entity
created: 2026-05-08
updated: 2026-06-02
entity_kind: tool
tags:
  - entity
  - tool
  - obsidian
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
status: active
---

# Obsidian

## What it is

The local markdown note environment that serves as the IDE, browser, and graph surface for this wiki.

## Why it matters here

The `LLM Wiki` pattern assumes a human can inspect live markdown pages while the LLM maintains them. Obsidian makes that practical through backlinks, graph view, templates, local files, and attachment handling.

## Notes

- The source recommends Obsidian Web Clipper as a fast path for getting articles into the raw corpus.
- Local attachment downloads fit naturally into `knowledge-base/raw/assets/`.
- Graph view is especially useful for spotting hubs, weakly linked areas, and orphans.
- Obsidian's local-first file model fits this vault because the knowledge base is meant to remain transparent and inspectable as plain markdown, not hidden behind an app-specific database.
- The tool is also a good fit for the ingest/query/lint loop because templates, wikilinks, and backlinks make maintenance work visible to both the human reader and the LLM maintainer.

## Related pages

- [[AI Knowledge Base Overview]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Ingest Query Lint Loop]]
- [[Andrej Karpathy - LLM Wiki]]
- [[Andrej Karpathy]]
