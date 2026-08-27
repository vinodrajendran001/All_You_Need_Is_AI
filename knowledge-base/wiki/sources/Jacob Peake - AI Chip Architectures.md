---
type: source-summary
created: 2026-08-25
updated: 2026-08-26
source_id: src-2026-08-25-jacob-peake-ai-chip-architectures
source_title: AI Chip Architectures
source_author: Jacob Peake
source_url: https://www.jacobpeake.com/ai-chip-architectures
tags: [source/summary, hardware, accelerators, gpu, tpu, systems]
source_ids: [src-2026-08-25-jacob-peake-ai-chip-architectures]
status: active
---

# Jacob Peake - AI Chip Architectures

## Summary

A long-form comparative survey of the six AI accelerator architectures that have won real deployment: NVIDIA GPUs, Google TPUs, AMD GPUs, the Cerebras Wafer-Scale Engine, AWS Trainium, and the Groq LPU. Each is examined through the same four lenses — genealogy, architecture, scaling (scale-up and scale-out), and software stack — and each is reduced to an explicit list of **bets** its designers made. The survey opens by framing the Hennessy–Patterson 2018 Turing Lecture prediction of "a Cambrian explosion of novel computer architectures" as now realised, and closes with per-chip and per-rack comparison tables spanning 2020–2027.

## Key claims

