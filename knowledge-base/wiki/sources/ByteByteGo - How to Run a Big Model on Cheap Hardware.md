---
type: source-summary
created: 2026-09-25
updated: 2026-09-25
source_id: src-2026-09-21-bytebytego-big-model-cheap-hardware
source_title: "How to Run a Big Model on Cheap Hardware?"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-to-run-a-big-model-on-cheap-hardware
tags: [source/summary, inference, quantization, local-llm]
source_ids: [src-2026-09-21-bytebytego-big-model-cheap-hardware]
status: active
---

# ByteByteGo - How to Run a Big Model on Cheap Hardware

## Summary

This survey organizes local inference around three levers: reduce memory, reduce computation, or move
work to a slower tier. It connects quantization, offloading, sparse experts, distillation, pruning,
KV-cache management, runtime kernels, and speculative decoding.

## Key claims

- An **8B** model requires about **16 GB** for 16-bit raw weights and theoretically **4 GB** at 4 bits,
  excluding metadata, cache, activations, and workspaces.
- A hypothetical **10 GB** transfer over a **10 GB/s** link costs about one second per generation step.
- A hypothetical 40B MoE at 4 bits still stores about **20 GB** even when only some experts execute.
- FlashAttention reduces memory traffic; PagedAttention reduces cache fragmentation; speculative
  decoding helps only when draft agreement repays verification and extra model memory.

## Why it matters

Capacity, active compute, memory tiers, and conversation state are different constraints. A model that
fits is not necessarily interactive, and savings from multiple techniques do not simply multiply.

## Tensions and caveats

The numerical examples are theoretical or hypothetical. The article supplies no named-model hardware
benchmark, quality result, latency result, or economic definition of cheap hardware.

## Raw capture

- [[2026-09-21 ByteByteGo - How to Run a Big Model on Cheap Hardware]]

## Affected pages

- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Mixture of Experts]]
- [[Speculative Decoding]]
- [[LLM Inference]]
- [[Inference Efficiency Frontier]]
- [[ByteByteGo]]

## Related pages

- [[Inference Serving Engines]]
- [[On-Device Reasoning]]
- [[Small Language Models]]
