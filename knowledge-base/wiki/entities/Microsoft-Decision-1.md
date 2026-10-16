---
type: entity
created: 2026-10-16
updated: 2026-10-16
entity_kind: model
tags: [entity, decision-models, calibration, routing]
source_ids:
  - src-2026-10-10-jaloza-microsoft-decision-1
status: active
---

# Microsoft-Decision-1

## What it is

Microsoft's model for single-pass probability scoring over fixed answer options, announced
as available through Microsoft Foundry and OpenRouter. The described release adapts
**Qwen3.5-9B**; future Microsoft AI and OpenAI backbones are a roadmap, not its current base.

## Why it matters here

[[Lisa Brown Jaloza - Microsoft-Decision-1]] adds a disclosed pretrained backbone to
[[Typed Probabilistic Decision Models]], alongside vendors with less disclosed architecture.
Uses include classification, routing, ratings, and rubric-based verification.

Microsoft reports leading accuracy on its **36-benchmark**, nearly **150,000-question**
suite, a **2.5x** speedup over H2O-Lightning-4B v1.1, and about **35x** over GPT-6 Sol
in the P50 latency comparison. These are first-party claims with incomplete common serving conditions,
not independently measured rankings or substitutes for task-level deployment evaluation.

## Notes

- The capture asserts calibration but supplies no numerical calibration table or curve.
  Option probabilities still need validation before setting act/defer/review thresholds.
- **1.3% average decision flips** across eight perturbation types and zero in selected
  categories do not establish universal paraphrase or option-order invariance.
- Listed pricing is **$0.042 per million input tokens**, with output tokens free. Request
  size, retries, routing, and other pipeline costs still determine cost per task.
- An editor's note adds Jev comparisons without captured numerical margins. This suite
  must remain separate from DecideBench, IMDb, and Microsoft's internal product anecdotes.
- A decision score does not grant authority, and an API-compatible backbone change would
  still require calibration and behavior to be re-evaluated.

## Related pages

- [[Lisa Brown Jaloza - Microsoft-Decision-1]]
- [[Typed Probabilistic Decision Models]]
- [[Model Routing]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
- [[Qwen]]
