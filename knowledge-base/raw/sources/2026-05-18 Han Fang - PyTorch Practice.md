---
type: raw-source
source_id: src-2026-05-18-hanfang-pytorch-practice
title: "PyTorch Practice - Learning Tutorial and Interview Prep"
author: Han Fang
url: https://github.com/hanfang/pytorch-practice
captured: 2026-05-18
status: immutable
tags:
  - pytorch
  - machine-learning
  - deep-learning
  - interview-prep
  - tutorials
---

> Composite raw-source manifest for the `pytorch-practice` repository capture. The canonical raw files are stored under `knowledge-base/raw/sources/pytorch-practice/`.

# PyTorch Practice - Learning Tutorial and Interview Prep

## What was captured

Captured a compact **7-file PyTorch tutorial repository** (**~42 KB total**) oriented toward **machine-learning engineer interview preparation**. The source is explicitly code-first: instead of long prose chapters, it teaches through runnable Python scripts that build concepts from basic tensor manipulation up through custom optimizers, attention, quantization, and training best practices.

The repository is best understood as **five progressive tutorial modules plus two support files**:
- a README that frames the curriculum and interview goals,
- five executable tutorial scripts,
- and an interactive runner that can launch the modules individually or in sequence.

## Raw location

- `knowledge-base/raw/sources/pytorch-practice/`

## File inventory

- `README.md` — Repository overview, tutorial structure, learning outcomes, interview-prep focus, setup instructions, and suggested next steps.
- `01_tensor_basics.py` — Tensor creation, shapes and dtypes, reshaping, broadcasting, indexing, NumPy interop, simple gradient examples, and optional CUDA moves.
- `02_autograd_gradients.py` — Autograd fundamentals, scalar/vector/matrix gradients, higher-order differentiation, `detach()` / `torch.no_grad()`, custom `autograd.Function`, and gradient-accumulation patterns.
- `03_neural_networks.py` — `nn.Module` basics, activations and losses, a full XOR training loop, model save/load flow, dropout, batch normalization, and parameter inspection.
- `04_interview_problems.py` — Ten interview-style implementations including numerically stable softmax, a custom `Dataset`, BatchNorm from scratch, LR schedulers, gradient clipping, multi-GPU setup, Focal Loss, initialization schemes, memory optimization, and ensembles.
- `05_advanced_topics.py` — Senior-level topics such as a custom SGD-with-momentum optimizer, multi-head attention with padding/causal masks, residual blocks with LayerNorm, warmup+cosine LR scheduling, mixed precision, hooks, profiling, dynamic graphs, quantization, and operational best practices.
- `run_tutorial.py` — Interactive CLI runner for executing all tutorial parts or selected modules.

## Pedagogical approach

This source teaches by **building implementations from scratch** and then comparing them to standard PyTorch idioms. The scripts are designed to be executed, inspected, and modified, which makes the repository useful both as a self-study path and as an interview drill source. Its durable pattern is: introduce a concept, implement it in code, print the results, and expose the operational details an interviewer is likely to ask about.

The material is practical rather than exhaustive, but it covers a strong span of foundational PyTorch knowledge: tensors, autograd, neural-network construction, optimization, normalization, attention, memory-efficiency techniques, and inference-time discipline.
