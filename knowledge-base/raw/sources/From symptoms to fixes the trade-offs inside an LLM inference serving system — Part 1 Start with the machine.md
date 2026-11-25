---
title: "From symptoms to fixes: the trade-offs inside an LLM inference serving system — Part 1: Start with the machine"
source: "https://medium.com/@wszjzhang/from-symptoms-to-fixes-the-trade-offs-inside-an-llm-inference-system-part-1-start-with-the-9aa825ca7969"
author:
  - "[[intelligentLearn]]"
published: 2026-11-05
created: 2026-11-25
description: "More"
tags:
  - "clippings"
---
Where the real trade-offs live, worked through with numbers you can check.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tJ99c5b8F-Jt9Q7x-fPRrw.png)

*From “Designing LLM inference systems”, the second half of a series on LLM inference serving. It follows* [*the opening piece on promises and measurements*](https://medium.com/@wszjzhang/what-good-inference-looks-like-promises-and-measurements-ac5a8b282df6)*, which ended with a chat service that starts taking long documents and asked what it should promise; this one starts there and asks what the machine has to do to keep the promise. It runs in four weekly parts: this is Part 1, and Parts 2 to 4 follow on November 10, 17 and 24. It assumes* [*the primer*](https://medium.com/@wszjzhang/how-llm-serving-works-from-one-request-to-a-gpu-cluster-e8785a90614b) *and reuses the six layers from* [*the six-layer map*](https://medium.com/@wszjzhang/the-six-layers-of-an-llm-inference-system-from-capacity-to-service-769a701aa278)*. The running case’s numbers are teaching assumptions and vendor datasheet constants; none of them is my own measurement.*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*EGZgUVT2Sk_Ay0VI.png)

The six layers, from the promise made to the consumer down to the GPUs that keep it. The layers divide responsibility; they are not stages every request passes through.

Imagine a chat service that starts accepting long documents. The model and GPU fleet stay the same, but the workload changes: some requests now arrive with tens of thousands of input tokens.

A document request may take a long time to produce its first token. An existing chat may instead start pausing between tokens. Both feel like a slow model to the user, but they can point to different bottlenecks. The first symptom may come from queueing or prompt processing; the second may come from a long prefill blocking decode, from state that has grown expensive to read, or from scheduling interference.

Several plausible fixes therefore answer different questions. A larger batch can improve weight reuse, yet leave less room for the state that grows with every active request. Separating prompt processing from token generation can reduce interference, but introduces state transfer and capacity-allocation decisions. Reusing a cached prefix can save computation while sending more work to an already busy replica. None of these actions is simply good or bad; each has to be matched to the symptom and workload.

To understand the serving stack, follow three things: **the computation a request performs, the state it keeps, and the time it spends waiting**. They constrain each other, but an improvement need not create an equal cost elsewhere: it may remove waste or add a cost, and either way it changes which constraint matters next. By the end, we should be able to take a serving symptom, locate the candidate problem in execution, state or scheduling, and say what to measure before choosing a remedy. The route runs from token and GPU fundamentals, through six intervention layers and a method for evaluating changes, to one worked long-document case.

This part follows the questions a reader meets in order: what creates the first token, why later tokens carry growing state, why peak GPU compute can remain unused, why batching helps only some operators, and what those limits mean for one concrete cluster. It is textbook background rather than corpus evidence; the vendor and reference sources it leans on are linked where they are used.

## 1\. What happens before the first token, and after it

**TTFT** (time to first token) runs from a request’s arrival to its first output token; the **token gap** is the spacing between later tokens. A request can be slow on either part of the timeline without being slow on both.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*og52LV-7kl8NNIr9VO71aw.png)

*Illustrative, not measured. TTFT and token gaps describe different parts of the same request timeline.*

> ***The three-ledger method — read every request three times, once per ledger.***

- **Operator ledger:** how much compute is done, and how many bytes move?
- **Memory budget:** how much weight and state — and how many concurrent requests — fit?
- **Request timeline:** is wall-clock time spent waiting, executing, transferring or blocked?

