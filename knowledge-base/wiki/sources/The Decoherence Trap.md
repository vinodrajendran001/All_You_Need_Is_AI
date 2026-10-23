---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-14-maevyn-decoherence-trap
source_title: "The Decoherence Trap: When AI slop drowns out the signal in an endless sea of noise"
source_author: Unattributed in capture (published at maevyn.codes)
source_url: https://maevyn.codes/decoherence
tags:
  - source/summary
  - technical-debt
  - coding-agents
  - recursive-self-improvement
source_ids:
  - src-2026-10-14-maevyn-decoherence-trap
status: active
---

# The Decoherence Trap

## Summary

A long essay proposing **decoherence** as a distinct category of technical debt: the accumulation of
**locally valid but mutually incompatible or redundant models** in a system that keeps changing. The
cost is not wear and not the need to upgrade, but the combinatorial burden of translating between
coexisting paradigms and preventing side effects across them.

The AI argument follows: if each rushed change increases future complexity, more agents cannot
indefinitely compensate. The essay's second half extends the same logic to recursive self-improvement —
an AI optimizing in a data-center bubble can improve local metrics without knowing whether its changes
remain globally coherent or useful.

**"Decoherence is, by far, the worst form of tech debt."**

## Key claims

### The concept

- Three kinds of debt are separated: **infrastructure debt** (wear), **technical-advancement debt** (the
  need to upgrade), and **decoherence** (extra complexity created by partial, inconsistent transitions).
  The motivating analogy is replacing a building's pipes floor by floor, leaving custom joints and
  undocumented interactions.
- With multiple coexisting paradigms, interactions become combinatorial — A→B, A→C, B→C, and longer
  chains — so each later change requires more analysis, and time pressure produces further shortcuts.
  **"The maze grows onward and onward until it swallows you whole."**
- **Recohering** is the deliberate reduction of accumulated incompatibility.

### The simulation

- A graph stands in for a codebase: nodes are components sized by component size, colors are paradigms,
  edges are connections, and actors implement features by walking and mutating regions. A **coherence
  factor** controls how carefully each actor reasons about context, trading speed against the
  probability of reducing complexity.
- **[Illustrative]** Coherence values **-0.2, +0.2, +0.6, +0.8** produced displayed feature counts of
  **152, 247, 417, 376**. The implied **sweet spot** is a moderate, actively maintained level: too
  little coherence collapses throughput, too much coherence work also slows delivery.
- The author's own disclaimer is explicit: **"The simulation has arbitrary weights and does not
  definitively prove that this is how complex systems will evolve."** It is offered only as evidence
  that the curve *can* emerge from simple local rules.

### Cited empirical support — all third-party

- A Harvard working paper (Fiona Chen and James Stratton) on **718 companies**: coding agents increased
  code written by **30%** without a measurable increase in finished work; pull requests took **49%
  longer** to review and **nearly twice as many** were returned for changes.
- A Carnegie Mellon study (He et al.) of open-source projects adopting Cursor: a large initial velocity
  increase that **did not last**, with rising code complexity contributing to the later slowdown. No
  effect size is quoted.
- An analysis (Liu et al.) of **over 300,000 AI-authored commits** across **more than 6,000
  repositories**: approximately **one in eleven** — and up to **one in seven** depending on assistant —
  introduced at least one quality issue, and **nearly a quarter** of those issues remained in the code.

### The recursive-self-improvement argument

- Isolated AI can improve software's speed, size, and efficiency but cannot verify **global coherence or
  usefulness** without contact with reality. The essay ties this to Tom Reed's **Goodhart Singularity**
  and Goodhart's law.
- The mathematics analogy: Boole published Boolean algebra in **1847**; Shannon connected it to relay
  circuits in **1937**. Formal results can be locally valid and globally unimportant until a real
  problem supplies the context. The essay cites a **September** declaration signed by Terence Tao and
  **24 other Fields Medalists** arguing that problem-solving is only a proxy for understanding.
- It quotes, in order to criticize, Tom Davidson's claim that **1,000 people** recording screens and
  wearing cameras could produce **300 years' worth of experience** in **4 months**.
- **Decoherence Collapse** is the end state: systems too complex for humans to repair, with agents unable
  to reverse the accumulated decoherence, locking organizations into a degrading model. The author
  estimates repair could take **"years or even decades"** — a qualitative forecast.

## Why it matters

This essay supplies [[Recursive Self-Improvement]] with a **mechanism-level objection** that differs
from [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]. Naam argues the scaling
exponent is too small; this essay argues the **substrate degrades as you scale on it**. Together they
are the vault's strongest pair of non-capability arguments against fast takeoff — and they disagree
about where the limit lives, which is worth preserving rather than merging.

For [[AI-Native Software Development Lifecycle]] and [[Legacy Code Modernization with AI Agents]], the
decoherence framing explains a pattern the vault has seen repeatedly without a name: agent-assisted
codebases where throughput rises while *finished* work does not. The three cited studies are the most
concrete negative evidence on coding-agent adoption the vault currently holds.

The "sweet spot" claim is also a useful corrective. The essay does not argue for maximum coherence; it
argues that both extremes reduce delivery and that some **jitter** is needed for adaptation.

## Tensions / open questions

- **Authorship is unresolved.** Neither frontmatter nor body states an author; the site is maevyn.codes.
  The capture also contains garbled embedded simulation SVG and UI text.
- The simulation **proves nothing about real systems** — the author says so. No fitted growth rate exists
  for decoherence in production codebases, and the linear-versus-exponential contrast is asserted, not
  measured.
- The cited studies concern specific companies, repositories, assistants, and periods. They do not
  establish universal causal effects, and the essay treats them as suggestive rather than conclusive.
- The essay does **not** show that agents cannot maintain or repair highly complex systems, nor that any
  real system has reached or will reach Decoherence Collapse.
- The claim that isolated recursive self-improvement is rate-limited by reality rests on analogy and
  assumption, not an impossibility result. The Boole/Shannon history shows context *can* matter; it does
  not show AI cannot generate useful concepts in isolation.
- The author's own concessions: humans also create decoherence, especially under pressure; AI has useful
  applications particularly at the margins; experimentation and forking matter in open source; and some
  domains with clear rules and victory conditions **do** support effective isolated optimization.

## Affected pages

- [[Recursive Self-Improvement]]
- [[AI-Native Software Development Lifecycle]]
- [[Legacy Code Modernization with AI Agents]]

## Raw capture

- [[The Decoherence Trap When AI slop drowns out the signal in an endless sea of noise]]

## Citations

- Raw capture: [[The Decoherence Trap When AI slop drowns out the signal in an endless sea of noise]]
- Canonical URL: <https://maevyn.codes/decoherence>
- Published 2026-10-14; captured 2026-10-22. **No author is stated anywhere in the capture.**
- Cites, but this ingest did not read: Chen and Stratton's Harvard working paper; He et al. on Cursor
  and software complexity; Liu et al. on AI-generated code quality; Tom Reed's *Goodhart Singularity*;
  Tom Davidson's data-bottleneck essay; Eth and Davidson's SIE paper; the Fields Medalists'
  declaration; and Shannon's 1937 thesis.

## Related pages

- [[Automated AI Research]]
- [[Coding Agent Harness]]
- [[Agentic Testing]]
- [[Synthetic Data Flywheel]]
- [[Software Performance Engineering]]
- [[Benchmark Optimization]]
- [[Reward Design for RL]]
