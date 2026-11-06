---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-03-bytebytego-nemotron
source_title: How Nvidia's New Nemotron Model Works
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-nvidias-new-nemotron-model-works
tags:
  - source/summary
  - model-architecture
  - mixture-of-experts
  - quantization
  - nvidia
source_ids:
  - src-2026-11-03-bytebytego-nemotron
status: active
---

# How Nvidia's New Nemotron Model Works

## Summary

ByteByteGo explains NVIDIA's Nemotron 3 family as an efficiency design for agent workloads, where a
coding agent "might have to make dozens of model calls" on one problem. The article is secondary
reporting: it walks through three NVIDIA documents (the Nemotron 3 family white paper, the Nemotron 3
Super technical report, and an NVIDIA developer-blog post) and adds no measurements of its own. Its
centre is a configuration it calls "Nemotron Lightning", described as having 30 billion total
parameters. That configuration interleaves Mamba layers, attention layers, and mixture-of-experts (MoE)
layers so that most sequence processing uses a fixed-size state while a few attention layers keep
precise access to earlier positions. Around that architecture the article lists a training recipe
(pretraining, supervised fine-tuning, reinforcement learning), multi-token prediction for speculative
decoding, NVFP4 quantization with quantization-aware distillation, and the larger Super and Ultra
models with LatentMoE. Its value is a compact map of which mechanism addresses which cost.

## Key claims

### Mamba and attention divide the sequence work

- A Mamba layer keeps a compact numerical state, and during generation its "state size and per-token
  update cost stay fixed", so it does not search an ever-growing cache. The stated trade-off is that
  compressing a long history into a bounded state can make precise retrieval difficult.
- Nemotron interleaves Mamba, attention, and expert layers in one network. "The remaining attention
  layers maintain KV caches", so the KV-cache bill applies only to the attention layers that remain.
  The article gives no Mamba-to-attention ratio.

### Sparse experts and grouped-query attention

- Lightning uses **128** routed experts per MoE layer with **6** selected per token, which is how a
  model of roughly **30** billion parameters uses only roughly **3** billion for a given token.
- Lightning's attention uses **32** query heads and only **2** key-value heads, a grouped-query
  attention (GQA) arrangement that keeps multiple ways of querying context while storing fewer
  key-value representations.

### Training recipe

- **Pretraining** on crawled and synthetic material covering code, maths, science, and general
  knowledge, moving from a broad mixture toward more emphasis on high-quality material.
- **Supervised fine-tuning (SFT)** in which user and system messages supply context but the
  objective is calculated on assistant tokens.
- **Reinforcement learning** with Group Relative Policy Optimization (GRPO): several responses per
  prompt are rewarded and compared relative to each other. The recipe's environment evaluates
  mathematical answers, executes code against tests, checks instruction compliance, and validates
  output schemas.

### Multi-token prediction for speculation

Multi-token prediction (MTP) trains an auxiliary mechanism to predict further ahead, which can
support speculative decoding at inference time. The article says "Nvidia's models ship with
integrated MTP capabilities and separate draft models". No acceptance rates or speedups are given.

### Four-bit weights with a fixed teacher

- NVFP4 stores four-bit floating-point values; groups of **16** values share an FP8 scale, with a
  further scale at the tensor level.
- Quantization-aware distillation (QAD) creates a quantized student from a BF16 model, keeps the
  BF16 model fixed as the teacher, and trains the student under simulated quantization to match the
  teacher's output scores.
- The reported result is a checkpoint shrinking from approx. **66 GB** in BF16 to approx. **22 GB** in
  NVFP4. The article does not say which model this is.

### Super, Ultra, and LatentMoE

- Nemotron 3 Super has approx. **120** billion total and **12** billion active parameters; Ultra has
  **550** billion total and **55** billion active. Both use the hybrid Mamba-attention design and
  introduce LatentMoE.
- LatentMoE projects token representations into a smaller space for routed expert computation,
  combines the expert outputs, and projects back. The narrower routed computation saves memory
  traffic and communication, which NVIDIA spends on "more experts and more active expert
  combinations at a similar inference budget".
- Ultra adds multi-teacher on-policy distillation: the student generates its own attempts and
  receives guidance from multiple domain-specialized teachers.

## Why it matters

[[Mixture of Experts]] and [[Linear Attention and Recurrent Memory]] gain a production-family example
of the hybrid pattern, plus LatentMoE as a way to reduce expert communication rather than simply add
experts. [[KV Cache]] gains a clear statement that a hybrid only pays cache costs in its attention
layers. [[Model Quantization and Efficiency]] gains NVFP4's two-level scaling and QAD, which joins a
teacher signal to quantization. [[LLM Training Pipeline]] gains a full pretrain-to-GRPO recipe with
verifiable checks, and [[Speculative Decoding]] a vendor shipping both built-in MTP and separate
drafters. For [[NVIDIA]], it adds the model-builder role to the hardware and runtime roles already
recorded. [[Knowledge Distillation]] and [[Multi-Teacher On-Policy Distillation]] gain a second,
secondary report of Ultra's multi-teacher recipe and a teacher-guided quantization case.

## Tensions / open questions

- Secondary reporting of first-party NVIDIA documents, which this ingest did not capture. Every
  configuration figure is NVIDIA's own and unverified here; the article reports no benchmarks,
  latency, throughput, or quality comparisons.
- "Nemotron Lightning" is not a name used elsewhere in the vault. The vault already records
  **NVIDIA-Nemotron-3-Nano-30B-A3B-FP8** as a hybrid of Mamba2, attention, and MoE layers. The two
  descriptions are similar (about 30B total, about 3B active), but the capture does not say they are
  the same model, so they are not merged here.
- The 66 GB to 22 GB result is unattributed to a specific model; 66 GB in BF16 would fit a model of
  roughly 30B to 33B parameters, but that is an inference, not a claim in the article.
- The sentence "ordinary generation can't proceed sequentially" reads as a slip for "can only proceed
  sequentially", given the explanation that follows it.
- The opening WorkOS sponsor block is advertising, not part of the article.

## Affected pages

- [[Mixture of Experts]]
- [[Linear Attention and Recurrent Memory]]
- [[KV Cache]]
- [[Speculative Decoding]]
- [[Model Quantization and Efficiency]]
- [[LLM Training Pipeline]]
- [[NVIDIA]]
- [[ByteByteGo]]
- [[Multi-Teacher On-Policy Distillation]]
- [[Knowledge Distillation]]

## Raw capture

- [[knowledge-base/raw/sources/How Nvidia's New Nemotron Model Works]]

## Citations

- Canonical URL: <https://blog.bytebytego.com/p/how-nvidias-new-nemotron-model-works>
- Byline: ByteByteGo. Underlying documents named in the capture: the Nemotron 3 family white paper,
  the Nemotron 3 Super technical report, and NVIDIA's developer-blog post "Inside Nvidia Nemotron 3".
- Published November 3, 2026; captured November 3, 2026. Email tracking parameters are omitted from
  the summary URL; the raw capture is unchanged.

## Related pages

- [[NVIDIA]]
- [[ByteByteGo]]
- [[Mixture of Experts]]
- [[Linear Attention and Recurrent Memory]]
- [[KV Cache]]
- [[Speculative Decoding]]
- [[Model Quantization and Efficiency]]
- [[LLM Training Pipeline]]
- [[Multi-Teacher On-Policy Distillation]]
- [[Knowledge Distillation]]
- [[Antonio Tiene et al - Pruning LLMs Like a Physicist]]
- [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]]
- [[Ali Zahid Raja - Your Model Doesn't Have to Fit in Your GPU Anymore]]
- [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
