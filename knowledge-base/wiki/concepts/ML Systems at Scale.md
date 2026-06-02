---
type: concept
created: 2026-05-21
updated: 2026-06-02
tags:
  - concept
  - machine-learning
  - system-design
  - scale
source_ids:
  - src-2026-05-21-bytebytego-batch
  - src-2026-05-28-bytebytego-airtable-search
  - src-2026-05-28-doordash-llm-judge
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-05-29-braintrust-multi-turn-scoring
status: active
---

# ML Systems at Scale

Production ML systems stop looking like isolated models and start looking like multi-stage serving pipelines. Across Netflix, Snap, Amazon, and Instacart, the winning pattern is consistent: retrieve or generate a manageable candidate set, enrich it with features or knowledge, score it under a strict latency budget, and keep the expensive work off the synchronous user path whenever possible.

## Shared serving shape

A common production decomposition appears across all four systems:

1. **Candidate generation / retrieval** narrows a huge corpus quickly.
2. **Feature or knowledge enrichment** attaches the context needed for more expensive reasoning.
3. **Ranking or final retrieval** applies heavier models or more precise search.
4. **Caching, feedback, or refresh loops** keep the system economically sustainable.

Snap makes this explicit through retrieval then ranking inside Bento. Netflix does the same structurally by persisting raw annotations, fusing them offline, then serving hybrid search over fused buckets. Instacart combines keyword and ANN retrieval before downstream ranking. Amazon precomputes commonsense edges and then serves them through COSMO-LM, a feature store, and a cache instead of invoking giant models on every request.

## Data locality matters more than model elegance

At scale, latency often comes from moving data around rather than from the model itself.

- Snap cut inference cost by splitting **embedding lookups to CPU** and **dense math to GPU**, then reduced latency further by shipping feature data as raw bytes with optimized Protobuf handling.
- Instacart roughly doubled search speed by moving joins and filtering into Postgres: **bring the compute to the data**.
- Amazon’s two-tier cache exists because even a good smaller model is too expensive to run synchronously for every search.
- Netflix accepts offline fusion delay so that cross-modal intersection work never blocks ingestion or interactive search.
- The Reiner Pope flashcards show the same locality law at cluster scale: an MoE layer naturally fits within one NVLink-connected rack because expert routing is all-to-all, while cross-rack bandwidth turns the same pattern into a bottleneck.

This is the practical face of ML systems engineering: placement of data and computation often dominates algorithm choice.

## Embeddings are the common substrate

The surface tasks differ, but embeddings show up everywhere:

- Netflix stores scene embeddings to support semantic video search.
- Snap relies on embedding-heavy ranking models and ANN-style retrieval services for large corpora.
- Amazon uses embeddings to filter out generated commonsense statements that are just paraphrases of the original query or product text.
- Instacart uses vector search to recover intent for vague grocery queries such as “healthy foods.”
- Airtable's Omni search layer stores per-base embeddings in self-hosted Milvus because the vectors are about 10x the size of the source rows and need dedicated ANN infrastructure.

Even when systems are not called “RAG,” they increasingly operate like retrieval systems over learned representations.

## Hybrid retrieval is the default, not the exception

Pure keyword and pure vector search both lose important signal.

- Netflix needs exact matching for named entities like characters, but semantic retrieval for settings and scene meaning.
- Instacart needs exact matching for precise product queries and ANN retrieval for intent-heavy search.
- Amazon needs symbolic knowledge-graph edges plus model-generated commonsense features.

The durable pattern is **hybrid retrieval**: lexical constraints for precision, learned representations for recall, and domain filters to keep results operationally relevant.

## Recommendation systems need world knowledge

Amazon’s COSMO shows a limit of classic recommendation systems: product attributes and collaborative signals do not fully capture *why* people want something. Commonsense relations such as audience, location, event, or function become missing retrieval features. That pushes production recommenders toward richer knowledge layers, whether those layers are explicit graphs, cached model outputs, or engineered features.

Snap’s ranking stack reaches a similar conclusion from another direction. The system is not just predicting relevance; it is serving an evolving approximation of user intent under freshness, cost, and experimentation pressure.

## Freshness, throughput, and precision trade against each other

These systems repeatedly make explicit trade-offs:

- Netflix chooses **offline fusion** over instant multimodal freshness.
- Snap balances smaller models, cheaper compute, and faster iteration against ever-growing model size and traffic.
- Amazon refreshes COSMO daily, accepting weaker real-time adaptability in exchange for predictable serving economics.
- Instacart consolidates into Postgres/pgvector for simpler filtering and recall, but acknowledges scale ceilings for very large vector indexes.
- Reiner Pope’s flashcards sharpen the training-side version of the same tradeoff: pipeline parallelism reduces some placement pressure but introduces bubbles, weak KV-cache savings at long context, and even model-architecture constraints that slow research iteration.

There is no universally best architecture; there are only architectures that fit the workload and the operational budget.

Airtable's Omni search layer sharpens that point. One partition per customer base simplified isolation and deletion, but only remained manageable because Airtable capped Milvus at 400 collections × 1,000 partitions, chose memory-hungry HNSW to hit sub-500 ms p99 latency with 99%+ recall, and then used hot/cold unloading so idle tenants did not consume RAM continuously.

## Evaluation infrastructure is production infrastructure

Serving stacks are only half of the story. [[DoorDash - LLM-as-a-Judge for Search Evaluation]] shows that once search quality depends on compositional natural-language intent, the evaluation loop itself becomes a system component. Explicit rubrics, adjudicated golden sets, and a calibrated [[LLM-as-a-Judge]] can be run daily for monitoring and PR guardrails, replacing slower human-only review cycles.

That is a production-systems lesson, not just an evaluation anecdote: if quality measurement cannot keep up with model and ranking changes, the rest of the stack loses its feedback loop.

The newer [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]] source pushes the same lesson into chatbot development. There, evaluation infrastructure includes an offline customer simulator, transcript-derived scenarios, realistic mock backend state, binary trace-level LLM judges, and a release-gating pass-rate target. The system is not just scoring outcomes after the fact; it is actively shaping how quickly the product can improve.

[[Braintrust - How to evaluate multi-turn conversations]] complements that pattern with the lower-level mechanics of trace instrumentation and online scoring: group turns into one conversation object, score both turns and traces, and aggregate failures with clustering rather than relying on manual spot checks.

## Why this matters for AI infrastructure

These examples show that “ML at scale” is really a systems-discipline question. The model is only one component inside a broader architecture of stores, indexes, filters, ranking stages, caches, feedback loops, and evaluation infrastructure. That same architecture vocabulary also underlies [[Search-Augmented Language Models]] and many forms of [[Retrieval-Augmented Generation]], even when the end product is not a chatbot.

## Related pages

- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[ByteByteGo - How Airtable Built the Search Layer]]
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[Braintrust - How to evaluate multi-turn conversations]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[AI Accelerator Architecture]]
- [[ByteByteGo]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[AI Knowledge Base Overview]]
