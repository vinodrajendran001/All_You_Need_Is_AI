---
type: source-summary
created: 2026-10-16
updated: 2026-10-16
source_id: src-2026-10-13-zancato-model-priming
source_title: "Can we change an AI model's architecture without retraining it from scratch?"
source_author: Luca Zancato
source_url: https://www.amazon.science/blog/can-we-change-an-ai-models-architecture-without-retraining-it-from-scratch
tags: [source/summary, architecture, state-space-models, distillation, inference]
source_ids: [src-2026-10-13-zancato-model-priming]
status: active
---

# Luca Zancato - Priming Hybrid Models from Pretrained Transformers

## Summary

An Amazon Web Services research account of **priming**: converting selected attention layers in an
already pretrained Transformer into state-space layers, rather than pretraining every hybrid from
scratch. The contribution is a controlled way to explore memory architectures using transferred
weights, short layerwise alignment, and full-model adaptation. This is not a training-free
architecture swap, and the reported savings exclude the original donor model's pretraining.

## Key claims

- **Selection precedes conversion.** Replace individual attention layers with sliding-window
  attention and measure degradation. Layers tolerant of that restriction are candidates for
  fixed-state conversion; other layers retain token-addressable attention. This is an empirical
  proxy motivated by the mixing matrix's Hankel rank, not a certificate that any substitution
  preserves behavior.
- **Three stages:** layer selection; transfer query/key/value projections and learn state-space
  parameters through short distillation/alignment; then adapt the whole hybrid with next-token
  prediction so its layers can coadapt.
- The pipeline reportedly uses **less than 0.5% of the donor's pretraining token budget**. The
  headline's **over 99% pretraining-cost reduction** is a different quantity; token counts are not
  measured total compute, elapsed time, or an all-in bill.
- At matched data, adaptation budget, and hybrid ratio, the reported ordering is
  **Gated KalmaNet (GKA) > Gated DeltaNet > Mamba-2**, especially on long-context tasks.
  The body says state-space hybrids beat corresponding sliding-window hybrids even when the
  window receives **two to four times** the state-memory budget. These are tested configurations,
  not a theorem that state-space models always beat attention.
- GKA exposes an iteration count at serving time. Moving from **30 to 10 iterations** reportedly
  gives **10% faster decoding** with roughly **1% accuracy loss on AIME 2025**. The article does
  not clearly distinguish relative percent from percentage points for that loss.

| Reported comparison | Condition and result |
| --- | --- |
| 32B hybrid versus source Transformer | Within about 1% on reported quality measures, with roughly half the KV cache |
| Decode throughput, 32B GKA at 10 iterations | 1.50x at 16K context; 2.06x at 128K |
| Decode throughput, 8B variants | 1.94x at 16K; 2.29x at 128K |
| Time to target accuracy on AIME 2025 | 1.2-1.4x faster on the full set; up to 1.6x on the hardest problems |
| Training-free context composition | 128K to 256K, with substantial reported RULER NIAH and BABILong accuracy, not a stated lossless extension |

The time-to-accuracy comparison uses the primed Qwen3-32B reasoner and a source model trained
with the same reasoning recipe, at concurrency where cache capacity matters. Similar trace
lengths do not themselves establish equal reasoning quality.

For context extension, independently process chunks with a shared prefix, concatenate attention
caches, and combine recurrent states using PICASO-style weighted composition. The release includes
8B/32B models, training code, kernels, and a vLLM plugin with batching, chunked prefill, and tensor
parallelism, described as Apache-2.0 artifacts.

## Why it matters

Architecture, weight reuse, and training budget are separable choices. Priming complements
[[Knowledge Distillation]] and [[Model Quantization and Efficiency]] without being ordinary
weight quantization or pure layer deletion. Its runtime iteration knob also separates internal
computation from a provider's visible reasoning-token budget.

## Tensions / open questions

- This is a first-party account; the linked paper, code, licenses, and benchmarks were not
  independently reproduced or audited in this ingest.
- The closing "no quality loss" pitch is broader than the reported near-source accuracy and
  explicit iteration/accuracy tradeoff. Preserve the operating point rather than the slogan.
- "Eidetic" attention means access to token-indexed representations, not literal storage of text
  or guaranteed recall. [[Transformer Architecture]] already distinguishes access from use.
- Halving KV cache is not halving all device memory: weights, recurrent states, workspace, and
  runtime overhead remain.
- Donor training is a sunk input. Amortization across variants, calibration data, kernel support,
  and broad capability regressions still determine whether conversion is economical.

## Affected pages

- [[Linear Attention and Recurrent Memory]]
- [[Transformer Architecture]]
- [[Knowledge Distillation]]
- [[LLM Training Pipeline]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Reasoning Effort Control]]
- [[Inference Efficiency Frontier]]
- [[Inference Serving Engines]]
- [[Qwen]]

## Raw capture

- [[Can we change an AI model’s architecture without retraining it from scratch]]

## Citations

- Canonical article: <https://www.amazon.science/blog/can-we-change-an-ai-models-architecture-without-retraining-it-from-scratch>
- Published October 13; captured October 14, 2026.
- Linked research, not separately ingested: <https://arxiv.org/abs/2605.08301>.
- Linked implementation: <https://github.com/awslabs/hybrid-model-factory>.

## Related pages

- [[Linear Attention and Recurrent Memory]]
- [[Knowledge Distillation]]
- [[KV Cache]]
- [[Reasoning Effort Control]]
- [[Serving Benchmarks and Goodput]]
- [[Qwen]]
