---
type: concept
created: 2026-05-13
updated: 2026-08-27
tags: [concept, reinforcement-learning, optimization, grpo, llm, training]
source_ids:
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-06-04-efficient-reasoning-edge
  - src-2026-06-04-dss-grpo-cot-compression
  - src-2026-06-22-cameron-wolfe-agentic-rl-frameworks
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
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
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]] shows how GRPO-style ideas are adapted for [[Agentic Reinforcement Learning]]. Agentic rollouts may contain many environment turns, tool observations, and non-agent tokens, so implementations commonly apply action masks and sometimes normalize advantages across tasks or environments rather than only within one prompt group.
- The same source also clarifies GRPO's limits: PPO and REINFORCE variants remain competitive, and critic-based PPO can be preferred for very long or compacted trajectories with highly variable numbers of trainable traces.
- [[Akhil Arora et al - Current Advances in LLM Reasoning]] gives the crispest statement of *why* GRPO mattered for reasoning: PPO needs **four models** (policy, reward model, critic baseline, and a KL reference); GRPO **drops the critic** and uses the **group mean and standard deviation** as the baseline, keeping the same clipping and a KL penalty to the base model at roughly **half the memory**. That memory saving is what made large-scale RL for reasoning practical.

## Agentic variants and neighboring ideas

- **Task-level advantage normalization** (AgentRL) computes normal GRPO-style trajectory advantages, broadcasts them to agent-generated tokens, then normalizes token-level advantages within a domain/task group so one environment does not dominate the update.
- **Environment Relative Policy Optimization (ERPO)** (AutoForge) keeps the per-question reward mean from GRPO but scales by reward variation across valid trajectories from the same environment.
- **StarPO** (RAGEN) is framed as trajectory-level optimization over state-thinking-action-reward traces and can be implemented with GRPO or PPO.

The broader pattern is that group-relative learning survives in agentic RL, but the "group" often needs to reflect task, environment, or trajectory structure rather than only multiple answers to one static prompt.

## Broader context

The PocketFlow tutorials on policy gradients and RLHF make the surrounding optimization ladder explicit: REINFORCE leads to baselines and actor-critic methods, which in turn lead to PPO-style constrained policy optimization. That broader framing helps place GRPO as one member of a larger family of LLM post-training objectives rather than as an isolated search-agent trick. See [[LLM Training Pipeline]] and [[The Pocket - PocketFlow Tutorial Docs]].

## A production configuration, in full

[[IBM Granite Team - Granite 4.2 LLMs How They're Built]] is the first source in this vault to give a
complete GRPO configuration for a shipped model family rather than a description of the method. Three
details are worth carrying.

**The baseline is leave-one-out.** Each response is scored against the mean reward of the *other*
samples drawn for the same prompt, not against the group mean including itself. This keeps the
critic-free property that made GRPO attractive while removing the sample's own contribution to its
own baseline.

**The batch shape is large and shallow.** Granite's RLVR stage pairs **256 prompts with 16 responses
each — a 4,096-example batch consumed in a single optimizer step**. Later stages trade prompt count
for depth as rollouts get longer: the terminal-agent stage drops to 8 prompts × 32 generations
because each rollout spans up to 64 environment turns. Group size stays in the 16–32 range
throughout, which is a useful reference point for how wide a "group" needs to be in practice.

**Asynchrony is embraced, then bounded.** Generation workers sample continuously into a shared buffer
while the trainer pulls batches and streams updated parameters back without pausing them. A refresh
can land mid-rollout, leaving a single trajectory stitched together from two adjacent policy
versions. IBM permits this deliberately — the alternative is rebuilding the KV cache after every
refresh — and controls it with one guardrail: workers may not drift more than **a single update**
behind the trainer. Residual mismatch is absorbed by **truncated importance sampling**, clamping the
train-versus-generation log-probability ratio to a fixed ceiling so a handful of stale tokens cannot
dominate an update. Ratio clip is 0.2 / 0.28.

This is the same staleness problem [[rLLM]] and [[RadixArk - Miles v0.1 Production-Level Post-Training]]
address, converging on the same tool. What Granite adds is the explicit statement that the trade is
made *to keep the KV cache warm* — the cost of preventing staleness is paid in cache rebuilds, which
is a systems reason for an algorithmic compromise.

## The KL coefficient should track the reward type

Granite's stage table shows KL varying from 0 to 0.05 across a single pipeline, and not arbitrarily:
**KL = 0 where the reward is verifiable** (RLVR, and the long-horizon SWE stage), **KL = 0.05 where
it is preference, safety, or a narrow skill graft** (RLHF, the code booster). The logic is that a
verifiable reward cannot be satisfied by drifting — if the tests pass, the behavior is good — while
a preference or safety reward makes drift and reward hacking indistinguishable.

This turns KL from a knob tuned by feel into something derivable from the objective. See
[[Staged Reinforcement Learning Curriculum]] for the full ladder.

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[Staged Reinforcement Learning Curriculum]]
- [[LLM Training Pipeline]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Agentic Reinforcement Learning]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[Perplexity]]
- [[Search-Augmented Language Models]]
- [[Efficient Reasoning on the Edge]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[On-Device Reasoning]]
- [[Reasoning Compression]]
- [[Reinforcement Learning]]
- [[Reward Design for RL]]
- [[LLM Reasoning]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[AI Knowledge Base Overview]]
