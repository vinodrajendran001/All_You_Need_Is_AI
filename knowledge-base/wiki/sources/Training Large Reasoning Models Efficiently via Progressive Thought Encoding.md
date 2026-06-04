---
type: source-summary
created: 2026-06-04
updated: 2026-06-04
source_id: src-2026-06-04-progressive-thought-encoding
source_title: Training Large Reasoning Models Efficiently via Progressive Thought Encoding
source_author: Zeliang Zhang et al.
source_url: https://arxiv.org/abs/2602.16839
tags:
  - source-summary
  - reasoning
  - efficiency
  - rl
source_ids:
  - src-2026-06-04-progressive-thought-encoding
status: active
---

# Training Large Reasoning Models Efficiently via Progressive Thought Encoding

## Summary

This paper targets an overlooked bottleneck in reasoning-model training: long outcome-reward rollouts make RL fine-tuning memory-heavy because autoregressive decoding dominates cache usage. Its answer is **Progressive Thought Encoding (PTE)**, a parameter-efficient method that progressively compresses intermediate reasoning into fixed-size vector states so the model can keep reasoning under bounded cache budgets.

The source matters because it treats reasoning compression not only as inference-time shortening, but also as a training-time memory problem. Instead of learning shorter visible traces only after the fact, it changes the representation of intermediate thought during RL itself.

## Key claims

- Long-rollout RL training for LRMs is bottlenecked by cache growth and memory, not only by model size.
- Progressive Thought Encoding compresses intermediate reasoning into fixed-size vectors, enabling bounded-memory training and constant-memory inference under tight cache limits.
- The method is parameter-efficient and works across multiple backbones, including Qwen2.5-3B, Qwen2.5-7B, and DeepSeek-R1-Distill-Llama-8B.
- The reported gains are large under constrained settings: the paper claims sizable average improvements over LoRA fine-tuning and non-fine-tuned baselines, especially on AIME-style benchmarks under fixed cache budgets.

## Why it matters

This source broadens the vault's efficient-reasoning branch by showing that compression can happen in **representation space**, not only by shortening emitted token traces. It also creates a bridge between explicit CoT compression and latent/internal reasoning ideas.

## Tensions / open questions

- How much reasoning fidelity survives when intermediate thought is aggressively vectorized rather than left as text?
- Does bounded-cache reasoning generalize beyond math-heavy settings to broader agentic workloads?
- When should fixed-size internal encodings replace explicit CoT, and when do they remove too much inspectability?

## Affected pages

- [[Reasoning Compression]]
- [[LLM Training Pipeline]]
- [[Latent-Space Reasoning]]
- [[On-Device Reasoning]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-06-04 Zeliang Zhang et al - Training Large Reasoning Models Efficiently via Progressive Thought Encoding.md`
- Local PDF: [2026-06-04 Zeliang Zhang et al - Training Large Reasoning Models Efficiently via Progressive Thought Encoding.pdf](../../raw/sources/2026-06-04%20Zeliang%20Zhang%20et%20al%20-%20Training%20Large%20Reasoning%20Models%20Efficiently%20via%20Progressive%20Thought%20Encoding.pdf)

## Related pages

- [[Reasoning Compression]]
- [[LLM Training Pipeline]]
- [[Latent-Space Reasoning]]
- [[On-Device Reasoning]]
- [[Efficient Reasoning on the Edge]]
