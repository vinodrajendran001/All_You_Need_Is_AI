---
type: source-summary
created: 2026-08-05
updated: 2026-08-26
source_id: src-2026-08-05-aibuilderclub-andrew-ng-loop-to-graph-engineering
source_title: "Andrew Ng's Agentic Design Patterns, Mapped to Graphs"
source_author: AI Builder Club
source_url: https://www.aibuilderclub.com/blog/andrew-ng-loop-to-graph-engineering
tags: [source/summary, ai-agents, ai-builder-club]
source_ids: [src-2026-08-05-aibuilderclub-andrew-ng-loop-to-graph-engineering]
status: active
---

# AI Builder Club - Andrew Ng's Agentic Design Patterns, Mapped to Graphs

## Summary

The article carefully separates Andrew Ng's published agentic design patterns—reflection, tool use, planning, and multi-agent collaboration—from AI Builder Club's own mapping of those patterns onto graph structures. It argues that Ng did not present the patterns as steps, a maturity ladder, or a progression from loops to graphs.

The proposed mapping is deliberately non-exclusive: reflection may be a self-review loop, tool-backed check, or critic node; planning may remain data inside one worker or become shared graph state; and multiple agents do not automatically create shared state or a well-defined graph.

## Key claims

- Ng's four patterns describe capabilities and collaboration techniques, not one required topology.
- Reflection can use deterministic tools, self-critique, or a separate evaluator.
- Tool calls may be internal to a worker or represented as explicit nodes.
- Planning and routing are related but distinct; a stored plan does not itself define control flow.
- Claims about an Ng-authored graph-engineering PDF were not verified from a primary source in the article's bounded search.

## Why it matters

The source protects attribution while giving [[Agent Planning]] and [[Agentic Loop]] a flexible implementation menu. It also warns against turning useful patterns into an invented sequence backed by borrowed authority.

## Tensions / open questions

- The absence of a verified PDF in the searched sources does not prove that no such document exists.
- The source's loop-to-graph recommendation is an editorial synthesis, not Ng's framework.
- Different implementations of the same pattern may have very different observability, cost, and reliability properties.

## Affected pages

- [[Agent Planning]]
- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]

## Citations

- Raw capture: [[2026-08-05 AI Builder Club - Andrew Ng's Agentic Design Patterns, Mapped to Graphs]]
- Canonical URL: [https://www.aibuilderclub.com/blog/andrew-ng-loop-to-graph-engineering](https://www.aibuilderclub.com/blog/andrew-ng-loop-to-graph-engineering)

## Raw capture

- [[2026-08-05 AI Builder Club - Andrew Ng's Agentic Design Patterns, Mapped to Graphs]]

## Related pages

- [[Coding Agent Harness]]
- [[Agent Memory]]
- [[Multi-Turn Evaluation]]

