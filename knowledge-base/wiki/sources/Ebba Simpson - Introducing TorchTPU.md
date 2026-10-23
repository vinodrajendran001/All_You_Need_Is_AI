---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-21-simpson-torchtpu
source_title: Introducing TorchTPU
source_author: Ebba Simpson
source_url: https://pytorch.org/blog/introducing-torchtpu/
tags:
  - source/summary
  - accelerators
  - compilers
  - distributed-training
source_ids:
  - src-2026-10-21-simpson-torchtpu
status: active
---

# Ebba Simpson - Introducing TorchTPU

## Summary

The PyTorch blog announcement of **TorchTPU**, a native PyTorch backend for Google TPUs built through a
Google-Meta collaboration begun in **mid 2025**. Its stated goal is that `.to("tpu")` should be the only
change an existing PyTorch program needs, with both eager execution and `torch.compile()` supported.

The post is long and unusually specific about mechanism, which makes it valuable; nearly all of its
performance numbers are **first-party**, and the post is candid that moving a workload is not the same
as making it fast.

## Key claims

### How it attaches to PyTorch

- TorchTPU registers a C++ **`PrivateUse1`** dispatcher backend and stores TPU tensors through PyTorch's
  own `at::Tensor` / `StorageImpl`, rather than sitting outside the dispatcher.
- Three eager modes: **Strict** (one ATen op at a time, dispatched asynchronously), **Debug** (one op at
  a time with host/device synchronization, `TORCH_TPU_LAUNCH_BLOCKING=1`), and **DeferAndFuse**
  (accumulate ops until a materialization point, then compile and fuse, `TORCH_TPU_DEFER_AND_FUSE=1`).
- `torch.compile(model, backend="tpu")` hands a Dynamo FX graph to TorchTPU, which traces it with all
  operations deferred, emits **one StableHLO program**, compiles it, and returns a callable.
- Compilation runs StableHLO or Mosaic through XLA; **the TPU ISA is proprietary** and not exposed.
  PjRT provides compile, launch, and copy APIs.
- The contrast drawn with **PyTorch/XLA** is that the older lazy-tensor integration required explicitly
  marked compilable regions, had high compile latency, had no native eager mode, and lagged on
  distributed features. TorchTPU also drops the JAX runtime dependency.

### Distribution and kernels

- Collectives are implemented at the PyTorch Process Group level and lowered to StableHLO collectives.
  TorchTPU enforces **one process per device**.
- **Skinny Collectives** isolate collectives into separate modules to avoid cross-rank graph
  inconsistency; `@spmd_safe` plus a compilation handshake can remove graph breaks when code is provably
  SPMD.
- `topology_aware_mesh()` maps communication-heavy parallelism onto high-bandwidth **ICI** and lighter
  data parallelism onto **DCN**.
- Custom kernels come from **Pallas** (wrapped via `torch.tpu.pallas.jax_op`), **Tokamax** for
  production kernels, and **Helion**, which is explicitly experimental.
- **Bounded dynamism** allocates buffers to compile-time maximum bounds while tracking runtime logical
  dimensions, padding and slicing instead of recompiling. Still in development; `torch.compile`
  currently forces `dynamic=False`.

### Reported numbers — all first-party unless noted

- Coverage: **~450 ATen ops** and the **5,000 most-downloaded Hugging Face models**.
- Validation corpus of **4,917** models across **500+** architecture families. Tier 1 pass rate **98%**
  (4,821/4,917); Tier 2 numerical parity with GPU **97%** (638/657); bounded dynamism **834/839**
  models, reported as **99%** numerical correctness.
- **DeferAndFuse** is said to be **50% or more faster** than Strict Eager — but with no stated workload,
  hardware, or baseline measurement.
- **Skinny Collectives** are said to cost **30-40% end-to-end** performance, again without configuration.
- Precision modes: `high` uses a **3-pass** algorithm at roughly **3x** MXU compute, `highest` a
  **6-pass** algorithm at roughly **6x**, relative to the default `medium`.
- Muse Glimmer 30B inference, **1 TPUv7 chip** (FSDP world size 2 because one chip exposes two devices):
  **~25.7k TPS / 59% MFU** at sequence length **5,120**, and **~22.4k TPS / 51% MFU** at **10,240**.
- Muse Glimmer training, **4 TPUv7 chips**: **~5.6k TPS per TPU / 38% MFU** at 5,120 and **~4.6k TPS /
  32% MFU** at 10,240, versus an externally produced TorchTitan implementation at **~5.3k / 36%** and
  **~4.2k / 29%**.
