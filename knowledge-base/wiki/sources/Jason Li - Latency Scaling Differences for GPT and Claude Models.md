---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-14-li-long-context-latency
source_title: "Latency Scaling Differences for GPT and Claude Models"
source_author: Jason Li
source_url: https://epoch.ai/publications/long-context-latency-scaling-gpt-vs-claude
tags: [source/summary, long-context, latency, inference]
source_ids: [src-2026-09-14-li-long-context-latency]
status: active
---

# Jason Li - Latency Scaling Differences for GPT and Claude Models

## Summary

Epoch AI measures time to first token from roughly 50K to 900K prompt tokens for GPT-5.6 Terra and
Sol and Claude Sonnet 5 and Opus 5 with reasoning disabled. Three estimators recover upward curvature
for the GPT models, while Sonnet is near-linear and noisy Opus remains consistent with little
curvature.

## Key claims

- The study uses 72 Terra, 30 Sol, 112 Sonnet, and 48 Opus requests.
- Quadratic fits are strongly favored for Terra (`p=8.87e-19`, delta AICc 75.50) and Sol
  (`p=1.48e-10`, delta AICc 37.29), but not for Sonnet or Opus.
- GPT pricing changes above 272K input tokens: input and cached input double, and output becomes 1.5x.
- Ten-million-token marginal-latency figures are explicit extrapolations, not observations.

## Why it matters

Observed API behavior suggests a smaller quadratic prefill component for Claude than GPT, but cannot
identify proprietary architecture. For agents, the result makes context retention a model-specific
systems decision rather than a universal rule.

## Tensions and caveats

TTFT includes upload, routing, queueing, cache lookup, prefill, generation, and return latency.
Serving configuration is unknown, Opus is noisy, shared-prefix affinity may affect routing, and
near-linear latency does not prove sparse or linear attention.

## Raw capture

- [[2026-09-14 Jason Li - Latency Scaling Differences for GPT and Claude Models]]

## Affected pages

- [[LLM Inference]]
- [[Context Engineering]]
- [[Serving Benchmarks and Goodput]]
- [[Epoch AI]]

## Related pages

- [[OpenAI]]
- [[Anthropic]]
- [[Linear Attention and Recurrent Memory]]

