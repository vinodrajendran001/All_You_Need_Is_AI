---
type: source-summary
created: 2026-06-29
updated: 2026-06-29
source_id: src-2026-06-29-maarten-grootendorst-visual-guide-quantization
source_title: A Visual Guide to Quantization
source_author: Maarten Grootendorst
source_url: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization
tags:
  - source-summary
  - quantization
  - llm
  - inference
  - efficiency
source_ids:
  - src-2026-06-29-maarten-grootendorst-visual-guide-quantization
status: active
---

# Maarten Grootendorst - A Visual Guide to Quantization

## Summary

This is a diagram-first, end-to-end tutorial on quantizing Large Language Models, built around 50+ custom visuals. It starts from why quantization is needed (a 70B model in FP32 needs ~280GB just to load), explains how floating-point numbers are represented (sign/exponent/mantissa, dynamic range vs precision), and then walks the full quantization stack: data types (FP16, BF16, INT8), symmetric vs asymmetric mapping, range/clipping/calibration, post-training quantization (dynamic vs static), the 4-bit era (GPTQ, GGUF), quantization-aware training, and the 1-bit/1.58-bit frontier (BitNet).

It is the canonical beginner-to-intermediate reference for the mechanics this vault already tracks under [[Model Quantization and Efficiency]]. Where other vault sources frame quantization as one lever among many (KV cache, LoRA, MoE), this source goes deep on the numerical machinery itself: how the affine map from floats to integers actually works and why each design choice trades accuracy for size.

## Key claims

- **Quantization reduces the bit-width of weights and activations** (e.g., FP32 → INT8) to cut memory and bandwidth, at some cost to accuracy.
- **Floating point splits bits into sign, exponent (dynamic range), and mantissa/fraction (precision).** BF16 keeps FP32's exponent range with fewer mantissa bits; FP16 has a narrower range but more precision per value.
- **Symmetric quantization** maps a zero-centered range `[-α, α]` with zero-point 0 (e.g., absmax INT8). **Asymmetric quantization** maps an arbitrary `[β, α]` with a non-zero zero-point. The affine map is `x_q = round(x/scale + zero_point)`.
- **Calibration** is the process of choosing the clipping range. Weights/biases are static and can be calibrated offline; activations vary per input and are harder.
- **Post-training quantization (PTQ)** quantizes an already-trained model. **Dynamic** PTQ computes activation ranges at runtime per input; **static** PTQ pre-computes them with a calibration dataset.
- **GPTQ** is a layer-wise 4-bit weight-only method using approximate second-order (Hessian) information to decide how to round, processing weights column-by-column and compensating remaining weights — GPU-oriented.
- **GGUF** is a CPU/Apple-Silicon-oriented format that splits weights into super-blocks and sub-blocks with their own scales, enabling flexible CPU/GPU offload.
- **Quantization-aware training (QAT)** simulates quantization during training so the model learns weights robust to low precision; it generally beats PTQ at very low bit-widths but costs a training run.
- **BitNet** pushes to 1-bit weights (and 1.58-bit, ternary {-1, 0, +1}) by training from scratch with quantization in the loop; the "0" state adds the ability to ignore a feature, recovering much of the quality.

## Why it matters

This source is the most thorough standalone explanation of quantization mechanics in the vault. It materially deepens [[Model Quantization and Efficiency]] (the affine map, symmetric vs asymmetric, PTQ vs QAT, GPTQ vs GGUF) and complements the runtime/cache-centric treatment in [[KV Cache]] and the new [[LLM Inference]] page. It also grounds the weight-space side of [[Siddhant Rai - TurboQuant - Online Vector Quantization]], which explicitly contrasts well-understood weight quantization against the harder online KV-cache case.

## Tensions / open questions

- The article is pedagogical and 2024-vintage; it predates some of the newest 4-bit hardware formats (NVFP4) and KV-cache-specific methods covered in other vault sources.
- It treats weight quantization as the main target; activation and KV-cache quantization (the dynamic, online problems) are acknowledged as harder but not solved here.
- BitNet's 1.58-bit results are framed optimistically; durable production evidence at scale remains an open question.

## Affected pages

- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Small Language Models]]
- [[Maarten Grootendorst]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/A Visual Guide to Quantization.md`
- Source URL: [https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-quantization)

## Related pages

- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Siddhant Rai - TurboQuant - Online Vector Quantization]]
- [[Nithin - What Actually Happens During LLM Inference]]
- [[Small Language Models]]
- [[Maarten Grootendorst]]
- [[AI Knowledge Base Overview]]
