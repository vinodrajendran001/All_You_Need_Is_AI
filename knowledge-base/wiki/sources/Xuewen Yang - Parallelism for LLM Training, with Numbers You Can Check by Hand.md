---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-01-xuewen-yang-parallelism-by-hand
source_title: Parallelism for LLM training, with numbers you can check by hand
source_author: Xuewen Yang
source_url: https://xuewyang.github.io/posts/parallelism/
tags:
  - source/summary
  - distributed-training
  - llm-training
  - mixture-of-experts
source_ids:
  - src-2026-11-01-xuewen-yang-parallelism-by-hand
status: active
---

# Parallelism for LLM Training, with Numbers You Can Check by Hand

## Summary

Xuewen Yang's post works through data, ZeRO, tensor, sequence, context, pipeline and expert
parallelism with examples small enough to check by hand. For each one it shows what gets split,
what moves between GPUs, and when to use it. The running case is a 27B model on H200 GPUs. Its
contribution is less a new technique than a set of calculations: memory per GPU under each ZeRO
stage, activation bytes per layer, pipeline bubbles, expert all-to-all volume, and the longest
sequence that fits on one or two nodes. It closes with rules of thumb that follow from the
communication patterns. It also gives a worked "parallel folding" example showing how attention and
MoE layers can use different layouts over the same GPUs.

## Key claims

### Memory sets the problem, and activations are as large as the model state

- Mixed-precision Adam needs about **16 bytes per parameter**, so a 27B model needs **432 GB**
  before any activation, against **141 GB** on one H200.
- On 8 GPUs, ZeRO-1/2/3 cut model state per GPU to **148.5 / 101 / 54 GB**. ZeRO-1 and ZeRO-2 add no
  traffic. ZeRO-3 (the same idea as FSDP) moves about **1.5x** the bytes of plain data parallelism.
  Megatron's `--use-distributed-optimizer` is presented as a ZeRO-1 equivalent.
- One 4K-token sequence needs about **293 GB** of activations with naive attention and about
  **51 GB** with FlashAttention, so activations are on the same scale as model state. ZeRO does not
  help, because every GPU still runs every layer. Recomputation keeps only each layer's input for
  "about a third more compute".

### Tensor, sequence and context parallelism

- Tensor parallelism (TP) needs **4 all-reduces per layer** on the critical path, so it belongs
  inside an NVLink node. With grouped-query attention, **8 KV heads at TP = 16** force each KV head
  to be replicated on two GPUs.
- Sequence parallelism (SP) costs the same bytes on the wire as TP and splits what TP cannot: TP8
  alone leaves **13·sbh** activation bytes per layer, against about **4.25·sbh** with SP, about
  **3x** less.
- Context parallelism (CP) with ring attention passes only K and V; the online-softmax statistics
  never leave their GPU (worked check: softmax([1, 3]) = [0.119, 0.881]). Causal masking makes four
  CP ranks do **6% / 19% / 31% / 44%** of the work. Splitting into 2 × CP chunks and pairing each
  early chunk with its mirror balances them.

### Pipeline and expert parallelism

- Pipeline bubble = (p − 1)/(m + p − 1): **3/7 ≈ 43%** with 4 stages and 4 micro-batches, **16%** at
  m = 16 and **9%** at m = 32. With 8 stages, a bubble under 10% needs m = 64. Interleaved virtual
  stages cut the example from 3/7 to **3/11** at the cost of more point-to-point traffic.
- Expert parallelism (EP): at T = 4096, d = 7168, K = 8 and EP = 8 in BF16, one direction of the
  all-to-all is about **411 MB**, so about **0.8 GB per layer** in the forward pass, and backward
  doubles it. DeepSeek-V3 caps each token at **4 nodes** and dispatches in FP8 to cut that.
- **Parallel folding:** attention uses TP × CP × DP and MoE layers use ETP × EP × EDP on the same
  GPUs, with TP · CP · DP = ETP · EP · EDP. The post's worked example uses attention TP 2 and DP 4
  against MoE ETP 1, EP 8 and EDP 1 on 8 GPUs.
- **TP without SP doubles expert work.** With attention TP = 2 and SP off, both TP ranks hold the
  same tokens and both dispatch them. On a run with 4096 tokens per TP group and K = 8, that is
  **65,536** token copies per MoE layer instead of **32,768**, and twice the expert FLOPs. Megatron
  raises an error for this case, as a performance guard rather than a correctness rule.

