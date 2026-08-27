---
type: source-summary
created: 2026-08-24
updated: 2026-08-26
source_id: src-2026-08-24-edward-yang-parallelize-transformer
source_title: How to Parallelize a Transformer for Training
source_author: Edward Z. Yang
source_url: https://thinkingmachines.ai/blog/definitive-guide-to-parallelizing-transformers/
tags: [source/summary, distributed-training, transformers, performance]
source_ids: [src-2026-08-24-edward-yang-parallelize-transformer]
status: active
---

# Edward Z. Yang - How to Parallelize a Transformer for Training

## Summary

Edward Z. Yang presents an interactive roofline model for selecting and composing data parallelism, FSDP, tensor parallelism, expert parallelism, and pipeline parallelism. The central method is to model memory, compute, collective communication, topology, and batch constraints together rather than apply a fixed recipe.

## Key claims

- Parallelism choices trade replicated memory, sharded state, communication volume, and implementation complexity.
- Tensor parallelism is communication-intensive and best confined to high-bandwidth domains.
- FSDP reduces memory through sharding but introduces all-gather and reduce-scatter traffic.
- Expert parallelism is natural for MoE layers but must control load imbalance and all-to-all cost.
- Pipeline parallelism helps span slower network boundaries but introduces bubbles and scheduling constraints.
- The best mesh depends on model shape, sequence length, batch size, hardware, and network topology.

## Why it matters

The article upgrades [[Distributed Training Parallelism]] from a glossary into a quantitative decision process grounded in an explicit transformer and network model.

## Tensions / open questions

- Simplifying assumptions can miss kernel inefficiency, contention, failures, and framework overhead.
- Real training plans still require profiling and implementation-specific validation.
- Recommendations age with interconnects, kernels, and model architectures.

## Affected pages

- [[Distributed Training Parallelism]]

## Citations

## Raw capture

- [[2026-08-24 Edward Z. Yang - How to Parallelize a Transformer for Training]]

## Related pages

- [[Agentic Reinforcement Learning]]
- [[Model Quantization and Efficiency]]
- [[ML Systems at Scale]]
- [[Mixture of Experts]]
- [[Software Performance Engineering]]

