---
type: entity
created: 2026-09-11
updated: 2026-09-11
entity_kind: organization
tags:
  - entity
  - hardware
  - inference
  - analysis
source_ids:
  - src-2026-09-07-semianalysis-tpu-inferencex
status: active
---

# SemiAnalysis

## What it is

Semiconductor and AI infrastructure research firm, publishing supply-chain analysis, datacenter
economics, and — through its **InferenceX** benchmarking arm — third-party measurements of inference
hardware and serving stacks.

## Why it matters here

SemiAnalysis produced the vault's first hard data on a non-NVIDIA accelerator at inference: the first
third-party TPUv7 Ironwood results, and the material behind
[[Accelerator Software Externalization]].

Its methodological contribution is larger than any single number. The same hardware measures as **50–96%
better per dollar**, **8–25% better**, or **roughly 30% worse** depending on whether you normalise by
chip-hour, by interactivity target, by end-to-end response time, or against a disaggregated GB300 NVL72.
SemiAnalysis states the boundary of each comparison — "applies to this datapoint specifically, rather than
every latency target" — which makes the article a worked example of why a normalisation axis must travel
with a serving result. That caveat belongs with [[Serving Benchmarks and Goodput]].

The second contribution is the tile-geometry finding: with the TPU matrix unit at 256×256 from v6e, a
head dimension of 128 caps attention matmuls at 50% utilisation and a head dimension of 64 at 25%. That is
hardware constraining model architecture, and it is why bring-up cost correlates poorly with model
popularity.

## Notes

- Bring-up model for the Ironwood preview was Qwen3.5 397B in FP8, on the InferenceX Official Preview.
- Documents Google's software transition from PyTorch/XLA lazy tensors through TorchAX to **TorchTPU**, a
  native PyTorch `PrivateUse1` device, with XLA remaining the compiler throughout.
- Reports Anthropic's commitment to over one million TPUs (~400k direct, ~600k rented via GCP).
- Notes Google splitting training and inference architectures for the first time (TPUv8t vs TPUv8i), with
  TPUv8i's 384 MB of on-chip SRAM sized to hold agentic KV cache — the first instance in this vault of an
  agent workload driving a hardware design decision.
- Results come from an Official Preview in which Google was presumably involved in tuning; the NVIDIA
  configurations may not have received equivalent attention.

## Related pages

- [[Accelerator Software Externalization]]
- [[AI Accelerator Architecture]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Serving Engines]]
- [[Prefill-Decode Disaggregation]]
- [[NVIDIA]]
- [[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]]
