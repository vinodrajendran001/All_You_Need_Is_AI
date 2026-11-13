---
type: concept
created: 2026-11-13
updated: 2026-11-13
tags:
  - concept
  - mathematics
  - automated-research
  - formal-verification
source_ids:
  - src-2026-11-06-psi-aaronson-ambainis-proof
  - src-2026-11-09-tillman-two-kinds-test-time-scaling
  - src-2026-11-08-alex-wang-reasoning-pathfinding
  - src-2026-10-19-naam-million-agents-superintelligence
  - src-2026-10-01-mollick-dot-swarm
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
  - src-2026-07-23-latent-space-eiso-kant-poolside-model-factory
status: active
---

# AI for Mathematical Discovery

## Definition

The use of AI systems to produce new mathematical results. These systems include single models,
agent teams, and automated search loops. The results include proofs of open conjectures, better
algorithms, and new constructions. This differs from solving benchmark or competition problems whose
answers are already known. The question that organizes this page is: **what checked the result, and
who is responsible for it?**

## Why it matters

Mathematics is where claims of AI research ability can be checked most directly. A proof can be
machine-checked, and an algorithm's operation count can be counted. That makes it an early signal
for [[Automated AI Research]] and [[Recursive Self-Improvement]] arguments. But the vault's records
of AI mathematics range from machine-checked proofs to self-reports with no recorded check. They
should not be read as one trend.

## Current synthesis

### A ladder of verification

The vault's cases, ordered roughly by how strongly the result has been checked:

| Case | Who did the work | What checked it | Caveat |
| --- | --- | --- | --- |
| Aaronson-Ambainis conjecture, open since 2008 ([[PSI Research - A Proof of the Aaronson-Ambainis Conjecture]]) | PSI's internal research system, using a non-public Anthropic model. A human scoped, ran, and reviewed the work. | Lean accepted the proof, and later an improved version. An advisor audited the proof. Stanford researchers are reading it. | First-party; no peer review recorded; the Lean statement and code are not shown |
| 48-multiplication algorithm for 4x4 complex matrices ([[Philipp Schmid - Recursive Self-Improvement]]) | AlphaEvolve's automated search | The result is a concrete algorithm, one multiplication fewer than Strassen's **49** | Reported through a survey |
| Formal-math benchmarks ([[Ramez Naam - Can a Million AI Agents Create Superintelligence]]) | Agent teams on predeclared theorem statements | Scored tasks: Opus 5.5 on **49** weighted statements; a Lean speed exponent | Measures scaling, not discovery |
| Navier-Stokes ([[Ramez Naam - Can a Million AI Agents Create Superintelligence]], [[Ethan Mollick - The Dot and the Swarm]]) | OpenAI, about **10,000** agents over **88** hours; Mollick describes roughly **2.7 million** messages | Mollick explicitly says it is **not formally accepted** | No single-agent control; Noam Brown attributes "not even 10%" to multi-agent scaling |
| Erdős 397 ([[Latent Space - Inside the Model Factory - Eiso Kant, Poolside AI]]) | Poolside's Laguna S, per Eiso Kant | None recorded | Launch-day self-report |

The table records what each source says, not whether the result is correct.

### What a proof checker settles, and what it leaves open

[[Alex Wang - What Objective Is Reasoning Solving]] argues that RL with an answer-only verifier
rewards the final answer and does not require the intermediate reasoning to be true. A proof
assistant changes this. In PSI's description, Lean is "a proof assistant in which a computer checks
every step". *This is the vault's synthesis, not a claim made by either source:* a machine-checked
proof removes the faithfulness gap for the argument itself.

It moves trust to two other places:

- **The formal statement.** Whether the Lean statement says what mathematicians mean by the
  conjecture. PSI's capture does not show the statement, and an advisor's comments on the
  formalization are mentioned but not described.
- **Expert understanding.** The Stanford group that settled a special case in August 2026 is writing
  a shorter exposition for experts. The capture records no completed community acceptance.

[[Reward Design for RL]] already notes that math rewards are checked either by matching a boxed
answer or by a Lean proof. The difference matters more for discovery than for training.

### Why mathematics may lead

[[James Tillman - Two Kinds of Test-Time Scaling]] argues that spending compute beyond what a model
used in training should pay off most easily "in domains where incremental progress is easy to
recognize", such as math or cyber. His cleanest evidence is a competition-math result (AIME25). This
agrees with the "Verifier's law" framing recorded in [[Automated AI Research]]: automation advances
fastest where outcomes can be checked. PSI's run fits the long-run pattern. The proof came during
the third day, and the system went on to improve the result twice. However, PSI reports no compute
figures, so it cannot be used to measure Tillman's ceiling or slope (see [[Test-Time Scaling]]).

### Division of labor

The clearest case keeps humans at both ends of the work.

- **Before the run.** PSI's David Turturean built the system, scoped the problem, and ran it.
- **After the run.** He prompted the model to draft the paper, reviewed it, and "is responsible for
  the paper's correctness". Two advisors audited the proof and commented on the formalization.

This matches the execution-versus-taste split in [[Automated AI Research]]: the system searched, and
a human chose the problem. The Navier-Stokes record cuts the other way for agent count. Brown's
attribution, and the absence of a single-agent control, mean the vault has no evidence that the
number of agents was what mattered (see [[Multi-Agent Coordination]]).

## Open questions

- How much of the PSI result came from the model, how much from the system design, and how much from
  human scoping? The capture does not say. It names neither the model nor the number of earlier
  attempts.
- When will a result in this vault be accepted through the normal mathematical process, such as an
  expert exposition, a replication, or a publication? Every case here is either first-party or
  relayed.
- Do mathematical results feed back into AI R&D? AlphaEvolve also sped up a Gemini training kernel
  (see [[Automated AI Research]]), but the vault has no comparable case for proofs.
- Tillman asks what the first sign would be that test-time scaling beyond training budgets reaches
  research taste. Mathematics, where problem choice is still human, is one place to look.

## Related pages

- [[PSI Research - A Proof of the Aaronson-Ambainis Conjecture]]
- [[James Tillman - Two Kinds of Test-Time Scaling]]
- [[Alex Wang - What Objective Is Reasoning Solving]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[Ethan Mollick - The Dot and the Swarm]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Latent Space - Inside the Model Factory - Eiso Kant, Poolside AI]]
- [[Automated AI Research]]
- [[Recursive Self-Improvement]]
- [[Test-Time Scaling]]
- [[Reward Design for RL]]
- [[LLM Reasoning]]
- [[Multi-Agent Coordination]]
- [[Anthropic]]
- [[Ethan Mollick]]
- [[Google DeepMind]]
