---
type: source-summary
created: 2026-06-17
updated: 2026-06-17
source_id: src-2026-06-17-prateek-singh-kv-cache-turboquant
source_title: KV Cache & TurboQuant
source_author: Prateek Singh
source_url: https://prateeksinghphd.in/kvcache-full-blog.html
tags:
  - source-summary
  - kv-cache
  - quantization
  - inference
  - long-context
source_ids:
  - src-2026-06-17-prateek-singh-kv-cache-turboquant
status: active
---

# Prateek Singh - KV Cache and TurboQuant

## Summary

An interactive explainer on KV cache memory pressure and TurboQuant, a 2026 Google / ICLR technique for aggressively compressing KV cache tensors. The article first explains the basic speed/memory tradeoff of KV caching, then surveys five major KV-cache compression directions, and finally breaks down TurboQuant's three-step pipeline: random rotation, scalar quantization, and QJL bias correction.

## Key claims

- KV cache solves the compute waste of autoregressive decoding by computing each past token's Keys and Values once and reusing them.
- The tradeoff is memory: KV cache stores K and V tensors for every token, every layer, and every head. Long contexts therefore hit GPU memory limits even when model weights fit.
- Long-context examples are stark:
  - LLaMA 3 8B: 4K context ~= 537 MB KV cache; 100K context ~= 13.1 GB; 1M context ~= 131 GB.
  - LLaMA 3 70B: 32K context ~= 10.7 GB; 100K context ~= 32.8 GB; 1M context ~= 327 GB.
- Existing KV-memory approaches each attack a different bottleneck:
  - **Token eviction** (H2O, StreamingLLM): delete low-importance cached tokens; strong compression but permanently loses context.
  - **Paged allocation** (vLLM / PagedAttention): change allocation strategy rather than representation; improves utilization but stores full-precision values.
  - **Architecture-level sharing** (GQA, MQA, MLA): train models that need fewer K/V heads or use latent projections; strong reductions but must be baked into the model.
  - **Predictive skipping** (SnapKV, PyramidKV): use earlier attention patterns to predict which tokens matter later; adaptive but error-prone.
  - **Simple INT8 quantization**: easy 2x reduction, but lower bit depths fail quickly without additional correction.
- TurboQuant's claim: compress KV cache to 3-4 bits with minimal quality loss, without retraining and without deleting tokens.

## TurboQuant pipeline

1. **Random rotation** — use a Hadamard-style orthogonal transform to spread lopsided KV energy across dimensions. The geometry / inner products are preserved, but outlier dimensions no longer dominate quantization.
2. **Scalar quantization** — after rotation, values look closer to Gaussian, so low-bit Lloyd-Max codebooks can map values to centroids. The article frames 3-bit as the production sweet spot.
3. **QJL bias correction** — store 1-bit sign sketches based on Johnson-Lindenstrauss projections to correct systematic quantization bias in attention scores.

## Reported results and caveats

- Claimed storage: TurboQuant compressed example per head is 928 bits vs 4,096 bits FP16 (about 4.4x); the article summarizes production gains as 4-6x / about 5x depending on setting.
- Reported benchmark impact:
  - 4-bit TurboQuant: <0.3 point drop.
  - 3-bit TurboQuant: <0.6 point drop, recommended sweet spot.
- Claimed serving impact: for LLaMA 3 8B with a 30 GB KV budget, 100K-context concurrency rises from 2 users to 11 users.
- Important caveats:
  - TurboQuant compresses **KV cache only**, not model weights.
  - Minimal benefit below 8K tokens because rotation overhead is not worth it.
  - As described, it is still research-stage and not a first-class vLLM / TensorRT-LLM feature.
  - The "8x faster" headline uses an FP32 baseline; against optimized FP16, the attention speedup is closer to 2-3x, while the memory reduction remains the main win.

## Why it matters

This source justifies splitting [[KV Cache]] into its own concept page. KV cache is not merely an implementation detail inside [[Transformer Architecture]]; it is now one of the core cost surfaces for long-context inference, agent loops, and on-device reasoning.

## Affected pages

- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[Transformer Architecture]]
- [[On-Device Reasoning]]
- [[AI Knowledge Base Overview]]

## Raw capture

- `knowledge-base/raw/sources/KV Cache & TurboQuant — Prateek Singh PhD.md`

## Related pages

- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[Transformer Architecture]]
- [[On-Device Reasoning]]
- [[Mixture of Experts]]
- [[AI Knowledge Base Overview]]
