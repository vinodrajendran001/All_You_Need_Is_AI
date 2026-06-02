---
type: log
created: 2026-05-08
updated: 2026-06-02
tags:
  - log
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-05-08-murphy-reinforcement-learning-overview
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-18-alphasignal-return-of-recursion
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-05-18-hanfang-pytorch-practice
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-05-21-leetcode-templates
  - src-2026-05-21-bytebytego-batch
  - src-2026-05-28-bytebytego-airtable-search
  - src-2026-05-28-doordash-llm-judge
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-02-dwarkesh-eric-jang-flashcards
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
  - src-2026-06-02-dwarkesh-reiner-pope-chip-design
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
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

## [2026-05-18] ingest | Alpha Signal - The Return of Recursion

- Raw source already in `knowledge-base/raw/sources/The return of recursion - How AI is rethinking complex reasoning.md`.
- Created [[Alpha Signal - The Return of Recursion]] source summary page.
- Created [[Latent-Space Reasoning]] and [[Recursive Architectures]] concept pages.
- Created [[Alpha Signal]] entity page.
- Updated index, overview, and log.

## [2026-05-18] lint | Full wiki lint pass

- Audited `knowledge-base/wiki` for broken wikilinks, orphans, related-pages coverage, frontmatter conformance, thin pages, contradiction risk, index/log completeness, raw-source coverage, and cross-link density.
- Fixed all broken control-file wikilinks by normalizing them to [[index|Knowledge Base Index]] and [[log|Knowledge Base Log]].
- Corrected invalid frontmatter in [[Kevin Murphy - Reinforcement Learning - An Overview]] and refreshed stale maturity wording in [[AI Knowledge Base Overview]].
- Strengthened reciprocal cross-links across Karpathy-, ByteByteGo-, and Perplexity-derived pages.
- Filed [[2026-05-18 Lint Pass]] and linked it from the index.

## [2026-05-18] ingest | The Pocket - PocketFlow Tutorial Docs

- Captured 39 tutorial documents from the PocketFlow Tutorial Video Generator repo to `raw/sources/pocketflow-tutorial-docs/`.
- Created raw source note and [[The Pocket - PocketFlow Tutorial Docs]] source summary page.
- Created [[The Pocket]] entity page.
- Created new concept pages: [[Transformer Architecture]], [[LLM Training Pipeline]], [[Neural Network Fundamentals]], [[Model Quantization and Efficiency]].
- Updated [[Reinforcement Learning]] with cross-links to detailed RL tutorial content.
- Updated index and overview.

## [2026-05-18] ingest | Han Fang - PyTorch Practice

- Captured 7 files (5 Python scripts + README + runner) from the pytorch-practice repo to `raw/sources/pytorch-practice/`.
- Created raw source note and [[Han Fang - PyTorch Practice]] source summary page.
- Created [[Han Fang]] entity page.
- Updated [[Neural Network Fundamentals]], [[Transformer Architecture]], [[Model Quantization and Efficiency]], and [[LLM Training Pipeline]] with cross-links to from-scratch PyTorch implementations.
- Updated index and overview.

## [2026-05-18] ingest | Classic RAG vs Graph RAG vs Agentic RAG

- Added frontmatter to raw source `Classic RAG vs Graph RAG vs Agentic RAG.md`.
- Created [[Classic RAG vs Graph RAG vs Agentic RAG]] source summary page.
- Created [[Retrieval-Augmented Generation]] concept page synthesizing across Classic, Graph, and Agentic RAG tiers.
- Updated [[Search-Augmented Language Models]], [[Agentic Loop]], and [[Tool Use and Function Calling]] with RAG cross-links.
- Updated index and overview.

## [2026-05-18] lint | Full wiki lint pass (post-ingest)

- Re-audited broken wikilinks, orphans, related-pages coverage, frontmatter, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and staleness risk across `knowledge-base/wiki`.
- Found no broken wikilinks, orphan substantive pages, missing related-pages sections, frontmatter gaps, thin substantive pages, index omissions, log mismatches, or raw-source coverage gaps.
- Corrected a stale source-ordering claim in [[AI Knowledge Base Overview]] so the Han Fang and RAG ingests now match chronological ingest order.
- Added an explicit raw-capture citation to [[Alpha Signal - The Return of Recursion]] to make the recursion-source coverage clearer.
- Filed [[2026-05-18 Lint Pass 2]] and linked it from the index.

## [2026-05-18] lint | Full wiki lint pass (post-consolidation)

- No broken wikilinks, orphan substantive pages, missing `## Related pages` sections, frontmatter gaps, thin pages, index omissions, log mismatches, raw-source coverage gaps, or cross-link density failures were found across `knowledge-base/wiki`.
- Verified that both `raw/sources/pytorch-practice/` and `raw/sources/2026-05-18 Han Fang - PyTorch Practice.md` intentionally map to [[Han Fang - PyTorch Practice]], so no new source summary was needed.
- Filed [[2026-05-18 Lint Pass 3]] and linked it from the index.

## [2026-05-21] ingest | Universal LeetCode Templates — The Complete Arsenal

- Added frontmatter to raw source `Universal LeetCode Templates — The Complete Arsenal.md`.
- Created [[Universal LeetCode Templates]] source summary page.
- Created [[Algorithm Templates for Interviews]] concept page synthesizing DSA templates with ML interview prep.
- Updated index and overview.

