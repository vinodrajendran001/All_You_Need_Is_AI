---
type: concept
created: 2026-06-05
updated: 2026-06-05
tags:
  - concept
  - agents
  - planning
  - execution
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
status: active
---

# Agent Planning

## Definition

Agent planning is the process of decomposing a goal into a sequence (or graph) of executable steps before acting. The key insight across every treatment in this vault is that plans are **data structures**, not internal thoughts: a Python dict or JSON object that can be inspected, validated, modified, and reused independently of execution.

## Why it matters

Without a plan, an agent either acts blindly on a single decision or relies on opaque chain-of-thought that is hard to debug. Explicit planning gives a human (and the surrounding system) a window into what the agent is going to do before it does it.

## Current synthesis

### Planning as structured data generation

[[pguso - Agents From Scratch]] makes this distinction sharper than any other source: planning is not sophisticated reasoning — it is the model generating structured JSON:

```python
plan = {"steps": ["Research topic", "Create outline", "Write draft", "Review"]}
```

Because planning is just another call to `generate_structured`, all the same reliability techniques apply: schema constraints, retries, validation before execution.

Separating the planning call from the execution loop means you can:
- Inspect or log the plan before anything runs
- Reject invalid plans early
- Re-use a cached plan across multiple executions
- Modify a plan in response to partial failure without restarting from the goal

### Atomic actions

Vague plan steps like `"Write article"` are unsafe because they are unparseable and untestable. Atomic actions convert each step into the smallest typed operation:

```python
{"action": "generate_text", "inputs": {"topic": "AI agents", "length": "500 words"}}
```

Properties of a good atomic action:
- Has a clear, singular intent
- Has a typed input schema that can be validated before execution
- Either succeeds completely or fails completely (no partial states)
- Is independently testable

The conversion from step-string → atomic-action dict uses the same `generate_structured` + validate + retry pattern as any other structured output call.

### AoT — Atom of Thought dependency graphs

Once you have atomic actions, the natural extension is to express ordering constraints explicitly rather than implicitly relying on sequential execution:

```json
{"nodes": [
  {"id": "1", "action": "research_topic", "depends_on": []},
  {"id": "2", "action": "create_outline",  "depends_on": ["1"]},
  {"id": "3", "action": "write_section_A", "depends_on": ["2"]},
  {"id": "4", "action": "write_section_B", "depends_on": ["2"]},
  {"id": "5", "action": "review",          "depends_on": ["3", "4"]}
]}
```

The graph structure enables:
- **Dependency resolution**: actions with no pending dependencies can start immediately
- **Parallel execution**: independent branches (3 and 4 above) can run concurrently
- **Validation**: circular dependencies and missing node references can be caught before any work is done
- **Observability**: the graph is explicit — you can log and inspect exactly which nodes ran and in what order

The pguso repo calls this AoT (Atom of Thought) and notes it "feels inevitable, not advanced" once you understand planning + atomic actions separately.

### The planning–execution boundary

A pattern that recurs across sources in this vault:
- **Plan** = produce the data structure (cheap, inspectable, reversible)
- **Execute** = act on the world (expensive, consequential, sometimes irreversible)

Keeping these phases separate provides a natural point for validation, human review, resource estimation, and rollback.

## Open questions

- How should an agent revise its plan mid-execution when early steps fail or return unexpected results?
- When does the plan granularity (coarse steps vs fully atomic) trade off against planning latency?
- How do AoT dependency graphs compose when one agent's plan calls sub-agents with their own plans?

## Related pages

- [[Agentic Loop]]
- [[Agent Memory]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]
- [[pguso - Agents From Scratch]]
- [[Direct Corpus Interaction]]
- [[AI Knowledge Base Overview]]
