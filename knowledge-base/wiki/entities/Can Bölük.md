---
type: entity
created: 2026-09-04
updated: 2026-09-04
entity_kind: person
tags:
  - entity
  - person
  - engineer
  - harness
  - systems
source_ids:
  - src-2026-09-02-can-boluk-harness-playbook
status: active
---

# Can Bölük

## What it is

Systems engineer and author of [[Can Bölük - The Harness Playbook]], a ~36,000-word architectural critique of
coding agent harnesses written from the position of someone who has worked inside two of them (omp and Pi) and
intends to rebuild one from scratch.

## Why it matters here

Bölük is the vault's only source who treats a harness as a **game engine** rather than as an application. That
framing is the entire contribution: durability, replication, spectating, configuration, and hot-reload are all
problems game engines solved decades ago, and the argument is that harnesses are rediscovering them badly. He
anchors [[Harness State Authority]] and supplies most of the evidence in [[Tool Roster Economics]].

What makes the source usable as reference material is that the criticism is measured rather than asserted. He
audits **78 official Pi extension examples** and reports that of the 17 with state, only two are correct; he times harnesses on a fixed task and reports
**36.6s / 37.0s / 42.2s**, having first confirmed the complaint that his own harness ran almost twice as slow as
Codex; he profiles a
render path and finds **267s reduced to 90ms**, with 98.7s of the original in one string-wrapping function. Where
a claim rests on judgement rather than measurement, he generally says so.

He is also willing to name his own side's mistakes. The two extensions that collide over a private workflow mutex
were both written by him, and he uses that as the evidence that the missing abstraction is real rather than as an
embarrassment to skip past.

## Notes

- Background is Source Engine and low-level systems work; the **convar** proposal for harness configuration and
  the incremental-snapshotting model for durability both come directly from that lineage.
- His reading of Dijkstra's "simplicity is prerequisite for reliability" — that it has been flattened into
  *simple good, complex bad* — paired with Ousterhout's "embrace suffering," is the philosophical spine of the
  piece: complexity should be pushed down into the module, not eliminated by refusing to build things.
- Position on implementation language is blunt: **"TypeScript is an awful choice at the moment,"** with the
  reasoning that a language's defaults act as a prior for generated code. His proposed rebuild is a Rust engine
  with Python extensions, chosen partly because Python can inspect its own AST.
- The piece is a design document for unbuilt software. Treat its prescriptions as hypotheses; only the audits,
  timings, and profiles are evidence.

## Related pages

- [[Can Bölük - The Harness Playbook]]
- [[Harness State Authority]]
- [[Tool Roster Economics]]
- [[Coding Agent Harness]]
- [[Harness Optimization]]
- [[Agent Plugin Architecture]]
- [[LLM-Native Extensible Software]]
- [[Agent Security and Governance]]
- [[Context Engineering]]
- [[AI Knowledge Base Overview]]
