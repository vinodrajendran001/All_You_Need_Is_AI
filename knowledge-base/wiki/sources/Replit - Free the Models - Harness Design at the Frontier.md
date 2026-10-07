---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-09-30-replit-free-models-harness-design
source_title: "Free the models: Harness design at the frontier"
source_author: "Daniel Furman, Jacky Zhao, Vaibhav Kumar, Ed Sioufi, Michele Catasta"
source_url: https://replit.com/blog/free-the-models
tags: [source/summary, coding-agents, multi-agent, routing, inference]
source_ids: [src-2026-09-30-replit-free-models-harness-design]
status: active
---

# Replit - Free the Models - Harness Design at the Frontier

## Summary

Replit describes a harness in which the core model chooses specialists, worker tiers, worker effort,
and when to revisit an existing subagent. Its own effort can change during a turn. The authors argue
for exposing useful primitives instead of prescribing one orchestration policy for every model.
This is a first-party design and benchmark report, not evidence that the harness can be removed.

## Key claims

The four primitives are domain specialists, tier-and-effort selection, reusable subagents, and
dynamic mid-turn effort. Replit still chooses the available specialists, interfaces, and guardrails;
simple work may use no subagents. Cache-preserving effort changes depend on model support.

Production observations were collected at **medium effort**, for one week per model in different
months. Their denominators must remain separate:

| Metric | Fable 5 | Fable 5.1 | Astra |
| --- | --- | --- | --- |
| Turns dispatching any subagent | 32% | 21% | 36% |
| Turns dispatching a general worker | 0.9% | 2.3% | 20% |
| Dispatches returning to an existing subagent | 17% | 29% | 42% |

These are different production cohorts, not randomized comparisons of model coordination ability.

The benchmark setup uses **Replit Max mode with Astra as the core**, with four repetitions.
The table below preserves the article's rounded prose figures:

| Configuration | DeepSWE v1.1 accuracy / cost per task | Terminal-Bench 4.0 accuracy / cost per task |
| --- | --- | --- |
| Replit Agent | 72% / $2.11 | 49% / $2.53 |
| Replit sidekick, one long-lived worker | 61% / $1.34 | 33% / $1.84 |
| Public mini-swe-agent Astra low | 67% / $1.60 | 42% / $2.25 |
| Public mini-swe-agent Astra xhigh | 74% / $4.43 | 60% / $5.86 |

DeepSWE contains **113 tasks**. Terminal-Bench contains **63 evaluated tasks after excluding three
GPU tasks**. The figure labels give Replit's less-rounded scores as **71.7%**, with a 95% interval
of **69.4-73.9**, and **49.2%**, with an interval of **44.6-53.8**. The corresponding sidekick
labels are **60.6%** and **32.5%**. The prose's 11- and 16-point gains are rounded comparisons,
not exact differences between the figure labels.

## Why it matters

Model-chosen coordination can be an efficiency policy while authority stays in the harness. The
benchmark is also a useful example of **nondominance**: Replit occupies a quality/cost tradeoff among
the reported points. The sidekick is cheaper but less accurate; xhigh is more accurate but more
expensive. Neither comparison establishes that Replit wins both axes.

## Tensions / open questions

The public baselines were not controlled reruns in Replit's environment. Task exclusions, harness
differences, model configuration, and cost accounting limit comparisons. The report does not isolate
each of the four primitives' causal contribution or establish general superiority of model-selected
routing. The opening claim that a router is always less capable than its chosen model is the
authors' argument; their system still includes a trained effort-escalation controller.

## Affected pages

- [[Agent Delegation]]
- [[Model Routing]]
- [[Reasoning Effort Control]]
- [[Coding Agent Harness]]
- [[Harness Optimization]]
- [[Inference Efficiency Frontier]]
- [[Graph Engineering]]
- [[Replit]]

## Raw capture

- [[Free the models Harness design at the frontier]]

## Citations

- Canonical URL: <https://replit.com/blog/free-the-models>
- Published September 30 and captured October 5, 2026.

## Related pages

- [[Ethan Mollick - The Dot and the Swarm]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Agent Security and Governance]]
- [[Serving Benchmarks and Goodput]]
