---
type: concept
created: 2026-06-29
updated: 2026-06-30
tags:
  - concept
  - llm
  - inference
  - serving
  - efficiency
source_ids:
  - src-2026-06-26-nithin-llm-inference
  - src-2026-06-29-maarten-grootendorst-visual-guide-quantization
  - src-2026-06-29-siddhant-rai-turboquant
  - src-2026-06-30-alisa-liu-book-of-llms
status: active
---

# LLM Inference

## Definition

LLM inference is the runtime process of turning a prompt into generated tokens. Its defining property is that it is **two workloads, not one**: a compute-bound **prefill** phase that processes the whole prompt at once, and a memory-bound **decode** phase that emits one token at a time. Optimizing inference means optimizing these two phases separately, because they hit opposite hardware limits.

## Why it matters

Most efficiency techniques in the vault only make sense once this split is clear. Quantization, KV-cache compression, and serving-engine design are all responses to the fact that decode is throttled by memory bandwidth, while prefill is throttled by arithmetic throughput. This page is the hub that ties [[KV Cache]], [[Model Quantization and Efficiency]], and production serving together at the runtime level.

## Current synthesis

### The two phases

[[Nithin - What Actually Happens During LLM Inference]] gives the clearest statement:

- **Prefill** — the engine processes the entire prompt in parallel as a large matrix-matrix multiply (**GEMM**). It is **compute-bound**: speed is set by how many FLOPS the accelerator can run. Prefill's job is setup — it computes and stores the prompt's attention states into the [[KV Cache]] so they are never recomputed.
- **Decode** — the engine generates one token at a time as a matrix-vector multiply (**GEMV**). To produce a single token it must re-read the entire multi-gigabyte weight file from VRAM plus the growing KV cache. It is **memory-bandwidth-bound**: the math finishes instantly and the cores starve waiting on High Bandwidth Memory (HBM).

This is why per-token latency in long generations is governed by *bytes moved*, not *operations done*. It is the same memory-bound framing that [[Dwarkesh Patel - Reiner Pope Flashcards]] expresses as "per-token latency is the max of compute time and memory time."

### Why the split drives every optimization

- **Weight compression** (see [[Model Quantization and Efficiency]] and [[Maarten Grootendorst - A Visual Guide to Quantization]]) shrinks the bytes that decode must move per token. The source lists AWQ and EXL2 (4-bit GPU serving, important weights kept higher-precision), FP8 (Hopper default) and NVFP4 (Blackwell) as native low-precision formats the cores compute on directly, and GGUF for consumer/split CPU-GPU running.
- **KV-cache compression** ([[KV Cache]], [[Siddhant Rai - TurboQuant - Online Vector Quantization]]) attacks the *other* growing object decode must read — the cache itself, which at long context can exceed model weights.
- **Loading format** matters: `mmap` maps the weight file into virtual memory and lazily loads pages on demand, giving near-zero startup and shared physical memory across processes.

### Serving multiple users

Production engines must serve many concurrent requests:

- **vLLM and SGLang** focus on dynamic memory via **PagedAttention**, slicing the KV cache into pages and treating VRAM like OS virtual memory to stop fragmentation.
- **TensorRT-LLM and TGI** lean on graph compilation and custom kernels for raw throughput.
- **Continuous batching** injects new prefill tasks directly into ongoing decode loops to keep utilization high. Because prefill saturates the tensor cores, active users' decode briefly pauses while a new prompt's prefill runs — a direct consequence of the compute-bound/memory-bound conflict.

### Connections

- The decode/memory-bound view is why [[Reasoning Compression]] treats reasoning tokens as a systems cost: more tokens means more memory-bound decode steps and a larger KV cache.
- [[Small Language Models]] and [[On-Device Reasoning]] inherit this page's constraints in their most extreme form, where every token competes for memory and power.
- [[Alisa Liu - Book of LLMs]] adds an interview-oriented checklist of the inference toolbox that complements this hub: **batching & packing**, **speculative decoding** (a small draft model proposes tokens a large model verifies), **KV cache** and how to reduce its size, sampling strategies, and **Flash Attention** (IO-aware exact attention). It is a good rapid-review companion for the inference questions described in [[ML Research Interview Preparation]].

## Open questions

- Where exactly is the prefill↔decode crossover for a given model/hardware, and how should schedulers (chunked prefill, disaggregated prefill/decode) exploit it?
- Which weight + KV compression combinations give the best end-to-end tokens/sec without unacceptable quality loss?
- As context windows grow, does decode become so memory-bound that KV-cache compression matters more than weight quantization?

## Related pages

- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[Nithin - What Actually Happens During LLM Inference]]
- [[Maarten Grootendorst - A Visual Guide to Quantization]]
- [[Siddhant Rai - TurboQuant - Online Vector Quantization]]
- [[Alisa Liu - Book of LLMs]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[Reasoning Compression]]
- [[AI Accelerator Architecture]]
- [[Transformer Architecture]]
- [[AI Knowledge Base Overview]]
