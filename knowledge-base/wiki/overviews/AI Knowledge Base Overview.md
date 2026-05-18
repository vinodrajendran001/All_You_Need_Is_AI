---
type: overview
created: 2026-05-08
updated: 2026-05-18
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

The first source in the system is [[Andrej Karpathy - LLM Wiki]], which establishes the baseline operating model for future ingests. The second source, [[Kevin Murphy - Reinforcement Learning - An Overview]], seeds the first domain-specific branch of the wiki around [[Reinforcement Learning]]. The third source, [[ByteByteGo - Connecting LLMs to the Real World]], opens the **LLM tooling and agents** branch covering [[Tool Use and Function Calling]], [[Model Context Protocol]], and the [[Agentic Loop]]. The fourth source, [[Perplexity - Advancing Search-Augmented Language Models]], deepens the RL and agents area with a concrete production pipeline for [[Search-Augmented Language Models]] and introduces [[Reward Design for RL]] as a cross-cutting concept. The fifth source, [[Alpha Signal - The Return of Recursion]], adds a new branch around [[Latent-Space Reasoning]] and [[Recursive Architectures]], framing recursive computation as a complementary path to faster, lower-cost reasoning systems. The sixth source, [[The Pocket - PocketFlow Tutorial Docs]], adds a major tutorial library covering LLM internals, LLM training pipelines, reinforcement-learning methods, and mathematical foundations, and it seeds [[Transformer Architecture]], [[LLM Training Pipeline]], [[Neural Network Fundamentals]], and [[Model Quantization and Efficiency]].

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
- [[Model Quantization and Efficiency]] - quantization, KV cache, and LoRA as deployment/adaptation efficiency levers
- [[Tool Use and Function Calling]] - how LLMs request real-world actions
- [[Model Context Protocol]] - open standard for universal tool integration
- [[Agentic Loop]] - the iterative cycle powering multi-step tool use
- [[Search-Augmented Language Models]] - LLMs with RL-trained search tool policies
- [[Reward Design for RL]] - composite reward signals for multi-objective LLM training
- [[Group Relative Policy Optimization]] - relative-policy optimisation method used in the Perplexity RL stage
- [[Latent-Space Reasoning]] - reasoning through internal latent states instead of explicit token traces
- [[Recursive Architectures]] - modern recursive reasoning systems such as HRM, TRM, and RecursiveMAS

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
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Search-Augmented Language Models]]
- [[Reward Design for RL]]
- [[Transformer Architecture]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Model Quantization and Efficiency]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[Alpha Signal - The Return of Recursion]]
- [[Alpha Signal]]
- [[Perplexity]]
