---
type: source-summary
created: 2026-08-03
updated: 2026-09-13
source_id: src-2026-07-27-waterloo-intern-gpt2-to-kimi-k3
source_title: "22580: From GPT2 to Kimi3, Explained"
source_author: "@waterloo_intern"
source_url: https://x.com/waterloo_intern/status/2081762065392541951
tags: [source/summary, kimi, moe, attention, social-post]
source_ids: [src-2026-07-27-waterloo-intern-gpt2-to-kimi-k3]
status: active
---

# @waterloo_intern - From GPT-2 to Kimi K3

## Summary

This visual social-media explainer uses the jump from GPT-2 to Kimi K3 as a lens on modern
architecture: sparse mixture-of-experts capacity, hybrid attention/recurrent memory, and
systems-aware long-context inference.

## Key claims

- The headline comparison is **2.8 trillion parameters** for Kimi K3 versus roughly **124 million**
  for GPT-2 — about **22,580x** as many total parameters.
- Total parameters do not equal active compute in a sparse MoE; only selected experts run for each
  token.
- Hybrid attention/recurrent mechanisms change the long-context cost profile relative to dense
  attention over every token.

## Why it matters

The parameter ratio explains the title but not practical serving cost. Architecture determines how
much of the 2.8T capacity activates and how recurrent state replaces or complements attention.

## Tensions / open questions

- The architecture and performance figures are frontier claims from a secondary explainer and need
  verification against primary technical reports.
- The 22,580x figure compares total parameter counts, not active parameters, FLOPs, memory traffic,
  training data, or capability.

## Raw capture

- [[2026-07-29 @waterloo_intern - 22580 From GPT2 to Kimi3, Explained|22580 From GPT2 to Kimi3, Explained]]

## Affected pages

- [[Linear Attention and Recurrent Memory]]
- [[Mixture of Experts]]

## Related pages

- [[Mixture of Experts]]
- [[Transformer Architecture]]
- [[LLM Inference]]
