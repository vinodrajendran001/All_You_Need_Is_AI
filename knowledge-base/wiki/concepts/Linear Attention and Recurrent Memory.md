---
type: concept
created: 2026-08-03
updated: 2026-09-04
tags: [concept, transformers, attention, memory]
source_ids:
  - src-2026-07-27-neural-avb-looped-transformers
  - src-2026-07-27-waterloo-intern-gpt2-to-kimi-k3
  - src-2026-04-20-moonshotai-flashkda-v1
  - src-2026-08-30-adlrocha-base-models-bottleneck
  - src-2026-09-02-raschka-astra-looped-transformers
status: active
---

# Linear Attention and Recurrent Memory

## Definition

Linear-attention and recurrent-memory architectures replace token-addressable attention state with a
fixed-size state updated as tokens arrive. They trade exact retrieval of an arbitrary earlier token for
bounded memory and potentially linear-time sequence processing.

## Why it matters

Standard attention's cost is the reason most of the vault's inference material exists: the KV cache grows with
conversation length, and a 70B model with an 8k conversation needs a few GB **per request** — see [[KV Cache]].
Every technique on [[Inference Efficiency Frontier]] works around that growth. Linear attention attacks the
cause instead, by refusing to keep a per-token state at all.

The trade is real and not free. A fixed-size state cannot losslessly hold an arbitrary history, so the design
question is never "linear or quadratic" but **where to spend the exact-retrieval budget** — which is why the
architectures that ship are hybrids.

## Current synthesis

- Looped transformers repeatedly apply shared blocks, trading depth-specific parameters for more recurrent
  computation.
- Delta and gated-delta updates aim to control interference as new information overwrites the state.
- Hybrid designs periodically retain full attention, reserving token-addressable retrieval for positions where
  recurrence is insufficient.
- Kimi Delta Attention and FlashKDA belong to the systems side of this branch: architecture choices only become
  useful at scale when the recurrent update is implemented as a numerically stable, fused kernel.

## A shipped hybrid ratio

[[adlrocha - Base Models Stopped Being the Bottleneck]] gives the vault a concrete, released instance of the
hybrid pattern above. **Qwen3.8-27B** is built as **64 layers arranged as 16 repeats of three Gated DeltaNet
blocks plus one Gated Attention block**, with multi-token prediction.

The **3:1 ratio** is the interesting number. It is a published answer to the question the synthesis above
leaves open — how much full attention a hybrid needs — and it says that in a production model, three quarters
of the layers can run recurrent updates provided one quarter retains token-addressable retrieval. No ablation
justifying 3:1 rather than 2:1 or 7:1 is offered, so it should be read as one lab's operating point rather
than as a discovered optimum.

The model is built on a Qwen3.5 foundation, with the config still declaring `model_type: qwen3_5`. See
[[Qwen]].

## The context policy can undo the architecture

Qwen3.8 pairs that architecture with a decision that pushes the opposite way. **`preserve_thinking` is on by
default**, retaining the thinking blocks of every historical message so the model can treat its own past
reasoning as working memory — with KV-cache reuse given as one of the three stated motivations.

These two choices are in tension, and holding them together is the point. A hybrid architecture exists to make
long contexts affordable; a retention policy that keeps every prior thinking block spends that affordability
back. Whether the net is favourable depends on the workload, and nothing in the release measures it — the
three stated motivations are mechanistic arguments rather than ablations.

The general lesson generalises past Qwen: **architectural context savings and application-level context
policies are separate budgets**, and a model's effective context cost is set by their interaction rather than
by either alone. See [[Context Engineering]] and [[Reasoning Effort Control]].

## A second shipped ratio, and the same missing curve

[[Sebastian Raschka - OpenAI Astra and Looped Transformers]] adds a parallel data point to the hybrid ratio
recorded above. Where Qwen3.8 fixes a 3:1 ratio of Gated DeltaNet to Gated Attention blocks, **Nanbeige4.2-3B
reuses a 22-layer stack twice** — a different lever on the same trade, buying capacity without buying parameters.
Its published operating point is more informative than Qwen's, because it comes with a cost: **two passes
retained roughly 75% of the token efficiency** of a standard architecture, and additional passes *"gave barely any
gains but made the training much slower and much more expensive."*

The shared feature of both results is what this vault should record most carefully: **neither is accompanied by
an ablation curve.** Qwen's 3:1 and Nanbeige's ×2 are each one lab's chosen point, reported as a conclusion
rather than as a measurement, on architectural axes where the interesting question is the shape of the trade
rather than any single setting. Two independent labs converging on "a small integer works, more does not help"
is suggestive, but it is not the curve.

## Open questions

- What determines the right full-attention ratio in a hybrid, and does it depend on task, sequence length, or
  scale? Qwen's 3:1 is a datapoint without a curve.
- Does a recurrent state degrade gracefully or sharply as history exceeds what it can hold? The failure profile
  matters more for deployment than the average-case benchmark.
- Is `preserve_thinking`-style retention a net win on a linear-attention backbone specifically, where retained
  context is cheaper to carry than on a standard transformer?
- How much of the practical benefit is architecture and how much is kernel engineering? FlashKDA suggests the
  latter is a large share.
- Do these architectures change what [[Test-Time Scaling]] costs, given that reasoning traces are exactly the
  long, self-generated sequences they handle best?

## Related pages

- [[@neural_avb - What Are Looped Transformers?]]
- [[@waterloo_intern - From GPT-2 to Kimi K3]]
- [[MoonshotAI - FlashKDA v1 Deep Dive]]
- [[adlrocha - Base Models Stopped Being the Bottleneck]]
- [[Qwen]]
- [[Recursive Architectures]]
- [[Transformer Architecture]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Inference Efficiency Frontier]]
- [[Context Engineering]]
- [[Reasoning Effort Control]]
- [[Test-Time Scaling]]
- [[Sebastian Raschka - OpenAI Astra and Looped Transformers]]
- [[Sebastian Raschka]]
