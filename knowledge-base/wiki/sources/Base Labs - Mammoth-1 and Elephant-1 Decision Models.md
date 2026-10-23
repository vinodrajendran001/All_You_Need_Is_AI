---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-21-baselabs-mammoth-elephant
source_title: "Mammoth-1 and Elephant-1: frontier decision models"
source_author: "Max Kirkby, Michael Psenka, Thomas Villeneuve, Aaryam Sharma, and Charles O'Neill"
source_url: https://labs.baseten.co/articles/mammoth-1-and-elephant-1-frontier-decision-models
tags: [source/summary, decision-models, synthetic-data, training, evaluation]
source_ids:
  - src-2026-10-21-baselabs-mammoth-elephant
status: active
---

# Base Labs - Mammoth-1 and Elephant-1 Decision Models

## Summary

Base Labs' first-party technical report on **elephant-1 (9B)** and **mammoth-1 (27B)**,
post-trained from Qwen3.5. It discloses a fixed-option readout, block-bidirectional full
attention, a **6.21M-example** data mixture, uncertainty-target construction, and a combined
cross-entropy/Brier objective. The most transferable lesson is a measured data-repair loop,
not the time-sensitive "best in the world" framing.

## Key claims

**Readout and cache boundary.** A shared prefix contains system instructions and state;
each question has a suffix with instructions and letter-labeled options. A softmax over
option-letter logits at the answer position yields probabilities without generating answer
text. The prefix is processed once; additional questions still require a suffix forward pass.
No generated answer does not mean no inference computation.

**Architecture.** Only full-attention layers become block-bidirectional: prefix tokens see
the prefix, suffix tokens see the prefix and their whole suffix. The prefix cannot see a
question, preserving cache reuse across questions. Gated DeltaNet layers stay causal.
The 27B model has **64 layers**, sixteen repeats of three recurrent layers plus one full
attention layer; 9B has **32 layers**, eight repeats.

A matched-data, **single-run** attention comparison on a public **10k** Jev sample reports
**44.8 causal versus 48.6 block-bidirectional**. It is more isolated than the mixture-history
comparison, but has no repeated-seed uncertainty estimate.

**Output semantics.** Choice supports **1-255** options; Yes/no returns P(true); Score
uses **2-10** levels and reports a distribution and expected level. Choice confidence is
`(max(p) - 1/k) / (1 - 1/k)`, distinct from the winning probability. The text says
calibration is trained and evaluated on **p**, not this confidence. The formula is undefined
at the allowed **k=1** boundary; the clipping does not supply that special case.

**Training data and filtering.** Final rows: **3.62M** core decision skills, **1.00M**
safety/abstention, **1.00M** judging/expert domains, and **0.59M** public decision examples.
Synthetic examples pass independent labeling (deterministic truth or at least **4 of 5**
judges agreeing after option shuffling), ambiguity rejection, benchmark-overlap removal,
an agent's shortcut audit, and a **240-step** pilot before inclusion. Public data keeps
original labels and joins at the final stage; not all 6.21M rows are synthetic.

| Mixture history, 9B | Rows | Reported public-suite score |
| --- | --- | --- |
| Mix 1 | 254k | 45.5 |
| Mix 2, also changes attention | 662k | 54.3 |
| Mix 4 | 4.19M | 66.0 |
| Mix 5, source repairs and abstention training | 4.35M | 71.5 |
| Mix 7, audit of all 253 sources | 5.98M | 73.9 |
| Mix 8, rewritten refusal/uncertainty/safety data plus new rows | 6.21M | 74.0 |

These are the authors' **public v0.3 runs excluding HLE**, not the private v0.4 leaderboard.
Mix 5 gains **5.5 points** with about **4%** more rows, but changes several ingredients;
it does not isolate cleaning alone. The prose also calls the final public-board result
**72.2**, without fully reconciling it with the table's **74.0**. Both are retained as
different reported figures, not silently merged.

**Uncertainty training.** On a dedicated subset, randomly add an "I don't know" option and
sometimes remove the correct answer. Relabel to abstention if the correct answer is absent
or its probability is below a threshold reported as a little under **0.5**. This is a
training-label construction, not a deployment-wide threshold recommendation.

Both models receive one epoch of full fine-tuning with the vision encoder frozen, using
cross-entropy plus Brier loss with **lambda=1**. Training is **text-only**; image/video
training and vision-board evaluation are future work. Training uses **128 H100s** for 9B
and **72 GB300s** for 27B; this report supplies no comparable serving-cost measurement.

| Result | Evidence boundary |
| --- | --- |
| Mammoth **71.24**, Elephant **62.65** | Reported Jev Decision Index **0.4 private Full** scores; Mammoth #1 of 208 at release |
| Mammoth **65.9**, Elephant **65.2** | Authors' replica of Artificial Analysis Decision Index |
| Elephant **65**, tied with d1-ultra | Reported official Artificial Analysis result; not the replica's 65.2 |

## Why it matters

[[Typed Probabilistic Decision Models]] gains a disclosed architecture and training recipe,
not just another API-compatible product. [[Synthetic Data Flywheel]] gains a concrete
quality-control loop with option-shuffle checks and source pilots. [[Baseten]] and [[Qwen]]
connect serving expertise, weight reuse, and a changed output contract.

## Tensions / open questions

- The authors assert zero benchmark contamination after deduplication; this is not an
  independent audit. Repeated evaluation-guided source generation can still overfit task
  families without copying benchmark items.
- Cross-entropy plus Brier is an objective, not a demonstrated local calibration curve.
  The capture provides no numerical held-out calibration result for choosing action thresholds.
- Public mixture runs, public-board prose, private leaderboard results, and the official
  versus replicated Artificial Analysis scores have different protocols.
- "Automating the data loop" end to end, looped inference, and multimodal training are
  proposed next steps, not demonstrated results.
- Released weight links do not establish license terms or quality under a particular
  deployment; model artifacts were not separately inspected or executed here.

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[Synthetic Data Flywheel]]
- [[Baseten]]
- [[Qwen]]

## Raw capture

- [[Mammoth-1 and Elephant-1 frontier decision models]]

## Citations

- Max Kirkby, Michael Psenka, Thomas Villeneuve, Aaryam Sharma, Charles O'Neill:
  <https://labs.baseten.co/articles/mammoth-1-and-elephant-1-frontier-decision-models>.
- Published October 21; captured October 23, 2026. The capture also cites
  <https://labs.baseten.co/058>. Tracking query removed from summary metadata.
- Linked weights: <https://huggingface.co/baselabs/mammoth-1> and
  <https://huggingface.co/baselabs/elephant-1>; not separately ingested.

## Related pages

- [[Typed Probabilistic Decision Models]]
- [[Synthetic Data Flywheel]]
- [[Baseten]]
- [[Qwen]]
- [[Model Routing]]
- [[LLM-as-a-Judge]]
- [[KV Cache]]
