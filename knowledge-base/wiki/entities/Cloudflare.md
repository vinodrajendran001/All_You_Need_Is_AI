---
type: entity
entity_kind: organization
created: 2026-10-27
updated: 2026-10-27
tags: [entity, organization, inference, prompt-caching, model-routing, code-review]
source_ids:
  - src-2026-10-20-cloudflare-inference-bill
  - src-2026-07-03-bytebytego-openai-voice
  - src-2026-10-20-husain-decision-model-evals
  - src-2026-08-20-jeremy-morrell-extensible-software
  - src-2026-10-08-talekar-decision-model-gold-rush
  - src-2026-09-28-bytebytego-agents-can-pay
status: active
---

# Cloudflare

## What it is

Cloudflare is the company whose engineering blog published the vault's captured source, a post on
cutting the cost of its internal AI code reviewer. There it appears as an operator of production agents:
a coordinator hands each merge request to specialist reviewer agents, and risk tiers decide how
intensive the review is. The reviewer runs on OpenCode v2, and the team reports experimenting with
running it on Durable Objects. The internal standards reviewer that Cloudflare calls Codex is its own
agent, not OpenAI's product.

## Why it matters here

[[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]] is a detailed
first-party account of an agent fleet's cost per run being taken apart and rebuilt. It contributes:

- a prompt-cache failure hidden by a healthy aggregate hit rate, fixed by changing the byte layout of
  each session's first request, to [[Semantic Caching]];
- randomized model and effort splits showing that cost per run, not price per token, is the number to
  compare, to [[Model Routing]] and [[Reasoning Effort Control]];
- two quality checks on a cheaper agent, author follow-through and blinded model judges, weighed on
  [[Reasoning Effort Control]].

The source summary also records small harness fixes, such as removing a tool the reviewers could not
use. [[Tool Roster Economics]], [[Context Engineering]], and [[LLM-as-a-Judge]] are related topics but do
not yet cite this source.

Cloudflare also appears in secondary roles elsewhere in the vault: its Clef decision models in
[[Swapnil Talekar - The Decision Model Gold Rush]] and
[[Hamel Husain - How To Use Decision Models for Evals]], Dynamic Workers as one possible deployment
substrate in [[Jeremy Morrell - Extensible Software in the Age of LLMs]], signaling steering in
[[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]], a cited report that automated systems generate
around 57.5% of HTTP requests to web content in [[ByteByteGo - AI Agents Can Think, Now They Can Pay]],
and a system-design case listed as 55 million requests per second on 15 Postgres clusters in
[[ML Systems at Scale]].

## Boundaries

The headline 68% is the average cost of one review against the two most expensive weeks, not the
company's whole inference bill, and the post uses several slightly different baselines. Cost attribution
compares hours before and after each change and is not a controlled experiment; only the model and
effort comparisons were randomized. The quality checks are imperfect proxies on small samples, the
evidence is self-reported telemetry from one workload, and the author is not named in the capture.

## Related pages

- [[Cloudflare - Cutting Our Inference Bill by 68% by Being Obsessive About Optimization]]
- [[Semantic Caching]]
- [[Model Routing]]
- [[Reasoning Effort Control]]
- [[Tool Roster Economics]]
- [[LLM-as-a-Judge]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Anthropic]]
- [[Inference Efficiency Frontier]]
