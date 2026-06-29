---
type: concept
created: 2026-06-28
updated: 2026-06-28
tags:
  - concept
  - transformers
  - video
  - attention
  - computer-vision
source_ids:
  - src-2026-06-28-mayank-pratap-singh-timesformer
status: active
---

# Video Transformers

## Definition

Video transformers extend the Vision Transformer (ViT) recipe from single images to video by turning every frame into patch tokens and using self-attention to model both **appearance** (within a frame) and **motion** (across frames). The central design question is how to arrange attention over the space-time token grid without paying the full quadratic cost of attending to every patch in every frame. TimeSformer is the canonical early example.

## Why it matters

This page extends [[Transformer Architecture]] beyond text and still images into the spatiotemporal setting, and it is a clean case study in a general theme: **factorizing attention along structured axes to control quadratic cost**. The same intuition reappears in axial/divided designs elsewhere and connects to the broader cost arguments in [[KV Cache]] and [[LLM Inference]].

## How a video becomes tokens

[[Mayank Pratap Singh - Transformers for Video - TimeSformer]] describes the setup: split each frame into N spatial patches, embed them, and stack over F frames to get a token tensor of shape `[B, F, N, D]`, plus separate **space and time positional embeddings** and a class token. Attention then operates over this grid.

## Five attention patterns

TimeSformer studies five ways to choose which patches a query may attend to:

1. **Space-only** — attend within the same frame only (`N+1` keys/query). Cheap; works when appearance alone predicts the label; cannot model change across frames.
2. **Joint space-time** — attend to every patch in every frame (`NF+1` keys/query). Full global view but expensive: at N=196, F=8 that is 1,569 keys/query; at F=96 it is 18,817, enough to exhaust GPU memory.
3. **Divided space-time** — the main TimeSformer design: inside each block, do **temporal attention** (same patch location across frames) then **spatial attention** (patches within a frame). Cost is only `N + F + 2` per query (206 vs 1,569 at F=8; 294 vs 18,817 at F=96).
4. **Sparse local-global** — dense local neighborhood plus a sparse set of global locations; underperformed divided attention in the paper.
5. **Axial** — decompose into 1-D passes over time, then width, then height; cheaper per op but constrains information flow.

## Why divided attention wins

Joint attention is the most expressive but is expensive and shares one set of parameters for space and time. Divided attention uses **separate temporal and spatial Q/K/V projections**, so it has more specialized capacity while doing far less pairwise work. The result holds on both cost and accuracy:

| Pattern | Kinetics-400 | Something-Something-V2 |
| --- | ---: | ---: |
| Space-only | 76.9% | 36.6% |
| Divided space-time | 78.0% | 59.5% |

Kinetics labels are often predictable from appearance (so space-only does okay), but Something-Something-V2 requires temporal reasoning, where space-only collapses and divided attention's temporal branch matters. The lesson is not "time replaces space" but "video needs both, just not in one giant attention matrix."

## Implementation trick

Divided attention is a reshape: run temporal attention with F as the sequence dimension (`rearrange(x, "b f n d -> (b n) f d")`), then spatial attention with N as the sequence dimension (`(b f) n d`). The rest (patch embedding, class token, positional embeddings, LayerNorm, MLP, head) is inherited from ViT.

## Vs 3D convolutional models

Before video transformers, strong classifiers used **3D convolutions**, which slide a local kernel over height, width, and time and carry a built-in local motion bias but build long-range relations slowly. TimeSformer instead connects distant patches directly via attention. Reported numbers: default TimeSformer 121.4M params at 0.59 TFLOPs vs 1.97 TFLOPs for SlowFast R50; TimeSformer-L processes 96 frames for 80.7% top-1 on Kinetics-400. The tradeoff: transformers benefit from large image-pretraining and data; 3D CNNs keep stronger inductive biases in small-data regimes.

## Open questions

- How do newer video models (masked video autoencoders, tube tokenization, state-space video models) compare with divided space-time attention?
- The best attention factorization appears dataset-dependent (appearance-biased vs temporal-reasoning benchmarks); is there a universal default?
- How far can divided/axial factorization scale clip length before KV/attention memory again dominates?

## Related pages

- [[Mayank Pratap Singh - Transformers for Video - TimeSformer]]
- [[Transformer Architecture]]
- [[Diffusion Models]]
- [[Vision-Language Grounding]]
- [[LLM Inference]]
- [[AI Knowledge Base Overview]]
