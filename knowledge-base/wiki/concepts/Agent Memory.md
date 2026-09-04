---
type: concept
created: 2026-06-05
updated: 2026-09-04
tags:
  - concept
  - ai-agents
  - memory
  - state
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-05-21-bytebytego-batch
  - src-2026-06-29-siddhant-rai-nested-learning
  - src-2026-07-02-alyona-vert-ai-concepts-2026
  - src-2026-08-05-aibuilderclub-ai-agents-101-part-3
  - src-2026-08-05-aibuilderclub-agent-memory-systems-guide
  - src-2026-08-05-aibuilderclub-ai-coding-agent-memory-agentmemory
  - src-2026-08-05-aibuilderclub-codebase-memory-mcp-guide
  - src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey
  - src-2026-09-02-meta-organizational-second-brain
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

### Episodic, semantic, and procedural memory

The AI Builder Club collection adds a functional taxonomy:

- **episodic memory** records events and prior runs;
- **semantic memory** stores durable facts and relationships;
- **procedural memory** stores reusable instructions, skills, and workflows.

This taxonomy cuts across storage technologies. Files, databases, vector indexes, and codebase maps are implementation choices; the harder questions are what gets written, how stale or conflicting items are handled, and what is promoted into active context. Automatic accumulation without provenance, expiry, or conflict policy creates memory poisoning rather than learning.

### A contrasting frame: memory as structure, not storage

The sources above treat memory as **explicit stored data** loaded into context — auditable, plain-text, application-controlled. [[Siddhant Rai - Nested Learning]] introduces a deliberately different and more radical view that is worth preserving alongside it: memory as **learnable structure inside the model's own computation**, updated during inference rather than retrieved into the prompt. See [[Nested Learning]].

- It places memory on a **learning spectrum** — in-context (attention as ephemeral memory, erased when context clears), continual (accumulate across tasks, threatened by catastrophic forgetting), and inference-time (weights update during the forward pass).
- Its **Continuum Memory System** organizes memory as a chain of modules updated at different frequencies (fast/volatile recent detail → slow/stable consolidated knowledge), a structural answer to the **plasticity-stability tradeoff**.
- The tension with the storage view is real and intentional: storage memory is auditable but external and inert; structural memory is integrated and adaptive but harder to inspect and carries stability/safety risk. This vault keeps both framings rather than collapsing them.
- [[Alyona Vert - AI Concepts and Techniques in 2026]] adds a third framing to track: **conditional (selective) memory**, illustrated by DeepSeek's Engram, where a model *retrieves* memory through sparse lookups instead of storing everything in parameters or an ever-growing context. Its "U-shaped allocation law" — the best systems balance memory capacity against computation rather than maximising either — is a frontier signal that memory is becoming something a model decides *what to keep and when to fetch*, sitting between the storage and structural poles above.

## Memory as one of several scaffold update surfaces

[[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]] places memory inside a wider frame
that is useful for this page. It treats memory as one component of an agent's **scaffold** — alongside
prompts, tools, and control logic — and treats a write to any of them as the same kind of event: a
durable, execution-derived update.

The clarifying consequence is the survey's boundary between durable and transient. Context-window
contents and KV state are explicitly *not* memory in this sense, no matter how much an agent appears
to remember within a session. Only what survives the session and is retrievable afterwards counts.
That gives this page a sharper test than "does the agent recall it" — namely, does anything get
written back, and can a later run retrieve it.

It also suggests memory should be governed like the other scaffold surfaces: **versioned, validated,
and reversible**. Memory writes are usually treated as append-only bookkeeping, but under this framing
a bad memory write is the same class of event as a bad tool registration — a durable change to future
behavior that ought to be inspectable and undoable. See [[Recursive Self-Improvement]].

## Memory as a compiled, reviewable artifact

[[Meta - An Organizational Second Brain]] describes a memory system whose defining property is that **every
update is a text diff a domain expert can review in 30 seconds.** The agent's durable knowledge is 200+ structured
files — position files, taxonomies, routing indexes, gateway files — and improvement happens by compiling expert
feedback into those files rather than by writing embeddings, appending to a scratchpad, or retraining.

Two design rules distinguish it from the memory architectures already on this page.

**Memory is typed, and the types are enforced.** *Recipes* hold procedures and no domain facts; *knowledge files*
hold declarative positions and no procedures. The purpose is failure attribution: when the agent is wrong, the
type tells you whether the procedure or the knowledge is at fault. Undifferentiated memory stores cannot make
that distinction, which is why their failures are hard to fix rather than merely hard to detect.

**Memory declares its own dependency graph.** Each file names `depends_on` and `referenced_by` in frontmatter, so
the consequences of an edit are a lookup rather than an investigation — and so a deterministic linter can reject
dangling references and dependency cycles before anything is served.

The retrieval boundary is drawn by **information density and expected usage frequency**: dense, frequently needed
material is promoted into curated memory; the rest stays in a retrieval corpus. Loading that memory by
progressive disclosure rather than in full is reported to cut **tokens per turn by about 80%**.

The costs are the usual ones for curated memory, and the source does not hide them: the compile-validate-review
loop is ongoing human and machine expense, and the reported outcomes after three sprints are qualitative with no
denominators. See [[Institutional Knowledge Agents]].

## Open questions

- At what memory store size does simple "get all" retrieval break down and semantic retrieval become necessary?
- How should conflicting facts be handled — does a newer memory overwrite an older one, or do both persist?
- How should memory be scoped when multiple users share an agent system?
- When is **storage memory** (auditable, external) the right tool versus **structural/inference-time memory** (integrated, adaptive but opaque)? See [[Nested Learning]].

## Related pages

- [[Zhe Ren et al - Self-Improvements in Modern Agentic Systems]]
- [[Agentic Loop]]
- [[Agent Planning]]
- [[AI Agents in Production]]
- [[Tool Use and Function Calling]]
- [[pguso - Agents From Scratch]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Retrieval-Augmented Generation]]
- [[Nested Learning]]
- [[Siddhant Rai - Nested Learning]]
- [[Alyona Vert - AI Concepts and Techniques in 2026]]
- [[AI Knowledge Base Overview]]
- [[AI Builder Club - Build AI Agents]]
- [[Context Engineering]]
- [[Agent Security and Governance]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[Schema-Driven Knowledge Base]]
