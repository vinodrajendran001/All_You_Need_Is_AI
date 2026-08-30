---
type: entity
created: 2026-08-30
updated: 2026-08-30
entity_kind: person
tags:
  - entity
  - person
  - agents
  - self-improvement
  - research
source_ids:
  - src-2026-07-16-lilian-weng-harness-engineering
status: active
---

# Lilian Weng

## What it is

A researcher and writer whose long-form technical surveys are widely used as reference material in the
LLM field. Formerly at OpenAI, she now writes at *Lil'Log*, where posts function less as commentary
than as literature reviews with an argument.

## Why it matters here

Weng supplies this vault's most complete map of agent scaffolding.
[[Lilian Weng - Harness Engineering for Self-Improvement]] introduces the **optimization ladder** —
prompts, structured context, workflow, harness code, optimizer code — that organizes
[[Harness Optimization]] and gives [[Recursive Self-Improvement]] a mechanical vocabulary it lacked.

Two of her reported findings do the most work in this vault:

- **STOP improved with GPT-4 but degraded with GPT-3.5 and Mixtral.** Recursive structure alone is not
  a source of gain.
- **Harness-updating capability is flat across model scale while harness-benefit is non-monotonic**
  (per Lin et al.), which predicts that scaffolding investment pays off most in the middle of the
  capability range.

## Notes

- Her survey style is to name failure modes precisely — **context collapse**, diversity collapse,
  "numerical duct tape" — and those names have been adopted directly into this vault's pages.
- She forecasts that harness techniques will be absorbed into core model behaviour the way prompt
  engineering was, while the need to specify goals, constraints, context, and evaluation persists.
- Her prescription that the evaluator stay read-only to the optimizing agent is the vault's clearest
  engineering answer to reward hacking in self-improving systems.

## Related pages

- [[Harness Optimization]]
- [[Recursive Self-Improvement]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
