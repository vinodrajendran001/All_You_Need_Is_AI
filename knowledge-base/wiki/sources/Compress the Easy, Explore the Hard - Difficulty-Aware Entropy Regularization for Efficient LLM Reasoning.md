---
type: source-summary
created: 2026-06-04
updated: 2026-06-04
source_id: src-2026-06-04-difficulty-aware-entropy-regularization
source_title: "Compress the Easy, Explore the Hard: Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning"
source_author: Qin-Wen Luo et al.
source_url: https://arxiv.org/abs/2602.22642
tags:
  - source-summary
  - reasoning
  - rl
  - entropy
source_ids:
  - src-2026-06-04-difficulty-aware-entropy-regularization
status: active
---

# Compress the Easy, Explore the Hard: Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning

## Summary

This paper argues that many RL-based compression methods fail because they collapse exploration too early. Its proposed method, **CEEH**, keeps a broader search distribution on hard questions through difficulty-aware entropy regularization while still compressing easy ones aggressively. It also adds a length target anchored to the historically shortest correct response.

## Key claims

- Length pressure alone can create entropy collapse, especially on hard questions that still need exploration.
- Compression should depend on question difficulty: easy prompts can be shortened more aggressively than hard ones.
- Entropy regularization and length penalties need to work together, or the model either becomes too verbose or too brittle.
- Across multiple reasoning benchmarks, the paper reports shorter responses with base-model-level accuracy and better Pass@k than length-only optimization.

## Why it matters

CEEH strengthens the view that efficient reasoning is as much about **preserving the right search space** as it is about cutting tokens. It is a reminder that shorter traces are only useful if the model still explores enough to find them.

## Tensions / open questions

- How stable is difficulty estimation during RL as the policy itself changes?
- Do entropy-based fixes remain effective on models that already under-explore?
- How much of the observed gain comes from the shortest-correct-response anchor versus the entropy regularization itself?

## Affected pages

- [[Reasoning Compression]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-06-04 Qin-Wen Luo et al - Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning.md`
- Local PDF: [2026-06-04 Qin-Wen Luo et al - Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning.pdf](../../raw/sources/2026-06-04%20Qin-Wen%20Luo%20et%20al%20-%20Compress%20the%20Easy,%20Explore%20the%20Hard%20-%20Difficulty-Aware%20Entropy%20Regularization%20for%20Efficient%20LLM%20Reasoning.pdf)

## Related pages

- [[Reasoning Compression]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[Efficient Reasoning on the Edge]]
