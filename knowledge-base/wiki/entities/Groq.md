---
type: entity
created: 2026-08-25
updated: 2026-08-25
entity_kind: organization
tags:
  - entity
  - organization
  - hardware
  - accelerators
  - inference
source_ids:
  - src-2026-08-25-jacob-peake-ai-chip-architectures
status: active
---

# Groq

## What it is

Designer of the LPU (Language Processing Unit), a deterministic SRAM-only inference accelerator. Per [[Jacob Peake - AI Chip Architectures]], the technology and much of the team — including Ross — were folded into NVIDIA via a reported $20B acquihire plus a non-exclusive licensing agreement, with the Groq 3 line continuing under NVIDIA.

## Why it matters here

Groq is the vault's purest expression of a single architectural conviction: **determinism over tolerance**. Every reactive component that a conventional processor uses to absorb uncertainty — caches, arbiters, branch predictors, reorder buffers — is deleted, and the compiler owns every cycle. Its second bet is spatial: the core is disaggregated into functional slices and operands stream through them, so *fusion is the floorplan* and data reuse lives in the wires rather than in a register-file dance.

That conviction extends to the network, which is the more surprising part. The scale-out fabric is **"scheduled, not routed"**: routing and flow control move to compile time, there is no back-pressure and no dynamic arbitration because the compiler has already proven the receiver is ready, and links carry forward error correction *instead of* retransmission because a retry would perturb the schedule. Keeping independently clocked chips in lockstep is handled by Hardware-Aligned Counters exchanged every 256 cycles over a spanning tree. The chips are the routers — no NICs, no switches — with 8 LPUs forming a node and 9 nodes a 72-chip rack.

For [[Arithmetic Intensity and the Roofline Model]] it occupies the same corner as [[Cerebras]]: enormous SRAM bandwidth against tiny capacity (230 MB per first-generation chip, 500 MB on Groq 3 LP30), which wins per-user decode latency and loses on throughput per dollar. SemiAnalysis's summary is the useful one — the LPU wins bill-of-materials per token when you optimise for latency, and loses to GPUs by roughly an order of magnitude on throughput per dollar once you batch. **The architecture is not competing on cost; it is competing on speed.**

## Notes

- The capacity bet has a system-level cost: a model replica is a rack, not a box. One analysis of Llama-2 70B on ~576 chips counted 144 host CPUs and 144 TB of host RAM alongside the LPUs, against two CPUs for an 8-GPU server.
- Groq 3 LPX pairs 128 GB of SRAM across 256 chips with a 12 TB DDR5 tier and is positioned alongside Rubin, which suggests the LPU now **complements** a large-memory GPU rack rather than replacing it.
- The wafer is cheap (14 nm GlobalFoundries, reportedly under $6k against ~$16k for an H100-class part) — but you need hundreds of them.

## Related pages

- [[Jacob Peake - AI Chip Architectures]]
- [[AI Accelerator Architecture]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Cerebras]]
- [[NVIDIA]]
- [[Inference Serving Engines]]
- [[LLM Inference]]
- [[AI Knowledge Base Overview]]
