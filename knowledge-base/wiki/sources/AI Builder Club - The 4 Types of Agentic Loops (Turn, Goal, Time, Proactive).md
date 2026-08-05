---
type: source-summary
created: 2026-08-05
updated: 2026-08-05
source_id: src-2026-08-05-aibuilderclub-types-of-agentic-loops
source_title: "The 4 Types of Agentic Loops (Turn, Goal, Time, Proactive)"
source_author: AI Builder Club
source_url: https://www.aibuilderclub.com/blog/types-of-agentic-loops
tags:
  - source/summary
  - ai-agents
  - ai-builder-club
source_ids:
  - src-2026-08-05-aibuilderclub-types-of-agentic-loops
status: active
---

# AI Builder Club - The 4 Types of Agentic Loops (Turn, Goal, Time, Proactive)

## Summary

AI Builder Club proposes a four-rung taxonomy based on which part of an agent cycle is delegated. Turn-based loops delegate approval of tool calls within a user-started turn. Goal-based loops delegate the stop decision to an external evaluator. Time-based loops delegate repeated triggering to a clock while a session remains available. Proactive loops run from schedules or events without an open session.

The taxonomy is the author’s synthesis of documented agent primitives, not a universally established standard. Its practical message is that each increase in autonomy should be earned by stronger verification, because automating triggers before automating trustworthy stopping creates “doom loops.”

## Key claims

- Turn-based automation is appropriate for supervised interactive work but relies on the acting model’s own judgment about completion.
- Goal-based loops are the pivotal step toward unattended work because a fresh evaluator checks a measurable completion condition after each turn.
- Completion conditions should specify an end state, evidence proving it, constraints that must remain true, and a hard turn or budget cap.
- Time-based loops are suitable for polling external processes but remain session-scoped and depend on the session’s tools and permissions.
- Proactive loops move execution to scheduled or event-driven infrastructure and therefore demand stronger state, security, monitoring, and recovery.
- The safe migration path is supervised turn-based work, then goal-based verification, then timed polling, and only then independent proactive execution.

## Why it matters

The taxonomy turns abstract autonomy into explicit handoffs and gives [[Agentic Loop]], [[Agent Planning]], and [[AI Agents in Production]] a practical maturity ladder. It also makes [[Multi-Turn Evaluation]] central to stopping behavior rather than merely offline quality measurement.

## Tensions / open questions

- Product-specific commands and scheduling behavior may change; the taxonomy is more durable than the cited implementations.
- A model-based stop evaluator may still accept incomplete evidence or share blind spots with the worker.
- The ladder implies a progression, but some event-driven tasks may be safe before they are naturally expressible as goal-based conversations.
- Hard caps control cost but do not define useful partial outcomes after termination.

## Affected pages

- [[Agentic Loop]]
- [[Agent Planning]]
- [[Multi-Turn Evaluation]]
- [[AI Agents in Production]]
- [[Coding Agent Harness]]

## Citations

- Raw capture: [[2026-08-05 AI Builder Club - The 4 Types of Agentic Loops (Turn, Goal, Time, Proactive)]]
- Canonical URL: https://www.aibuilderclub.com/blog/types-of-agentic-loops

## Related pages

- [[Tool Use and Function Calling]]
- [[Agent Memory]]
- [[Context Engineering]]
- [[AI Knowledge Base Overview]]
