---
type: source-summary
created: 2026-05-08
updated: 2026-05-13
source_id: src-2026-05-08-karpathy-llm-wiki
source_title: LLM Wiki
source_author: Andrej Karpathy
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
tags:
  - source/summary
  - llm/wiki
  - obsidian
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
status: active
---

# Andrej Karpathy - LLM Wiki

## Summary

Karpathy proposes replacing query-time-only RAG with a persistent, LLM-maintained wiki that sits between raw sources and downstream questions. Instead of repeatedly rediscovering knowledge from source files, the LLM continuously compiles, links, and updates markdown pages that reflect the current state of understanding.

## Key claims

- The durable artifact should be the wiki, not the transient chat answer.
- The LLM should maintain summaries, cross-links, contradictions, and page updates as new sources arrive.
- A schema file such as `CLAUDE.md` is what turns the model into a disciplined knowledge-base maintainer.
- `ingest`, `query`, and `lint` are the three core operations.
- A simple `index.md` plus `log.md` can work well before heavier search infrastructure is needed.

## Why it matters

This pattern fits the workspace well because the vault already contains AI notes and markdown artifacts that can be gradually ingested into a single, navigable wiki. It also aligns with Obsidian's strengths: local files, backlinks, graph view, templates, and a strong note-linking workflow.

## Tensions / open questions

- How much of the existing vault should be backfilled into the new structure versus left as background material?
- At what scale should this wiki adopt dedicated search tooling instead of relying on the index and filesystem search?
- What is the right threshold for filing a chat answer into `queries/` or `syntheses/`?

## Affected pages

- [[AI Knowledge Base Overview]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Ingest Query Lint Loop]]
- [[Index and Log]]
- [[Andrej Karpathy]]
- [[Obsidian]]

## Citations

- Raw capture: `knowledge-base/raw/sources/2026-05-08 Andrej Karpathy - LLM Wiki.md`

## Related pages

- [[AI Knowledge Base Overview]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Ingest Query Lint Loop]]
- [[Index and Log]]
- [[Andrej Karpathy]]
- [[Obsidian]]
