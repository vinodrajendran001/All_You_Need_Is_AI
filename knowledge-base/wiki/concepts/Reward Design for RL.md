---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags: [rl, reward, training, alignment, llm]
source_ids:
  - src-2026-04-22-perplexity-search-augmented-lm
status: active
---

# Reward Design for RL

The practice of constructing reward signals that guide reinforcement learning of LLMs toward desired behaviours across multiple objectives simultaneously.

## Why it matters

Naive reward functions cause pathological behaviours. In search-agent training, a simple linear combination of accuracy and preference scores allows the model to hack rewards — strong style scores can compensate for wrong answers. Reward design must encode the correct priority structure.

## Gated reward aggregation (Perplexity)

Perplexity's approach uses a conditional structure:

```
R(τ) = r_base(τ) × (1 + s(τ)) − pen_eff(τ)
```

- **r_base** — binary correctness (QA match or rubric satisfaction). This is the hard gate: no preference credit without correctness.
- **s(τ)** — Bradley-Terry preference score ∈ [0,1], measuring informativeness, clarity, and tone.
- **pen_eff(τ)** — anchored efficiency penalty for tool overuse and verbosity.

The key principle: **correctness is a necessary condition** before any preference or style reward is applied.

## Anchored efficiency penalties

Rather than penalising tool calls or length in absolute terms (which suppresses necessary exploration), penalties are computed **relative to successful solutions within the same [[Group Relative Policy Optimization|GRPO]] group**:

- **Tool-call penalty** — excess calls beyond a baseline sampled from the group's "winner set" (correct rollouts).
- **Length penalty** — penalises verbose winners and terse losers, anchored to group-specific length baselines from correct-and-preferred rollouts.

## Rubric-based rewards

For non-verifiable tasks (rewriting, planning, open-ended chat), deployment requirements are converted into **rubrics**: atomic, objective, necessary checks. A pass@4 calibration filter ensures rubric sets are neither too easy nor too hard.

## Variance balancing

Different data types produce different gradient magnitudes. Perplexity uses a 90/10 prompt mixture (verifiable QA / rubric-based) to balance the harder QA signal against the easier rubric signal.

## Related pages

- [[Search-Augmented Language Models]]
- [[Group Relative Policy Optimization]]
- [[Reinforcement Learning]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Agentic Loop]]
