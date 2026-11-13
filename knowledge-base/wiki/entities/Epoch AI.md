---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-11-13
tags: [entity, organization, ai-research]
source_ids:
  - src-2026-09-14-li-long-context-latency
  - src-2026-10-02-epoch-agent-population
  - src-2026-10-15-potter-how-to-train-your-robot
  - src-2026-11-09-zvi-ai-rd-acceleration-rsi
status: active
---

# Epoch AI

## What it is

Epoch AI is an AI research organization. In this vault it contributes external measurements of
frontier-model behavior when providers do not disclose their serving architecture, and explicitly
conditional models of compute supply and serving capacity.

## Why it matters here

[[Jason Li - Latency Scaling Differences for GPT and Claude Models]] measures long-context API
latency with three statistical estimators and reports different curvature for GPT-5.6 and Claude 5.
The work is useful because it separates observed behavior from architectural certainty: API latency
can suggest a quadratic component without revealing whether attention, routing, caching, or serving
policy caused it.

## Agent population as a supply scenario

[[Jason Li - How Many AI Agents Could We Run]] combines agent traces, API-price normalization,
reference serving deployments, and HBM shipment estimates. Its modeled population is concurrent
sessions under deployment, full-allocation, service-rate, and cost assumptions, not observed
agents, unique users, or productive human equivalents.

The closed-model economic model and the alternative DeepSeek V4 Pro throughput model use
different quality assumptions. Likewise, output streaming targets omit first-token delay, and
the annual API-equivalent spending scenario is not a provider margin or break-even estimate.
The contribution is an inspectable chain of assumptions; individual outputs should travel with
that chain rather than become an unconditional forecast.

## Text-data trends, cited secondhand

[[Brian Potter - How to Train Your Robot]] uses two Epoch findings as the baseline for robotics'
data gap: language-model training datasets have doubled in size about every six months since the
early 2010s, and Epoch's 2024 estimate puts the total stock of quality, accessible text at around
**300 trillion tokens**. The vault records these as Potter's citations; the underlying Epoch reports
have not been ingested. Both figures describe text. The robot side has no comparable stock estimate,
which is the contrast the essay builds on; see [[Robot Training Data]].

## Anthropic's version of the Capabilities Index

[[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]] reports that [[METR]]'s
assessment of AI R&D acceleration at [[Anthropic]] rests mainly on AECI, Anthropic's version of the
Epoch Capabilities Index computed on internal benchmarks. Charles Foster (METR) notes that each ECI
point multiplies a model's odds of success on every benchmark, and that historically each 5-point
increase corresponded to roughly a doubling in time horizon. Anthropic's AECI has grown 1.9x its
pre-October 2025 rate (95% CI 1.5-2.8x), or 1.4x with non-Anthropic models included. This is a
downstream use of Epoch's method, not Epoch's public index, and the capture has no Epoch statement.
It bears on [[Ramez Naam]]'s forecast, which names the public index (see
[[Recursive Self-Improvement]]).

## Related pages

- [[Brian Potter - How to Train Your Robot]]
- [[Robot Training Data]]
- [[Jason Li - How Many AI Agents Could We Run]]
- [[AI Accelerator Architecture]]
- [[Inference Efficiency Frontier]]
- [[AI Agents in Production]]
- [[ML Systems at Scale]]

- [[Jason Li - Latency Scaling Differences for GPT and Claude Models]]
- [[LLM Inference]]
- [[Serving Benchmarks and Goodput]]
- [[OpenAI]]
- [[Anthropic]]
- [[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]]
- [[METR]]
- [[Ramez Naam]]
