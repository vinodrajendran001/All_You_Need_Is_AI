---
type: entity
created: 2026-09-11
updated: 2026-09-11
entity_kind: person
tags:
  - entity
  - ai-agents
  - context-engineering
source_ids:
  - src-2026-09-01-iusztin-scoped-subagents
status: active
---

# Paul Iusztin

## What it is

Engineer and educator behind the Decoding AI newsletter, author of an open-source course that builds a
coding agent called **Decode** from scratch in Python. The course is structured as numbered lessons, each
pairing a design argument with the corresponding code in the Decode repository.

## Why it matters here

Iusztin supplies the vault's most concrete treatment of **subagents as a context-engineering mechanism**
rather than as a multi-agent architecture. His formulation — "subagents are context engineering" — reduces
delegation to a single economic test: a child that burns tens of thousands of tokens and returns a
1,000–2,000-token summary is worth spawning; one whose work would fit in the parent's window is not.

The second contribution is the distinction between spawning a subagent as an **in-harness tool** (a
context primitive) and spawning the CLI under `tmux` (a process primitive). Framing these as
non-competing answers to different questions — protect the parent's context, versus get a real security
boundary and live observability — turns a matter of taste into a design decision, and it is how
[[Agent Delegation]] now records the choice.

His Agents Catalog design also sharpens the vault's treatment of [[Agent Skill]]: a persona is a Markdown
file with YAML front matter carrying name, description, tools allowlist, default permission mode, and a
subagent flag, with the system prompt in the body. The tools allowlist and the permission mode are
explicitly different knobs — a tool absent from the system prompt can never be called, so the permission
mode has no effect on it.

## Notes

- Decode's fan-out guards are worth remembering as concrete numbers: 6 prompts per call, `Semaphore(4)`
  for concurrency, `UsageLimits(request_limit=25)` per child, and a shared 16,000-byte result budget
  divided by the number of prompts.
- Guard violations return `ModelRetry` — a correction to the model rather than an exception — which is a
  reusable pattern for tool-level policy.
- His own practice diverges from his artifact: beyond ten agents he reaches for Claude Code's dynamic
  workflows, and says he rarely uses `tmux`. The tmux case is argued more than used.
- He publishes no measurements — the material is budgets and limits, not before/after results.

## Related pages

- [[Agent Delegation]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Agent Skill]]
- [[Harness Optimization]]
- [[Agent Plugin Architecture]]
- [[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]]
