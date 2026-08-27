---
type: source-summary
created: 2026-07-06
updated: 2026-08-26
source_id: src-2026-07-06-sarthak-rastogi-production-agent
source_title: "Making an AI Agent Production-Ready [Tutorial With Code]"
source_author: Sarthak Rastogi
source_url: https://sarthakai.substack.com/p/making-an-ai-agent-production-ready
tags:
  - source/summary
  - ai-agents
  - production
  - rag
  - observability
source_ids:
  - src-2026-07-06-sarthak-rastogi-production-agent
status: active
---

# Sarthak Rastogi - Making an AI Agent Production-Ready

## Summary

This code-first tutorial walks through the full architecture of a production customer-support agent (an "Apple support bot") and, more usefully, the **failure modes** that a demo ignores but production cannot: prompt-injection/jailbreaks, cost blowups from re-answering identical questions, no observability when something breaks at 2am, and partial answers to multi-part questions. Each failure maps to a concrete layer in the design.

The reference stack is FastAPI + **LangGraph** (one graph invocation and one **LangSmith** trace per request), with PageIndex for retrieval, **Ragas** for hallucination detection, **Rival AI** for prompt-attack detection, and **GPTCache** for semantic caching. The durable, tool-agnostic lesson is an ordering principle — *things that **prevent** work go **before** the graph; things that **are** work go **inside** it* — and a layered pipeline of safety → intelligence → memory → retrieval → execution → validation, each observable and independently resilient.

## Key claims

- **Put the cheap guards outside the graph.** Middleware (rate limiting, structured logging) and the **semantic cache** check run before LangGraph is even invoked, because graph compilation, checkpointer setup, and state init aren't free — a cache hit should be a pure lookup-and-return. Rule of thumb: *prevent-work before the graph, do-work inside it.*
- **Semantic caching is a first-class cost lever.** Identical/near-identical questions ("how do I reset my AirPods") shouldn't spawn a fresh LLM call thousands of times a day; GPTCache returns a cached answer on semantic match. This is the production face of [[Model Routing]]'s spend-governance argument.
- **Safety is a dedicated node, split in two.** A PII-scrub step and a prompt-**attack-detect** step (backed by an isolated Rival AI microservice) gate every request before generation. Untrusted user input is treated as hostile by default.
- **Retrieval is a node (PageIndex), not the whole app.** RAG is one stage inside the graph, feeding validated context to generation — echoing [[Retrieval-Augmented Generation]] but embedded in a broader safety/validation pipeline.
- **Output validation runs faithfulness *and* completeness in parallel.** A faithfulness node (Ragas-style hallucination detection) checks the answer against retrieved context; a completeness node checks that multi-part questions are fully answered; both run simultaneously and merge — directly extending [[LLM-as-a-Judge]] from offline scoring into an inline production gate.
- **Observability is one trace per request.** LangSmith captures the whole graph execution so a 2am failure is debuggable — you can see which node failed, not just that the request failed.
- **Resilience is explicit:** retries with backoff and **circuit breakers** around external dependencies, plus resource isolation for the security microservice (a dedicated memory budget so the Rival model can't starve the main app on a shared host).
- **Evals gate change, not just launch.** A regression suite compares faithfulness + completeness against a baseline on every prompt/model change (LangSmith datasets), because a model upgrade that raises average quality can silently regress a specific query category; A/B model testing routes N% of traffic before cutover.

## Why it matters

This is the vault's most concrete end-to-end **production agent architecture**, and it materially deepens [[AI Agents in Production]] with a layered-defense blueprint (guards-before-graph, safety gate, parallel faithfulness+completeness validation, per-request tracing, retries/breakers). It connects several existing branches into one runnable system: [[Agentic Loop]] (LangGraph nodes as the concrete loop), [[Retrieval-Augmented Generation]] (PageIndex as one node), [[LLM-as-a-Judge]] (Ragas as an inline validator), [[Multi-Turn Evaluation]] (regression suites gating change), [[Context Engineering]] (query-intelligence + session memory), and [[Model Routing]] (semantic caching as cost control).

## Tensions / open questions

- It is opinionated and vendor-specific (LangGraph, LangSmith, PageIndex, Ragas, Rival AI/"Bhairava," GPTCache); the *patterns* are durable but the exact tools will churn.
- The published date (2026-04-10) predates capture (2026-07-06); some library specifics may already have shifted.
- Cross-session/long-term memory ("this user has a 15 Pro, complained about battery before") is flagged as a worthwhile next step, not implemented — a gap that connects to [[Agent Memory]].

## Affected pages

- [[AI Agents in Production]]
- [[Agentic Loop]]
- [[Context Engineering]]
- [[LLM-as-a-Judge]]
- [[Model Routing]]
- [[Multi-Turn Evaluation]]
- [[Retrieval-Augmented Generation]]

## Citations
- Source URL: [sarthakai.substack.com](https://sarthakai.substack.com/p/making-an-ai-agent-production-ready)

## Raw capture

- [[Making an AI Agent Production-Ready Tutorial With Code]]

## Related pages

- [[AI Agents in Production]]
- [[Agentic Loop]]
- [[Retrieval-Augmented Generation]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Context Engineering]]
- [[Model Routing]]
- [[Agent Memory]]
- [[AI Knowledge Base Overview]]
