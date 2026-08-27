---
type: source-summary
created: 2026-07-03
updated: 2026-08-26
source_id: src-2026-07-01-anastasiia-alekseeva-parallel-training
source_title: "The Simple Maths Behind Parallel Traning"
source_author: Anastasiia Alekseeva
source_url: https://www.linkedin.com/pulse/simple-maths-behind-parallel-traning-anastasiia-alekseeva-oqhye/
tags:
  - source/summary
  - training
  - distributed-training
  - parallelism
  - gpu
source_ids:
  - src-2026-07-01-anastasiia-alekseeva-parallel-training
status: active
---

# Anastasiia Alekseeva - The Simple Maths Behind Parallel Training

## Summary

This LinkedIn essay derives every major distributed-training strategy from a single premise: the heavy work of a neural network is **matrix multiplication (GEMM)**, everything else (bias adds, norms, activations) is rounding error, and a GPU exists to exploit the independence hidden in those matrix products. It starts from the 2009 Raina/Madhavan/Ng result (a 45M-parameter net trained 12–72× faster on a GeForce GTX 280 than on CPU) and scales the same insight up to frontier clusters.

The article then walks each parallelism axis in order of the bottleneck it removes: **data parallelism** (batch across devices) and its memory fix **FSDP/ZeRO** (shard weights + gradients + optimiser state); **tensor parallelism** (Megatron-LM's column-then-row split of each GEMM so only two all-reduces per layer are needed); **sequence parallelism** (shard the layer-norm/dropout/residual activations tensor parallelism leaves replicated); and, when even those are not enough, **context parallelism** (Ring Attention, DeepSpeed-Ulysses), **expert parallelism** (MoE all-to-all dispatch), and **pipeline parallelism** (layer-group stages with micro-batches to shrink the bubble). The closing thesis: arithmetic is never the bottleneck; coordination and keeping every device fed is.

## Key claims

- **GEMM is the whole game.** The vast majority of GPU time in a neural net is matrix multiplication; the axes of independence in a Transformer layer are across examples (data parallelism) and across weight matrices / attention heads (tensor parallelism).
- **Data parallelism** gives each GPU a full model copy and a different batch slice, then averages gradients — mathematically identical to one big-batch gradient because examples are independent.
- **The memory villain is optimiser state.** Mixed-precision Adam costs 16 bytes/param (2 fp16 weight + 2 fp16 grad + 12 optimiser), so a 70B model needs >1 TB/device if replicated; the 12 optimiser bytes dominate.
- **FSDP/ZeRO** (ZeRO: Rajbhandari 2020, arXiv:1910.02054; FSDP: Zhao 2023, arXiv:2304.11277) shards that state so per-device memory drops ~proportionally to GPU count; weights are all-gathered on demand per layer and discarded after use. It cuts memory but not per-layer compute.
- **Tensor parallelism** (Megatron-LM, Shoeybi 2019, arXiv:1909.08053) splits MLP matrix A column-wise and B row-wise so the element-wise GeLU needs no sync, giving just **two all-reduces per layer forward + two backward**. Attention splits Q/K/V column-wise (each device owns whole heads) with a row-wise output projection.
- **Tensor parallelism's leftover cost is activation memory:** layer norms, dropout, and residual paths stay replicated; **sequence parallelism** (Korthikanti 2022, arXiv:2205.05198) shards them along the sequence dimension with no extra bandwidth (all-reduce = reduce-scatter + all-gather).
- **Very long context breaks attention itself:** **Ring Attention** (Liu, Zaharia & Abbeel 2023, arXiv:2310.01889) streams KV blocks around a ring with overlapped comms and exact online softmax; **DeepSpeed-Ulysses** (Jacobs 2023, arXiv:2309.14509) all-to-alls sequence shards into head shards (degree capped by head count).
- **Expert parallelism** (MoE; Shazeer 2017, arXiv:1701.06538) adds all-to-all token dispatch as a new communication dimension; **pipeline parallelism** (GPipe, Huang 2019, arXiv:1811.06965) assigns layer groups to stages, needs only point-to-point links (good for lower-bandwidth inter-node), and hides its bubble with micro-batches.

## Why it matters

This is the vault's first source that lays out the **full parallelism taxonomy** end to end and grounds it in the one invariant (GEMM independence). It seeds the new concept [[Distributed Training Parallelism]] and connects the training-stage view in [[LLM Training Pipeline]] with the hardware view in [[AI Accelerator Architecture]] (the "compute vs communication" law) and the sparse-model view in [[Mixture of Experts]] (expert parallelism). It also gives concrete memory arithmetic (16 bytes/param for Adam) that complements [[Model Quantization and Efficiency]] and the where-the-GEMMs-live map in [[Transformer Architecture]].

## Tensions / open questions

- The article is a conceptual explainer; it gives no throughput/scaling-efficiency numbers or the crossover points where one parallelism axis should replace another.
- Real frontier runs compose several axes at once (3D/4D parallelism); the interactions, load-balancing, and failure modes are only gestured at.
- The published date field in the capture reads `2001-06-28` (an obvious typo; the content and `created` date place it in mid-2026).

## Affected pages

- [[AI Accelerator Architecture]]
- [[Distributed Training Parallelism]]
- [[LLM Training Pipeline]]
- [[Mixture of Experts]]
- [[NVIDIA]]
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]

## Citations
- Source URL: [https://www.linkedin.com/pulse/simple-maths-behind-parallel-traning-anastasiia-alekseeva-oqhye/](https://www.linkedin.com/pulse/simple-maths-behind-parallel-traning-anastasiia-alekseeva-oqhye/)

## Raw capture

- [[2026-07-01 Anastasiia Alekseeva - The Simple Maths Behind Parallel Traning|The Simple Maths Behind Parallel Traning]]

## Related pages

- [[Distributed Training Parallelism]]
- [[LLM Training Pipeline]]
- [[Mixture of Experts]]
- [[AI Accelerator Architecture]]
- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[AI Knowledge Base Overview]]
