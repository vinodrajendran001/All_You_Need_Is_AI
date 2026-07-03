---
type: source-summary
created: 2026-07-03
updated: 2026-07-03
source_id: src-2026-07-03-fergus-finn-cuda-kernel
source_title: "What happens when you run a CUDA kernel"
source_author: Fergus Finn
source_url: https://fergusfinn.com/blog/what-happens-when-you-run-a-gpu-kernel/
tags:
  - source-summary
  - gpu
  - cuda
  - systems
  - hardware
source_ids:
  - src-2026-07-03-fergus-finn-cuda-kernel
status: active
---

# Fergus Finn - What Happens When You Run a CUDA Kernel

## Summary

This blog post traces a single `vadd` vector-add kernel (a million floats, one thread each) end to end: from `nvcc` compilation down to the warps that execute it and back up to the printed answer. It is a systems-level tour of the CUDA/GPU **execution model** — how source becomes device code, how the CPU hands work across the PCIe bus, how the GPU turns a linear instruction stream into a massively parallel program, and why this trivial kernel ends up bound by memory bandwidth.

Along the way it makes visible the machinery normally hidden: the multi-compiler `nvcc` pipeline (`cicc` → PTX → `ptxas` → SASS, bundled with a PTX fallback in a fatbin); the host launch stub and constructor registration; the channel abstraction (pushbuffer, GPFIFO, USERD cursors, and the QMD launch descriptor) plus the **doorbell** MMIO write that wakes the GPU; the compute work distributor spreading 4096 blocks across 128 SMs; and warp **eligibility** driven by compiler-written stall counts and scoreboard barriers.

## Key claims

- **`nvcc` is a driver over many compilers.** Device code goes `cicc` (LLVM) → **PTX** (a virtual ISA with infinite typed registers, device-agnostic) → `ptxas` → **SASS** (real, architecture-specific). The cubin (an ELF) plus a PTX fallback are bundled in a **fatbin** welded into an ordinary Linux executable; the driver can JIT the PTX if run on an uncovered architecture.
- **Kernel arguments live in constant bank 0**, a broadcast read the constant cache can serve to all 32 lanes at once; the compiler fuses PTX address arithmetic (`mul.wide` + `add`, `cvta`) into single `IMAD.WIDE` SASS instructions.
- **A GPU takes no function calls.** It reads driver commands from host memory across PCIe. A launch is one fully-formed command placed into a **channel**: the driver writes GPU **methods** into a **pushbuffer**, points a **GPFIFO** ring entry at that span, advances the `GP_PUT` cursor (in USERD), and rings a **doorbell** register via a single MMIO store to make the host engine look.
- **The QMD (Queue Meta Data)** is the launch descriptor: grid/block dims (4096, 256), registers/thread, shared memory, the program's start address, and the constant-bank address of the arguments. It is streamed inline into the pushbuffer via `SET_INLINE_QMD_ADDRESS` + `LOAD_INLINE_QMD_DATA`.
- **`cuLaunchKernel` is asynchronous** — it returns the instant the doorbell is rung; the CPU runs on while the GPU works.
- **Occupancy is set by the tightest resource cap.** On the RTX 4090 (AD102, 128 SMs), 256-thread blocks using 16 registers/thread are limited by the 1,536-threads/SM cap to **6 resident blocks (48 warps) per SM**, spread across 4 sub-partitions (12 warps each). Each scheduler issues at most one instruction per cycle and picks an *eligible* warp.
- **The GPU hides latency instead of reordering.** Rather than out-of-order machinery, `ptxas` packs per-instruction control bits — a **static stall count** (fixed-latency ops), a **yield hint**, and **scoreboard barrier** indices (0–5) for variable-latency ops like global loads. A warp waiting on a load barrier is ineligible and skipped, keeping hardware scheduling near-zero-overhead.
- **Coalesced memory + arithmetic intensity explain the runtime.** 32 consecutive 4-byte loads coalesce into four 32-byte sectors down L1 → L2 (72 MB) → GDDR6X. With one `FADD` per 12 bytes moved, the kernel is memory-bound: `ncu` shows ~82% warps active but only ~5% issue activity and ~80% DRAM throughput, finishing in **10.78 µs** — set by how fast DRAM can feed it. The result is returned via a completion **semaphore** and a copy engine served straight from L2 (no DRAM round trip).

## Why it matters

This is the vault's first bottom-up account of the **GPU execution model** and seeds the new concept [[GPU Execution Model]]. It is the software/runtime complement to [[AI Accelerator Architecture]] (which covers hardware/cluster *design*): the same "compute vs communication" and memory-bound story, but from the perspective of one kernel's warps. Its arithmetic-intensity conclusion — a low-FLOP kernel is limited by memory bandwidth — is the micro-level version of the **decode is memory-bound** argument in [[LLM Inference]] and the reason [[KV Cache]] and [[Model Quantization and Efficiency]] focus on bytes moved.

## Tensions / open questions

- It deliberately studies a trivially memory-bound kernel; compute-bound GEMMs, tensor-core paths, and shared-memory tiling (the workloads that dominate real training/inference) follow different scheduling and locality dynamics.
- The SASS control-word layout is undocumented and reconstructed from microbenchmarking, so exact bit fields are architecture-specific and may drift across GPU generations.
- Everything is traced on one RTX 4090 (Ada); occupancy math and method classes differ on Hopper/Blackwell.

## Affected pages

- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
- [[LLM Inference]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/What happens when you run a CUDA kernel.md`
- Source URL: [https://fergusfinn.com/blog/what-happens-when-you-run-a-gpu-kernel/](https://fergusfinn.com/blog/what-happens-when-you-run-a-gpu-kernel/)

## Related pages

- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
- [[LLM Inference]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]]
- [[AI Knowledge Base Overview]]
