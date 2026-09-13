---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-rahman-quantizing-llms-gke
source_title: "Quantizing LLMs on GKE for Faster and Cheaper Inference"
source_author: Mofi Rahman
source_url: https://medium.com/google-cloud/quantizing-llms-on-gke-for-faster-and-cheaper-inference-59bfc6b15e43
tags:
  - source/summary
  - quantization
  - inference
  - google-cloud
source_ids:
  - src-2026-09-13-rahman-quantizing-llms-gke
status: active
---

# Mofi Rahman - Quantizing LLMs on GKE

## Summary

A practical GKE quantization tutorial built around a useful capacity calculation: precision determines whether a 27B model needs a multi-GPU deployment or can fit its weights on one L4. The source also distinguishes post-training quantization from quantization-aware training and gives a deployable GPTQ workflow.

## Key claims

- Gemma 3 27B at BF16 uses **27 billion x 2 bytes = at least 54 GB** for weights.
- An NVIDIA L4 has **24 GB VRAM**. Three devices satisfy raw capacity, but the source says attention-head and framework divisibility can require **4 GPUs**.
- At 4 bits, weights occupy roughly **13.5 GB**, fitting the weight tensor on one L4 before KV cache, activations, workspaces, and runtime overhead.
- Lower weight and KV-cache precision can increase concurrency and reduce memory-bandwidth traffic, but acceleration depends on compatible kernels.
- PTQ is cheaper and faster to apply; representative calibration is still needed, and degradation is more likely **below 4 bits**.
- QAT inserts fake quantization during training so the high-precision weights adapt to rounding and clipping.
- The source reports quality losses spanning **1% to 30+%** and says QAT can approach original quality. The range is not tied to named models, tasks, or metrics.
- The worked path uses vLLM `llmcompressor`, GPTQ, a GPU-enabled GKE cluster, Artifact Registry, Cloud Build, a Kubernetes Job, and a Hugging Face secret.
- The source recommends evaluating existing community checkpoints before quantizing from scratch.

## Why it matters

The arithmetic cleanly separates **weight fit** from **runtime fit**. Saying a 13.5 GB weight tensor fits on a 24 GB GPU is not saying the served model fits under a useful context and concurrency target. That qualifier is central to honest quantization sizing.

## Tensions / open questions

- The 54 GB and 13.5 GB figures exclude cache, activations, CUDA workspace, and framework overhead.
- The broad quality-loss range is not reproducible without named benchmarks and calibration data.
- Lower precision is not automatically faster if kernels dequantize or lack native support.
- Community checkpoints add provenance, licensing, compatibility, and evaluation risk.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Model Quantization and Efficiency]]
- [[Inference Efficiency Frontier]]
- [[KV Cache]]
- [[Google Cloud]]

## Citations

- Mofi Rahman, "Quantizing LLMs on GKE for Faster and Cheaper Inference", 2025-11-06.

## Raw capture

- [[2026-09-13 Mofi Rahman - Quantizing LLMs on GKE]]

## Related pages

- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[On-Device Reasoning]]

