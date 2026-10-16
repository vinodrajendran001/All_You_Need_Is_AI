---
type: source-summary
created: 2026-08-30
updated: 2026-10-16
source_id: src-2026-07-20-raschka-reasoning-effort
source_title: "Controlling Reasoning Effort in LLMs"
source_author: "Sebastian Raschka"
source_url: "https://magazine.sebastianraschka.com/p/controlling-reasoning-effort-in-llms"
tags:
  - source/summary
  - reasoning
  - post-training
  - inference
source_ids:
  - src-2026-07-20-raschka-reasoning-effort
status: active
---

# Sebastian Raschka - Controlling Reasoning Effort in LLMs

## Summary

A mechanism-level walkthrough of learned reasoning modes, external trace budgets, and
token-efficient training policies. Raschka surveys six models, distinguishing what training
installs from what an inference-time switch or stopping budget selects.

The starting correction is that **`<think>` tags do not confer reasoning ability by themselves**.
They delimit a trace so it can be displayed, budgeted, or stripped. Models
learn to emit them through a *format reward* added to the RL objective, `R_total = R_accuracy +
R_format` — the accuracy term teaches reasoning, the format term teaches where to put it.

## Key claims

**Two surveyed routes to learned effort levels.** Either condition the RLVR
run itself on an effort level and apply an effort-dependent length penalty, or run RLVR normally and
then do a supervised stage on targets labelled with effort levels.

**Soft switch vs hard switch.** Qwen3's "Thinking Mode Fusion" SFT stage trains on `/think` and
`/no_think` variants, where `/no_think` targets carry an *empty* `<think></think>` block. The soft
switch is the user flag; the hard switch (`enable_thinking=False`) prefills the empty block to
close the designated trace phase. This changes the expected response mode, not the model's
ability to compute internally.

**Per-model recipes converge on the same few tricks.**

| Model | Mechanism |
| --- | --- |
| **DeepSeek V4** | Three mode specialists, each with its own context window and length penalty, distilled into a single checkpoint |
| **Nemotron 3 Ultra** | Medium-effort behaviour bootstrapped from GPT-OSS-120B traces, plus random-budget truncation with `</think>` masked from the loss, applied to ~2.5% of RLVR prompts; yields a learned mode *and* a separate external budget |
| **Kimi K2.5 report: Toggle** | Alternating budgeted and unconstrained RL phases; the budget comes from a percentile of correct-rollout lengths and activates after an accuracy threshold. The reported evaluation on **K2 Thinking** reduces generated tokens by **25-30% with little change in benchmark performance**. No runtime selector between these training phases; K2.5's separate thinking/instant switch is not Toggle |
| **GLM-5** | Interleaved, preserved, and turn-level thinking installed via SFT |
| **Qwen3** | Mode fusion plus inference-time truncation; partial-reasoning behaviour *emerged* rather than being trained |
| **Inkling** | Continuous effort in the range 0.2-0.99 conditioned during RL, with `R(e) = R_task - lambda(e) * N_tokens` |

**Training scaling and inference scaling are two knobs whose curves overlap.** A smaller model run at
high effort can match a larger model run at low effort. Effort is therefore a deployment-time
substitute for parameters, and the choice between them is an economic one.

**Toggle changes the learned policy, not just the length of an unchanged trace.** Its reported
25-30% reduction on K2 Thinking shows a more token-efficient trained policy on the evaluated
benchmarks. It does not identify which tokens in the original policy were causally unnecessary:
training can reorganize the computation.

## Why it matters

The vault already treats [[Test-Time Scaling]] as a dial and [[Reasoning Compression]] as a training
problem; this source connects the two. It also separates delimiters and UI presentation from the
computation performed while generating a trace. Suppressing that trace is not proof of no internal
reasoning, and shorter output after training is not a token-level causal ablation.

For anyone choosing a model, the overlapping-curves claim is directly actionable — effort level and
parameter count trade against each other, so the right comparison is cost at matched quality rather
than benchmark score at default settings.

## Tensions / open questions

- Raschka is explicit that GPT-5.6's internals are unknown and that his Figure 21 is "a possible
  implementation, not a confirmed description." Claims about closed models here are inference.
- Qwen3's partial-reasoning behaviour under truncation *emerged* rather than being trained. Nobody
  explains why it works, or whether it degrades in ways benchmarks miss.
- The October 16 lint removes this summary's earlier "cannot reason" and "never load-bearing"
  claims and restores **little change in benchmark performance**, not zero accuracy cost.
  The raw's K2.5 section/figure framing is broader than its explicit attribution of the Toggle
  evaluation to K2 Thinking; the result is recorded under that tested model.
- No selector between Toggle's training phases does not mean K2.5 lacks an inference-time
  thinking/instant switch. The raw describes that separate switch while noting that its full
  training recipe is undisclosed.
- Which computations change under token-efficient training, and what that does to trace
  faithfulness or monitoring quality, require separate experiments.
- Effort levels are trained against benchmark distributions. Whether "medium effort" means anything
  stable on out-of-distribution work is untested.

## Affected pages

- [[Reasoning Effort Control]]
- [[Reasoning Compression]]
- [[Test-Time Scaling]]
- [[LLM Reasoning]]
- [[Chain-of-Thought Monitoring]]
- [[Sebastian Raschka]]

## Citations

- Raw capture: [[2026-07-20 Sebastian Raschka - Controlling Reasoning Effort in LLMs]]
- Original: <https://magazine.sebastianraschka.com/p/controlling-reasoning-effort-in-llms> (published 2026-07-18)

## Related pages

- [[Chain-of-Thought Monitoring]]
- [[Staged Reinforcement Learning Curriculum]]
- [[Reward Design for RL]]
- [[Knowledge Distillation]]
- [[Group Relative Policy Optimization]]
- [[LLM Training Pipeline]]
