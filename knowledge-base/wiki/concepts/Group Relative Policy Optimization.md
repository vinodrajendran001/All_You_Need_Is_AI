---
type: concept
created: 2026-05-13
updated: 2026-06-04
tags: [rl, optimization, grpo, llm, training]
source_ids:
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-06-04-efficient-reasoning-edge
  - src-2026-06-04-dss-grpo-cot-compression
status: active
---

# Group Relative Policy Optimization

## Definition

Group Relative Policy Optimization (GRPO) is a reinforcement-learning objective that updates a policy by comparing multiple sampled rollouts for the same prompt against one another rather than against a single absolute baseline.

## Why it matters here

In this vault, GRPO first appeared as the optimisation method behind Perplexity's RL stage for search agents. It now also appears in [[Efficient Reasoning on the Edge]] as the optimiser for budget-forced reasoning adapters on mobile hardware. That broader reuse matters because it shows GRPO is not tied to web-search agents specifically; it is a general way to optimise multi-objective LLM behaviour when the reward depends on relative rollout quality inside a sampled group.

## Key mechanics

- Sample a group of candidate trajectories for the same prompt.
- Score each trajectory with a composite reward.
- Convert those scores into relative advantages inside the group, so the policy learns from better-than-peer rollouts.
- Use importance-sampling corrections to reduce training-inference mismatch during optimisation.
- In the Qualcomm paper, apply the same relative-update idea to a different reward shape: binary answer correctness multiplied by a soft budget-compliance term over total response length.
- [[Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression]] shows that GRPO can also be **segmented**: relative advantages need not be computed only for a whole completion. They can be separated across think and answer spans, then routed with token masks so compression pressure does not leak across the boundary.

## Broader context

The PocketFlow tutorials on policy gradients and RLHF make the surrounding optimization ladder explicit: REINFORCE leads to baselines and actor-critic methods, which in turn lead to PPO-style constrained policy optimization. That broader framing helps place GRPO as one member of a larger family of LLM post-training objectives rather than as an isolated search-agent trick. See [[LLM Training Pipeline]] and [[The Pocket - PocketFlow Tutorial Docs]].

## Related pages

- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[Perplexity]]
- [[Search-Augmented Language Models]]
- [[Efficient Reasoning on the Edge]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[On-Device Reasoning]]
- [[Reasoning Compression]]
- [[Reinforcement Learning]]
- [[AI Knowledge Base Overview]]
