---
type: raw-source
source_id: src-2026-06-04-dss-grpo-cot-compression
title: "Shorter Thoughts, Same Answers: Difficulty-Scaled Segment-Wise RL for CoT Compression"
author: Ye Tian and Aijun Liu
url: https://arxiv.org/abs/2603.07598
pdf_url: https://arxiv.org/pdf/2603.07598.pdf
doi: 10.48550/arXiv.2603.07598
arxiv_id: 2603.07598
published: 2026-03-08
updated: 2026-06-04
captured: 2026-06-04
pdf_file: 2026-06-04 Ye Tian et al - Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression.pdf
pdf_sha256: eb6c603e31852aa48aab4a7070e7d53baf5b711d54a1e6c08d8f8eccd1ca0bf9
pdf_size_bytes: 447253
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - rl
---

> Canonical local PDF: [2026-06-04 Ye Tian et al - Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression.pdf](2026-06-04%20Ye%20Tian%20et%20al%20-%20Shorter%20Thoughts,%20Same%20Answers%20-%20Difficulty-Scaled%20Segment-Wise%20RL%20for%20CoT%20Compression.pdf)

# Shorter Thoughts, Same Answers: Difficulty-Scaled Segment-Wise RL for CoT Compression

## Bibliographic snapshot

- **Authors:** Ye Tian, Aijun Liu
- **arXiv:** [2603.07598](https://arxiv.org/abs/2603.07598)
- **DOI:** [10.48550/arXiv.2603.07598](https://doi.org/10.48550/arXiv.2603.07598)

## Abstract

Chain-of-thought (CoT) improves reasoning reliability but increases token cost, motivating post-training compression of explicit reasoning traces. However, the shortest sufficient reasoning is not universal: it depends on difficulty, model capacity, and training state, making fixed length targets brittle. In practice, naive RL-based compression can also undesirably shorten the user-facing answer, because a single completion-level learning signal leaks across the think/answer boundary. We propose Difficulty-Scaled Segment-Wise GRPO (DSS-GRPO), which decomposes returns into think and answer components, computes group-relative advantages per segment, and routes them with hard token masks so compression updates act only on think while answer alignment acts only on answer. DSS-GRPO uses prompt-wise within-group shaping and difficulty-aware scaling to encourage concise reasoning without collapsing answer behavior.

## Capture notes

- Downloaded from arXiv into `knowledge-base/raw/sources/`.
- This markdown note preserves the bibliographic metadata, abstract, and canonical local PDF reference for future wiki updates.
