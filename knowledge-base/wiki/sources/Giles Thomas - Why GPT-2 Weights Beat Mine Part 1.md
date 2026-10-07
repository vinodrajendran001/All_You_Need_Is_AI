---
type: source-summary
created: 2026-08-03
updated: 2026-10-07
source_id: src-2026-07-29-giles-thomas-gpt2-weights-part-1
source_title: "Why do OpenAI's GPT-2 weights beat mine?"
source_author: Giles Thomas
source_url: https://www.gilesthomas.com/2026/07/why-do-openai-gpt2-weights-beat-mine-1-intro
tags: [source/summary, gpt2, training, evaluation]
source_ids: [src-2026-07-29-giles-thomas-gpt2-weights-part-1]
status: active
---

# Giles Thomas - Why GPT-2 Weights Beat Mine? Part 1

## Summary

Thomas opens a reproduction investigation: some of his models have lower FineWeb next-token loss
than OpenAI's GPT-2 small, yet score worse **after a separate instruction fine-tuning procedure**.
The two evaluations have different targets. This post contains the original diagnostic baseline;
Part 2 later corrects the checkpoint/evaluation code and changes some numbers without closing the
OpenAI gap.

## Key claims

The IFT procedure fine-tunes each base model on an Alpaca subset until validation loss rises,
generates answers for a held-out instruction test split, and uses **GPT 5.5** to assign scores
out of 100. Those judge scores are not percentages of questions answered correctly.

Selected **pre-fix** rows from Part 1:

| Model | FineWeb test loss | Mean IFT judge score |
| --- | --- | --- |
| OpenAI GPT-2 small | 3.499677 | 26.73 |
| JAX, MHA bias, no dropout | 3.418784 | 19.25 |
| Cloud FineWeb, 8x A100 40 GiB | 3.673623 | 20.71 |

The lowest-loss local model is not the best local model on the instruction judge. Model size is
also not matched: OpenAI small uses weight tying and about **124M parameters**, versus roughly
**163M** in Thomas's models. The OpenAI medium row is a larger comparison, not an equal-size control.

Thomas considers pretraining data quality, dropout, and training beyond his roughly **3.2B-token**
budget as hypotheses. WebText is unavailable, and one weak dropout result does not rule out
dropout generally. Faster arrival at rising validation loss is an observation, not proof of the
proposed loss-landscape explanation.

## Why it matters

The case distinguishes base-model language loss, subsequent instruction adaptation, and a
fallible judge of generated answers. It motivates task-specific evaluation without proving that
next-token loss is useless or that a particular architecture caused the gap.

## Tensions / open questions

Use [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 2 - Bugfix]] for the corrected baseline.
The original table must not be mixed with later judge runs as if their scores were calibrated
absolute measurements. The result is an individual reproduction investigation, not a controlled
comparison of every difference in size, data, initialization, or training recipe.

## Affected pages

- [[LLM Training Pipeline]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]

## Raw capture

- [[2026-07-31 Giles Thomas - Why do OpenAI's GPT-2 weights beat mine|Why do OpenAI's GPT-2 weights beat mine]]

## Citations

- Canonical URL: <https://www.gilesthomas.com/2026/07/why-do-openai-gpt2-weights-beat-mine-1-intro>
- Published July 29 and captured July 31, 2026.

## Related pages

- [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 2 - Bugfix|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 2: Bugfix]]
- [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 3 - Overtraining|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 3: Overtraining]]
- [[LLM Training Pipeline]]
- [[LLM-as-a-Judge]]
