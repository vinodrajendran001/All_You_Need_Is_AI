---
type: entity
entity_kind: organisation
created: 2026-05-13
updated: 2026-05-13
tags: [search, ai, agents, llm]
source_ids:
  - src-2026-04-22-perplexity-search-augmented-lm
status: active
---

# Perplexity

An AI company building search products powered by language models. Their research arm (Perplexity Research) publishes work on training search-augmented LLMs, focusing on the intersection of retrieval, reinforcement learning, and multi-objective optimisation.

## Why it matters to this vault

Perplexity published a detailed technical article on their post-training pipeline for web search agents, providing one of the most concrete public descriptions of how search-augmented LLMs are trained with RL in production. The article introduces several reusable techniques: gated reward aggregation, anchored efficiency penalties, rubric-based rewards, and synthetic multi-hop QA construction.

## Key contributions referenced

- Two-stage SFT → RL pipeline for search agents
- Gated reward aggregation to prevent reward hacking
- Anchored, group-relative efficiency penalties
- Synthetic verifiable QA via sequential expansion
- Rubric-based reward design for non-verifiable tasks

## Related pages

- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Search-Augmented Language Models]]
- [[Reward Design for RL]]
- [[Reinforcement Learning]]
- [[AI Knowledge Base Overview]]
