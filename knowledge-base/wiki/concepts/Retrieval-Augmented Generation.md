---
type: concept
created: 2026-05-18
updated: 2026-06-02
tags: [rag, retrieval, agents, knowledge-graphs, llm]
source_ids:
  - src-2026-05-18-rag-architecture-comparison
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-05-21-bytebytego-batch
  - src-2026-05-28-bytebytego-airtable-search
  - src-2026-06-02-alphasignal-look-past-rag-pipeline
status: active
---

# Retrieval-Augmented Generation

The general pattern of improving LLM outputs by **retrieving external context at inference time** and conditioning generation on that context instead of relying only on the model's parametric memory.

## Core idea

In its simplest form, RAG means: retrieve relevant information, place it into the model context, then generate an answer grounded in that evidence. The key advantage is freshness and specificity: the system can use information that is too recent, too specialized, or too large to fit reliably inside model weights alone.

RAG is best treated as a **family of architectures**, not a single pipeline. As retrieval problems become more relational or more reasoning-heavy, the retrieval layer tends to evolve from fixed vector search into graph traversal and then into agentic, multi-step search.

The new [[Direct Corpus Interaction]] source adds an important refinement: sometimes the next step beyond fixed vector retrieval is not a better retriever but a **higher-resolution interface to the raw corpus itself**.

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

## Production analogues beyond chatbots

Several production search and recommendation stacks look RAG-like even when they are not implemented as general-purpose chat systems.

- **Netflix** persists raw multimodal annotations, fuses them into one-second buckets, and retrieves them through hybrid keyword-plus-vector search before reconstructing useful clip spans.
- **Instacart** combines lexical and semantic retrieval with inventory-aware filtering, showing how retrieval pipelines depend on external operational state.
- **Amazon COSMO** pairs a knowledge graph with a smaller generation model and cache, effectively serving retrieved commonsense features to downstream ranking and navigation systems.
- **Airtable Omni** is a production example of classic RAG-like semantic retrieval over customer-owned tables: retrieve a small, relevant row set from a dedicated vector store, then pass only that slice downstream to the AI feature instead of exposing the full base.

These examples broaden the intuition behind RAG: the important pattern is not “chat over PDFs,” but **retrieve structured external context at inference time, then let a downstream model or ranking stage use it**.

Airtable also makes the infrastructure point explicit: once retrieval is multi-tenant and memory-heavy, partitioning strategy, ANN index economics, and hot/cold loading become first-class RAG design decisions rather than implementation details.

## Relation to the agentic loop

[[Agentic Loop]] describes the generic plan-act-observe cycle behind multi-step tool use. Agentic RAG is that same loop specialized for retrieval: the plan is a search strategy, the actions are retrieval/tool calls, the observations are returned documents or structured results, and the loop may repeat until the evidence is sufficient.

## Relation to tool use

RAG is also a subtype of [[Tool Use and Function Calling]]. A vector store, search engine, SQL database, browser, or knowledge-graph query engine can all be exposed as tools. What changes across Classic, Graph, and Agentic RAG is how much control the model has over those tools and how many retrieval rounds it performs.

## Direct corpus interaction and hybrid retrieval

The Alpha Signal DCI article argues that coding and IT-operations agents often fail under vector-only retrieval because the missing evidence is lexical or procedural rather than semantic: exact error strings, version constraints, file paths, and weak cross-file signals. If a vector index filters that evidence out before the agent begins reasoning, the loop starts from the wrong evidence set.

[[Direct Corpus Interaction]] is one answer. Instead of only retrieving chunks from an index, the agent can inspect the live corpus through terminal-like tools, refine its hypotheses, and search again. For large corpora, the article recommends a hybrid design: semantic retrieval for broad candidate discovery, then DCI for precise verification and local expansion.

## Why the distinction matters

The three-tier framing prevents a common failure mode: diagnosing every weak retrieval system as "bad embeddings" when the real issue is architectural mismatch.

- If the answer is already present in a passage, **Classic RAG** is usually enough.
- If the answer depends on relationships, **Graph RAG** is a better fit.
- If the answer depends on iterative search and reasoning across sources, **Agentic RAG** is the right escalation.

## Related pages

- [[Classic RAG vs Graph RAG vs Agentic RAG]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[ByteByteGo - How Airtable Built the Search Layer]]
- [[ML Systems at Scale]]
- [[Direct Corpus Interaction]]
- [[Search-Augmented Language Models]]
- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[AI Knowledge Base Overview]]
