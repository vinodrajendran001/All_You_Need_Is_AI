---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-11-cam-pedersen-derive-kernels
source_title: "Don't Write Kernels, Derive Them"
source_author: "Cam Pedersen"
source_url: "https://muni.works/research/tang"
tags:
  - source/summary
  - kernels
  - compilers
  - gpu
  - inference
source_ids:
  - src-2026-11-11-cam-pedersen-derive-kernels
status: active
---

# Don't Write Kernels, Derive Them

## Summary

A long research write-up of **tang**, a `no_std` Rust library whose tensor IR has only two constructs:
**views** (affine maps from an iteration space to tensor coordinates, covering broadcast, transpose,
slicing, striding, padding and gathers) and **comprehensions** (reductions under a monoid whose body is
a scalar expression graph). The thesis is that "**a kernel is a theorem, not a program**": fusion,
flash attention and its backward pass should be *derived* as rewrites and searched as schedules rather
than written by hand per operator, per chip and per fusion. One graph lowers to WGSL, CUDA, Metal,
OpenCL, GLSL and C.

The paper is unusually candid. It reports wins and losses against PyTorch, llama.cpp, FlexAttention,
FlashAttention-2/3, fla, mamba_ssm and vLLM, and says repeatedly where a result is over its own
baseline rather than over the state of the art. All measurements are first-party, several were taken
on shared GPUs (marked by the authors), and much of the production evidence compares derived kernels
against the authors' own hand-written engine.

## Key claims

### Kernels from rewrites

- **Fusion is one substitution rule.** Maps are spliced into their consumers. Reductions are never
  substituted, only inlined by a schedule decision, which "separates algebra from scheduling".
- **Flash attention is a rewrite.** `stabilize_softmax` merges the max and the exponential sums into
  one reduction under the **online-softmax monoid**; the staging rule then produces flash attention's
  tile structure. Logsumexp, Welford variance and top-k are the same rewrite with different monoids.
  The paper lists twelve "rediscoveries", including split-K GEMM, SwiGLU gate|up fusion, the paged KV
  cache (as a gather view) and chunked SSD / gated-delta scans.
- **Gradients are comprehensions**, so the same passes optimize the backward. The compiler proves per
  graph that a stabilizing max has no gradient and drops it. On CUDA this cut a training step from
  **63 kernels to 49** and summed best-per-kernel time from **1.80 to 1.22 ms** at sequence 512 on an
  RTX 3090. On WGSL and Metal the intermediate-free backward currently *costs* speed: **0.68–0.93×**
  the materialized schedule on Metal and **0.25–0.34×** under Vulkan.
- **Precision is a schedule field.** An emulating interpreter accepts or rejects a format against an
  error budget before running. It matches GPU f16 kernels "to 1 ulp when the reduction order is the
  same"; at equal reduction length prediction and measurement agree "within about 1.7×", but
  predictions can be far off when length or order differs.

### Measured against hand kernels and frameworks

- **The fastest schedule is not a property of the operator.** On the M4 Max the best causal-attention
  schedule "flipped between two runs of the same code", and rules tuned on the M4 picked the wrong
  matmul schedule on an RTX 3090.
- **Against PyTorch (idle RTX 3090, the table the authors say to cite):** tang's transformer-block
  forward wins at seq 512 (**0.331 ms** vs **0.396** for PyTorch in a CUDA graph with TF32 and
  **0.407** for `torch.compile`), loses at seq 128 (**0.196** vs **0.162**), and ties forward plus
  backward. A lone matmul is **1.1× slower** than cuBLAS TF32; "the gain comes from fusion across
  operator boundaries".
- **Attention variants:** where the score is modified (soft cap, ALiBi) the derived forward is "up to
  3.4× faster" than FlexAttention fp32. It loses badly elsewhere: a sliding window is **25× slower**
  (masked tiles are computed, not skipped), the forward wins **0 of 8** against FA2 in the full sweep,
  and at one head dimension no tensor-core forward is generated, a **150×** gap. FA2 here is PyTorch's
  bundled SDPA kernel, because `flash_attn` would not build.
- **A whole model as one graph:** Qwen3-8B (MLX 4-bit) decodes as one IR graph lowered to **584
  kernels** at **148.7 tok/s** against llama.cpp's **149.4** at short context and **124.2** vs
  **134.9** at 4k, with arg-max equal to an f32 reference at **257/257** positions. llama.cpp ran a
  Q4_0 GGUF requantized from the same checkpoint, so formats are close but not identical.

### Deriving a production engine

The target is the authors' own hand-written engine serving Qwen3-Coder-Next (80B, 3B active, 4.5-bit
GGUF) on one H200.

- **MoE layer, equal work:** derived is **18%** slower at batch 1, **7%** slower at batch 4, ties at 8
  and is **5%** faster at 64. Weights were "random valid k-quant blocks".
- **Inside the model** (derived path only from 16 window rows up): over five interleaved rounds a
  decode step takes **13.99 vs 15.84 ms** at 16 streams, **21.36 vs 23.44** at 32 and **28.43 vs
  30.00** at 48, i.e. **5–12%** less time. It misses the engine's 48-stream agreement gate at
  **98.93%** against a 99% bar; the hand engine also fails, at exactly **99.00%** against a strict
  inequality.
- **Prefill:** derived head-dim-256 attention plus a derived gated-delta scan cut time to first token
  at 44k tokens from **8.33 s to 5.54 s**. But vLLM on the official FP8 checkpoint reached first token
  in **1.08 s** at 44k against the engine's **13.8 s** in the same session — "about 12× faster". The
  authors say they "have not reconciled" 13.8 s with the 8.33 s baseline, so the prefill table "should
  be read as relative".