## [2026-05-21] lint | Full wiki lint pass

- Audited 45 markdown wiki pages for broken wikilinks, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and staleness risk.
- Found no structural defects; all substantive pages resolve, are indexed, have valid frontmatter, and remain covered by the log and raw-source graph.
- Flagged the MCP timeline/security notes as time-sensitive monitor items for future ingests, but found no current contradictions requiring content edits.
- Filed [[2026-05-21 Lint Pass]] and linked it from the index.

## [2026-05-21] ingest | ByteByteGo - System Design and AI at Scale (May 2026 Batch)

- Added source_id frontmatter to 8 raw ByteByteGo articles in `raw/sources/`.
- Created composite source summary [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]].
- Created new concept pages: [[ML Systems at Scale]] and [[AI Agents in Production]].
- Updated [[ByteByteGo]] entity page, [[Agentic Loop]], [[Model Context Protocol]], [[Search-Augmented Language Models]], and [[Retrieval-Augmented Generation]] with cross-links.
- Updated index and overview.

## [2026-05-21] lint | Full wiki lint pass (post-ByteByteGo batch)

- Audited `knowledge-base/wiki` for broken wikilinks, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and contradiction/staleness risk.
- Found no structural defects; all substantive pages resolve, are indexed, have valid frontmatter, and remain covered by the log and raw-source graph, including the composite ByteByteGo batch mapping.
- No immediate content-page fixes were required beyond control-file updates.
- Filed [[2026-05-21 Lint Pass 2]] and linked it from the index.

## [2026-05-29] ingest | Airtable Search + DoorDash LLM-as-a-Judge

- Added source_id frontmatter to 2 new raw articles.
- Created [[ByteByteGo - How Airtable Built the Search Layer]] and [[DoorDash - LLM-as-a-Judge for Search Evaluation]] source summary pages.
- Created [[LLM-as-a-Judge]] concept page.
- Created [[DoorDash]] entity page.
- Updated [[ML Systems at Scale]], [[Retrieval-Augmented Generation]], and [[ByteByteGo]] with cross-links.
- Updated index and overview.

## [2026-05-29] lint | Full wiki lint pass

- Audited 54 markdown wiki pages for broken wikilinks, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, log consistency, raw-source coverage, cross-link density, and contradiction/staleness risk.
- Strengthened [[Search-Augmented Language Models]] and [[ML Systems at Scale]] with [[LLM-as-a-Judge]] links and DoorDash-derived evaluation notes so the new production-evaluation branch is fully integrated.
- Filed [[2026-05-29 Lint Pass]] and linked it from the index.

## [2026-06-02] ingest | Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club

- Captured the YouTube video metadata as `knowledge-base/raw/sources/2026-06-02 Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club.md`.
- Saved the auto-generated transcript in both VTT and cleaned text form under `knowledge-base/raw/assets/`.
- Created [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]] as the source summary page.
- Seeded [[World Models]] and [[Y Combinator]].
- Updated [[Model Quantization and Efficiency]], [[LLM Training Pipeline]], [[AI Knowledge Base Overview]], and the index with the new source.

## [2026-06-02] ingest | Dwarkesh Patel - Eric Jang interview + flashcards

- Captured the article as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch.md` and preserved extracted body HTML plus readable transcript assets under `knowledge-base/raw/assets/`.
- Captured the flashcards as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Eric Jang Flashcards.md` and preserved structured JSON plus readable markdown assets under `knowledge-base/raw/assets/`.
- Created [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]] and [[Dwarkesh Patel - Eric Jang Flashcards]] as source summary pages.
- Seeded [[Monte Carlo Tree Search]], [[Automated AI Research]], and [[Eric Jang]].
- Updated [[Reinforcement Learning]], [[Agentic Loop]], [[AI Knowledge Base Overview]], and the index with the new sources and concepts.

## [2026-06-02] ingest | Dwarkesh Patel - Reiner Pope article + flashcards

- Captured the article as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Reiner Pope - Chip design from the bottom up.md` and preserved extracted body HTML plus readable transcript assets under `knowledge-base/raw/assets/`.
- Captured the flashcards as `knowledge-base/raw/sources/2026-06-02 Dwarkesh Patel - Reiner Pope Flashcards.md` and preserved structured JSON plus readable markdown assets under `knowledge-base/raw/assets/`.
- Created [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]] and [[Dwarkesh Patel - Reiner Pope Flashcards]] as source summary pages.
- Seeded [[AI Accelerator Architecture]] and [[Reiner Pope]].
- Updated [[Model Quantization and Efficiency]], [[ML Systems at Scale]], [[LLM Training Pipeline]], [[AI Knowledge Base Overview]], and the index with the new sources and hardware/compute branch.

## [2026-06-02] lint | Full wiki lint pass

- Audited 67 markdown wiki pages for broken wikilinks, relative links, orphan pages, related-pages coverage, frontmatter conformance, thin pages, index completeness, and staleness risk.
- Found no structural defects: no broken links, no orphans, no missing related-pages sections, and no index omissions.
- Expanded [[Alpha Signal]], [[Andrej Karpathy]], and [[Obsidian]] to address the only immediate content issue: thin entity coverage.
- Filed [[2026-06-02 Lint Pass]] and linked it from the index.
