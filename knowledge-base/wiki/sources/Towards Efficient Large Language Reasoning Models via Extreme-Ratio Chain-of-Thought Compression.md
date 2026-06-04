---
type: source-summary
created: 2026-06-04
updated: 2026-06-04
source_id: src-2026-06-04-extreme-ratio-cot-compression
source_title: Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression
source_author: Yuntian Tang et al.
source_url: https://arxiv.org/abs/2602.08324
tags:
  - source-summary
  - reasoning
  - compression
  - cot
source_ids:
  - src-2026-06-04-extreme-ratio-cot-compression
status: active
---

# Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression

## Summary

This paper tackles the "high compression ratio" regime directly. Its claim is that most CoT compression methods fail not because compression is impossible, but because they lose too much logical fidelity when token budgets become very small. The proposed **Extra-CoT** pipeline uses a learned compressor, mixed-ratio SFT, and a hierarchical RL objective to train models that can operate under aggressive compression budgets without collapsing answer quality.

## Key claims

- High-ratio CoT compression usually fails because supervision is not semantically faithful enough at extreme budgets.
- A dedicated semantically preserved compressor can create better compressed supervision than crude truncation or weak heuristics.
- Mixed-ratio SFT teaches a model to respond under a spectrum of compression budgets instead of one fixed target.
- Hierarchical ratio-aware RL further encourages solving the task under low budgets, and the paper reports strong token reduction with slight accuracy gains on MATH-500.

## Why it matters

Extra-CoT pushes the vault's efficient-reasoning branch toward **extreme compression**, where the question is no longer whether a model can be shorter, but whether it can stay logically reliable when most of the visible trace disappears.

## Tensions / open questions

- How much of the gain comes from the learned compressor versus the mixed-ratio fine-tuning and RL stages?
- Do extreme-ratio traces stay interpretable enough to be audited by humans?
- Are math-centered compression gains transferable to broader reasoning or agent tasks?

## Affected pages

- [[Reasoning Compression]]
- [[LLM Training Pipeline]]
- [[Reward Design for RL]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-06-04 Yuntian Tang et al - Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression.md`
- Local PDF: [2026-06-04 Yuntian Tang et al - Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression.pdf](../../raw/sources/2026-06-04%20Yuntian%20Tang%20et%20al%20-%20Towards%20Efficient%20Large%20Language%20Reasoning%20Models%20via%20Extreme-Ratio%20Chain-of-Thought%20Compression.pdf)

## Related pages

- [[Reasoning Compression]]
- [[LLM Training Pipeline]]
- [[Reward Design for RL]]
- [[Efficient Reasoning on the Edge]]
