---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-20-husain-decision-model-evals
source_title: How To Use Decision Models for Evals
source_author: Hamel Husain
source_url: https://hamel.dev/blog/posts/decision-model-evals/
tags:
  - source/summary
  - decision-models
  - evaluation
  - calibration
source_ids:
  - src-2026-10-20-husain-decision-model-evals
status: active
---

# Hamel Husain - How To Use Decision Models for Evals

## Summary

The first source in this vault that uses decision models as **automated evaluators** and then does the
unglamorous work the category usually skips: tuning the decision threshold on labeled data, checking
whether the returned probabilities are calibrated, and pricing the result.

Husain's headline practical finding is that **the default 0.50 threshold is an arbitrary inheritance**,
not an optimum. His headline comparative finding — OpenAI Decisions strongest but roughly **4.5x** the
cost of the cheapest qualifying candidate — is explicitly scoped to one dataset.

## Key claims

### Setup

- **100** traces from an apartment-leasing agent, containing conversations and actions. The task is
  spotting errors such as failed bookings or missed human handoffs.
- After excluding **2** internal QA examples, scoring used **98** production traces: **61** known
  failures and **37** without a labeled failure. The 61 comprise **39** from original human review plus
  **22** manually validated discoveries from Braintrust and Arize.
- Systems tested: Jev **1.13**, Perplexity Decider **1.1 27B**, Liquid **d1** and **d1-ultra**,
  Cloudflare Clef Flash, and OpenAI Decisions on GPT-6 Luna. Models received **masked traces** without
  labels or reviewer notes; the original conversations are private.

### Thresholds

- Each model returns a failure probability from 0 to 1; scores at or above **0.50** are flagged by default.
- A hypothetical model scoring failures **0.40** and passes **0.10** classifies perfectly at threshold
  **0.30** and catches nothing at **0.50**. This is the author's illustration, not a measurement.
- Tuning used stratified **five-fold** cross-validation, choosing thresholds on training folds and
  measuring on held-out folds.
- Candidate thresholds were constrained to meet at least **80% precision and 80% recall** on training
  data where feasible. That requirement is presented as **an example of a business rule**, not a standard.
- The constrained procedure fell back to unconstrained F1 in **36 of 100** training splits for Perplexity
  and **29 of 100** for Liquid d1-ultra, versus **0 of 100** for OpenAI. These are training-split
  feasibility counts, not held-out guarantees.

### Cost and performance

- Perplexity was the cheapest remaining candidate at **0.82 cents per 100 eval runs** with **F1 0.79**.
- OpenAI Decisions reached **F1 0.87** at **3.72 cents per 100 eval runs**, about **4.5 times** the cost.
- Costs cover **100** eval runs, one per trace. Liquid list prices were **$0.02 per million input tokens**
  (d1) and **$0.042 per million input tokens** (d1-ultra) as of October 17, 2026; the experiment recorded
  d1 at **$0.04** and repriced saved token usage.

### Calibration

- A returned number between 0 and 1 is not automatically a calibrated probability. One Clef Flash score
  group averaged a predicted failure probability of about **8%** while **60%** of those traces actually
  contained failures.
- Brier scores on saved out-of-fold probabilities, **before → after Platt scaling**: Jev
  **0.187 → 0.188**; Liquid d1-ultra **0.173 → 0.172**; OpenAI **0.159 → 0.164**. An exploratory
  direct-probability refit gave OpenAI **0.154**.
- **Platt scaling made OpenAI's reported Brier score worse** in the main fit. Calibration is not a
  guaranteed improvement.
- The reliability chart uses **5** groups of **19 or 20** traces from out-of-fold predictions.

### Cited, not run here

- Latency means from separate runs: Jev **4.33 s**, Perplexity **7.85 s**, Liquid d1 **7.38 s**,
  Liquid d1-ultra **1.56 s**, Clef Flash **2.09 s**, OpenAI **2.77 s**. Husain deliberately keeps these
  out of the main comparison because batching, concurrency, and infrastructure distance dominate.
- A small manual Jev experiment moved default-threshold F1 from **0.78** to **0.80** by adding a
  checklist of failure types. The footnote explicitly states this did **not** use GEPA and does not
  establish the benefit of systematic prompt optimization.
- Randy Olson's broader comparison is cited for the claim that decision models can match LLMs on
  classification and routing at lower cost while LLMs lead on knowledge- and reasoning-heavy tasks.

## Why it matters

[[Typed Probabilistic Decision Models]] has accumulated a long trail of vendor latency and cost
multipliers with incompatible scopes. This source does something different: it runs several of these
models **on the same private task with the same protocol** and reports the operational knobs that
actually decide whether one is usable.

It also supplies [[LLM-as-a-Judge]] and [[Multi-Turn Evaluation]] with a concrete separation the vault
has asserted but never demonstrated with numbers: **task discrimination, threshold choice, and
probability calibration are three different properties.** A model can rank traces well, be unusable at
the default cutoff, and still emit miscalibrated probabilities — Clef Flash's 8%-predicted/60%-actual
group is exactly that case.

## Tensions / open questions

- Results are from **one 98-trace dataset in one domain**. Husain repeatedly says performance varies
  substantially across tasks and that readers should measure on their own data.
- The original conversations are private, so the evaluation is **not independently reproducible**.
- Brier score mixes discrimination and calibration, so the before/after comparisons do not isolate
  calibration quality, and neither Platt scaling nor isotonic regression guarantees improvement on new
  examples.
- The deliberately broad "any failure" task may **exaggerate** model differences; Husain recommends
  separate judges per failure mode, which could shrink the gaps.
- OpenAI's higher F1 at higher cost hints that harder evaluation tasks justify an LLM, but one dataset
  does not establish that.
- Threshold tuning on training folds does not guarantee the same held-out behavior, and the 36/100 and
  29/100 fallback counts show the 80/80 requirement was often infeasible.
- Reported costs assume these providers, prices, token lengths, and no batching.

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Hamel Husain]]

## Raw capture

- [[How To Use Decision Models for Evals]]

## Citations

- Raw capture: [[How To Use Decision Models for Evals]]
- Canonical URL: <https://hamel.dev/blog/posts/decision-model-evals/>
- Published 2026-10-20; captured 2026-10-22.
- Cites Randy Olson's decision-model comparison and the GEPA prompt-optimization method; neither was
  read during this ingest.

## Related pages

- [[Agentic Testing]]
- [[Model Routing]]
- [[Inference Efficiency Frontier]]
- [[Sebastian Raschka - Language Models for Text Classification - From Bag-of-Words to Jev]]
- [[Swapnil Talekar - The Decision Model Gold Rush]]
- [[Liquid AI]]
- [[Perplexity]]
- [[OpenAI]]
