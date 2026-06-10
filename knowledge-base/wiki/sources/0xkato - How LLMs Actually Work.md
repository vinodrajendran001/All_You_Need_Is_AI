---
type: source-summary
created: 2026-06-10
updated: 2026-06-10
source_id: src-2026-06-10-0xkato-how-llms-actually-work
source_title: How LLMs Actually Work
source_author: 0xkato
source_url: https://www.0xkato.xyz/how-llms-actually-work/?utm_source=tldrai
tags:
  - source-summary
  - llm
  - transformer
  - architecture
  - inference
source_ids:
  - src-2026-06-10-0xkato-how-llms-actually-work
status: active
---

# 0xkato - How LLMs Actually Work

## Summary

A from-the-ground-up tutorial article that explains modern decoder-only LLMs as repeated Transformer blocks rather than as a mysterious new class of model. The post walks cleanly from tokenization to embeddings, positional encoding, attention, multi-head attention, feed-forward networks, residual streams, normalization, next-token prediction, and the generation loop. Its main value to this vault is not novelty but integration: it ties together several pieces already present in separate notes and explains why the current "modern transformer stack" has converged on RoPE, GQA, RMSNorm, SwiGLU, and occasionally MoE.

## Key claims

- Modern LLMs mostly share the same **transformer-family skeleton**. Differences between major model families come more from trained weights, scale/configuration, and post-training than from radically different core architectures.
- **Tokenization** is a compute/coverage compromise. Whole-word vocabularies are too large; character-level vocabularies are too small; subword tokenization balances efficiency with generalization.
- **Embeddings** give token IDs meaning, but not order. Positional structure must be added separately.
- **RoPE** is better understood as position information inside the attention calculation itself: it rotates Q/K vectors so relative distance shows up in their comparison, rather than adding absolute position vectors to embeddings.
- The article gives a very clear description of **attention** as Q/K/V matching plus weighted Value copying, and links **induction heads** to in-context learning.
- **Grouped-Query Attention (GQA)** is one of the major inference-era architectural refinements: many query heads can share fewer key/value heads, substantially reducing KV-cache memory pressure.
- The **feed-forward network** is not just generic post-attention compute; it stores a large share of the model's factual/semantic structure, which is why targeted model-editing methods such as ROME operate on FFN weights.
- The **residual stream** is the central additive object that every block reads from and writes back to. This matters for both trainability and interpretability.
- **RMSNorm** and pre-norm placement are part of the practical recipe that made deeper Transformers train reliably.
- **Speculative decoding** is a durable inference optimization: a small draft model proposes tokens ahead, the large model verifies them in parallel, and the resulting distribution can match running the large model alone.

## Why it matters

This source materially deepens [[Transformer Architecture]] by turning several isolated mechanism notes into one integrated walkthrough. It also sharpens the vault's distinction between *architecture* and *trained behavior*: the architecture has converged more than marketing language around model families often suggests.

## Tensions / open questions

- The article is intentionally light on math, which makes it accessible but means some implementation subtleties are simplified.
- It focuses on the dominant Transformer design space. Alternative sequence-model families such as state-space models appear only briefly at the end.

## Affected pages

- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]
- [[Mixture of Experts]]
- [[Model Quantization and Efficiency]]
- [[AI Knowledge Base Overview]]

## Raw capture

- `knowledge-base/raw/sources/How LLMs Actually Work.md`

## Related pages

- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]
- [[Mixture of Experts]]
- [[Model Quantization and Efficiency]]
- [[AI Knowledge Base Overview]]
