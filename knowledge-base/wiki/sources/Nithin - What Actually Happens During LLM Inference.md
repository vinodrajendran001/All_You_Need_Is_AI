---
type: source-summary
created: 2026-06-26
updated: 2026-06-26
source_id: src-2026-06-26-nithin-llm-inference
source_title: "What Actually Happens During LLM Inference?"
source_author: Nithin
source_url: https://medium.com/@nithinellanki/what-actually-happens-during-llm-inference-e9e756715fc8
tags:
  - source-summary
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

This Medium article gives a compact systems-level account of LLM inference, organized around its central claim: inference is not one workload but two, with opposite bottlenecks. The **prefill** phase processes the whole prompt at once as a large matrix-matrix multiply (GEMM) and is **compute-bound** (FLOPS-limited); it builds the KV cache. The **decode** phase generates one token at a time as a matrix-vector multiply (GEMV), must re-read the entire multi-gigabyte weight file plus the growing KV cache per token, and is therefore **memory-bandwidth-bound**.

From that split, the article derives why loading format and weight compression matter (mmap, AWQ/EXL2/FP8/NVFP4/GGUF) and how production serving engines (vLLM, SGLang, TensorRT-LLM, TGI) use PagedAttention and continuous batching — and why injecting a new prefill into an active decode batch briefly slows everyone's generation.

## Key claims

- **Inference splits into two phases with different bottlenecks.** Prefill = compute-bound GEMM over the full prompt; decode = memory-bound GEMV, one token at a time.
- **Prefill builds the KV cache** so the prompt's attention states are never recomputed during decode.
- **Decode re-reads the whole model (and growing KV cache) from VRAM per token**, so cores sit idle waiting on High Bandwidth Memory (HBM); speed is set by memory bandwidth, not math.
- **`mmap` (memory mapping)** maps the weight file into virtual memory and lazily loads pages on demand, giving near-zero startup and shared physical memory across processes.
- **Weight compression cuts bytes moved during decode:** AWQ and EXL2 are 4-bit GPU-serving methods that keep important weights higher-precision; FP8 (Hopper default) and NVFP4 (Blackwell) are native low-precision formats the cores compute on directly; GGUF targets consumer/split CPU-GPU running.
- **Serving engines differ in strategy:** vLLM/SGLang focus on dynamic memory via PagedAttention (treating VRAM like OS virtual memory to stop fragmentation); TensorRT-LLM/TGI lean on graph compilation and custom kernels for raw throughput.
- **Continuous batching** injects new prefill tasks into ongoing decode loops to keep utilization high; because prefill saturates the tensor cores, active users' decode briefly pauses until the new prefill finishes.

## Why it matters

This article gives the vault its clearest single statement of the **prefill/decode, compute-bound/memory-bound** distinction, which several pages reference implicitly. It seeds the new concept [[LLM Inference]] and connects [[KV Cache]] (why decode is memory-bound) with [[Model Quantization and Efficiency]] (why weight compression buys decode speed). It also adds named serving engines and the PagedAttention/continuous-batching pattern already referenced from [[KV Cache]] and [[Small Language Models]].

## Tensions / open questions

- The article is a high-level explainer; exact FLOPS/bandwidth numbers and the prefill↔decode crossover depend on model size, batch, context length, and hardware.
- It lists compression formats without head-to-head accuracy/latency data; comparisons live in [[Maarten Grootendorst - A Visual Guide to Quantization]] and the TurboQuant sources.
- Continuous-batching interference (prefill stalling decode) is described qualitatively; scheduling mitigations (chunked prefill, disaggregated prefill/decode) are not covered.

## Affected pages

- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[ML Systems at Scale]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/What Actually Happens During LLM Inference.md`
- Source URL: [https://medium.com/@nithinellanki/what-actually-happens-during-llm-inference-e9e756715fc8](https://medium.com/@nithinellanki/what-actually-happens-during-llm-inference-e9e756715fc8)

## Related pages

- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[Maarten Grootendorst - A Visual Guide to Quantization]]
- [[Siddhant Rai - TurboQuant - Online Vector Quantization]]
- [[Small Language Models]]
- [[AI Knowledge Base Overview]]
