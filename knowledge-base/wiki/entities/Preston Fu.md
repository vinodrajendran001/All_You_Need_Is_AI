---
type: entity
created: 2026-09-11
updated: 2026-09-11
entity_kind: person
tags:
  - entity
  - reinforcement-learning
  - reasoning
source_ids:
  - src-2026-09-10-fu-progressive-point-matching
status: active
---

# Preston Fu

## What it is

Researcher and first author of *Long-Horizon Language Model Reinforcement Learning via Progressive Point
Matching* (arXiv 2609.07303), with Kevin Frans, Oleh Rybkin, Sergey Levine and Aviral Kumar. Writes
short author's notes on his own work at prestonfu.com.

## Why it matters here

Fu supplies the vault's treatment of [[Long-Horizon Credit Assignment]], including the diagnosis that
makes the problem quantitative: sparse outcome rewards produce policy gradients that degrade
**exponentially** in signal-to-noise with the task horizon.

The method's construction is the contribution worth keeping. Progressive Point Matching defines progress
over a set-valued state space so it can never be undone, then repairs the one place the naive version is
biased — via **shortcutting**, where a point counts as reached if everything depending on it has been
reached. The consequence is that any successful trajectory earns full credit, so the shaped reward's
optimal policy is also optimal under the original outcome reward. That is a stronger justification than
the usual empirical defence of dense rewards.

## Notes

- His most striking measurement is negative: on a near-impossible math dataset, **GRPO could not fill a
  single training batch after 24 hours** — the difference between slow training and no training.
- Reports that training at 4K context was comparable to or better than 8K, explaining it behaviourally:
  the 8K policy collapses output length and guesses early. This transfers beyond the method.
- Names the practical bottleneck honestly — reasoning points are generated with an off-the-shelf LLM and
  "required a significant amount of iteration."
- Treats test-time budget control as an unsolved deployment problem, citing Claude Code's
  `/effort ultracode` mode as insufficient.

## Related pages

- [[Long-Horizon Credit Assignment]]
- [[Reward Design for RL]]
- [[Group Relative Policy Optimization]]
- [[Reinforcement Learning]]
- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Preston Fu - Progressive Point Matching]]
