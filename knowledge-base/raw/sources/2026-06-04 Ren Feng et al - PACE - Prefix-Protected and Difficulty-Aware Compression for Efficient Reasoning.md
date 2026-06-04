---
type: raw-source
source_id: src-2026-06-04-pace-efficient-reasoning
title: "PACE: Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning"
author: Ren Feng et al.
url: https://arxiv.org/abs/2602.11639
pdf_url: https://arxiv.org/pdf/2602.11639.pdf
doi: 10.48550/arXiv.2602.11639
arxiv_id: 2602.11639
published: 2026-02-12
updated: 2026-06-04
captured: 2026-06-04
pdf_file: 2026-06-04 Ren Feng et al - PACE - Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning.pdf
pdf_sha256: 29a44f4c2a358c9c27f533b54d3ba4b2f56f183dddce2f67ed0a443905cced72
pdf_size_bytes: 3891115
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - compression
---

> Canonical local PDF: [2026-06-04 Ren Feng et al - PACE - Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning.pdf](2026-06-04%20Ren%20Feng%20et%20al%20-%20PACE%20-%20Prefix-Protected%20and%20Difficulty-Aware%20Compression%20for%20Efficient%20Reasoning.pdf)

# PACE: Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning

## Bibliographic snapshot

- **Authors:** Ren Feng, Yuntao Wen, Silin Zhou, Ke Shi, Yifan Wang, Ran Le, Zhenwei An, Zongchao Chen, Chen Yang, Guangyue Peng, Yiming Jia, Dongsheng Wang, Tao Zhang, Lisi Chen, Yang Song, Shen Gao, Shuo Shang
- **arXiv:** [2602.11639](https://arxiv.org/abs/2602.11639)
- **DOI:** [10.48550/arXiv.2602.11639](https://doi.org/10.48550/arXiv.2602.11639)

## Abstract

Language Reasoning Models (LRMs) achieve strong performance by scaling test-time computation but often suffer from ``overthinking'', producing excessively long reasoning traces that increase latency and memory usage. Existing LRMs typically enforce conciseness with uniform length penalties, which over-compress crucial early deduction steps at the sequence level and indiscriminately penalize all queries at the group level. To solve these limitations, we propose PACE, a dual-level framework for prefix-protected and difficulty-aware compression under hierarchical supervision. At the sequence level, prefix-protected optimization employs decaying mixed rollouts to maintain valid reasoning paths while promoting conciseness. At the group level, difficulty-aware penalty dynamically scales length constraints based on query complexity, maintaining exploration for harder questions while curbing redundancy on easier ones. Extensive experiments on DeepSeek-R1-Distill-Qwen (1.5B/7B) demonstrate that PACE achieves a substantial reduction in token usage (up to 55.7%) while simultaneously improving accuracy (up to 4.1%) on math benchmarks, with generalization ability to code, science, and general domains.

## Capture notes

- Downloaded from arXiv into `knowledge-base/raw/sources/`.
- This markdown note preserves the bibliographic metadata, abstract, and canonical local PDF reference for future wiki updates.
