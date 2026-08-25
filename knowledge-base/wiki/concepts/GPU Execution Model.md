---
type: concept
created: 2026-07-03
updated: 2026-08-25
tags:
  - concept
  - gpu
  - cuda
  - systems
  - hardware
source_ids:
  - src-2026-07-03-fergus-finn-cuda-kernel
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
status: active
---

# GPU Execution Model

## Definition

The GPU execution model is the software-and-runtime path by which a written kernel becomes work running on thousands of hardware lanes: how source is compiled to device code, how the CPU submits work across the PCIe bus, how the GPU turns one linear instruction stream into a massively parallel program across its streaming multiprocessors, and how latency is hidden by scheduling many warps rather than reordering one.

## Why it matters

This is the layer between the model and the metal. [[AI Accelerator Architecture]] explains how the hardware is *designed* (arithmetic units, memory hierarchy, systolic arrays, cluster topology); the execution model explains how a program actually *runs* on it — and therefore why some kernels are compute-bound and others, like a plain vector add, are limited entirely by memory bandwidth. Understanding it is what lets you read a profiler and know whether you are FLOP-limited or byte-limited, the same distinction that governs [[LLM Inference]] and motivates [[KV Cache]] and [[Model Quantization and Efficiency]].

## Current synthesis

[[Fergus Finn - What Happens When You Run a CUDA Kernel]] traces one `vadd` kernel from `nvcc` to warps and back, making the whole path concrete.

### Compilation: virtual then real

- `nvcc` is a driver over several compilers. Device code goes `cicc` (LLVM) → **PTX** → `ptxas` → **SASS**.
- **PTX** is a virtual ISA: infinitely many typed registers, no knowledge of the hardware — it is device-agnostic and verbose (forming one address can take three instructions).
- **SASS** is the real, architecture-specific assembly; `ptxas` fuses PTX sequences (e.g. `mul.wide` + `add` into one `IMAD.WIDE`) and allocates the finite physical registers.
- Both are bundled — cubin (an ELF holding SASS) plus a PTX fallback — into a **fatbin** embedded in an ordinary host executable. If run on an uncovered architecture, the driver JITs the PTX at load time. Kernel arguments sit in **constant bank 0** because every thread reads the identical pointers (a broadcast the constant cache serves to all 32 lanes at once).

### Submission: the CPU crosses the bus

- A GPU takes no function calls; it reads driver commands from host memory across PCIe. Work is submitted through a **channel** made of a **pushbuffer** (GPU *methods* — register/value pairs) and a **GPFIFO** ring of `(base, length)` pointers into it.
- Two cursors coordinate producer and consumer: the driver advances `GP_PUT`, the GPU advances `GP_GET` (both in USERD). The launch itself is described by a **QMD** (Queue Meta Data): grid/block dimensions, registers and shared memory per thread, the program start address, and the argument constant-bank address.
- Modern host engines do not poll the cursor, so the driver rings a **doorbell** — a single MMIO store to a mapped register — to make the engine fetch the new work by DMA. `cuLaunchKernel` is **asynchronous**: it returns the instant the doorbell rings.

### Execution: one stream, many warps

- The **compute work distributor** (one per GPU) spreads blocks across the streaming multiprocessors (SMs) to keep all of them saturated. One linear SASS stream lives in VRAM, cached per-SM; each warp keeps its own program counter, so warps run the same code at different speeds or down different branches.
- **Occupancy is set by the tightest resource cap** — threads/SM, registers, or shared memory. (In the example: 256-thread blocks × 16 registers hit the 1,536-thread cap first, giving 6 resident blocks / 48 warps per SM, spread over 4 sub-partitions.)
- The GPU **hides latency by switching warps**, not by reordering instructions. `ptxas` writes per-instruction control bits: a **static stall count** for fixed-latency ops, a **yield hint**, and **scoreboard barriers** (6 per warp) for variable-latency ops like global loads. A warp waiting on a load barrier is *ineligible* and simply skipped — near-zero hardware scheduling overhead, the opposite of a CPU's out-of-order machinery.

### Why the trivial kernel is memory-bound

- 32 threads reading consecutive 4-byte floats **coalesce** into four 32-byte sector requests down L1 → L2 → GDDR6X.
- **Arithmetic intensity** is the deciding ratio: one `FADD` per 12 bytes moved is almost pure data movement, so the kernel runs at ~80% of DRAM throughput with schedulers issuing only ~5% of cycles. The result returns via a completion **semaphore** and a copy engine served from L2 without a DRAM round trip.

That ratio generalises far beyond a vector add, and [[Arithmetic Intensity and the Roofline Model]] develops it into the cross-cutting frame. Two anchors: [[Jacob Peake - AI Chip Architectures]] shows the same law selecting between whole architectures — training and prefill are compute-bound GEMMs while decode degenerates to GEMVs, and every deployed accelerator is a different strategy for the resulting data-movement problem — and [[Changyi Yang - Why MLA and MTP Fight Each Other]] shows it deciding kernel dispatch inside one model, where sglang chooses between two algebraically identical attention bracketings at a crossover of roughly 171 query tokens. The balance point on an H100 under BF16 is about **295 FLOP/byte**, which is the number the ~5% issue activity above is failing to reach by three orders of magnitude.

## Open questions

- How do compute-bound GEMMs and tensor-core kernels — the workloads that dominate real training/inference — change the scheduling, register, and shared-memory picture drawn by a memory-bound vector add?
- How much of this model shifts across generations (Ada → Hopper → Blackwell) as method classes, control-word layouts, and memory hierarchies evolve?
- Where is the crossover at which shared-memory tiling and occupancy tuning stop helping because a kernel is already bandwidth-saturated?

## Related pages

- [[Fergus Finn - What Happens When You Run a CUDA Kernel]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[AI Accelerator Architecture]]
- [[LLM Inference]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Distributed Training Parallelism]]
- [[Speculative Decoding]]
- [[AI Knowledge Base Overview]]
