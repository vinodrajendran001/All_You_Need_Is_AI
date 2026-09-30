---
type: concept
created: 2026-06-03
updated: 2026-09-30
tags:
  - concept
  - llm
  - moe
  - efficiency
  - sparse-models
source_ids:
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-07-01-anastasiia-alekseeva-parallel-training
  - src-2026-07-03-bytebytego-thinking-machines-interaction
  - src-2026-07-27-waterloo-intern-gpt2-to-kimi-k3
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-09-14-alphasignal-deepseek-v4-1-flash
  - src-2026-09-21-bytebytego-big-model-cheap-hardware
  - src-2026-09-28-inferact-tpu-megakernels-kimi-k3
  - src-2026-09-21-tiene-pruning-llms-ising
status: active
---

# Mixture of Experts

## Definition

Mixture of Experts (MoE) is a sparse-model architecture where only a subset of specialized sub-networks, or experts, is activated for a given token or input instead of executing the full parameter set every time.

## Why it matters

MoE matters because it changes the tradeoff between **total model capacity** and **active inference cost**. A model can be large enough to store more capability while only paying the compute and memory price of a smaller active subnetwork on each step.

## Current synthesis

- The Reiner Pope flashcards show the systems side of MoE: expert routing is an all-to-all communication pattern, which makes rack topology and interconnect bandwidth first-class design constraints.
- The Liquid AI LFM2.5 source shows the product side: an 8B total / 1B active model can still feel fast enough for laptop and phone deployment while preserving a larger capacity budget than a similarly cheap dense model.
- That makes MoE a different kind of efficiency lever from quantization or KV caching:
  - **Quantization** shrinks stored precision.
  - **KV cache** avoids recomputing old attention state.
  - **MoE** reduces the amount of the network that is active per token.
