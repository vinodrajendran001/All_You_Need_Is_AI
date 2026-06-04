---
type: index
created: 2026-05-08
updated: 2026-06-03
tags:
  - index
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
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-02-dwarkesh-eric-jang-flashcards
  - src-2026-06-02-dwarkesh-reiner-pope-chip-design
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-06-02-alphasignal-look-past-rag-pipeline
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-05-29-braintrust-multi-turn-scoring
  - src-2026-06-03-fareed-khan-train-llm-from-scratch
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-06-03-nvidia-locateanything
  - src-2026-06-04-efficient-reasoning-edge
status: active
---

# Knowledge Base Index

Start here. This file is the content-oriented routing layer for the wiki.

## Overviews

- [[AI Knowledge Base Overview]] - Workspace-specific orientation page for this persistent AI knowledge base.

## Concepts

- [[Persistent Wiki]] - The wiki as a durable knowledge layer that compounds over time.
- [[Schema-Driven Knowledge Base]] - Why a schema file turns a generic model into a disciplined maintainer.
- [[Ingest Query Lint Loop]] - The three recurring operations that keep the wiki alive.
- [[Index and Log]] - Why the catalog and ledger are first-class control surfaces.
- [[Reinforcement Learning]] - Hub page for sequential decision making and RL method families.
- [[Transformer Architecture]] - Decoder-only Transformer synthesis spanning attention, RoPE, and KV-cache inference.
- [[LLM Training Pipeline]] - Pretraining, SFT, RLHF, DPO, and LoRA as one post-training map.
- [[Neural Network Fundamentals]] - Gradient descent, backpropagation, PyTorch, and Adam as the substrate of modern models.
- [[Algorithm Templates for Interviews]] - Template-based approach to DSA and ML engineering interviews.
- [[Model Quantization and Efficiency]] - Quantization, KV cache, LoRA, and sparse activation as core efficiency levers.
- [[On-Device Reasoning]] - Local reasoning under phone/laptop-class memory, latency, and power limits.
- [[Tool Use and Function Calling]] - How LLMs request actions from external systems via structured function calls.
- [[Model Context Protocol]] - Open standard (Anthropic) that solves the N×M tool-integration problem.
- [[Agentic Loop]] - The iterative plan-act-observe cycle that enables multi-step LLM tool use.
- [[AI Agents in Production]] - Real-world deployment of AI agents for team productivity and design workflows.
- [[Search-Augmented Language Models]] - LLMs that use web search as part of generation, with RL-trained tool-use policies.
- [[ML Systems at Scale]] - Production ML serving patterns from Netflix, Snapchat, Amazon, Instacart, and Airtable.
- [[Retrieval-Augmented Generation]] - Hub page for Classic, Graph, and Agentic RAG architectures.
- [[Direct Corpus Interaction]] - Raw-file retrieval via terminal tools as a precision layer for agentic search.
- [[LLM-as-a-Judge]] - Using calibrated LLMs to evaluate search relevance and generation quality at scale.
- [[Multi-Turn Evaluation]] - Turn-level plus conversation-level scoring for simulated and live multi-turn systems.
- [[Mixture of Experts]] - Sparse architectures that activate only part of the network per token.
- [[Reward Design for RL]] - Constructing composite reward signals for multi-objective LLM training.
- [[Group Relative Policy Optimization]] - Relative-policy optimisation method used in the search-agent RL pipeline.
- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[World Models]] - Learned predictive models for planning, control, and embodied intelligence.
- [[Vision-Language Grounding]] - Text-conditioned spatial localization for objects, GUIs, documents, and scenes.
- [[Monte Carlo Tree Search]] - Search-time planning procedure that guides AlphaGo-style RL and clarifies dense supervision.
- [[Automated AI Research]] - Agentic research loops that automate experiments more readily than question selection.
- [[AI Accelerator Architecture]] - Hardware-level and cluster-level design tradeoffs behind AI compute.

## Entities

- [[Andrej Karpathy]] - Author of the pattern that seeded this implementation.
- [[ByteByteGo]] - Engineering newsletter; source for the tool-use and MCP article.
- [[Braintrust]] - Evaluation platform whose material in this vault focuses on multi-turn traces and online scoring.
- [[DoorDash]] - Delivery platform; source for LLM-as-a-Judge search evaluation and country-launch architecture.
- [[Fareed Khan]] - Repository author whose code-first LLM project ties Pile preprocessing, Transformer implementation, and training into one workflow.
- [[Han Fang]] - Author of the PyTorch Practice interview tutorial.
- [[Liquid AI]] - Model company focused here on sparse on-device assistants and local tool calling.
- [[NVIDIA]] - Research organization whose current source opens the multimodal grounding branch.
- [[Obsidian]] - The note environment that acts as IDE, browser, and graph surface for the wiki.
- [[Qualcomm AI Research]] - Mobile/edge deployment group focused here on efficient on-device reasoning.
- [[Perplexity]] - AI search company; source for the search-augmented LM training pipeline.
- [[Alpha Signal]]
- [[The Pocket]] - Organization behind PocketFlow and its tutorial-documentation curriculum.
- [[Y Combinator]] - Startup accelerator and publisher of YC Paper Club frontier-research sessions.
- [[Eric Jang]] - Researcher whose AlphaGo reconstruction ties together MCTS, RL, and autoresearch.
- [[Reiner Pope]] - Hardware researcher whose material ties chip design to LLM throughput and serving math.

