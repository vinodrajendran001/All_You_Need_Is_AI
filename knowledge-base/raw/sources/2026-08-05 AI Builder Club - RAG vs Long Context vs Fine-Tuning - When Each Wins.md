---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-rag-vs-long-context-vs-fine-tuning
title: 'RAG vs Long Context vs Fine-Tuning: When Each Wins'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/rag-vs-long-context-vs-fine-tuning
published: '2026-06-12'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# RAG vs Long Context vs Fine-Tuning: When Each Wins

**Your model doesn't know your data. There are exactly three ways to fix that, and most builders pick the wrong one first.** They reach for fine-tuning (expensive, slow, usually unnecessary), or dump everything into a long context window (works until it [rots](/blog/context-engineering-guide)), when what they needed was retrieval - or sometimes the reverse.

The cleanest way to keep the three straight is an exam analogy:

- **Long context** = bring the entire textbook into the exam. Everything's there; finding the right page mid-exam is your problem.
- **RAG** = open-book exam with a librarian. You ask, the librarian fetches the two relevant pages, you answer from those.
- **Fine-tuning** = study the subject for a semester. The knowledge is *in you* now - but it's frozen at study time, and re-studying costs real money.

Here's when each wins, how a modern RAG pipeline actually works, and why the 2023-era "chunk everything and embed it" recipe is quietly being replaced.

---

## The Decision Table First

|  | Long context | RAG | Fine-tuning |
| --- | --- | --- | --- |
| Knowledge freshness | Per-request | Per-request | Frozen at training |
| Corpus size | Up to ~1M tokens | Unbounded | Unbounded (baked in) |
| Cost per query | High (pay for every token, every time) | Low (pay for retrieved slices) | Lowest per query, highest upfront |
| Updates | Re-paste | Re-index one doc | Re-train |
| Citations possible | Weak | Yes - retrieval gives you sources | No |
| Changes model behavior/style | No | No | Yes - this is its real job |
| Failure mode | [Context rot](/blog/context-engineering-guide), 98%→64% accuracy decay | Bad retrieval = confident nonsense | Catastrophic forgetting, stale facts |

The three rules of thumb that fall out:

1. **Corpus fits in ~50K tokens and rarely changes?** Just put it in context. RAG infrastructure for a 30-page handbook is premature engineering.
2. **Corpus is large, changing, or needs citations?** RAG. This is 90% of "chat with our docs/database/knowledge base" use cases.
3. **You need to change how the model *behaves* - tone, format, domain vocabulary, task specialization?** Fine-tuning. It's terrible at adding facts (facts go stale; weights don't update) but it's the only option that rewires style and skill.

And the combo nobody mentions: production systems usually run **RAG on top of a (sometimes fine-tuned) base, inside a managed context window**. The three aren't rivals; they're layers.

---

## What RAG Actually Is

Retrieval-Augmented Generation: at query time, fetch relevant material from an external knowledge store and inject it into the prompt before the model answers. The model's weights stay frozen; its *inputs* get smart. That single move solves the two structural problems of every LLM:

- **Knowledge cutoff** - the model's training data ended months ago; your data changed this morning
- **Fact hallucination** - asked about things it doesn't know, the model generates plausible text anyway. Grounding it in retrieved passages turns "make something up" into "answer from this evidence, with sources"

![The modern RAG pipeline: query rewriting, hybrid retrieval, reranking, context assembly, grounded generation](/images/blog/rag-pipeline-diagram.png "The modern RAG pipeline: query rewriting, hybrid retrieval, reranking, context assembly, grounded generation")

## The Modern Pipeline, Stage by Stage

### 1. Indexing (offline): chunking is where quality is decided

Documents get split into chunks, embedded, and stored. Chunking sounds mechanical; it's actually the highest-leverage decision in the system:

- **Fixed window + overlap** - 500-1,000 tokens, 10-20% overlap. The baseline. Works, but happily slices a paragraph mid-argument.
- **Semantic splitting** - break on sections, headings, paragraphs. Keeps meaning intact; chunk sizes vary.
- **The modern default: structure-aware** - split on document structure first (headings, sections), cap size second. Tools like [MarkItDown](/blog/markitdown-microsoft-convert-files-markdown-llm) exist precisely to convert PDFs into clean markdown *so the structure survives* to inform chunking.

