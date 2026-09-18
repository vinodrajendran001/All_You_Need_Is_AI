---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-09-18
tags: [entity, organization, models, inference]
source_ids:
  - src-2026-09-14-alphasignal-deepseek-v4-1-flash
status: active
---

# DeepSeek

## What it is

DeepSeek is an AI model developer represented in this vault through architecture, distillation,
speculative decoding, attention, and inference-efficiency discussions.

## Why it matters here

[[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]] makes DeepSeek relevant as an
example of separating total capacity from active serving cost. V4.1-Flash is described as combining
sparse experts, asymmetric prefill/decode activity, local-state replay, compressed sparse
long-context retrieval, and FP4 cache storage.

The source is secondary and contains no measured serving benchmark, so the architecture figures are
useful as a systems hypothesis rather than independent proof of cost or latency.

## Related pages

- [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]
- [[KV Cache]]
- [[Mixture of Experts]]
- [[Inference Efficiency Frontier]]
- [[Transformer Architecture]]

