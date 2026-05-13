---
type: log
created: 2026-05-08
updated: 2026-05-13
tags:
  - log
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-05-08-murphy-reinforcement-learning-overview
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-04-22-perplexity-search-augmented-lm
status: active
---

# Knowledge Base Log

Append-only operational history for the wiki.

## [2026-05-08] scaffold | Knowledge base initialized

- Created the `knowledge-base/raw/`, `knowledge-base/wiki/`, and `knowledge-base/templates/` directory scaffold inside the current workspace.
- Added the root `CLAUDE.md` schema with workflows, page conventions, and maintenance rules.
- Seeded `knowledge-base/wiki/index.md` and this log for navigation and chronology.

## [2026-05-08] ingest | Andrej Karpathy - LLM Wiki

- Captured the raw gist in `knowledge-base/raw/sources/2026-05-08 Andrej Karpathy - LLM Wiki.md`.
- Created [[Andrej Karpathy - LLM Wiki]] as the first source summary page.
- Seeded [[AI Knowledge Base Overview]], [[Persistent Wiki]], [[Schema-Driven Knowledge Base]], [[Ingest Query Lint Loop]], [[Index and Log]], [[Andrej Karpathy]], and [[Obsidian]] from the source.

## [2026-05-08] ingest | Kevin Murphy - Reinforcement Learning: An Overview

- Captured the paper as `knowledge-base/raw/sources/2026-05-08 Kevin Murphy - Reinforcement Learning - An Overview.pdf`.
- Added `knowledge-base/raw/sources/2026-05-08 Kevin Murphy - Reinforcement Learning - An Overview.md` as the immutable raw-source note with arXiv metadata and abstract.
- Created [[Kevin Murphy - Reinforcement Learning - An Overview]] as the source summary page.
- Seeded [[Reinforcement Learning]] as the first domain concept page derived from the paper and updated [[AI Knowledge Base Overview]] plus the index.

## [2026-05-08] query | Mathematical foundations for reinforcement learning

- Filed [[2026-05-08 Mathematical Foundations for Reinforcement Learning]] in response to a query about the math needed to go from Murphy's survey to expert-level RL understanding.
- Linked the answer into the index as the first durable query note in the knowledge base.

## [2026-05-08] lint | knowledge-base/wiki

- Audited the wiki for broken internal links, orphans, thin seed pages, and schema conformance.
- Confirmed all internal wikilinks resolve and no wiki pages are orphaned.
- Fixed a stale claim in [[AI Knowledge Base Overview]] about empty operational folders.
- Added missing `## Related pages` sections to both source summary pages to align them with the schema.
- Filed [[2026-05-08 Wiki Lint Pass]] and linked it from the index.

## [2026-05-13] ingest | Connecting LLMs to the Real World: Tool Use, Function Calling, and MCP

- Moved raw capture from `raw/` to `raw/sources/` per schema convention.
- Created [[ByteByteGo - Connecting LLMs to the Real World]] as source summary page with 10 durable claims and an adoption timeline.
- Seeded three new concept pages: [[Tool Use and Function Calling]], [[Model Context Protocol]], and [[Agentic Loop]].
- Created [[ByteByteGo]] entity page.
- Updated [[AI Knowledge Base Overview]] and the index with the new domain area (LLM tooling and agents).

## [2026-05-13] lint | knowledge-base/wiki

- Audited `knowledge-base/wiki` for broken internal wikilinks, orphans, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, and raw-source coverage.
- Fixed six broken or out-of-scope wikilinks by replacing unresolved wiki targets with valid in-scope references or explicit raw-source file paths.
- Confirmed there are no orphan substantive pages, no missing `## Related pages` sections in scoped content folders, no frontmatter omissions, and no thin pages below the current body-text threshold.
- Verified every scoped content page is listed in the index, every ingest in the log has a corresponding source summary page, and every file in `raw/sources/` is covered by a source summary page.
- Filed [[2026-05-13 Lint Pass]] and linked it from the index.

## [2026-05-13] ingest | Advancing Search-Augmented Language Models

- Raw capture already in `raw/sources/Advancing Search-Augmented Language Models.md`.
- Created [[Perplexity - Advancing Search-Augmented Language Models]] as source summary page with 10 durable claims covering the two-stage SFT→RL pipeline, gated reward aggregation, anchored efficiency penalties, and benchmark results.
- Seeded two new concept pages: [[Search-Augmented Language Models]] and [[Reward Design for RL]].
- Created [[Perplexity]] entity page.
- Updated [[Reinforcement Learning]] with cross-links to the new search-agent RL techniques.
- Updated [[AI Knowledge Base Overview]] and the index with the new source and concepts.

## [2026-05-13] lint | knowledge-base/wiki (pass 2)

- Re-audited `knowledge-base/wiki` after the Perplexity ingest, including broken links, orphans, related-pages coverage, frontmatter, thin pages, index/log completeness, raw-source coverage, and cross-link density.
- Found one broken wikilink to [[Group Relative Policy Optimization]] and fixed it by creating the missing concept page.
- Added reciprocal cross-links from [[Tool Use and Function Calling]] and [[Agentic Loop]] to the new search-agent pages to improve integration density.
- Confirmed that all internal wikilinks now resolve, no substantive pages are orphaned, all scoped pages include `## Related pages`, and all non-PDF raw sources are covered by source summary pages.
- Filed [[2026-05-13 Lint Pass 2]] and linked it from the index.
