---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags: [rl, optimization, grpo, llm, training]
source_ids:
  - src-2026-04-22-perplexity-search-augmented-lm
status: active
---

# Group Relative Policy Optimization

## Definition

Group Relative Policy Optimization (GRPO) is a reinforcement-learning objective that updates a policy by comparing multiple sampled rollouts for the same prompt against one another rather than against a single absolute baseline.

## Why it matters here

In this vault, GRPO is the optimisation method behind Perplexity's RL stage for search agents. It matters because it supports reward structures that combine correctness, user preference, and efficiency while keeping credit assignment tied to within-group relative performance.

## Key mechanics

- Sample a group of candidate trajectories for the same prompt.
- Score each trajectory with a composite reward.
- Convert those scores into relative advantages inside the group, so the policy learns from better-than-peer rollouts.
- Use importance-sampling corrections to reduce training-inference mismatch during optimisation.

## Related pages

- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Search-Augmented Language Models]]
- [[Reward Design for RL]]
- [[Reinforcement Learning]]