## Sources

- [[Andrej Karpathy - LLM Wiki]] - Summary of the original `LLM Wiki` gist and its implications for this vault.
- [[Kevin Murphy - Reinforcement Learning - An Overview]] - Survey source that seeds the vault's RL area.
- [[ByteByteGo - Connecting LLMs to the Real World]] - Tool use, function calling, and MCP evolution from isolated LLMs to real-world agents.
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]] - Eight articles on production ML systems, AI agents, and architecture patterns.
- [[ByteByteGo - How Airtable Built the Search Layer]] - Vector search architecture with HNSW, hot/cold tiering, and hierarchical partitioning.
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]] - Facet-based LLM evaluation replacing noisy human annotation for NL search.
- [[Perplexity - Advancing Search-Augmented Language Models]] - Two-stage SFT→RL pipeline for training web search agents with gated rewards.
- [[Alpha Signal - The Return of Recursion]]
- [[Alpha Signal - As AI agents evolve, we need to look past the RAG pipeline]] - Argument that coding agents need higher-resolution corpus interfaces than vector-only RAG, motivating DCI and hybrid retrieval.
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]] - Support-chatbot simulation and evaluation flywheel with transcript-derived scenarios and LLM judges.
- [[Braintrust - How to evaluate multi-turn conversations]] - Operational recipe for turn-level and trace-level evaluation over grouped conversation traces.
- [[The Pocket - PocketFlow Tutorial Docs]] - Composite tutorial source spanning LLM internals, training pipelines, RL methods, and math foundations.
- [[Classic RAG vs Graph RAG vs Agentic RAG]] - Comparison of three RAG architecture tiers and their use cases.
- [[Han Fang - PyTorch Practice]] - Code-first PyTorch tutorial for ML engineer interview preparation.
- [[Universal LeetCode Templates]] - 20 battle-tested algorithm templates with pattern recognition and complexity analysis.
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]] - Frontier-research discussion session spanning inference, diffusion control, world models, generalization, and pretraining scaling.
- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]] - Long-form interview connecting AlphaGo, MCTS, RL-for-LLMs, and autoresearch loops.
- [[Dwarkesh Patel - Eric Jang Flashcards]] - Retrieval-oriented companion distilling MCTS, self-play, and AlphaZero training into compact Q/A form.
- [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]] - Blackboard lecture on AI chip design from logic gates to GPUs, TPUs, FPGAs, and memory hierarchy.
- [[Dwarkesh Patel - Reiner Pope Flashcards]] - Structured companion on LLM training/serving math, batching, memory bandwidth, MoE racks, and pipeline parallelism.
- [[Fareed Khan - Train LLM From Scratch]] - Code-first PyTorch repo for Pile preprocessing, decoder-only Transformer training, and text generation.
- [[Liquid AI - LFM2.5-8B-A1B]] - On-device MoE model emphasizing sparse inference, long context, multilingual tokenization, and local tool calling.
- [[NVIDIA - LocateAnything]] - Parallel Box Decoding framework for fast, high-quality visual grounding and detection.
- [[Efficient Reasoning on the Edge]] - End-to-end on-device reasoning pipeline with LoRA adapters, budget forcing, switcher routing, verifier-guided parallel decoding, and 4-bit deployment.

## Queries

- [[2026-05-08 Mathematical Foundations for Reinforcement Learning]] - Structured answer on the math stack needed to move from Murphy's survey to RL expertise.

## Lint reports

- [[2026-05-08 Wiki Lint Pass]] - Structural lint pass covering link integrity, schema conformance, and current wiki gaps.
- [[2026-05-13 Lint Pass]] - Comprehensive lint pass covering structural integrity, coverage, and immediate fixes.
- [[2026-05-13 Lint Pass 2]] - Follow-up lint pass after the Perplexity ingest, covering new-page integration and residual structural issues.
- [[2026-05-18 Lint Pass]] - Full-vault lint pass covering broken links, schema conformance, coverage gaps, and cross-link fixes.
- [[2026-05-18 Lint Pass 2]] - Post-ingest full wiki lint covering structural checks, raw-source coverage, and one overview staleness fix.
- [[2026-05-18 Lint Pass 3]] - Post-consolidation full wiki lint verifying structural integrity and Han Fang raw-source coverage.
- [[2026-05-21 Lint Pass]] - Seventh comprehensive lint pass covering full-wiki structural integrity after the Universal LeetCode Templates ingest.
- [[2026-05-21 Lint Pass 2]] - Eighth comprehensive lint pass covering full-wiki structural integrity after the ByteByteGo system-design batch ingest.
- [[2026-05-29 Lint Pass]] - Ninth comprehensive lint pass covering the full wiki after the Airtable search and DoorDash LLM-as-a-Judge ingests.
- [[2026-06-02 Lint Pass]] - Tenth comprehensive lint pass covering the post-Reiner wiki and fixing three thin entity pages.
- [[2026-06-02 Lint Pass 2]] - Eleventh comprehensive lint pass covering the expanded evaluation branch and finding no new structural defects.
- [[2026-06-03 Lint Pass]] - Twelfth comprehensive lint pass covering the sparse-model and multimodal-grounding expansions and finding no structural defects.

## Control files

- [[log|Knowledge Base Log]] - Chronological record of scaffolding, ingests, queries, and lint passes.
