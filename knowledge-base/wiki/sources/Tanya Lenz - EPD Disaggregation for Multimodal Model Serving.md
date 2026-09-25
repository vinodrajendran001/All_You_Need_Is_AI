---
type: source-summary
created: 2026-09-25
updated: 2026-09-25
source_id: src-2026-09-10-lenz-epd-multimodal-serving
source_title: "When to Use Encode-Prefill-Decode Disaggregation to Accelerate Multimodal Model Serving"
source_author: Tanya Lenz
source_url: https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/
tags: [source/summary, inference, multimodal, serving]
source_ids: [src-2026-09-10-lenz-epd-multimodal-serving]
status: active
---

# Tanya Lenz - EPD Disaggregation for Multimodal Model Serving

## Summary

This NVIDIA study extends prefill-decode disaggregation with a separate multimodal encoder tier.
Encode-prefill-decode disaggregation helps when vision encoding is a meaningful bottleneck and loses
value when decode or transfer overhead dominates.

## Key claims

- The test used Qwen3.5 122B-A10B NVFP4, four GB200 GPUs for prefill/decode, RTX 6000D encoder GPUs,
  a 20 Gbps network, and an **ITL below 100 ms** goodput SLO.
- At 10 images, 256 tokens/image, and output length 1,024, TTFT fell **58%** with colocated EPD and
  **50%** with heterogeneous EPD; the latter served **70% more traffic** at the same SLO.
- Across image-heavy cells TTFT improved **25-93%**, but colocated E2E gain changed from **+11.8% to
  -2.5%** as output length rose from 128 to 2,048.
- Relative colocated goodput was **2.62x / 1.50x / 0.65x** for 4B / 9B / 27B models. Quantization
  shifted the bottleneck toward the still-BF16 vision encoder.

## Why it matters

Disaggregation is a bottleneck-placement decision, not a universal scale-out rule. Model size,
precision, image load, output length, network, and SLO jointly determine the useful topology.

## Tensions and caveats

This is an NVIDIA-authored Dynamo benchmark on NVIDIA hardware. The 5x TTFT and 7x E2E headlines are
upper-bound vendor claims; detailed results are narrower. Transfer and coordination can erase gains,
and homogeneous disaggregated placement reportedly underperformed without a full analysis.

## Raw capture

- [[2026-09-10 Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]]

## Affected pages

- [[Prefill-Decode Disaggregation]]
- [[Inference Serving Engines]]
- [[LLM Inference]]
- [[Serving Benchmarks and Goodput]]
- [[Model Quantization and Efficiency]]
- [[NVIDIA]]

## Related pages

- [[Mixture of Experts]]
- [[Vision-Language Grounding]]
- [[KV Cache]]
