---
type: source-summary
created: 2026-08-03
updated: 2026-08-26
source_id: src-2026-04-20-moonshotai-flashkda-v1
source_title: "FlashKDA v1: A Deep Dive"
source_author: MoonshotAI
source_url: https://github.com/MoonshotAI/FlashKDA/blob/master/docs/20260420-flashkda-v1-deep-dive.md
tags: [source/summary, kernels, attention, performance]
source_ids: [src-2026-04-20-moonshotai-flashkda-v1]
status: active
---

# MoonshotAI - FlashKDA v1 Deep Dive

## Summary

FlashKDA is a fused GPU kernel implementation of Kimi Delta Attention. The report explains chunking, SM80 tensor-core mapping, bf16 persisted state with fp32 updates, and split K1/K2 kernels. Its central lesson is that recurrent-attention algorithms need numerical and memory-layout co-design to realize their theoretical efficiency.

## Key claims

- The selected `CHUNK=16` balances parallel work, register pressure, and state reuse.
- Splitting the kernel and fusing recurrent-update work reduces memory traffic; the report attributes at least a 15% end-to-end gain to its kernel strategy.
- Precision is selective: persistent state is compact, while updates preserve fp32 precision for stability.

## Affected pages

- [[Linear Attention and Recurrent Memory]]
- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]

## Citations
## Raw capture

- [[FlashKDAdocs20260420-flashkda-v1-deep-dive.md at master]]

## Related pages

- [[Linear Attention and Recurrent Memory]]
- [[GPU Execution Model]]
- [[AI Accelerator Architecture]]
