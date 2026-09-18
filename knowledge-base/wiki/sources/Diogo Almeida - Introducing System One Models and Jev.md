---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-17-almeida-system-one-jev
source_title: "Introducing System One Models & Jev"
source_author: Diogo Almeida
source_url: https://typesafe.ai/blog/introducing-system-one-models-and-jev
tags: [source/summary, decision-models, structured-output, inference]
source_ids: [src-2026-09-17-almeida-system-one-jev]
status: active
---

# Diogo Almeida - Introducing System One Models and Jev

## Summary

TypeSafe AI introduces Jev, an early-access model for fast typed decisions embedded in software.
Instead of arbitrary text, it returns predefined values with probabilities and confidence scores in
parallel. TypeSafe calls the category "System One Models" and attributes it to a new architecture,
hardware-aware sampling, and Reinforcement Learning for Calibrated Decisions.

## Key claims

- Claimed pricing is **$0.042 per million input tokens** with unmetered output.
- Claimed end-to-end latency is **70-500 ms**, framed as 40x-200x faster on suitable tasks.
- Workflow headlines report **193.6x faster** and **444.6x cheaper**, which the source itself says
  likely represent the high end of real-world gains.
- Native output cardinality is at most 255; larger choice sets use a two-stage process.
- The "0% schema errors" claim follows from constrained output design and is not an empirical result.

## Why it matters

Typed probabilistic decision models trade open-ended generation for interface guarantees, parallel
sampling, and explicit uncertainty. That is useful for routing and workflow decisions, but schema
validity does not imply semantic correctness.

## Tensions and caveats

This is a vendor product launch. Architecture, parameter count, RLCD details, calibration curves, and
independent benchmarks are absent. Reference labels are averages from other models rather than ground
truth, and the vendor authored both workflows and evaluation setup.

## Raw capture

- [[2026-09-17 Diogo Almeida - Introducing System One Models and Jev]]

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[Inference Efficiency Frontier]]
- [[LLM-as-a-Judge]]
- [[TypeSafe AI]]

## Related pages

- [[Tool Use and Function Calling]]
- [[Model Routing]]

