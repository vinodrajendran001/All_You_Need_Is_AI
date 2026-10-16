---
type: source-summary
created: 2026-10-16
updated: 2026-10-16
source_id: src-2026-10-10-jaloza-microsoft-decision-1
source_title: "Microsoft-Decision-1: Our model for fast decision-making"
source_author: Lisa Brown Jaloza
source_url: https://commandline.microsoft.com/microsoft-decision-1-model-foundry/
tags: [source/summary, decision-models, calibration, evaluation, routing]
source_ids: [src-2026-10-10-jaloza-microsoft-decision-1]
status: active
---

# Lisa Brown Jaloza - Microsoft-Decision-1

## Summary

Microsoft's announcement of **Microsoft-Decision-1**, a Qwen3.5-9B-derived model post-trained
for single-pass scoring over fixed answer options. It returns option probabilities through a
structured API for classification, routing, rating, verification, and workflow control.
The product is presented as available through Microsoft Foundry and OpenRouter.

This is first-party product and evaluation reporting. It adds a disclosed backbone and a
different evaluation suite to the decision-model branch, not an independent resolution of
the vault's competing vendor benchmarks.

## Key claims

- The described base is **Qwen3.5-9B**. Rebasing on Microsoft AI and OpenAI models is planned,
  not the architecture of the announced version. The detailed scoring-head and training
  recipe are not disclosed in the capture.
- Supported tasks include yes/no, multiple-choice, ratings, and rubric-based assessment of
  generated answers or proposed actions. Fixed options narrow the output contract without
  guaranteeing a correct decision or production calibration.
- Microsoft reports the highest accuracy in its **36-benchmark** comparison covering nearly
  **150,000 questions**, with benchmarks kept blind from training. The suite includes public
  and private tasks. This is the developer's contamination/generalization claim, not a
  separately audited guarantee.
- Reported latency is **2.5x faster than H2O-Lightning-4B v1.1** and about **35x faster than
  GPT-6 Sol**, with the latter explicitly described as P50 latency. The capture does not
  provide a complete common serving/hardware/request boundary or an absolute universal latency.
- Across **eight perturbation types**, the decision flips **1.3% on average**, with zero flips
  in the stated option-description paraphrase and reversal/shuffle categories. These observations
  do not prove invariance for arbitrary paraphrases, inputs, or option sets.
- The API's probability is intended to support act/defer/review decisions. The article asserts
  calibration, but this capture contains no numerical calibration table or curve from which
  to validate a deployment threshold.
- Safety testing covers **5,250 requests across 11 benchmarks**. The prose claims harmful
  refusal with useful behavior retained, without a complete confusion matrix or scoped error
  rates in the capture.
- Listed pricing is **$0.042 per million input tokens**, with output tokens free. This is not
  a per-task price, nor a measurement of total system cost.

### Internal examples remain separate workloads

Xbox Research reports classifying more than **10,000 feedback items**, with quality competitive
with GPT-6 Sol, over **14x** faster and **200x** less expensive. Copilot quality-control testing
reports competitive quality with GPT5.6 Luna and **100x** speed. Microsoft Discovery reports
**46x** score consistency, **3x** scoring speed, and nearly **4x** adaptive-replanning speed.
Definitions, protocols, and uncertainty are incomplete; these are not interchangeable
measurements or evidence for one universal multiplier.

## Why it matters

[[Typed Probabilistic Decision Models]] now contains both opaque vendor architectures and a
declared pretrained backbone adapted for scoring. [[LLM-as-a-Judge]] and [[Model Routing]]
must still distinguish option probability, empirical calibration, task accuracy, and the
operational threshold that permits action.

## Tensions / open questions

- An editor's note says Jev accuracy and calibration comparisons were added. Their exact
  numerical results are not present in this clipping, so this note does not invent a Jev
  margin or merge this suite with DecideBench or IMDb.
- Developer-held-out benchmarks, robustness perturbations, calibration, and safety are different
  axes. A good aggregate on one cannot fill missing evidence on another.
- A classifier's refusal score is not an authorization boundary. Structured grading also
  does not replace deterministic checks for mechanically verifiable conditions.
- Roadmap backbone changes would require re-evaluation of semantics, calibration, and thresholds,
  even if an API remains compatible.

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[Model Routing]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
- [[Microsoft-Decision-1]]
- [[Qwen]]

## Raw capture

- [[Microsoft-Decision-1 Our model for fast decision-making]]

## Citations

- Canonical article: <https://commandline.microsoft.com/microsoft-decision-1-model-foundry/>
- Published October 10; captured October 13, 2026.
- Linked documentation, not separately tested:
  <https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision>.

## Related pages

- [[Microsoft-Decision-1]]
- [[Typed Probabilistic Decision Models]]
- [[Model Routing]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
- [[Qwen]]
