---
type: concept
created: 2026-09-18
updated: 2026-09-25
tags: [concept, decision-models, structured-output, inference]
source_ids:
  - src-2026-09-17-almeida-system-one-jev
  - src-2026-09-18-nandakishor-nonautoregressive-decisions
  - src-2026-09-18-0xmovez-jev-engineering
  - src-2026-09-22-canham-jev-explained
status: active
---

# Typed Probabilistic Decision Models

## Definition

Typed probabilistic decision models map unstructured or structured state directly to values from a
predeclared schema plus probabilities or confidence, rather than generating an arbitrary text string.

## Why it matters

Many software decisions are bounded: route to one queue, choose an action, rank candidates, or decide
whether a condition holds. Giving up free-form generation can make interface validity intrinsic,
enable parallel output, and expose uncertainty directly. It does not make the selected value true.

## Current synthesis

[[Diogo Almeida - Introducing System One Models and Jev]] is the first source in this vault for the
pattern. TypeSafe AI calls its implementation a "System One Model," but that is a vendor category;
this page uses a functional name.

Jev reportedly samples typed decisions in parallel and supports up to 255 native choices. Larger
sets use independent scoring followed by an explicit-choice stage. The vendor claims 70-500 ms
end-to-end latency and very low input pricing, but provides no public architecture, calibration
curves, or independent benchmark.

Two validity layers must stay separate:

1. **Schema validity:** the output is one of the allowed types or values.
2. **Semantic validity:** the selected value is correct, calibrated, and useful.

Constrained construction can guarantee the first. It cannot guarantee the second, so "cannot
hallucinate" is too broad.

## A pattern, not one product category

[[Nandakishor M - Non-Autoregressive Decision Models and Laya]] supplies an open competing
implementation: a 421M bidirectional model with typed questions, calibration-oriented RL, and an
explicit escalation action. Its benchmark and priority claims remain self-reported.

[[0xMovez - Jev Engineering]] contributes the deployment pattern—dynamic option menus, parallel
questions, confidence gates, and bounded middleware—while [[Matthew Canham - Jev Explained]] reduces
the interface to state, question, options, and probabilities. Their speed and cost ranges are
secondary claims with incompatible scopes, not independent replications of the vendor benchmark.

## Open questions

- How is confidence calibrated under distribution shift?
- When does parallel decision sampling outperform a small autoregressive model plus constrained decoding?
- How should large or changing action spaces be represented without a two-stage error cascade?
- What independent ground truth should replace teacher-model averages in evaluation?

## Related pages

- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[TypeSafe AI]]
- [[Tool Use and Function Calling]]
- [[LLM-as-a-Judge]]
- [[Inference Efficiency Frontier]]
