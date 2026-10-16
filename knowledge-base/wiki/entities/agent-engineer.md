---
type: entity
created: 2026-10-16
updated: 2026-10-16
entity_kind: tool
tags: [entity, coding-agents, plugins, skills, evaluation]
source_ids:
  - src-2026-10-12-rastogi-agent-engineer
status: active
---

# agent-engineer

## What it is

Sarthak Rastogi's coding-assistant plugin combining **11 skills, four subagents, and five
hooks** in the captured version. Its article claims support across several assistant hosts;
those compatibility and implementation claims were not independently tested in this ingest.

## Why it matters here

[[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]] supplies a small comparison
of a complete guidance/hooks/delegation bundle rather than another assertion that more
instructions must improve an agent. Six tasks, three runs per arm, and a blinded prewritten
checklist yielded **53% of requirements met versus 34%** without the plugin.

That **19-percentage-point** difference is not a 10x productivity gain or a full-task success
rate. Only tasks 5 and 6 are explicitly held out from experiment-driven changes; no component
ablation or independent replication is provided.

## Notes

- Optional `agent-engineering/` records preserve design and experiment context with user
  agreement. Their existence does not establish correctness or zero maintenance cost.
- The evaluation gate can be disabled and blocks at most once per session. It is a workflow
  aid, not an external, non-bypassable authorization boundary.
- In one failed run the gate corrected the final message but left an already-written report
  falsely claiming 100% accuracy. Evidence checks must cover persistent artifacts, not only
  the last response.
- On-demand skill-body loading does not demonstrate zero discovery, hook, or integration cost.
- Two raw captures preserve the same article body; they are one source and experiment.

## Related pages

- [[Sarthak Rastogi - Make Your Coding Assistant a 10x AI Engineer]]
- [[Sarthak Rastogi]]
- [[Agent Plugin Architecture]]
- [[Agent Skill]]
- [[Agentic Testing]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Agent Security and Governance]]