- Qwen3 MoE 235B on **64 TPU v7**: **1,828 TPS** for TorchTitan/PyTorch versus **1,937 TPS** for
  JAX/MaxText — that is, the PyTorch path is slightly **behind** the JAX baseline here.
- Qwen3 weak scaling at **1,024 / 2,048 / 4,096 / 8,192** TPU v7 chips: **2,236 / 2,214 / 2,095 /
  2,104 TPS per TensorCore**, MFU **28.8% / 28.5% / 26.9% / 27.1%**, step times **29.3s / 29.6s /
  31.3s / 31.2s**.
- FLUX optimization sequence: **11.49s** baseline (0.26 samples/s) → DeferAndFuse **9.95s** (1.15x) →
  SimpleFSDP **6.52s** (1.76x) → Pallas SplashAttention **5.55s** (2.07x) → full `torch.compile`
  **3.02s** (3.80x) → peephole-rewritten **2.78s** (1.08 samples/s).
- Llama 3 405B on **1,024 TPU v7x**, 8K context, BF16: **500 tokens/sec/chip** at **50+% MFU**.
- DLRM v2 on **32 TPU v7x**: **18.3 ms** step latency, described as **100% parity** with a JAX baseline.
- Hardware context given as generation-specific examples: MXUs with **256x256** multiply-accumulators;
  TPU 8i with **288 GB** HBM at **8.6 TB/s**; ICI **19.2 TBps**; TPU 8t DCN **400 GBps**.
- **[Third-party]** SemiAnalysis InferenceX is cited as independent benchmarking of TPU v7 with
  vLLM-TorchTPU; reported costs **2.01 cents per million tokens** on 8K/1K (down from **3.6 cents** at
  the September debut) and **0.83 cents per million tokens** on AgentX. The post does not reproduce the
  methodology.

## Why it matters

This vault's [[Accelerator Software Externalization]] thread has mostly covered one direction: making
non-NVIDIA hardware usable by porting kernels. TorchTPU is the **framework-level** version of the same
problem, and it is the clearest worked example the vault holds of what a second-source accelerator has
to supply before a framework's users can reach it: a dispatcher backend, a real eager mode, a compiler
entry point, collectives, a kernel DSL, and a dynamic-shape story.

It also gives [[Distributed Training Parallelism]] and [[AI Accelerator Architecture]] concrete detail
on what differs from GPUs — single-process-per-device, effectively single-threaded TensorCores,
compile-time-known shapes, and topology-aware mesh construction — rather than treating accelerators as
interchangeable FLOPs.

## Tensions / open questions

- Essentially all performance figures are **first-party**, and several headline claims
  (DeferAndFuse "50% or more", Skinny Collectives "30-40%") carry **no workload, baseline, or
  configuration**.
- The Qwen3 comparison shows PyTorch **slightly below** the JAX/MaxText baseline, which complicates the
  post's general framing.
- The post's own caveat is the important one: `.to("tpu")` should run, but **peak performance generally
  requires** Pallas kernels and TPU-specific stacks such as vLLM-TorchTPU, SGLang-TorchTPU, or
  TorchTitan-TorchTPU. Portability and performance are separate achievements.
- TPUs support **only one user-space process**, so RL colocation does not work out of the box.
- `@spmd_safe` is described as brittle if the code is actually MPMD.
- FlexAttention was unsupported in one TorchTitan example and replaced with vanilla scaled dot-product
  attention, so some PyTorch features do not yet carry over.
- The FLUX scaling report gives per-sample step time **0.92s → 1.00s** from 8 to 256 chips and also
  states **3.01s total step time** without explaining the relationship.
- "Industry-competitive", "near-linear", and "100% parity" are descriptive phrasings, not
  workload-general results. Nothing here establishes that all 5,000 supported models run unchanged in
  production.
- The roadmap — bounded dynamism, FP8/FP4, RL integration — is **6-12 month** future work, not shipped.

## Affected pages

- [[Accelerator Software Externalization]]
- [[AI Accelerator Architecture]]
- [[Distributed Training Parallelism]]
- [[PyTorch]]

## Raw capture

- [[Introducing TorchTPU]]

## Citations

- Raw capture: [[Introducing TorchTPU]]
- Canonical URL: <https://pytorch.org/blog/introducing-torchtpu/>
- Published 2026-10-21; captured 2026-10-22.
- Cites SemiAnalysis InferenceX benchmarking, not read during this ingest.

## Related pages

- [[GPU Kernel Optimization]]
- [[AI-Generated Kernels]]
- [[Inference Serving Engines]]
- [[ML Systems at Scale]]
- [[Mixture of Experts]]
- [[Megakernels]]
- [[Meta]]
- [[Google Cloud]]
- [[SemiAnalysis]]
