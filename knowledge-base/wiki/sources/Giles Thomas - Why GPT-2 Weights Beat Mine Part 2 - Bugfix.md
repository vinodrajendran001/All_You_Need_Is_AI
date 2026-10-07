---
type: source-summary
created: 2026-08-03
updated: 2026-10-07
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

The second post corrects a mutable-checkpoint bug and reruns the instruction fine-tuning baseline.
The fixes change some local-model rankings, but OpenAI's GPT-2 models remain ahead in this
evaluation. Fixing the experiment does not by itself explain the original capability gap.

## Key claims

- `model.state_dict()` supplied references to live tensors, not an immutable snapshot. Later
  training mutated the supposedly saved best state, making restoration effectively a no-op.
  `deepcopy(model.state_dict())` preserves the intended checkpoint.
- Validation had examined only **the first five batches**. The revised code uses the full
  validation set, so checkpoint restoration and stopping evaluation change together.
- The GPT 5.5 judge sees all models' answers to a question in one prompt, with order shuffled.
  This attempts to reduce comparison inconsistency; it does not establish perfect judge
  consistency or independent errors.
- OpenAI small changes **26.73 to 26.11** in mean judge score and remains rank two. The
  no-MHA-bias/no-dropout JAX model changes **14.66 to 20.72**, moving rank eleven to three.
  These are scores out of 100, not task accuracies or an isolated effect of the deep-copy fix.

## Tensions / open questions

Thomas suspects earlier dropout settings may also have differed for some JAX evaluations, but
cannot reconstruct the old commands. Judge scores vary across runs; his one-to-two-point noise
rule is a heuristic, not an estimated confidence interval. The intervention does not isolate
checkpoint copying, validation coverage, and possible configuration changes.

## Why it matters

Checkpoint immutability and validation coverage matter before interpreting a capability gap.
The corrected baseline preserves the original question while preventing future experiments from
comparing against a checkpoint that was not actually saved.

## Raw capture

- [[2026-07-31 Giles Thomas - Why do OpenAI's GPT-2 weights beat mine  Part two the bugfix|Why do OpenAI's GPT-2 weights beat mine  Part two the bugfix]]

## Affected pages

- [[LLM Training Pipeline]]

## Citations

- Canonical URL: <https://www.gilesthomas.com/2026/07/why-do-openai-gpt2-weights-beat-mine-2-the-bugfix>
- Published and captured July 31, 2026.

## Related pages

- [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 1|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 1]]
- [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 3 - Overtraining|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 3: Overtraining]]
- [[LLM Training Pipeline]]
- [[Automated AI Research]]
