---
type: concept
created: 2026-07-03
updated: 2026-08-24
tags:
  - concept
  - training
  - distributed-training
  - parallelism
  - gpu
  - systems
source_ids:
  - src-2026-07-01-anastasiia-alekseeva-parallel-training
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-08-24-edward-yang-parallelize-transformer
status: active
---

# Distributed Training Parallelism

## Definition

Distributed training parallelism is the set of strategies for splitting a single model's training step across many accelerators when the model, its optimiser state, or its activations no longer fit — or no longer run fast enough — on one device. Each strategy partitions a different axis of the computation (examples, weight matrices, sequence positions, experts, or layers) and pays a different, characteristic communication cost.

## Why it matters

A frontier model is trained on trillions of tokens with parameters and optimiser state measured in terabytes; no single accelerator can hold or process that. Which parallelism axes you combine, and in what order, sets the ceiling on how large a model you can train and how efficiently the cluster runs. The recurring lesson (see [[AI Accelerator Architecture]]) is **compute versus communication**: modern GPUs already do the matrix arithmetic near peak, so the real limits are moving partial results between devices and keeping every device fed.

## The one invariant: GEMM independence

[[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]] grounds the whole taxonomy in one fact: the heavy work of a network is **matrix multiplication (GEMM)**, and a matrix product exposes independence that hardware can exploit. In a [[Transformer Architecture|Transformer]] layer the parallelizable axes are:

- **Across examples** — different sequences in a batch pass through the weights independently (the data-parallel axis).
- **Across weight matrices** — each GEMM can be partitioned column- or row-wise, and attention is additionally independent across heads (the tensor-parallel axis).

A product `AB` can be read column-wise (each output column needs only its own column of `B`), row-wise (each output row needs only its own row of `A`), or as an outer-product sum over the shared inner dimension. The first two need no coordination; the third forces a summation (an all-reduce). Choosing the partition is choosing the communication cost.

## Current synthesis

- **Data parallelism** replicates the full model on every device, gives each a different batch slice, and averages gradients before the optimiser step — mathematically identical to one large-batch gradient. Its weakness is memory: every device holds the whole model *state*.
- **The optimiser state is the memory villain.** Mixed-precision Adam costs **16 bytes/parameter** (2 fp16 weight + 2 fp16 gradient + 12 optimiser: fp32 master weight + two moment estimates). A 70B model therefore needs >1 TB of state per device if replicated, and 12 of the 16 bytes are optimiser state.
- **FSDP / ZeRO** shard that state (parameters, gradients, optimiser) across devices instead of copying it, so per-device memory falls roughly proportionally to the device count. Each device holds only its shard and the group **all-gathers** the full weight tensor on demand just before a layer, then discards the non-local parts. This cuts memory but not per-layer compute — every device still runs the full GEMM for its reconstructed weights. (ZeRO: Rajbhandari 2020; PyTorch FSDP: Zhao 2023.)
- **Tensor parallelism** distributes the multiplication itself. Megatron-LM (Shoeybi 2019) splits the MLP's first matrix column-wise and second row-wise so the element-wise GeLU needs no synchronisation, collapsing communication to **two all-reduces per layer in the forward pass and two in the backward** — four collectives per layer regardless of model size. Attention splits Q/K/V column-wise (each device owns whole [[Mixture of Experts|heads]]) with a row-wise output projection.
- **Sequence parallelism** removes what tensor parallelism leaves replicated. Layer norm, dropout, and residual activations (shape sequence × batch × hidden) stay duplicated on every device and dominate memory as context grows. Korthikanti (2022) shards them along the sequence dimension for free — an all-reduce equals a reduce-scatter plus all-gather, so total bandwidth is unchanged.
- **Context parallelism** handles attention over hundreds of thousands to millions of tokens, where each device otherwise needs the full sequence. **Ring Attention** (Liu, Zaharia & Abbeel 2023) streams KV blocks around a ring of devices with overlapped communication and exact online softmax; **DeepSpeed-Ulysses** (Jacobs 2023) uses all-to-all to convert sequence shards into head shards (parallelism degree capped by head count). Causal masking makes ring load-balancing non-trivial because earlier tokens attend to fewer keys.
- **Expert parallelism** is the [[Mixture of Experts|MoE]] axis: tokens must be dispatched by an all-to-all collective to whichever device holds their routed expert, then collected back — a new communication dimension layered on top of data and tensor parallelism, with expert load-balancing as the central concern.
- **Pipeline parallelism** assigns consecutive layer groups to consecutive device stages when a model is too deep for one node's tensor-parallel group. It needs only **point-to-point** communication between adjacent stages (well suited to lower-bandwidth inter-node links), divides model memory by stage count, and hides its **pipeline bubble** — idle time waiting on the previous stage — by splitting batches into micro-batches. The [[Dwarkesh Patel - Reiner Pope Flashcards]] sharpen the tradeoff: pipelining relieves weight-placement pressure but adds bubbles, gives weak relief for KV-heavy long-context work, and can even constrain model architecture.

## How the axes compose

Real frontier runs combine several axes (often called 3D or 4D parallelism): data parallelism across replicas, tensor + sequence parallelism inside a node, expert parallelism for MoE layers, and pipeline parallelism across nodes. The [[AI Accelerator Architecture|hardware topology]] decides where each boundary should sit — e.g., an MoE all-to-all wants a single NVLink-connected rack, while pipeline point-to-point tolerates slower cross-node links. The design goal is always the same: maximise multiplications running in parallel while minimising coordination.

[[Edward Z. Yang - How to Parallelize a Transformer for Training]] turns this composition problem into an interactive roofline exercise. Instead of prescribing one mesh, it estimates parameter, optimizer, gradient, and activation memory; FLOPs; collective communication; network domains; and pipeline bubbles for a specific model and cluster. The practical rule is to place communication-intensive axes such as tensor parallelism inside the fastest topology, then use sharding or pipelines to cross slower boundaries only when memory or scale requires them. The model remains an estimate: kernels, contention, load imbalance, and framework overhead still require profiling.

## Open questions

- What are the crossover points at which one parallelism axis should replace or augment another for a given model shape, context length, and cluster?
- How do the axes interact under real load-balancing and fault-tolerance pressure, especially MoE routing skew and pipeline bubbles at scale?
- How much of the memory story changes as optimiser-state compression, 8-bit optimisers, and lower-precision training mature (see [[Model Quantization and Efficiency]])?

## Related pages

- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]]
- [[LLM Training Pipeline]]
- [[Mixture of Experts]]
- [[AI Accelerator Architecture]]
- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]
- [[Model Quantization and Efficiency]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[GPU Execution Model]]
- [[AI Knowledge Base Overview]]
- [[Edward Z. Yang - How to Parallelize a Transformer for Training]]
