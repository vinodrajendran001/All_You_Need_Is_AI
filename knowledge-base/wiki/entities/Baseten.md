---
type: entity
entity_kind: organization
created: 2026-09-03
updated: 2026-10-23
tags: [entity, inference, serving, kernels, vendor]
source_ids:
  - src-2026-09-02-baseten-efficient-frontier-inference
  - src-2026-08-29-baseten-agentic-kernels-production
  - src-2026-10-21-baselabs-mammoth-elephant
status: active
---

# Baseten

A model inference and serving company that publishes unusually detailed engineering writing about the
production side of running large models.

## Why it matters to this vault

Baseten's initial two sources cover both the **theory** and the **practice** of inference
optimization; Base Labs' decision-model report adds post-training and data engineering.

[[Philip Kiely - The Efficient Frontier of LLM Inference]] supplies the taxonomy: every optimization either
moves a deployment **along** the latency-throughput frontier or **pushes the frontier out**. That distinction
became [[Inference Efficiency Frontier]], which now acts as a classifier over techniques the vault previously
documented only individually. Its most useful operational claim is that the frontier is **jagged** — cutoff
points are unintuitive and must be found by empirical sweeps.

[[Baseten - Agentic Kernels in Production]] is the worked example, and the vault's first end-to-end production
account of AI-generated kernels: an agentic framework that profiles a live workload, proposes optimizations,
generates kernels and ships them, reporting **42.3% latency reduction on Qwen-Image**, **15.2% on FLUX.2**,
and **5.5% more tok/s on MiniMax M3**. Two findings there carry beyond Baseten — the four specific reasons
**kernel benchmark wins do not transfer to production**, which sharpens [[AI-Generated Kernels]]; and the
**maturity-headroom relationship**, where the same framework yields 42.3% on diffusion but only 5.5% on LLMs
because LLM kernels are already heavily optimized.

Its optimization loop also keeps a knowledge base recording **both successes and failures with root causes**,
which makes it a concrete instance of the scaffold-memory pattern on [[Recursive Self-Improvement]].

## Caveats

Baseten sells inference. Both sources are vendor publications: the frontier post links its own EAGLE-3 and
DFlash work throughout and closes by promoting the author's book, and every kernel measurement is Baseten's
own, on Baseten's stack, against a prior baseline that is never characterised. The taxonomy stands
independently of the commercial interest; the performance claims should be read as self-reported.

## Base Labs adds fixed-option models and an auditable recipe

[[Base Labs - Mammoth-1 and Elephant-1 Decision Models]] describes Qwen3.5-derived **9B
Elephant** and **27B Mammoth**, trained on **6.21M** examples with modified full-attention
masks and a combined cross-entropy/Brier loss. The source's strongest reusable contribution
is its source-labeling, shortcut-review, pilot-training, and repair loop, not the release-day
"best model" claim.

Reported private Jev v0.4 scores are **62.65** and **71.24**, respectively. Public-mixture
scores and the authors' Artificial Analysis replica use different protocols; the reported
official Elephant score of **65** is not its replica score of **65.2**. The models retain
a frozen vision encoder but train on text alone. These are first-party training and
benchmark claims, not a demonstration of local probability calibration or serving economics.

## Related pages

- [[Base Labs - Mammoth-1 and Elephant-1 Decision Models]]
- [[Typed Probabilistic Decision Models]]
- [[Synthetic Data Flywheel]]

- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
- [[Baseten - Agentic Kernels in Production]]
- [[Philip Kiely]]
- [[Inference Efficiency Frontier]]
- [[AI-Generated Kernels]]
- [[GPU Kernel Optimization]]
- [[Speculative Decoding]]
- [[Prefill-Decode Disaggregation]]
- [[Inference Serving Engines]]
- [[LLM Inference]]
