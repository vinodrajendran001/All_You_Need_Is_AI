---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-13-kim-helion-compile-time-heuristics
source_title: "Fast by Default: Compile-Time Heuristics for Helion Kernels"
source_author: "Caleb Min Sup Kim, Ethan Che, Jongsok Choi, Jason Ansel"
source_url: "https://pytorch.org/blog/fast-by-default-compile-time-heuristics-for-helion-kernels/"
tags:
  - source/summary
  - kernels
  - compilers
  - autotuning
  - pytorch
source_ids:
  - src-2026-11-13-kim-helion-compile-time-heuristics
status: active
---

# Fast by Default: Compile-Time Heuristics for Helion Kernels

## Summary

A PyTorch blog post on **Helion**, "PyTorch's domain-specific language (DSL) for performance portable
machine learning kernels". Helion has relied on autotuning: one kernel definition can lower into
"thousands of different Triton kernels", and the autotuner picks one by compiling and benchmarking
candidates, at a cost that is "*per kernel and per shape*". The motivating example: a team tuning a
single paged-attention kernel across **72** shapes spent **10 hours** in Helion's quick mode "and 25
at full effort".

The post introduces compile-time heuristics that read a kernel's device IR and dataflow and emit a
config directly, **without any autotuning**. The authors are explicit that the goal "is not to come up
with a better config than the autotuner" but "to add a point in the tradeoff space between
performance and wait time". All results are first-party, measured on NVIDIA H100 (and the heuristics
ship for H100 and B200 on the Triton backend).

## Key claims

### How the heuristics work

- **Classify, then apply a family heuristic.** Any matmul (for example `hl.dot` or `torch.baddbmm`)
  routes to the matmul heuristic; a reduction with no matmul routes to the reduction heuristic;
  everything else is pointwise. If extents are not all known at compile time, "no heuristic fires" and
  Helion falls back to its original default.
