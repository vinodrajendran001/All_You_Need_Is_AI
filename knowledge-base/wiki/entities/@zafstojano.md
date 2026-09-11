---
type: entity
created: 2026-09-11
updated: 2026-09-11
entity_kind: person
tags:
  - entity
  - topic/training
  - topic/synthetic-data
  - topic/reinforcement-learning
source_ids:
  - src-2026-09-09-zafstojano-recursive-synthetic-improvement
status: active
---

# @zafstojano

## What it is

Researcher and creator of **Reasoning Gym**, a library of procedural task generators used in the training
mixes of Olmo 3 and Nemotron 3 Super. Writes long surveys of the training stack.

## Why it matters here

His survey *Recursive Synthetic Improvement* is the vault's map of [[Synthetic Data Flywheel]], and its
organising claim reframes [[Recursive Self-Improvement]] into something checkable: the recursion runs
through **artifacts** rather than weights, across five stages — Judge, Corpus, Teacher, Curriculum,
Environment — each of which can be independently examined for whether the human has actually been removed.

The survey's most useful property is that it assembles primary results rather than narrative: DCLM
discarding ~98% of extracted tokens, BeyondWeb's gains tracing to per-token information density rather
than generator knowledge, OpenThoughts3 finding QwQ-32B a better teacher than the stronger DeepSeek-R1,
and GLM-5.3 improving non-marginally over GLM-5.2 with identical architecture and parameters after one
month of environment and RL scaling.

He is also the source of the caveat that most limits the framing, and it is his own: the apparent
exponential "is mostly an artifact of just how little these labs disclose."

## Notes

- Reasoning Gym is his own project and appears in the Environment section of his own survey — a stated
  interest worth noting when weighing that section.
- Collects the market data on [[RL Environment Design]]: Anthropic leadership reportedly discussing over
  $1B on environments in a single year, Mercor dominant at roughly $2B gross annualised run rate, and
  Prime Intellect open-sourcing through the Environments Hub.
- Treats the Kimi K3 distillation allegations carefully, presenting the trace-stealing disclosure and the
  RL-does-not-distil counter-evidence side by side and reaching no verdict.
- Quotes [[Nathan Lambert]] on the limits of distillation as an explanation: "One does not simply
  'distill' RL environments, infrastructure to run them at scale, or algorithms to mix them together
  effectively."

## Related pages

- [[Synthetic Data Flywheel]]
- [[Recursive Self-Improvement]]
- [[RL Environment Design]]
- [[Knowledge Distillation]]
- [[LLM-as-a-Judge]]
- [[LLM Training Pipeline]]
- [[Reward Design for RL]]
- [[@zafstojano - Recursive Synthetic Improvement]]
