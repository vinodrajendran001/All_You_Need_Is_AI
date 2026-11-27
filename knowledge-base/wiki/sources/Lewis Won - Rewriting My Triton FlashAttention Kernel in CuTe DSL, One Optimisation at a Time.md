---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-15-lewis-won-triton-to-cute-flashattention
source_title: "Rewriting My Triton FlashAttention Kernel in CuTe DSL, One Optimisation at a Time"
source_author: Lewis Won
source_url: https://dev.to/lewis_won/rewriting-my-triton-flashattention-kernel-in-cute-dsl-one-optimisation-at-a-time-1dnm
tags:
  - source/summary
  - kernels
  - gpu
  - attention
  - benchmarking
source_ids:
  - src-2026-11-15-lewis-won-triton-to-cute-flashattention
status: active
---

# Rewriting My Triton FlashAttention Kernel in CuTe DSL, One Optimisation at a Time

## Summary

Lewis Won had tuned a FlashAttention-2 (FA2) forward kernel in Triton until it matched PyTorch's
`scaled_dot_product_attention` (SDPA) on his RTX 4070 SUPER. He now ports it to NVIDIA's **CuTe
DSL**, "a Python library for writing kernels at the level of CUTLASS". He reads Triton's GPU-level
IR (TTGIR) and SASS to list what Triton decided automatically, starts from a port without those
decisions, and adds them back one round at a time, profiling each round. The final kernel ties or
slightly beats Triton and beats SDPA on every tested shape. Two schedules that Triton's `tl`
language cannot express are both slower on this card. The durable content is a measured inventory
of what a tile compiler does for a kernel author, plus a benchmarking protocol that records clock
and power. All results are self-reported on one consumer GPU.

## Key claims

### Triton's automatic decisions are most of the performance

The straight port (v0) keeps Triton v5's algorithm but uses "the simplest thing that works" for
everything else. At N = 4096, non-causal, it takes **5.436 ms (25.3 TFLOP/s)**, against **1.968 ms
(69.8)** for Triton v5 and **2.158 ms (63.7)** for SDPA, and in the harness it is **2.5–2.8× slower**
than both. Its tensor cores run at **33.7%** of peak, against **88.9%** for SDPA and **87.4%** for
Triton v5, while L1 and shared memory are 99% busy. Warps stall queuing shared-memory instructions
(MIO throttle) and waiting for their results (short scoreboard).

TTGIR and SASS show what Triton chose: four warps stacked along the rows, a swizzled shared layout,
**76 `LDSM`** (ldmatrix) instructions, `P` passed between the two multiplies by a layout conversion,
**32 `cp.async`** copies, and autotuned tiles and stages. Pinned at the same 64 × 64 tiles, 4 warps
and 2 stages, Triton uses 168 registers per thread and the Round 4 CuTe kernel 165, with the same
24,576 bytes of shared memory.

### Each round, with its mechanism

Figures are N = 4096, non-causal, unless stated. Harness and Nsight Compute figures are measured
differently and should not be compounded.

| Round | Change | Reported effect |
| --- | --- | --- |
| 1 | `Swizzle<3,3,3>` shared layout | bank conflicts **554 M → 0**; tensor cores 33.7% → 71.3%; harness **5.436 → 2.686 ms** (causal 2.997 → 1.324) |
| 2 | `ldmatrix` operand loads | **224 `LDS` + 64 `PRMT` → 40 `LDSM`** per pass; tensor cores 71.3% → 86.9%; harness 2.248 ms (causal 1.119) |
| 3 | `P` kept in registers | shared memory 32 KB → 24 KB; about **1%** (2.19 → 2.17 ms, Nsight Compute) |
| 4 | `cp.async`, FA2 copy order | tensor cores **93.2%** (2.04 ms, Nsight Compute); harness 2.100 ms (causal 1.040) |
| 5 | tile/stage sweep, K/V ring | **4%** over v4 at N = 512 non-causal, **0–2%** at N ≥ 1024; one digit lost (0.038 → 0.039 ms) at N = 512 causal |

- **Swizzle.** A 64-wide bf16 row is 128 bytes, exactly the 32 four-byte banks, so column 0 of every
  row sits in bank 0 and operand loads over 8 rows collide 8 ways. Storing chunk c of row r at
  position c XOR (r mod 8) spreads those reads over 8 bank groups. Registers jumped from 118 to 253,
  "most likely" from precomputed swizzled addresses.
- **ldmatrix** reads four 8 × 8 tiles per warp-wide instruction and hands each lane the values the
  tensor-core multiply wants, transposing V on the way. Load/store-pipe use falls 72.5% → 26.0%.
