---
type: source-summary
created: 2026-08-03
updated: 2026-08-26
source_id: src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey
source_title: "Self-Improvements in Modern Agentic Systems: A Survey"
source_author: Zhe Ren et al.
source_url: https://arxiv.org/html/2607.13104v1
tags: [source/summary, ai-agents, self-improvement, survey]
source_ids: [src-2026-07-24-ren-et-al-self-improvements-agentic-systems-survey]
status: active
---

# Zhe Ren et al - Self-Improvements in Modern Agentic Systems

## Summary

The survey defines an FM agent as model parameters plus a scaffold of prompts, memory, tools, and control logic. It treats self-improvement as a durable, execution-derived update to either component rather than transient context or KV state.

## Key claims

- Parameter updates can use generated demonstrations, intrinsic evaluation, or grounded experience.
- Scaffold updates can modify prompts, memory, tools, workflows, and control logic; these changes should be versioned, validated, and reversible.
- Skills are serialized reusable updates; meta-level skills modify the system that executes future tasks.

## Caveat

The captured text ends during section 6.2.1, so it does not support claims about the survey's promised later evaluation and safety sections.

## Raw capture

- [[Self-Improvements in Modern Agentic Systems A Survey]]

## Related pages

- [[Recursive Self-Improvement]]
- [[Agent Skill]]
- [[Agent Memory]]
- [[Agentic Reinforcement Learning]]
