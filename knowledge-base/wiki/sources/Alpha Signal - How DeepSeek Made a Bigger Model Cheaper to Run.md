---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-14-alphasignal-deepseek-v4-1-flash
source_title: "How DeepSeek made a bigger model cheaper to run"
source_author: Alpha Signal
source_url: https://www.deepseek.com/news/deepseek-v4-1-flash/
tags: [source/summary, deepseek, inference, kv-cache]
source_ids: [src-2026-09-14-alphasignal-deepseek-v4-1-flash]
status: active
---

# Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run

## Summary

This secondary explainer uses DeepSeek V4.1-Flash to show why total parameters poorly predict serving
cost. It describes a 552B-parameter sparse backbone with separate encoder/decode activity, local state
reconstruction, compressed sparse long-range retrieval, and an FP4 global KV cache.

## Key claims

- The reported backbone has **552B total parameters**, 384 routed experts, one shared expert, and six
  routed experts per token; an alternative 763B count includes auxiliary components.
- Active parameters are reported as **8B per input token** and **16B per generated token**.
- Global cache growth falls from about **48 KB/token** in V3.2 to **3,514 bytes** in V4-Flash and
  **890 bytes** in V4.1-Flash.
- Hierarchical retrieval narrows history to at most 2,048 blocks and selects up to 512 compressed
  positions; the global cache is stored in FP4.
- The article reports roughly one-quarter V4-Flash HBM and one-eighth its persistent SSD cache.

## Why it matters

Inference economics depends on active parameters, cache bytes, persistence, and retrieval work—not
the headline parameter count. Long-context efficiency is an architectural stack rather than one trick.

## Tensions and caveats

The clipping has no byline and points through Alpha Signal redirects to DeepSeek's announcement. It
reports no hardware, throughput, latency, or independent verification. The encoder/decoder activity
description and all product figures should be checked against the primary technical report.

## Raw capture

- [[2026-09-14 Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]

## Affected pages

- [[KV Cache]]
- [[Mixture of Experts]]
- [[Inference Efficiency Frontier]]
- [[DeepSeek]]

## Related pages

- [[LLM Inference]]
- [[Linear Attention and Recurrent Memory]]
- [[Alpha Signal]]

