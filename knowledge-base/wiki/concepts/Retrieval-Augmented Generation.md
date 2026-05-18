---
type: concept
created: 2026-05-18
updated: 2026-05-18
tags: [rag, retrieval, agents, knowledge-graphs, llm]
source_ids:
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
status: active
---

# Retrieval-Augmented Generation

The general pattern of improving LLM outputs by **retrieving external context at inference time** and conditioning generation on that context instead of relying only on the model's parametric memory.

## Core idea

In its simplest form, RAG means: retrieve relevant information, place it into the model context, then generate an answer grounded in that evidence. The key advantage is freshness and specificity: the system can use information that is too recent, too specialized, or too large to fit reliably inside model weights alone.

RAG is best treated as a **family of architectures**, not a single pipeline. As retrieval problems become more relational or more reasoning-heavy, the retrieval layer tends to evolve from fixed vector search into graph traversal and then into agentic, multi-step search.

## Three tiers of RAG

### 1. Classic RAG

The standard pipeline is:

```text
Query → Embed → Vector DB → Top-K Chunks → LLM → Answer
```

This is the default pattern for document-grounded QA. It is fast, relatively cheap, and often good enough when the answer is already written in one or two source passages.

Typical use cases:
- support bots
- policy lookup
- documentation assistants
- HR or operations FAQs

Primary limitation: it retrieves by **semantic similarity**, so it may miss answers that depend on explicit relationships across entities, records, or events.

### 2. Graph RAG

Graph RAG adds an intermediate structure layer:

```text
Query → Entity Extraction → Knowledge Graph → Connected Context → LLM → Answer
```

Here the system retrieves not only similar text but also the edges between entities. This matters when the answer depends on who is connected to whom, what belongs to what, or how multiple facts compose into a structured view.

Typical use cases:
- fraud and anomaly investigation
- legal or compliance entity mapping
- supply-chain or organizational relationship tracing

The ingested comparison source also notes that LazyGraphRAG (Microsoft, 2025) reportedly reduces graph retrieval cost to 0.1% of earlier approaches, making graph-backed retrieval more operationally plausible.

### 3. Agentic RAG

Agentic RAG turns retrieval into a tool-using control loop:

```text
Query → Reasoning Agent → Vector DB + Knowledge Graph + Tools → Self-Evaluation → Answer
```

Instead of a single fixed retrieval step, the model decides what to search, calls tools, evaluates results, and iterates when the first pass is incomplete. This is the RAG tier most closely aligned with modern agents.

Typical use cases:
- research workflows
- contract analysis
- enterprise support across many systems
- complex, multi-source synthesis tasks

## Relation to search-augmented LMs

[[Search-Augmented Language Models]] are a concrete instance of **Agentic RAG**. They do not merely retrieve context once; they learn a search policy that decides when to query the web, how many retrieval steps to take, and how to balance answer quality against tool cost.

Perplexity's training pipeline is especially important here because it shows that retrieval quality is not only a systems problem; it is also a post-training problem. The model must be optimized to use retrieval tools effectively.

## Relation to the agentic loop

[[Agentic Loop]] describes the generic plan-act-observe cycle behind multi-step tool use. Agentic RAG is that same loop specialized for retrieval: the plan is a search strategy, the actions are retrieval/tool calls, the observations are returned documents or structured results, and the loop may repeat until the evidence is sufficient.

## Relation to tool use

RAG is also a subtype of [[Tool Use and Function Calling]]. A vector store, search engine, SQL database, browser, or knowledge-graph query engine can all be exposed as tools. What changes across Classic, Graph, and Agentic RAG is how much control the model has over those tools and how many retrieval rounds it performs.

## Why the distinction matters

The three-tier framing prevents a common failure mode: diagnosing every weak retrieval system as "bad embeddings" when the real issue is architectural mismatch.

- If the answer is already present in a passage, **Classic RAG** is usually enough.
- If the answer depends on relationships, **Graph RAG** is a better fit.
- If the answer depends on iterative search and reasoning across sources, **Agentic RAG** is the right escalation.

## Related pages

- [[Classic RAG vs Graph RAG vs Agentic RAG]]
- [[Search-Augmented Language Models]]
- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[AI Knowledge Base Overview]]
