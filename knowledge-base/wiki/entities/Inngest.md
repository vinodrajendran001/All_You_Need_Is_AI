---
type: entity
created: 2026-06-22
updated: 2026-06-22
entity_kind: orchestration platform
tags:
  - entity
  - agents
  - orchestration
  - durable-execution
source_ids:
  - src-2026-06-22-djfarrelly-agent-loop-architecture
status: active
---

# Inngest

## What it is

Inngest is a durable workflow and orchestration platform. In [[djfarrelly - The Agent Loop Architecture]], it is presented as an execution engine for agent loop architecture: cron triggers, event-driven functions, `step.run`, `step.invoke`, retries, failure hooks, concurrency controls, run history, and step-level observability.

## Why it matters here

Inngest matters to this vault because it is a concrete implementation of the broader [[Agentic Loop]] infrastructure problem. The source's claim is not merely that agents need better prompts; they need an execution layer that can checkpoint decisions, resume after crashes, avoid duplicate side effects, and expose run traces that humans and agents can inspect.

## Notes

- The source frames agents as **loops + skills + orchestration**, with the LLM and tools inside that execution layer.
- Inngest's `utah` project is cited as an agent harness where an agent can write and edit Inngest functions in its own workspace, extending itself with durable [[Agent Skill|skills]].
- The architectural lesson is broader than Inngest as a product: production agent loops need durable workflow primitives similar to those in job queues and workflow engines.

## Related pages

- [[djfarrelly - The Agent Loop Architecture]]
- [[Agentic Loop]]
- [[Agent Skill]]
- [[Agent Planning]]
- [[AI Agents in Production]]
- [[Context Engineering]]
