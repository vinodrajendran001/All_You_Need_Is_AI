---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-12-schulz-tvb-filler-token-reasoning
source_title: "LLMs can learn (some) multi-step reasoning on filler tokens"
source_author: "Wuschel Schulz and tvb"
source_url: "https://www.lesswrong.com/posts/EHkwCDAmhWPAWEziM/llms-can-learn-some-multi-step-reasoning-on-filler-tokens-2"
tags:
  - source/summary
  - reasoning
  - chain-of-thought
  - monitoring
  - safety
source_ids:
  - src-2026-11-12-schulz-tvb-filler-token-reasoning
status: active
---

# LLMs Can Learn (Some) Multi-Step Reasoning on Filler Tokens

## Summary

A LessWrong research update by Wuschel Schulz and tvb, from a project in MARS 5 and the Meridian
Visiting Researcher Programme. **Filler-token reasoning** means a model uses extra token positions to
compute an answer while the words at those positions carry nothing; the canonical filler is a run of
"." tokens. Attention can move information between positions without routing it through the emitted
words, so the dots give the model "more parallel, but not more serial, computation".

The reference point is Pfau, Merrill & Bowman's 2024 "Let's Think Dot by Dot" paper. It trained models
from scratch on fully parallelizable (TC⁰) tasks and argued that filler tokens cannot help beyond TC⁰,
because serial tasks did not train. Schulz and tvb change the training method and report that LoRA
fine-tunes of **Qwen3.6-35B-A3B** and **gpt-oss-20b** do learn multi-step tasks on filler tokens: "two
models and three out of seven multi-step reasoning tasks". They pair this with an upper-bound analysis
of how many transformer layers each task needs. Their stated motivation is methodological. Their main
research is **steganographic reasoning** (reasoning hidden inside innocuous-looking text), and
filler-token reasoning is a confound they must rule out before crediting a hidden channel in the words.

## Key claims

### The training change

- Pfau et al. trained models to output dots then the answer, mixed with open-reasoning samples. Here
  the dots are the **input** and the open reasoning is the **target**: at each dot position the label is
  one reasoning step. The authors note that the trained models "are no longer next-token predictors";
  their chains of thought must be **prefilled** with dots, "since they would be reasoning openly
  otherwise".
- They train **rank-32 LoRAs** on existing LLMs rather than training from scratch.
- Two regimes: a **curriculum** that lengthens the task once answer accuracy reaches **0.9**, and
  **direct** training at full length (100 steps by default, shorter for some tasks). Each curriculum stage
  uses **2,000** examples, evaluates on 20 items every 100 steps, and the final evaluation uses **200**
  items.

### Seven synthetic tasks

Mod sum (running sum modulo n), A5 (a ball under five cups through shuffles), GL(3,2) (three lamps
under two moves), modular arithmetic (chains of +, −, × modulo 8), ProntoQA (chained "every A is a B"
rules, adjusted to remove shortcuts), HornQA (Horn-clause rules "A and B ⇒ C", described as
P-complete) and function composition (a value pushed through 8-entry lookup tables). Unbounded numbers
in the reasoning are encoded in binary, a constraint inherited from the steganography setting.

### Filler tokens beat answer-only on the tested combinations

Three model/task combinations (mod sum and GL(3,2) on Qwen3.6-35B-A3B, mod sum on gpt-oss-20b) were
trained with the authors' method, Pfau et al.'s method and an **answer-only** baseline, on the same
10 → 20 → 40-step curriculum with the same examples per stage, using "at least 3 different seeds". The
decision rule is stated in advance: beating answer-only counts as filler-token reasoning. The text says
their method "clearly beats the answer-only baseline" and Pfau et al.'s does not. The per-seed values
are in a chart that the capture does not reproduce as numbers.

### Theory: depth grows with task length, but sublinearly

- The authors define a bounded-precision transformer in the spirit of RASP. Attention copies a value
  exactly only when it matches a single earlier position; otherwise it can only count matches. MLPs act
  as lookup tables. They implement this as an executable program, have **swarms of Opus 5.5 agents**
  search for the shallowest algorithm for each task, check each submission for correctness and allowed
  operations, and score it by layer count.
- Limits differ by architecture, so the analysis was run per model. Most of Qwen3.6-35B-A3B's layers
  use linear attention, modelled as "a memory that returns the most recent matching entry" (see
  [[Linear Attention and Recurrent Memory]]); half of gpt-oss-20b's layers "only see a window of recent
  positions".
- Some limits were "chosen by fiat". In particular the MLP lookup input is capped at **32 bits**, which
  sets the slope of every curve. The authors expect the shape, not the slope, to survive other choices.
- Results are **upper bounds, not minima**. No task was fully parallelized; every algorithm gets deeper
  as tasks lengthen. For all but HornQA, depth grows "much more slowly than the number of steps", which
  is why models can do **more reasoning steps than they have layers**. Mod sum, the main task in two
  earlier steganography papers (Skaf et al. 2025; Zolkowski et al. 2025), "scales very gently".
- They note that "in theory parallelizable" (TC⁰) and "parallelizable in an actual transformer" differ:
  a limited-precision transformer cannot solve arbitrarily long mod-2 sums in one forward pass.

### Empirical limits do not match theory

