---
type: source-summary
created: 2026-08-30
updated: 2026-08-30
source_id: src-2026-08-28-philipp-schmid-recursive-self-improvement
source_title: "Recursive Self-Improvement"
source_author: "Philipp Schmid"
source_url: "https://www.philschmid.de/recursive-self-improvement"
tags:
  - source/summary
  - topic/agents
  - topic/self-improvement
  - topic/evaluation
source_ids:
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
status: active
---

# Philipp Schmid - Recursive Self-Improvement

## Summary

A short, sharply argued piece that defines recursive self-improvement precisely enough to test, then
shows that no public system currently meets the definition. Schmid's definition: *a loop in which a
system makes a persistent change that improves its future performance **and its ability to produce
subsequent improvements***.

The organizing device is a three-tier taxonomy separated by **which layer persists after a run**, and
in particular by whether the verifier moves:

| Loop | Output | System | Verifier |
| --- | --- | --- | --- |
| **Iteration** — edit code, rerun the test | changes | fixed | fixed |
| **Self-improvement** — add a tool, record a skill | changes | changes | fixed |
| **Recursive self-improvement** — raise the bar itself | changes | changes | **rises** |

Everything shipping today, Schmid argues, is the middle row.

## Key claims

**A rising task score proves self-improvement, not recursion.** Recursion is a claim about a second
curve: does the next round face a *harder* bar that the system still cannot cheat? Nobody is
measuring that curve.

**Recursive self-improvement does not require a better model.** A frozen model with an honest
verifier and a writable environment can climb on its own. The easiest target is the harness.

**Concrete evidence that the bounded loop works.** Karpathy's autoresearch ran ~700 experiments on
one GPU against nanochat, kept ~20 changes that transferred, and cut time-to-GPT-2-quality from 2.02
to 1.80 hours; Prime Intellect scaled the same keep-or-revert loop to ~10,000 trials and beat the
human baseline. AlphaEvolve found a 48-multiplication algorithm for 4x4 complex matrix multiplication
(one fewer than Strassen's 49) and sped up a kernel used to train Gemini by 23%. Cline hill-climbed
Opus 4.5 from 47% to 57% on Terminal Bench by hand, then had an agent run the same method for 17
hours and about $50 of compute, moving Kimi K3 from 69 to 79 of 89 tasks.

**But the evidence is uneven and often negative.** HarnessOpt-Bench separates the editing agent from
the tester, evaluating candidate harnesses on hidden tasks; across 111 runs, 5 optimizer models, and
4 tasks, results varied sharply by model and by task. PAST-Bench asks whether stored experience helps
later episodes and finds that in many scenarios turning memory on **does not help**. A Princeton-led
study found agents can execute much of the engineering of AI research while still struggling to
choose original and useful directions.

**Model-harness co-evolution is the near-term shape.** SIA updates both a task agent's harness and its
weights; Recursive Harness Self-Improvement edits a harness partly to produce better traces for
training future models.

**Harnesses are becoming plugin kernels, which enlarges what an agent can rewrite.** Schmid ranks
three postures: conservative (Claude Code, Codex, Cursor — skills, hooks, and plugins extend a fixed
core); Pi (four built-in tools `read`, `write`, `edit`, `bash` and a system prompt under 1,000 tokens,
with everything else a TypeScript extension auto-discovered from `.pi/extensions/` that an agent can
write and reload mid-session); and DeepSeek Harness (built on the Cordis plugin kernel, where models,
tools, sessions, sandboxes, and the control loop itself are swappable, and plugin side effects unwind
on unload so the runtime can replace parts of itself without dying — shorthand `Agent = Model +
Harness`). More rewritable surface means more capability the developers did not predict, and more
ways to break compatibility or weaken a permission boundary.

**The agent and the verifier must stay apart, for now.** "If it can edit evaluation, it can jailbreak
itself. Reward hacking is the default behavior of a system asked to raise a number." Humans still set
the objective and hide the real score.

**Taste lives outside the loop.** "Agents will raise any number you give them. Recursive
self-improvement without taste is a faster way to optimize the wrong thing."

## Why it matters

This supplies the vault's sharpest operational test for a term that is usually used loosely. The
taxonomy is falsifiable — you can look at any system and ask which of the three layers persisted —
and it explains why the impressive results above are all *bounded*: in every one of them the fitness
function sits outside the editable region.

The archive-based search point is a useful counter to greedy optimization: in Schmid's illustration a
generation-1 variant scoring 58 (worse than its 62-scoring parent) is the one that parents the best
later agent at 84. Greedy selection would have pruned it. This is the same diversity-collapse concern
[[Lilian Weng - Harness Engineering for Self-Improvement]] lists among its open challenges.

## Tensions / open questions

- Schmid's definition requires improving *the ability to improve*, but he offers no measurement for
  it beyond "did the next round face a harder honest bar." The RSI Benchmark he cites is a proposal,
  not a result.
- If a system could strengthen its own verifier without capturing it, how would we verify *that*
  claim without an outer verifier — and does the regress terminate?
- Plugin-kernel harnesses (Pi, DeepSeek) maximize the rewritable surface at exactly the moment the
  argument says the verifier must stay unreachable. The two trends point in opposite directions.
- PAST-Bench's negative memory result sits awkwardly against the vault's file-system-as-memory
  enthusiasm; it is not clear whether the failure is in memory as a mechanism or in retrieval policy.

## Affected pages

- [[Recursive Self-Improvement]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Agent Plugin Architecture]]
- [[Philipp Schmid]]

## Related pages

- [[Agent Memory]]
- [[Agent Skill]]
- [[Loop Engineering]]
- [[Reward Design for RL]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]

## Citations

- Raw capture: [[2026-08-28 Philipp Schmid - Recursive Self-Improvement]]
- Original: <https://www.philschmid.de/recursive-self-improvement> (published 2026-08-21)
