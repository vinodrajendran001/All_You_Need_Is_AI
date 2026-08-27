---
type: entity
created: 2026-07-04
updated: 2026-07-04
entity_kind: person
tags:
  - entity
  - person
  - hardware
  - inference
source_ids:
  - src-2026-06-30-onur-sirin-local-llm-memory-hardware
status: active
---

# Onur Sirin

## What it is

Onur Sirin is the author of the Silicon Tales guide [[Onur Sirin - How Local LLMs Run]], which explains local LLM execution, memory sizing, and hardware tradeoffs across consumer GPUs, Apple unified memory, and GB300-class coherent memory systems.

## Why it matters here

His source gives the vault a practical local-hardware layer for [[LLM Inference]], [[AI Accelerator Architecture]], [[On-Device Reasoning]], and [[Small Language Models]]. It translates abstract claims like "decode is memory-bound" into concrete questions: how much memory does the model occupy, what type of memory does it sit in, and is it running from a flat pool, a tiered pool, or a tiny fast VRAM island?

## Notes

- The guide is explanatory rather than a benchmark paper; it compares hardware philosophies and includes some estimates/rumors for future systems.

## Related pages

- [[Onur Sirin - How Local LLMs Run]]
- [[LLM Inference]]
- [[AI Accelerator Architecture]]
- [[On-Device Reasoning]]
- [[AI Knowledge Base Overview]]
