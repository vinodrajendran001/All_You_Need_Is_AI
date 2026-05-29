---
type: overview
created: 2026-05-08
updated: 2026-05-29
tags:
  - overview
  - ai
  - knowledge-base
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
status: active
---

# AI Knowledge Base Overview

## Scope

This wiki is the persistent knowledge layer for the `All_You_Need_Is_AI` vault. It is meant to accumulate sources, syntheses, and durable answers about AI instead of rediscovering them from scratch on every query.

## Current picture

The workspace now implements Karpathy's three-layer pattern:

- Raw sources live under `knowledge-base/raw/`.
- Curated wiki pages live under `knowledge-base/wiki/`.
- The operating schema lives in the root `CLAUDE.md` note.

The first source in the system is [[Andrej Karpathy - LLM Wiki]], which establishes the baseline operating model for future ingests. The second source, [[Kevin Murphy - Reinforcement Learning - An Overview]], seeds the first domain-specific branch of the wiki around [[Reinforcement Learning]]. The third source, [[ByteByteGo - Connecting LLMs to the Real World]], opens the **LLM tooling and agents** branch covering [[Tool Use and Function Calling]], [[Model Context Protocol]], and the [[Agentic Loop]]. The fourth source, [[Perplexity - Advancing Search-Augmented Language Models]], deepens the RL and agents area with a concrete production pipeline for [[Search-Augmented Language Models]] and introduces [[Reward Design for RL]] as a cross-cutting concept. The fifth source, [[Alpha Signal - The Return of Recursion]], adds a new branch around [[Latent-Space Reasoning]] and [[Recursive Architectures]], framing recursive computation as a complementary path to faster, lower-cost reasoning systems. The sixth source, [[The Pocket - PocketFlow Tutorial Docs]], adds a major tutorial library covering LLM internals, LLM training pipelines, reinforcement-learning methods, and mathematical foundations, and it seeds [[Transformer Architecture]], [[LLM Training Pipeline]], [[Neural Network Fundamentals]], and [[Model Quantization and Efficiency]]. The seventh source, [[Han Fang - PyTorch Practice]], reinforces that practical deep-learning branch with a compact interview-oriented PyTorch repo full of runnable from-scratch implementations for optimization, normalization, attention, training-loop mechanics, and model-efficiency techniques. The eighth source, [[Classic RAG vs Graph RAG vs Agentic RAG]], adds a retrieval-architecture taxonomy that unifies Classic, Graph, and Agentic RAG under the new hub page [[Retrieval-Augmented Generation]]. The ninth source, [[Universal LeetCode Templates]], expands the interview-preparation branch beyond ML implementation drills into reusable DSA problem-solving patterns, and it seeds [[Algorithm Templates for Interviews]] as a bridge between LeetCode-style template selection and [[Han Fang - PyTorch Practice]]. The tenth source, [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]], broadens the vault into production system design and ML-at-scale, seeding [[ML Systems at Scale]] and [[AI Agents in Production]] while connecting AI concepts to real architectures at Netflix, Snap, Amazon, Instacart, Grab, Figma, and DoorDash. The eleventh source, [[ByteByteGo - How Airtable Built the Search Layer]], deepens the retrieval branch with a concrete vector-search infrastructure case study around Milvus partitioning, HNSW latency/recall tradeoffs, and hot/cold memory tiering for Airtable's AI features. The twelfth source, [[DoorDash - LLM-as-a-Judge for Search Evaluation]], opens a new evaluation branch around [[LLM-as-a-Judge]], showing how facet-based rubrics, calibration, and continuous automated judging can replace noisy periodic annotation for natural-language search.

## Key pages

- [[index|Knowledge Base Index]] - main entry point into the wiki
- [[Persistent Wiki]] - the central idea behind the whole system
- [[Schema-Driven Knowledge Base]] - how the schema keeps maintenance disciplined
- [[Ingest Query Lint Loop]] - the repeating maintenance cycle
- [[Index and Log]] - control files that help the LLM navigate the vault
- [[Reinforcement Learning]] - first domain hub page seeded from an ingested paper
- [[Transformer Architecture]] - decoder-only Transformer blueprint plus attention, RoPE, and KV-cache synthesis
- [[LLM Training Pipeline]] - pretraining, SFT, RLHF, DPO, and LoRA as one connected map
- [[Neural Network Fundamentals]] - gradient descent, backpropagation, PyTorch, and Adam as the substrate under higher-level model pages
- [[Algorithm Templates for Interviews]] - template-selection map connecting classic DSA interview patterns with ML engineering preparation
- [[Model Quantization and Efficiency]] - quantization, KV cache, and LoRA as deployment/adaptation efficiency levers
- [[Tool Use and Function Calling]] - how LLMs request real-world actions
- [[Model Context Protocol]] - open standard for universal tool integration
- [[Agentic Loop]] - the iterative cycle powering multi-step tool use
- [[Search-Augmented Language Models]] - LLMs with RL-trained search tool policies
- [[Retrieval-Augmented Generation]] - Classic, Graph, and Agentic RAG as a single retrieval-architecture map
- [[Reward Design for RL]] - composite reward signals for multi-objective LLM training
- [[Group Relative Policy Optimization]] - relative-policy optimisation method used in the Perplexity RL stage
- [[Latent-Space Reasoning]] - reasoning through internal latent states instead of explicit token traces
- [[Recursive Architectures]] - modern recursive reasoning systems such as HRM, TRM, and RecursiveMAS
- [[ML Systems at Scale]] - production ML serving patterns spanning multimodal search, recommendation, hybrid retrieval, and vector-search infrastructure.
- [[LLM-as-a-Judge]] - calibrated LLM evaluators for search relevance, quality assurance, and continuous regression monitoring.
- [[AI Agents in Production]] - operational patterns for deploying agents with tool boundaries, MCP, guardrails, and human review.

## System design and ML-at-scale branch

- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]] adds a dedicated production-systems branch to the wiki.
- [[ByteByteGo - How Airtable Built the Search Layer]] adds a detailed vector-search infrastructure case study around Milvus partitioning, HNSW index selection, and hot/cold serving.
- [[ML Systems at Scale]] synthesizes shared serving patterns from Netflix, Snap, Amazon, Instacart, and now Airtable's semantic-search infrastructure.
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]] adds a production evaluation case study for natural-language search.
- [[LLM-as-a-Judge]] captures the calibrated-LLM-evaluator pattern as a durable concept.
- [[AI Agents in Production]] captures how Grab and Figma operationalize agents for data engineering and design↔code workflows.

## Gaps

- Existing notes elsewhere in the workspace have not yet been ingested into this structure.
- Reinforcement learning now has a denser hub page and stronger tutorial coverage, but its major subtopics are still not yet broken into dedicated notes.
- The `queries/` folder is active, `lint/` now has recurring reports, and `syntheses/` remains the least-developed content area.
- No search tooling has been added yet because the index is enough at the current scale.

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Obsidian]]
- [[Reinforcement Learning]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Search-Augmented Language Models]]
- [[Retrieval-Augmented Generation]]
- [[ML Systems at Scale]]
- [[LLM-as-a-Judge]]
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]]
- [[ByteByteGo - How Airtable Built the Search Layer]]
- [[AI Agents in Production]]
- [[Reward Design for RL]]
- [[Transformer Architecture]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Model Quantization and Efficiency]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Han Fang - PyTorch Practice]]
- [[Universal LeetCode Templates]]
- [[Algorithm Templates for Interviews]]
- [[Han Fang]]
- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[Alpha Signal - The Return of Recursion]]
- [[Alpha Signal]]
- [[Perplexity]]
