---
type: concept
created: 2026-08-25
updated: 2026-10-09
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
  - src-2026-09-08-cohere-megakernel-serving
status: active
---

# Arithmetic Intensity and the Roofline Model

## Definition

**Arithmetic intensity** (AI) is arithmetic performed per byte moved across a specified memory boundary, usually FLOPs per byte. The **roofline model** bounds performance by `min(peak compute, memory bandwidth * AI)`. Below the *ridge* or *knee*, the bandwidth ceiling is lower; above it, the compute ceiling is lower. A kernel can run below either ceiling because of utilization, launch, synchronization, or other costs.

The balance point depends on hardware, precision, and the chosen bandwidth/compute ceilings. The sources use roughly **295 FLOP/byte on an H100 under BF16** and **206 FLOP/byte on an H200**, with H100 and B200 in the two-to-three-hundred range. These are modelled boundaries, not measured utilization guarantees.

## Why it matters

Arithmetic intensity explains why apparently independent optimizations can compete for the same
headroom. It helps identify candidate bottlenecks and compare compute-for-memory trades, but does
not predict end-to-end latency alone. The achieved kernel behavior and the rest of the request
path still need measurement.

## The core asymmetry: prefill versus decode

[[Jacob Peake - AI Chip Architectures]] states the hardware-side version: the *shape* of the matmul decides the regime.

- **Training and prefill** can reuse weights across many token positions through large matrix-matrix operations (GEMMs). Sufficiently large operations often approach the compute side of the roofline; small chunks or other kernels may not.
- **Dense, unbatched decode** has narrow matrix-vector work (GEMV), often limited by weight and [[KV Cache]] traffic. Batching restores weight reuse across sequences, and attention kernels have their own reuse patterns; not every decode matmul is a GEMV.

[[Changyi Yang - Why MLA and MTP Fight Each Other]] models the attention core as
`AI_prefill ≈ (H_q/H_kv)·(L/b)` and estimates an H100 crossover at roughly six hundred tokens
for MHA, earlier for GQA/MQA. The assumptions omit projections and other costs. The October 9 lint
removes this page's earlier claim that prefill has no memory-bound problem: a scoped attention-core
estimate is not a universal classification of every prefill or decode workload.

## Attention variants are data-reuse engineering

The cleanest result in the vault on this point: for BF16 single-token decode, counting only the attention core's pass over the cached KV, the four attention structures collapse to one formula with a sliding KV-head count.

| Structure | Attention-core arithmetic intensity |
| --- | --- |
| MHA | `1` |
| GQA | `H_q / H_kv` |
| MQA | `H_q` |
| MLA | `~2 · H_q` |

Context length and head dimension cancel out completely; even MLA's latent dimension cancels. Two consequences follow:

- **At fixed query heads, fewer KV heads need not reduce the QK/PV attention-core FLOPs.** They reduce history bytes read from HBM because query heads share KV. This statement excludes K/V projection and other work; it is not a claim that total prefill FLOPs are unchanged.
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

## Primary sources for the model

[[Wafer - AI Performance Engineering Resources]] places this page's material at the foundation of its learning path and supplies the primary citations the vault had been reasoning from second-hand. The roofline model originates in Williams, Waterman, and Patterson's *Roofline: An Insightful Visual Performance Model for Multicore Architectures*; the transformer-specific application — deriving arithmetic intensity from model dimensions, batch size, and sequence length — is set out in kipply's *Transformer Inference Arithmetic*, which that list treats as the entry point for reasoning about a model's own compute-to-bandwidth ratio before touching any hardware.

The list also makes the model's practical consequence explicit: it is the tool that tells you *which* optimization to reach for. A memory-bound decode is not made faster by a better GEMM kernel, and a compute-bound prefill is not made faster by compressing the KV cache. Every entry in its optimization section is indexed by which side of the ridge point it moves. That is also where [[GPU Kernel Optimization]] begins — the ladder of transformations there is a sequence of moves along this roofline.

## Reporting decode as a percentage of speed-of-light

[[Cohere - North Mini Code Megakernel Serving Engine]] frames its entire result against an explicit roofline rather than against a
baseline, which makes the remaining headroom legible.

**The calculation:** at BF16 the model streams **6.6 GB of weights per decode step** plus roughly **0.5 GB
of KV cache at 8K context**; an H100 at **3.35 TB/s** therefore caps decode at about **470 tok/s**. The
megakernel reaches **292 tok/s = 62% of that ceiling**, against vLLM's **185 tok/s = 39%**.

Stating results this way is more informative than a speedup ratio: it says both how much was gained and
how much is left. It also identifies **four distinct sources of the gain**, only one of which is the
expected launch-overhead saving: reduced launch and synchronisation overhead; **wave quantisation** (a
partial wave backfilled with unrelated work); **dropping false dependencies** (with per-task counters the
O-projection for a KV group starts as soon as *that group's* attention lands); and **weight prefetch**
(weights are immutable, so weight tiles stream before activation dependencies resolve — visible in the
code as `prefetch_weight_tiles` above `wait_input_bars`).

**The bound weakens as batch size rises**, since arithmetic intensity increases and the memory-bandwidth
limit that motivates the technique loosens. The reported ceiling of batch 8 means this is untested exactly
where the roofline argument would start to change.

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
- [[Wafer - AI Performance Engineering Resources]]
- [[GPU Kernel Optimization]]
- [[Prefill-Decode Disaggregation]]
- [[Serving Benchmarks and Goodput]]
- [[Wafer]]
- [[Cohere - North Mini Code Megakernel Serving Engine]]
- [[Megakernels]]
- [[Cohere]]
