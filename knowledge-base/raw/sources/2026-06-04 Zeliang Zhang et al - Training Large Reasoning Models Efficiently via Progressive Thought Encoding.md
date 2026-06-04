---
type: raw-source
source_id: src-2026-06-04-progressive-thought-encoding
title: Training Large Reasoning Models Efficiently via Progressive Thought Encoding
author: Zeliang Zhang et al.
url: https://arxiv.org/abs/2602.16839
pdf_url: https://arxiv.org/pdf/2602.16839.pdf
doi: 10.48550/arXiv.2602.16839
arxiv_id: 2602.16839
published: 2026-02-18
updated: 2026-06-04
captured: 2026-06-04
pdf_file: 2026-06-04 Zeliang Zhang et al - Training Large Reasoning Models Efficiently via Progressive Thought Encoding.pdf
pdf_sha256: d9989f668cf5a9927323952c30a444d51f36a197fad10a1f420870403caa799a
pdf_size_bytes: 801079
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - efficiency
---

> Canonical local PDF: [2026-06-04 Zeliang Zhang et al - Training Large Reasoning Models Efficiently via Progressive Thought Encoding.pdf](2026-06-04%20Zeliang%20Zhang%20et%20al%20-%20Training%20Large%20Reasoning%20Models%20Efficiently%20via%20Progressive%20Thought%20Encoding.pdf)

# Training Large Reasoning Models Efficiently via Progressive Thought Encoding

## Bibliographic snapshot

- **Authors:** Zeliang Zhang, Xiaodong Liu, Hao Cheng, Hao Sun, Chenliang Xu, Jianfeng Gao
- **arXiv:** [2602.16839](https://arxiv.org/abs/2602.16839)
- **DOI:** [10.48550/arXiv.2602.16839](https://doi.org/10.48550/arXiv.2602.16839)

## Abstract

Large reasoning models (LRMs) excel on complex problems but face a critical barrier to efficiency: reinforcement learning (RL) training requires long rollouts for outcome-based rewards, where autoregressive decoding dominates time and memory usage. While sliding-window cache strategies can bound memory, they disrupt long-context reasoning and degrade performance. We introduce Progressive Thought Encoding, a parameter-efficient fine-tuning method that enables LRMs to reason effectively under fixed-size caches. By progressively encoding intermediate reasoning into fixed-size vector representations, our approach eliminates the need to backpropagate through full-cache rollouts, thereby reducing memory usage, while maintaining constant memory during inference. Experiments on three models, including Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct, and DeepSeek-R1-Distill-Llama-8B, on six widely used challenging mathematical benchmarks show consistent gains: our method achieves +19.3% improvement over LoRA-based fine-tuning and +29.9% over LRMs without fine-tuning on average, with up to +23.4 accuracy improvement on AIME2024/2025 under the same tight cache budgets. These results demonstrate that Progressive Thought Encoding not only improves reasoning accuracy but also makes RL training of LRMs substantially more efficient and scalable under real-world memory constraints.

## Capture notes

- Downloaded from arXiv into `knowledge-base/raw/sources/`.
- This markdown note preserves the bibliographic metadata, abstract, and canonical local PDF reference for future wiki updates.
