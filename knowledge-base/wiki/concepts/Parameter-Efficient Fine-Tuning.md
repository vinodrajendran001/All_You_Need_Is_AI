---
type: concept
created: 2026-09-25
updated: 2026-09-25
tags:
  - fine-tuning
  - model-training
  - efficiency
source_ids:
  - src-2026-09-23-bytebytego-model-customization
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

## Open questions

- How should adapter rank and target modules be selected under a fixed data and compute budget?
- When do multiple adapters interfere enough to justify a merged or fully fine-tuned model?
- Which retained-capability tests best detect catastrophic specialization?

## Related pages

- [[LLM Training Pipeline]]
- [[Model Quantization and Efficiency]]
- [[Knowledge Distillation]]
- [[Direct Preference Optimization]]
- [[ByteByteGo - How to Customize a Model to Learn New Tricks]]
