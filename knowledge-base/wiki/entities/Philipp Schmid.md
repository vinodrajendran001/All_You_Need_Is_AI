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
  - open-models
source_ids:
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
status: active
---

# Philipp Schmid

## What it is

An AI engineer and writer (Google DeepMind; previously Hugging Face) who publishes practitioner-facing
analysis at philschmid.de, typically pairing a crisp definition with a survey of what the current
evidence does and does not support.

## Why it matters here

[[Philipp Schmid - Recursive Self-Improvement]] gives this vault its sharpest operational test for a
term that is usually used loosely. His three-tier taxonomy separates loops by **which layer persists
after a run**:

| Loop | Output | System | Verifier |
| --- | --- | --- | --- |
| Iteration | changes | fixed | fixed |
| Self-improvement | changes | changes | fixed |
| Recursive self-improvement | changes | changes | **rises** |

The test is falsifiable, and applying it shows that everything shipping today is the middle row. His
definition — *a loop in which a system makes a persistent change that improves its future performance
**and its ability to produce subsequent improvements*** — is the one [[Recursive Self-Improvement]]
now uses.

## Notes

- Two lines from him recur across this vault's pages: **"Reward hacking is the default behavior of a
  system asked to raise a number,"** and **"Agents will raise any number you give them. Recursive
  self-improvement without taste is a faster way to optimize the wrong thing."**
- He ranks harness postures by how much the agent may rewrite — conservative (Claude Code, Codex,
  Cursor), Pi, DeepSeek Harness — a ranking that doubles as a risk ladder in
  [[Agent Plugin Architecture]].
- He is careful to label the impressive results he cites (Karpathy's autoresearch, AlphaEvolve, Cline's
  overnight harness hill-climb) as **bounded** self-improvement, because in each the fitness function
  sat outside the editable region.

## Related pages

- [[Recursive Self-Improvement]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Agent Plugin Architecture]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Philipp Schmid - Recursive Self-Improvement]]