- **P in registers.** The first multiply's output layout lines up with the second's input layout,
  so the bf16 accumulator is re-viewed as an operand without moving data. The gain is small because
  the round trip "was already conflict-free".
- **cp.async** copies global to shared memory without a register. v4 loads V for block j during
  S = QKᵀ and K for block j + 1 during the softmax, reaching parity with Triton v5's 92.2%
  (64 × 128 tiles, 2 stages) at the same fixed clock.
- **Sweep.** Shared memory is capped at 99 KB per block, `2·D·(bM + 2·S·bN) ≤ 101,376` bytes. Three
  64 × 64 stages (56 KB) leave room for one block per SM: **58.1 TFLOP/s** against **70.8** with one
  stage. The resulting table uses 64 × 32 tiles with 3 stages at N = 512, and 64 × 64 tiles with 1
  stage (non-causal) or 2 (causal) at N ≥ 1024.

### Ownership and occupancy

Stacking warps along rows (`(4, 1, 1)`) keeps each row of the score tile in one warp, and
`mma.m16n8k16` gives each row to one quad of 4 lanes. The online softmax's row maximum and sum
therefore need two register shuffles, where `(2, 2, 1)` would send them through shared memory on
every key block. Registers set residency: at 168 per thread, 3 blocks fit per SM (shared memory
would allow 4), "the 25% theoretical occupancy Nsight Compute reports". Registers are allocated in
steps of 8, so 165 and 168 land in the same band and "make no measurable difference". The author
adds that "a kernel limited by the tensor cores does not need many" resident warps.

### Final comparison and the fair-fight protocol

Harness medians at N = 4096 (10 runs for CuTe v5 and Triton v5, 3 for NVIDIA's example, 35 for
SDPA):

| Kernel | Non-causal | Causal |
| --- | --- | --- |
| CuTe v5 | 1.991 ms, 69.1 TFLOP/s | 1.029 ms, 66.8 TFLOP/s |
| Triton v5 | 1.968 ms, 69.8 TFLOP/s | 1.079 ms, 63.7 TFLOP/s |
| SDPA | 2.158 ms, 63.7 TFLOP/s | 1.118 ms, 61.5 TFLOP/s |
| NVIDIA's CuTe example | 1.950 ms, 70.5 TFLOP/s | 1.038 ms, 66.2 TFLOP/s |

Over 8 shapes, CuTe v5 beats SDPA on all, is **2–5% faster than Triton v5 on 5 and ties on 3**, and
NVIDIA's example lands within 4% of it everywhere. At a fixed 2.52 GHz, v5 reaches **93.2%** of
tensor peak against 92.2% for Triton v5 and 88.9% for SDPA, using 165 registers and 24.6 KB of
shared memory against 255 and 41.0 or 49.2 KB.

The author then asks "Was it a fair fight?", since "A kernel at a lower clock looks slower for
reasons unrelated to its code". A separate script runs each kernel back to back for 4 s, interleaved
over 3 rounds with 30 s cool-downs, sampling every 10 ms (SM clock, power, power-cap share and
temperature). CuTe v5 and Triton v5 ran at median clocks within 1.1% at every N, and no run showed a
thermal slowdown. At N = 4096 both sat at the power cap in 93–98% of samples. CuTe v5 stayed 4–5%
faster causal at N ≥ 1024, and at Triton tile sizes doing the same causal work Triton was still
3.9–4.1% slower. The author's likely cause is leaner compiled code, **350 instructions per key
block against 388**, "which `tl` gives no control over"; none of Rounds 1–5 is CuTe-only.

### Beyond `tl`: two schedules that did not pay on sm_89

The tensor-core floor is `t_min = operations / (512 · 56 · f_SM)`. At sustained median clocks it is
**1.815 ms** non-causal and **0.912 ms** causal, against v5's **1.954** and **1.037 ms**. The Round 6
table lists a wave tail of 1.9% non-causal and none causal: 2,048 blocks make 12.19 waves, and at
exactly 8 waves v5's throughput is 1.9% higher. Two bitwise-identical candidates were both slower. **Per-buffer mbarriers** cost
+2.4% non-causal and +7.0% causal, because on sm_89 an mbarrier wait is a polling loop with 25–33%
more instructions; CuTe DSL 4.8.1's own mbarrier helpers refuse sm_89. **Software pipelining** cost
+2.1% and +2.8%, because other warps already fill those gaps. Warp specialisation works on sm_89 in
neither `tl` nor **Gluon** (`triton.experimental.gluon`, shipped with Triton 3.6), which always emits
the Hopper/Blackwell instruction `setmaxnreg`. Gluon does compile the other two schedules: "That is
beyond `tl`, not beyond Triton." The conclusion is scoped: "On this card, scheduling beyond `tl`
does not pay."