> *Counting only operators misses queueing and admission effects; counting only memory misses latency.*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*xi4GxjskC5d5LCh7mM1Ciw.png)

*Read every mechanism three times. Keep only the first ledger and offloading state looks free.*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HDaXKXlUnsKgXC3ycX1cWg.png)

*Before a change, identify the binding constraint; afterwards, read the three ledgers again.*

## Prefill produces the first token; decode produces the rest

An autoregressive model produces one token at a time. In the basic path used here, **prefill** runs the whole prompt through the model in one unchunked forward pass, as large matrix-matrix operations, and produces the first output token. Each **decode** step then consumes the latest token, produces the next one and appends its state; each request contributes one token per step, so the shapes are thin. If output length N includes the first token, generation is one prefill pass plus N−1 decode passes. Chunked prefill (Part II, section 6) spreads the prompt over several passes, and speculative decoding changes the decode count.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MBAW60F7LPBH2hNNzZnPkA.png)

*Prefill is one large shape; decode is N−1 thin steps after the first output token, in an unchunked, non-speculative baseline.*

The number of decode passes is set by output length, not input length. Their thin shape also offers little weight reuse at small batch; sections 3 and 4 make that statement quantitative.

## 2\. Why generation keeps state

Without a cache, each step would recompute the prefix. The KV cache instead stores every past token’s K and V at every layer, so a new token computes only its own K and V.

> *The KV cache trades* ***storing and reading historical state*** *for* ***repeated computation****. The new token’s full attention still visits an ever-longer history, so the cache does not eliminate attention’s growth with context.*

Fix model size and let S be current context length. The new token’s projections and FFN are essentially constant in S; full attention over its history grows linearly with S; stored historical KV also grows linearly with S. Thus generation inherits two different limits: **time to read history** and **capacity to store it**. The formula applies to standard autoregressive MHA/GQA, not unchanged to every architecture or cache policy. Part II relaxes those assumptions.

## 3\. Why a GPU can be underfilled

> *This section uses a* ***dense, autoregressive, full-attention decoder-only Transformer****. Unless stated otherwise, weights and KV are resident on the GPU, without speculative decoding, sliding windows or prefix sharing.*

## HBM feeds a much smaller on-chip hierarchy

Weights and KV normally reside in **HBM**, the GPU’s off-chip memory: 80 GB and 3.35 TB/s on an H100 SXM5. An operator moves data from HBM through much smaller on-chip tiers (L2, per-SM shared memory, registers), reusing tiles there before writing results back. If it moves many HBM bytes for little arithmetic, compute units wait for data and headline peak FLOPS remain unused.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GNKGP9oTeH_YYeE0rZeGbA.png)

