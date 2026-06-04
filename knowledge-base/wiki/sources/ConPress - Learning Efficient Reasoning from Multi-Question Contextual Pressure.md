---
type: source-summary
created: 2026-06-04
updated: 2026-06-04
source_id: src-2026-06-04-conpress
source_title: "ConPress: Learning Efficient Reasoning from Multi-Question Contextual Pressure"
source_author: Jie Deng et al.
source_url: https://arxiv.org/abs/2602.01472
tags:
  - source-summary
  - reasoning
  - self-supervision
  - cot
source_ids:
  - src-2026-06-04-conpress
status: active
---

# ConPress: Learning Efficient Reasoning from Multi-Question Contextual Pressure

## Summary

ConPress is built around a striking empirical observation: when a model must answer multiple independent questions in one prompt, it often **self-compresses** its reasoning traces. The paper turns that phenomenon into a training signal by generating multi-question prompts, extracting concise per-question traces, and using them for self-supervised fine-tuning in ordinary single-question settings.

## Key claims

- Multi-question prompts create contextual pressure that naturally shortens reasoning traces without external teachers.
- This self-compression effect is reproducible across models and benchmarks, not just a one-off artifact.
- The method avoids RL, manual pruning, and external teacher models; it relies on self-generated compressed reasoning data.
- With only a small fine-tuning set, the paper reports large reductions in reasoning tokens while maintaining competitive accuracy on MATH500 and AIME25.

## Why it matters

ConPress adds a distinct family to the vault's compression branch: efficient reasoning learned from **contextual pressure and self-supervision**, rather than reward design or handcrafted compression targets.

## Tensions / open questions

- Why does multi-question contextual pressure induce shorter traces so reliably?
- Does self-compression preserve correctness on tasks that are less modular than math problems?
- How far can this idea scale before multi-question prompting becomes its own source of interference?

## Affected pages

- [[Reasoning Compression]]
- [[LLM Training Pipeline]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-06-04 Jie Deng et al - ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure.md`
- Local PDF: [2026-06-04 Jie Deng et al - ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure.pdf](../../raw/sources/2026-06-04%20Jie%20Deng%20et%20al%20-%20ConPress%20-%20Learning%20Efficient%20Reasoning%20from%20Multi-Question%20Contextual%20Pressure.pdf)

## Related pages

- [[Reasoning Compression]]
- [[LLM Training Pipeline]]
- [[Efficient Reasoning on the Edge]]
