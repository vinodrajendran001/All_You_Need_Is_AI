---
type: source-summary
created: 2026-06-26
updated: 2026-10-09
source_id: src-2026-06-26-nithin-llm-inference
source_title: "What Actually Happens During LLM Inference?"
source_author: Nithin
source_url: https://medium.com/@nithinellanki/what-actually-happens-during-llm-inference-e9e756715fc8
tags:
  - source/summary
  - inference
  - serving
  - kv-cache
  - quantization
status: active
source_ids:
  - src-2026-06-26-nithin-llm-inference
---

# Nithin - What Actually Happens During LLM Inference

## Summary

This Medium article explains autoregressive inference through two common operating regimes:
**prefill** processes many prompt positions together and can be compute-bound; low-batch **decode**
often spends more time reading weights and KV state than on arithmetic. The article presents the
contrast categorically, but it is a useful simplified model rather than a universal bottleneck
classification.

From that split, it motivates weight compression, KV caching, loading formats, and production
scheduling. A long prefill can interfere with active decodes on a shared worker; the outcome also
depends on the scheduler rather than following inevitably from continuous batching.

## Key claims

- **Two phases, with workload-dependent bottlenecks.** Prefill reuses weights across prompt positions. A dense, unbatched decode has narrow matrix-vector work; batching can reuse those weights across sequences. Architecture, context, and kernels affect the actual bottleneck.
- **Prefill builds reusable KV state.** While retained, those states avoid re-projecting the same prefix at each decode step; this is not a guarantee against recomputation after eviction.
- **Memory traffic can dominate decode.** The article's whole-weight-read argument describes the dense, low-batch case, not every sparse, sharded, cached, or batched execution.
- **`mmap` defers file reads.** It maps a file into virtual memory and can share file-backed pages. The source's "near-zero startup" claim concerns avoiding eager loading, not eliminating cold-page I/O, first-use latency, or transfers into GPU memory.
- **Weight compression cuts bytes moved during decode:** AWQ and EXL2 are 4-bit GPU-serving methods that keep important weights higher-precision; FP8 (Hopper default) and NVFP4 (Blackwell) are native low-precision formats the cores compute on directly; GGUF targets consumer/split CPU-GPU running.
- **Serving engines differ in strategy:** vLLM/SGLang focus on dynamic memory via PagedAttention (treating VRAM like OS virtual memory to stop fragmentation); TensorRT-LLM/TGI lean on graph compilation and custom kernels for raw throughput.
- **Continuous batching** lets requests join and leave between iterations. Prefill/decode contention is a possible scheduling cost; chunking and worker separation change it.

## Why it matters

This article gives the vault its clearest single statement of the **prefill/decode, compute-bound/memory-bound** distinction, which several pages reference implicitly. It seeds the new concept [[LLM Inference]] and connects [[KV Cache]] (why decode is memory-bound) with [[Model Quantization and Efficiency]] (why weight compression buys decode speed). It also adds named serving engines and the PagedAttention/continuous-batching pattern already referenced from [[KV Cache]] and [[Small Language Models]].

## Tensions / open questions

- The article is a high-level explainer; exact FLOPS/bandwidth numbers and the prefill↔decode crossover depend on model size, batch, context length, and hardware.
- **October 9 qualification:** the previous summary repeated the bottlenecks and startup claim as unconditional facts. [[Arithmetic Intensity and the Roofline Model]] and [[Prefill-Decode Disaggregation]] retain the regime and scheduling limits; inference need not include a decode loop at all.
- It lists compression formats without head-to-head accuracy/latency data; comparisons live in [[Maarten Grootendorst - A Visual Guide to Quantization]] and the TurboQuant sources.
- Continuous-batching interference (prefill stalling decode) is described qualitatively; scheduling mitigations (chunked prefill, disaggregated prefill/decode) are not covered.

## Affected pages

- [[Arithmetic Intensity and the Roofline Model]]
- [[Inference Serving Engines]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Model Quantization and Efficiency]]
- [[Prefill-Decode Disaggregation]]

## Citations
- Source URL: [https://medium.com/@nithinellanki/what-actually-happens-during-llm-inference-e9e756715fc8](https://medium.com/@nithinellanki/what-actually-happens-during-llm-inference-e9e756715fc8)

## Raw capture

- [[2026-06-26 Nithin - What Actually Happens During LLM Inference|What Actually Happens During LLM Inference]]

## Related pages

- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[Maarten Grootendorst - A Visual Guide to Quantization]]
- [[Siddhant Rai - TurboQuant - Online Vector Quantization]]
- [[Small Language Models]]
- [[AI Knowledge Base Overview]]
- [[ML Systems at Scale]]
