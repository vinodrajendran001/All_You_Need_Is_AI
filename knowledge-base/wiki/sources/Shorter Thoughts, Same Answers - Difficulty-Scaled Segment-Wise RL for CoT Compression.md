---
type: source-summary
created: 2026-06-04
updated: 2026-06-04
source_id: src-2026-06-04-dss-grpo-cot-compression
source_title: "Shorter Thoughts, Same Answers: Difficulty-Scaled Segment-Wise RL for CoT Compression"
source_author: Ye Tian and Aijun Liu
source_url: https://arxiv.org/abs/2603.07598
tags:
  - source-summary
  - reasoning
  - rl
  - grpo
source_ids:
  - src-2026-06-04-dss-grpo-cot-compression
status: active
---

# Shorter Thoughts, Same Answers: Difficulty-Scaled Segment-Wise RL for CoT Compression

## Summary

This paper focuses on a specific failure mode of RL-based compression: when compression pressure applies at the whole-completion level, it can accidentally shorten the final answer along with the thinking trace. Its proposed solution, **DSS-GRPO**, splits the return into think and answer segments, applies group-relative advantages separately, and uses hard token masks so only the reasoning segment is compressed.

## Key claims

- The shortest sufficient reasoning trace depends on prompt difficulty, so fixed targets are brittle.
- Whole-completion RL signals leak across the think/answer boundary and can damage answer behavior.
- Segment-wise GRPO with masked routing can compress reasoning tokens while preserving answer alignment.
- Difficulty-aware scaling further adjusts compression pressure so harder prompts are not over-shortened.

## Why it matters

This source adds a more fine-grained view of efficient reasoning: the object being optimized is not just "the completion" but **different functional parts of the completion** with different objectives.

## Tensions / open questions

- How robust is the think/answer boundary in models that do not use a stable explicit formatting convention?
- Do segment-wise masks still work well once reasoning becomes partially latent or compressed into non-text state?
- How much extra training complexity is justified by preserving answer behavior more cleanly?

## Affected pages

- [[Reasoning Compression]]
- [[Reward Design for RL]]
- [[Group Relative Policy Optimization]]
- [[LLM Training Pipeline]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-06-04 Ye Tian et al - Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression.md`
- Local PDF: [2026-06-04 Ye Tian et al - Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression.pdf](../../raw/sources/2026-06-04%20Ye%20Tian%20et%20al%20-%20Shorter%20Thoughts,%20Same%20Answers%20-%20Difficulty-Scaled%20Segment-Wise%20RL%20for%20CoT%20Compression.pdf)

## Related pages

- [[Reasoning Compression]]
- [[Reward Design for RL]]
- [[Group Relative Policy Optimization]]
- [[LLM Training Pipeline]]
- [[Efficient Reasoning on the Edge]]
