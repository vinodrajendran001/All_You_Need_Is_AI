---
type: source-summary
created: 2026-08-03
updated: 2026-10-07
source_id: src-2026-07-31-giles-thomas-gpt2-weights-part-3-overtraining
source_title: "Why do OpenAI's GPT-2 weights beat mine? Part three: testing overtraining"
source_author: Giles Thomas
source_url: https://www.gilesthomas.com/2026/07/why-do-openai-gpt2-weights-beat-mine-3-overtraining
tags: [source/summary, gpt2, training, evaluation]
source_ids: [src-2026-07-31-giles-thomas-gpt2-weights-part-3-overtraining]
status: active
---

# Giles Thomas - Why GPT-2 Weights Beat Mine? Part 3: Overtraining

## Summary

The third captured post tests whether a larger pretraining budget closes Thomas's GPT-2
instruction-evaluation gap. Two longer runs lower next-token test loss and give small increases
in judge score. The author considers those increases inconclusive under his noise heuristic,
not proof that overtraining has zero effect.

## Key claims

The two new runs process **6.4B unique FineWeb tokens in one long epoch**, or the original
**3.2B tokens twice**. The comparable original JAX configuration processes 3.2B tokens once.

| Configuration | Next-token test loss | First IFT judging | Second IFT judging |
| --- | --- | --- | --- |
| Original JAX, MHA bias, no dropout | 3.418784 | 17.53 | 18.30 |
| One long epoch | 3.324953 | 18.75 | 18.45 |
| Two normal epochs | 3.326482 | 18.45 | 19.45 |

IFT scores are **GPT 5.5 grades out of 100 after Alpaca instruction fine-tuning**, not accuracy.
The first judging gives gains of **1.22 and 0.92 points** over the comparable original model.
A second judging reverses the order of the two overtrained models. Thomas treats differences
of roughly one or two points as probably noise; two runs do not establish a formal detection
threshold or a zero-effect result.

The experiment also exposes a checkpoint-selection issue: "best" had come to mean lowest loss
on changing training batches, not on a fixed validation set. The author compares candidate
checkpoints on the reported test set and uses the better-performing latest checkpoint. That
test set is therefore also used for selection, not an untouched final-only evaluation.

## Why it matters

Lower language-model loss did not establish a material improvement on this downstream judge.
The practical lesson is to match the evaluation to the intended use and characterize its
uncertainty, not to conclude that additional pretraining is useless.

## Tensions / open questions

The original GPT-2 training budget remains uncertain, and doubling Thomas's budget is not a
reproduction of it. The author explicitly says the hypothesis is **not falsified**: more training
or a more precise evaluation might resolve an effect. The capture does not provide a formal
power analysis, a matched multi-seed study, or an independent contamination audit.

## Raw capture

- [[2026-07-31 Giles Thomas - Why do OpenAI's GPT-2 weights beat mine  Part three testing overtraining|Why do OpenAI's GPT-2 weights beat mine  Part three testing overtraining]]

## Affected pages

- [[Benchmark Optimization]]
- [[LLM Training Pipeline]]
- [[LLM-as-a-Judge]]

## Citations

- Canonical URL: <https://www.gilesthomas.com/2026/07/why-do-openai-gpt2-weights-beat-mine-3-overtraining>
- Published and captured July 31, 2026.

## Related pages

- [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 1|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 1]]
- [[Giles Thomas - Why GPT-2 Weights Beat Mine Part 2 - Bugfix|Giles Thomas - Why GPT-2 Weights Beat Mine? Part 2: Bugfix]]
- [[LLM Training Pipeline]]
- [[LLM-as-a-Judge]]
