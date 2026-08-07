---
type: source-summary
created: 2026-08-07
updated: 2026-08-07
source_id: src-2026-08-07-rllm-realtime-rl-agents
source_title: Continual Learning via Real-Time RL for Agents
source_author: rLLM
source_url: https://rllm-project.com/post.html?post=realtime_rl.md
tags:
  - source/summary
  - agents
  - reinforcement-learning
  - continual-learning
source_ids:
  - src-2026-08-07-rllm-realtime-rl-agents
status: active
---

# rLLM - Continual Learning via Real-Time RL for Agents

## Summary

rLLM studies how an agent could update from a stream of one-off production-style trajectories rather than repeated rollouts of the same prompt. On MigrationBench, the authors train Qwen3-Coder-30B for Java 8→17 migration using one rollout per task and a reward centered against the cross-task batch mean. They report success increasing from 43% to 59.2%, compared with 48.2% for raw-reward REINFORCE at batch size 128.

The batch-relative baseline gives failed zero-reward trajectories a negative learning signal and reduces single-rollout variance. The post also studies asynchronous stale rollouts: PPO clipping plus truncated importance sampling stabilizes rollout/training log-probability mismatch, whereas the reported no-TIS run collapses.

## Key claims

- Production interactions often provide one trajectory per task, breaking GRPO's same-prompt group-relative assumption.
- Centering rewards across different prompts in a batch makes nearly every trajectory informative.
- Under an equal 32-rollout budget, the reported single-rollout method tracks and slightly exceeds GRPO.
- Larger batches improve the reliability of the population reward baseline.
- Asynchronous continual learning must correct both stale policies and numerical mismatch between rollout and training engines.
- Regression gates are required before a continually updated checkpoint serves users.

## Why it matters

This is the vault's first concrete method for [[Continual Learning for Agents]]. It extends [[Agentic Reinforcement Learning]] from build-time isolated rollouts toward post-deployment streams and makes policy staleness, checkpoint promotion, reward reliability, and catastrophic regression central production concerns.

## Tensions / open questions

- MigrationBench is a clean mocked environment, not uncontrolled production traffic.
- A cross-task baseline compares rewards from tasks that may differ greatly in difficulty; task mix can bias the signal.
- The empirical batch mean depends on sampled rollouts and is not the exact rollout-independent baseline in the standard unbiasedness argument.
- Live feedback can be noisy, delayed, manipulated, privacy-sensitive, or correlated with user populations.
- The post does not solve safe online checkpoint promotion, rollback, forgetting, or long-term distribution drift.

## Affected pages

- [[Continual Learning for Agents]]
- [[Agentic Reinforcement Learning]]
- [[Reward Design for RL]]
- [[AI Agents in Production]]
- [[Multi-Turn Evaluation]]

## Citations

- Raw capture: [[2026-08-07 rLLM - Continual Learning via Real-Time RL for Agents]]
- Canonical URL: https://rllm-project.com/post.html?post=realtime_rl.md

## Related pages

- [[Group Relative Policy Optimization]]
- [[Recursive Self-Improvement]]
- [[Context Engineering]]
- [[rLLM]]