- **Against FlashAttention-3** at head dimension 256 the derived Hopper attention runs at **0.43–0.54**
  of its speed forward and **0.22–0.40** backward.
- A whole derived decode step ties the hand engine on Qwen3-8B but trails it by **13%** at context
  128 and **35%** at 4k on Qwen3-Coder-Next (1,924 kernels).
- The hand MoE kernel, ported to GLM-5.3, was correct but "up to 2.5× *slower*" than the engine's
  generic path below 64 tokens per expert — the authors' one production data point for "tuned for one
  model is the wrong point on the next".

### A speed-of-light floor read off the kernel

- For a comprehension over affine views, the **least memory traffic and the tile that attains it are
  the primal and dual of one linear program** (via Brascamp–Lieb). It reproduces matmul's cube tile and
  gives FlashAttention's blocks as attention's dual tile. Weak duality is proved in Lean for a
  restricted model; strides, multi-term addresses and masks are outside it.
- A **time floor** adds launch cost, DRAM latency and an occupancy term. It "never exceeds the measured
  time" on **24** GEMV-class and epilogue kernels on two GPUs, reaching **0.76–0.93** of measured time
  on large RTX 3090 kernels but only **0.05–0.66 (median 0.38)** on the H200, "and we have no validated
  term for the gap". No candidate beat the floor in **892** timings.
- **The traffic-optimal tile does not win on time.** The model matches the M4 Max autotuner's tile only
  for register capacities from **4096 to 8192** words; a per-tile estimate picks within **2.5%** of the
  fastest on seven of eight kernels and loses the eighth by **1.27×**.
- **Removing launches did not speed up decode.** On the H200 a decode step's traffic floor is only
  **0.16–0.29** of its time; fusing block-local chains removed **96 of 548** launches yet the step went
  from **4.05 to 4.44 ms**. On the 3090 a persistent megakernel running the whole step as one launch
  with **437** phases was "correct but 19% slower", because one register budget spilled the largest
  GEMV. Earlier floor-based bounds "missed in both directions".

### Verification

`tang-verify` fills each kernel's outputs with NaN before it runs and names the failing kernel by
provenance; it was built after four structural bugs in the hand engine "slipped past every unit test".
Core rewrites are mechanized in Lean 4 with Mathlib over the reals; floating point is not modelled.

## Why it matters

The vault's [[GPU Kernel Optimization]] page describes a ladder climbed by hand and asks "How much of
the kernel ladder survives as compilers absorb it?" This is the strongest compiler-side answer so far:
FlashAttention and its backward fall out of one algebraic rewrite, and the schedule search, not the
operator, carries chip-specific knowledge. It also extends
[[Arithmetic Intensity and the Roofline Model]] with a floor computed from the kernel's own IR and
checked against hardware counters, and it
gives [[Megakernels]] a counter-datapoint: launch removal alone was time-neutral or worse here. For
[[AI-Generated Kernels]], it offers a contrasting correctness story — derived kernels are checked by
construction against an f64 interpreter of the same graph rather than by benchmark tests that models
can game.

## Tensions / open questions

- **Wins are local and conditional.** Forward-only at seq 512 beats PyTorch; seq 128 loses; training
  ranking "is not established" (a contended run had tang at 5.05 ms vs PyTorch's 4.21 ms).
- **Baselines.** Several production gains are over the authors' own engine, which is about 12× behind
  vLLM on prefill; the MoE layer test uses random weights; FA2 is PyTorch's bundled kernel.
- **Shape-keyed emitters remain.** The paper says no kernel was written "for any one operator", but
  lowering still uses a short list of emitters keyed on graph shape (flash kernel, Hopper backward,
  GEMV, integer tensor-core stage, chunked scan). The conclusion concedes they are needed "for the
  hottest schedules".
- **The f32 tolerance failure.** The fused CUDA attention backward computes in bf16 and fails an f32
  tolerance; one rejected placement with error 7.0 is "caught by the check but not yet explained".
- **The floor is a bound, not a predictor.** It is loose on the H200, says nothing about compute-shaped
  kernels, and "as a guide to which optimizations pay it has been wrong as often as right".
- **Capture quirk:** inline math was stripped, so several sizes and head dimensions read as gaps ("At
  the forward trails FlashAttention-2", "no tensor-core forward is generated at"). Numbers above are
  only those present in the capture.

## Affected pages

- [[GPU Kernel Optimization]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Megakernels]]
- [[AI-Generated Kernels]]
- [[Inference Determinism]]

## Raw capture

- [[knowledge-base/raw/sources/Don't Write Kernels, Derive Them]]

## Citations

- Canonical URL: <https://muni.works/research/tang> (captured link carried a `utm_source=tldrai`
  parameter, removed here).
- Author as captured: Cam Pedersen. The text is written as "we"; a read-only fetch of the canonical
  page to confirm the full byline timed out, so co-authors, if any, are unverified.
- Published November 11, 2026 per the capture; captured November 20, 2026. `source_id` uses the
  publication date.
- All measurements are first-party; the authors mark shared-GPU runs and report minima for them.

## Related pages

- [[GPU Kernel Optimization]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Megakernels]]
- [[AI-Generated Kernels]]
- [[GPU Execution Model]]
- [[Inference Serving Engines]]
- [[Linear Attention and Recurrent Memory]]
- [[Mixture of Experts]]
- [[Qwen]]
- [[Cohere - North Mini Code Megakernel Serving Engine]]
- [[Ant Group and vLLM - Humming Quantized Inference Kernels]]
