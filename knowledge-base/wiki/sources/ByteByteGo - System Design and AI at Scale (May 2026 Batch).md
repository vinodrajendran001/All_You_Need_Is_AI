---
type: source-summary
source_id: src-2026-05-21-bytebytego-batch
source_title: "ByteByteGo - System Design and AI at Scale (May 2026 Batch)"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com
created: 2026-05-21
updated: 2026-05-21
tags:
  - source-summary
  - system-design
  - machine-learning
  - ai-at-scale
  - architecture
status: active
---

# ByteByteGo - System Design and AI at Scale (May 2026 Batch)

## Overview

This composite source covers eight ByteByteGo / Alex Xu newsletter articles clipped together in May 2026. As a batch, they map a recurring production pattern: keep hot paths simple, push expensive computation off the critical path, standardize interfaces between modules, and let retrieval, ranking, caching, and human review absorb complexity at the edges.

The articles span multimodal video search at Netflix, billion-prediction ML serving at Snap, AI-agent workflows at Grab and Figma, commonsense recommendations at Amazon, hybrid search at Instacart, workflow modularity at DoorDash, and architecture trade-offs across monoliths, microservices, and serverless systems.

## Per-article summaries

### 1. How Netflix is Using Multimodal AI to Power Video Search

Netflix treats multimodal video search as a data-fusion problem more than a single-model problem. A season can produce roughly 2,000 hours of footage, or about 216 million frames, so the production system uses a three-stage pipeline instead of trying to search raw model outputs directly.

- **Stage 1: transactional persistence** stores raw annotations from specialist models in Apache Cassandra with zero transformation so ingest throughput never blocks on downstream computation.
- **Stage 2: offline fusion** maps heterogeneous model outputs into fixed one-second temporal buckets, intersects annotations inside each bucket, and upserts a single fused record per `(asset_id, time_bucket)`.
- **Stage 3: real-time indexing** writes fused buckets to Elasticsearch as nested documents so queries can match character labels, dialogue text, and scene embeddings inside the same parent interval.
- Query-time search is explicitly **hybrid**: exact keyword matching for proper nouns, vector similarity for scene semantics, phrase/slop search for dialogue, and a user-visible toggle between exact k-NN and ANN retrieval.
- Netflix exposes **union vs intersection retrieval modes**, plus post-processing that reconstructs natural clip boundaries from one-second buckets so editors see coherent scenes rather than arbitrary slices.

The main architectural lesson is that multimodal AI becomes operational only after persistence, temporal alignment, and indexing are cleanly separated.

### 2. How Snapchat Serves a Billion Predictions Per Second

Snap’s Bento platform is built for asymmetric ranking workloads where one user request fans out into hundreds or thousands of `(user, candidate)` scoring operations. The scale numbers define the architecture: more than **1 billion predictions per second**, **1 TB/s of feature reads**, and **10 trillion events per day** through the feature pipelines.

- Bento splits work into **retrieval** (cheap candidate generation) and **ranking** (expensive deep models), matching the classic production recommendation pipeline.
- The training side uses **Kubeflow** plus a layered code structure: shared Core framework, team-specific model code, and YAML configuration. This makes hundreds of experiments per day cheap to launch.
- Model export is hardware-aware: **embedding lookups and feature parsing stay on CPU**, while dense matrix math runs on GPU.
- Snap’s Spark-based feature platform, **Robusta**, keeps offline Iceberg features and the online key-value store synchronized to reduce train/serve skew. The online store alone holds about **800 TB**.
- Bento uses two serving strategies for high fanout: **feature collocation** on inference nodes when the corpus fits in memory, or a separate **Retrieval service** that combines ANN, inverted-index, and forward-index lookups when it does not.
- Data-plane work mattered as much as model work: moving feature transfer closer to raw bytes and optimizing Protobuf handling delivered **2x lower latency** and **10x cheaper data-plane cost**.

This is a strong example of production ML where the serving platform, not just the model, is the main innovation surface.

### 3. How Grab is Using AI Agents to Boost Team Productivity

Grab’s Analytics Data Warehouse team turned a repeated human investigation workflow into a production multi-agent system. The team manages **15,000+ tables** used by roughly **1,000 monthly internal users**, and its best engineers had been losing two full days each week to support-style questions.

- Grab explicitly **decouples the brain from the hands**: the LLM handles reasoning, while tools and specialist agents fetch metadata, trace lineage, run SQL, and inspect operational health.
- The production stack uses **FastAPI** for request handling, **LangGraph** for cyclical multi-agent orchestration, **Redis** for session/cache needs, and **PostgreSQL** for conversation history and metadata.
- Investigation work is routed through a **Classifier**, **Data Agent**, **Code Search Agent**, **On-call Agent**, and **Summarizer Agent**. Write actions go down a separate, human-gated **Enhancement Agent** path.
- The system’s most important production lessons came from failures: context overflow across agent handoffs, tool bloat, risky SQL/code execution, and lack of user trust.
- Grab addressed those with token tracking, aggressive context pruning, slimmer tool descriptions, multi-layer SQL and PII guardrails, staging-only enhancement flows, and visible human review controls.
- Reported impact: bots now handle most routine inquiries, resolution time fell by an **order of magnitude**, and the team recovered multiple FTEs’ worth of engineering time.

