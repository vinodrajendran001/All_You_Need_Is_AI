---
type: concept
created: 2026-05-13
updated: 2026-05-18
tags: [search, rag, agents, llm, retrieval]
source_ids:
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-05-18-rag-architecture-comparison
status: active
---

# Search-Augmented Language Models

LLMs that use web search (or other retrieval tools) as part of their generation pipeline, moving beyond pure parametric knowledge to ground answers in real-time or up-to-date information.

## Core idea

A search-augmented LM is not just an LLM with a search API bolted on. The model must learn **when** to search, **what** to query, and **how** to synthesise retrieved evidence into a final answer — all while balancing accuracy, efficiency, and user preferences. This makes search augmentation a multi-objective optimisation problem.

## Training approaches (Perplexity pipeline)

Perplexity Research describes a two-stage post-training recipe:

1. **SFT stage** — establishes deployment-critical behaviours (guardrails, instruction following, language consistency) using preference-oriented examples and production-format tool-use trajectories. Base models: Qwen3.5 family.

2. **RL stage** — uses [[Group Relative Policy Optimization]] (GRPO) with a composite reward:
   - **Baseline correctness** — binary signal: did the answer match ground truth (QA) or satisfy all rubrics (chat)?
   - **Preference score** — Bradley-Terry model trained on human and cross-model preference data.
   - **Efficiency penalty** — group-relative, anchored penalties for excessive tool calls and verbose responses.
   - Correctness gates preference credit (gated aggregation), preventing reward hacking.

## Broader training context

Perplexity's pipeline is one specialized application of a broader post-training stack. [[The Pocket - PocketFlow Tutorial Docs]] supplies the first-principles background for that stack across pretraining, SFT, RLHF + PPO, DPO, LoRA, and policy gradients; see [[LLM Training Pipeline]] for the synthesized version.

## Key challenges

- **Multi-objective tension** — optimising accuracy alone causes tool overuse; optimising brevity sacrifices reliability.
- **Tool-use efficiency** — more tool calls have diminishing returns (plateaus around budget=7 across benchmarks). Anchored penalties regularise tool use relative to successful solutions rather than imposing hard limits.
- **Reward hacking** — without gating, strong preference signals can compensate for factual failures.
- **Training-inference mismatch** — KL divergence drifts upward at extended training steps; token-level importance sampling helps but may not scale indefinitely.

## Relationship to RAG

Search-augmented LMs can be seen as a production-grade evolution of [[Reinforcement Learning|RL]]-trained retrieval-augmented generation, where the model actively decides its retrieval strategy rather than following a fixed retrieve-then-generate pipeline.

More specifically, they are a concrete form of [[Retrieval-Augmented Generation|Agentic RAG]]: retrieval is no longer a single preprocessing step but a learned, iterative policy over search actions, evidence gathering, and answer synthesis.

## Relationship to tool use

Search is a specific instance of [[Tool Use and Function Calling]]. The model issues structured `search_web` calls, and the [[Agentic Loop]] handles execution and result integration. The efficiency penalties described here directly address the cost of unnecessary tool invocations.

## Related pages

- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[ByteByteGo]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[Reinforcement Learning]]
- [[Tool Use and Function Calling]]
- [[Agentic Loop]]
- [[Retrieval-Augmented Generation]]
- [[Perplexity]]
