---
type: concept
created: 2026-08-05
updated: 2026-10-07
tags:
  - concept
  - ai-agents
  - multi-agent
  - orchestration
source_ids:
  - src-2026-08-05-aibuilderclub-graph-engineering-guide-2026
  - src-2026-08-05-aibuilderclub-graph-engineering-vs-loop-engineering
  - src-2026-08-05-aibuilderclub-agent-graph-vs-loop-when-to-use
  - src-2026-08-05-aibuilderclub-is-graph-engineering-just-langgraph
  - src-2026-08-05-aibuilderclub-five-layers-ai-engineering
  - src-2026-08-05-aibuilderclub-graph-engineering-with-claude-code
  - src-2026-08-05-aibuilderclub-graph-engineering-peter-steinberger
  - src-2026-08-05-aibuilderclub-andrew-ng-loop-to-graph-engineering
  - src-2026-08-05-aibuilderclub-graph-engineering-karpathy-loop
  - src-2026-08-12-alyona-vert-agent-frameworks-sdks
  - src-2026-09-30-replit-free-models-harness-design
  - src-2026-10-01-mollick-dot-swarm
status: active
---

# Graph Engineering

Graph engineering is the design of a multi-node agent or workflow system: nodes perform specialized agentic or deterministic work, edges encode routing and retry behavior, and explicit shared state carries artifacts and provenance across handoffs. A single [[Agentic Loop]] can be viewed as a one-node graph with a return edge; a larger graph is justified only when one loop can no longer represent the work cleanly.

## When a graph earns its cost

A graph can help when the task genuinely requires:

- different specialist contexts, tools, permissions, or models;
- conditional routing between qualitatively different procedures;
- fan-out and fan-in for independent work;
- a separate reviewer or verifier;
- isolated retries and failure domains;
- auditable handoffs across a long-running process.

The first valuable extra node is often a read-only reviewer, not a fleet of conversational personas.

## Costs and failure modes

Graphs multiply system surfaces: prompts, state schemas, handoffs, routing decisions, credentials, logs, latency, and spend. Clean context isolation can improve focus but also loses tacit assumptions unless state records preserve evidence, uncertainty, and artifact identity. Parallelism can reduce wall-clock time while increasing total compute and correlated-error risk.

Use the smallest topology that matches the task. Fix prompt, context, tool, or harness failures at those layers before adding nodes. If a deterministic function can do a step, it need not become an agent.

## Relationship to prior art

The architecture overlaps state machines, DAG schedulers, workflow engines, actor systems, LangGraph, AutoGen, and Google ADK. "Graph engineering" is best treated as a design lens for agent orchestration rather than a new foundational computer-science primitive.

[[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]] shows how this lens appears in current runtimes: LangGraph, Google ADK, and Microsoft Agent Framework expose explicit graph/state primitives, while other frameworks favor role-based crews, event workflows, or minimal loops. Framework choice does not determine whether a graph is warranted.

## A graph can emerge within a designed boundary

[[Replit - Free the Models - Harness Design at the Frontier]] distinguishes exposing coordination
primitives from hard-coding a topology. The core chooses when to spawn or revisit a worker and
which specialist, tier, and effort to use; a simple task can stay one loop. Its first-party
benchmarks support a quality/cost tradeoff against a cheaper one-worker design, not a rule that
larger graphs always win.

[[Ethan Mollick - The Dot and the Swarm]] supplies the broader hypothesis that models will absorb
more of the coordination humans once scripted. His examples are anecdotes, and he leaves sustained
organizational work unresolved. Together the sources qualify rather than erase this page's advice:
**design the contracts, permissions, evidence, and stopping boundaries; measure whether topology
also needs to be prescribed**. Learned dispatch and deterministic business gates can coexist.

## Open questions

- What benchmarks reveal the point where specialization exceeds coordination overhead?
- How should state schemas preserve provenance without becoming another context dump?
- Which routing decisions should be deterministic, learned, or human-controlled?

## Related pages

- [[Replit - Free the Models - Harness Design at the Frontier]]
- [[Ethan Mollick - The Dot and the Swarm]]
- [[Agent Delegation]]
- [[Agent Workflow Maturity]]
- [[Loop Engineering]]
- [[Agentic Loop]]
- [[Agent Planning]]
- [[Agent Memory]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Multi-Turn Evaluation]]
- [[AI Agents in Production]]
- [[AI Builder Club - Build AI Agents]]
- [[Agent Frameworks]]
- [[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]]
