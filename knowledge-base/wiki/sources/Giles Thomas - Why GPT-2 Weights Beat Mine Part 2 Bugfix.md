---
type: source-summary
created: 2026-08-03
updated: 2026-08-26
source_id: src-2026-07-31-giles-thomas-gpt2-weights-part-2-bugfix
source_title: "Why do OpenAI's GPT-2 weights beat mine? Part two: the bugfix"
source_author: Giles Thomas
source_url: https://www.gilesthomas.com/2026/07/why-do-openai-gpt2-weights-beat-mine-2-the-bugfix
tags: [source/summary, gpt2, training, evaluation]
source_ids: [src-2026-07-31-giles-thomas-gpt2-weights-part-2-bugfix]
status: active
---

# Giles Thomas - Why GPT-2 Weights Beat Mine? Part 2: Bugfix

## Summary

The second post finds an experimental bug: checkpoint state was not deeply copied, so a saved best-model reference could be mutated by later training. It also replaces a partial validation check with full-set evaluation.

## Why it matters

The result is a concrete reproducibility warning: checkpoint immutability and complete validation matter before interpreting capability gaps as architectural or data effects.

## Raw capture

- [[2026-07-31 Giles Thomas - Why do OpenAI's GPT-2 weights beat mine  Part two the bugfix|Why do OpenAI's GPT-2 weights beat mine  Part two the bugfix]]

## Affected pages

- [[LLM Training Pipeline]]

## Related pages

- [[Giles Thomas - Why GPT-2 Weights Beat Mine? Part 1]]
- [[Giles Thomas - Why GPT-2 Weights Beat Mine? Part 3: Overtraining]]
- [[LLM Training Pipeline]]
- [[Automated AI Research]]
