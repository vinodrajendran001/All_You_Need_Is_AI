---
type: raw-source
source_id: src-2026-06-04-extreme-ratio-cot-compression
title: Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression
author: Yuntian Tang et al.
url: https://arxiv.org/abs/2602.08324
pdf_url: https://arxiv.org/pdf/2602.08324.pdf
doi: 10.48550/arXiv.2602.08324
arxiv_id: 2602.08324
published: 2026-02-09
updated: 2026-06-04
captured: 2026-06-04
pdf_file: 2026-06-04 Yuntian Tang et al - Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression.pdf
pdf_sha256: e980df2581ad4e427502828122e28126ff4f6f12e149cb2aa5f6f6c218280e1c
pdf_size_bytes: 896726
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - compression
---

> Canonical local PDF: [2026-06-04 Yuntian Tang et al - Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression.pdf](2026-06-04%20Yuntian%20Tang%20et%20al%20-%20Towards%20Efficient%20Large%20Language%20Reasoning%20Models%20via%20Extreme-Ratio%20Chain-of-Thought%20Compression.pdf)

# Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression

## Bibliographic snapshot

- **Authors:** Yuntian Tang, Bohan Jia, Wenxuan Huang, Lianyue Zhang, Jiao Xie, Wenxi Li, Wei Li, Jie Hu, Xinghao Chen, Rongrong Ji
- **arXiv:** [2602.08324](https://arxiv.org/abs/2602.08324)
- **DOI:** [10.48550/arXiv.2602.08324](https://doi.org/10.48550/arXiv.2602.08324)

## Abstract

Chain-of-Thought (CoT) reasoning successfully enhances the reasoning capabilities of Large Language Models (LLMs), yet it incurs substantial computational overhead for inference. Existing CoT compression methods often suffer from a critical loss of logical fidelity at high compression ratios, resulting in significant performance degradation. To achieve high-fidelity, fast reasoning, we propose a novel EXTreme-RAtio Chain-of-Thought Compression framework, termed Extra-CoT, which aggressively reduces the token budget while preserving answer accuracy. To generate reliable, high-fidelity supervision, we first train a dedicated semantically-preserved compressor on mathematical CoT data with fine-grained annotations. An LLM is then fine-tuned on these compressed pairs via a mixed-ratio supervised fine-tuning (SFT), teaching it to follow a spectrum of compression budgets and providing a stable initialization for reinforcement learning (RL). We further propose Constrained and Hierarchical Ratio Policy Optimization (CHRPO) to explicitly incentivize question-solving ability under lower budgets by a hierarchical reward. Experiments on three mathematical reasoning benchmarks show the superiority of Extra-CoT. For example, on MATH-500 using Qwen3-1.7B, Extra-CoT achieves over 73% token reduction with an accuracy improvement of 0.6%, significantly outperforming state-of-the-art methods.

## Capture notes

- Downloaded from arXiv into `knowledge-base/raw/sources/`.
- This markdown note preserves the bibliographic metadata, abstract, and canonical local PDF reference for future wiki updates.
