---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-nevsky-gemini-multi-agent-system
source_title: "Building a Multi-Agent AI System with Gemini 3 and Google Cloud: From Single Agent to Orchestrated Intelligence"
source_author: Alex Nevsky
source_url: https://medium.com/google-cloud/build-multi-agent-ai-system-with-gemini-3-1-google-cloud-single-bot-orchestrated-intelligence-dc0c111e30e7
tags:
  - source/summary
  - ai-agents
  - multi-agent
  - google-cloud
source_ids:
  - src-2026-09-13-nevsky-gemini-multi-agent-system
status: active
---

# Alex Nevsky - Building a Multi-Agent AI System with Gemini 3 and Google Cloud

## Summary

A detailed customer-support tutorial decomposing one prompt into triage, research, action, QA, and orchestration agents. Its strongest material is not the Gemini product choice but the contracts: typed handoffs, one designated writer, bounded QA repair, human confirmation, and explicit state retention.

## Key claims

- The prior monolithic prompt had exceeded **3,000 tokens** and reportedly suffered constraint bleed, attention dilution, brittle routing, and difficult debugging.
- The architecture uses **5 agents**: Pro for orchestration and QA, Flash-Lite for triage, and Flash for research and action.
- ADK AutoFlow injects `transfer_to_agent()` for orchestrators with sub-agents; Pydantic input/output schemas define handoff contracts.
- Only the action agent writes to business APIs. Refunds require confirmation and amounts **over $500** escalate.
- QA checks the exact amount, policy support, tone, complete intent coverage, and unauthorized promises. Failed work can loop back at most **2 times** before human escalation.
- The source recommends summaries rather than raw tool responses in memory, a **24–48 hour TTL**, and masking PII before shared-state storage.
- Its rule of thumb is to decompose near **3,000 prompt tokens** or when components need materially different tools; simple FAQs and **3–5 tool lookups** may remain single-agent.
- Reported expectations are **3–8 seconds** for five agents versus **1–2 seconds** for one. Sequential specialization adds **4–6 seconds**; parallel independent work may reduce latency **30–40%**.
- The source estimates **4–5x** the API calls and about **$530/month** for **100,000 complex queries**, roughly **$0.005 per interaction**, with about **30%** of calls using Pro. These are estimates, not measured benchmark results.

## Why it matters

This is a concrete multi-agent design where delegation is coupled to authority. The architecture does not merely assign roles: it centralizes mutation in one agent, validates transfers with schemas, and makes QA a bounded control loop. Those are portable patterns even if the prices and model names expire.

## Tensions / open questions

- Cost and latency figures are estimates without a disclosed workload or controlled comparison.
- Prompt-level rules do not replace API-side authorization.
- The tutorial's unauthenticated Cloud Run example needs another authentication layer for sensitive support work.
- More specialists add schema, state, routing, and partial-failure complexity.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Agent Delegation]]
- [[Agent Frameworks]]
- [[AI Agents in Production]]
- [[Agent Security and Governance]]

## Citations

- Alex Nevsky, "Building a Multi-Agent AI System with Gemini 3 and Google Cloud", 2026-03-18.

## Raw capture

- [[2026-09-13 Alex Nevsky - Building a Multi-Agent AI System with Gemini 3 and Google Cloud]]

## Related pages

- [[Agent Memory]]
- [[Agent Observability]]
- [[Model Routing]]

