---
type: concept
created: 2026-09-25
updated: 2026-10-23
tags:
  - concept
  - coding-agents
  - software-engineering
  - testing
source_ids:
  - src-2026-09-09-mistral-legacy-code-modernization
  - src-2026-10-05-faik-ai-native-software-factory
  - src-2026-10-14-maevyn-decoherence-trap
status: active
---

# Legacy Code Modernization with AI Agents

## Definition

AI-assisted legacy modernization combines behavioral characterization, documentation, dependency
decomposition, code translation, and review. Its central invariant is parity with the runnable legacy
system, not syntactic similarity between old and new code.

## Why it matters

Legacy scientific and industrial systems often encode domain behavior that has outlived their authors,
tests, and documentation. Agents can accelerate exploration and migration only after that behavior is
made observable enough to verify.

## Current synthesis

[[Mistral - Modernizing Complex Legacy Code with AI Agents]] begins with a parity harness: instrument
the Fortran system to export intermediate state, load those checkpoints in C++, and compare numerical
behavior before refactoring architecture. That converts the old executable into an oracle while
avoiding an assumption that translated code is correct because it compiles.

The next stage maps the caller-callee tree and documents manageable subtrees. More than 100 agents
reportedly helped document the case-study codebase, while migration units stayed below roughly 10,000
Fortran lines. Planner, coder, tester, and reviewer roles then operated inside bounded units with human
approval gates.

The source's qualitative comparison argues against maximum autonomy: unconstrained agents lose
system-level constraints, while structured workflows preserve a single migration contract. This is
one vendor case study, not a measured claim that a particular agent count or module size generalizes.

## Deterministic migration belongs in the comparison

[[Adam Faik - How to Build an AI-Native Software Factory]] supplies a counterweight to the
agent-centered Fortran case. In the reported Uber JUnit migration, generative AI was tried
unsuccessfully; deterministic Shepherd automation then produced **5,000+ diffs** and migrated
**75,000+ test classes in four months**, with AI assisting failures.

The lesson is not that deterministic tools always beat agents. A regular, checkable transformation
and an undocumented scientific-code translation are different tasks. It is that the migration
contract should choose the tool: automate known transformations directly, use agents where
interpretation or repair is needed, and retain parity checks in either case. Faik's figures are
secondary company reporting, not a controlled comparison with Mistral's workflow.

## Incremental migration is itself a debt-producing mechanism

[[The Decoherence Trap]] is an **unattributed essay** — no author appears anywhere in the capture, which is
published at maevyn.codes — and it argues rather than measures. Its contribution here is a name for the cost
this page's own method incurs.

The essay separates three kinds of debt: **infrastructure debt** (wear), **technical-advancement debt** (the
need to upgrade), and **decoherence** — the extra complexity created by **partial, inconsistent transitions**,
where locally valid but mutually incompatible models coexist and every later change has to translate between
them. Its motivating analogy is replacing a building's pipes floor by floor, leaving custom joints and
undocumented interactions. That is a description of staged migration, which is what this page recommends.

**This qualifies the page's existing framing rather than contradicting it.** The sections above treat bounded
migration units and dependency decomposition as risk controls, which they are. The essay points out they are
also the mechanism that produces a mixed-paradigm system: migrating below roughly 10,000-line Fortran units
means old and new coexist for the duration, and the cost of being in that state is not captured by a parity
harness, which asks only whether behaviour matched — not whether the system got harder to change. Read this
way, **parity is a correctness control and decoherence is a separate, unmeasured cost of the same plan**, and
the deterministic Shepherd case is the one that minimises it: a regular, mechanical transformation applied
uniformly leaves no patchwork behind, which is an argument for deterministic migration this page did not
previously have.

The essay also warns against the obvious over-correction. Its simulation suggests a **sweet spot** — too little
coherence work collapses throughput and too much also slows delivery — so the target is a moderate, actively
maintained level with some adaptive "jitter", not maximum uniformity. The simulation is **not evidence**: the
author states that **"The simulation has arbitrary weights and does not definitively prove that this is how
complex systems will evolve."**

The cited third-party research is the more usable part, and all of it concerns agent-assisted development in
general rather than modernization specifically:

| Study, as cited | Scope | Reported result |
| --- | --- | --- |
| Chen and Stratton, Harvard working paper | 718 companies | coding agents increased code written by **30%** with no measurable increase in finished work; pull requests took **49% longer** to review and **nearly twice as many** were returned for changes |
| He et al., Carnegie Mellon | open-source projects adopting Cursor | a large initial velocity increase that **did not last**, with rising code complexity contributing to the later slowdown. **No effect size is quoted** |
| Liu et al. | over **300,000** AI-authored commits across more than **6,000** repositories | approximately **one in eleven** commits — up to **one in seven** depending on assistant — introduced at least one quality issue; **nearly a quarter** of those issues remained in the code |

Two of those bear directly on the agent-count question. The Mistral case reports that more than 100 agents
helped document the codebase; the Harvard figures suggest that **code volume and review burden can rise
together without finished work rising**, which is the same failure the essay predicts when parallel capacity
is added to a system whose complexity is growing. None of these studies examined a migration, none is a
controlled experiment on this page's workload, and the essay itself treats them as suggestive.

The essay's larger claim — that systems could pass a point where humans cannot repair them and agents cannot
recohere them, which it calls **Decoherence Collapse** and estimates would take **"years or even decades"** to
reverse — is a qualitative forecast with no instance behind it. Its value to this page is the vocabulary and
the warning, not a prediction to plan against. See [[Recursive Self-Improvement]], where the same essay's
bubble-optimisation argument is recorded, and [[AI-Native Software Development Lifecycle]].

## Open questions

- How should parity tolerances account for floating-point and algorithmic differences?
- Which dependency cuts minimize cross-module behavioral ambiguity?
- How should teams measure migration effort and defects against non-agent baselines?
- **What would a decoherence measurement look like on a migration?** The essay supplies no fitted growth rate
  for complexity in real codebases and does not demonstrate that decoherence grows exponentially anywhere. A
  parity harness answers correctness; this page has no instrument for the mixed-paradigm cost it incurs.
- **How long may a system stay half-migrated?** Nothing in the vault's sources sizes the window in which old
  and new paradigms coexist, or what the per-change tax is while it lasts.
- **Do the cited coding-agent studies apply here at all?** They measured general adoption across companies and
  repositories, not a bounded migration with a parity oracle and human approval gates. The essay does not
  establish that AI-generated code is the sole or dominant cause of the complexity it describes, nor that
  agents cannot maintain or repair highly complex systems.
- **Where is the sweet spot for a migration specifically?** The claim that both too little and too much
  coherence work slow delivery comes from a simulation with arbitrary weights; it gives no operating point.

## Related pages

- [[The Decoherence Trap]]
- [[Recursive Self-Improvement]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
- [[Coding Agent Harness]]
- [[Agentic Testing]]
- [[Agent Planning]]
- [[AI-Native Software Development Lifecycle]]
- [[Mistral - Modernizing Complex Legacy Code with AI Agents]]
