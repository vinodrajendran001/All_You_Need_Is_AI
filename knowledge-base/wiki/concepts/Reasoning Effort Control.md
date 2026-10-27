---
type: concept
created: 2026-08-30
updated: 2026-10-27
tags:
  - concept
  - reasoning
  - post-training
  - inference
source_ids:
  - src-2026-07-20-raschka-reasoning-effort
  - src-2026-08-30-adlrocha-base-models-bottleneck
  - src-2026-09-30-replit-free-models-harness-design
  - src-2026-09-27-willison-llms-2026-so-far
  - src-2026-10-13-zancato-model-priming
  - src-2026-10-20-cloudflare-inference-bill
status: active
---

# Reasoning Effort Control

## Definition

Reasoning effort control is the set of mechanisms that let a model spend more or less computation on a
single request (and, in an agent, across a run's model calls; see below) — the low/medium/high selectors,
`/think` and `/no_think` flags, and token budgets exposed by current reasoning models. Many selectors
invoke **trained behaviors**; external budgets and architectural iteration counts can also constrain the
computation directly.

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

The accuracy term rewards successful answers; the format term rewards the requested structure.
Selecting a no-trace mode changes how the model responds, but an empty reasoning block does not
demonstrate that it performed no internal computation or that answer quality is unchanged.

### Two surveyed routes to learned effort levels

Raschka groups learned effort-level recipes into two routes, distinct from direct runtime budgets:

1. **Effort-conditioned RLVR** — condition the RL run on an effort level and apply an
   effort-dependent length penalty, so the policy learns different length regimes directly.
2. **Post-RLVR SFT** — run RLVR normally, then fine-tune on targets labelled with effort levels.

### Soft switch vs hard switch

Qwen3's **Thinking Mode Fusion** SFT stage trains on `/think` and `/no_think` variants, where the
`/no_think` targets carry an *empty* `<think></think>` block. The **soft switch** is the user-facing
flag, which the model may or may not honour. The **hard switch** (`enable_thinking=False`) prefills
the empty block to close the designated trace phase. This constrains the expected output format,
not the model's ability to compute internally; an empty trace is not an absence of reasoning.

### Per-model recipes

| Model | Mechanism |
| --- | --- |
| **DeepSeek V4** | Three mode specialists, each with its own context window and length penalty, distilled into one checkpoint |
| **Nemotron 3 Ultra** | Medium-effort behaviour bootstrapped from GPT-OSS-120B traces, plus random-budget truncation with `</think>` masked from the loss on ~2.5% of RLVR prompts; produces a learned mode *and* a separate external budget |
| **Kimi K2.5 report: Toggle** | Alternating budgeted and unconstrained RL phases; the budget comes from a percentile of correct-rollout lengths and activates after an accuracy threshold. The evaluation on **K2 Thinking** reports **25-30% fewer generated tokens with little change in benchmark performance**. No selector between Toggle's training phases; K2.5's thinking/instant switch is separate |
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

### Shorter learned traces are not a causal token ablation

The Toggle result on K2 Thinking demonstrates a more token-efficient policy after training.
The **25-30% reduction with little change in benchmark performance** does not show that the
same fraction of the original policy's trace could simply be deleted. Weight updates can
reorganize computation. The October 16 lint replaces this page's earlier inference that those
tokens were necessarily nonessential; faithfulness and monitorability need their own evidence.

## Two shipped policies, and a disagreement about the floor

[[adlrocha - Base Models Stopped Being the Bottleneck]] documents two contemporaneous open-weight releases
that made opposite choices about whether reasoning can be switched off.

**Qwen3.8-27B** exposes `reasoning_effort` with three settings — `xhigh`, `medium`, `low` — defaulting to
`xhigh`, and permits its explicit **thinking mode to be disabled**. **GLM-5.3 does not expose that
mode-off option**.

The disagreement is about whether operators can skip the explicit trace phase, not whether a
model can perform zero internal computation. A required trace adds work that cannot be removed
through that mode switch; its cost still depends on the request and serving setup. See
[[Inference Efficiency Frontier]], where effort is one axis alongside latency and throughput.

[[Qwen]] adds a second, less familiar control on the same surface: **`preserve_thinking`, on by default**,
which retains the thinking blocks of every historical message so that RL could teach the model to treat past
reasoning as **working memory**. The three stated motivations are decision consistency, avoiding re-reasoning,
and KV-cache reuse. Effort control and thinking retention are separate knobs that interact — a high effort
setting with retention on compounds context growth turn over turn. No ablation separating the three
motivations is offered.

## Effort can be a policy inside the turn

[[Replit - Free the Models - Harness Design at the Frontier]] adds a serving-time controller above
these trained behaviors. The core selects worker tier and effort and can adjust its own effort
mid-turn. Preserving the prompt cache across that change is model-specific; an effort selector is
not a portable promise about cache behavior.

Replit's medium-effort production observations and Max-mode Astra benchmarks are different
experiments. The benchmarks show a quality/cost tradeoff among configurations rather than an
ablation proving that dynamic effort alone caused the gain.

[[Simon Willison - 2026 in LLMs (so far)]] supplies the failure-side anecdote: Opus 5.5 used
128,000 reasoning tokens on a pelican SVG without reaching an answer. More effort can consume the
budget rather than improve the delivered artifact. His Qwen3.8-27B example took 21 minutes locally;
he calls its default "high", while the earlier configuration account above names `xhigh`.
Keep the wording discrepancy and the anecdotal workload scope rather than changing the documented
API setting or treating either example as a broad model ranking.

## Internal iterations are a different effort knob from trace length

[[Luca Zancato - Priming Hybrid Models from Pretrained Transformers]] adds Gated KalmaNet's
serving-time iteration count. Reducing **30 to 10 iterations** reportedly gives **10% faster
decoding** with roughly **1% accuracy loss on AIME 2025**; the source does not specify whether
that loss is relative percent or percentage points.

This broadens the earlier trained-selector framing. A runtime can change internal work without
requesting a shorter natural-language trace. The reported **1.2-1.4x time-to-target-accuracy**
gain on the full benchmark is also distinct from raw tokens per second or the up-to-1.6x
hardest-problem result. Neither the iteration knob nor similar trace lengths guarantee equal
quality across tasks. Compare complete cost and accuracy at each operating point.

## Effort sets how far a coding agent looks, and its value differs by role

[[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] measures effort
on a production agent and checks whether its output was real. In [[Cloudflare]]'s internal AI code
reviewer, effort changed how far the agent explored, not only how long it reasoned. On Sonnet 5.5 at
medium effort the code quality reviewer made **1.7** model calls per run instead of **6.2** (a baseline
the post does not name), and more than half its runs finished in a single call, opening no other file in
the repository. "We were concerned that this made reviews shallower". At high effort it made **3.4**
calls. In a 50/50 split since 5 October, high effort cost **61%** more per run after one day and posted
**58%** more critical and warning findings: "That's about two cents per review". Code quality is moving
to high effort, and the post's cost figures assume it.

The value of effort differed by role. For the coordinator, medium effort finished full-tier jobs **20%**
sooner on the same model, and Opus 5.5 at high effort cost more than at medium without a meaningful
increase in findings. That is a milder, production instance of the failure side drawn from
[[Simon Willison - 2026 in LLMs (so far)]]: more effort consumed budget without improving the result.
For the code quality reviewer, "Medium effort did lose real findings." In the randomized split, medium
led to roughly a quarter as many acted-on findings as high. The post also says performance lost real
findings at medium: its blinded [[LLM-as-a-Judge]] check found about **64%** fewer important performance
issues per review, about one fewer every 24 full-tier reviews. But that check compares the period before
the changes with now, across the model switch and every other change, so it does not isolate effort.
Security fell by about a quarter, not statistically significant.

On this page's open questions, the answer is local but concrete: in one workload, *medium* was enough
for the coordinator and lost real findings for a finding-generating reviewer. The post gives no exchange
rate between effort and model size. Unlike the in-turn controller in
[[Replit - Free the Models - Harness Design at the Frontier]], effort here is a fixed setting per role,
chosen for code quality by a randomized split.

The limits are the source's own. The figures are self-reported from one company's reviewer, and the
effort split had run one day. "An author changing the flagged lines shows they did something, not that
the finding was right", and "The judges are models too", with 35 to 66 findings per group. Performance
and security are still at medium effort; testing them at high is next.

## Open questions

- How does token-efficient training redistribute computation, and which trace interventions
  actually preserve quality or monitoring signals at fixed weights?
- Qwen3's partial-reasoning behaviour under truncation emerged rather than being trained. Why it works,
  and whether it degrades in ways benchmarks miss, is unexplained.
- Effort levels are calibrated against benchmark distributions. Does "medium effort" mean anything
  stable on out-of-distribution work?
  [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] gives one
  production data point, in the role question below: medium effort was enough for the coordinator but not
  for the code quality reviewer.
- Closed-model behaviour here is inferred. Raschka is explicit that GPT-5.6's internals are unknown and
  that his proposed diagram is "a possible implementation, not a confirmed description."
- If effort substitutes for parameters, what is the exchange rate, and does it hold across task types?
- What predicts a role's sensitivity to effort? At Cloudflare, high effort added cost without a
  meaningful increase in findings for the coordinator, while medium effort left code quality with
  roughly a quarter as many acted-on findings as high. Is the difference how much a role must explore,
  in calls and files opened, rather than how much it must reason? The two roles also ran different
  models, Opus 5.5 and Sonnet 5.5, so role and model are not separated.

## Related pages

- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[Cloudflare]]
- [[LLM-as-a-Judge]]
- [[Luca Zancato - Priming Hybrid Models from Pretrained Transformers]]
- [[Replit - Free the Models - Harness Design at the Frontier]]
- [[Simon Willison - 2026 in LLMs (so far)]]
- [[Model Routing]]
- [[Coding Agent Harness]]
- [[Reasoning Compression]]
- [[Test-Time Scaling]]
- [[LLM Reasoning]]
- [[Staged Reinforcement Learning Curriculum]]
- [[Reward Design for RL]]
- [[Knowledge Distillation]]
- [[LLM Training Pipeline]]
- [[Sebastian Raschka - Controlling Reasoning Effort in LLMs]]
- [[Qwen]]
- [[Z.ai]]
- [[Inference Efficiency Frontier]]
- [[adlrocha - Base Models Stopped Being the Bottleneck]]
