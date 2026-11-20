---
type: concept
created: 2026-11-20
updated: 2026-11-20
tags:
  - concept
  - quantization
  - training
  - distributed-training
source_ids:
  - src-2026-11-13-thinking-machines-end-to-end-4-bit-training
  - src-2026-11-05-huggingface-moe-training-handbook
  - src-2026-11-02-anil-compute-islands
status: active
---

# Low-Precision Training

## Definition

Low-precision training runs some of a model's training arithmetic or communication in formats
narrower than BF16. Today that means FP8 variants such as MXFP8 and 4-bit block-scaled formats such
as NVFP4. The format is part of the training recipe, not a compression step after training.
Deployment-side compression is covered in [[Model Quantization and Efficiency]].

## Why it matters

Narrower formats run faster on current accelerators and move fewer bytes. On GB300, NVFP4 is listed
at **15** PFLOPS against **5** for MXFP8 and **2.5** for BF16, per
[[Thinking Machines - End-to-End 4-Bit Training]]. Rounding errors still accumulate across layers and
steps, so the useful question is *where* in training low precision is safe.

## Current synthesis

- **Error and bias are different risks.** Thinking Machines separates the two. Forward passes and RL
  sampling mainly need low error. Backward passes and the RL trainer need low bias, meaning values
  that consistently round one way, because bias "can compound across layers, samples, and training
  steps".
- **Keep the sensitive parts wider.** [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]]
  keeps the router, norms and attention core in higher precision under FP8. It relays the Megatron
  Core team's figure of about **10 to 25%** more end-to-end throughput on a large MoE. It also relays
  that Nemotron 3 Super's NVFP4 pretraining kept the last **15%** of the network in BF16. Thinking
  Machines keeps the last **16.6%** of layers in MXFP8 and puts NVFP4 only in expert-layer forward
  passes. Neither source ablates the cut-off.
- **The transpose problem.** Block scales are computed along one axis. The backward pass needs the
  transpose, which groups values along the other axis. Thinking Machines found NVIDIA's 16×16-tile fix
  "too coarse" and instead re-quantizes with stochastic rounding (SR), which keeps forward and
  backward copies equal in expectation.
- **Faster math moves the bottleneck to the wire.** Once the expert GEMMs got faster, expert-parallel
  communication limited Thinking Machines' MoE layer. Quantized dispatch (NVFP4) and combine (a
  Hadamard transform plus S2F6) followed. [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
  also compressed cross-site transfers, with stochastic rounding plus error feedback. See
  [[Distributed Training Parallelism]].
- **RL is where it is most contested.** The handbook relays a Qwen study in which NVFP4 rollouts
  against a BF16 trainer collapsed after about **150** steps. Thinking Machines reports "no
  discernible difference in reward" with one numerics recipe shared by sampler and trainer. Both
  results are unreplicated in the vault, and the two setups differ in more than numerics.
- **Determinism is a by-product worth tracking.** Thinking Machines describes its kernel stack, BBBK,
  as "fully deterministic", and says per-token outer scales give "batch-invariance". See
  [[Inference Determinism]].

All figures are first-party or relayed. No source in the vault gives an independent ablation.

## Open questions

- How much of a theoretical speedup survives end to end? Thinking Machines cites about 3× for the MoE
  forward pass but **8%** for pretraining wall-clock.
- Does a shared numerics recipe between sampler and trainer explain the different RL outcomes, or do
  model and setup differences?
- Can backward passes go to FP4? Thinking Machines names this as its next step.
- How portable are recipes that depend on vendor-specific instructions (SR, S2F6, K=96 UMMA)?

## Related pages

- [[Model Quantization and Efficiency]]
- [[LLM Training Pipeline]]
- [[Distributed Training Parallelism]]
- [[Mixture of Experts]]
- [[NVIDIA]]
- [[Thinking Machines]]
- [[Inference Determinism]]
- [[GPU Kernel Optimization]]
- [[Thinking Machines - End-to-End 4-Bit Training]]
- [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]]
- [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
