---
type: concept
created: 2026-08-30
updated: 2026-08-30
tags:
  - concept
  - agents
  - multi-agent
  - governance
source_ids:
  - src-2026-08-28-google-cloud-agent-delegation
status: active
---

# Agent Delegation

## Definition

Agent delegation is the act of one agent handing a sub-task, with some scope of authority and data
access, to another agent or model. It is distinct from orchestration: orchestration is about *how*
work is routed and merged, delegation is about *what authority and intent travel with the work* — and
what is lost in the handoff.

## Why it matters

Multi-agent systems are usually designed for throughput. Delegation asks the accountability question
instead: as a request passes down a chain, who is still checking that the work being done is the work
that was wanted?

## Current synthesis

### The zone of indifference

[[Nenad Tomasev and Reshu Yadav - How Agents Can Delegate Better]], distilling Google DeepMind's
*Intelligent AI Delegation* (arXiv 2602.11865), borrows Chester Barnard's 1938 concept and applies it
to agents. An agent **complies with any instruction that does not trigger a hard violation** — it sits
inside a zone where it simply does not push back.

The consequence is cumulative. As delegation chains lengthen, small intent mismatches propagate
unchallenged, and each agent becomes **"an unthinking router rather than a responsible actor."** No
single agent does anything wrong; the chain still drifts arbitrarily far from the original intent.

The proposed remedy is **dynamic cognitive friction** — deliberately inserting points where an agent
must stop and check intent rather than forward the request. The idea is named but not specified.

### Contract-first decomposition gives a stopping criterion

Decompose a task only as far as each sub-task can be stated as a **verifiable contract**. If a
sub-task's completion cannot be checked, the decomposition has gone too far: the delegator has given
away work it cannot evaluate.

This is a genuinely useful rule because [[Agent Planning]] otherwise leaves decomposition depth to
judgement. It is also demanding — many real sub-tasks (summarize this, judge whether the tone is
right) have no cheap contract, which would forbid delegating exactly the work agents are most often
used for.

### Cost-aware routing follows from verifiability

Match sub-tasks to model tiers by difficulty rather than sending everything to the strongest model.
The contract principle supplies the safety margin: where output is cheaply verifiable, a weaker and
cheaper model is a bounded risk. See [[Model Routing]].

### Least privilege, enforced rather than asserted

A sub-agent should receive the minimum data needed. The concrete proposal is **zero-knowledge
proofs**, letting a sub-agent prove it computed a result correctly *without revealing the underlying
data*. This is the first cryptographic enforcement mechanism in this vault's
[[Agent Security and Governance]] material, which otherwise treats least privilege as policy — a
statement of intent rather than a guarantee.

### How this relates to the harness view

Delegation is where the harness stops being a single-agent concern. The evaluator-outside-the-loop
principle in [[Harness Optimization]] and the contract-first principle here are the same idea at
different scales: work you cannot verify should not be work you hand off, whether the recipient is a
sub-agent or a future version of yourself.

## Open questions

- Zero-knowledge proofs for arbitrary LLM computation are a research direction, not a shipping
  capability. What class of sub-agent work is actually provable today?
- "Dynamic cognitive friction" needs specification: which checkpoints, triggered by what conditions,
  at what latency and token cost?
- The zone-of-indifference argument predicts degradation with chain length, but no measurement of the
  effect is offered. How fast does intent drift, and is it detectable from outputs alone?
- If contract-first decomposition forbids delegating unverifiable work, what is the right practice for
  the large class of tasks that are only partly checkable?
- Does raising an agent's willingness to push back trade against its usefulness, and where is that
  frontier?

## Related pages

- [[AI Agents in Production]]
- [[Agent Planning]]
- [[Agent Security and Governance]]
- [[Model Routing]]
- [[Agent Frameworks]]
- [[Agentic Loop]]
- [[Harness Optimization]]
- [[Google DeepMind]]
- [[Nenad Tomasev and Reshu Yadav - How Agents Can Delegate Better]]