The article shows that production agents are mostly workflow, tooling, safety, and review engineering.

### 4. Figma Design to Code, Code to Design Clearly Explained

Figma frames its MCP server as the middle ground between two failed extremes: screenshot-only prompting (visually approximate but imprecise) and raw Figma JSON dumps (precise but too noisy and token-heavy).

- The MCP server turns raw design data into an **LLM-friendly structured representation**: layout relationships instead of raw coordinates, design-token references instead of literal hex codes, and flattened layer structure that better matches how developers think.
- In the **design-to-code** flow, agents discover tools such as `get_design_context`, `get_screenshot`, and `get_metadata`, parse node IDs from Figma URLs, then request transformed design context instead of raw API responses.
- **Code Connect** attaches Figma components to concrete code file paths so the model can reuse existing UI components rather than regenerating them.
- In the **code-to-design** flow, `generate_figma_design` captures a live DOM rather than a screenshot, walks computed styles and hierarchy, and reconstructs native Figma layers with auto-layout, editable text, and image fills.
- Token budget is a first-class systems concern: Figma documents a **scan first, then zoom in** pattern using `get_metadata` before `get_design_context`, partly because Claude Code’s default MCP tool-response limit is around **25,000 tokens**.
- The roundtrip is intentionally **lossy**. Visual structure can move between code and design, but business logic, state, and API integration do not survive the trip and must be re-inferred.

The article is one of the clearest concrete descriptions of how MCP servers create useful context by shaping data, not merely exposing an API.

### 5. How Amazon Uses LLMs to Recommend Products

Amazon’s COSMO system addresses the semantic gap between what users type and what product catalogs explicitly say. The key idea is a **commonsense knowledge graph** that encodes why a shopper might want a product, not just what the product is.

- Amazon sampled **3.14 million co-purchase pairs** and **1.87 million query-purchase pairs** across **18 product categories**, then used internal deployments of **OPT-175B and OPT-30B** on **16 A100 GPUs** because customer-behavior data could not leave Amazon infrastructure.
- LLM generation alone was too noisy: only about **35%** of search-buy explanations and **9%** of co-purchase explanations met Amazon’s quality bar before filtering.
- Amazon built a multi-stage refinement pipeline: rule-based cleanup, embedding-similarity filtering, **30,000 human annotations**, and classifier generalization with **DeBERTa-large** plus an in-house model.
- The result is a commonsense graph with roughly **6.3 million nodes** and **29 million edges**, organized around **15 relation types** mined from actual model outputs.
- Amazon then instruction-tuned **LLaMA 7B and 13B** into **COSMO-LM**, a smaller model that can generate and score commonsense knowledge in production without running the full giant-model-plus-classifier stack each time.
- Serving uses a **feature store** plus a two-tier **asynchronous cache**: yearly frequent queries are preloaded, newer requests are batch-processed daily, and **SageMaker** manages daily refreshes.
- Reported impact includes improved benchmark performance, an **8% increase in navigation engagement**, and about a **0.7% relative increase in product sales** on a 10% U.S. traffic experiment, worth hundreds of millions in annualized revenue.

COSMO is a useful example of LLMs in production as knowledge-generation infrastructure, not just chat interfaces.

### 6. How Instacart Built a Search for Billions of Products

Instacart’s search problem is shaped by a combination of **billions of items**, **millions of searches per day**, and **billions of writes per day** because grocery data changes constantly.

- Elasticsearch initially fit the keyword-search problem but mismatched Instacart’s write-heavy workload because denormalized documents had to be fully rewritten when any field changed.
- Moving search into **Postgres** with normalized tables reduced write amplification by about **10x** and let the team store large ML-feature tables close to retrieval data.
- Semantic retrieval first lived in a separate **FAISS** service, creating a two-system architecture: Postgres for keywords, FAISS for vectors, and an application-layer merge step.
- That design improved relevance but created operational sync overhead, weak attribute filtering, and a ceiling on how well lexical and semantic signals could be fused.
- Instacart later consolidated on **pgvector**, keeping vectors and relational filters in the same datastore. This enabled **pre-filtering for in-stock items before ANN search**, improved recall, and simplified operations.
- Prototype testing showed pgvector met production latency/throughput needs with better recall than FAISS, and production A/B tests showed a **6% drop in zero-result searches**.
- The broader principle is explicit in the article: **bring the compute to the data**. Consolidation roughly doubled search speed because joins and filters moved inside the database rather than across multiple network hops.

