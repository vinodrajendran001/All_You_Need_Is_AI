---
type: concept
created: 2026-08-25
updated: 2026-11-27
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
  - src-2026-11-11-cam-pedersen-derive-kernels
  - src-2026-11-15-anshuman-mishra-baseten-2000tps
  - src-2026-11-05-intelligentlearn-inference-trade-offs-part-1
  - src-2026-11-14-intelligentlearn-inference-systems-part-2
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

In Yang's attention-core estimates, DeepSeek-style MLA reaches ~256 FLOP/B at a single query and
Kimi K3's MLA layer ~192 FLOP/B, around the modeled H200 balance point of ~206 FLOP/B.
Taking S to 2 gives 512 and 384, moving the modeled work onto the compute side. MQA at
AI ≈ 70–100 has more theoretical arithmetic headroom. These are **QK/PV kernel-scope
calculations**, not measured end-to-end latency or proof that speculation is nearly free:
drafting, launches, cache traffic, and scheduling can still cost time.

Zyphra's *Compressed Convolutional Attention* (arXiv:2510.04476) reached the same conclusion independently and adds a second mechanism: **MLA also loses under tensor parallelism**, because the shared KV must be replicated per TP rank, giving back the reuse MQA had bought.

## Verification blocks raise intensity in dense layers, not necessarily in expert layers

[[Anshuman Mishra - I Reverse Engineered Baseten's 2000TPS Inference Engine]] qualifies the
`AI(S) ≈ S · AI(S=1)` rule above for mixture-of-experts models. For FP4 weights with a one-byte scale per
32 weights, one token position gives about **3.76 FLOPs per weight-byte** and seven positions about
**26.35**. An HGX B300 at **7.7 TB/s** and **4.5 PFLOPS** dense FP8 balances near **584 FLOPs/byte**, so
even a seven-position verification block stays far on the memory side.

The reuse argument holds only when positions read the same weights. Each DeepSeek-V4.1-Flash token picks
**6 of 384** experts. If all seven positions pick the same six, intensity stays at 26.35. If their
choices are disjoint (42 experts), it falls back to **3.76**. A hypothetical uniform independent router
touches about **40.08** experts, about **3.94** FLOPs/byte. Real routes can be correlated, so the true
value lies between these bounds and is not measured.

These are the author's illustrative calculations, not kernel timings. They imply that speculation's free
headroom in an MoE model depends on how correlated the experts chosen for neighbouring draft positions
are.

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

## A floor read off the kernel's own IR

[[Cam Pedersen - Don't Write Kernels, Derive Them]] computes speed-of-light from the compiler's IR
rather than from model dimensions. For a comprehension over affine views, the least memory traffic and
the tile that attains it are the **primal and dual of one linear program** (via Brascamp–Lieb); for
attention the dual tile is FlashAttention's blocks. A time floor adds launch cost, DRAM latency and an
occupancy term — "a roofline with latency, launch and occupancy terms".

Validated against hardware counters, it "never exceeds the measured time" on **24** GEMV-class and
epilogue kernels and reaches **0.76–0.93** of measured time on large RTX 3090 kernels, but only
**0.05–0.66 (median 0.38)** on the H200, "and we have no validated term for the gap". Two cautions
extend `## Where the model breaks down`: the **traffic-optimal tile does not win on time**, and as a
guide to which optimizations pay the floor "has been wrong as often as right". On the H200 a decode
step's traffic floor is only **0.16–0.29** of measured time — the opposite of the Cohere framing above,
where bandwidth is assumed to be the binding limit. All figures are first-party.

## Batching moves the weight operators, not the history operators

[[intelligentLearn - From Symptoms to Fixes - Part 1 - Start with the Machine]] derives the same H100 BF16 ridge this page uses: about **989 TFLOPS** ÷ **3.35 TB/s** ≈
**295 FLOP/byte**, from vendor datasheet constants. It states the October 9 correction above as a
rule: "There is one ridge, not one per phase". Prefill and decode operators sit at different points
on the same roofline and move with batch, context, and implementation. Only an operator can be
classified, not a phase.

Its batching table separates the two decode operators that this page treats together:

- **Weight-reading linear layers** reach about **B FLOP/byte** in BF16, so they touch the ridge only
  near **B ≈ 295**.
- **Attention over historical KV** stays near **8 FLOP/byte** under GQA 8:1 (about **1** for MHA),
  "about 37x below the ridge". It does not move with B, because each request reads its own history.

Both values match this page's attention-core table for single-token decode: `H_q / H_kv` for GQA,
here 64 query heads over 8 KV heads, and `1` for MHA. The conclusion matches [[Jacob Peake - AI Chip Architectures]]: batching restores weight
reuse, but long-context decode becomes KV-bandwidth-bound.

The part is also explicit about the accounting boundary. The 295 counts weight bytes only. Counting
activation and output bytes as NVIDIA's GEMM guide does, one 8192 × 2048 TP=4 weight shard reaches
only about **250 FLOP/byte at B = 295** and crosses nearer **B = 360**, and real kernels move the
crossover again. Summed operator inputs and outputs are not HBM traffic, because fusion, tiling, and
register reuse change it, with FlashAttention as the canonical case. Below the ridge, a kernel can be
latency-limited rather than bandwidth-limited, "so the roofline says what to investigate, not which
resource is saturated". That is consistent with the H200 traffic-floor result above, where bandwidth
explained only part of measured decode time. Precision moves the two coordinates differently. Full
FP8 raises the ridge to about **591** and leaves the crossing batch essentially unchanged. FP8
weights with BF16 compute keep the ridge at 295 and roughly halve the crossing batch, to **148**.

[[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]] applies the split to the batch-size decision. A larger batch helps only weight-reading
layers, and only while each added request's KV still fits. In its long-document case the memory
ceiling falls to about **14** requests per replica, far short of the batch that reaches the ridge,
while history attention stays at about 8 FLOP/byte. The FastDecode paper it reads splits the
transformer block along the same line. Its S-Part is the shared-weight layers that batch well, and
its R-Part is per-sequence attention over KV. Moving R-Part off the GPU relocates the pressure to
the interconnect, and at short sequences S-Part becomes the bottleneck again. All of
intelligentLearn's figures are modelled estimates, not measurements.

## Open questions

- Is the MLA/MTP conflict a hard architectural limit or a coincidence of current hardware balance points?
- Can a selective-GEMM operator close the gap that currently makes sparsity useful only on the latent path?
- As inference fragments across accelerators with wildly different bytes-per-FLOP ratios (Cerebras at ~1.3, GPUs near 0.002 — see [[Cerebras]] and [[Groq]]), does a single roofline framing remain useful, or does each architecture need its own?
- How correlated are expert choices across adjacent draft positions in real MoE traffic? That correlation decides whether a verification block's arithmetic intensity is closer to 26.35 or 3.76 FLOPs/byte in the worked example.
- What term explains the H200 gap? tang's traffic floor reaches only 0.16–0.29 of a decode step's measured time there, and removing launches did not close it.
- At what batch does a production linear-layer kernel actually cross the ridge? intelligentLearn's own estimates move from about 295 (weight bytes only) to about 360 (counting activations and outputs) for one H100 shard, and real kernels move it again.

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
- [[Anshuman Mishra - I Reverse Engineered Baseten's 2000TPS Inference Engine]]
- [[Cam Pedersen - Don't Write Kernels, Derive Them]]
- [[Mixture of Experts]]
- [[intelligentLearn - From Symptoms to Fixes - Part 1 - Start with the Machine]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]]
- [[intelligentLearn]]