- **A shared resource estimate underneath.** A liveness analysis over the compiler IR estimates, for
  candidate block sizes, how many registers, how much shared memory and — on Blackwell — how much
  tensor memory one CTA needs. That yields **occupancy** (whichever budget runs out first decides it;
  a CTA needing six tenths of tensor memory gets one CTA per SM because two "would go over the tensor
  memory budget by 20%") and **register pressure** (whether the assembler will spill). The authors
  call this a hard prediction problem and the estimate "approximate".
- **Matmul knobs.** Shrink block size if the launch produces fewer CTAs than SMs; use as many pipeline
  stages as shared memory allows, but not so many that occupancy falls (three stages with two CTAs per
  SM can beat six with one); choose `num_warps` from **dynamic matmul work** — below four warps or an
  M block under 64, Triton emits the smaller synchronous MMA rather than `wgmma`/`tcgen05`, which can
  win when there is little matmul work — and from register pressure. A final feasibility pass is
  "mostly defensive".
- **Multiple matmuls** (attention, linear attention) are resolved by ranking dots: a loop-carried
  accumulator first, then dynamic matmul work, then output area; the top-ranked dot sets `num_warps`.
- **Reduction knobs.** A warp ladder from reduction width, residency against a per-SM CTA limit,
  spill avoidance, smaller blocks to buy residency without breaking coalescing on the stride-1 axis,
  and a **persistence** rule: when a row is provably read twice (RMSNorm), staying persistent may cost
  some spilling because "it saves the second trip to memory". Warps and blocks iterate to a fixed point.
- **Cheap.** Compile time with heuristics on versus off differs by "tens of milliseconds".

### Results with no tuning time (H100)

| Suite | Previous default | Heuristic config | Full autotune |
| --- | --- | --- | --- |
| Linear attention, 9 variants, 96 cells, vs hand-written FLA Triton | **0.52x** | **1.18x** fwd; **1.12x** with backward | **1.26x** |
| vLLM reduction kernels, 6 kernels, 153 cells, vs vLLM's CUDA/C++ | **0.58x** | **1.27x** | **1.31x** |
| 10 reduction kernels, 80 cells, vs `torch.compile` max-autotune | **0.27x** | **1.09x** | not run |
| 13 matmul families, 70 shapes, vs `torch.compile` max-autotune | **0.51x** | **1.88x** | not run |

- On the vLLM kernels, autotuning "buys only about **3%**" over the computed config.
- The highlights also state the heuristic is **2.13x** faster than the previous default on linear
  attention and **2.2x** on the vLLM kernels.
- The **1.88x** carries two caveats from the authors: comparisons are "not always apples-to-apples"
  because some PyTorch implementations materialize intermediates the Helion kernel fuses, and jagged
  HSTU attention regresses (old default **3.72x**, heuristic **3.27x**).
- The `torch.compile` baseline is forced onto its Triton backend (`max-autotune-no-cudagraphs`), so it
  is generated Triton, not cuBLAS.

### Seeding the autotuner helps early, not late

Helper heuristics also emit roughly **5–20** related configs to seed the autotuner. Over **38**
matmul and multi-matmul kernels, one shape each, full autotuning was run unseeded and seeded. Median
configs tried:

| Target | Unseeded / seeded |
| --- | --- |
| within 50% of best | 35.5 / **1.0** |
| within 25% | 103.5 / **2.5** |
| within 5% | 255.5 / **175.0** |
| complete search | 521.5 / **420.5** |

That is "35x fewer configs to reach something merely decent, 41x to get within 25%, but only 1.5x to
get within 5% and 1.2x to finish". Seeding "does not make the final config any better": replayed
winners land "within a fraction of a percent of each other".

## Why it matters

This is the vault's clearest measurement of what search actually buys in kernel tuning. On these
suites a static, resource-model-driven config recovers most of the autotuned result — and on the vLLM
kernels all but about 3% — which moves [[GPU Kernel Optimization]]'s open question about compilers
absorbing the ladder from argument to data. It pairs naturally with
[[Cam Pedersen - Don't Write Kernels, Derive Them]], which takes the opposite stance on the same
trade-off (search per chip because rules mis-transfer), and with
[[Ant Group and vLLM - Humming Quantized Inference Kernels]], whose default selection also uses device
heuristics with autotuning planned. For [[PyTorch]], Helion is a second compiler surface beyond
`torch.compile`, now competitive out of the box with hand-written Triton and CUDA on named suites.

## Tensions / open questions

- **Predicting another compiler.** Every budget depends on guessing what Triton keeps in registers,
  shared or tensor memory; "Plenty of it we get wrong."
- **Selected suites, one vendor.** Everything is evaluated on NVIDIA, with constants "tuned against
  these two chips"; other backends are untested.
- **Ratio arithmetic is not fully reconcilable from the capture.** On linear attention, 1.18x over
  0.52x would be about 2.27x, while the post reports 2.13x over the previous default; the post does not
  say how its headline ratios are aggregated or whether the 0.52x/1.26x chart is forward-only.
- **Narrow fire conditions.** No heuristic fires when extents are only known at runtime; the base
  default is then used, which the post's own numbers show is "very bad".
- **Tension with derivation-by-search.** Pedersen's tang paper reports that rules tuned on one chip
  "picked the wrong matmul schedule" on another and that best schedules flipped between runs; Helion's
  heuristics are tuned on H100/B200 only. Neither source tests the other's claim.
- The authors' own conclusion: full autotuning "remains the right call when you are shipping a fixed
  set of shapes and can pay for it once".

## Affected pages

- [[GPU Kernel Optimization]]
- [[PyTorch]]

## Raw capture

- [[knowledge-base/raw/sources/Fast by Default Compile-Time Heuristics for Helion Kernels]]

## Citations

- Canonical URL: <https://pytorch.org/blog/fast-by-default-compile-time-heuristics-for-helion-kernels/>
  (captured link carried a `utm_source=tldrai` parameter, removed here).
- **Author recovered.** The capture lists "Ebba Simpson". A read-only fetch of the canonical page on
  2026-11-20 shows the visible byline "By Caleb Min Sup Kim, Ethan Che, Jongsok Choi, Jason Ansel";
  "Ebba Simpson" appears only in the page's `author` meta tag, which looks like the publishing
  account. Only the byline was taken from the web; no figures were imported.
- Published November 13, 2026 per the capture (the page's `article:published_time` is
  2026-11-12T16:45 UTC, which is November 13 at +08:00); captured November 20, 2026. `source_id`
  uses the capture's publication date.
- All results are first-party PyTorch/Helion-team measurements.

## Related pages

- [[GPU Kernel Optimization]]
- [[PyTorch]]
- [[Cam Pedersen - Don't Write Kernels, Derive Them]]
- [[Ant Group and vLLM - Humming Quantized Inference Kernels]]
- [[Ebba Simpson - Introducing TorchTPU]]
- [[Linear Attention and Recurrent Memory]]
- [[Inference Serving Engines]]
- [[GPU Execution Model]]
- [[AI-Generated Kernels]]
