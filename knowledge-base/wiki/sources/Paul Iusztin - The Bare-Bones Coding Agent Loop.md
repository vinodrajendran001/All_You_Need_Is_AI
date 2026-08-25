---
type: source-summary
created: 2026-08-07
updated: 2026-08-07
source_id: src-2026-08-07-paul-iusztin-bare-bones-coding-agent-loop
source_title: The Bare-Bones Coding Agent Loop
source_author: Paul Iusztin
source_url: https://www.decodingai.com/p/the-coding-agent-loop
tags:
  - source/summary
  - ai-agents
  - coding-agents
  - harness
source_ids:
  - src-2026-08-07-paul-iusztin-bare-bones-coding-agent-loop
status: active
---

# Paul Iusztin - The Bare-Bones Coding Agent Loop

## Summary

Paul Iusztin builds a small coding-agent harness named Decode with Pydantic AI, a terminal UI, nine tools, three interchangeable model providers, OpenTelemetry tracing, safe steering queues, and append-only JSONL session logs. The article treats the core ReAct cycle as simple and puts the engineering emphasis on the harness boundaries that keep the loop observable and steerable.

The execution cycle is plan → explore → apply → execute → observe. Read-only and mutating tools are separated through approval gates; new user messages are buffered and injected only at model-request or would-stop boundaries so they do not corrupt an active tool call.

## Key claims

- Harness architecture can materially change coding-agent performance while holding the model fixed.
- A minimal system prompt and small tool catalog reduce context cost and tool-selection confusion.
- Provider-specific logic belongs behind one model factory so the loop is not coupled to Gemini, OpenRouter, Modal, or another backend.
- Exact-match editing should normalize invisible formatting, reject ambiguous replacements, and write atomically.
- Steering, follow-up, and cooperative abort need different queues and safe injection boundaries.
- Append-only JSONL can provide inspectable session persistence without introducing a database.
- Tracing should be present from the start because terminal output omits spans, token counts, tool arguments, and configuration needed for debugging.

## Why it matters

The source gives [[Coding Agent Harness]] a concrete reference architecture and deepens [[Agentic Loop]] with pause/resume and user-steering semantics. It also connects minimal tools, session logs, approvals, context limits, and tracing as one coherent runtime rather than independent features.

## Tensions / open questions

- The Pi-inspired choice to omit a hard step limit conflicts with the production safety case for explicit budgets and termination caps.
- An append-only local log is transparent but does not by itself provide concurrency, remote durability, access control, or replay guarantees.
- Bash remains a broad capability even when file tools are jailed to a working directory; strong containment requires a sandbox.
- The Terminal-Bench harness claim is presented as motivation but needs the original experiment for exact controls and comparability.

## Affected pages

- [[Coding Agent Harness]]
- [[Agentic Loop]]
- [[Context Engineering]]
- [[Agent Security and Governance]]
- [[AI Agents in Production]]

## Citations

- Raw capture: [[2026-08-07 Paul Iusztin - The Bare-Bones Coding Agent Loop]]
- Canonical URL: https://www.decodingai.com/p/the-coding-agent-loop

## Related pages

- [[Agent Planning]]
- [[Agent Memory]]
- [[Multi-Turn Evaluation]]
- [[Loop Engineering]]

