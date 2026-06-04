---
type: raw-source
source_id: src-2026-06-04-efficient-reasoning-edge
title: Efficient Reasoning on the Edge
author: Yelysei Bondarenko et al.
url: https://arxiv.org/abs/2603.16867
pdf_url: https://arxiv.org/pdf/2603.16867.pdf
doi: 10.48550/arXiv.2603.16867
arxiv_id: 2603.16867
arxiv_version: v2
published: 2026-03-17
updated: 2026-06-03
captured: 2026-06-04
project_page: https://qualcomm-ai-research.github.io/llm-reasoning-on-edge/
pdf_file: 2026-06-04 Yelysei Bondarenko et al - Efficient Reasoning on the Edge.pdf
pdf_sha256: a80a4972ae314ec7a6d1467b49d0df204aa3fd444e18ee1dfd5535c2ee862fcc
pdf_size_bytes: 861107
status: immutable
tags:
  - source/raw
  - paper
  - reasoning
  - edge-ai
  - quantization
---

> Canonical local PDF: [2026-06-04 Yelysei Bondarenko et al - Efficient Reasoning on the Edge.pdf](2026-06-04%20Yelysei%20Bondarenko%20et%20al%20-%20Efficient%20Reasoning%20on%20the%20Edge.pdf)

# Efficient Reasoning on the Edge

## Bibliographic snapshot

- **Authors:** Yelysei Bondarenko, Thomas Hehn, Rob Hesselink, Romain Lepert, Fabio Valerio Massoli, Evgeny Mironov, Leyla Mirvakhabova, Tribhuvanesh Orekondy, Spyridon Stasis, Andrey Kuzmin, Anna Kuzina, Markus Nagel, Ankita Nayak, Corrado Rainone, Ork de Rooij, Paul N Whatmough, Arash Behboodi, Babak Ehteshami Bejnordi
- **arXiv:** [2603.16867](https://arxiv.org/abs/2603.16867)
- **DOI:** [10.48550/arXiv.2603.16867](https://doi.org/10.48550/arXiv.2603.16867)
- **Project page:** [Qualcomm AI Research - LLM Reasoning on Edge](https://qualcomm-ai-research.github.io/llm-reasoning-on-edge/)
- **Latest version visible at ingest:** v2
- **Subjects:** Machine Learning (cs.LG), Computation and Language (cs.CL)

## Abstract

Large language models (LLMs) with chain-of-thought reasoning achieve state-of-the-art performance across complex problem-solving tasks, but their verbose reasoning traces and large context requirements make them impractical for edge deployment. These challenges include high token generation costs, large KV-cache footprints, and inefficiencies when distilling reasoning capabilities into smaller models for mobile devices. Existing approaches often rely on distilling reasoning traces from larger models into smaller models, which are verbose and stylistically redundant, undesirable for on-device inference. In this work, we propose a lightweight approach to enable reasoning in small LLMs using LoRA adapters combined with supervised fine-tuning. We further introduce budget forcing via reinforcement learning on these adapters, significantly reducing response length with minimal accuracy loss. To address memory-bound decoding, we exploit parallel test-time scaling, improving accuracy at minor latency increase. Finally, we present a dynamic adapter-switching mechanism that activates reasoning only when needed and a KV-cache sharing strategy during prompt encoding, reducing time-to-first-token for on-device inference. Experiments on Qwen2.5-7B demonstrate that our method achieves efficient, accurate reasoning under strict resource constraints, making LLM reasoning practical for mobile scenarios.

## Capture notes

- Copied from the user-provided local PDF at `/mnt/c/Users/uie49878/Downloads/efficient_reasoning_on_edge.pdf` into `knowledge-base/raw/sources/`.
- This markdown note preserves the arXiv metadata, abstract, project page, and canonical local PDF reference for future wiki updates.
