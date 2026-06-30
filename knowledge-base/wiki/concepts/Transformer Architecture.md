---
type: concept
created: 2026-05-18
updated: 2026-06-30
tags:
  - concept
  - llm
  - transformer
  - attention
  - inference
source_ids:
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-05-18-hanfang-pytorch-practice
  - src-2026-06-03-fareed-khan-train-llm-from-scratch
  - src-2026-06-10-0xkato-how-llms-actually-work
  - src-2026-06-17-prateek-singh-kv-cache-turboquant
  - src-2026-06-28-mayank-pratap-singh-timesformer
  - src-2026-06-30-alisa-liu-book-of-llms
status: active
---

# Transformer Architecture

## Definition

A Transformer architecture is the attention-centered neural-network design behind modern LLMs: tokens are embedded into vectors, enriched with positional information, passed through repeated blocks of masked self-attention and MLP computation, and finally projected into next-token logits.

## Why it matters

This is the core blueprint behind most of the vault's LLM-related material. If this page is clear, other topics such as pretraining, SFT, RLHF, RoPE, KV cache, and quantization become much easier to place.

## Current synthesis

- The PocketFlow tutorials make the decoder-only GPT pattern legible by separating it into a few stable parts: **token embeddings**, **position handling**, **causal self-attention**, **MLP blocks**, **residual connections**, **layer normalization**, and the **autoregressive generation loop**.
- The attention tutorial isolates the central move: static token vectors become context-sensitive because each token forms **queries, keys, and values**, scores other tokens with scaled dot products, applies a causal mask, and mixes information with a weighted sum.
- The broader Transformer tutorial shows that the model's power is not from one exotic component but from **stacking many identical blocks**. Each block alternates relational computation (attention) with per-token transformation (MLP), while residual paths and normalization keep optimization stable.
- The RoPE tutorial reframes positional encoding as a property of the **attention calculation itself**. Instead of adding a learned absolute position vector to the input, RoPE rotates Q/K vectors so their dot product naturally depends on **relative distance**, which better matches how language patterns recur at different offsets.
- The KV-cache tutorial highlights that architecture is not just a training-time blueprint; it also determines inference behavior. In naive generation, the model repeatedly recomputes keys and values for the entire prefix. KV cache turns this into **incremental decoding** by storing past K/V tensors and computing only the new token's additions.
- Put differently, the PocketFlow material makes Transformer understanding happen on three levels at once:
  - **Representational** — embeddings plus positional structure
  - **Relational** — attention as context construction
  - **Operational** — caching and masking as the mechanics of real generation
- A useful durable takeaway is that modern LLM improvements often modify one of these layers rather than replacing the whole architecture: RoPE changes positional handling, KV cache changes inference-time state reuse, and quantization changes numerical/storage strategy.
- [[Han Fang - PyTorch Practice]] reinforces the implementation view with a from-scratch multi-head attention module that projects Q/K/V, reshapes them to `(batch, heads, seq, d_k)`, applies padding and causal masks inside scaled dot-product attention, and then concatenates heads back into the model dimension.
- [[Fareed Khan - Train LLM From Scratch]] adds a plain GPT-style baseline implementation: learned token and absolute position embeddings, repeated blocks of causal multi-head attention plus MLP, layer normalization, and a simple multinomial sampling loop for next-token generation. That is a useful complement to newer RoPE/KV-cache-oriented explanations because it makes the unadorned decoder-only backbone concrete.
- [[0xkato - How LLMs Actually Work]] fills in several gaps between those sources. It makes explicit that tokenization, embeddings, positional encoding, attention, feed-forward computation, residual accumulation, and the next-token loop are separate problems that later model families keep solving with slightly better choices rather than radically different blueprints.
- The article also clarifies some "modern stack" details that are easy to blur together:
  - **RoPE** is position information expressed inside Q/K comparisons rather than another additive input vector.
  - **GQA** is largely an inference-memory optimization: many query heads can share fewer key/value heads, reducing KV-cache pressure.
  - **RMSNorm + pre-norm** are part of the recipe that made very deep Transformers more stable to train.
  - **Speculative decoding** belongs to the generation loop side of the stack, not the training architecture proper.
- A useful vault-level synthesis from the article is that current model families differ less in fundamental layout than in **trained weights**, **scale/configuration**, and **post-training**. The transformer skeleton has converged more than vendor branding suggests.
- [[Prateek Singh - KV Cache and TurboQuant]] makes the operational side concrete enough that [[KV Cache]] now deserves its own page. KV cache is not only "store old K/V tensors"; it is the main memory surface for long-context decoding. GQA, MQA, MLA, PagedAttention, token eviction, predictive skipping, and TurboQuant all exist because the attention architecture's cached state grows linearly with context.
- [[Mayank Pratap Singh - Transformers for Video - TimeSformer]] extends the same attention skeleton beyond text and images into the spatiotemporal setting. It shows that the quadratic cost of attention can be controlled by **factorizing it along structured axes** — TimeSformer's divided space-time attention runs temporal then spatial attention with separate Q/K/V projections, cutting cost from `NF+1` to `N+F+2` keys per query while improving accuracy. This is the video branch of the architecture, developed on its own page [[Video Transformers]].
- [[Alisa Liu - Book of LLMs]] adds an interview-oriented consolidation of this same architecture: Attention, **RMSNorm**, the **SwiGLU FFN** (`(xW₁) ⊙ Swish(xW₂)`), and **RoPE**, plus an unusually explicit "accounting" view — how to count parameters, activation memory, and forward/backward FLOPs. That accounting framing is a useful study layer for the rapid-fire technical-discussion round described in [[ML Research Interview Preparation]].

## Open questions

- How far can the current attention-centric blueprint scale before alternative architectures become more attractive for long-context reasoning?
- Which efficiency techniques should be treated as architectural essentials versus implementation details?

## Related pages

- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Han Fang - PyTorch Practice]]
- [[Fareed Khan - Train LLM From Scratch]]
- [[Alisa Liu - Book of LLMs]]
- [[0xkato - How LLMs Actually Work]]
- [[Video Transformers]]
- [[Mayank Pratap Singh - Transformers for Video - TimeSformer]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Prateek Singh - KV Cache and TurboQuant]]
- [[LLM Training Pipeline]]
- [[Neural Network Fundamentals]]
- [[Model Quantization and Efficiency]]
- [[AI Knowledge Base Overview]]
