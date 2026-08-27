---
type: entity
created: 2026-08-27
updated: 2026-08-27
entity_kind: organization
tags:
  - entity
  - organization
  - open-models
  - reinforcement-learning
source_ids:
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
status: active
---

# IBM

Enterprise technology company whose **Granite** family is its open-weight language-model line,
released under Apache 2.0 and published on Hugging Face with accompanying build reports.

## Why this entity matters here

IBM enters this vault through a single source, but an unusually useful one. Most open-weight
releases documented here publish a model card with benchmark numbers and a rough method
description. [[IBM Granite Team - Granite 4.2 LLMs How They're Built]] instead publishes the
**recipe with its hyperparameters** — the full post-training ladder, prompts and generations per
step, KL coefficients, learning rates, rollout turns, and the infrastructure underneath.

That level of disclosure is what makes IBM matter to this vault rather than the models themselves.
The vault's coverage of [[Agentic Reinforcement Learning]] came from surveys and framework
write-ups describing what teams *could* do. Granite 4.2 is the first source here stating what one
team actually did, end to end, for a family that shipped. It is the worked example behind
[[Staged Reinforcement Learning Curriculum]].

## Granite 4.2 in brief

- Three dense decoder-only reasoning models — 3B, 8B, 30B — pre-trained from scratch on ~15T tokens
  and released under Apache 2.0.
- Every model has a thinking / non-thinking switch plus a **low-effort** mode that spends a short
  reasoning budget on easy questions, and native tool calling in OpenAI function-calling format.
- Post-training runs as a chain of separate GRPO stages: RLVR → skill boosters → SWE agent →
  Terminal agent → Search agent → RLHF, with the agentic block trained only for 8B and 30B.
- Trained on an NVIDIA GB200 NVL72 cluster hosted by CoreWeave, using [[NVIDIA]]'s NeMo-RL and
  NeMo-Gym stack.

## Position in the open-model landscape

IBM's release sits in the same Apache-2.0, weights-and-report tier as the other permissive families
tracked on [[Open Model Ecosystems]]. What distinguishes it is the direction of the openness:
Granite's headline benchmark scores are not what a reader takes away, since they are self-reported
and offered without cross-family comparison. The training methodology is.

The vault should treat IBM as a **methodology source first and a capability source second**. The
recipe is reusable; the benchmark table is a first-party claim.

## Caveats

- The Granite 4.2 report is written by the team that shipped the model, on its own model card.
  Benchmarks are self-reported, unaudited, and not compared against other families.
- Nothing in the recipe is ablated. Every design choice — the staged chain, the leave-one-out
  baseline, the KL schedule, bounded-staleness asynchronous rollouts — is presented as what was
  done, not as what was tested against an alternative.
- The report contains an unresolved internal inconsistency about context length: pre-training phase
  5 is said to reach 512K tokens while the architecture table lists 131,072 and long-context results
  stop at RULER 128K.
- The raw capture bylines four individual contributors — Yousaf Shah, Swanand Kadhe, Riddhiman
  Moulick, and Ashish Sunil Agrawal — while the post itself attributes authorship to "Granite Team,
  IBM". This vault attributes the source to the team.

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[Staged Reinforcement Learning Curriculum]]
- [[Agentic Reinforcement Learning]]
- [[Open Model Ecosystems]]
- [[Group Relative Policy Optimization]]
- [[NVIDIA]]
- [[Hugging Face]]
