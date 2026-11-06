---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-axjns-sticky-note-problem
source_title: The Sticky-Note Problem
source_author: Unattributed in capture
source_url: https://axjns.dev/blog/sticky-note-problem
tags:
  - source/summary
  - multi-agent
  - handoffs
  - incident-response
source_ids:
  - src-2026-11-04-axjns-sticky-note-problem
status: active
---

# The Sticky-Note Problem

## Summary

The post is subtitled "Making Agent Handoffs Reliable". It is the handoff-focused companion to
[[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]]. Its
"sticky-note problem" is that a handoff records only what one participant thought worth passing on
at one moment. A handoff rarely says three things:

- what has changed since;
- which assumptions remain open;
- who now owns the action.

The post grounds this in a hypothetical **2:47 AM** database incident, in which detection, forensics
and containment agents each hold part of the picture. It argues that the missing piece is an
application-level contract defining what a finding, a handoff and an approval mean. Frameworks and
protocols can carry that contract, but they do not define it. The post borrows its record design
from human incident management, and it insists that a plain workflow engine plus database be tested
as the alternative.

## Key claims

### The failure is information that never reaches the decision-maker

- In the scenario, three agents each hold part of the picture:
  - detection flags unusual outbound traffic;
  - forensics finds a scheduled export that could explain it;
  - containment prepares to isolate the server.

  Containment could interrupt a legitimate export, or the team could dismiss a real compromise
  without checking.
- The post labels the scenario hypothetical. It says the scenario "captures a concrete design
  failure: decisions depend on information that exists somewhere in the system and never reaches the
  decision-maker". Adding agents can make the omissions harder to find.

### "Done" is not an authorisation

- A paragraph marked "done" might mean three different things:
  - the investigation is complete;
  - the current subtask is complete;
  - "the agent has run out of useful ideas".

  "A downstream agent should not have to infer which interpretation authorises a production action."
- Several existing tools can carry state:
  - LangGraph persistence and checkpoints;
  - a shared database;
  - a workflow engine;
  - A2A;
  - MCP.

  "The problem is not that these systems only move strings". The application still has to define
  the meaning of the records.

### Research motivates the problem but does not pick the fix

- The MAST study examines **more than 1,600** annotated traces across **seven** frameworks. Model
  capability is therefore only part of the problem.
- The post adds: "A failure taxonomy does not tell us which architecture will fix it. An agent can
  have the right evidence and still reason badly." Better shared state is "a candidate intervention".
- Salemi and colleagues' blackboard still has a central agent posting requests. The post says that
  result does not prove "that every task should use a blackboard, or that central coordination is
  the enemy".

### Records borrowed from incident command

- ICS and Google SRE practice combine shared information with a defined authority structure. They
  use a living incident document, clear roles and deliberate handoffs.
- The post translates this into four records:
  - **evidence** with a source and timestamp;
  - **hypotheses** linked to that evidence;
  - **actions** with an owner and an approval state;
  - a **current incident view** that preserves unresolved disagreement.
- "Human doctrine supplies design questions, not experimentally established constants for LLMs."
  Team size and escalation thresholds must be measured.

### What each missing control breaks

- A board without access controls exposes sensitive evidence.
- A board without ownership "can send two agents to execute the same action".
- A board without retractions keeps circulating a conclusion after its evidence has been withdrawn.
- Three further rules restrain the design:
  - Summaries should keep links to their evidence.
  - "A repeated claim should not become more credible merely because several agents copied it."
  - "Permission to read a recommendation should never imply permission to execute it."

### The simpler alternative stays in the comparison

- The desired behaviour is that a restart preserves the action owner and the unresolved question. A
  new agent should not have to guess from a transcript.
- The post says this "is also behaviour that a well-designed workflow and database could provide".
  The membrane "earns its place only if" reusability improves completion, recovery or operator
  control enough to cover its cost.

## Why it matters

- [[Agent Delegation]] gains a concrete handoff contract: what a delegated result must carry beyond
  "done". It also gets the warning that reading a recommendation is not permission to act on it.
- [[Multi-Agent Coordination]] gains the incident-command framing. Coordination keeps an authority
  structure; it does not dissolve it.

## Tensions / open questions

- The post is a first-party design argument illustrated by a hypothetical scenario. It reports no
  experiment of its own.
- The four record types are a proposal. The post gives no evidence that typed records reduce the
  "done" ambiguity in practice. The paper concedes that typed records "cannot ensure that two models
  interpret evidence correctly".
- The post does not specify how an incident lead is chosen when the lead is itself an agent.

## Affected pages

- [[Agent Delegation]]
- [[Multi-Agent Coordination]]

## Raw capture

- [[knowledge-base/raw/sources/The Sticky-Note Problem]]

## Citations

- Canonical URL: https://axjns.dev/blog/sticky-note-problem
- Site: axjns.dev. The capture names no author and gives no publication date. It links the GitHub
  repositories `sympozium-ai/sympozium` and `AlexsJones/research`, and the v2.2 paper, which credits
  Alex Jones. No byline is assigned here.
- Captured: 2026-11-04.

## Related pages

- [[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]]
- [[axjns.dev - Agents Need Somewhere to Share Their Work]]
- [[axjns.dev - The Agent Environment Should Be a Lease]]
- [[axjns.dev - Testing Celln's Boundary]]
- [[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]]
- [[Agent Delegation]]
- [[Multi-Agent Coordination]]
- [[Harness State Authority]]
- [[Agent Memory]]
