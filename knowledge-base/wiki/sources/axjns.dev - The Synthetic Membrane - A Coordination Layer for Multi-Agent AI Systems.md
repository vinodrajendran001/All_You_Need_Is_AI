---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-axjns-synthetic-membrane-paper
source_title: "The Synthetic Membrane: A Coordination Layer for Multi-Agent AI Systems"
source_author: Alex Jones
source_url: https://axjns.dev/research/0001-synthetic-membrane-coordination-layer
tags:
  - source/summary
  - multi-agent
  - coordination
  - agent-governance
source_ids:
  - src-2026-11-04-axjns-synthetic-membrane-paper
status: active
---

# The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems

## Summary

This is a position paper, v2.2, that develops the proposal introduced in
[[axjns.dev - Agents Need Somewhere to Share Their Work]]. It argues that multi-agent systems need
more than delegation. When work spans several agents, sessions or authority boundaries, the system
must keep a reliable account of four things:

- what has been observed;
- what remains disputed;
- who owns the next action;
- who may authorise it.

It proposes a **synthetic membrane**: a policy-controlled shared workspace with five functional
layers and one cross-cutting defence responsibility. The paper names the blackboard as the closest
precedent. Its claimed contribution is narrow: one explicit contract that connects evidence, access
decisions and action ownership across runtimes, plus a plan for testing that contract.

The hypothesis is bounded to a specific workload class. The paper claims no production case study
and no end-to-end validation. Its most durable material is a set of boundary statements: what
convergence, quorum, leases, hashes and revocation can and cannot guarantee.

## Key claims

### A bounded hypothesis, with the evidence placed honestly

- The hypothesis is that for tasks with "distributed evidence, changing membership, and constrained
  authority", a persistent workspace with selective delivery and explicit ownership "can improve task
  completion and recovery at a comparable total resource budget".
- On that framing, a single agent with tools is "the first baseline, not a stage to be outgrown
  automatically".
- Each cited study is placed as motivation, not as validation of the membrane:
  - **MAST** (Cemri et al.) analyses **more than 1,600** annotated traces across **seven**
    frameworks. Its failure categories are system design, inter-agent misalignment and task
    verification. The paper says it does not show that a missing workspace causes every failure.
  - **Superminds Test** probes a platform hosting **more than two million** agents. The paper notes
    it is "not a controlled comparison of coordination architectures".
  - **Salemi et al.** report **13–57%** relative improvements in end-to-end success over their
    strongest baselines on **three** data-discovery benchmarks. That blackboard design retains a
    central agent, so it does not reject central coordination.
  - **Han and Zhang** report competitive performance with lower token use on their evaluated tasks.
  - **Bai et al.** report substantial token overhead and variation in agentic coding. The paper says
    that measures coding workloads, not inter-agent communication alone.

### Protocols are building blocks, not the contract

- MCP "includ[es] negotiated subscription capabilities". Describing MCP servers as "necessarily
  passive or incapable of exposing shared state would misstate the protocol".
- A2A carries discovery, tasks, messages, artefacts and lifecycle state. LangGraph provides persisted
  graph state, checkpoints and replay, and is "a credible implementation substrate and comparison
  baseline".
- The distinction drawn is between "a transport or runtime and an application-level coordination
  contract". The paper adds: "No claim is made that existing tools are incapable of it." Terrarium
  already revisits blackboards for safety and security research.

### Five contract requirements

1. **Addressable evidence.** Each observation carries an ID, source, scope and observation time.
   Interpretations refer to evidence; they do not silently replace it.
2. **Enforced access.** Identity and policy are checked on writes, reads and notifications.
   "Model-generated trust scores cannot grant permissions."
3. **Explicit ownership.** Each actionable task has an owner, a lease or expiry rule, and a
   separately recorded authorisation decision.
4. **Recoverable state.** A replacement agent receives an authorised snapshot plus later changes. It
   does not replay the whole conversation.
5. **Inspectable decisions.** Outputs link to the evidence versions and policy decisions used.
   Conflicting claims stay visible until resolved.

### Six responsibilities and the boundary each must hold

| Layer | Boundary it must preserve |
| --- | --- |
| Governance (L−1) | Agreement among agents does not grant authority |
| Discovery (L0) | A capability claim is not proof of competence or permission |
| Permeability (L1) | Relevance ranking cannot bypass access control |
| Shared medium (L2) | Convergent records need not contain true conclusions |
| Coordination (L3) | Concurrent workers cannot acquire the same exclusive authority |
| Defence (cross-cutting) | Suspect claims and their derivatives stay distinguishable |

### Consistency and effects

