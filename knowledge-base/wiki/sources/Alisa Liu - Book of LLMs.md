---
type: source-summary
created: 2026-06-30
updated: 2026-06-30
source_id: src-2026-06-30-alisa-liu-book-of-llms
source_title: Alisa's book of LLMs
source_author: Alisa Liu
source_url: https://alisawuffles.notion.site/alisa-s-book-of-llms
tags:
  - source-summary
  - llm
  - study-reference
  - interview-prep
status: active
source_ids:
  - src-2026-06-30-alisa-liu-book-of-llms
---

# Alisa Liu - Book of LLMs

## Summary

A comprehensive, continuously-maintained personal study reference for LLM technical interviews, built alongside Stanford CS336. It organizes the whole field into one coherent map: neural-net basics, the supporting math, the modern transformer (with an unusually thorough "accounting" block on parameters / activations / FLOPs / memory), inference optimizations, scaling laws, GPUs, non-transformer architectures, post-training/RL, precision, parallelism, and multimodality. It is the technical companion to [[Alisa Liu - The AI Research Job Search]].

For this vault its value is twofold: it is a **model of how to consolidate the field for interviews** (feeding [[ML Research Interview Preparation]]), and it **corroborates and cross-links many existing technical concept pages** with a single-author, exam-oriented framing.

*(Capture caveat: the source is a JS-rendered Notion page; it was retrieved via a rendering proxy, with the table of contents preserved faithfully and inline LaTeX flattened — see the raw capture.)*

## Key claims / coverage

- **Neural-net basics:** MLP as `h = f(Wx + b)`; non-linearities are what give depth its power (without them, `W₁W₂x = Wx` collapses to one linear map); gradients, backprop, optimizers, learning-rate schedules.
- **Supporting math:** information theory (entropy, cross-entropy, KL), numerical-stability tricks (stable softmax / log-sum-exp), basic statistics, gradient flow through sampling (reparameterization / straight-through).
- **Modern transformer:** architecture + implementation notes, then a detailed **accounting** of parameter counts, activation memory, forward/backward FLOPs, and inference- vs train-time memory; deep dives on Attention, **RMSNorm**, **SwiGLU FFN** (`(xW₁) ⊙ Swish(xW₂)`), and **RoPE**.
- **Inference:** batching & packing, **speculative decoding**, **KV cache** and techniques to reduce its size, sampling strategies, **Flash Attention**.
- **Scaling laws; GPUs.**
- **Other architectures:** RNNs (vanilla, LSTM) vs transformers; **state space models**.
- **Post-training:** policy gradients → **PPO**, **RLHF**, **GRPO**, **DPO**.
- **Precision; Parallelism** (collective ops; data / pipeline / tensor parallelism); **Multimodality**.

## Why it matters

It strengthens the vault's core technical spine as a consolidated, interview-oriented reference. Materially relevant to [[Neural Network Fundamentals]] (MLP/backprop/optimizers, numerical stability), [[Transformer Architecture]] (attention, RMSNorm, SwiGLU, RoPE, the accounting view), [[LLM Inference]] (batching, speculative decoding, Flash Attention), [[KV Cache]] (cache sizing/reduction), [[Reinforcement Learning]] and [[Group Relative Policy Optimization]] / [[Direct Preference Optimization]] (PPO/RLHF/GRPO/DPO), [[Model Quantization and Efficiency]] (precision), and [[Mixture of Experts]] / scaling. It anchors the "study reference" pillar of [[ML Research Interview Preparation]].

## Tensions / open questions

- It is a single-author study aid, not a primary source; its job is consolidation and intuition, so durable claims should still trace to primary papers already cited on the relevant concept pages.
- The capture preserves structure and prose but not the original LaTeX/diagrams; exact formulas should be checked against the live page or primary sources.
- It is a living document and will keep changing after the 2026-06-30 capture.

## Affected pages

- [[ML Research Interview Preparation]]
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]
- [[LLM Inference]]
- [[Alisa Liu]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/2026-06-30 Alisa Liu - Book of LLMs.md`
- Source URL: [https://alisawuffles.notion.site/alisa-s-book-of-llms](https://alisawuffles.notion.site/alisa-s-book-of-llms)

## Related pages

- [[ML Research Interview Preparation]]
- [[Alisa Liu - The AI Research Job Search]]
- [[Alisa Liu - Math Notes]]
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Reinforcement Learning]]
- [[Alisa Liu]]
- [[AI Knowledge Base Overview]]
