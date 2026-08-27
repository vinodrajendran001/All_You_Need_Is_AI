---
type: source-summary
created: 2026-07-04
updated: 2026-08-26
source_id: src-2026-06-30-onur-sirin-local-llm-memory-hardware
source_title: "How Local LLMs Run: Memory and Hardware"
source_author: Onur Sirin
source_url: https://silicontales.com/local-llm-complete-guide/?trk=feed_main-feed-card_feed-article-content
tags:
  - source/summary
  - inference
  - local-llm
  - hardware
  - memory
status: active
source_ids:
  - src-2026-06-30-onur-sirin-local-llm-memory-hardware
---

# Onur Sirin - How Local LLMs Run

## Summary

This Silicon Tales guide explains local LLM execution from two angles: an eight-stage pipeline for how a prompt becomes streamed tokens, and the memory arithmetic that determines which models fit and how fast they run. It compares four hardware shapes — RTX 5090 desktop, Mac Studio M3 Ultra, rumored M5 Ultra, and Asus ET900N G3 / GB300 — to show that "local LLM" performance is not one scalar. Capacity, bandwidth, and memory topology matter differently at different stages.

The most durable point is the same one now central to [[LLM Inference]]: **prefill is compute-bound, decode is bandwidth-bound**. But this guide adds an especially concrete local-hardware layer: the model's total memory need is roughly **weights + KV cache + activations + overhead**, Q4 is a practical local sweet spot, and **fitting in memory is not the same as running at full speed**. A model that spills from fast VRAM/HBM into slower system RAM or LPDDR may technically fit but decode far slower.

## Key claims

- A local prompt passes through eight stages: cold load, tokenize, prefill, hold KV cache, decode one token, sample, repeat the generation loop, and detokenize/stream output.
- **Prefill** processes the whole prompt at once and is **compute-bound**; it is limited by tensor/GPU core throughput.
- **Decode** produces one token at a time and is **bandwidth-bound**; it reads model weights plus the growing KV cache from memory per token, so tokens/sec depends on memory bandwidth.
- Model memory is not just weights: total need is **weights + KV cache + activations + overhead**. At medium context, a practical shortcut is `total ≈ weights × 1.2`; at very long context, KV cache must be counted separately.
- Weight size is approximately `parameter count × bytes per parameter`: FP16 ≈ 2 bytes/parameter, Q8 ≈ 1 byte/parameter, Q4 ≈ 0.5–0.55 bytes/parameter.
- **Q4** is the common local sweet spot: roughly 4× smaller than FP16 with usually small quality loss. Q4_K_M is described as a balanced recipe; NVFP4 is NVIDIA's hardware-optimized 4-bit format.
- Hardware memory types matter:
  - **GDDR7 / VRAM**: small, very fast, consumer GPU memory (RTX 5090 ≈ 32GB, ~1.79 TB/s).
  - **Unified memory**: CPU/GPU share one flat pool (Mac Studio; lower bandwidth but more capacity and no copy boundary).
  - **HBM3e**: premium high-bandwidth memory near the accelerator (GB300, ~7.1 TB/s fast tier).
  - **LPDDR5X**: large, lower-power, slower memory used as a second coherent tier in GB300.
- **MoE saves speed, not capacity**: the whole model must fit in memory, but per token only active experts are read. This is why a much larger MoE can decode quickly if active experts fit in fast memory.
- **Fitting is not full-speed running**: flat/unified memory has one speed everywhere; tiered systems may fit huge models but run at mixed speeds depending on which weights land in HBM vs LPDDR; a 5090 spilling over PCIe to system RAM collapses in speed.

## Why it matters

This source turns the vault's existing prefill/decode and KV-cache ideas into a concrete local-hardware decision framework. It deepens [[LLM Inference]] with a full eight-stage local pipeline, strengthens [[AI Accelerator Architecture]] with the distinction between **flat**, **tiered**, and **tiny-but-fast** memory shapes, and makes [[On-Device Reasoning]] and [[Small Language Models]] more practical: the deployment question is not only "can the model fit?" but "where does it fit, and at what bandwidth?"

## Tensions / open questions

- The machine comparison mixes available systems with rumored / estimated future hardware (especially M5 Ultra), so those claims should be treated as directional.
- The source's speed examples compare different models on different machines; it explicitly warns these are not head-to-head races.
- The guide is local-hardware oriented, not production serving oriented. It complements but does not replace serving-engine discussions in [[Nithin - What Actually Happens During LLM Inference]].

## Affected pages

- [[AI Accelerator Architecture]]
- [[LLM Inference]]
- [[Model Quantization and Efficiency]]
- [[On-Device Reasoning]]
- [[Onur Sirin]]
- [[Small Language Models]]

## Citations
- Source URL: [https://silicontales.com/local-llm-complete-guide/](https://silicontales.com/local-llm-complete-guide/?trk=feed_main-feed-card_feed-article-content)

## Raw capture

- [[How Local LLMs Run - Memory and Hardware]]

## Related pages

- [[LLM Inference]]
- [[AI Accelerator Architecture]]
- [[Model Quantization and Efficiency]]
- [[On-Device Reasoning]]
- [[Small Language Models]]
- [[Nithin - What Actually Happens During LLM Inference]]
- [[Onur Sirin]]
- [[AI Knowledge Base Overview]]
