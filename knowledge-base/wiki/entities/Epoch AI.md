---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-09-18
tags: [entity, organization, ai-research]
source_ids:
  - src-2026-09-14-li-long-context-latency
status: active
---

# Epoch AI

## What it is

Epoch AI is an AI research organization. In this vault it contributes external measurements of
frontier-model behavior when providers do not disclose their serving architecture.

## Why it matters here

[[Jason Li - Latency Scaling Differences for GPT and Claude Models]] measures long-context API
latency with three statistical estimators and reports different curvature for GPT-5.6 and Claude 5.
The work is useful because it separates observed behavior from architectural certainty: API latency
can suggest a quadratic component without revealing whether attention, routing, caching, or serving
policy caused it.

## Related pages

- [[Jason Li - Latency Scaling Differences for GPT and Claude Models]]
- [[LLM Inference]]
- [[Serving Benchmarks and Goodput]]
- [[OpenAI]]
- [[Anthropic]]

