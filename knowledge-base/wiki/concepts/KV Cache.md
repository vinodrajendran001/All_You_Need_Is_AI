---
type: concept
created: 2026-06-17
updated: 2026-06-29
tags:
  - concept
  - kv-cache
  - inference
  - long-context
  - quantization
source_ids:
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-06-10-0xkato-how-llms-actually-work
  - src-2026-06-17-prateek-singh-kv-cache-turboquant
  - src-2026-06-24-bytebytego-llm-vs-slm
  - src-2026-06-26-nithin-llm-inference
  - src-2026-06-29-siddhant-rai-turboquant
status: active
---

# KV Cache

## Definition

KV cache is the stored collection of Key and Value tensors from previous tokens during autoregressive Transformer generation. Instead of recomputing Keys and Values for the entire prefix every time the model generates a new token, the model computes them once, stores them, and appends only the new token's K/V tensors on each decoding step.

## Why it matters

KV cache turns generation from "reread the whole book every token" into "reuse the notes already taken." That is essential for fast autoregressive decoding, but it creates a different bottleneck: long contexts consume huge GPU memory because the cache grows with context length, layer count, head dimension, number of K/V heads, and precision.

## Current synthesis

- [[Transformer Architecture]] treats KV cache as the operational side of attention: architecture is not just a training blueprint, because real decoding depends on cached inference state.
- [[0xkato - How LLMs Actually Work]] clarifies the basic role of KV cache inside multi-head attention: each attention head would otherwise need old Key and Value vectors for every token repeatedly. Modern GQA reduces memory pressure by letting many query heads share fewer K/V heads.
- [[Prateek Singh - KV Cache and TurboQuant]] gives the clearest systems framing: KV cache trades repeated compute for memory storage. For short contexts this is an obvious win; for long contexts, memory becomes the main limiter.
- [[ByteByteGo - Large Language Models vs Small Language Models]] shows how KV-cache pressure shapes [[Small Language Models]]. Grouped-query attention, sliding-window attention, and layer-level cache sharing are not just academic attention variants; they are direct responses to the memory limits of phones, edge devices, and high-volume serving.
- [[Nithin - What Actually Happens During LLM Inference]] places the cache inside the inference lifecycle (see [[LLM Inference]]): the **prefill** phase computes and stores the prompt's K/V states so they are never recomputed, and the **decode** phase must re-read the growing cache (plus all weights) every token. This is the concrete reason decode is memory-bandwidth-bound and why cache size directly caps tokens/sec.

## Memory scaling

KV cache grows linearly in sequence length:

```
KV memory ~= 2 x tokens x layers x KV_heads x head_dim x bytes_per_value
```

The leading `2` is for Keys and Values. The practical implication is severe: doubling context length doubles the cache. The source's example numbers show why long-context serving is hard even when model weights fit:

| Model | 4K tokens | 32K tokens | 100K tokens | 1M tokens |
| --- | ---: | ---: | ---: | ---: |
| LLaMA 3 8B | 537 MB | 4.3 GB | 13.1 GB | 131 GB |
| LLaMA 3 70B | 1.3 GB | 10.7 GB | 32.8 GB | 327 GB |
| Mistral 7B | 537 MB | 4.3 GB | 13.1 GB | 131 GB |

## Optimization families

KV-cache optimization is not one technique. The current design space has several families:

1. **Token eviction** — H2O and StreamingLLM identify low-importance tokens and delete them from the cache. This can produce high compression but is risky for retrieval or tasks where a "low-attention" token later becomes crucial.
2. **Paged allocation** — vLLM / PagedAttention do not shrink the tensor values; they allocate cache memory in pages to reduce fragmentation and raise utilization.
3. **Architecture-level sharing** — GQA, MQA, and MLA reduce the number or representation size of K/V heads. These are powerful but must be built into the model architecture/training recipe.
4. **Predictive skipping** — SnapKV and PyramidKV use early-layer signals to predict which tokens matter later, trading memory for task-dependent prediction risk.
5. **KV quantization** — store K/V values in fewer bits. Simple INT8 gives a safe 2x reduction; more aggressive 3-4 bit schemes require additional tricks to avoid corrupting attention scores.
6. **Sliding-window and cache-sharing designs** — restrict some layers to recent context or reuse cache state across layers. These are especially relevant for small/on-device models where every additional token competes with memory and battery budgets.

## TurboQuant

TurboQuant is an aggressive KV quantization pipeline described in [[Prateek Singh - KV Cache and TurboQuant]]. Its key promise is 3-4 bit KV cache compression without retraining and without token deletion.

The pipeline:

1. **Random rotation** spreads outlier-heavy KV values across dimensions with an orthogonal transform, preserving inner products while making quantization easier.
2. **Scalar quantization** maps the rotated values into low-bit centroids, with 3-bit framed as the production sweet spot.
3. **QJL bias correction** stores lightweight Johnson-Lindenstrauss sign sketches to correct systematic attention-score bias introduced by quantization.

The important distinction: TurboQuant compresses **runtime KV cache**, not model weights. It should be combined with separate weight-compression methods such as GPTQ/AWQ if the model weights themselves are the bottleneck.

[[Siddhant Rai - TurboQuant - Online Vector Quantization]] adds the deeper mathematical account behind this pipeline. It reframes KV quantization as a **rate-distortion problem** whose true objective is preserving the attention inner product `qᵀk ≈ qᵀk̂`, not raw MSE. The reason weight-style methods fail on the cache is statistical: weights are static and roughly Gaussian (calibrate offline once), while KV vectors are **dynamic and shift per input**, so any fixed codebook (INT4 uniform, NF4 Gaussian) is misaligned. TurboQuant therefore *transforms then quantizes* — rotate into a known Gaussian space and apply a **Lloyd-Max optimal codebook** (the "where the vector is" / MSE branch) — and handles the leftover with **QJL**, a Johnson-Lindenstrauss random projection plus 1-bit sign quantization (the "which direction" / inner-product branch). Reported results include perfect needle-in-a-haystack recall at ~4× compression.

## Open questions

- Which KV-compression methods preserve retrieval accuracy best under 100K+ context lengths?
- Can aggressive KV quantization become a standard serving-kernel feature, or will implementation complexity keep it research-stage?
- How should agent systems decide when to summarize, evict, quantize, or route around expensive long-context state?

## Related pages

- [[Prateek Singh - KV Cache and TurboQuant]]
- [[Siddhant Rai - TurboQuant - Online Vector Quantization]]
- [[Nithin - What Actually Happens During LLM Inference]]
- [[LLM Inference]]
- [[Small Language Models]]
- [[ByteByteGo - Large Language Models vs Small Language Models]]
- [[Transformer Architecture]]
- [[Model Quantization and Efficiency]]
- [[On-Device Reasoning]]
- [[Context Engineering]]
- [[Reasoning Compression]]
- [[Mixture of Experts]]
- [[AI Knowledge Base Overview]]
