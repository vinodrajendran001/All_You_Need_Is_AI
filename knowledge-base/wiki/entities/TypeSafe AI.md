---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-09-25
tags: [entity, organization, decision-models]
source_ids:
  - src-2026-09-17-almeida-system-one-jev
  - src-2026-09-18-nandakishor-nonautoregressive-decisions
  - src-2026-09-18-0xmovez-jev-engineering
  - src-2026-09-22-canham-jev-explained
status: active
---

# TypeSafe AI

## What it is

TypeSafe AI is an AI lab building models that return typed probabilistic decisions for software
automation. Its first public product is Jev.

## Why it matters here

[[Diogo Almeida - Introducing System One Models and Jev]] introduces a model interface that gives up
open-ended string generation for predefined values, probabilities, and confidence. The design is a
useful counterpoint to constrained decoding around general-purpose LLMs.

All available evidence is vendor-authored and early-access. Claims about latency, price, calibration,
and "no hallucinations" require independent evaluation; schema validity should not be confused with
semantic correctness.

## External explanations and dispute

[[0xMovez - Jev Engineering]] and [[Matthew Canham - Jev Explained]] broaden the use cases but repeat
incompatible performance ranges without controlled baselines. [[Nandakishor M - Non-Autoregressive Decision Models and Laya]]
claims prior work and reports an open alternative; it does not establish copying or an independently
controlled comparison with Jev.

## Related pages

- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[Typed Probabilistic Decision Models]]
- [[Inference Efficiency Frontier]]
- [[LLM-as-a-Judge]]
