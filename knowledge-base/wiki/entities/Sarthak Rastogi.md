---
type: entity
created: 2026-09-11
updated: 2026-09-30
entity_kind: person
tags:
  - entity
  - ai-agents
  - production
  - observability
source_ids:
  - src-2026-07-06-sarthak-rastogi-production-agent
  - src-2026-09-06-rastogi-agent-observability
  - src-2026-09-25-rastogi-6-ways-jev-agents-reliable
status: active
---

# Sarthak Rastogi

## What it is

Engineer writing on production AI systems at sarthakai.substack.com, with a practitioner focus on what
has to be true before an agent is allowed real traffic.

## Why it matters here

Rastogi supplies the vault's foundational material for [[Agent Observability]], and the framing is what
makes it durable: observability is the ability to reconstruct a **causal chain** for a single run, and it
is neither evaluation nor logging. His production gate — if nobody can answer *what did the agent do, why,
and what did it cost* for any run from the last 30 days, it does not touch production traffic — is the
clearest statement of the standard in this vault.

Two of his findings invert common intuitions and are worth carrying independently of the source. A
**near-zero fallback-response rate is a defect signal**, not a health signal, because it means the agent
has never met an ambiguous situation it did not answer confidently. And guardrails need **sabotage
validation** — feeding known-bad input on a schedule — because one team running it found 67 checks
silently no-op'ing for months.

He also makes the case that random sampling is structurally wrong for LLM traffic, since two
near-identical inputs can produce a correct answer, a hallucination and a refusal; the replacement is
tail-based, outcome-aware sampling with routine successes at 5–20%.

His Jev material sits at a different evidence grade from the rest, and the distinction should travel with
any citation of it. [[Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]] is a
**secondary explainer restating [[TypeSafe AI]]'s vendor figures** — about **100 milliseconds**, **$0.042
per million input tokens** with output tokens free, **40x to 200x faster** and **up to 400x cheaper** —
not independent measurement. It carries **no benchmark and no controlled comparison**, and the guardrail
results it cites are TypeSafe's own cookbook, run on **`jev-1.12`** and described only as having worked
"pretty well". What is his is the operational discipline around the product: shadow mode first, **100 to
200 labelled cases**, thresholds set after labelling rather than before, and the conclusion he draws from
TypeSafe's **`jev-1.13`** jaggedness notes that a typed screen is a filter and not a security boundary.
Read the figures as attributed vendor claims and the sequencing as practitioner advice.

## Notes

- Cites a Sherlocks AI analysis of 73 production agent incidents (January–May 2026): 4.2 hours average
  resolution without decision-trace logging, under an hour with full tracing.
- Documents the OpenTelemetry GenAI semantic conventions' six span types, and the deliberate decision to
  keep prompt/response content in span **events** rather than indexed attributes so it can be redacted at
  the collector.
- His retry arithmetic — 20,000 runs/day × 6 tool calls × 0.5% failure × 3 retries ≈ 1,800 retried calls
  daily — is the bridge between observability and [[LLM Application Resilience]].
- Writes evenhandedly about vendors, naming Salesforce Agentforce Observability as a fair
  counter-example to platforms that ship adoption metrics early and reasoning traces late.

## Related pages

- [[Agent Observability]]
- [[AI Agents in Production]]
- [[Agent Security and Governance]]
- [[LLM Application Resilience]]
- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[Sarthak Rastogi - Making AI Agents Observable, Monitorable, and Production-Ready]]
- [[Sarthak Rastogi - Making an AI Agent Production-Ready]]
- [[Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]]
- [[Typed Probabilistic Decision Models]]
- [[TypeSafe AI]]
