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

Lewis Won had already tuned a FlashAttention-2 (FA2) forward kernel in Triton until it matched
PyTorch's `scaled_dot_product_attention` (SDPA) on his RTX 4070 SUPER. Here he ports it to NVIDIA's
**CuTe DSL**, "a Python library for writing kernels at the level of CUTLASS". He first reads Triton's
GPU-level IR (TTGIR) and the compiled SASS to list what Triton decided automatically. He then starts
from a direct port without those decisions and adds them back one round at a time: a swizzled
shared-memory layout, `ldmatrix` operand loads, keeping the softmax weights `P` in registers,
`cp.async` background copies, and a tile/stage sweep. Each round is profiled in Nsight Compute and
timed with the unchanged harness from the earlier article. The final CuTe kernel ties or slightly
beats the Triton kernel and beats SDPA on every tested shape. A last round tries two schedules that
Triton's `tl` language cannot express, and both are slower on this card. The durable content is a
measured, itemized account of what a tile compiler does for a kernel author, plus a benchmarking
protocol that records clock and power. All results are self-reported on one consumer GPU.

## Key claims

### Triton's automatic decisions are most of the performance

The straight port (v0) keeps Triton v5's algorithm: 64 query rows per block, 4 warps, an unmasked
loop then a masked loop over the diagonal, and `exp2` with the scale folded in. Everything else is
"the simplest thing that works". At N = 4096, non-causal, v0 takes **5.436 ms (25.3 TFLOP/s)**,
against **1.968 ms (69.8)** for Triton v5 and **2.158 ms (63.7)** for SDPA. In the harness it is
**2.5–2.8× slower** than both. Nsight Compute puts v0's tensor cores at **33.7%** of peak, against
**88.9%** for SDPA and **87.4%** for Triton v5, with L1 and shared memory 99% busy. The longest
stalls are MIO throttle (17.1 cycles per instruction) and short scoreboard (6.3): warps queue to
issue shared-memory instructions, then wait for their results.

From TTGIR and SASS the author recovers Triton's choices. It stacks four warps along the rows
(`warpsPerCTA = [4, 1]`), uses a swizzled shared layout, and emits **76 `LDSM`** (ldmatrix)
instructions. It passes `P` between the two multiplies through a layout conversion, emits **32
`cp.async`** copies, and lets `@triton.autotune` pick tiles and stages. For a fair comparison both
kernels are pinned at 64 × 64 tiles, 4 warps, 2 stages, D = 64, bf16 and no mask. Triton then uses
168 registers per thread and 24,576 bytes of shared memory, and the Round 4 CuTe kernel uses 165
registers and the same 24,576 bytes.

### Each round, with its mechanism

Figures are for N = 4096, non-causal, unless stated. Harness and Nsight Compute figures are
measured differently and should not be compounded.

| Round | Change | Reported effect |
| --- | --- | --- |
| 1 | `Swizzle<3,3,3>` shared layout | bank conflicts **554 M → 0**; tensor cores 33.7% → 71.3%; harness **5.436 → 2.686 ms** (causal 2.997 → 1.324) |
| 2 | `ldmatrix` operand loads | **224 `LDS` + 64 `PRMT` → 40 `LDSM`** per pass; 594 → 342 instructions; tensor cores 71.3% → 86.9%; harness 2.248 ms (causal 1.119) |
| 3 | `P` kept in registers | 342 → 321 instructions; shared memory 32 KB → 24 KB; about **1%** (2.19 → 2.17 ms, Nsight Compute) |
| 4 | `cp.async`, FA2 copy order | tensor cores **93.2%** (2.04 ms, Nsight Compute); harness 2.100 ms (causal 1.040) |
| 5 | tile/stage sweep, K/V ring | **0–4%** over v4, depending on shape |

- **Swizzle.** A 64-wide bf16 row is 128 bytes, exactly the 32 four-byte banks, so in a row-major
  tile column 0 of every row is in bank 0. The operand loads read the same columns of 8 rows and
  collide 8 ways. The swizzle stores chunk c of row r at chunk position c XOR (r mod 8), so the same
  chunk of 8 rows lands in 8 bank groups. The same 117 M loads drop from 671 M wavefronts to 117 M.
  Registers jumped from 118 to 253, "most likely" swizzled V addresses precomputed outside the loop.
- **ldmatrix.** One warp-wide instruction reads four 8 × 8 tiles and hands each lane the values the
  tensor-core multiply wants, transposing V on the way. Load/store-pipe use falls 72.5% → 26.0%.
- **P in registers.** The first multiply's output layout lines up with the second multiply's input
  layout, so converting the accumulator to bf16 and re-viewing it (`as_a_operand`) moves no data. The
  gain is small because the shared-memory round trip "was already conflict-free".