- The starting point is a durable event history with materialised views. Corrections append
  superseding or retracting records.
- CRDTs suit mergeable data. They "do not resolve contradictory diagnoses or enforce arbitrary
  cross-record invariants".
- Exclusive ownership needs stronger coordination; a first implementation can use transactional
  updates with version checks and lease fencing within an incident partition. The system should
  "fail closed for actions" when it cannot confirm authority.
- "A lease alone cannot prevent an expired worker from acting". The executor must reject stale
  fencing tokens.
- An idempotency key prevents duplicates only "if the downstream system honours it". Otherwise
  recovery must reconcile external state before retrying.
- A halt recorded in shared memory is insufficient if workers continue to use cached authority. The
  suspension must be enforced at execution.
- Several things are explicitly not proof:
  - Quorum is not proof of correctness, because agents may share models, prompts and evidence.
  - Repeated summaries of one source are "dependent reports, not independent corroboration".
  - Content hashes do not establish truth or authorship.
- Retrieved text stays untrusted. "Revocation cannot erase information already delivered". Sensitive
  work may require terminating affected sessions.

### Worked example and evaluation plan

- The worked example is a hypothetical ransomware incident opened at **02:17 UTC**. It exposes the
  decision boundary between containment and evidence preservation. An expired lease rejects a
  restarted agent's old request. The communications agent receives only a restricted summary. The
  paper concedes that a conventional incident database plus workflow engine could do the same.
- The evaluation plan compares **four** configurations under matched models, tools and budgets:
  - a single agent with tools;
  - an orchestrator with persistent state;
  - a blackboard with comparable controls;
  - the membrane.
- The plan also specifies:
  - paired, preregistered trials;
  - ablations of persistence, selective delivery and ownership;
  - fault injection: stale evidence, a poisoned claim, a failed notification, and a crash between
    approval and execution.
- The paper states in advance what would count against the hypothesis. If a controlled blackboard
  matches it with lower overhead, "the separate abstraction has not earned its place".

## Why it matters

- [[Multi-Agent Coordination]] gets the vault's most explicit coordination contract and a falsifiable
  evaluation design.
- [[Harness State Authority]] gets an event-history-plus-views model of authoritative state for
  several agents.
- [[LLM Application Resilience]] and [[Agent Delegation]] get the lease, fencing and idempotency
  boundaries stated precisely.
- [[Agent Security and Governance]] gets the rules that trust scores cannot grant permissions and
  that revocation cannot recall delivered information.
- [[Model Context Protocol]] gets a correction to a common misreading of MCP as passive.
- [[Agent Frameworks]] gets the transport/runtime versus coordination-contract split.
- [[Persistent Wiki]] gets the rule that repeated summaries are dependent reports.

## Tensions / open questions

- The paper is first-party and unvalidated, and says so. Every proposed mechanism awaits the
  four-way comparison.
- The paper says model-generated trust cannot grant permissions. The companion blog demo gates reads
  on trust scores, which that post labels "simplified rules".
- Human incident doctrine (Google SRE, ICS) is used as an analogy with stated limits. A human
  span-of-control ratio "is not a measured optimum for LLM teams".
- Several practical limits remain unresolved:
  - partitions force a trade-off between availability and exclusive authority;
  - a central service can become a bottleneck;
  - persisted mistakes can outlive their author.

## Affected pages

- [[Multi-Agent Coordination]]
- [[Harness State Authority]]
- [[LLM Application Resilience]]
- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Model Context Protocol]]
- [[Agent Frameworks]]
- [[Persistent Wiki]]
- [[Agent Memory]]

## Raw capture

- [[knowledge-base/raw/sources/The Synthetic Membrane A Coordination Layer for Multi-Agent AI Systems]]

## Citations

- Canonical URL: https://axjns.dev/research/0001-synthetic-membrane-coordination-layer
- Byline in the captured body: "Alex Jones · July 2026 · Revised September 2026 · v2.2". The
  capture's frontmatter author and published fields are empty. The site is axjns.dev.
- Captured: 2026-11-04.

## Related pages

- [[axjns.dev - Agents Need Somewhere to Share Their Work]]
- [[axjns.dev - The Sticky-Note Problem]]
- [[axjns.dev - The Agent Environment Should Be a Lease]]
- [[axjns.dev - Testing Celln's Boundary]]
- [[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]]
- [[Multi-Agent Coordination]]
- [[Harness State Authority]]
- [[LLM Application Resilience]]
- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Model Context Protocol]]
- [[Agent Frameworks]]
- [[Persistent Wiki]]
- [[Agent Memory]]
- [[Celln]]
