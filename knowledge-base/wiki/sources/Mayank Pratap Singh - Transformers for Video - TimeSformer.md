---
type: source-summary
created: 2026-06-28
updated: 2026-06-28
source_id: src-2026-06-28-mayank-pratap-singh-timesformer
source_title: "Transformers for Video: TimeSformer"
source_author: Mayank Pratap Singh
source_url: https://vizuara.substack.com/p/transformers-for-video-timesformer
tags:
  - source-summary
  - transformers
  - video
  - attention
  - computer-vision
status: active
source_ids:
  - src-2026-06-28-mayank-pratap-singh-timesformer
---

# Mayank Pratap Singh - Transformers for Video - TimeSformer

## Summary

This Vizuara explainer adapts the Vision Transformer idea to video through TimeSformer. A video is cut into per-frame patch tokens, embedded, and given both space and time positional information; attention then models appearance within frames and motion across frames. The article's core contribution is a clear comparison of five attention patterns over the space-time token grid and an argument for why **divided space-time attention** is the practical winner.

It covers tokenization (`[B, F, N, D]` tensors), the five patterns (space-only, joint space-time, divided space-time, sparse local-global, axial), the cost arithmetic that makes joint attention blow up, a `rearrange`-based implementation sketch of divided attention, what the model learns (attention tracks hand-object interactions; cleaner t-SNE action clusters), and a comparison with 3D-convolutional video models.

## Key claims

- **A video becomes patch tokens per frame**; with N spatial patches over F frames, the model reasons over an `[B, F, N, D]` token grid plus space and time positional embeddings and a class token.
- **Five attention patterns** are studied: space-only (frame-local), joint space-time (global, expensive), divided space-time (temporal then spatial), sparse local-global, and axial (time → width → height).
- **Joint space-time attention** gives each query `NF+1` keys; at N=196, F=8 that is 1,569 keys/query, and at F=96 it is 18,817 — enough to exhaust GPU memory.
- **Divided space-time attention** factorizes a block into temporal attention (same patch across frames) then spatial attention (patches within a frame), costing only `N + F + 2` comparisons/query (206 vs 1,569 at F=8; 294 vs 18,817 at F=96).
- **Divided attention wins on accuracy too**: 78.0% on Kinetics-400 and 59.5% on Something-Something-V2, beating the other patterns; space-only reaches 76.9% on Kinetics-400 but collapses to 36.6% on SSv2, which needs temporal reasoning.
- **Divided attention gives separate temporal and spatial Q/K/V projections** — more specialized capacity while doing less pairwise work than joint attention.
- **Implementation trick**: reshape so temporal attention treats F as the sequence (`(b n) f d`) and spatial attention treats N as the sequence (`(b f) n d`).
- **Vs 3D CNNs**: 3D convolutions have a built-in local motion bias but build long-range relations slowly; TimeSformer connects distant patches directly. Default TimeSformer is 121.4M params at 0.59 TFLOPs vs 1.97 TFLOPs for SlowFast R50; TimeSformer-L processes 96 frames for 80.7% top-1 on Kinetics-400.

## Why it matters

This source seeds [[Video Transformers]] as a new concept and extends [[Transformer Architecture]] from text/image into the spatiotemporal setting. It connects to [[KV Cache]] / [[LLM Inference]] only loosely (attention cost), but strongly to the general lesson that factorizing attention along structured axes controls quadratic cost — a theme shared with axial/divided designs elsewhere. It is the second Vizuara / [[Mayank Pratap Singh]] source after [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]], reinforcing the [[Vizuara]] entity.

## Tensions / open questions

- TimeSformer benefits from large-scale image pretraining; 3D CNNs may still be easier in small-data regimes (the source states this tradeoff explicitly).
- The article covers the original TimeSformer attention designs; newer video models (video MAE, tokenized-tube, state-space video) are out of scope.
- Sparse local-global and axial patterns underperform divided attention here, but the result is dataset-dependent and not a universal ranking.

## Affected pages

- [[Video Transformers]]
- [[Transformer Architecture]]
- [[Mayank Pratap Singh]]
- [[Vizuara]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/Transformers for Video TimeSformer.md`
- Source URL: [https://vizuara.substack.com/p/transformers-for-video-timesformer](https://vizuara.substack.com/p/transformers-for-video-timesformer)

## Related pages

- [[Video Transformers]]
- [[Transformer Architecture]]
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]]
- [[Mayank Pratap Singh]]
- [[Vizuara]]
- [[AI Knowledge Base Overview]]