### Rules of thumb

The post lists six: TP inside a node; SP whenever TP is on; CP when sequences get long; PP across
nodes with enough micro-batches; ZeRO-1 over DP "almost always"; and for MoE, expert TP of 1 with
enough EP, inside a node if possible.

### The longest sequence that fits

The post states its assumptions: BF16, FlashAttention, one sequence per micro-batch, about 120 GB
usable per GPU, and a distributed optimizer. Under them, the 27B model fits about:

| Nodes | Layout | Max sequence |
| --- | --- | --- |
| 1 | TP8 | ≈ 13K |
| 1 | TP8 + SP | ≈ 40K |
| 1 | TP8 + SP + full recomputation | ≈ 310K (about 450K with a chunked loss) |
| 2 | TP8 + SP, DP2 | ≈ 53K |
| 2 | TP8 + SP + PP2 | ≈ 59K |
| 2 | TP8 + SP + CP2 | ≈ 105K |
| 2 | TP8 + SP + CP2 + full recomputation | ≈ 820K |

- **PP does not buy length.** Under 1F1B the first stage holds activations for all layers. DP adds
  GPUs but only its ZeRO savings help. Across nodes, CP is what doubles length.
- **Fitting is not the same as fast.** At 310K tokens one sequence needs about **2.9 × 10¹⁷**
  attention FLOPs, roughly **1.5 minutes** on 8 H200s at 40% utilization. "Long-context training
  usually runs out of time before it runs out of memory."
- For scale, Megatron-LM's 8.3B GPT-2 used 8-way TP × 64-way DP on 512 V100s. DeepSeek-V3 trained a
  671B MoE with **no TP**: PP16 × EP64 × ZeRO-1, with DualPipe hiding the expert all-to-all.

## Why it matters

The post makes [[Distributed Training Parallelism]] checkable. Several of the vault's qualitative
claims become numbers: the 16-bytes-per-parameter budget, why TP stays in a node, why SP pairs
with TP, and why causal CP needs load balancing. Its MoE section adds the EP traffic estimate and
parallel folding to [[Mixture of Experts]], plus a concrete failure mode: TP without SP silently
doubles expert work. It complements [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]],
which measures EP across nodes rather than deriving it. The same handbook warns, for example, that
EP16 across two nodes ran well below EP8 inside one.

## Tensions / open questions

- **Estimates, not measurements.** The author says the numbers are "good to maybe ±30%". Temporary
  buffers, grouped-query attention, SwiGLU MLPs and MoE layers change the coefficients. No run
  validates the sequence-length table.
- **One model, one GPU type.** Everything is worked for a 27B model on H200s with stated assumptions
  (about 120 GB usable per 141 GB GPU). The ratios transfer better than the absolute numbers.
- **Ring attention only.** Context parallelism is covered through ring attention. The vault's
  [[Distributed Training Parallelism]] page also records DeepSpeed-Ulysses, which uses an all-to-all
  to turn sequence shards into head shards; this post does not discuss it.
- **The time ceiling is stated, not resolved.** The 1.5-minute attention estimate shows why
  long-context training is slow, but the post gives no guidance on trading length for throughput.
- The capture uses CRLF line endings and has frontmatter with author, URL and dates; nothing is
  missing.

## Affected pages

- [[Distributed Training Parallelism]]
- [[Mixture of Experts]]

## Raw capture

- [[knowledge-base/raw/sources/Parallelism for LLM training, with numbers you can check by hand]]

## Citations

- Canonical URL: https://xuewyang.github.io/posts/parallelism/
- Byline: Xuewen Yang (personal blog).
- Published: 2026-11-01. Captured: 2026-11-08.
- The post cites Megatron-LM, Korthikanti et al., Ring Attention, GPipe and successors, ZeRO,
  GShard, Switch Transformer and DeepSeek-V3 as the papers it follows.

## Related pages

- [[Distributed Training Parallelism]]
- [[Mixture of Experts]]
- [[LLM Training Pipeline]]
- [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]]
- [[Edward Z. Yang - How to Parallelize a Transformer for Training]]
- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]]
- [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
- [[Arithmetic Intensity and the Roofline Model]]
