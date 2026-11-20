---
title: "Fast by Default: Compile-Time Heuristics for Helion Kernels"
source: "https://pytorch.org/blog/fast-by-default-compile-time-heuristics-for-helion-kernels/?utm_source=tldrai"
author:
  - "[[Ebba Simpson]]"
published: 2026-11-13
created: 2026-11-20
description: "TL;DR Helion now uses compile-time heuristics that analyze a kernel’s IR and dataflow to pick fast settings without slow autotuning. It classifies the kernel as matmul, reduction, or pointwise and..."
tags:
  - "clippings"
---
### Featured projects

### TL;DR

Helion now uses compile-time heuristics that analyze a kernel’s IR and dataflow to pick fast settings without slow autotuning. It classifies the kernel as matmul, reduction, or pointwise and chooses block sizes, warps, and stages, giving near-autotuned speed for free.

## Introduction

Helion, PyTorch’s domain-specific language (DSL) for performance portable machine learning kernels, relies heavily on autotuning for its performance. Autotuning time can be a major bottleneck: for example, a previous team tuning a single paged-attention kernel across 72 shapes spent 10 hours in Helion’s quick mode, and 25 at full effort. To address these issues, we’ve developed **a set of heuristics** that read a kernel’s IR and dataflow at compile time and emit a config directly, **without any autotuning**.

We classify kernels into broad families based on the operations they contain – matmul, reduction, or pointwise – and apply a family-specific heuristic to each. These families are intentionally general: the matmul heuristic, for example, looks for any kernel containing a matmul operation such as hl.dot or torch.baddbmm, not just standard m-n-k matrix multiplications. These are designed to be generic and apply broadly to custom kernels that users may write.

Highlights:

