---
type: entity
entity_kind: model-family
created: 2026-09-03
updated: 2026-10-16
tags: [entity, open-models, china, reasoning, architecture]
source_ids:
  - src-2026-08-30-adlrocha-base-models-bottleneck
  - src-2026-09-27-willison-llms-2026-so-far
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
  - src-2026-10-13-zancato-model-priming
  - src-2026-10-10-jaloza-microsoft-decision-1
status: active
---

# Qwen

Alibaba's open-weight model family, and one of the most widely derived-from lineages in the open ecosystem.
The vault covers **Qwen3.8-27B** as well as third-party conversions and scoring models derived
from other Qwen checkpoints. Their results are not interchangeable measurements of the family.

## Why it matters to this vault

Qwen is the **contrast case** to [[Z.ai]] in the vault's account of where capability now comes from. Where
GLM-5.3 reused its base model entirely, Qwen3.8-27B **did retrain** — on a Qwen3.5 foundation, with the config
still declaring `model_type: qwen3_5`. Its architecture is 64 layers arranged as 16 repeats of three Gated
DeltaNet blocks plus one Gated Attention block, with multi-token prediction. See
[[Linear Attention and Recurrent Memory]].

Its two most interesting choices are nonetheless post-training choices, per
[[adlrocha - Base Models Stopped Being the Bottleneck]]:

- **`preserve_thinking`, on by default.** The model keeps the thinking blocks of every historical message in
  context, and RL taught it to treat its own past reasoning as **working memory**. The three stated
  motivations are decision consistency, avoiding re-reasoning, and KV-cache reuse. This is new territory for
  the vault — reasoning traces retained as durable state rather than discarded per turn. See
  [[Context Engineering]], [[KV Cache]] and [[Agent Memory]].
- **`reasoning_effort` as an explicit knob** taking `xhigh`, `medium` or `low`, defaulting to `xhigh`, with
  the explicit thinking mode disableable — which GLM-5.3 does not permit. A concrete instance for
  [[Reasoning Effort Control]].

Qwen also supplies the vault's cleanest evidence for the **harness effect** at release time: under "Downstream
Compatibility: broader support for popular harnesses", **all of its coding benchmarks were run through the
Claude Code harness**. The reading offered is *"if you want a model to work inside a real agent loop, you
post-train it inside a real agent loop"* — which bears directly on [[Harness Optimization]] and
[[Coding Agent Harness]].

Separately, **Qwen-Image** is the model on which [[Baseten - Agentic Kernels in Production]] reports its
largest result, a **42.3% end-to-end latency reduction**, making Qwen a recurring subject on the serving side
as well.

## Caveats

The release is read here through a practitioner blog post mixing model-card reading with personal testing,
not through an independent evaluation. The source is explicit that the **distillation question is unsettled**:
whether Qwen3.8's gains come from its architecture or from training on stronger models' outputs is not
resolved by anything in the release. The three stated reasons for `preserve_thinking` are mechanistic
arguments rather than ablations.

## A local-use anecdote does not revise the effort API

[[Simon Willison - 2026 in LLMs (so far)]] describes a **17 GB Qwen3.8-27B** local setup taking
**21 minutes** on his illustrative SVG task. He calls its default effort "high"; adlrocha's
configuration account above specifies **`xhigh`**. Preserve that wording discrepancy and the
workload scope rather than replace the documented setting or derive a general speed ranking.

## An older Qwen checkpoint tests the limits of behavioral repair

[[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]] uses
**Qwen2.5-32B**, not the Qwen3.8 model above. Self-modeling is not uniformly preventive: the
Qwen bad-medical-advice condition does not improve. Identity/domain confounds and uneven
metrics prevent a universal repair claim, and its "agentic" evaluations are single-turn
scenarios without tools. This is separate evidence about fine-tuning robustness, not the
alignment status of the whole Qwen lineage.

## A donor for changed memory architectures and output interfaces

[[Luca Zancato - Priming Hybrid Models from Pretrained Transformers]] uses Qwen-derived
8B/32B hybrids to explore replacing selected attention layers with state-space layers.
The 32B reasoner's time-to-target-accuracy comparison uses a source model trained with the
same reasoning recipe. Reported near-source quality and cache savings are specific to that
conversion and serving setup, not an evaluation of Qwen3.8's native hybrid design.

[[Lisa Brown Jaloza - Microsoft-Decision-1]] gives another reuse path: adapt **Qwen3.5-9B**
for single-pass fixed-option scoring. That disclosed backbone does not disclose the full
training/scoring recipe or guarantee task calibration. Microsoft's planned Microsoft AI and
OpenAI backbones are future alternatives, not the base of the captured release.

Together these sources distinguish inheriting weights from preserving architecture or output
behavior. A derivative's benchmark does not transfer to every Qwen checkpoint or deployment.

## Related pages

- [[Luca Zancato - Priming Hybrid Models from Pretrained Transformers]]
- [[Lisa Brown Jaloza - Microsoft-Decision-1]]
- [[Microsoft-Decision-1]]

- [[Simon Willison - 2026 in LLMs (so far)]]
- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Emergent Misalignment]]
- [[LLM Training Pipeline]]

- [[adlrocha - Base Models Stopped Being the Bottleneck]]
- [[Z.ai]]
- [[Reasoning Effort Control]]
- [[Linear Attention and Recurrent Memory]]
- [[Open Model Ecosystems]]
- [[Harness Optimization]]
- [[Context Engineering]]
- [[KV Cache]]
- [[Baseten - Agentic Kernels in Production]]
- [[Small Language Models]]
