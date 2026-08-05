---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-karpathy-llm-wiki
title: 'Karpathy''s LLM Wiki: A Knowledge Base That Compounds'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/karpathy-llm-wiki
published: '2026-05-27'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Karpathy's LLM Wiki: A Knowledge Base That Compounds

In April 2026, Andrej Karpathy published a gist that quietly changed how a lot of builders think about knowledge management.

It is not a tool. It is a pattern. And it fixes a problem every serious AI builder has: **the more you read, the less you remember — and every LLM session starts from zero.**

He called it the **LLM Wiki**.

*Update (June 2026): Karpathy has since joined Anthropic's pre-training team, but the LLM Wiki pattern stands on its own. It also pairs with the rest of his frameworks, which we collect in the [Karpathy AI engineering playbook](/blog/karpathy-ai-engineering-playbook).*

---

## The problem with RAG (and why most people build it wrong)

Most people's experience with LLMs and documents looks like RAG: you upload files, the LLM retrieves relevant chunks at query time, and generates an answer.

This works. But it has a fundamental flaw: **nothing accumulates.**

Ask a subtle question that requires synthesizing five documents and the LLM has to find and piece together the relevant fragments every time. The knowledge is never built up. NotebookLM, ChatGPT file uploads, most RAG systems — all work this way.

Karpathy's insight: what if instead of retrieving from raw documents at query time, an LLM **incrementally builds and maintains a persistent wiki**?

---

## What the LLM Wiki actually is

Instead of indexing documents for retrieval, an agent reads each new source and integrates it into a structured, interlinked collection of markdown files:

- **Entity pages** (people, companies, tools)
- **Concept pages** (ideas, frameworks, definitions)
- **Summaries** of each source
- **Contradictions** between sources flagged
- **Cross-references** already built
- An evolving synthesis that reflects everything you have read

Karpathy's key phrase: **"the wiki is a persistent, compounding artifact."**

You never write it yourself. The LLM writes and maintains all of it. You curate sources, ask questions, and direct the analysis. The LLM does the bookkeeping.

His setup: Claude Code open on one side, Obsidian open on the other. The LLM makes edits in real time. He browses the results — following links, checking the graph view, reading updated pages.

> "Obsidian is the IDE. The LLM is the programmer. The wiki is the codebase."

---

## The three-layer architecture

**Layer 1: Raw sources** — your curated documents. Articles, papers, data files. Immutable — the LLM reads from them but never modifies them. Source of truth.

**Layer 2: The wiki** — LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, synthesis. The LLM owns this layer entirely. You read it; the LLM writes it.

**Layer 3: The schema** — a CLAUDE.md or AGENTS.md file that tells the LLM how the wiki is structured, what conventions to follow, and what workflows to run when ingesting sources or answering questions. This is what turns a generic chatbot into a disciplined wiki maintainer.

---

## The three operations

### Ingest

You drop a new source in and tell the LLM to process it. The LLM reads it, discusses key takeaways with you, writes a summary page, updates the index, updates relevant entity and concept pages across the wiki, and appends a log entry.

A single source might touch 10–15 wiki pages.

### Query

You ask questions against the wiki. The LLM searches relevant pages, reads them, and synthesizes an answer with citations.

Crucially: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and should not disappear into chat history.

### Lint

Periodically, ask the LLM to health-check the wiki. Look for contradictions, stale claims, orphan pages, missing cross-references, important concepts with no page.

The LLM suggests new questions to investigate and new sources to look for.

---

## Why this works (and why humans abandon wikis)

The tedious part of maintaining a knowledge base is not reading or thinking. It is the bookkeeping: updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages.

**Humans abandon wikis because the maintenance burden grows faster than the value.**

LLMs do not get bored. They do not forget to update a cross-reference. They can touch 15 files in one pass. The wiki stays maintained because **the cost of maintenance is near zero**.

The human's job: curate sources, direct the analysis, ask good questions, think about what it all means.

The LLM's job: everything else.

---

## What you can build this for

Karpathy's examples from the gist:

- **Personal:** tracking goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, building a structured picture over time.
- **Research:** going deep on a topic over weeks or months — papers, articles, reports — incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book:** filing each chapter as you go, building out pages for characters, themes, plot threads. By the end you have a rich companion wiki.
- **Business/team:** an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls.
- **Competitive analysis, due diligence, trip planning, hobby deep-dives** — anything where you accumulate knowledge over time and want it organized rather than scattered.

---

## The practical setup (what Karpathy actually uses)

- **Obsidian Web Clipper:** browser extension that converts web articles to markdown for quick ingestion
- **Local image downloads:** bind a hotkey to download all images in a clipped article locally — lets the LLM view and reference images directly
- **Obsidian graph view:** best way to see the shape of your wiki — what is connected, which pages are hubs, which are orphans
- **qmd:** local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, with both CLI and MCP server interfaces — useful once your wiki grows past a few hundred pages
- **Git:** the wiki is just a git repo of markdown files. Version history, branching, collaboration for free.

