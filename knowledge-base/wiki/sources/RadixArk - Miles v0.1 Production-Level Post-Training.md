---
type: source-summary
created: 2026-08-24
updated: 2026-08-26
source_id: src-2026-08-20-radixark-miles-v0-1
source_title: Miles v0.1 - Production-Level Post-Training
source_author: RadixArk
source_url: https://www.lmsys.org/blog/2026-08-18-miles-v0-1
tags: [source/summary, reinforcement-learning, post-training, ai-agents]
source_ids: [src-2026-08-20-radixark-miles-v0-1]
status: active
---

# RadixArk - Miles v0.1 Production-Level Post-Training

## Summary

Miles is a full-stack post-training system that couples SGLang rollout workers, Megatron or FSDP trainers, weight synchronization, sandboxed agent environments, and asynchronous evaluation. It targets long, variable-duration agent trajectories where synchronous generation leaves accelerators idle.

## Key claims

- Fully asynchronous rollout and training reduce blocking caused by long-tail trajectories.
- Session routing and RadixAttention reuse multi-turn prefixes while balancing load.
- Token-In-Token-Out preserves exact rollout token IDs through tool execution and message reconstruction.
- Sandboxes and environments plug into the rollout layer through shared interfaces.
- Shared, dedicated, and external evaluation modes preserve checkpoint attribution even when results arrive late.

## Why it matters

The source turns [[Agentic Reinforcement Learning]] from an algorithm diagram into an infrastructure stack and makes token fidelity, policy staleness, sandbox lifecycle, and evaluation provenance first-class.

## Tensions / open questions

- Fully asynchronous learning increases off-policy and staleness pressure.
- Production-readiness and throughput claims are project-reported.
- Black-box harnesses with subagents and compaction still require experimental trajectory-tree handling.

## Affected pages

- [[Agentic Reinforcement Learning]]
- [[Continual Learning for Agents]]
- [[Distributed Training Parallelism]]
- [[LLM Inference]]

## Citations

- Raw capture: [[2026-08-20 RadixArk - Miles v0.1 Production-Level Post-Training]]
- Repository: https://github.com/radixark/miles

## Raw capture

- [[2026-08-20 RadixArk - Miles v0.1 Production-Level Post-Training]]

## Related pages

- [[rLLM - Continual Learning via Real-Time RL for Agents]]
- [[Cameron R. Wolfe - Agentic RL Frameworks and Best Practices]]
- [[Multi-Turn Evaluation]]

