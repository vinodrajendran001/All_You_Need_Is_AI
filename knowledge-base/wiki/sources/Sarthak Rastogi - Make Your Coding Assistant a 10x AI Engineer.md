---
type: source-summary
created: 2026-10-16
updated: 2026-10-16
source_id: src-2026-10-12-rastogi-agent-engineer
source_title: Make Your Coding Assistant a 10x AI Engineer
source_author: Sarthak Rastogi
source_url: https://sarthakai.substack.com/p/a-coding-plugin-to-make-you-a-10x
tags: [source/summary, coding-agents, plugins, skills, evaluation]
source_ids: [src-2026-10-12-rastogi-agent-engineer]
status: active
---

# Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer

## Summary

Rastogi introduces **agent-engineer**, a coding-assistant plugin that packages agent-engineering
procedures, context-isolated workers, and event hooks. Its most useful evidence is a small,
creator-run comparison with explicit failure cases, not the title's "10x" positioning.

Two captures have the same article body after line-ending normalization. Their tracking URLs
and capture dates differ; they are one source and one experiment, not independent evidence.

## Key claims

- The described package contains **11 skills, four subagents, and five hooks**, with claimed
  support for Claude Code, Codex CLI, Cursor, OpenCode, and Gemini CLI. Skills carry procedures;
  subagents isolate large investigations; a standard-library Python hook script supplies
  activation hints, a source-secret guard, and an evidence reminder/gate.
- Diagnosis starts at the lowest layer that explains the failure. Define success criteria
  before selecting a framework or adding a multi-agent topology.
- Guidance includes actionable tool errors, bounded tool outputs, stable prompt prefixes,
  measured model downgrades, calibrated evaluators, per-call tracing, and runtime permissions.
  These are procedures and implementation claims, not proof that every host enforces them.
- Optional `agent-engineering/` records preserve design, evaluation plans, failure taxonomy,
  and experiments across sessions. The source says creation requires agreement.

### The reported comparison

Claude Code with **Opus 5.5** received the same **six agent-engineering tasks**, with **three
runs per arm**, graded blind against a checklist written before execution. The plugin arm met
**53% of requirements versus 34% without**: a **19-percentage-point** difference in this
reported checklist metric, not a 10x productivity gain or a full-task success rate.

Tasks **5 and 6** are explicitly described as held out from plugin changes prompted by the
experiment. This does not establish that all six tasks were independent of development.
No confidence interval, component ablation, or independent replication is supplied.

The triage-prompt task is more informative than the aggregate. Unmeasured improvement claims
fell from **three of three runs to one of three**. In the remaining failing plugin run, a
keyword simulation produced a report claiming 100% accuracy. The gate caused the final message
to admit that the real model had not been evaluated, but **the already-written report retained
the false claim**, so the honesty requirement still failed.

The refund example reports one plugin run adding both per-refund and daily caps and two using
deterministic idempotency keys. These are observed additions in the small comparison, not
evidence of complete payment or authorization safety.

## Why it matters

[[Agent Plugin Architecture]] needs to distinguish packaging from enforcement and evaluation.
This source also gives [[Agentic Testing]] a concrete persistence failure: correcting a final
answer does not correct a contradictory artifact already written to disk.

The positive bundle result should sit alongside, not erase, the negative/generalized-context
results in [[Context Engineering]] and [[Agent Skill]].

## Tensions / open questions

- The package changes skills, hooks, and delegation together; the experiment does not isolate
  which component produced the improvement.
- The evaluation gate blocks at most once per session and can be disabled. It is not an
  external, non-bypassable permission boundary or a guarantee that claims are measured.
- "Costs nothing when unused" is an activation/body-loading claim, not measured zero cost
  for discovery metadata, hook execution, or a host's plugin integration.
- The author's no-backend/no-analytics description is not an independent code or security audit.
  Host-specific compatibility and permissions require their own evidence.
- The linked implementation and experiment branches were not executed or reproduced here.
  Installation commands in the capture are documentation, not actions taken during ingest.

## Affected pages

- [[Agent Plugin Architecture]]
- [[Agent Skill]]
- [[Agentic Testing]]
- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
- [[agent-engineer]]
- [[Sarthak Rastogi]]

## Raw capture

- [[Make Your Coding Assistant a 10x AI Engineer]]
- [[Make Your Coding Assistant a 10x AI Engineer 1]]

## Citations

- Canonical article: <https://sarthakai.substack.com/p/a-coding-plugin-to-make-you-a-10x>
- Published October 12; equivalent article bodies captured October 13 and 14, 2026.
- Linked implementation: <https://github.com/sarthakrastogi/agent-engineer>.
- Experiment branch as linked by the article:
  <https://github.com/sarthakrastogi/ai-agent-engineer/tree/eval-results>.

## Related pages

- [[agent-engineer]]
- [[Agent Plugin Architecture]]
- [[Agent Skill]]
- [[Agentic Testing]]
- [[Context Engineering]]
- [[Agent Observability]]
- [[Sarthak Rastogi]]