---

## The navigation system

Two special files keep the LLM oriented as the wiki grows:

**index.md** — content-oriented catalog of everything in the wiki. Each page listed with a link, a one-line summary, and metadata. Organized by category. The LLM reads this first when answering any query. Works well up to a few hundred pages without needing vector search.

**log.md** — chronological, append-only record of every ingest, query, and lint pass. Use a consistent prefix format so entries stay parseable:

code

```
## [2026-04-02] ingest | Article Title
```

Run `grep "^## \[" log.md | tail -5` to see the last five entries.

---

## Why this is different from a second brain

Tools like Obsidian, Notion, and Roam are great for human-maintained knowledge. But they depend on you doing the filing, tagging, and linking. Most people fall behind and the system collapses.

Karpathy's pattern eliminates the human bottleneck. The wiki grows with every source you add and every question you ask. **The more you use it, the richer it gets.** The maintenance never falls behind because the LLM handles it continuously.

Karpathy draws a direct line to Vannevar Bush's 1945 Memex concept — a personal, curated knowledge store with associative trails between documents. Bush could not solve who does the maintenance. The LLM handles that.

---

## How to start

The gist is intentionally abstract — it describes the pattern, not a specific implementation. That is by design.

Karpathy's advice: share the gist with your LLM agent and work together to instantiate a version that fits your domain.

**A minimal starting point:**

1. Create a folder structure: `raw/` for sources, `wiki/` for LLM-generated pages
2. Write a CLAUDE.md schema that describes the wiki structure and ingestion workflow
3. Clip your first 5–10 articles using Obsidian Web Clipper
4. Start ingesting one at a time, staying involved — read the summaries, check the updates, guide the LLM on emphasis
5. Query against what you have built and file good answers back in

The wiki compounds from the first source. Start small.

---

AI Builder Club members are building these exact systems in our community — personal research wikis, competitive analysis bases, team knowledge tools. If you want to go deeper, [join us](https://www.aibuilderclub.com/pricing?utm_source=blog&utm_medium=article&utm_campaign=llm-wiki) and bring your own use case.

The LLM Wiki is a pattern published by Andrej Karpathy in April 2026 where instead of using RAG to retrieve from raw documents, an LLM agent incrementally builds and maintains a persistent, structured wiki of markdown files. It includes entity pages, concept pages, source summaries, contradictions, and cross-references. The wiki compounds over time — every source you add and every question you ask makes it richer. The LLM does all the bookkeeping; you curate sources and ask questions.

RAG retrieves relevant chunks from raw documents at query time and generates an answer. Nothing accumulates — ask a subtle question requiring five documents and the LLM must find and piece together fragments every time. The LLM Wiki pre-processes sources into a structured, interlinked collection. Knowledge is built up incrementally. Cross-references are maintained. Contradictions are flagged. The wiki is a persistent, compounding artifact rather than a retrieval index.

Karpathy's setup: Claude Code as the LLM agent, Obsidian as the wiki viewer (graph view, markdown rendering, local links). Additional tools: Obsidian Web Clipper for converting articles to markdown, qmd for local BM25/vector search across wiki files, and Git for version history. His phrase: 'Obsidian is the IDE. The LLM is the programmer. The wiki is the codebase.'

Layer 1: Raw sources — your curated documents (articles, papers, data). Immutable, the LLM reads but never modifies. Layer 2: The wiki — LLM-generated markdown files (summaries, entity pages, concept pages, comparisons). The LLM owns this entirely. Layer 3: The schema — a CLAUDE.md or AGENTS.md file that tells the LLM how the wiki is structured, what conventions to follow, and what workflows to run. This schema is what turns a generic chatbot into a disciplined wiki maintainer.

Ingest: drop a new source, the LLM reads it, writes a summary, updates the index, updates entity and concept pages (touching 10-15 pages per source). Query: ask questions against the wiki, the LLM searches relevant pages and synthesizes answers — good answers get filed back as new pages. Lint: periodically health-check the wiki for contradictions, stale claims, orphan pages, and missing cross-references. The LLM suggests new questions and sources to investigate.

Minimal starting point: (1) Create a folder structure — raw/ for sources, wiki/ for LLM-generated pages. (2) Write a CLAUDE.md schema describing the wiki structure and ingestion workflow. (3) Clip your first 5-10 articles using Obsidian Web Clipper. (4) Ingest one at a time, staying involved — read summaries, guide the LLM on emphasis. (5) Query against what you've built and file good answers back in. The wiki compounds from the first source.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
