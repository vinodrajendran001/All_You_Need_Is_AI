---
type: concept
created: 2026-05-13
updated: 2026-05-18
tags: [rl, optimization, grpo, llm, training]
source_ids:
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-18-pocketflow-tutorial-docs
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

## Broader context

The PocketFlow tutorials on policy gradients and RLHF make the surrounding optimization ladder explicit: REINFORCE leads to baselines and actor-critic methods, which in turn lead to PPO-style constrained policy optimization. That broader framing helps place GRPO as one member of a larger family of LLM post-training objectives rather than as an isolated search-agent trick. See [[LLM Training Pipeline]] and [[The Pocket - PocketFlow Tutorial Docs]].

## Related pages

- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[Perplexity]]
- [[Search-Augmented Language Models]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[Reinforcement Learning]]
- [[AI Knowledge Base Overview]]