- **Understanding any AI chip reduces to four questions**: where data *lives*, how it *moves* to the compute units, what the *compute units* look like, and how chips *talk to each other at scale*. Every architecture is a different strategy for winning the data-movement game against the **memory wall**.
- **The workload shape, not the chip, decides the regime.** Training and prefill stack many tokens against the same weight matrix, so each layer is a large GEMM and is compute-bound. Decode emits one token at a time, so every matmul degenerates to a GEMV and arithmetic intensity drops by orders of magnitude. Continuous batching, speculative decoding, and multi-token prediction all exist to promote GEMVs back to GEMMs — with the caveat that under continuous batching each user still reads their own KV cache, so long-context decode shifts from weight-bandwidth-bound to **KV-bandwidth-bound**.
- **Per-chip FP8 has converged.** B200 (4.5 PF), TPU Ironwood (4.6 PF) and MI355X (10 PF) sit within roughly 2× of each other; the architectures now diverge at the rack and pod, not the die.
- **The TPU deletes dynamic scheduling on principle.** VLIW issue with a 322-bit eight-slot bundle, no instruction cache miss, no warp scheduler, no out-of-order engine, no branch predictor — the compiler is the scheduler and the saved area is spent on MACs. Its ICI interconnect is message-passing over a torus with optical circuit switches at the rack boundary, the inverse of NVLink's hardware-coherent address space.
- **Cerebras breaks the comparison's axes.** No HBM at all: 44 GB of on-wafer SRAM at ~21 PB/s aggregate, about 1.3 bytes per dense FLOP where GPU rows sit near 0.002. The WSE is a flat 900,000-core 2D mesh with no cache hierarchy and no die boundary — extra metal laid across the scribe lines makes 84 reticle-field dies present as one chip — and execution is dataflow: *the arrival of data is the schedule*.
- **Cerebras's speed is independently verified and its economics are the sharp edge.** Artificial Analysis measured 1,850 tok/s on Llama 3.1 8B and 2,522 tok/s on Llama 4 Maverick. But 44 GB per wafer means a frontier-scale model consumes fleets (SemiAnalysis estimates ~24 CS-3s for a 1.6T-class model), KV cache competes with weights for the same SRAM so context is capped at 131K, and per-token API pricing runs 3–5× GPU providers.
- **Groq's two bets are determinism and spatial slices.** Every reactive component — caches, arbiters, predictors, reorder buffers — is deleted and the compiler owns every cycle. The scale-out fabric is *scheduled, not routed*: no back-pressure, no dynamic arbitration, forward error correction instead of retransmission because a retry would perturb the schedule, and plesiochronous links kept in lockstep by Hardware-Aligned Counters exchanged every 256 cycles.
- **Groq competes on latency, not cost.** SemiAnalysis's reading: the LPU wins bill-of-materials per token when optimising for latency and loses to GPUs by roughly an order of magnitude on throughput per dollar once you batch.
- **Trainium competes on economics rather than the spec sheet.** Per-chip it trails (Trn2's 1.3 PF FP8 is roughly a quarter of MI355X), but AWS owns every layer from the Nitro card to the API, and Anthropic running over a million Trainium2 chips validates it at frontier scale.
- **Power per chip is rising fast** — 700 W (Hopper) → 1,000 W (Blackwell) → 1,400 W (B300, MI355X) → ~1,800 W (analyst-estimated Rubin Ultra). Liquid cooling becomes mandatory above ~1,000 W; air cooling effectively ends with Hopper.
- **HBM capacity has been AMD's persistent win** (192 → 256 → 288 GB, 2023–2025), while rack-scale coherent scale-up was NVIDIA's until AMD reached it with Helios in 2026.

## Why it matters

This is the vault's most complete single treatment of [[AI Accelerator Architecture]] and the first to place all six deployed architectures on shared axes. Its "bets" framing turns hardware comparison into a set of falsifiable design commitments rather than a spec-sheet contest, and its problem statement — that the shape of the matmul, not the chip, decides whether you are compute- or bandwidth-bound — is the hardware-side statement of the same law that [[Changyi Yang - Why MLA and MTP Fight Each Other]] derives analytically for attention. Together they anchor [[Arithmetic Intensity and the Roofline Model]].

## Tensions / open questions

- **Many headline figures are analyst-derived or era-inferred**, and the article marks these explicitly with an asterisk (Rubin, Rubin Ultra, MI455X, WSE-3 FLOPs, several power numbers). Anything dated 2026–2027 should be read as projection.
- **The comparison tables are not apples-to-apples and say so**: memory bandwidth is HBM for GPUs/TPUs/Trainium but aggregate on-chip SRAM for Cerebras and Groq, and "scale-up bandwidth" follows each vendor's own convention — per-chip aggregate, rack aggregate, or true bisection.
- Several vendors do not disclose the numbers that would settle the argument: Cerebras has never published batch sizes or per-system throughput, and TPU TDP is undisclosed throughout.
- The narrative treats the NVIDIA–Groq arrangement as an acquihire plus non-exclusive license; how much LPU determinism survives inside NVIDIA's product line is unresolved.
- Software remains the asymmetry the tables cannot show: the Cerebras compiler is a *kernel matcher* with static graphs only, no dynamic shapes, and no data-dependent control flow, and the Dutch national compute centre reports no 1:1 porting path from standard PyTorch.

## Affected pages

- [[AI Accelerator Architecture]]
- [[Anthropic]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Cerebras]]
- [[GPU Execution Model]]
- [[Groq]]
- [[Inference Serving Engines]]
- [[Jacob Peake]]
- [[LLM Inference]]
- [[NVIDIA]]
- [[Prefill-Decode Disaggregation]]
- [[Speculative Decoding]]

## Citations

- Raw capture: [[2026-08-25 Jacob Peake - AI Chip Architectures]]
- Canonical URL: https://www.jacobpeake.com/ai-chip-architectures
- The source page carries no publication date; 2026-08-25 is the capture date. Its most recent cited events are from mid-2026.
- Third-party measurements cited within: Artificial Analysis (Cerebras decode throughput), SemiAnalysis (Cerebras and Groq unit economics), SURF (Cerebras CS-2 practitioner evaluation).

## Raw capture

- [[2026-08-25 Jacob Peake - AI Chip Architectures]]

## Related pages

- [[Distributed Training Parallelism]]
- [[KV Cache]]
- [[Speculative Decoding]]
- [[Mixture of Experts]]
- [[ML Systems at Scale]]
- [[Inference Serving Engines]]
