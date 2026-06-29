---
type: source-summary
created: 2026-06-29
updated: 2026-06-29
source_id: src-2026-06-29-siddhant-rai-turboquant
source_title: "TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate"
source_author: Siddhant Rai
source_url: https://vizuara.substack.com/p/turboquant-online-vector-quantization
tags:
  - source-summary
  - quantization
  - kv-cache
  - vector-quantization
  - long-context
status: active
source_ids:
  - src-2026-06-29-siddhant-rai-turboquant
---

# Siddhant Rai - TurboQuant - Online Vector Quantization

## Summary

This Vizuara deep-dive explains TurboQuant, an online vector-quantization method for compressing the KV cache of long-context LLMs with provable near-optimal distortion. The article first builds the problem: the KV cache (not weights) is often the dominant memory cost at long context, and it must be compressed *online* because its distribution is dynamic and shifts with every input — unlike static, roughly-Gaussian weights. It then reframes quantization as a **rate-distortion optimization** whose true objective is preserving the attention inner product `qᵀk ≈ qᵀk̂`, not raw MSE.

TurboQuant's solution is a two-step decomposition: (1) an **MSE/where-the-vector-is** branch that rotates data into a known (Gaussian) space and applies a precomputed **Lloyd-Max optimal codebook**, and (2) an **inner-product/which-direction** branch that handles the residual with **QJL** — a Johnson-Lindenstrauss random projection followed by 1-bit sign quantization that provably preserves inner products. The combination of an (N−1)-bit codebook plus a 1-bit QJL residual beats naive N-bit quantization and reaches near-optimal distortion online.

## Key claims

- **There are two places to quantize an LLM:** weight space (static, one-time, well-understood) and token/activation space (dynamic, online, where the KV cache lives). KV-cache quantization is the open frontier.
- **KV cache size** `= 2 × L × H × d × n × bytes`; at 128k context a single LLaMA-70B layer's KV cache can rival the model weights, and across layers it exceeds them.
- **KV cache is a "necessary evil":** dropping it pushes attention back to O(n²) recompute. It trades quadratic compute for linear memory, so the real question is how small it can get without losing what attention needs.
- **Naive INT4/INT8 (weight-style) quantization corrupts the KV cache** because its distribution is non-uniform, dynamic, and shifts per input; fixed codebooks (INT4 uniform, NF4 Gaussian) are misaligned with the data geometry.
- **The right objective is rate-distortion**, preserving the attention score `qᵀk`, not minimizing `‖A − B‖²` blindly. Each bit is a dimension of information that should be spent on the highest-variance (principal) directions.
- **TurboQuant transforms then quantizes:** rotate data into a known Gaussian space, apply a precomputed Lloyd-Max codebook (optimal for that distribution), then handle the residual separately.
- **QJL (Quantized Johnson-Lindenstrauss)** uses a random projection plus 1-bit sign quantization; sign quantization still preserves enough information to recover inner products, and `(N−1)-bit + 1-bit QJL` beats `N-bit`.
- **Results:** theoretical distortion bounds hold empirically; perfect needle-in-a-haystack recall at ~4× compression; better recall and zero indexing time on nearest-neighbor search vs baselines.

## Why it matters

This is the second, deeper TurboQuant source in the vault. [[Prateek Singh - KV Cache and TurboQuant]] introduced TurboQuant as one of five KV-optimization families; this source supplies the mathematical core — the rotation + optimal-codebook + QJL-residual structure and the rate-distortion reframing. It materially deepens [[KV Cache]] and [[Model Quantization and Efficiency]], and pairs with [[Maarten Grootendorst - A Visual Guide to Quantization]] (which covers the well-understood weight-space side TurboQuant deliberately contrasts against).

## Tensions / open questions

- Vector quantization with rotation + codebooks adds runtime complexity; whether it becomes a standard serving-kernel feature or stays research-stage is unresolved (the same open question raised in [[KV Cache]]).
- The article's bit-allocation intuition (bits as principal-component dimensions) is idealized; real per-input rotations must be cheap enough to run online.
- Reported gains (4× compression, perfect recall) are from the source's cited experiments; independent long-context production validation is still open.

## Affected pages

- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[LLM Inference]]
- [[Siddhant Rai]]
- [[Vizuara]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/TurboQuant - Online Vector Quantization with Near-optimal Distortion Rate.md`
- Source URL: [https://vizuara.substack.com/p/turboquant-online-vector-quantization](https://vizuara.substack.com/p/turboquant-online-vector-quantization)

## Related pages

- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[Prateek Singh - KV Cache and TurboQuant]]
- [[Maarten Grootendorst - A Visual Guide to Quantization]]
- [[LLM Inference]]
- [[2026-06-19 Efficient Edge Reasoning and TurboQuant]]
- [[Siddhant Rai]]
- [[Vizuara]]
- [[AI Knowledge Base Overview]]
