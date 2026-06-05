---
type: source-summary
created: 2026-06-05
updated: 2026-06-05
source_id: src-2026-06-05-pguso-agents-from-scratch
source_title: AI Agents from Scratch
source_author: pguso (GitHub)
source_url: https://github.com/pguso/agents-from-scratch
tags:
  - source-summary
  - agents
  - tutorial
  - python
  - local-llm
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
status: active
---

# pguso - Agents From Scratch

## Summary

A MIT-licensed Python repository that teaches AI agents from first principles using only local GGUF models (no frameworks, no cloud APIs). The repo builds a single evolving `agent.py` file across 12 progressive lessons, from raw LLM calls to a fully observable, testable agent with structured outputs, tools, memory, planning, atomic actions, dependency graphs, evals, and telemetry.

The defining philosophy is **mechanical understanding**: every decision is explicit, every state transition is visible, and nothing happens behind the scenes. The repo actively avoids anthropomorphic language (agents don't "think") and framework abstractions (LangChain etc. are tools to evaluate *after* you understand what they abstract).

## Key claims

- An agent is `while not done: observe → decide → act` — a loop with state, not a personality.
- **Structure beats cleverness**: a mediocre prompt with good structure (JSON schema + retries) beats a clever prompt with free-form output.
- **Constraints enable reliability**: the more constrained the action space, the more predictably the system behaves.
- The model **requests** tools; the application layer **executes** them — this boundary is where safety and control live.
- **Plans are data structures**, not thoughts. Planning is structured data generation that produces inspectable, modifiable Python dicts.
- **Atomic actions** (smallest typed operations) make execution safe by catching errors before anything runs.
- **AoT (Atom of Thought)** = planning + atomic actions + explicit dependency edges → a validated execution graph that naturally enables parallel execution.
- **Evals = golden datasets + assertions.** Run before every prompt change. If a golden case fails, the agent is broken.
- **Telemetry = structured logging + traces + metrics.** Spans are individual operations; traces link a full interaction. Enables post-hoc debugging.
- ReAct is bypassed: tool calling + good prompts accomplishes the same goals more explicitly and debuggably.

## Lesson map

| Phase | Lessons | What is built |
|-------|---------|--------------|
| Foundation | 1–3 | Raw LLM call → system prompts → structured output + retries |
| Agency | 4–6 | Decision routing → tool request/execute → agent loop with state |
| Intelligence | 7–10 | Persistent memory → plans as data → atomic actions → AoT dependency graphs |
| Observability | 11–12 | Golden-dataset evals → JSONL telemetry with trace IDs |

## Why it matters

This source is the most detailed ground-up treatment of the **Agentic Loop** in this vault. It makes explicit what most other sources assume: how state transitions work, why structured JSON output is the reliability lever rather than prompt cleverness, how memory is just explicit storage loaded into context, and how planning and execution should be separate phases. It also adds the first treatment of **agent-specific regression testing and runtime observability**, which complements the evaluation branch from the ByteByteGo and Braintrust sources.

## Tensions / open questions

- The repo uses llama-cpp-python for local inference. The principles are portable, but the specific `generate_structured` retry loop may need adjustment for cloud models with native function-calling APIs.
- The simple "get all" memory retrieval works for small knowledge bases but does not scale — the repo acknowledges this without solving it.
- The evals use hard assertions and exact string matching; semantic/LLM-as-judge evaluation is explicitly deferred as "too complex for now."

## Affected pages

- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]
- [[Agent Planning]]
- [[Agent Memory]]
- [[Multi-Turn Evaluation]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture note: `knowledge-base/raw/sources/2026-06-05 pguso - Agents From Scratch.md`
- Source URL: [https://github.com/pguso/agents-from-scratch](https://github.com/pguso/agents-from-scratch)

## Related pages

- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]
- [[Agent Planning]]
- [[Agent Memory]]
- [[Multi-Turn Evaluation]]
- [[Direct Corpus Interaction]]
- [[Model Context Protocol]]
- [[AI Knowledge Base Overview]]
