---
title: "Agents Need Somewhere to Share Their Work"
source: "https://axjns.dev/blog/synthetic-membrane"
author:
published:
created: 2026-11-04
description: "What makes agents useful as a team, and how a shared, policy-controlled workspace might help."
tags:
  - "clippings"
---
I keep coming back to the gap between a collection of capable agents and a team that can build on its own work. Adding another agent is straightforward. Making its contribution useful to the others is a different problem.

The [Superminds Test](https://arxiv.org/abs/2604.22452) makes that distinction hard to ignore. Researchers probed MoltBook, a platform hosting more than two million agents, and found weak joint reasoning, limited synthesis, and shallow interaction. That is a result about a particular agent society and its tests. It does not mean two million agents were assembled into one controlled team, or that all multi-agent systems fail.

Still, it challenges an attractive assumption: enough individually capable participants will somehow become collectively capable. I want to understand what infrastructure helps them get there.

## Give the work somewhere to live

A useful team accumulates more than messages. It has a codebase, shared documents, decisions that can be revisited, and a way to tell what remains unfinished. Those artefacts let people contribute without reconstructing every conversation that preceded them.

Agent systems can have those properties too. Shared memory, persistent graph state, and blackboard architectures already exist. The question I am exploring is how to make the boundary around shared work explicit: what an agent can publish, what another agent should receive, and what either is allowed to do with it.

I call that boundary a **synthetic membrane**. The biological metaphor is selective permeability. It helps name the design intention; it is not evidence that software agents will behave like cells. The implementation is familiar infrastructure: records, queries, subscriptions, policy checks, and task ownership.

## Three responsibilities at the centre

First, **selective exchange**. An agent publishes a finding under a visibility policy. Other agents discover or subscribe to relevant changes within their permissions. Access control decides what they may receive; relevance and context budgets decide what is useful to deliver now. A model's confidence in a peer cannot override those permissions.

Second, **persistent shared state**. Evidence, interpretations, and actions have stable identities. A summary points back to its source. A retracted claim stays identifiable as retracted. A replacement agent can read the current view and recent changes instead of consuming the whole conversation history.

Third, **explicit coordination**. Agents can discover work, claim a task, propose an action, and transfer responsibility. An exclusive claim needs enforcement at execution time so that two workers cannot act on competing assumptions about ownership. Shared memory on its own does not provide that guarantee.

Discovery and governance surround these responsibilities; defence cuts across them. The full proposal has six conceptual responsibilities, with observability throughout. They need not become six services. A small implementation with clear semantics is more useful than a diagram that gets ahead of the code.

![Proposed membrane responsibilities: governance, discovery, access, shared state, coordination, and cross-cutting defence](https://axjns.dev/architecture.svg)

Conceptual responsibilities; implementation and evaluation remain in progress.

## Start with the blackboard precedent

The closest relative is the blackboard: specialists contribute to a common workspace.[Han and Zhang](https://arxiv.org/abs/2507.01701) investigate that pattern for LLM collaboration. [Salemi and colleagues](https://arxiv.org/abs/2510.01285v2) evaluate it for data discovery. Their results make shared work worth testing, without establishing that my particular combination is better.

The membrane's proposed value is in connecting that workspace to permissions, provenance, and action ownership across runtimes. None of those ideas is individually new. If an existing blackboard or persistent workflow can provide the same behaviour more simply, it should win the comparison.

That also means the membrane should compose with agent protocols. MCP can expose its tools and resources; A2A can carry task interactions. Agents still communicate through messages. The difference is that the state of the work remains addressable after a message has been delivered.

## The economics depend on who reads

A shared store can remove repeated publication and make selective retrieval possible. It cannot make the cost of reading disappear. If N agents each contribute F facts and every agent reads every fact, the total information delivered still grows as O(N²F).

This matters for the small simulation below. Its message counts and token-equivalent estimates describe a stipulated exchange model. They are not measurements of an LLM team's accuracy, latency, or API bill. Fewer envelopes can help, but fewer messages are not automatically less context or better decisions.

The table is consistent with a baseline of 1,240N(N−1) token-equivalents and a membrane estimate of 300N² + 540N for five facts per agent. **Both estimates are quadratic in N.** The membrane estimate is lower under those assumptions because its overhead differs, not because shared storage has made all communication linear.

Real savings would have to come from delivering fewer irrelevant facts, reusing useful work, or avoiding retries. Those benefits must include the cost of indexing, summarisation, gating, and any missed evidence. They need measurement at the model boundary.

## What the prototype can tell us

The five-agent simulation exercises registration, visibility checks, publication, retraction, and group activation. Its terminal output is a recorded demonstration of those mechanics. The trust thresholds in that demonstration are simplified rules, not a validated model of identity or permission.

The intended integration setting is [Sympozium](https://github.com/sympozium-ai/sympozium). The engineering task is to turn a small coordination contract into enforceable behaviour, then compare it with a single agent, a persistent orchestrator, and a conventional blackboard under matched budgets. The [revised paper](https://axjns.dev/research/0001-synthetic-membrane-coordination-layer) sets out that test in more detail.

I would like this to make agent teams easier to operate: less repeated context, clearer handoffs, and a record that explains why an action happened. I do not yet have evidence that it delivers all three. That is the work ahead, and the most useful feedback is a workload or a simpler design that puts the proposal under pressure.[Implementation](https://github.com/sympozium-ai/sympozium)

[

sympozium-ai / sympozium

github.com →

](https://github.com/sympozium-ai/sympozium)[

Research

AlexsJones / research

github.com →

](https://github.com/AlexsJones/research)[

Paper

Full paper (v2.2), read on site

axjns.dev →

](https://axjns.dev/research/0001-synthetic-membrane-coordination-layer)

Additional Visualizations

## State Graph

![State transition graph](https://axjns.dev/state_graph.svg)

## Illustrative Communication Costs

These are illustrative simulation results. Message and step counts describe the demo protocol; token-equivalents use stipulated costs of 90 tokens per envelope, 60 per fact, and 8 per acknowledgement. They are not measured API usage or evidence of better task outcomes. Store requests can carry many facts, so a reduction in message count need not imply the same reduction in context.

![Illustrative three-agent simulation: 60 versus 18 messages and 7,440 versus 4,320 modelled token-equivalents](https://axjns.dev/benchmark.svg)

## Five-Agent Simulation

```
──  Five-agent coordination simulation  ──
registration · permeability · trust · subscriptions · swarms

BOOT   membrane instantiated
       · store · permeability engine · swarm engine

▸ orchestrator  register_agent  caps=[coordination, planning, synthesis]
▸ researcher    register_agent  caps=[research, fact_check, data_analysis]
▸ writer        register_agent  caps=[writing, drafting, summarization]
▸ editor        register_agent  caps=[editing, reviewing, style]
▸ reviewer      register_agent  caps=[reviewing, critique, quality_check]

▸ orchestrator  set_trust  → writer = 0.7
▸ orchestrator  set_trust  → editor = 0.7
▸ orchestrator  set_trust  → researcher = 0.7
▸ writer        set_trust  → editor = 0.9
▸ editor        set_trust  → writer = 0.9
▸ editor        set_trust  → reviewer = 0.8

▸ orchestrator  expose  tasks.brief  [public]
▸ researcher    query tasks.* → HIT  "Write a 500-word brief..."

▸ researcher    expose  findings.heat_islands  [public]
▸ researcher    expose  findings.coastal_risk  [public]
▸ researcher    expose  findings.green_infra  [public]
▸ researcher    expose  findings.notes_internal  [PRIVATE]

▸ writer        query findings.* → 3 hits  (PRIVATE note: HIDDEN)
▸ writer        expose  drafts.intro  [trusted]
▸ writer        expose  drafts.body  [trusted]
▸ writer        expose  drafts.outro  [trusted]

▸ reviewer      query drafts.* → DENIED  (trust=0.00 < 0.50)
▸ editor        query drafts.* → HIT  (trust=0.90)

▸ editor        expose  feedback.intro  [trusted]
▸ editor        expose  feedback.body  [trusted]
▸ writer        query feedback.* → HIT → revising...
▸ writer        retract  drafts.intro  (superseded)
▸ writer        expose  final.brief  [public]

▸ orchestrator  swarm_create  "Final Review"  cap=reviewing  threshold=2
▸ editor        swarm_join  members=1/2  active=False
▸ reviewer      swarm_join  members=2/2  active=True  ★ ACTIVATED

▸ writer        broadcast  "Brief complete"  → 4 recipients

──  Final Store State  ──
events       32    registered    5    entries     8
subscriptions 4    broadcasts    1    swarms      1
trust edges  7    last seq      32

key                    owner         tier      value
────────────────────────────────────────────────────
tasks.brief            orchestrator  public    Write a 500-word brief...
findings.heat_islands  researcher    public    Urban heat islands raise...
findings.coastal_risk  researcher    public    1B people exposed to...
findings.green_infra   researcher    public    Green roofs reduce cooling...
findings.notes_internal researcher   private   TODO verify IPCC citation...
feedback.intro         editor        trusted   Strengthen the opening...
feedback.body          editor        trusted   Cite the IPCC AR6 figures...
final.brief            writer        public    Cities like Singapore...

simulation complete · 32 events · 22ms wall-clock
```

## Scaling: N agents × 5 facts each

Both series are modelled token-equivalents for five facts per agent. Both grow quadratically: 1,240N(N−1) for the baseline and 300N² + 540N for the membrane. The lower estimate reflects this model's exchange assumptions, not a general change from quadratic to linear token consumption.

| Agents | Baseline Estimate | Membrane Estimate | Reduction |
| --- | --- | --- | --- |
| 3 | 7,440 | 4,320 | 41.9% |
| 5 | 24,800 | 10,200 | 58.9% |
| 8 | 69,440 | 23,520 | 66.1% |
| 12 | 163,680 | 49,680 | 69.6% |
| 20 | 471,200 | 130,800 | 72.2% |

```
──  Baseline vs. Membrane  ·  3 agents  ·  5 facts each  ──

┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃  metric               ┃  baseline  ┃  membrane  ┃           reduction  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│  messages             │        60  │        18  │      70.0%  (60→18)  │
│  token-equivalent     │     7,440  │     4,320  │               41.9%  │
│  cost                 │            │            │         (7440→4320)  │
│  consensus steps      │         6  │         2  │        66.7%  (6→2)  │
└───────────────────────┴────────────┴────────────┴──────────────────────┘

──  Scaling sweep · N agents · 5 facts each  ──

┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃  agents  ┃  baseline estimate  ┃  membrane estimate  ┃  reduction  ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│       3  │            7,440  │            4,320  │      41.9%  │
│       5  │           24,800  │           10,200  │      58.9%  │
│       8  │           69,440  │           23,520  │      66.1%  │
│      12  │          163,680  │           49,680  │      69.6%  │
│      20  │          471,200  │          130,800  │      72.2%  │
└──────────┴───────────────────┴───────────────────┴─────────────┘
```