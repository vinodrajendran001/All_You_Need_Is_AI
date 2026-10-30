---
type: concept
created: 2026-09-25
updated: 2026-10-30
tags:
  - concept
  - fine-tuning
  - model-training
  - efficiency
source_ids:
  - src-2026-09-23-bytebytego-model-customization
  - src-2026-10-15-li-gradient-is-covariance
  - src-2026-10-27-bytebytego-apple-on-device
status: active
---

# Parameter-Efficient Fine-Tuning

## Definition

Parameter-efficient fine-tuning (PEFT) adapts a pretrained model by training a small set of new or
selected parameters while leaving most base weights frozen. LoRA represents each update with
low-rank matrices; QLoRA adds quantized storage for the frozen base model.

## Why it matters

PEFT separates a reusable base model from many cheaper specializations. Teams can train, version,
swap, and sometimes merge adapters without storing or updating a full model copy per task.

## Current synthesis

[[ByteByteGo - How to Customize a Model to Learn New Tricks]] places PEFT after a capability test:
prompt when the behavior already exists, retrieve when knowledge changes, and fine-tune when a
behavior must recur without repeated instruction. LoRA rank is a capacity choice rather than a
quality guarantee; example ranks such as 8, 16, 32, and 64 are search points.

QLoRA reduces the frozen model's storage, commonly to 4 bits, but adapter computation, optimizer
state, activations, and runtime work remain at higher precision. Quantizing the base therefore does
not make training memory equal to raw weight bytes.

Deployment preserves another choice. Keeping adapters separate saves storage and enables switching;
merging produces a standalone model but duplicates the base across specializations. Either path still
requires held-out task evaluation and regression checks on capabilities the adaptation was not meant
to change.

## Sparse updates are not low-rank updates

[[Yingru Li - The Gradient Is a Covariance]] cites full-parameter evidence that RL fine-tuning
changes only **5–30%** of a model's parameters across seven algorithms and ten models. On-policy
distillation and SFT on near-policy data reportedly behave similarly. Li argues that which
coordinates *can* move is predictable before any reward is seen. The cited overlap is that the
top **1%** of coordinates by Fisher hold **47.40%** of the top 1% by gradient magnitude, versus
**1%** at random.

That is a different structural claim from LoRA's. Sparsity limits **how many coordinates**
change; low rank limits the **dimension** of the change. A product of two low-rank factors is
generally dense in the original coordinates. This is the vault's observation, not Li's.

The post does not test adapters, masked fine-tuning, or Fisher-selected parameter subsets. Its
empirical figures are secondhand, and they come from full-parameter post-training rather than
adapter training. A Fisher ranking is therefore a candidate rule for choosing what to tune, not
a demonstrated PEFT method.

## Adapter reuse is a deployment-memory strategy as well as a training strategy

[[ByteByteGo - How Apple Fits an LLM on Your iPhone]] describes task-specific **rank-16
LoRA adapters stored at 16 bits**, occupying tens of megabytes around one frozen on-device
base. Several features can therefore share base-weight storage instead of each loading a
separate full model.

This extends the separate-versus-merged choice above: adapter modularity can matter at
inference even after training is over. The base's low-bit representation and the adapter's
precision are different choices, and reduced checkpoint duplication does not eliminate
activations, KV cache, switching overhead, or task-quality evaluation. The source reports the
design, not a controlled comparison of adapter ranks or whole-device performance.

## Open questions

- How should adapter rank and target modules be selected under a fixed data and compute budget?
- When do multiple adapters interfere enough to justify a merged or fully fine-tuned model?
- Which retained-capability tests best detect catastrophic specialization?
- Could a Fisher ranking computed on the model's own samples choose target modules or sparse
  parameter subsets as well as rank and module heuristics do?

## Related pages

- [[ByteByteGo - How Apple Fits an LLM on Your iPhone]]
- [[Apple]]
- [[On-Device Reasoning]]
- [[Yingru Li - The Gradient Is a Covariance]]
- [[Reinforcement Learning]]

- [[LLM Training Pipeline]]
- [[Model Quantization and Efficiency]]
- [[Knowledge Distillation]]
- [[Direct Preference Optimization]]
- [[ByteByteGo - How to Customize a Model to Learn New Tricks]]
