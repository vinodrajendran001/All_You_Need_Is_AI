---
type: entity
entity_kind: organization
created: 2026-10-07
updated: 2026-10-07
tags: [entity, organization, coding-agents, orchestration]
source_ids:
  - src-2026-09-30-replit-free-models-harness-design
status: active
---

# Replit

## What it is

Replit is a software-development platform and the operator of Replit Agent. In this vault it
contributes a first-party account of model-selected delegation and effort allocation.

## Why it matters here

[[Replit - Free the Models - Harness Design at the Frontier]] describes domain specialists,
tier-and-effort selection, reusable subagents, and dynamic mid-turn effort. The model chooses
among harness-provided capabilities rather than following one fixed worker topology; the harness
still defines the choices and guardrails.

Its Max-mode Astra benchmarks place the system between cheaper lower-accuracy and more expensive
higher-accuracy configurations. The result is a reported quality/cost tradeoff, not a win on both
axes. The comparison uses four repetitions on 113 DeepSWE v1.1 tasks and 63 Terminal-Bench 4.0
tasks, excluding three GPU tasks from the latter.

## Evidence limits

The public baselines are not controlled reruns, and the four primitives are not separately ablated.
Medium-effort production telemetry comes from different one-week cohorts across models and months;
it should not be blended with the Max-mode benchmark into a causal coordination claim.

## Related pages

- [[Replit - Free the Models - Harness Design at the Frontier]]
- [[Agent Delegation]]
- [[Coding Agent Harness]]
- [[Model Routing]]
- [[Reasoning Effort Control]]
- [[Harness Optimization]]
- [[Graph Engineering]]
