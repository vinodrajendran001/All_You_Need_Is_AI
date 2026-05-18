---
type: source-summary
source_id: src-2026-05-18-rag-architecture-comparison
source_title: "Classic RAG vs Graph RAG vs Agentic RAG"
source_author: Unknown (LinkedIn post)
source_url: null
created: 2026-05-18
updated: 2026-05-18
tags:
  - source-summary
  - rag
  - retrieval-augmented-generation
  - knowledge-graphs
  - agentic-ai
status: active
---

# Classic RAG vs Graph RAG vs Agentic RAG

## Summary

This short source argues that "RAG" is not a single architecture but a family of retrieval patterns matched to different problem shapes. Its practical framing is a three-tier ladder: **Classic RAG** for straightforward document lookup, **Graph RAG** for relationship-aware retrieval, and **Agentic RAG** for multi-step reasoning across heterogeneous sources.

The durable takeaway is that these architectures are **complementary rather than competitive**. The right choice depends on whether the task mainly needs semantic similarity, explicit relational structure, or iterative reasoning.

## Durable claims

1. **Classic RAG covers most routine retrieval needs** — the post claims roughly 70% of use cases can be handled by the standard `query → embed → vector DB → top-K chunks → LLM → answer` pipeline.
2. **Classic RAG breaks down on relationships** — similarity search can surface relevant passages, but it does not represent how entities or facts connect.
3. **Graph RAG adds structure-aware retrieval** — it inserts entity extraction and knowledge-graph traversal before generation so the retrieved context preserves relationships.
4. **Graph retrieval is becoming cheaper** — the post cites LazyGraphRAG (Microsoft, 2025) as reducing graph retrieval cost to 0.1% of prior approaches, making graph-backed retrieval more practical at scale.
5. **Agentic RAG introduces a reasoning policy** — instead of one fixed retrieval pass, an agent decides what to search, which tools to call, how to evaluate results, and whether another step is needed.
6. **Agentic RAG suits multi-source, multi-step work** — examples include research workflows, contract analysis, enterprise support, and other questions where one retrieval hop is insufficient.
7. **Architecture choice should follow task structure** — simple lookup favours Classic RAG, relationship-centric tasks favour Graph RAG, and reasoning-heavy tasks favour Agentic RAG.

## Pipeline map

### Classic RAG

```text
Query → Embed → Vector DB → Top-K Chunks → LLM → Answer
```

Best fit: support bots, policy lookup, HR FAQs, and other cases where the answer already sits in a document and the user query is relatively direct.

### Graph RAG

```text
Query → Entity Extraction → Knowledge Graph → Connected Context → LLM → Answer
```

Best fit: fraud detection, legal entity mapping, and other settings where relationships between people, organizations, events, or facts are part of the answer.

### Agentic RAG

```text
Query → Reasoning Agent → Vector DB + Knowledge Graph + Tools → Self-Evaluation → Answer
```

Best fit: research, contract review, enterprise support, and broader multi-source questions that need iterative search and verification.

## Why it matters

This source is useful because it gives the vault a simple taxonomy for retrieval systems. It separates three design choices that are often blurred together under the blanket term "RAG":

- **retrieval by similarity**
- **retrieval by explicit relationships**
- **retrieval plus iterative reasoning**

That taxonomy links naturally to [[Search-Augmented Language Models]], [[Agentic Loop]], and [[Tool Use and Function Calling]], because production retrieval systems increasingly act like tool-using agents rather than single-pass context stuffing pipelines.

## Affected pages

- [[Retrieval-Augmented Generation]]
- [[Search-Augmented Language Models]]
- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[AI Knowledge Base Overview]]
- [[index|Knowledge Base Index]]

## Raw capture

`knowledge-base/raw/sources/Classic RAG vs Graph RAG vs Agentic RAG.md`

## Related pages

- [[Retrieval-Augmented Generation]]
- [[Search-Augmented Language Models]]
- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
