---
type: concept
created: 2026-08-25
updated: 2026-08-26
tags:
  - concept
  - arithmetic-intensity
  - roofline
  - inference
  - hardware
source_ids:
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-07-03-fergus-finn-cuda-kernel
  - src-2026-06-26-nithin-llm-inference
  - src-2026-07-06-mayank-pratap-singh-speculative-decoding
  - src-2026-08-23-wafer-ai-performance-engineering-resources
status: active
---

# Arithmetic Intensity and the Roofline Model

## Definition

**Arithmetic intensity** (AI) is the ratio of arithmetic performed to bytes moved across the memory boundary, usually expressed in FLOPs per byte. The **roofline model** plots achievable performance against arithmetic intensity: below a hardware-specific balance point — the *ridge* or *knee* — a kernel is memory-bandwidth-bound and adding compute buys nothing; above it the kernel is compute-bound and adding bandwidth buys nothing.

The balance point is a property of the chip, not the model. Roughly **295 FLOP/byte on an H100 under BF16**, about **206 FLOP/byte on an H200**, with H100 and B200 in the two-to-three-hundred range.

## Why it matters

Arithmetic intensity is the single number that explains why so many independently developed techniques in this vault converge. It tells you which resource is actually scarce, and almost every inference optimisation is a trade that moves a workload along the roofline rather than a free improvement. Once you know where a workload sits relative to the knee, you can predict whether a proposed optimisation will help, do nothing, or actively cost latency — and two optimisations that each look good in isolation can be revealed as competitors for the same headroom.

## The core asymmetry: prefill versus decode

[[Jacob Peake - AI Chip Architectures]] states the hardware-side version: the *shape* of the matmul decides the regime.

- **Training and prefill** stack many tokens against the same weight matrix, so each layer is a large matrix-matrix multiply (GEMM) with high arithmetic intensity. These are compute-bound.
- **Decode** is autoregressive and emits one token at a time, so every matmul degenerates to a matrix-vector product (GEMV). Producing one token requires a full pass over every weight plus a full read of the [[KV Cache]]. Arithmetic intensity drops by orders of magnitude.

[[Changyi Yang - Why MLA and MTP Fight Each Other]] gives the analytic version for attention specifically: `AI_prefill ≈ (H_q/H_kv)·(L/b)`, i.e. the decode AI multiplied by the input length. Even plain MHA crosses the H100 line past roughly six hundred tokens, and GQA/MQA cross within a few dozen. **There is no memory-bound problem in prefill at all** — which is precisely why the whole MHA → GQA → MQA → MLA lineage exists: decode has exactly one query token and therefore no reuse to exploit.

## Attention variants are data-reuse engineering

The cleanest result in the vault on this point: for BF16 single-token decode, counting only the attention core's pass over the cached KV, the four attention structures collapse to one formula with a sliding KV-head count.

| Structure | Attention-core arithmetic intensity |
| --- | --- |
| MHA | `1` |
| GQA | `H_q / H_kv` |
| MQA | `H_q` |
| MLA | `~2 · H_q` |

Context length and head dimension cancel out completely; even MLA's latent dimension cancels. Two consequences follow:

- **Removing KV heads does not reduce FLOPs.** It reduces the history read from HBM, because one KV is reused by more query heads. GQA and MQA do not change prefill FLOPs whatsoever — they only shrink the cache and push an already-over-the-line AI higher.
- **MQA's ceiling is the query head count, and that number does not grow.** Architectures fix it at 32, 64, or 128, so piling on query heads cannot reach the few-hundred FLOP/byte balance point. MLA's extra factor of just under 2 comes from a different mechanism entirely: one latent serving as both K and V.

## The headroom is a shared, finite resource

This is the durable insight. A memory-bound decode leaves GPU compute idle, and **several unrelated techniques all spend that same idle compute**:

- **Batching** ([[LLM Inference]], [[Inference Serving Engines]]) promotes GEMVs back to GEMMs by stacking many users' decode steps. Under continuous batching each user still reads their own KV cache, so long-context decode shifts from weight-bandwidth-bound to **KV-bandwidth-bound**.
- **[[Speculative Decoding]] and multi-token prediction** stack K drafted tokens per request and verify them in one pass. Because HBM traffic barely grows with S while QK/PV compute scales nearly linearly, `AI(S) ≈ S · AI(S=1)`.
- **MLA** spends extra compute to buy stronger cache reuse.

The collision: DeepSeek-style MLA already reaches ~256 FLOP/B at a single query and Kimi K3's MLA layer ~192 FLOP/B — at or past the H200 balance point *before any speculation*. Take S to 2 and these become 512 and 384, sailing past the knee. **MTP's extra arithmetic is then no longer using otherwise idle compute; it starts costing real latency.** On a low-AI MQA workload at AI ≈ 70–100 the GPU is far from the knee and speculation is nearly free.

Zyphra's *Compressed Convolutional Attention* (arXiv:2510.04476) reached the same conclusion independently and adds a second mechanism: **MLA also loses under tensor parallelism**, because the shared KV must be replicated per TP rank, giving back the reuse MQA had bought.

## Sparsity flips the direction

The clean roofline story assumes attention reads *all* L cached tokens. DeepSeek-V3.2's DSA and GLM's equivalent break that premise with a selector that keeps only the top-k (`index_topk = 2048`). The effect is asymmetric: the MLA algorithm gathers latents by index so its cost goes from L to k, while the dense path must still expand the whole history for a GEMM because no selective GEMM operator exists. sglang's DSA backend threshold defaults to exactly 2048 — below it top-k selects everything and sparsity buys nothing.

## Where the model breaks down

- **AI is a predictor, not the objective.** Near the crossover a higher arithmetic intensity does not automatically mean a faster kernel. Zyphra puts it directly: "model quality and latency, not SM utilization, is the end goal."
- The clean constants assume a fused kernel and ignore softmax, projections, and output projection as lower-order terms.
- The balance points are generation-specific. A bandwidth-heavier future part moves the knee and with it every conclusion drawn against it.
- [[GPU Execution Model]] shows the micro-scale version and the same caveat: a low-intensity vector add runs at ~80% of DRAM bandwidth but only ~5% issue activity — the chip is starved by data movement, not arithmetic.

## Open questions

- Is the MLA/MTP conflict a hard architectural limit or a coincidence of current hardware balance points?
- Can a selective-GEMM operator close the gap that currently makes sparsity useful only on the latent path?
- As inference fragments across accelerators with wildly different bytes-per-FLOP ratios (Cerebras at ~1.3, GPUs near 0.002 — see [[Cerebras]] and [[Groq]]), does a single roofline framing remain useful, or does each architecture need its own?

## Related pages

- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Jacob Peake - AI Chip Architectures]]
- [[KV Cache]]
- [[Speculative Decoding]]
- [[LLM Inference]]
- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
- [[Inference Serving Engines]]
- [[Transformer Architecture]]
- [[Model Quantization and Efficiency]]
- [[Software Performance Engineering]]
