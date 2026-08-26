---
type: concept
created: 2026-08-03
updated: 2026-08-03
tags: [concept, transformers, attention, memory]
source_ids:
  - src-2026-07-27-neural-avb-looped-transformers
  - src-2026-07-27-waterloo-intern-gpt2-to-kimi-k3
  - src-2026-04-20-moonshotai-flashkda-v1
status: active
---

# Linear Attention and Recurrent Memory

Linear-attention and recurrent-memory architectures replace token-addressable attention state with a fixed-size state updated as tokens arrive. They trade exact retrieval of an arbitrary earlier token for bounded memory and potentially linear-time sequence processing.

## Current synthesis

- Looped transformers repeatedly apply shared blocks, trading depth-specific parameters for more recurrent computation.
- Delta and gated-delta updates aim to control interference as new information overwrites the state.
- Hybrid designs periodically retain full attention, reserving token-addressable retrieval for positions where recurrence is insufficient.
- Kimi Delta Attention and FlashKDA belong to the systems side of this branch: architecture choices only become useful at scale when the recurrent update is implemented as a numerically stable, fused kernel.

## Related pages

- [[@neural_avb - What Are Looped Transformers?]]
- [[@waterloo_intern - From GPT-2 to Kimi K3]]
- [[MoonshotAI - FlashKDA v1 Deep Dive]]
- [[Recursive Architectures]]
- [[Transformer Architecture]]
- [[KV Cache]]
- [[LLM Inference]]