*Capacity shrinks as locality and bandwidth rise. Shared memory and registers both support on-chip reuse, and the operand path depends on the instruction: Hopper’s* [*WGMMA*](https://docs.nvidia.com/cutlass/4.5.2/media/docs/pythonDSL/mma_docs/wgmma_programming.html) *reads matrix operands from shared memory and keeps accumulators in registers.*

## Kernels, fusion and tiling reduce traffic

A **kernel** is a GPU program launched once across many threads. **Fusion** can reduce both kernel-launch overhead and intermediate HBM traffic: separate kernels may write an intermediate to HBM and read it back, whereas a fused kernel can keep it on-chip. **Tiling** brings blocks through the hierarchy so each block is reused before eviction.

Therefore, **do not add operator inputs and outputs and call the sum actual HBM traffic**. Fusion, tiling, caching and register reuse change it. [FlashAttention](https://arxiv.org/abs/2205.14135) is the canonical case of nearly unchanged semantics with substantially different HBM access. The ledger gives magnitude and structure, not measured traffic.

## Weight reuse determines arithmetic intensity

**Arithmetic intensity** is FLOP/byte for a workload and implementation at a stated memory boundary. The **ridge point** is a hardware compute-to-bandwidth ratio at a stated precision and bandwidth convention. On the vendor figures used below, H100 SXM5’s BF16 dense ridge is 989 ÷ 3.35 ≈ **295 FLOP/byte**.

There is one ridge, not one per phase: prefill and decode operators sit at different points on the same roofline, moving with batch, context and implementation. Below the ridge, HBM bandwidth sets the lower roof in this model. A kernel can still be limited by too little parallelism, launch overhead or synchronization, which [NVIDIA’s performance guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html) calls latency-limited, so the roofline says what to investigate, not which resource is saturated.

## 4\. Why batching helps — and where it stops

Batching lets multiple requests reuse weights fetched for the same linear layer. It does not let one request reuse another request’s historical KV. The estimates below are idealized and operator-level: the linear-layer row counts only weight traffic, and the attention row counts historical K/V traffic with ideal reuse across grouped query heads.

**Weight-reading linear layers** — How arithmetic intensity moves with B: **rises with B**: about `B` FLOP/byte in BF16 when weight traffic dominates; magnitude on the input card: reaching the ridge at 295 needs B ≈ **295**

**Attention reading historical KV** — How arithmetic intensity moves with B: **does not move with B**: each request has its own KV; magnitude on the input card: about 8 FLOP/byte under GQA 8:1 (about 1 for MHA)

**Communication and scheduling overhead** — How arithmetic intensity moves with B: varies with parallelism strategy and request count; magnitude on the input card: outside this table’s convention, counted separately

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*pcPp1Yzu-SOTiOzhNeDLzw.png)

*Batching reuses weights across requests; it does not make any request’s history cheaper to read.*

Thus only the weight-reading linear layers can cross the ridge as B rises. Historical-KV attention remains near 8 FLOP/byte — about 37x below the ridge — because each request reads its own history. It is therefore too broad to call all of decode compute-bound after batching.

The 295 is a weight-only estimate, not a universal GEMM threshold. Counting activation and output bytes as well, as [NVIDIA’s GEMM guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) does, an 8192 × 2048 weight shard (one TP=4 slice) reaches only about 250 FLOP/byte at B = 295 and crosses the ridge nearer B = 360; real kernels move the crossover again.

Precision illustrates why the accounting boundary matters; under the same weight-only count, if weights, activations and matmuls all use FP8, FLOP/byte roughly doubles but H100 dense peak also roughly doubles to 1979 TFLOPS; the ridge rises to about 591, leaving the crossing batch essentially unchanged. If only weights are stored as FP8 while compute stays BF16, the ridge stays 295 and the crossing batch roughly halves to **148**. Likewise, INT4 weights occupy about a quarter of FP16 bytes, but attention, communication, sampling and framework overhead do not become four times faster.

## Tensor parallelism splits operators, not requests

BF16 weights for a 70B model are about 141 GB, too large for one 80 GB GPU. **Tensor parallelism** (TP) splits each operator across GPUs, cutting each GPU’s weight bytes and compute; the TP group acts as one replica, with each request’s KV spread across it. Every layer pays collective communication, so latency does not fall linearly with TP degree.

On the running case, TP=4 leaves each GPU reading roughly 35 GB of weights per step; at 3.35 TB/s that is about 10.5 ms. This idealized lower bound excludes KV reads, communication and kernel overhead.

## 5\. How large the limits are in the running case

The opening cluster becomes four questions:

1. Why is simply turning up batch size not enough?
2. When is colocated chunked prefill enough, and when is P/D disaggregation worth it?
3. Why does disaggregation force routing to be reconsidered?
4. When does a cache hit save less execution than the queueing it adds?

The walkthrough may end at “**needs measurement to decide**”. Its numbers are **teaching assumptions, not measurements**, and correspond to no real deployment.

**Model** — dense, autoregressive, decoder-only, 70B class; 80 layers, d\_model 8192, 64 query heads / 8 KV heads (GQA 8:1), head\_dim 128

**Precision** — BF16 for both weights and KV

**Hardware** — a single node of 8× H100 SXM5 80GB, NVLink within the node

**Deployment** — TP=4, two replicas on one node

**Original workload** — short chat: input ≈ 500 tokens, output ≈ 200 tokens

**New workload** — long document: input ≈ 32,768 tokens, output ≈ 512 tokens

**SLO** — TTFT P95 ≤ 2 s; P95 inter-output-token gap ≤ 50 ms

**Prefix reuse** — the same document is asked about over several turns, so long-document requests share reusable prefixes

The SLO names a quantity, a threshold and a percentile, and it takes the percentile over individual token gaps rather than an average. It leaves two parts of a promise open: the population, since one objective covers both short chats and long documents, and the failure behaviour, which Part II returns to at the contract layer (section 11).

The calculations below use a **cold-cache baseline**: each request processes its full prompt and holds its own copy of KV. The workload offers prefix reuse, but cache hits and shared KV blocks are left out of these estimates; Part II takes them up.

**Hardware constants** ([NVIDIA H100 SXM5 80GB datasheet](https://www.nvidia.com/en-us/data-center/h100/), **vendor spec, not my measurement**, checked 2026–09–14; dense Tensor Core value without sparsity): HBM bandwidth 3.35 TB/s and BF16 throughput ≈ 989 TFLOPS.

## KV capacity

For standard autoregressive GQA, KV bytes per token = `2 (K,V) × n_kv × head_dim × dtype_bytes × layers` = 2 × 8 × 128 × 2 B × 80 = 327,680 B = **320 KiB/token**.

Per GPU, 80 GB − 35.25 GB weights (141 GB ÷ TP 4) − roughly 5 GB activation/framework overhead leaves 39.75 GB; across four GPUs the replica has ≈ **159 GB** for KV. This derivation uses decimal GB (1 GB = 10⁹ bytes). Treating 159 as GiB would change the long-document ceiling from 14 to 15. The primer derives the same 320 KiB and 159 GB from the same input card.

**KV per request** — short chat (700 tokens): ≈ 0.229 GB; long document (33,280 tokens): ≈ 10.9 GB

**Concurrency ceiling from memory alone** — short chat (700 tokens): ≈ 690; long document (33,280 tokens): ≈ 14

Both ceilings are floored to whole requests; the short-chat floor is 693, shown as ≈ 690. They double at node level because the node has two replicas.

**\[Upload figure 7: export/wechat-png/k3-kv-budget.png\]**

*Without prefix sharing, KV at 320 KiB/token grows linearly with context; batching cannot recover that capacity.*

Context grows **47.5x** and the ceiling falls by roughly the same factor (690 → 14, about 49x after flooring). This is only a capacity ceiling: scheduling, latency targets and bursts push achievable concurrency lower.

## Prefill sensitivity

For 32,768 input tokens, the weight term ≈ `2 × parameters × tokens` ≈ **4.6 PFLOP** and causal-attention term ≈ `2 × S² × d_model × layers` ≈ **1.4 PFLOP**, totaling ≈ **6.0 PFLOP**. TP=4 has a BF16 dense peak near 3.96 PFLOPS. At an assumed 40% of peak (**a teaching assumption; I did not find a citable reference for it**, and actual efficiency depends strongly on implementation, shape and parallelism), prefill takes about **3.8 s** wall clock on the replica—about 15 GPU-seconds across four GPUs if TP scales perfectly. Using the unrounded FLOP counts above, finishing within 2 s would require ≈ **76%** of dense peak. The 40% assumption therefore leaves this cold request's prefill alone above the two-second threshold, and the 76% leaves no budget for queueing or other overhead. Whether the service meets P95 TTFT ≤ 2 s has to be evaluated over the defined request population, not inferred from this one request. This is a sensitivity result, not a production measurement: **first test isolated-request execution feasibility on an empty system, then investigate queueing and colocation interference.**

Attention’s share of prefill compute rises from about **0.5%** at 512 tokens (close to the 500-token short input) to about **23%** at 32,768, so its importance depends on context length.

The first decision, then, is not which optimization to enable but which limit binds. For the long-document workload, separate cold-request execution time, resident-state capacity and waiting time first. These estimates narrow the search; they do not choose a serving configuration. Part II looks at what each layer can change, and what each change costs.