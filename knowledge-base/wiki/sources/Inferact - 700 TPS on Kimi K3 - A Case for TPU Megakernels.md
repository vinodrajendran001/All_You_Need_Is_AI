---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-28-inferact-tpu-megakernels-kimi-k3
source_title: "700 TPS on Kimi K3: A Case for TPU Megakernels"
source_author: Inferact
source_url: https://inferact.ai/blog/tpu-megakernels
tags: [source/summary, kernels, tpu, accelerators, inference, speculative-decoding]
source_ids: [src-2026-09-28-inferact-tpu-megakernels-kimi-k3]
status: active
---

# Inferact - 700 TPS on Kimi K3: A Case for TPU Megakernels

## Summary

Inferact reports open-source TPU v7 megakernels for Kimi K3 and Qwen 3.8 27B that collapse the whole
decoder into a single Pallas kernel. The design leans on TPU's software-managed VMEM: weights are
prefetched by program-issued asynchronous HBM-to-VMEM DMA that overlaps with computation, including
across layer boundaries. Inferact reports higher small-batch decode throughput than a published
GB200/vLLM recipe, with the largest margin at batch size 1. The results are vendor-reported and
specialized to one model, one topology, and small-batch decode.

## Key claims

- The megakernel is a single grid-less TPU program with explicit VMEM lifetimes managed via Pallas
  `run_scoped`, replacing kernel boundaries with cross-layer scheduling.
- TPU v7 exposes **64 MiB of VMEM per TensorCore** and **128 MiB per chip, addressed as two pools**,
  against GB200's **~111 MiB of SRAM, split 152 ways** (**256 KB Tensor Memory** and **228 KB shared
  memory per SM** across **152 SMs**, **~38 MiB** Tensor Memory per GPU).
- Headline hardware figures: TPU v7 at **2.31 PFLOPS BF16 / 4.61 PFLOPS FP8 / 206 GB HBM /
  7,380 GB/s HBM / 1,200 GB/s ICI** versus GB200 at **2.5 PFLOPS BF16 / 5 PFLOPS FP8 / 186 GB HBM /
  8,000 GB/s HBM / 1,800 GB/s NVLink 5**. TPU is behind on both peak FLOPS and HBM bandwidth.
- Kimi K3 has **92 MoE layers**; the kernel uses **16 TPU v7 chips / 32 TensorCores** in a **2x2x4**
  topology, attention split across **32 ranks**, routed experts at **TP4 x EP8**.
- Without speculation, TPU versus GB200 tokens/s: batch 1 **249 vs 127 (1.96x)**, batch 2
  **392 vs 227 (1.73x)**, batch 4 **515 vs 373 (1.38x)**, batch 8 **865 vs 636 (1.36x)**. The
  advantage shrinks monotonically as batch size grows.
- With speculative decoding the megakernel acts as verifier, evaluating **1 anchor and 7 proposed
  continuations** per launch at batch 8, with a **~8.5 ms** decode step and a draft model typically
  yielding **3 to 6 accepted tokens per step**. At acceptance length 3: **350 vs 229 tokens/s
  (1.53x)**; at acceptance length 6: **709 vs 452 tokens/s (1.57x)**.
- Qwen 3.8 27B with speculation at acceptance length 6: **1,515 tokens/s on 4x TPU v7** versus
  **695 tokens/s on 4x GB200 (2.18x)**.
- The entire megakernel compiles in **less than 90 seconds**, against **30+ minutes** regularly seen
  for a large XLA model.
- Validation under greedy decoding at maximum reasoning effort: **0.944 on GPQA-Diamond** and
  **0.972 on GSM8K**.

## Why it matters

The vault's megakernel evidence has been GPU-centric. This source argues the technique is a better
fit on TPU precisely because VMEM is large and software-managed, so the prefetch schedule the
programmer must write by hand on a GPU is the native programming model on a TPU. It also supplies a
clean statement of where the win lives: a memory-bandwidth-bound regime at small batch, degrading as
concurrency rises and vector arithmetic plus inter-device traffic take over.

## Tensions and caveats

Inferact compares its own hand-written TPU kernel against a published vLLM GB200 recipe, which is not
a symmetric baseline. There is no independent reproduction, no confidence interval, no energy or
cost-per-token figure, and no full methodology. The headline "over 700 tokens/s" requires speculative
decoding at a favorable acceptance length, not ordinary decode. The "nearly 2x" claim is the
batch-one no-speculation case only. The accuracy numbers are sanity checks against numerical
regression, not evidence of parity across broad evaluation. The collectives are topology-specific, so
other chip arrangements need new code.

## Raw capture

- [[2026-09-28 Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]

## Affected pages

- [[Megakernels]]
- [[AI Accelerator Architecture]]
- [[GPU Kernel Optimization]]
- [[Serving Benchmarks and Goodput]]
- [[Mixture of Experts]]
- [[NVIDIA]]

## Related pages

- [[LLM Inference]]
- [[Inference Efficiency Frontier]]
- [[Accelerator Software Externalization]]
- [[Speculative Decoding]]
