---
type: entity
created: 2026-11-13
updated: 2026-11-13
entity_kind: organization
tags:
  - entity
  - organization
  - open-models
  - post-training
  - agents
source_ids:
  - src-2026-11-06-nous-arete-27b
  - src-2026-08-05-aibuilderclub-hermes-nous-research-self-improving-agent
  - src-2026-11-02-anil-compute-islands
status: active
---

# Nous Research

## What it is

Nous Research is an AI lab that works on open-weight models and releases models, datasets,
evaluations, and agent software. The vault meets it in three roles. It is the author of Arete-27B,
a values-targeted fine-tune of Qwen3.8-27B. It built Hermes Agent, a self-hosted agent daemon. A
repository link also identifies it as the host of the DisTrO report on low-communication
distributed training. The Hermes Agent capture describes Nous as "the team behind the Hermes,
Nomos, and Psyche model families"; the vault has no source on those families.

## Why it matters here

[[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]]
is the vault's first source written by Nous. It shows a lab whose method is to operate on other
organizations' open weights. Nous frames open weights as a hedge against frontier labs that "all
share a remarkably similar worldview", effective "so long as there are companies like Nous that can
operate on the weights". It published Arete's weights, evaluation, and training data. It also
chose its teacher partly by licence, picking an open model to avoid terms-of-use restrictions on
"illicit distillation". See [[Open Model Ecosystems]] and [[Knowledge Distillation]].

The same release states the constraint that method creates. Nous reports "similar contamination" to
what it suspects in Nemotron 3 Ultra. It explains that "the vast majority of high quality open
models are Chinese, and only open models have terms of use that permit this kind of tinkering and
experimentation". On the vault's reading, a lab that post-trains open weights inherits whatever
those weights and teachers carry. It then needs its own evaluation to see that inheritance, which
is what the 803-prompt evaluation is for.

## Notes

- **Agents.** [[AI Builder Club - Hermes Agent - Self-Hosted AI That Never Forgets You (2026)]]
  profiles Hermes Agent as built by Nous: a self-hosted, provider-agnostic daemon with persistent
  memory, scheduled work, and self-written skills. The capture gives a release date of February
  25, 2026. It relays "Nous Research's internal benchmarks", which claim that agents with 20+
  self-created skills complete similar tasks 40% faster than fresh instances. That is a
  third-party relay of an unverified first-party claim. See [[Agent Memory]] and [[Agent Skill]].
- **Benchmarks.** Arete's capability check uses Hermes Bench, which Nous calls its "internal
  general-capability benchmark" without describing it. Its scores are not comparable outside Nous's
  own reports.
- **Distributed training.** [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
  lists DisTrO, with DeMo, as "a separate line that compresses optimizer momentum in a transformed
  representation". It links DisTrO's preliminary report from a NousResearch GitHub repository. The
  capture does not otherwise discuss Nous, so this attribution rests on the link alone. See
  [[Distributed Training Parallelism]].
- **Evaluation stance.** Nous grades Arete with a third-party model, Grok 4.7, on its own rubric. It
  invites others to rerun the open evaluation, but the vault holds no independent rerun. See
  [[LLM-as-a-Judge]].
- Every Nous claim in the vault is first-party or relayed. Arete's political framing is Nous's own.

## Related pages

- [[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]]
- [[AI Builder Club - Hermes Agent - Self-Hosted AI That Never Forgets You (2026)]]
- [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
- [[Qwen]]
- [[Open Model Ecosystems]]
- [[Knowledge Distillation]]
- [[LLM-as-a-Judge]]
- [[Thinking Machines]]
- [[NVIDIA]]
- [[Agent Memory]]
- [[Agent Skill]]
- [[Distributed Training Parallelism]]
