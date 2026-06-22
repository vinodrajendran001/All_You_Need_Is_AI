---
type: source-summary
created: 2026-06-22
updated: 2026-06-22
source_id: src-2026-06-22-djfarrelly-agent-loop-architecture
source_title: The Agent Loop Architecture
source_author: djfarrelly
source_url: https://x.com/djfarrelly/status/2067677007140278630
tags:
  - source-summary
  - agents
  - orchestration
  - durable-execution
  - skills
source_ids:
  - src-2026-06-22-djfarrelly-agent-loop-architecture
status: active
---

# djfarrelly - The Agent Loop Architecture

## Summary

This source argues that the next bottleneck in agent systems is not the model or the prompt, but **what runs the loop**. Simple `/loop`, `/goal`, or `while true` agent patterns work for single-session work, but they break when loops need to survive restarts, run on schedules, supervise sub-agents, avoid duplicate side effects, and remain observable after the fact.

The proposed architecture has three layers:

1. **Loop** — a cron or trigger plus an LLM decision-maker that periodically evaluates state and decides what should happen.
2. **Skill** — a durable workflow: multi-step, retryable, composable, independently deployable, and callable by loops or agents.
3. **Orchestrator** — the execution engine that schedules triggers, checkpoints steps, handles retries/failures, enforces concurrency, stores run history, and hot-deploys new workflows without disrupting in-flight runs.

The source uses Inngest as the concrete platform example, but its architectural claim is broader: production agents are not just `LLM + tools`; they are **loops + skills + orchestration**, with the LLM and tools sitting inside a durable execution layer.

## Key claims

- "The loop" is not the LLM itself. It is the surrounding execution structure that triggers work, asks the LLM for a decision, runs durable steps, and resumes safely after interruptions.
- Basic long-running processes fail because they lose step state on deploys, crashes, OOMs, or VM restarts. Recovery without checkpoints causes duplicate LLM calls, duplicate notifications, duplicate sub-agent launches, and wasted token spend.
- Durable execution requires step-level checkpoints, independent step retries, failure hooks, guaranteed event delivery, parent-child sub-agent lifecycle management, concurrency controls, hot deploys, and post-hoc observability.
- A skill is "not a prompt" in this framing; it is a durable workflow that can combine deterministic code and LLM decisions.
- Agents can become orchestration-aware: they can write new durable functions, register them with the orchestration engine, test them, observe run history, and later revise them through scheduled review loops.
- Developer ownership remains necessary. Agent-authored skills are durable infrastructure that humans must inspect, debug, edit, delete, or ask the agent to repair.
- The compounding value is a skill library: workflows, decision patterns, and run-history feedback persist even if the underlying generalist model is swapped.

## Why it matters

This source deepens the vault's agent branch by moving one layer below [[Agentic Loop]]. Prior notes describe the loop mechanics, tool boundaries, memory, planning, and telemetry. This source asks what production runtime makes those loops reliable after crashes, deploys, retries, schedules, and long-running sub-agent calls.

The durable takeaway is that agent reliability depends on an **execution substrate**. If the loop cannot checkpoint decisions, resume partially completed work, and expose run history, then the agent may appear autonomous while actually being operationally fragile.

## Tensions / open questions

- How much of the proposed pattern is generic durable-execution architecture versus specific to Inngest's product model?
- When an agent writes new skills, what governance prevents unsafe code, duplicate functionality, or unbounded self-modification?
- How should systems version, evaluate, and roll back agent-authored skills when live performance degrades?
- At what point does the overhead of durable orchestration outweigh the benefit for small one-off local agents?

## Affected pages

- [[Agentic Loop]]
- [[Agent Skill]]
- [[Agent Planning]]
- [[AI Agents in Production]]
- [[Inngest]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/The Agent Loop Architecture.md`
- Source URL: [https://x.com/djfarrelly/status/2067677007140278630](https://x.com/djfarrelly/status/2067677007140278630)

## Related pages

- [[Agentic Loop]]
- [[Agent Skill]]
- [[Agent Planning]]
- [[AI Agents in Production]]
- [[Context Engineering]]
- [[Inngest]]
- [[pguso - Agents From Scratch]]
- [[AI Knowledge Base Overview]]
