---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-12-zhang-recurrent-looped-transformer
source_title: "Recurrent Looped Transformer"
source_author: Yifan Zhang
source_url: https://yifanzhang-pro.github.io/recurrent-looped-tranformer/
tags: [source/summary, recurrent-transformers, latent-reasoning, reinforcement-learning]
source_ids: [src-2026-09-12-zhang-recurrent-looped-transformer]
status: active
---

# Yifan Zhang - Recurrent Looped Transformer

## Summary

The Recurrent Looped Transformer combines a causal encoder with a recurrent decoder that carries both
its final hidden state and layerwise sliding-window KV state across prompt and response tokens. Prompt
ingestion and generation therefore share one continuous state transition rather than resetting at
the prefill/decode boundary.

## Key claims

- The concrete design has 48 encoder and 48 decoder layers with compatible attention and feed-forward
  weights shared between them.
- After `t` tokens, the recurrent temporal path has traversed `48t` decoder blocks, while each token
  still executes 96 logical blocks.
- Encoder work over known prompt tokens can be parallelized, but recurrent decoder updates remain
  token-ordered.
- Exact full backpropagation must include recurrent outputs, decoder KV, and encoder-memory paths.
- Parameter updates invalidate cached state for exact current-policy replay; behavior probabilities
  must come from the actual sampler.

## Why it matters

The design joins recurrent latent computation, serving state, and RL replay into one contract. Its
"unbounded depth" is temporal path length as a sequence grows—not unlimited per-token computation.

## Tensions and caveats

This is an architecture specification without a training run, benchmark, parameter count, FLOP
comparison, throughput result, or quality ablation. The author explicitly says reasoning gains,
hardware efficiency, and RL scaling remain unestablished.

## Raw capture

- [[2026-09-12 Yifan Zhang - Recurrent Looped Transformer]]

## Affected pages

- [[Recursive Architectures]]
- [[Linear Attention and Recurrent Memory]]
- [[Long-Horizon Credit Assignment]]
- [[Yifan Zhang]]

## Related pages

- [[Latent-Space Reasoning]]
- [[KV Cache]]
- [[Agentic Reinforcement Learning]]

