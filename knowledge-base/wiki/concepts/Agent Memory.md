---
type: concept
created: 2026-06-05
updated: 2026-06-05
tags:
  - concept
  - agents
  - memory
  - state
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-05-21-bytebytego-batch
status: active
---

# Agent Memory

## Definition

Agent memory is the set of mechanisms by which an agent retains information beyond the immediate prompt context. This vault's sources distinguish three layers: **in-context state** (what the model can see right now), **short-term session memory** (facts stored within one interaction sequence), and **long-term persistent storage** (data that survives across separate sessions).

## Why it matters

Without memory, every agent interaction starts from scratch. Memory is what enables agents to accumulate context over time, maintain user preferences, and build on earlier steps in a workflow. It is also what makes agent behaviour auditable — memory is explicit storage, not a hidden internal state.

## Current synthesis

### The context/memory distinction

[[pguso - Agents From Scratch]] makes the clearest definition in this vault:
- **Context** = everything currently in the prompt. Temporary. Gone when the interaction ends.
- **Memory** = persistent storage that outlives the prompt. Loaded into context on demand.

The model never accesses memory directly. It only sees what the surrounding system chooses to include in the prompt. This keeps memory auditable and controllable.

### Explicit over implicit

The pguso repo stores memory as a simple list of strings and gives the model explicit control over what gets saved:

```python
# Agent returns structured output including what to remember
{"reply": "Nice to meet you, Alice!", "save_to_memory": "User's name is Alice"}
```

The application layer writes this to the memory store. On the next interaction, it prepends all stored facts to the prompt:

```
You remember the following:
- User's name is Alice
```

This pattern is simple, inspectable, and gives the developer full visibility into what the agent "knows." There is no opaque embedding lookup; facts are plain text.

### Short-term vs long-term

| Layer | Lifetime | Storage | Use case |
|-------|----------|---------|----------|
| In-context state | One loop iteration | `AgentState` object (steps, done, current_plan) | Loop control, step counting |
| Session memory | One multi-turn session | In-memory list or Redis | User name, task progress, partial results |
| Long-term memory | Across sessions | PostgreSQL, files, vector DB | User preferences, historical summaries, project facts |

The Grab production case from [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]] uses Redis for fast session needs and PostgreSQL for conversation history — a direct instance of this tiered pattern.

### Memory as a reliability lever

Simple exact-match retrieval ("get all facts") is surprisingly powerful for small knowledge bases and is the right starting point. The upgrade path to semantic retrieval (embedding-based lookup for large memory stores) is a separate architectural decision that need not happen at the beginning.

The important invariant is: **memory content should always be auditable plain data, not an opaque learned embedding.** Even when embeddings are used for retrieval, the retrieved item should be a readable fact.

### State vs memory

[[pguso - Agents From Scratch]] also distinguishes agent *state* from agent *memory*:
- **State** (`AgentState`) tracks loop mechanics: step count, done flag, current plan. It resets between runs.
- **Memory** stores facts the agent should know. It persists across runs.

Both are Python objects the developer can inspect at any time, which is what makes debugging possible.

## Open questions

- At what memory store size does simple "get all" retrieval break down and semantic retrieval become necessary?
- How should conflicting facts be handled — does a newer memory overwrite an older one, or do both persist?
- How should memory be scoped when multiple users share an agent system?

## Related pages

- [[Agentic Loop]]
- [[Agent Planning]]
- [[AI Agents in Production]]
- [[Tool Use and Function Calling]]
- [[pguso - Agents From Scratch]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Retrieval-Augmented Generation]]
- [[AI Knowledge Base Overview]]
