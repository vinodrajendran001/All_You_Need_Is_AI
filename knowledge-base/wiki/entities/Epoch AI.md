---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-10-07
tags: [entity, organization, ai-research]
source_ids:
  - src-2026-09-14-li-long-context-latency
  - src-2026-10-02-epoch-agent-population
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

## Related pages

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