- MoE also changes the economics of explicit reasoning. Liquid AI argues that sparse models can afford more reasoning tokens because each step is cheaper than in a dense model with similar total capacity.
- The downside is routing and systems complexity. Sparse models only deliver their theoretical win if runtimes, kernels, memory layout, and cluster topology support efficient expert dispatch.
- MoE therefore lives at the boundary of architecture and infrastructure: it is both a model design choice and a deployment problem.
- **Expert parallelism** is the training-side face of that boundary. [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]] frames MoE as its own axis of [[Distributed Training Parallelism]]: because only a fraction of experts fire per token, capacity can grow without proportional compute — but tokens must be dispatched by an **all-to-all** collective to whichever device holds their routed expert and collected back, adding a new communication dimension on top of data and tensor parallelism, with expert load-balancing as the central concern (this is why the [[AI Accelerator Architecture|Reiner Pope flashcards]] place an MoE layer inside one NVLink rack).
- **Interaction models are pushing sparse scale into real-time serving.** [[ByteByteGo - Inside Thinking Machines Interaction Models|Thinking Machines' TML-Interaction-Small]] is a 276B-parameter MoE with only 12B active, deliberately sized so the *active* cost stays inside a 200 ms latency budget — a concrete demonstration that MoE's total-vs-active split is what makes a large model viable for [[Real-Time Voice AI]].
- **Headline parameter growth can conceal a different execution model.** [[@waterloo_intern - From GPT-2 to Kimi K3]] contrasts Kimi K3's 2.8T total parameters with GPT-2's roughly 124M — about 22,580x — but Kimi activates sparse experts and mixes recurrent with full-attention layers. The ratio describes stored capacity, not per-token FLOPs or memory traffic, and comes from a secondary explainer rather than a primary benchmark.

## The systems layer MoE actually runs on

[[Wafer - AI Performance Engineering Resources]] treats MoE primarily as a distributed-systems problem, which is where most of the difficulty lives once the routing algorithm is fixed. **DeepSeek-V3** is its reference report for a large sparse model end to end; **DeepEP** is the expert-parallel communication library that makes all-to-all dispatch and combine affordable; **EPLB** is the expert-parallel load balancer that keeps hot experts from serializing the step; **MegaScale-Infer** addresses serving disaggregation for MoE specifically.

The pattern is that sparsity converts a compute problem into a *communication and balance* problem. Every token's route decides which GPU does its work, so an imbalanced router costs wall-clock time on every device that finished early — a cost entirely invisible in FLOP accounting. That is the same accounting gap [[Arithmetic Intensity and the Roofline Model]] warns about, one level up the stack.

## Active capacity split by inference phase

[[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]] reports a 552B DeepSeek V4.1-Flash
backbone with 384 routed experts but only **8B active parameters per input token** and **16B per
generated token**. The asymmetry reinforces that "active parameters" is not one model-wide number;
prefill and decode can activate different computation. The figures remain secondary reporting until
checked against DeepSeek's primary technical report.

## Sparse execution still needs dense storage accounting

[[ByteByteGo - How to Run a Big Model on Cheap Hardware]] uses a hypothetical 40B MoE at 4 bits to
show that low active parameters do not remove roughly 20 GB of resident raw weights. Sparse routing
reduces token compute; offloading, sharding, or memory capacity must still solve total storage.

## An expert layer is a partitioning unit at serving time and a removable unit at compression time

Two September 2026 sources treat MoE layers as objects to be placed and objects to be deleted, and
reading them together complicates the total-versus-active framing above.

**Placement.** [[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]] reports fitting **Kimi
K3's 92 MoE layers** onto **16 TPU v7 chips / 32 TensorCores in a 2x2x4 topology**, with attention
split across **32 ranks** and routed experts at **TP4 x EP8**, all inside one megakernel. This is the
page's all-to-all claim in its most literal form: the collectives are written against that specific
chip arrangement, so any other chip *topology* — including a different arrangement of the same 16
chips — needs new collectives. The reported decode advantage over a
published vLLM GB200 recipe is **249 vs 127 tokens/s at batch 1 without speculation (1.96x)**,
shrinking monotonically to **865 vs 636 (1.36x) at batch 8** — vendor-reported, and consistent with
this page's claim that sparsity converts a compute problem into a communication problem, since
Inferact attributes the decay to vector arithmetic and inter-device traffic taking over as batch
grows.

**Removal.** [[Antonio Tiene et al - Pruning LLMs Like a Physicist]] approaches an MoE layer from the
other side, as a block that can be dropped. On **NVIDIA-Nemotron-3-Nano-30B-A3B-FP8**, a hybrid that
interleaves Mamba2, attention and MoE layers, the authors' constrained binary optimization selects
**2-3 MoE layers or 2 attention layers** for removal and is reported to beat a block-influence
baseline on AIME25 and GPQA **without retraining**. The method's central claim is that removals
interact, so the best set of M blocks is generally not the M best blocks — which for a hybrid model
means "how much MoE can go" is not answerable one layer at a time.

That sits awkwardly beside this page's usual account, and the tension is worth keeping rather than
smoothing. The total-versus-active split treats the expert layers as where capacity is stored and
routing as the mechanism that rations it per token. If whole MoE layers can be removed without
retraining and still beat a block-influence baseline on two benchmarks — the blog publishes no
unpruned scores, so the absolute cost is unknown — then part of that capacity *may* be redundant at
the *layer* level, not merely unused per token — a different kind of slack than sparse routing is
designed to exploit.

Both readings need their caveats. Inferact's numbers are batch-1-to-8 decode on one model, one
topology, against an asymmetric baseline. Tiene et al. is a Multiverse Computing blog summarizing the
authors' own
paper, with ablations, solver comparisons and complete tables deferred; "removes 2-3 MoE layers"
describes what the optimizer selected on one hybrid model, not a general redundancy rate for MoE.

## Open questions

- When does the routing overhead outweigh the compute saved by sparsity?
- Which applications benefit most from MoE: long-context assistants, agentic tool use, multilingual models, or something else?
- How much of future sparse-model progress will depend on better runtimes rather than better expert architectures?
- If whole MoE layers can be removed without retraining at a cost the source does not quantify, where does the redundancy live — in the experts, in the router, or in the residual stream that routes around them?
- Does deleting MoE layers improve the all-to-all picture by removing dispatch rounds, or only shrink stored weights while leaving the per-token communication pattern intact?
- Expert-parallel layouts are written against a fixed topology (Inferact's TP4 x EP8 on 2x2x4). Is there a portable way to express MoE collectives, or is per-deployment kernel work the standing cost of sparsity?

## Related pages

- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[Model Quantization and Efficiency]]
- [[AI Accelerator Architecture]]
- [[Distributed Training Parallelism]]
- [[Real-Time Voice AI]]
- [[AI Agents in Production]]
- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]]
- [[ByteByteGo - Inside Thinking Machines Interaction Models]]
- [[@waterloo_intern - From GPT-2 to Kimi K3]]
- [[Liquid AI]]
- [[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]
- [[Antonio Tiene et al - Pruning LLMs Like a Physicist]]
- [[Megakernels]]
- Wafer - AI Performance Engineering Resources
- Prefill-Decode Disaggregation
