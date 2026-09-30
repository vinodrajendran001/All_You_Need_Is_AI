---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-21-tiene-pruning-llms-ising
source_title: "Pruning LLMs Like a Physicist: Block Removal as an Ising Optimization Problem"
source_author: Antonio Tiene, Ali Hashemi, David Jansen, Roman Rausch
source_url: https://huggingface.co/blog/MultiverseComputingCAI/pruning-llms-like-a-physicist-block-removal-as-an
tags: [source/summary, compression, efficiency, optimization, inference]
source_ids: [src-2026-09-21-tiene-pruning-llms-ising]
status: active
---

# Antonio Tiene et al - Pruning LLMs Like a Physicist

## Summary

Multiverse Computing researchers recast transformer block removal as constrained binary optimization
instead of independent block ranking. A second-order Taylor expansion yields an approximate Hessian
whose diagonal encodes individual block importance and whose off-diagonal terms encode interactions
between removals - the part that per-block scoring throws away. Candidate configurations are then
ranked by a cheap Ising/QUBO energy, so enormous search spaces can be explored without running the
model once per candidate. The reported gains concentrate at aggressive compression ratios.

## Key claims

- Each block gets a binary variable (**0 = keep, 1 = remove**). The objective minimizes `x^T H^0 x`
  subject to removing exactly **M of N blocks**, which is an Ising glass at fixed magnetization; the
  equivalent QUBO folds the constraint into a penalty.
- The Hessian is computed **once** from forward and backward passes on a small calibration dataset
  and is **reusable across compression targets**, because the couplings do not depend on `M`.
- Search cost collapses to one cheap energy evaluation per candidate: a few million configurations
  take **seconds**. Removing **8 of Llama-3.3-70B's 80 blocks** spans about **29 billion
  configurations** and took roughly **two days** on one GPU by brute force; an open-source tabu solver
  reached the lowest-energy states in **seconds** on the hardest cases verified by brute force.
- Llama-3.3-70B-Instruct **without retraining**, MMLU: original **82.2**; at **32/80 blocks removed**
  CBO **76.6** versus block influence **59.3**; at **40/80** CBO **76.9** versus block influence
  **54.0**. On Qwen3-14B at **12/40 removed**, CBO leads MMLU by about **10 points**.
- The lowest-energy state is **not always the best model**. On Llama-3.1-8B-Instruct at **16/32 blocks
  removed**, the **17th excited state** is the first to propose removing a block near the beginning,
  and after light retraining it outperforms the ground state across several benchmarks.
- On NVIDIA-Nemotron-3-Nano-30B-A3B-FP8, which interleaves Mamba2, attention, and MoE layers, CBO
  removes **2-3 MoE layers or 2 attention layers** and is reported to beat block influence on AIME25
  and GPQA without retraining.
- Depth pruning composes with quantization, low-rank/SVD compression, width pruning, and
  distillation-based healing.

## Why it matters

The vault's compression pages mostly treat pruning as ranking components by an importance score.
This source names the assumption that makes ranking wrong: removals interact, so the best set of `M`
blocks is generally not the `M` best blocks. The energy function is what makes the combinatorial
formulation affordable - it decouples search cost from model evaluation cost.

## Tensions and caveats

This is a company blog summarizing the authors' own paper; the derivation, ablations, solver
comparisons, calibration sensitivity, and complete tables are deferred. The authors are explicit that
the energy is a strong proxy but not an exact predictor, which the excited-state result demonstrates
against their own objective. Gains are concentrated under aggressive compression and described as
comparable at lighter ratios. The blog's headline "almost 23 percentage points" rounds a 76.9-versus-
54.0 gap of **22.9 points**. Some examples use light retraining while the main Llama-3.3 table is
explicitly without retraining; the two conditions must not be conflated. "Ising glass" is an
optimization formulation here, not a claim of quantum advantage.

## Raw capture

- [[2026-09-21 Antonio Tiene et al - Pruning LLMs Like a Physicist]]

## Affected pages

- [[Model Quantization and Efficiency]]
- [[Inference Efficiency Frontier]]
- [[Mixture of Experts]]
- [[Small Language Models]]

## Related pages

- [[LLM Inference]]
- [[Knowledge Distillation]]
- [[Transformer Architecture]]
- [[Serving Benchmarks and Goodput]]
