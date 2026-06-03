---
type: concept
created: 2026-06-03
updated: 2026-06-03
tags:
  - concept
  - llm
  - moe
  - efficiency
  - sparse-models
source_ids:
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
status: active
---

# Mixture of Experts

## Definition

Mixture of Experts (MoE) is a sparse-model architecture where only a subset of specialized sub-networks, or experts, is activated for a given token or input instead of executing the full parameter set every time.

## Why it matters

MoE matters because it changes the tradeoff between **total model capacity** and **active inference cost**. A model can be large enough to store more capability while only paying the compute and memory price of a smaller active subnetwork on each step.

## Current synthesis

- The Reiner Pope flashcards show the systems side of MoE: expert routing is an all-to-all communication pattern, which makes rack topology and interconnect bandwidth first-class design constraints.
- The Liquid AI LFM2.5 source shows the product side: an 8B total / 1B active model can still feel fast enough for laptop and phone deployment while preserving a larger capacity budget than a similarly cheap dense model.
- That makes MoE a different kind of efficiency lever from quantization or KV caching:
  - **Quantization** shrinks stored precision.
  - **KV cache** avoids recomputing old attention state.
  - **MoE** reduces the amount of the network that is active per token.
- MoE also changes the economics of explicit reasoning. Liquid AI argues that sparse models can afford more reasoning tokens because each step is cheaper than in a dense model with similar total capacity.
- The downside is routing and systems complexity. Sparse models only deliver their theoretical win if runtimes, kernels, memory layout, and cluster topology support efficient expert dispatch.
- MoE therefore lives at the boundary of architecture and infrastructure: it is both a model design choice and a deployment problem.

## Open questions

- When does the routing overhead outweigh the compute saved by sparsity?
- Which applications benefit most from MoE: long-context assistants, agentic tool use, multilingual models, or something else?
- How much of future sparse-model progress will depend on better runtimes rather than better expert architectures?

## Related pages

- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[Model Quantization and Efficiency]]
- [[AI Accelerator Architecture]]
- [[AI Agents in Production]]
- [[Liquid AI]]