The longest length learned on filler tokens is compared against answer-only fine-tuning (same
curriculum) and open reasoning (trained directly at the longest length), taking the best across both
filler methods and multiple seeds. HornQA "fails after very few steps", as theory predicted. Mod sum is
"learned very easily". But **modular arithmetic and function composition "hit a wall at 1–3 steps"**
despite being theoretically easy. The authors' reading: models struggle "when large packets of
information (lookup tables, premises,...) need to be transported across token positions". This is a
pattern they observe, not a tested mechanism.

### Conclusion and implication for monitoring

Pfau et al.'s limit "holds in the limit of infinitely long tasks", but "since even small models can
learn to do 60 steps on filler tokens, this may not be much comfort in practice". The authors cite Nanda
(2026) that recent models such as Astra show an increased ability to answer reasoning questions
without reasoning about them. If that continues, it "could endanger CoT monitorability even without
the specters of looped architectures or steganographic reasoning coming true". They also argue that
"any pressure not to verbalize certain multi-step reasoning could, with enough training, lead to
similar results". Their practical recommendation is that researchers studying steganographic or
encoded reasoning put their tasks through a test like this, because some tasks they started with
"did not get harder with more steps at all".

## Why it matters

[[Chain-of-Thought Monitoring]] assumes that serial work a model needs shows up in its written trace.
This source reports a third route, beside steganography and architectural depth, by which useful serial
computation can sit across token positions while the words say nothing. It also gives monitoring
research a confound check: a model that writes unrelated text and then answers correctly has not
necessarily hidden reasoning in the text.

For [[Latent-Space Reasoning]], it adds a mechanism the page lacks. The vault's existing argument is
about computation *per token* (looped or larger models may need fewer visible tokens). Filler tokens
instead add *positions* whose content is meaningless, and the source shows sublinear-depth circuits
using them for multi-step tasks. It also tempers the idea that hidden computation is unbounded: depth
still grows with task length, and tasks that move large packets of information across positions failed
almost at once.

## Tensions / open questions

- **Non-standard training.** The authors say so directly: the protocol "is not normally part of an LLM
  training pipeline", the models are no longer next-token predictors, and the dots must be prefilled.
  The result shows learnability under this protocol, not that deployed models do this.
- **Small, first-party, mostly chart-reported.** Training runs are "quite small". The headline
  comparison covers three model/task combinations with at least 3 seeds each, and its per-seed results
  and the longest learned lengths live in figures the capture does not give as numbers.
- **"Three out of seven" is not itemized.** The text names mod sum and GL(3,2) as learned and HornQA,
  modular arithmetic and function composition as hard. It does not name the third learned task in prose;
  A5 or ProntoQA would be an inference from the charts.
- **The "60 steps" figure is not otherwise sourced in the text.** Direct training defaults to 100 steps and
  the curriculum demonstration stops at 40. Where 60 comes from is presumably a chart.
- **"40 or 24 steps".** The theory section says the depth curves stay below the model's depth "far
  beyond 40 or 24 steps". The capture does not explain the two numbers; they may be the two models' layer
  counts, but the source does not state this.
- **Theory is an upper bound with a chosen constant.** The 32-bit lookup limit was picked by fiat, and
  agent-found algorithms are not proven optimal. A lower bound for any task is not given.
- **Capture losses.** The GL(3,2) encoding example ends "would be encoded as )" with the number missing,
  and the appendix's MLP input limit appears as a blank "( )". The summary does not fill them.
- **Secondhand trend.** The claim that Astra-class models show an increased ability to answer
  without reasoning is attributed to Nanda (2026) and not measured here. The vault's
  [[Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]] records a lab statement
  that Astra's monitorability regression is not contingent on architecture; this source's argument is
  compatible with that but does not test it.

## Affected pages

- [[Chain-of-Thought Monitoring]]
- [[Latent-Space Reasoning]]

## Raw capture

- [[knowledge-base/raw/sources/LLMs can learn (some) multi-step reasoning on filler tokens]]

## Citations

- Canonical URL: <https://www.lesswrong.com/posts/EHkwCDAmhWPAWEziM/llms-can-learn-some-multi-step-reasoning-on-filler-tokens-2>
  (the captured link carried a `utm_source=tldrai` parameter, removed here).
- Authors as captured: Wuschel Schulz and tvb (LessWrong usernames). Published 2026-11-12; captured
  2026-11-20. The `source_id` date is the publication date.
- Code and agent-constructed algorithms are linked from the post at
  `github.com/stegano-ai/filler-token-reasoning`; they were not inspected for this summary.
- Cited works named in the capture: Pfau, Merrill & Bowman (2024); Saparov & He; Skaf et al. (2025);
  Zolkowski et al. (2025); Weiss, Goldberg & Yahav (2021, RASP); Nanda (2026).

## Related pages

- [[Chain-of-Thought Monitoring]]
- [[Latent-Space Reasoning]]
- [[LLM Reasoning]]
- [[Reasoning Compression]]
- [[Transformer Architecture]]
- [[Linear Attention and Recurrent Memory]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Sebastian Raschka - OpenAI Astra and Looped Transformers]]
- [[Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]]
- [[Melody Guan et al - Complementary Metrics for Monitorability]]
- [[Alex Wang - What Objective Is Reasoning Solving]]
