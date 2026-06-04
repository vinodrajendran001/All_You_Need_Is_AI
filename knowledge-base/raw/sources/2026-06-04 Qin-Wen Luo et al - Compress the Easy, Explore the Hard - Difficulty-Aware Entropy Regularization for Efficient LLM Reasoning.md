---
type: raw-source
source_id: src-2026-06-04-difficulty-aware-entropy-regularization
title: "Compress the Easy, Explore the Hard: Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning"
author: Qin-Wen Luo et al.
url: https://arxiv.org/abs/2602.22642
pdf_url: https://arxiv.org/pdf/2602.22642.pdf
doi: 10.48550/arXiv.2602.22642
arxiv_id: 2602.22642
published: 2026-02-26
updated: 2026-06-04
captured: 2026-06-04
pdf_file: 2026-06-04 Qin-Wen Luo et al - Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning.pdf
pdf_sha256: 7d33f244226ebfb4a4eb3f773f003baa442d18f5cf3fadbff504bd531d777e0d
pdf_size_bytes: 2856863
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - rl
---

> Canonical local PDF: [2026-06-04 Qin-Wen Luo et al - Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning.pdf](2026-06-04%20Qin-Wen%20Luo%20et%20al%20-%20Compress%20the%20Easy,%20Explore%20the%20Hard%20-%20Difficulty-Aware%20Entropy%20Regularization%20for%20Efficient%20LLM%20Reasoning.pdf)

# Compress the Easy, Explore the Hard: Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning

## Bibliographic snapshot

- **Authors:** Qin-Wen Luo, Sheng Ren, Xiang Chen, Rui Liu, Jun Fang, Naiqiang Tan, Sheng-Jun Huang
- **arXiv:** [2602.22642](https://arxiv.org/abs/2602.22642)
- **DOI:** [10.48550/arXiv.2602.22642](https://doi.org/10.48550/arXiv.2602.22642)

## Abstract

Chain-of-Thought (CoT) has substantially empowered Large Language Models (LLMs) to tackle complex reasoning tasks, yet the verbose nature of explicit reasoning steps incurs prohibitive inference latency and computational costs, limiting real-world deployment. While existing compression methods - ranging from self-training to Reinforcement Learning (RL) with length constraints - attempt to mitigate this, they often sacrifice reasoning capability for brevity. We identify a critical failure mode in these approaches: explicitly optimizing for shorter trajectories triggers rapid entropy collapse, which prematurely shrinks the exploration space and stifles the discovery of valid reasoning paths, particularly for challenging questions requiring extensive deduction. To address this issue, we propose Compress responses for Easy questions and Explore Hard ones (CEEH), a difficulty-aware approach to RL-based efficient reasoning. CEEH dynamically assesses instance difficulty to apply selective entropy regularization: it preserves a diverse search space for currently hard questions to ensure robustness, while permitting aggressive compression on easier instances where the reasoning path is well-established. In addition, we introduce a dynamic optimal-length penalty anchored to the historically shortest correct response, which effectively counteracts entropy-induced length inflation and stabilizes the reward signal. Across six reasoning benchmarks, CEEH consistently reduces response length while maintaining accuracy comparable to the base model, and improves Pass@k relative to length-only optimization.

## Capture notes

- Downloaded from arXiv into `knowledge-base/raw/sources/`.
- This markdown note preserves the bibliographic metadata, abstract, and canonical local PDF reference for future wiki updates.