### Correctness and the hand-written checklist

The harness and tests are byte-for-byte copies of the previous article's, with published checksums,
and every version passes the unchanged test file.
The fp32 inputs are rounded to fp16, which, unlike Triton's TF32, overflows above 65,504. The author
also reports an apparent CuTe DSL 4.8.1 bug: under a swizzle, one indexing form returns block 0's
values for blocks 1–3; his kernels avoid it. His ten-item checklist of what Triton decided includes
"a wrong order is a race, not a slowdown", "a wrong answer can still be fast", and "Interleave, cool
down, and record clock, power and throttle reasons next to every time."

## Why it matters

[[GPU Kernel Optimization]] gains a one-decision-at-a-time account of what a tile compiler
contributes, and a qualified answer to whether hand-written kernels still win. [[GPU Execution Model]]
gets a compute-bound counterpart to its vector add. [[Arithmetic Intensity and the Roofline Model]]
gets a compute-side floor that moves with the clock. [[NVIDIA]] and [[PyTorch]] appear as the CuTe
DSL publisher and the SDPA baseline. [[Software Performance Engineering]] gains a clock- and
power-aware protocol, and [[Transformer Architecture]] gets FA2's work partitioning made concrete.

## Tensions / open questions

- Self-reported by one author on one consumer GPU (RTX 4070 SUPER, sm_89, 56 SMs, 220 W cap), for
  D = 64, B = 4, H = 8 and the forward pass only. The vault has not re-run the linked results, and
  Hopper or Blackwell, where the missing features exist, are not tested.
- Margins sit near the noise. Non-causal N = 4096 times "jump between two speeds for every kernel"
  (CuTe v5 1.92–1.95 or 2.03–2.10 ms). In the sustained table, 1.946 against Triton's 2.119 ms is
  still called a tie, and there Triton trails SDPA (2.021 ms), reversing the harness order. The
  harness also calls N = 512 causal a tie at 0.039 against 0.042 ms.
- Triton v5 is profiled at 64 × 64 (register comparison), "64 × 32 tiles there" (Round 0, 87.4%) and
  64 × 128 (Round 4 and final, 92.2%), so per-round comparisons do not share one Triton setting.
- Nsight Compute fixes the clock, so its "durations are not wall-clock speeds"; round gains from the
  two measurements cannot be summed.
- Causes stated as likely, not isolated: the causal advantage, the 253-register jump, and the
  165-vs-168 difference ("I did not look into why"). The CuTe DSL bug has a repro but no captured
  NVIDIA confirmation. The SDPA backend is not stated.
- The author says the article "was written with the assistance of AI". The earlier Triton article is
  not in the vault and its link is a placeholder, so Triton v5's design is known only from here.

## Affected pages

- [[GPU Kernel Optimization]]
- [[GPU Execution Model]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[NVIDIA]]
- [[PyTorch]]
- [[Software Performance Engineering]]
- [[Transformer Architecture]]

## Raw capture

- [[knowledge-base/raw/sources/Rewriting My Triton FlashAttention Kernel in CuTe DSL, One Optimisation at a Time]]

## Citations

- Canonical URL:
  <https://dev.to/lewis_won/rewriting-my-triton-flashattention-kernel-in-cute-dsl-one-optimisation-at-a-time-1dnm>
- By Lewis Won, published on DEV (dev.to) on November 15, 2026; captured November 27, 2026. Byline
  and dates come from the capture's frontmatter.
- Code and result files are in the author's GitHub repository
  `searlion/cs336-2026-assignment2-systems`, linked throughout but not separately captured.
- The link to the author's previous Triton article is a placeholder
  (`todo-dev.to-url-of-the-follow-up-article`), so that article cannot be cited. DEV's promotional
  footer is excluded.

## Related pages

- [[GPU Kernel Optimization]]
- [[GPU Execution Model]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[NVIDIA]]
- [[PyTorch]]
- [[Software Performance Engineering]]
- [[Transformer Architecture]]
- [[Cam Pedersen - Don't Write Kernels, Derive Them]]
- [[Caleb Min Sup Kim et al - Fast by Default - Compile-Time Heuristics for Helion Kernels]]
- [[Ant Group and vLLM - Humming Quantized Inference Kernels]]
- [[Wafer - AI Performance Engineering Resources]]
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]]
- [[MoonshotAI - FlashKDA v1 Deep Dive]]
- [[Cohere - North Mini Code Megakernel Serving Engine]]
- [[AI-Generated Kernels]]