- **cp.async.** One instruction copies 16 bytes from global to shared memory without a register, and
  the thread moves on. v4 orders work as FA2 does: V for block j loads during S = QKᵀ, and K for block
  j + 1 loads during the softmax and P·V. Long-scoreboard stalls leave the top four, barrier stalls
  fall from 2.3 to 1.9 cycles, and the result is "on par with Triton v5's 92.2% (64 × 128 tiles, 2
  stages)" at the same fixed clock.
- **Sweep.** Shared memory is capped at 99 KB per block: `2·D·(bM + 2·S·bN) ≤ 101,376` bytes. Three
  64 × 64 stages need 56 KB, leaving room for only one block on a 100 KB SM, which gives **58.1
  TFLOP/s** at N = 4096 non-causal against **70.8** with one stage. The best settings were 64 × 32,
  4 warps, 3 stages at N = 512; 64 × 64, 4, 1 for N ≥ 1024 non-causal; and 64 × 64, 4, 2 for causal.
  The 2-stage ring cut causal barrier stalls from 2.21 to 0.66 cycles.

### Ownership and occupancy

`cute.make_tiled_mma(..., (4, 1, 1))` stacks the four warps along the rows, so every row of the
score tile S stays inside one warp. The `mma.m16n8k16` instruction gives each row to one quad of 4
lanes, so the online softmax's row maximum and sum need two register-to-register shuffles. Under
`(2, 2, 1)`, each row would be split between two warps and the maximum would go through shared
memory on every key block. Registers, not shared memory, set residency. At 168 registers × 128
threads, 3 blocks fit per SM (shared memory would allow 4), which is 12 of 48 warps, "the 25%
theoretical occupancy Nsight Compute reports". Registers are allocated in steps of 8 per thread, so
165 and 168 fall in the same band, and "the 3 fewer registers make no measurable difference". The
author adds that "a kernel limited by the tensor cores does not need many" resident warps.

### Final comparison and the fair-fight protocol

Harness medians at N = 4096 (10 runs for CuTe v5 and Triton v5, 3 for NVIDIA's example, 35 for
SDPA):

| Kernel | Non-causal | Causal |
| --- | --- | --- |
| CuTe v5 | 1.991 ms, 69.1 TFLOP/s | 1.029 ms, 66.8 TFLOP/s |
| Triton v5 | 1.968 ms, 69.8 TFLOP/s | 1.079 ms, 63.7 TFLOP/s |
| SDPA | 2.158 ms, 63.7 TFLOP/s | 1.118 ms, 61.5 TFLOP/s |
| NVIDIA's CuTe example | 1.950 ms, 70.5 TFLOP/s | 1.038 ms, 66.2 TFLOP/s |

Across 8 shapes (N = 512 to 4096, with and without the mask), CuTe v5 beats SDPA on every shape,
is **2–5% faster than Triton v5 on 5 and ties on 3**, and NVIDIA's example lands within 4% of v5
everywhere. Under Nsight Compute at a fixed 2.52 GHz, non-causal, v5 reaches **93.2%** of tensor
peak against 92.2% for Triton v5 and 88.9% for SDPA. It does so with 165 registers and 24.6 KB of
shared memory, against 255 registers and 41.0 KB or 49.2 KB.

The author's question "was it a fair fight?" gets its own experiment, because "a kernel at a lower
clock looks slower for reasons unrelated to its code". Each kernel's benchmark runs back to back for
4 s, interleaved over 3 rounds with 30 s cool-downs, sampling every 10 ms. CuTe v5 and Triton v5
drew the same power at median clocks within 1.1% at every N, and none of the 38 benchmark runs
showed a thermal slowdown. Below N = 2048 nothing reached the 220 W power cap. At N = 4096 both
custom kernels sat at the cap in 93–98% of samples. Under these conditions CuTe v5 was 4–5% faster
causal at N ≥ 1024. That gap survives with Triton at the same tile sizes (still 3.9–4.1% slower),
so it is not the 1.6% of extra diagonal work done by Triton's 64 × 128 tiles. The author's likely
cause is leaner compiled code, **350 instructions per key block against 388**, "which `tl` gives no
control over". He notes that none of Rounds 1–5 is CuTe-only.

### Beyond `tl`: two schedules that did not pay on sm_89

The tensor-core floor is `t_min = operations / (512 · 56 · f_SM)`: 512 bf16 operations per clock
per SM, on 56 SMs. At v5's median clocks in a sustained run that is **1.815 ms** non-causal and
**0.912 ms** causal, against v5's **1.954** and **1.037 ms**. The author lists a wave tail as one
part of the non-causal gap, and none for causal: 2,048 blocks are 12.19 waves, and at exactly 8
waves v5's throughput is 1.9% higher.

Both candidates give O and L bitwise equal to v5, and both are slower:

- **v6, per-buffer mbarriers** instead of block-wide barriers (+2.4% non-causal, +7.0% causal). On
  sm_89 an mbarrier wait is a polling loop costing 25–33% more instructions, and CuTe DSL 4.8.1's
  own mbarrier helpers refuse sm_89.