One chunk, one idea. A chunk answering half a question retrieves well and answers badly.

### 2. Retrieval: hybrid beats either alone

- **Vector search** - embed the query, find nearest chunks by cosine similarity. Catches paraphrase: "login system" matches "authentication middleware."
- **Keyword search (BM25)** - exact term matching. Catches what embeddings fumble: `auth.ts`, error codes, product SKUs, names.
- **Hybrid** - run both, merge. Same conclusion as in [agent memory retrieval](/blog/agent-memory-systems-guide): either alone leaves recall on the table. Every serious 2026 stack ships hybrid.

Worth stealing from the research: **query rewriting**. Questions and answers have different shapes in embedding space - "how do we handle auth?" sits far from "JWT validation in middleware, 24h expiry." HyDE fixes this by having the model draft a hypothetical answer first and searching with *that*. The fake answer is wrong but answer-shaped, and shape is what similarity measures.

### 3. Reranking: cheap pass, then expensive pass

Vector search scores query and chunk *independently* - fast but coarse. A reranker (a cross-encoder) reads the query and each candidate *together* and scores actual relevance. Too slow for millions of chunks, perfect for re-scoring the top 50.

TIP

The cascade - cheap retrieval over everything, expensive reranking over candidates - typically lifts answer quality more than any embedding model swap. If you add one component to a basic pipeline, add this.

### 4. Assembly + generation: don't undo your own work

You retrieved five good chunks; now don't ruin it in the prompt. Order matters (relevant-first - models attend more to context edges), labels matter (`[Source 3: pricing-policy.md]` enables citations), and instructions matter: *"Answer from the provided sources. If they don't contain the answer, say so."* That last line is the anti-hallucination payload - skip it and the model pads retrieval gaps with fiction, now wearing the costume of a grounded answer.

---

## Why Classic RAG Is Losing Ground

LlamaIndex founder Jerry Liu put it bluntly: retrieval isn't dead, but **the fixed chunk+embedding pattern is**. The 2023 recipe - shred everything to 500-token pieces, embed, hope - has known failure modes: retrieved fragments missing their surrounding context, no view of document-level structure, single-shot retrieval that can't recover from a bad first fetch.

What's replacing it is **agentic retrieval**: give the model retrieval *tools* and let it search, read results, refine, and search again. Claude Code is the existence proof - it answers codebase questions with grep and targeted file reads, no vector index in sight. The agent expands context around hits dynamically, which makes obsessing over chunk size pointless. The [progressive disclosure](/blog/agent-skills-best-practices-guide) pattern in Skills is the same philosophy: index first, fetch on demand.

The honest trade: agentic retrieval is slower and burns more tokens per query; classic RAG is fast and cheap per query but dumber. High-volume FAQ bot → classic pipeline. Complex research over messy documents → agentic. Hybrid (cheap retrieval as a *tool* the agent can call repeatedly) is increasingly the answer.

---

## A Concrete Starting Stack

For a Next.js/Supabase builder, the no-new-infrastructure version:

1. **Store:** Supabase Postgres + pgvector - embeddings live next to your relational data, one fewer service
2. **Index:** convert docs to markdown (MarkItDown for PDFs), structure-aware chunks ~800 tokens, embed, insert
3. **Retrieve:** pgvector cosine similarity + Postgres full-text search, merged - hybrid in ~30 lines of SQL
4. **Generate:** top 5 chunks, labeled, with the "say so if sources don't cover it" instruction

Ship that, measure where it fails on real queries, and only then add reranking, query rewriting, or agentic loops. The fancy stages earn their complexity with evidence - which, conveniently, is the subject of [how to evaluate AI agents](/blog/how-to-evaluate-ai-agents).

---

## The Takeaway

Small static corpus → context. Large or changing corpus → RAG. Behavior change → fine-tuning. Build the boring hybrid pipeline first, treat chunking as the real design decision, add a reranker before you swap embedding models, and watch the agentic pattern - because the librarian is learning to browse the shelves herself.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
