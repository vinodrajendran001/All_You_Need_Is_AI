---
type: entity
created: 2026-10-16
updated: 2026-10-16
entity_kind: organization
tags: [entity, organization, energy-based-models, reasoning]
source_ids:
  - src-2026-10-12-bytebytego-energy-based-reasoning
status: active
---

# Logical Intelligence

## What it is

The company behind Kona, represented in this vault through a ByteByteGo interview with
founder Eve Bodnia about energy-based reasoning. The evidence is a secondary account of
the company's own demonstration, not an independently reproduced model evaluation.

## Why it matters here

[[ByteByteGo - How to Build Models Without Language]] motivates a separation between a
learned compatibility score, inference-time search, and an independent checker. It seeds
[[Energy-Based Model]] and extends the vault's account of reasoning without a long visible
token trace.

Kona reportedly solved **96.2%** of the Sudoku demonstration's puzzles, versus **2%** across
the compared LLM panel and **6.9%** for the best LLM. This motivates investigating constrained
specialists; it does not establish broad reasoning superiority or an inability of language
models to use search and tools.

## Notes

- The source explicitly separates its generic energy-model walkthrough from Kona's
  undisclosed implementation. Do not infer Kona's optimizer, relaxation, or losses from
  the tutorial.
- Reported GPU-time cost versus API charges, and mean runtime versus maximum runtime, have
  different denominators. They are not general price or speed multipliers.
- The account reports training on partially hidden Sudoku grids without reinforcement
  learning. It supplies neither a complete training recipe nor independent solver baselines.
- Bodnia's proposed language-interface/specialist-search division is a design direction,
  not evidence of measured cross-domain deployment performance.

## Related pages

- [[ByteByteGo - How to Build Models Without Language]]
- [[Energy-Based Model]]
- [[Latent-Space Reasoning]]
- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[ByteByteGo]]
