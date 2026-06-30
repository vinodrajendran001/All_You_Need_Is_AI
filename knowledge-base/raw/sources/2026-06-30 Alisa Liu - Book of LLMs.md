---
type: raw-source
source_id: src-2026-06-30-alisa-liu-book-of-llms
title: "Alisa's book of LLMs"
author: Alisa Liu (alisawuffles)
url: https://alisawuffles.notion.site/alisa-s-book-of-llms
captured: 2026-06-30
status: immutable
tags:
  - source/raw
  - llm
  - study-reference
  - interview-prep
---

> Preserve the source body below this line as the canonical capture.
> **Capture note:** This is a living Notion page (a JS-rendered single-page app). The raw HTML contains no content, so it was captured via a JS-rendering reader proxy on 2026-06-30. The full prose was retrieved, but inline LaTeX was flattened by the proxy and is not reproduced verbatim here. What follows is (1) the complete, faithful **table of contents** and (2) a structured synopsis of each section's coverage. The author's companion to the job-search post; described there as "my LLM notes, which I worked on continuously throughout the [job search] process."

# Alisa's book of LLMs

A comprehensive personal study reference for LLM technical interviews, organized as one coherent map of the field. Built alongside Stanford CS336 (Language Modeling from Scratch).

## Full table of contents (verbatim)

- **Neural net basics** — Multi-layer perceptrons; Activation functions; Gradients; Backpropagation; Optimizers; Learning rate
- **Mathy things** — Information theory; Numerical stability and other tricks; Basic statistics; Gradient flow through sampling; Theoretical CS
- **The modern transformer LM**
  - Architecture; Implementation notes
  - **Accounting** — Model parameters; Model activations; FLOPs in forward pass; FLOPs in backward pass; Inference memory use; Train memory use
  - Attention; RMSNorm; SwiGLU FFN; RoPE
- **Inference** — Batching & packing; Speculative decoding; KV cache; Reducing KV cache size; Sampling strategies; Flash Attention
- **Scaling laws**
- **GPUs**
- **Other architectures** — RNNs (Vanilla RNN; LSTM; vs. transformers); State space models
- **Post-training** — policy gradients; PPO; RLHF; GRPO; DPO
- **Precision**
- **Parallelism** — Background: core collective operations; Data parallelism; Pipeline parallelism; Tensor parallelism
- **Multimodality**

## Section synopsis (what each part covers)

- **Neural net basics.** MLP as fully-connected network (input, ≥1 hidden, output layers); a neuron computes `y = f(wᵀx + b)`; a layer as matrix multiply `h = f(Wx + b)`. Non-linearities are essential — without them, stacked layers collapse to a single linear transform `W₁W₂x = Wx`; with non-linearities, deeper nets approximate arbitrary functions. Covers activation functions, gradients, backpropagation, optimizers, and learning-rate schedules.
- **Mathy things.** Information theory (entropy, cross-entropy, KL), numerical-stability tricks (e.g., log-sum-exp, stable softmax), basic statistics, gradient flow through sampling (reparameterization / straight-through), and a touch of theoretical CS.
- **The modern transformer LM.** The decoder-only architecture and concrete implementation notes, plus a detailed **accounting** block: how to count model parameters, activation memory, and FLOPs in the forward and backward passes, and how to estimate inference- vs train-time memory. Deep dives on Attention, RMSNorm, the SwiGLU feed-forward block (`SwiGLU(x) = (xW₁) ⊙ Swish(xW₂)`), and RoPE.
- **Inference.** Batching & packing; speculative decoding (a small draft model proposes tokens a big model verifies); KV cache and techniques for reducing its size; sampling strategies; Flash Attention (IO-aware exact attention).
- **Scaling laws.** Compute-optimal model/data tradeoffs.
- **GPUs.** Hardware view relevant to throughput and memory.
- **Other architectures.** RNNs (vanilla, LSTM) and how they compare to transformers; state space models.
- **Post-training.** Policy gradients as the foundation, then PPO, RLHF, GRPO, and DPO.
- **Precision.** Numerical formats for training/inference.
- **Parallelism.** Core collective operations (all-reduce, etc.) and the data / pipeline / tensor parallelism dimensions.
- **Multimodality.** Extending LMs beyond text.

*(Representative excerpt of the prose style, from the SwiGLU section: "without non-linearities, neural nets can't do anything more than a linear transform; extra layers can be compiled down to a single linear transform `W₁W₂x = Wx`. With more layers that include non-linearities, they can approximate any complex function.")*
