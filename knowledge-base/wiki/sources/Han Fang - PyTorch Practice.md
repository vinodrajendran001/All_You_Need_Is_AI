---
type: source-summary
source_id: src-2026-05-18-hanfang-pytorch-practice
source_title: "PyTorch Practice - Learning Tutorial and Interview Prep"
source_author: Han Fang
source_url: https://github.com/hanfang/pytorch-practice
created: 2026-05-18
updated: 2026-05-18
tags:
  - source-summary
  - pytorch
  - machine-learning
  - deep-learning
  - interview-prep
source_ids:
  - src-2026-05-18-hanfang-pytorch-practice
status: active
---

# Han Fang - PyTorch Practice

## Overview

This source is a compact **code-first PyTorch curriculum** organized into **five progressive modules**: tensor basics, autograd, neural networks, interview problems, and advanced topics. The repository is explicitly interview-oriented, but its main value for this vault is broader: it turns core deep-learning ideas into runnable scripts that show how implementations actually behave.

The teaching style is unusually durable for a wiki because the source does not just describe APIs; it repeatedly builds mechanisms from scratch—softmax, BatchNorm, SGD with momentum, attention, schedulers, and quantization-adjacent workflows—then places them back inside standard PyTorch training loops.

## Durable claims

1. **Numerically stable softmax subtracts `max(x)` before exponentiation** so large logits do not overflow during `exp`.
2. **Broadcasting rule example:** tensors shaped `(3, 1)` and `(1, 3)` broadcast to `(3, 3)`, making row/column expansion a core tensor-manipulation pattern.
3. **Gradient accumulation works by dividing the loss by the number of accumulation steps and delaying `optimizer.step()`** until all micro-batches have contributed gradients.
4. **Focal Loss down-weights easy examples** by multiplying BCE-with-logits loss with an `(1 - pt)^gamma` factor (optionally scaled by `alpha`).
5. **Weight initialization is architecture-sensitive:** Xavier initialization is used for linear layers, while Kaiming initialization is used for convolution layers paired with ReLU.
6. **Custom BatchNorm uses batch statistics during training and running statistics during evaluation**, while keeping learnable scale/shift parameters (`gamma`/`beta`, implemented here as weight/bias).
7. **Multi-head attention splits projected Q, K, and V into `(batch, heads, seq, d_k)` tensors** and applies scaled dot-product attention independently per head before concatenation.
8. **Warmup + cosine annealing schedules are two-phase:** linearly ramp learning rate for `warmup_steps`, then decay toward `min_lr` with a cosine curve.
9. **Dynamic quantization to `qint8` is presented as a major model-size reduction lever**—roughly the expected 4× storage drop from fp32 to int8—with only small output/accuracy degradation.
10. **Correct inference requires both `model.eval()` and `torch.no_grad()`**: the first switches module behavior (for example Dropout/BatchNorm), while the second avoids unnecessary gradient tracking.

## Content map

- `README.md` — Frames the repository as a runnable PyTorch tutorial for learning plus interview prep, with coverage extending from tensors to attention, quantization, and debugging.
- `01_tensor_basics.py` — Covers tensor creation, tensor metadata, reshaping, slicing, broadcasting, concatenation/stacking, NumPy interop, CUDA moves, and a first `requires_grad` example.
- `02_autograd_gradients.py` — Explains how PyTorch computes gradients for scalars, vectors, and matrices; shows higher-order gradients; and demonstrates gradient-flow control with `detach()` and `torch.no_grad()`.
- `03_neural_networks.py` — Shows how `nn.Module` packages layers and forward passes, how common activations/losses fit into training loops, and how the full optimization cycle works on an XOR problem.
- `04_interview_problems.py` — Collects ten high-signal interview exercises: stable softmax, custom data pipelines, BatchNorm from scratch, LR schedulers, clipping, multi-GPU wrapping, Focal Loss, initialization, gradient accumulation/checkpointing, and ensembles.
- `05_advanced_topics.py` — Extends the curriculum into custom optimizers, masked multi-head attention, residual connections with LayerNorm, warmup/cosine scheduling, mixed precision, hooks, profiling, dynamic graphs, quantization, and best practices.
- `run_tutorial.py` — Adds a lightweight interactive runner for executing one module or the full series.

## Why it matters

This source strengthens the vault's practical PyTorch layer. [[The Pocket - PocketFlow Tutorial Docs]] already provides broad tutorial coverage across neural networks, Transformers, training, and efficiency; Han Fang's repository complements that breadth with a **single coherent interview-drill repo** full of runnable Python examples. It is especially useful where this vault needs concrete reference implementations rather than conceptual summaries.

## Affected pages

- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]
- [[Model Quantization and Efficiency]]
- [[LLM Training Pipeline]]
- [[AI Knowledge Base Overview]]
- [[index|Knowledge Base Index]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-05-18 Han Fang - PyTorch Practice.md`
- Raw file directory: `knowledge-base/raw/sources/pytorch-practice/`

## Related pages

- [[Han Fang]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]
- [[Model Quantization and Efficiency]]
- [[LLM Training Pipeline]]
- [[AI Knowledge Base Overview]]
