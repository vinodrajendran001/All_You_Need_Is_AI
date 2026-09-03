---
type: entity
entity_kind: person
created: 2026-09-03
updated: 2026-09-03
tags: [entity, author, inference, serving]
source_ids:
  - src-2026-09-02-baseten-efficient-frontier-inference
status: active
---

# Philip Kiely

Writer at [[Baseten]] and author of the free book *Inference Engineering*.

## Why they matter to this vault

[[Philip Kiely - The Efficient Frontier of LLM Inference]] gave the vault a **classifier** for inference
optimizations rather than another catalogue of them: does a technique move a deployment *along* the
latency-throughput frontier, or push the **frontier out**? That distinction became
[[Inference Efficiency Frontier]] and now organises material the vault had documented only technique by
technique.

Two secondary contributions are load-bearing. The observation that **the frontier is jagged** — cutoffs are
unintuitive and must be found by empirical sweeps — implies that any published single-configuration benchmark
describes a chosen point rather than a capability. And the argument that **speculative decoding has changed
category**, from tradeoff technique to frontier-moving one, partially revises the framing on
[[Speculative Decoding]].

## Caveats

The author writes for an inference vendor; the post links Baseten's own EAGLE-3 and DFlash work throughout and
closes by promoting his book. No measurements are given — every claim is directional, and the compounding 4×
example is illustrative arithmetic.

## Related pages

- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
- [[Baseten]]
- [[Inference Efficiency Frontier]]
- [[Speculative Decoding]]
- [[LLM Inference]]
- [[Prefill-Decode Disaggregation]]
