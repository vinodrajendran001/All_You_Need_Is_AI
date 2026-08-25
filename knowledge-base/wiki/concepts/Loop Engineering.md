---
type: concept
created: 2026-08-05
updated: 2026-08-24
tags:
  - concept
  - ai-agents
  - orchestration
  - evaluation
source_ids:
  - src-2026-08-05-aibuilderclub-loop-engineering-guide-2026
  - src-2026-08-05-aibuilderclub-loop-engineering-anthropic-playbook
  - src-2026-08-05-aibuilderclub-loop-engineering-karpathy
  - src-2026-08-05-aibuilderclub-loops-md-karpathy
  - src-2026-08-05-aibuilderclub-types-of-agentic-loops
  - src-2026-08-05-aibuilderclub-loop-engineering-addy-osmani
  - src-2026-08-05-aibuilderclub-self-improving-agent-loops
  - src-2026-08-05-aibuilderclub-loop-engineering-case-study
  - src-2026-08-12-yoko-li-loop-convergence
  - src-2026-08-20-liquid-ai-production-loops
status: active
---

# Loop Engineering

Loop engineering is the design of a repeated agent cycle around an objective: what triggers it, what state it reads and writes, how it plans and acts, what verifies progress, when it retries or escalates, and what stops it. It extends the basic [[Agentic Loop]] from control flow into an operating discipline for unattended or repeatedly invoked work.

## The verifier is the scarce component

Generating another candidate is usually cheap. Determining whether that candidate improved the world is harder. A useful loop therefore needs an operational verifier rather than a request to "review your own work":

- deterministic checks such as tests, schemas, type checks, or policy rules;
- behavioral checks that operate the artifact through its real interface;
- external signals such as conversion, incident, or quality metrics;
- rubric-based model judges where deterministic truth is unavailable;
- human review for ambiguous or high-impact decisions.

Generation and evaluation should be separated when possible. A fresh evaluator still has blind spots, but it avoids inheriting the producer's full reasoning path and assumptions.

## Loop contract

A durable loop makes six things explicit:

1. **Objective** — the state to improve, not merely an activity to perform.
2. **Trigger** — turn, goal, schedule, event, or external signal.
3. **State and artifacts** — inspectable files, records, or checkpoints shared across iterations.
4. **Actions** — bounded tools and permissions available to the worker.
5. **Verifier** — evidence that distinguishes progress from plausible output.
6. **Exit and escalation** — success, budget exhaustion, repeated failure, or human handoff.

Open loops permit exploration under budgets and quality floors. Closed loops converge toward explicit pass criteria. Self-improving loops add another risk: the system can modify prompts, skills, or harness rules, so proposed changes need held-out regressions and rollback rather than self-approval.

## Terminology and prior art

"Loop engineering" is useful vocabulary, but much of the machinery predates the label: control loops, CI, workflow engines, retry policies, state machines, and optimization systems already encode objectives, feedback, state, and stop conditions. The durable contribution is the emphasis on verification as the autonomy bottleneck, not a claim that repeated workflows were invented in 2026.

## Convergence and stopping economics

[[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]] sharpens the loop contract into four convergence conditions: a target state, observable current state, precise local actions, and an external stopping rule. Editability and verifiability are properties of the task representation, so reframing an opaque output as structured code, SVG paths, or a scene graph can move a task into a regime where repair is possible.

Completion is also economic. Loops need impossibility detection, diminishing-return limits, cost per iteration, and progress per dollar. Otherwise a verifier can repeatedly reject a correct ceiling diagnosis while the growing transcript makes every unproductive iteration more expensive.

## Production-scale execution as specification discovery

[[Liquid AI - Designing Loops for Production-Grade Work]] shows why an executable target is part of the specification. Coding agents building a tokenizer trainer cleared obvious functional tests but encountered encoding, memory, parallelism, tokenization, ordering, and duplicate-input failures only against real datasets and external reference implementations.

The resulting pattern is:

- specify interfaces and invariants without prescribing the implementation;
- run against representative production-scale inputs;
- keep the acceptance harness outside the agent's write boundary;
- feed exact failures back into bounded iterations;
- stop only on externally measured behavior.

The case study does not prove universal autonomy, but it demonstrates that iteration can convert production failures into missing requirements that a one-shot prompt never contained.

## Open questions

- How should loops verify strategic or long-horizon work when feedback arrives late?
- How can teams detect proxy optimization when the measured verifier diverges from the real objective?
- What evidence should be required before a loop earns more permissions, budget, or runtime?

## Related pages

- [[Agentic Loop]]
- [[Graph Engineering]]
- [[Multi-Turn Evaluation]]
- [[Coding Agent Harness]]
- [[Agent Planning]]
- [[Agent Skill]]
- [[Agent Security and Governance]]
- [[AI Builder Club - Build AI Agents]]
- [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- [[Test-Time Scaling]]
- [[Liquid AI - Designing Loops for Production-Grade Work]]
