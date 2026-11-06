---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-10-27-morgan-train-decision-model
source_title: "Train your own decision model"
source_author: "Abby Morgan"
source_url: "https://www.comet.com/site/blog/train-a-decision-model/"
tags:
  - source/summary
  - decision-models
  - calibration
  - fine-tuning
source_ids:
  - src-2026-10-27-morgan-train-decision-model
status: active
---

# Abby Morgan - Train Your Own Decision Model

## Summary

A Comet blog tutorial that builds a small decision model to show what separates the category from an
LLM with structured output. Morgan's definition is about mechanism, not interface: a decision model
reads a probability for every declared answer in a single pass, can answer several questions about
one input without them influencing each other, and is trained so a 0.9 is right about 90% of the
time. The build uses **Qwen3-0.6B-Base** with LoRA adapters, a decision head trained from scratch,
and the public typed-decisions dataset. Training is tracked in Comet and the model is tested in
Opik. The central result is an ablation: training against the full gold distribution, rather than a
single label, produced the accuracy and calibration gains, and swapping the language-model head
for a dedicated decision head changed nothing measurable — "the readout isn't what separates them;
the loss is." Invariance tests show option order still moves the trained models' answers.

## Key claims

### What a decision model is

- A structured-output LLM generates token by token, conditions later answers on earlier ones, and
  exposes only next-token probabilities. A decision model reads all answer probabilities in one
  pass, so cost and latency depend on input length rather than answer length.
- It does an encoder's job but receives its questions and options per request, unlike a BERT
  classifier whose labels are fixed at training time. "BERT-like with modern LLM data and compute"
  is a common summary of Jev, but "TypeSafe hasn't published Jev's backbone." TypeSafe trains Jev
  with a method it calls Reinforcement Learning for Calibrated Decisions (RLCD).
- Calibration is not accuracy: a model saying 0.6 on everything and right 60% of the time is
  calibrated but useless, so "a useful decision model needs both." Calibrated probabilities let
  thresholds be set in code from error costs.

### Build mechanics

- **Data**: typed-decisions (LocalLLaMA, Apache-2.0) covers four workflows — agent-run review,
  customer support, vendor invoices, and security alerts — with five typed questions per case
  (choice, score, noul). A teacher model labeled each case three times and the gold answer is the
  average, so ambiguous cases carry spread-out targets.
- **Packing**: one state plus all five questions in a single sequence cut tokens processed by
  **2.1 times** and time per case from **329 to 175 ms** on a T4.
- **Attention mask and positions**: each question sees the state but not other questions, and its
  positions restart after the state, so an answer is the same packed or alone; the repo's tests check
  this to within floating-point error.
- **Head**: a linear layer sized for **16** options, with unused slots masked; yes/no expressed as
  `[0, z]` so all types share one loss; option order shuffled every epoch to stop slot shortcuts;
  weights initialized to zero.
- **Loss**: cross-entropy against the gold distribution, a proper scoring rule. With gold **0.9**,
  predicting 0.9 costs **0.33**, an overconfident 0.99 costs **0.47**, and a hedging 0.7 costs
  **0.44**.

### Results

| Validation | Accuracy | KL | Brier | ECE |
| --- | --- | --- | --- | --- |
| Prior (reads nothing) | 0.502 | 0.402 | 0.199 | 0.074 |
| Zero-shot baseline | 0.430 | 0.628 | 0.354 | 0.245 |
| Fine-tuned baseline (gold label, full vocabulary) | 0.714 | 0.290 | 0.119 | 0.134 |
| Baseline with the new loss (gold distribution, answer tokens) | 0.768 | 0.110 | 0.059 | 0.011 |
| Decision head | 0.757 | 0.111 | 0.061 | 0.019 |

- Changing the objective added five points of accuracy, cut KL by **62%**, and halved Brier. Every
  difference between the last two rows falls inside its 95% interval.
- Temperature scaling took the fine-tuned baseline's ECE from **0.134 to 0.027** (logits divided by
  about two); before scaling, answers given more than 90% confidence agreed with a teacher sample
  only about **81%** of the time. Models on the new loss had fitted temperatures within **8%** of 1.
- On **400** test cases in Opik: zero-shot **0.43** accuracy / **0.25** ECE; fine-tuned **0.76** /
  **0.12**; new loss **0.78** / **0.02**; decision model **0.78** / **0.02**.
- Invariance tests (total variation distance): reversing option order changed the top answer on
  **30%** of choice questions for the zero-shot baseline and **5 to 9%** for trained models. In one
  case "technical" fell from **0.96 to 0.25**. An irrelevant option took **1 to 5%** of the
  probability. Isolation shift was **0** for every model, by construction of the mask.
- `predict(state, questions)` takes and returns the same request format as Jev, so the same Opik
  experiments could run against it.

## Why it matters

[[Typed Probabilistic Decision Models]] has argued that proper scoring rules can calibrate without
RL, and records open alternatives that read answers from an option-letter softmax. Morgan supplies a
disclosed ablation, with public code and runs, that separates the readout from the objective, and it
supports both points. For [[TypeSafe AI]], it is a third-party restatement that Jev's backbone and
RLCD remain unpublished, plus an evaluation harness compatible with Jev's request format.

## Tensions / open questions

- **Vendor tutorial.** The post showcases Comet and Opik; the model is a teaching build, not a
  production decision model, and it is not compared with Jev or any hosted system.
- **Gold labels are a teacher's.** Calibration and ECE are measured against a teacher model's
  three-sample average, and "the model is only as calibrated as its training labels." No human or
  outcome ground truth is used.
- **ECE definition is custom.** It compares confidence with the chance that a teacher sample agrees
  with the top answer, so these values are not comparable with ECE figures elsewhere in the vault.
- **Small and single-dataset.** A 0.6B backbone, four workflows from one dataset, and no reported
  variance across training seeds; 95% intervals are cited only for the head-versus-loss comparison.
- **Order sensitivity persists.** Training with shuffled options still leaves **5 to 9%** top-answer
  changes when order is reversed.
- The six-alternatives-in-two-days count is attributed to Latent.Space, not verified here.

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[TypeSafe AI]]

## Raw capture

- [[knowledge-base/raw/sources/Train your own decision model]]

## Citations

- Canonical URL: <https://www.comet.com/site/blog/train-a-decision-model/> (`utm_*` parameters
  removed). Companion repository: <https://github.com/anmorgan24/decision-model>.
- By Abby Morgan, published on the Comet blog on October 27, 2026; captured November 2, 2026.

## Related pages

- [[Typed Probabilistic Decision Models]]
- [[TypeSafe AI]]
- [[Microsoft-Decision-1]]
- [[Base Labs - Mammoth-1 and Elephant-1 Decision Models]]
- [[Hamel Husain - How To Use Decision Models for Evals]]
- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[Alpha Signal - Why the Future AI Stack Needs More Than One Foundation Model]]
- [[Small Language Models]]
