---
type: entity
entity_kind: organization
created: 2026-09-03
updated: 2026-09-03
tags: [entity, open-models, china, reasoning, architecture]
source_ids:
  - src-2026-08-30-adlrocha-base-models-bottleneck
status: active
---

# Qwen

Alibaba's open-weight model family, and one of the most widely derived-from lineages in the open ecosystem.
The vault's detailed coverage centres on **Qwen3.8-27B**.

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
  thinking disableable entirely — which GLM-5.3 does not permit. A concrete instance for
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

## Related pages

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
