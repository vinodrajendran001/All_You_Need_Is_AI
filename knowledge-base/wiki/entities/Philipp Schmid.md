---
type: entity
created: 2026-08-30
updated: 2026-11-13
entity_kind: person
tags:
  - entity
  - person
  - ai-agents
  - self-improvement
  - open-models
source_ids:
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
  - src-2026-11-01-philipp-schmid-code-mode
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

His second piece in the vault,
[[Philipp Schmid - Why Agents Are Soon Only Going to Have 1 Tool]], is a design argument rather than
a taxonomy. He predicts that agents will expose one code-execution tool to the model and call every
other tool as a typed function inside a script ("Code Mode"; see [[Programmatic Tool Calling]]). The
essay is useful for its mechanisms: tool schemas compiled into type declarations, an `ALL_TOOLS` map
for large catalogs, `text()`/`image()`/`audio()` helpers that choose what returns to the model, and a
host bridge that can inject OAuth tokens outside the sandbox, validate schemas, or pause for
confirmation on destructive calls. Asked whether every agent will soon have only a single `exec` tool,
he answers "Not necessarily", and the essay reports no measurement of its own.

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
- In the Code Mode essay he cites Factory's Droid 1.0 for "+3.5 points" of accuracy and "15%" lower
  model spend from switching to Code Mode; the Factory post reports those as two different
  comparisons (see [[Programmatic Tool Calling]]), so the pairing should not be cited as one measured
  effect.

## Related pages

- [[Philipp Schmid - Why Agents Are Soon Only Going to Have 1 Tool]]
- [[Programmatic Tool Calling]]
- [[Tool Use and Function Calling]]
- [[Recursive Self-Improvement]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Agent Plugin Architecture]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