- **Autotuner Heuristics.** Our heuristics cover a large set of kernels, including GEMM, reductions, and even linear attention.
- **Linear attention.** Over 96 kernel-and-shape cells spanning nine linear-attention variants, the computed config beats the hand-written Triton in [Flash Linear Attention](https://github.com/fla-org/flash-linear-attention) (FLA) by **1.18x** in the forward pass, and by **1.12x** with backward included on H100. Overall the heuristic is **2.13x** faster than Helion’s previous no-autotune default on H100.
- **vLLM reduction kernels.** Over 153 kernel-and-shape cells across six production kernels on H100, the computed config is **1.27x** faster than vLLM’s own handwritten CUDA/C++ operators, and **2.2x** faster than Helion’s previous default.
- **The analysis itself is cheap.** Compiling a kernel with the heuristics on versus off differs negligibly (tens of milliseconds), which is lost in the noise of Triton compilation.

## Our Approach: Decide the Config at Compile Time

A single Helion kernel can lower into thousands of different Triton kernels. One definition covers block sizes, loop orders, indexing modes and pipelining strategies, but the autotuner has to choose which of those thousands to emit, by compiling and benchmarking many candidates. And this autotuning cost is *per kernel and per shape*, which multiplies the problem the more kernels, shapes, and hardware backends you want to support.

We compute the config at compile time instead of searching for it at tuning time. We read the device IR and record structural facts about it: which axes are tiled, which block sizes are tunable, which tiles are live at which part of the kernel, etc. A heuristic reads those facts and emits a config.

The point here is not to come up with a better config than the autotuner, which has the benefit of benchmarking potentially thousands of configs before selecting one. It is to add a point in the tradeoff space between performance and wait time.

![](https://pytorch.org/wp-content/uploads/2026/11/page-02-image-01.png)

Our heuristics serve two purposes. A primary heuristic emits the default config used when autotuning is disabled. When autotuning is enabled, helper heuristics generate roughly 5–20 related or alternative configs that seed the autotuner. The goals are different: the default config should perform well on its own, while the seeds should give the autotuner several promising starting points to speed up autotuning. In this blog, we’ll touch on both, but focus on the primary heuristic that gets emitted with autotuning off.

## How the Heuristics Work

A heuristic sets the values for various config knobs, which must be tuned carefully to achieve high performance and are normally picked by the autotuner. These include block sizes for each tiled axis, num\_warps, num\_stages, the L2 grouping, load eviction policies, and more.

We pick a heuristic by scanning the device IR for the operations a kernel contains. Any matmul routes to the matmul heuristic regardless of what else is in the kernel; a reduction with no matmul routes to the reduction heuristic; everything else receives the pointwise heuristic. If a kernel’s extents are not all known at compile time, no heuristic fires and Helion falls back to the original default.

Our heuristics all lean on the same underlying analysis, which estimates resource usage of the kernel. At any step of the kernel, the analysis determines: given a candidate set of block sizes, how many registers, shared memory, and — on Blackwell — how much tensor memory, one CTA needs at that moment.

To do this, we run a liveness analysis on the compiler IR and walk each graph to find where every value is last used, and guess where it will be placed in memory. This is a hard problem: we are trying to predict what Triton will keep in registers, what it will stage through shared memory, what it will materialize at all rather than fuse away. Sometimes it is easier to predict (e.g., we assume the output of an hl.dot will be placed in TMEM on B200), but the estimate is approximate.

![](https://pytorch.org/wp-content/uploads/2026/11/page-03-image-01.png)

Using this we can estimate things that matter for performance, such as:

- **Occupancy**: how many CTAs fit on an SM at once. Whichever space runs out first decides it, e.g., a CTA needing a tenth of the SM’s registers and a tenth of its shared memory, but six tenths of its tensor memory, gets one CTA per SM, since two CTAs would go over the tensor memory budget by 20% (0.6 x 2 = 1.2).
- **Register pressure:** Peak live registers spread over the threads we intend to launch tells us whether the assembler will be forced to spill.

These considerations inform the selection of different config knobs. We’ll illustrate this for the **matmul heuristic**:

- **block\_size:** If the launch produces fewer CTAs than the GPU has SMs, we shrink block size on a grid axis to produce more of them.
- **num\_stages:** More stages hide more load latency, so we want as many as shared memory allows. But stages can also accidentally lose occupancy: six of them might fit while eating the CTA’s entire shared-memory budget, leaving one CTA per SM, where three stages and two CTAs per SM is the better trade.
- **num\_warps.** Two things pull on this:
	- *Which instruction Triton emits.* Below four warps, or with an M block under 64, Triton uses the smaller synchronous MMA; otherwise it uses the big high-throughput one (wgmma on Hopper, tcgen05 on Blackwell). Usually we want the big one. But when there is little matmul work sometimes the better answer is many CTAs per SM running small MMAs that overlap each other’s loads. So we count **dynamic matmul work** (essentially counting the number of times the hl.dot will be executed dynamically) and choose based on that.
	- *Register pressure.* Warps divide the tile across more threads, so more warps means less pressure on each one. If the peak live state at the current count would spill, that argues for increasing warps.
- **Feasibility Check.** A final pessimistic pass over the whole kernel: add up tensor memory, shared memory and registers, and confirm the config can actually launch. The adjustments above already respect these budgets, so this is mostly defensive.

In the case where there are **multiple matmuls** in one kernel (for example for attention and linear attention), we run the matmul heuristic on each hl.dot and use those as the starting point. They may disagree: two dots can share one block-size knob — one dot’s N is frequently the next dot’s K — and there is only one num\_warps for the whole kernel.

To resolve these tradeoffs, we rank each dot by estimated importance: priority goes to any dot with a loop-carried accumulator, since that accumulator stays resident for the whole loop and its tile sets the kernel’s footprint; then its dynamic matmul work; then its own output area. Wherever two dots disagree about a knob, the higher-ranked one wins (for example num\_warps is set by the top-ranked dot alone).

The **reduction heuristic** works through a similar set of knobs:

- **num\_warps.** Three pressures here, pulling in different directions:
	- *Enough warps to do the reduction.* A wide reduction needs warps working on it, so a ladder off the largest selected reduction sets the starting point: 128 elements wants one or two warps, 16,384 wants many more.
	- *Residency.* More warps per CTA means fewer CTAs per SM (there is a per-SM CTA limit), so we also test fewer warps.
	- *Register pressure.* Adjust warps to not spill registers.
- **block\_size.** Fitting more CTAs per SM means potentially *smaller* tiles, so we shrink blocks back down to buy residency. The constraint is that an axis with stride 1 is the one carrying the coalesced loads, and shrinking it too far loses load coalescing.
- **Persistence.** A reduction can be kept resident and done in one pass, or walked in chunks. The case that matters is a row the kernel reads twice — RMSNorm reads it once to compute the scale and again to apply it — and when we can prove that, staying persistent is allowed to cost some spilling and some residency, because it saves the second trip to memory.

Because the warp count depends on the blocks and the blocks depend on the warp count, we iterate until both hold still for a full round (in practice this doesn’t take very long).

## Result 1: Config Quality, with No Tuning Time

### Linear attention

We measured nine linear-attention variants in forward and forward-plus-backward, over six production shapes, on H100. The six shapes span batch 1 to 8, 8 to 96 heads, sequence 1024 to 16384 and head dimension 64 to 256. The baseline is [Flash Linear Attention](https://github.com/fla-org/flash-linear-attention) (FLA), an open-source, widely used library of hand-written Triton kernels. The autotuned arm in the charts (“Helion AOT config”) is the result of running the full autotuner once per shape and saving the winner — how you would ship a Helion kernel for a known set of shapes today.

![](https://pytorch.org/wp-content/uploads/2026/11/page-06-image-01.png)

Before this work the choice was binary: take Helion’s no-autotune default and run at **0.52x** of handwritten FLA Triton, or spend GPU-hours autotuning and reach **1.26x**. The heuristic adds a third option that did not exist before: **1.18x**, with no autotuning price (most of what autotuning finds, available immediately) and it moves Helion’s out-of-the-box behavior from *losing* to handwritten Triton to *beating* it, at least for this set of kernels.

### vLLM’s reduction kernels

[vLLM](https://github.com/vllm-project/vllm) is a widely deployed open-source LLM inference engine, and it ships its own hand-written CUDA/C++ kernels for the operations on its serving hot path. There are six reduction kernels — two FP8 quantizers, RMSNorm and SiLU-and-multiply each fused with quantization, and fused QK-normalization plus RoPE– for which vLLM already had Helion implementations, contributed by the team behind [an earlier post in this series](https://pytorch.org/blog/portable-vllm-model-inference-kernels-in-helion/). That makes them a good test: production kernels, written by someone else, against the hand-written CUDA they were meant to replace.

![](https://pytorch.org/wp-content/uploads/2026/11/page-07-image-01.png)

And we get a similar result, in a different codebase. Helion’s no-autotune default runs at **0.58x** of vLLM’s CUDA; the computed config reaches **1.27x**; full autotuning gets to **1.31x**. The interesting number is the last gap: on these kernels autotuning buys only about **3%** over the config we compute for free.

### The everyday kernels, against torch.compile

Both comparisons above are specialist libraries — linear-attention variants and FP8 quantizers. This one is deliberately the opposite: the kernels everybody writes. RMSNorm, LayerNorm, softmax, cross entropy and friends, similar to the suite the [introduction post](https://pytorch.org/blog/helion/) benchmarked when it first measured Helion. Most of the kernels benchmarked in this section can be found [here](https://github.com/pytorch/helion/tree/main/examples).

The reference baseline here is torch.compile(mode=”max-autotune-no-cudagraphs”): we force torch.compile onto its Triton backend so we are not comparing against handwritten libraries (e.g.. cuBLAS) but instead against generated Triton from a widely-used compiler. There is no tuned-config arm in this section, for the mundane reason that we do not have full autotune runs for these kernels (which would take many GPU hours to produce).

On a suite of ten reduction kernels and 80 (kernel, shape) combinations, the computed config comes out at **1.09x** of max-autotune torch.compile, with no tuning of its own. Helion’s unseeded default is **0.27x**.

![](https://pytorch.org/wp-content/uploads/2026/11/page-08-image-01.png)

We also sweep across thirteen matmul kernel families over 70 shapes. The computed config comes out at **1.88x** of max-autotune torch.compile overall, against **0.51x** for Helion’s default. Two caveats on that 1.88x. The comparisons are not always apples-to-apples – for some of these kernels the PyTorch implementation materializes intermediates that the Helion kernel fuses. And jagged HSTU attention is a genuine regression: the old default happens to land on a good config there (3.72x) and the heuristic does worse (3.27x).

## Result 2: Does the Seed Make the Search Faster?

Everything above is about the config Helion emits when autotuning is *off*. But the same configs can be handed to the autotuner as its starting population, and in principle a good starting point should let the search finish sooner. In addition to this primary config, the helper heuristics also add somewhere between 5 and 20 new variations / approaches.

To test it we took 38 matmul and multi-matmul kernels — linear attention, attention, Mamba, and other wild cards like squeeze-and-excitation — and one shape for each kernel. Then we ran the full autotune effort on every cell twice: once from random configs, once with the compiler’s seeds in the initial population.

The short answer from this run is that **seeding buys a lot early but much less late**. Here is one cell, chosen as a clear example of the pattern. The x-axis tracks the number of configs tried, while the y-axis tracks performance relative to the best config we found.

![](https://pytorch.org/wp-content/uploads/2026/11/page-09-image-01.png)

Seeded, the *first* config is far superior to the unseeded first config. But unseeded quickly catches up, and they end up sitting on the same answer while the search grinds through several hundred more configs. The early advantage is enormous while the final advantage is zero.

That is the pattern across all 38 cells. Medians below; counts include configs that failed to compile or failed to produce a timing, since those consume budget too.

| Search target | Median configs (no seeds / seeded) |
| --- | --- |
| within 50% of the best found | 35.5 / **1.0** |
| within 25% | 103.5 / **2.5** |
| within 5% | 255.5 / **175.0** |
| complete search | 521.5 / **420.5** |

The advantage is concentrated entirely at the start: 35x fewer configs to reach something merely decent, 41x to get within 25%, but only 1.5x to get within 5% and 1.2x to finish the search.

One thing this result is not: seeding does not make the final config any better. Replaying both arms’ winners on one GPU, they land within a fraction of a percent of each other. This is about how long the search takes, not where it ends up.

## Limitations and Future Work

A central limitation is that these heuristics predict what another compiler will do. Every budget depends on guessing where a value ends up — registers, shared memory, or tensor memory — and that is Triton’s decision, not ours. Some of it is safe to bet on: on B200 a matmul result is going to be in tensor memory. Plenty of it we get wrong. There are several possible directions of future work.

**Measure instead of predicting.** The cleanest fix for the limitation above is to stop guessing: compile once, read the register and shared-memory usage the assembler reported, and correct the estimate from there.

**Fire on more kernels.** We currently decline whenever we lack the information to size anything — a loop tiled over a range only known at runtime, for instance. A less-educated guess would be easy: a default extent, a mean, something. Configs would be worse without that information, but the alternative today is the base default, which the results above show is very bad — so the guess is probably still worth making.

**Touch more knobs.** We set block sizes, num\_warps and num\_stages, plus some L2 grouping and L2 eviction policy. That leaves a long list untouched — tensor descriptors versus pointer arithmetic, persistent versus flat launch, etc. Individually these are probably worth less than the ones we do set, but there is certainly performance left on the table.

**Specialize the heuristics.** They are deliberately general: one multi-matmul heuristic has to do well on attention *and* linear attention, one reduction heuristic on RMSNorm *and* vLLM’s quantization kernels. An alternative is parent heuristics with children — a vLLMQuantizationHeuristic that starts from ReductionHeuristic’s answer and then specializes on what it knows about that family.

**Other backends.** Everything here is evaluated on NVIDIA, and the heuristics ship enabled for H100 and B200 on the Triton backend. Nothing in the approach is NVIDIA-specific — the analysis is parameterized by hardware limits that should apply across backends — but the constants and ladders were tuned against these two chips.

## Conclusion

These heuristics are merged into Helion and enabled by default on H100 and B200 with the Triton backend. If you would like to learn more, please check out the [autotuner heuristics](https://github.com/pytorch/helion/tree/main/helion/_compiler/autotuner_heuristics).

The point is not that static analysis beats search, but rather that the gap is now small enough that skipping the search is a reasonable thing to do for some kernels. Helion’s out-of-the-box behavior went from 0.52x handwritten FLA Triton to 1.18x, and from 0.58x vLLM’s handwritten CUDA to 1.27x, with nothing compiled and nothing benchmarked. On a general suite of reduction kernels it sits at 1.09x torch.compile max-autotune. Full autotuning remains the right call when you are shipping a fixed set of shapes and can pay for it once; what changed is that the alternative is no longer a large concession.