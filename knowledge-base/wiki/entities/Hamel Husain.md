---
type: entity
created: 2026-10-23
updated: 2026-11-20
entity_kind: person
tags:
  - entity
  - evaluation
  - llm-applications
source_ids:
  - src-2026-10-20-husain-decision-model-evals
  - src-2026-11-19-shankar-husain-evals-three-gulfs
status: active
---

# Hamel Husain

## What it is

Co-author, with Shreya Shankar, of the O'Reilly book *Evals for AI Engineers* (see Notes), and author
of **"How To Use Decision Models for Evals"**, the first source in this vault to use
[[Typed Probabilistic Decision Models]] as **automated evaluators** and then carry out the unglamorous
work the category usually skips: tuning the decision threshold on labeled data, checking whether the
returned probabilities are calibrated, and pricing the result.

## Why it matters here

The contribution is **methodological rather than conceptual**, which is exactly what the vault's
evaluation pages were missing.

**The default threshold is an arbitrary inheritance.** A model returning a failure probability is
conventionally thresholded at 0.50, and Husain's work treats that as a parameter to be fit on labeled
data under an explicit business rule — in his example, at least 80% precision and 80% recall — using
stratified five-fold cross-validation with thresholds chosen on training folds and measured on held-out
folds. The constrained procedure's feasibility is itself a signal: it fell back to unconstrained F1 in
36 of 100 training splits for one model and 0 of 100 for another.

**A number between 0 and 1 is not a probability.** One score group averaged a predicted failure
probability of about 8% while 60% of those traces actually contained failures. This is the sharpest
demonstration in the vault that calibration must be checked rather than assumed — and his Brier scores
before and after Platt scaling (OpenAI 0.159 → 0.164) show that **calibration correction is not
guaranteed to help**.

**Capability and cost are separable decisions.** His comparison found the strongest system at F1 0.87
and 3.72 cents per 100 eval runs, against a cheaper qualifying candidate at F1 0.79 and 0.82 cents —
roughly **4.5x the cost for 0.08 F1**, on one dataset of 98 production traces. Whether that trade is
worth making is a deployment question, not a benchmark question.

## Notes

### What the work does not establish

Husain scopes his own findings tightly, and the vault should preserve that scoping:

- Everything rests on **one dataset** — 98 traces from a single apartment-leasing agent, 61 known
  failures and 37 without a labeled failure. Rankings on another task distribution are unknown.
- Latency means from separate runs are reported but **deliberately kept out of the main comparison**,
  because batching, concurrency, and infrastructure distance dominate them.
- A small manual experiment that moved default-threshold F1 from 0.78 to 0.80 by adding a failure-type
  checklist explicitly **did not use systematic prompt optimization** and does not establish its benefit.
- Models were given **masked traces** without labels or reviewer notes; the original conversations are
  private, so the experiment is not directly reproducible.

### Why this pairs with the rest of the vault

The threshold and calibration discipline here applies to any scored evaluator, not only decision
models — including [[LLM-as-a-Judge]] setups, which routinely report scores without checking whether
those scores mean what their scale implies. See [[Embedded Evaluation]] and
[[Interpretability Evaluation]].

### The book and the Three Gulfs

Husain co-authored *Evals for AI Engineers* (O'Reilly) with Shreya Shankar. An excerpt republished by
ByteByteGo is summarised in [[Shreya Shankar and Hamel Husain - Evals for AI Engineers]]. It sets out the **Three Gulfs** (comprehension,
specification, generalization), "adapted from Shankar et al. (2025) and inspired by Norman (1988)", and
an **Analyze-Measure-Improve** lifecycle. Read traces first, fix specification gaps in the prompt, and
build evaluators only for the generalization failures that remain. That is the upstream half of the
threshold-and-calibration work above, deciding *what* to score before asking whether the score means
anything.

ByteByteGo's introduction, not the excerpt, describes Husain as "an ML engineer at OpenAI with 20 years
of experience", previously at Airbnb and GitHub, who has helped "more than 35 companies", and says the
pair have trained "more than 4,500 engineers and product managers". These are publisher-supplied bio
claims, unverified here. The excerpt's copyright line reads "© 2027".

## Related pages

- [[Typed Probabilistic Decision Models]]
- [[Embedded Evaluation]]
- [[LLM-as-a-Judge]]
- [[Interpretability Evaluation]]
- [[Benchmark Optimization]]
- [[Agent Observability]]
- [[Hamel Husain - How To Use Decision Models for Evals]]
- [[Why Decision Models, and Why Now - A Taxonomy of Automated Decision-Making|Why Decision Models, and Why Now]]
- [[Shreya Shankar and Hamel Husain - Evals for AI Engineers]]
