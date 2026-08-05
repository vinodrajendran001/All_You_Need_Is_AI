---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-andrew-ng-loop-to-graph-engineering
title: Andrew Ng's Agentic Design Patterns, Mapped to Graphs
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/andrew-ng-loop-to-graph-engineering
published: '2026-07-29'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Andrew Ng's Agentic Design Patterns, Mapped to Graphs

**Andrew Ng published reflection, tool use, planning, and multi-agent collaboration as design patterns for agentic workflows. His March 2024 post does not present them as an ordered progression from loop engineering to graph engineering.** This article keeps his source claim intact and adds a separate implementation view: how we at AI Builder Club might place those patterns inside an [agent graph](/blog/graph-engineering-guide-2026).

The distinction matters because two widely shared X posts describe an Andrew Ng PDF that neither post links. Their loop-to-graph packaging can still prompt a useful architecture discussion, as long as it is labeled as someone else's synthesis rather than Ng's method.

## What Ng actually published

In his [March 2024 post](https://x.com/AndrewYNg/status/1773393357022298617), Ng called reflection, tool use, planning, and multi-agent collaboration "four design patterns for AI agentic workflows." He described agentic work as prompting an LLM multiple times so it can build toward a better result.

His reflection example also rules out a narrow one-node interpretation. Ng wrote that tools such as unit tests or web search can evaluate an output. He then described another implementation with a generator agent and a separate critic agent. Reflection can be a self-review cycle, a tool-backed evaluation cycle, or a collaboration between agents.

The current [Agentic AI course](https://www.deeplearning.ai/courses/agentic-ai) teaches the same patterns alongside evaluation and error analysis. Its access language is specific: free auditors can watch course videos and participate in the community forum, while assessments, certificates, and project tools require Pro membership. The Pro description also names quizzes and interactive labs.

None of those sources calls the patterns steps, orders them as a maturity ladder, or identifies multi-agent collaboration with a graph. The loop-to-graph order below is our synthesis.

## What we could verify about the PDF claims

The [@0xCodila post](https://x.com/0xCodila/status/2080344428179259846) says Ng released an 8-page PDF, while the [@0xMovez post](https://x.com/0xMovez/status/2080728910291959884) claims 12 pages and uses a different title. Neither post links a document hosted by Ng or DeepLearning.AI.

Our check was bounded. As of 2026-07-29, we found no primary-source graph engineering PDF in the sources listed for this article. That finding supports caution about these two claims; it does not prove that no document can exist anywhere.

The useful material is already available directly through Ng's design-pattern post, Agentic AI course, and later feedback-loop letter. Readers do not need an unlinked PDF claim to study them.

## One possible mapping onto an agent graph

Ng's patterns describe capabilities and collaboration techniques. A graph describes execution structure through nodes, edges, routing, and state. The same pattern can have several graph implementations.

| Ng's pattern | One possible graph implementation | Other valid implementations |
| --- | --- | --- |
| Reflection | Route a draft to a critic, then return failed work for revision | A single worker can self-critique; tests or web search can supply feedback; a separate critic agent can review |
| Tool use | Represent a tool call as its own node and choose it with a conditional edge | A worker node can call a tool internally; either choice may be appropriate |
| Planning | Store a plan in graph state so later nodes can read and update it | A plan can drive a fixed sequence, remain data for one worker, or inform a router |
| Multi-agent collaboration | Give specialized agents separate nodes with explicit handoff edges | Agents can collaborate without shared state, and adding agents alone does not define a graph |

This table is an implementation menu, not a translation key. Tool use can change graph shape. Planning and routing solve related but different problems. Shared state has to be designed; it does not appear automatically when several agents collaborate.

## Our loop-to-graph synthesis

For a workflow with one objective and one reliable stopping condition, a single worker loop may be enough. Reflection can improve that loop, and tools can provide external evidence without requiring a multi-agent system.

When a plan needs to survive across actions, persist it as inspectable state. Add conditional edges only where the execution path genuinely branches. Introduce a specialized agent when a role needs its own instructions, context, permissions, or evaluation criteria.

That order is our build recommendation. It is not Ng's sequence, and the patterns do not depend on it. A tool node can appear before reflection, a planner can work inside one loop, or two agents can collaborate in a simple fixed chain.

Deterministic transforms, tool calls, routers, and human checkpoints are all valid nodes. Agentic worker nodes that are intended to revise their output need a verifier and a stopping condition, but every node in a multi-agent graph does not have to be a loop.

Ng's later [three-loop feedback model](/blog/loop-engineering-guide-2026#loops-nest-andrew-ngs-three-loop-model) covers a separate question about how product feedback arrives at different cadences around a system.

## How to choose an implementation

Keep the architecture small when one worker can own the task and its verifier. Tool calls can stay inside that worker if making them separate nodes adds no useful control or observability.

Use explicit graph structure when the path branches, a handoff must survive across runs, state needs inspection, or a human checkpoint controls what happens next. Multi-agent collaboration earns its cost when specialized roles have genuinely different context or evaluation criteria.

Define what passes and when retries stop for any node that produces iterative work. A deterministic transform or recorded human decision may need no loop; the [graph or loop decision guide](/blog/agent-graph-vs-loop-when-to-use) covers those tradeoffs in more detail.

---

## Related Content

- **[Graph Engineering: The 2026 Guide](/blog/graph-engineering-guide-2026)** - Nodes, edges, state, frameworks, and the cases where a graph earns its complexity.
- **[Graph or Loop: How to Decide](/blog/agent-graph-vs-loop-when-to-use)** - Architecture signals, costs, and failure modes.
- **[Graph Engineering with Claude Code](/blog/graph-engineering-with-claude-code)** - A practical implementation using subagents and explicit orchestration.
- **[Loop Engineering Guide](/blog/loop-engineering-guide-2026)** - Verifiers, stopping conditions, and the feedback loop inside an agentic worker.

---

## Start Here

Start with a task that already has a clear pass condition. Build one reliable worker, make its evidence visible, and add structure only when the next failure requires a branch, persistent state, or a specialized handoff.

The [**Loop Engineering course**](/courses/loop-engineering) covers the worker-level discipline behind that foundation. AI Builder Club also publishes source-linked teardowns when new agent architecture claims spread faster than their receipts.

If you want the version with receipts instead of claims, Jason showed three graphs running his own company in our August 2 workshop, and none of them are built on a framework. [Watch the session](/courses/live-ai-workshops?utm_source=blog&utm_medium=article&utm_campaign=andrew-ng-loop-to-graph-engineering).

[Join AI Builder Club](https://www.aibuilderclub.com)

In March 2024, Andrew Ng named reflection, tool use, planning, and multi-agent collaboration as design patterns for agentic workflows. That post does not call them steps or present them as an ordered path from loop engineering to graph engineering.

No. The patterns come from Ng. The ordered implementation mapping in this article comes from AI Builder Club, and it is one possible way to apply those patterns. They can be combined in other orders and architectures.

As of 2026-07-29, we found no primary-source PDF hosted by Andrew Ng or DeepLearning.AI in the sources searched. The two X posts characterized here claim different lengths, 8 pages and 12 pages, and neither links such a document.

One implementation can use a reflection cycle, tool nodes or in-node tool calls, a plan stored in state, conditional routing, and specialized agent nodes. None of those mappings is an identity: reflection can use a critic agent, planning can exist without routing, tool use can change graph shape, and multi-agent collaboration does not automatically provide shared state.

No. The course teaches useful agentic patterns and evaluation practices, while graph design adds explicit control flow and state where a workflow needs them. Free auditors can watch the videos and use the community forum, but the current course page reserves assessments, certificates, and project tools for Pro members.

Andrew Ng's March 2024 X post is the primary source for reflection, tool use, planning, and multi-agent collaboration as design patterns. It does not present an ordered loop-to-graph method. The implementation mapping in this article is our synthesis. We also checked Ng's June 2026 loop letter, the current DeepLearning.AI Agentic AI course page, and two X posts claiming conflicting PDF lengths. As of 2026-07-29, we found no Andrew Ng or DeepLearning.AI-hosted graph engineering PDF in those sources. See our [editorial standards](/about).
