---
type: raw-source
source_id: src-2026-06-04-conpress
title: "ConPress: Learning Efficient Reasoning from Multi-Question Contextual Pressure"
author: Jie Deng et al.
url: https://arxiv.org/abs/2602.01472
pdf_url: https://arxiv.org/pdf/2602.01472.pdf
doi: 10.48550/arXiv.2602.01472
arxiv_id: 2602.01472
published: 2026-02-01
updated: 2026-06-04
captured: 2026-06-04
pdf_file: 2026-06-04 Jie Deng et al - ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure.pdf
pdf_sha256: 3fd11db20c296f3a89f8285e045fee08c6849323396ea9c7ba2a4fdeb31c4da7
pdf_size_bytes: 827251
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - self-supervision
---

> Canonical local PDF: [2026-06-04 Jie Deng et al - ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure.pdf](2026-06-04%20Jie%20Deng%20et%20al%20-%20ConPress%20-%20Learning%20Efficient%20Reasoning%20from%20Multi-Question%20Contextual%20Pressure.pdf)

# ConPress: Learning Efficient Reasoning from Multi-Question Contextual Pressure

## Bibliographic snapshot

- **Authors:** Jie Deng, Shining Liang, Jun Li, Hongzhi Li, Yutao Xie
- **arXiv:** [2602.01472](https://arxiv.org/abs/2602.01472)
- **DOI:** [10.48550/arXiv.2602.01472](https://doi.org/10.48550/arXiv.2602.01472)

## Abstract

Large reasoning models (LRMs) typically solve reasoning-intensive tasks by generating long chain-of-thought (CoT) traces, leading to substantial inference overhead. We identify a reproducible inference-time phenomenon, termed Self-Compression: when multiple independent and answerable questions are presented within a single prompt, the model spontaneously produces shorter reasoning traces for each question. This phenomenon arises from multi-question contextual pressure during generation and consistently manifests across models and benchmarks. Building on this observation, we propose ConPress (Learning from Contextual Pressure), a lightweight self-supervised fine-tuning approach. ConPress constructs multi-question prompts to induce self-compression, samples the resulting model outputs, and parses and filters per-question traces to obtain concise yet correct reasoning trajectories. These trajectories are directly used for supervised fine-tuning, internalizing compressed reasoning behavior in single-question settings without external teachers, manual pruning, or reinforcement learning. With only 8k fine-tuning examples, ConPress reduces reasoning token usage by 59% on MATH500 and 33% on AIME25, while maintaining competitive accuracy.

## Capture notes

- Downloaded from arXiv into `knowledge-base/raw/sources/`.
- This markdown note preserves the bibliographic metadata, abstract, and canonical local PDF reference for future wiki updates.
