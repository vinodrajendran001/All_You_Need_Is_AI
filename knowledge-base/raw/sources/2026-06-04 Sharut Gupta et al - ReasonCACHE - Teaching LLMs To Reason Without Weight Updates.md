---
type: raw-source
source_id: src-2026-06-04-reasoncache
title: "ReasonCACHE: Teaching LLMs To Reason Without Weight Updates"
author: Sharut Gupta et al.
url: https://arxiv.org/abs/2602.02366
pdf_url: https://arxiv.org/pdf/2602.02366.pdf
doi: 10.48550/arXiv.2602.02366
arxiv_id: 2602.02366
published: 2026-02-02
updated: 2026-06-04
captured: 2026-06-04
pdf_file: 2026-06-04 Sharut Gupta et al - ReasonCACHE - Teaching LLMs To Reason Without Weight Updates.pdf
pdf_sha256: 4ce5159fa93dcd6099df119e628ae00255c66b4704b68b9f7ac6de549e287c35
pdf_size_bytes: 2654524
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - icl
---

> Canonical local PDF: [2026-06-04 Sharut Gupta et al - ReasonCACHE - Teaching LLMs To Reason Without Weight Updates.pdf](2026-06-04%20Sharut%20Gupta%20et%20al%20-%20ReasonCACHE%20-%20Teaching%20LLMs%20To%20Reason%20Without%20Weight%20Updates.pdf)

# ReasonCACHE: Teaching LLMs To Reason Without Weight Updates

## Bibliographic snapshot

- **Authors:** Sharut Gupta, Phillip Isola, Stefanie Jegelka, David Lopez-Paz, Kartik Ahuja, Mark Ibrahim, Mohammad Pezeshki
- **arXiv:** [2602.02366](https://arxiv.org/abs/2602.02366)
- **DOI:** [10.48550/arXiv.2602.02366](https://doi.org/10.48550/arXiv.2602.02366)

## Abstract

Can Large language models (LLMs) learn to reason without any weight update and only through in-context learning (ICL)? ICL is strikingly sample-efficient, often learning from only a handful of demonstrations, but complex reasoning tasks typically demand many training examples to learn from. However, naively scaling ICL by adding more demonstrations breaks down at this scale: attention costs grow quadratically, performance saturates or degrades with longer contexts, and the approach remains a shallow form of learning. Due to these limitations, practitioners predominantly rely on in-weight learning (IWL) to induce reasoning. In this work, we show that by using Prefix Tuning, LLMs can learn to reason without overloading the context window and without any weight updates. We introduce ReasonCACHE, an instantiation of this mechanism that distills demonstrations into a fixed key-value cache. Empirically, across challenging reasoning benchmarks, including GPQA-Diamond, ReasonCACHE outperforms standard ICL and matches or surpasses IWL approaches. Further, it achieves this all while being more efficient across three key axes: data, inference cost, and trainable parameters. We also theoretically prove that ReasonCACHE can be strictly more expressive than low-rank weight update since the latter ties expressivity to input rank, whereas ReasonCACHE bypasses this constraint by directly injecting key-values into the attention mechanism. Together, our findings identify ReasonCACHE as a middle path between in-context and in-weight learning, providing a scalable algorithm for learning reasoning skills beyond the context window without modifying parameters. Project page: https://reasoncache.github.io/

## Capture notes

- Downloaded from arXiv into `knowledge-base/raw/sources/`.
- This markdown note preserves the bibliographic metadata, abstract, and canonical local PDF reference for future wiki updates.