- **v7, software pipelining**, running the next QKᵀ in slices between pieces of the current softmax
  (+2.1%, +2.8%). Other warps already fill those gaps. Loop rotation in plain `tl` slowed Triton by
  0.4–5.3% (clocks not logged).

A producer-warp design was not built, because a CuTe producer warp would poll v6's mbarriers. Warp
specialisation works on sm_89 in neither `tl` nor **Gluon** (`triton.experimental.gluon`, shipped
with Triton 3.6). Gluon always emits `setmaxnreg`, which Hopper and Blackwell have and sm_89 lacks.
Gluon does compile v6's and v7's constructs: "That is beyond `tl`, not beyond Triton." The
conclusion is scoped to the hardware: "On this card, scheduling beyond `tl` does not pay."

### What the author must now write by hand

The closing checklist names ten items Triton had decided for him. They are warp ownership, swizzled
layouts (bank conflicts "should be zero"), ldmatrix copies, re-viewing the accumulator, and the copy
schedule ("a wrong order is a race, not a slowdown"). Then come ragged edges, a configuration table
checked against 99 KB, compiling once per configuration, and checking results after every change
("a wrong answer can still be fast"). The last is fair comparisons: "Interleave, cool down, and
record clock, power and throttle reasons next to every time."

Correctness is handled throughout. The harness and test file are byte-for-byte copies with published
checksums, and every version passes the unchanged tests. The fp32 inputs are rounded to fp16 rather
than Triton's TF32. They pass the tests at unchanged tolerance, but fp16 overflows above 65,504. The
author also reports an apparent CuTe DSL 4.8.1 bug: with a swizzled layout, one of two indexing forms
returns block 0's values for blocks 1–3. His kernels use the correct form.

## Why it matters

[[GPU Kernel Optimization]] gains a measured, one-decision-at-a-time account of what a tile compiler
contributes, and a qualified answer to whether hand-written kernels still win. [[GPU Execution Model]]
gets the compute-bound counterpart to its vector-add example: registers bounding residency, ownership
fixed by the tensor-core instruction, and bank conflicts. [[Arithmetic Intensity and the Roofline Model]]
gets a compute-side floor that moves with the clock. [[NVIDIA]] and [[PyTorch]] appear as the CuTe
DSL publisher and the SDPA baseline. [[Software Performance Engineering]] gains a clock- and
power-aware benchmarking protocol. [[Transformer Architecture]] gets FA2's work partitioning made
concrete.

## Tensions / open questions

- Everything is self-reported by one author on one consumer GPU (RTX 4070 SUPER, sm_89, 56 SMs, 220 W
  cap), for one head size (D = 64), B = 4, H = 8, and the forward pass only. The linked repository
  holds raw results, but the vault has not re-run them. Results on Hopper or Blackwell, where the
  missing features exist, are not shown.
- The margins are close to the noise. Non-causal N = 4096 times "jump between two speeds for every
  kernel" (CuTe v5 1.92–1.95 or 2.03–2.10 ms). In the sustained table, 1.946 ms for CuTe v5 against
  2.119 ms for Triton v5 is still labelled a tie, and there Triton is slower than SDPA's 2.021 ms,
  reversing the harness order (1.968 against 2.158). The harness table also calls N = 512 causal a
  tie at 0.039 against 0.042 ms; the sustained run gives 0.037 for both.
- Triton v5 appears at different tile configurations: pinned at 64 × 64 for the register comparison,
  "64 × 32 tiles there" for the Round 0 profile (87.4%), and 64 × 128 with 2 stages for Round 4 and
  the final profile (92.2%). Per-round comparisons are not all against one Triton configuration.
- Round gains are measured in the harness or under Nsight Compute at a fixed base clock, and the
  author warns that Nsight Compute "durations are not wall-clock speeds". They cannot be summed.
- Several causes are stated as likely, not isolated: the causal advantage ("likely" leaner code), the
  253-register jump ("most likely"), and the 165-vs-168 register difference ("I did not look into
  why"). The CuTe DSL indexing issue "looks like a bug", shown with a repro; no NVIDIA confirmation
  is captured.
- The SDPA backend PyTorch selected is not stated. The `permutation_mnk` setting was taken from
  NVIDIA's FA2 example, and the author "did not time the default".
- The author states the article "was written with the assistance of AI" and invites corrections.
- The earlier Triton article is not in the vault, and its link in the capture is a placeholder URL.
  Triton v5's design and its "Problem 3" are known only through this article.

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
- Code, profiles and result files are in the author's GitHub repository
  `searlion/cs336-2026-assignment2-systems`, linked throughout the capture but not separately captured.
- The capture's link to the author's previous Triton article is a placeholder
  (`todo-dev.to-url-of-the-follow-up-article`), so that article cannot be cited. DEV's promotional
  footer is excluded from this summary.

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
