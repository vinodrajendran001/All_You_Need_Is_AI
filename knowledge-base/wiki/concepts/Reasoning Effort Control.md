---
type: concept
created: 2026-08-30
updated: 2026-08-30
tags:
  - concept
  - reasoning
  - post-training
  - inference
source_ids:
  - src-2026-07-20-raschka-reasoning-effort
status: active
---

# Reasoning Effort Control

## Definition

Reasoning effort control is the set of mechanisms that let a model spend more or less computation on
a single request — the low/medium/high selectors, `/think` and `/no_think` flags, and token budgets
exposed by current reasoning models. Despite looking like inference-time settings, these are almost
entirely **trained behaviours**.

## Why it matters

Effort is the dial that connects quality to cost at serving time. It also turns out to be partly
interchangeable with model size, which changes how deployments should be compared: the right question
is cost at matched quality, not benchmark score at default settings.

## Current synthesis

### `<think>` tags are cosmetic

[[Sebastian Raschka - Controlling Reasoning Effort in LLMs]] corrects a common misreading. The tags
confer no reasoning ability; they only **delimit** a trace so it can be displayed, budgeted, or
stripped. Models learn to emit them through a *format reward* added to the RL objective:

```
R_total = R_accuracy + R_format
```

The accuracy term teaches reasoning. The format term teaches where to put it. This matters because it
means "turning off thinking" is not disabling a capability — it is suppressing a delimiter and the
text inside it.

### Two ways to install effort levels

After RL with verifiable rewards, teams take one of two routes:

1. **Effort-conditioned RLVR** — condition the RL run on an effort level and apply an
   effort-dependent length penalty, so the policy learns different length regimes directly.
2. **Post-RLVR SFT** — run RLVR normally, then fine-tune on targets labelled with effort levels.

### Soft switch vs hard switch

Qwen3's **Thinking Mode Fusion** SFT stage trains on `/think` and `/no_think` variants, where the
`/no_think` targets carry an *empty* `<think></think>` block. The **soft switch** is the user-facing
flag, which the model may or may not honour. The **hard switch** (`enable_thinking=False`) prefills
the empty block so the model structurally cannot reason. One is a request; the other is a constraint.

### Per-model recipes

| Model | Mechanism |
| --- | --- |
| **DeepSeek V4** | Three mode specialists, each with its own context window and length penalty, distilled into one checkpoint |
| **Nemotron 3 Ultra** | Medium-effort behaviour bootstrapped from GPT-OSS-120B traces, plus random-budget truncation with `</think>` masked from the loss on ~2.5% of RLVR prompts; produces a learned mode *and* a separate external budget |
| **Kimi K2.5 "Toggle"** | Alternating budgeted and unconstrained RL phases; the budget comes from a percentile of correct-rollout lengths and activates only once accuracy passes a threshold. **25-30% token reduction with little performance change** — and no inference-time selector at all, since it operates entirely in training |
| **GLM-5** | Interleaved, preserved, and turn-level thinking installed via SFT |
| **Qwen3** | Mode fusion plus inference-time truncation; partial-reasoning behaviour **emerged** rather than being trained |
| **Inkling** | Continuous effort in 0.2-0.99 conditioned during RL, with `R(e) = R_task - lambda(e) * N_tokens` |

The spread of designs hides a narrow set of ideas: condition on a level, penalize length in proportion
to it, and optionally distil the resulting specialists back together.

### Training scaling and inference scaling are overlapping curves

Raschka's most portable claim: **a smaller model at high effort can match a larger model at low
effort**. Effort is a deployment-time substitute for parameters. This connects
[[Test-Time Scaling]] (spend more at inference) to [[Reasoning Compression]] (need less at
inference) as two views of one budget, and makes the serving decision an economic one rather than a
capability one.

### The efficiency result worth generalizing

Kimi's 25-30% token reduction with little performance loss, obtained purely by shaping the RL
curriculum, implies a substantial fraction of a reasoning trace was never load-bearing. The vault has
no account of *which* parts those are — see the open questions.

## Open questions

- What were the removed 25-30% of tokens doing? Without a theory of which trace segments carry the
  computation, effort budgets are tuned empirically per model.
- Qwen3's partial-reasoning behaviour under truncation emerged rather than being trained. Why it works,
  and whether it degrades in ways benchmarks miss, is unexplained.
- Effort levels are calibrated against benchmark distributions. Does "medium effort" mean anything
  stable on out-of-distribution work?
- Closed-model behaviour here is inferred. Raschka is explicit that GPT-5.6's internals are unknown and
  that his proposed diagram is "a possible implementation, not a confirmed description."
- If effort substitutes for parameters, what is the exchange rate, and does it hold across task types?

## Related pages

- [[Reasoning Compression]]
- [[Test-Time Scaling]]
- [[LLM Reasoning]]
- [[Staged Reinforcement Learning Curriculum]]
- [[Reward Design for RL]]
- [[Knowledge Distillation]]
- [[LLM Training Pipeline]]
- [[Sebastian Raschka - Controlling Reasoning Effort in LLMs]]