This article is a strong production case for hybrid lexical-plus-vector search built around workload fit rather than fashionable infrastructure choices.

### 7. EP210 Monolithic vs Microservices vs Serverless

This newsletter issue packages several diagrams, but the durable architecture takeaway is its concise comparison of three common deployment styles.

- **Monoliths** optimize for early simplicity: one codebase, one database, one deployment. They are often the right default for small teams.
- **Microservices** buy independent scaling and deployability at the cost of service discovery, distributed tracing, request routing, and more coordination overhead.
- **Serverless** shifts server management to the cloud provider and often improves elasticity/cost for event-driven workloads, but cold starts, debugging complexity, and provider lock-in become meaningful trade-offs.
- The article’s practical recommendation is hybrid rather than ideological: many mature systems keep a monolithic core, carve out a few independently scaled services where justified, and use serverless selectively for tasks like notifications or background jobs.

For this vault, the article matters because it reinforces the workload-first design attitude also visible in the other seven articles.

### 8. How DoorDash Launches a New Country in One Week

DoorDash’s unified Dasher onboarding platform shows how modular system design compounds operationally once country-specific branching becomes the dominant source of complexity.

- The new architecture uses three layers: a **thin Orchestrator** that routes by country/market, **Workflow Definitions** that specify ordered step lists, and **Step Modules** that own actual business logic behind standardized interfaces.
- Steps are reusable because they are workflow-agnostic and share a contract: process the step, report whether it is complete, and return response data.
- The system supports **composite steps** and **conditional/dynamic steps**, so markets can group or repeat logic without rewriting the underlying modules.
- State moved from scattered tables into a single JSON **status map**, where each step owns its own status entry and updates it atomically.
- Migration ran side by side with legacy V2/V3 flows until completion, which let new and old systems coexist safely during rollout.
- The compounding outcome was dramatic: the U.S. migration proved the design, then **Australia finished in under a month**, **Canada in two weeks**, **Puerto Rico in one week**, and **New Zealand with almost no new development**, all with zero regressions.

The article is a reminder that interface design and modularity can matter more than deployment topology; DoorDash’s reusable steps are modules inside one service, not a fleet of microservices.

## Cross-cutting themes

### ML serving at scale is mostly systems work

Netflix, Snap, Amazon, and Instacart all show the same pattern: the hard part is not merely training a model. It is choosing the right decomposition between ingest, feature computation, retrieval, ranking, caching, and feedback loops.

### Hybrid retrieval beats single-technique purity

Keyword search, vector search, knowledge graphs, feature stores, and caches repeatedly appear together rather than separately. Netflix mixes lexical and vector retrieval. Instacart mixes BM25-style text search with ANN. Amazon combines a static knowledge graph with an instruction-tuned model and cached serving.

### LLMs in production need narrower interfaces than demos suggest

Grab and Figma both emphasize context and tool design over raw model capability. Token budgets, tool descriptions, state handoffs, and human review determine whether the system is operationally useful.

### Architecture decisions should match workload shape

Instacart moved away from Elasticsearch because of write amplification. Snap split CPU and GPU work because embeddings and dense layers stress different hardware resources. DoorDash kept reusable steps inside one service rather than over-distributing them. The architecture article makes this principle explicit: most real systems are hybrids.

### Thin orchestrators and explicit boundaries recur everywhere

DoorDash’s orchestrator, Grab’s classifier-plus-specialists pattern, Figma’s MCP boundary, and Netflix’s three-stage pipeline all keep control layers narrow while pushing domain-specific work into modules with clear contracts.

## Affected pages

- [[ByteByteGo]]
- [[ML Systems at Scale]]
- [[AI Agents in Production]]
- [[Agentic Loop]]
- [[Model Context Protocol]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[AI Knowledge Base Overview]]
- [[index|Knowledge Base Index]]
- [[log|Knowledge Base Log]]

## Raw captures

- `knowledge-base/raw/sources/How Netflix is Using Multimodal AI to Power Video Search.md`
- `knowledge-base/raw/sources/How Snapchat Serves a Billion Predictions Per Second.md`
- `knowledge-base/raw/sources/How Grab is Using AI Agents to Boost Team Productivity.md`
- `knowledge-base/raw/sources/Figma Design to Code, Code to Design Clearly Explained.md`
- `knowledge-base/raw/sources/How Amazon Uses LLMs to Recommend Products.md`
- `knowledge-base/raw/sources/How Instacart Built a Search for Billions of Products.md`
- `knowledge-base/raw/sources/EP210 Monolithic vs Microservices vs Serverless.md`
- `knowledge-base/raw/sources/How DoorDash Launches a New Country in One Week.md`

## Related pages

- [[ByteByteGo]]
- [[ML Systems at Scale]]
- [[AI Agents in Production]]
- [[Agentic Loop]]
- [[Model Context Protocol]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[AI Knowledge Base Overview]]
