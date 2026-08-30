---
type: source-summary
created: 2026-08-30
updated: 2026-08-30
source_id: src-2026-08-28-google-cloud-agent-delegation
source_title: "How agents can delegate better"
source_author: "Nenad Tomasev and Reshu Yadav (Google Cloud / Google DeepMind)"
source_url: "https://cloud.google.com/blog/products/ai-machine-learning/how-agents-can-delegate-better"
tags:
  - source/summary
  - topic/agents
  - topic/multi-agent
  - topic/governance
source_ids:
  - src-2026-08-28-google-cloud-agent-delegation
status: active
---

# Nenad Tomasev and Reshu Yadav - How Agents Can Delegate Better

## Summary

A distillation of Google DeepMind's *Intelligent AI Delegation* paper (arXiv 2602.11865) into four
design principles for multi-agent systems. The framing treats delegation as a first-class engineering
problem rather than an emergent property of putting agents in a loop, and borrows from organizational
theory to name the failure mode that makes long delegation chains dangerous.

## Key claims

**Contract-first decomposition.** Decompose a task only as far as each sub-task can be stated as a
verifiable contract. If a sub-task's completion cannot be checked, the decomposition has gone too far
— the delegator has given away work it cannot evaluate.

**Cost-aware routing.** Match sub-tasks to model tiers by difficulty. Routing everything to the
strongest model is both expensive and, per the contract principle, unnecessary for sub-tasks whose
outputs are cheaply verifiable.

**Least-privilege data sharing, enforced cryptographically.** A sub-agent should receive the minimum
data needed. The post's most concrete proposal is **zero-knowledge proofs**, which let a sub-agent
prove it computed a result correctly *without revealing the underlying data* to the delegator or to
itself beyond what the task requires.

**The zone of indifference is the core risk.** Borrowing Chester Barnard's 1938 concept, the authors
observe that an agent will comply with any instruction that does not trigger a hard violation — it
sits inside a zone where the agent simply does not push back. As delegation chains lengthen, small
intent mismatches propagate unchallenged, and each agent becomes **"an unthinking router rather than
a responsible actor."** The proposed remedy is **dynamic cognitive friction**: deliberately inserting
points where an agent must stop and check intent rather than forward the request.

## Why it matters

Most multi-agent material in this vault is about orchestration mechanics — how to route, how to pass
state, how to merge results. This source is about *what gets lost* in the passing, and the zone of
indifference names it precisely: compliance is not agreement, and a chain of compliant agents can
drift arbitrarily far from the original intent without any single agent doing anything wrong.

The contract-first rule is also a useful decomposition stopping criterion, which
[[Agent Planning]] otherwise leaves to judgement: stop subdividing when you can no longer verify.

Zero-knowledge proofs for sub-agent computation is the first concrete cryptographic proposal in the
vault's [[Agent Security and Governance]] material, and it addresses a real gap — least privilege is
usually asserted as policy, not enforced.

## Tensions / open questions

- Zero-knowledge proofs for arbitrary LLM computation are a research direction, not a shipping
  capability. The post does not say what class of sub-agent work is actually provable today.
- "Dynamic cognitive friction" is named but not specified. Which checkpoints, triggered by what, at
  what latency and token cost?
- Contract-first decomposition assumes verifiability is available at the right granularity. Many
  real sub-tasks (summarize this, judge tone) have no cheap contract, which would forbid delegating
  exactly the work agents are most often used for.
- The zone-of-indifference argument predicts degradation with chain length but no measurement of the
  effect is offered.

## Affected pages

- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Agent Planning]]
- [[Model Routing]]
- [[Google DeepMind]]

## Related pages

- [[AI Agents in Production]]
- [[Agent Frameworks]]
- [[Agentic Loop]]
- [[Reasoning Trace Privacy]]
- [[Multi-Turn Evaluation]]

## Citations

- Raw capture: [[2026-08-28 Nenad Tomasev - How agents can delegate better]]
- Original: <https://cloud.google.com/blog/products/ai-machine-learning/how-agents-can-delegate-better> (published 2026-08-21)
- Underlying paper: *Intelligent AI Delegation*, arXiv 2602.11865
