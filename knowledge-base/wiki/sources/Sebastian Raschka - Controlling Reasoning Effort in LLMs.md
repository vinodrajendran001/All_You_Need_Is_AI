---
type: source-summary
created: 2026-08-30
updated: 2026-08-30
source_id: src-2026-07-20-raschka-reasoning-effort
source_title: "Controlling Reasoning Effort in LLMs"
source_author: "Sebastian Raschka"
source_url: "https://magazine.sebastianraschka.com/p/controlling-reasoning-effort-in-llms"
tags:
  - source/summary
  - topic/reasoning
  - topic/post-training
  - topic/inference
source_ids:
  - src-2026-07-20-raschka-reasoning-effort
status: active
---

# Sebastian Raschka - Controlling Reasoning Effort in LLMs

## Summary

A mechanism-level walkthrough of how modern LLMs acquire *reasoning effort* controls — the
low/medium/high toggles and `/think` flags users now take for granted — and why the answer is
almost always training, not inference-time plumbing. Raschka works through six recent models and
extracts the shared machinery.

The starting correction is the most useful one: **`<think>` tags are cosmetic**. They confer no
reasoning ability; they only delimit a trace so it can be displayed, budgeted, or stripped. Models
learn to emit them through a *format reward* added to the RL objective, `R_total = R_accuracy +
R_format` — the accuracy term teaches reasoning, the format term teaches where to put it.

## Key claims

**Two ways to install effort levels after RL with verifiable rewards.** Either condition the RLVR
run itself on an effort level and apply an effort-dependent length penalty, or run RLVR normally and
then do a supervised stage on targets labelled with effort levels.

**Soft switch vs hard switch.** Qwen3's "Thinking Mode Fusion" SFT stage trains on `/think` and
`/no_think` variants, where `/no_think` targets carry an *empty* `<think></think>` block. The soft
switch is the user flag; the hard switch (`enable_thinking=False`) prefills the empty block so the
model cannot reason even if it wanted to.

**Per-model recipes converge on the same few tricks.**

| Model | Mechanism |
| --- | --- |
| **DeepSeek V4** | Three mode specialists, each with its own context window and length penalty, distilled into a single checkpoint |
| **Nemotron 3 Ultra** | Medium-effort behaviour bootstrapped from GPT-OSS-120B traces, plus random-budget truncation with `</think>` masked from the loss, applied to ~2.5% of RLVR prompts; yields a learned mode *and* a separate external budget |
| **Kimi K2.5 "Toggle"** | Alternating budgeted and unconstrained RL phases; the budget is set from a percentile of correct-rollout lengths and only activates once accuracy passes a threshold. 25-30% token reduction with little performance change, entirely in training — no inference-time selector |
| **GLM-5** | Interleaved, preserved, and turn-level thinking installed via SFT |
| **Qwen3** | Mode fusion plus inference-time truncation; partial-reasoning behaviour *emerged* rather than being trained |
| **Inkling** | Continuous effort in the range 0.2-0.99 conditioned during RL, with `R(e) = R_task - lambda(e) * N_tokens` |

**Training scaling and inference scaling are two knobs whose curves overlap.** A smaller model run at
high effort can match a larger model run at low effort. Effort is therefore a deployment-time
substitute for parameters, and the choice between them is an economic one.

**Kimi's result is the cleanest efficiency claim.** Cutting 25-30% of tokens with little performance
loss, achieved purely by shaping the RL curriculum, means much of a reasoning trace was never load-bearing.

## Why it matters

The vault already treats [[Test-Time Scaling]] as a dial and [[Reasoning Compression]] as a training
problem; this source shows they are the same problem seen from two ends. It also settles a recurring
confusion: the visible artefacts of reasoning (tags, traces, "thinking" UI) are presentation, and the
controllable quantity underneath is token budget shaped during post-training.

For anyone choosing a model, the overlapping-curves claim is directly actionable — effort level and
parameter count trade against each other, so the right comparison is cost at matched quality rather
than benchmark score at default settings.

## Tensions / open questions

- Raschka is explicit that GPT-5.6's internals are unknown and that his Figure 21 is "a possible
  implementation, not a confirmed description." Claims about closed models here are inference.
- Qwen3's partial-reasoning behaviour under truncation *emerged* rather than being trained. Nobody
  explains why it works, or whether it degrades in ways benchmarks miss.
- If 25-30% of reasoning tokens can be removed with no accuracy cost, it is unclear what the removed
  tokens were doing — the vault has no account of which parts of a trace are load-bearing.
- Effort levels are trained against benchmark distributions. Whether "medium effort" means anything
  stable on out-of-distribution work is untested.

## Affected pages

- [[Reasoning Effort Control]]
- [[Reasoning Compression]]
- [[Test-Time Scaling]]
- [[LLM Reasoning]]
- [[Sebastian Raschka]]

## Related pages

- [[Staged Reinforcement Learning Curriculum]]
- [[Reward Design for RL]]
- [[Knowledge Distillation]]
- [[Group Relative Policy Optimization]]
- [[LLM Training Pipeline]]

## Citations

- Raw capture: [[2026-07-20 Sebastian Raschka - Controlling Reasoning Effort in LLMs]]
- Original: <https://magazine.sebastianraschka.com/p/controlling-reasoning-effort-in-llms> (published 2026-07-18)
