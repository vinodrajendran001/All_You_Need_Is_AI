---
type: entity
created: 2026-10-23
updated: 2026-11-27
entity_kind: person
tags:
  - entity
  - ai-agents
  - forecasting
source_ids:
  - src-2026-10-19-naam-million-agents-superintelligence
  - src-2026-11-09-zvi-ai-rd-acceleration-rsi
  - src-2026-11-24-zanichelli-swarms-raise-the-roof
status: active
---

# Ramez Naam

## What it is

Author of **"Can a Million AI Agents Create Superintelligence?"**, a survey-and-synthesis essay that
assembles roughly a dozen multi-agent scaling results and argues they are consistently **logarithmic or
sub-logarithmic**.

## Why it matters here

Naam supplies the vault's most carefully assembled **negative result** on multi-agent scaling, and the
distinction he builds it on is the durable part:

> **"More agents are useful for speed: they can solve many problems faster. They're less useful for
> boosting AI intelligence."**

Three mechanisms are offered for the gap: **coordination** cost, **homogeneity** producing shared blind
spots, and the **sequential structure** of hard problems — *"A million independent searches can run at
once. A sequential investigation can't."*

This matters to [[Recursive Self-Improvement]] and [[Automated AI Research]] because it attacks a
specific modelling assumption rather than the general idea. Several published takeoff models assume
doubling effective research labor multiplies the improvement rate by substantially more than one;
Naam's point is that **the same observed inputs produce wildly different predictions** under different
scaling exponents — a spread of roughly 1.1x to 25x for one worked period — and that the spread itself
is the argument for measuring rather than extrapolating.

His proposed measurement is the constructive contribution: report **G** (verified task-performance gain
per multiplication of agents), **λ** (speed-cost scaling), and **N** (the team size where gains
saturate), **separately for 1→10, 10→100, and 100→1,000 agents**. Averaging across those ranges hides
exactly the saturation the data shows.

## Notes

### Epistemic stance

Naam states his own position plainly: **"We're all operating on far too little real world data."** The
essay is explicitly a synthesis of **third-party results**, not an experiment, and the vault treats it
as a well-sourced argument rather than as evidence in itself.

### The pattern across the assembled evidence

Several independent results point the same way, which is what gives the essay its force — while each
individually carries its own scope limits:

- Formal-math scaling where the local speed exponent fell from about **0.75 to 0.33** as teams grew from
  10→30 and then 30→100 agents.
- A hundred-agent formal-math team that gained **27 score points** going from ten to one hundred agents
  and only **two** beyond that, despite self-organizing a hierarchy with 12 sub-leads and spending 10x
  the aggregate runtime.
- A security benchmark whose peak scores rose about **5.2 points total** across two fourfold increases
  in agent count — **3.1** then **2.1**.
- A diversity study showing substantial gains up to **8 agents**, then barely any movement.
- A large concurrent research run whose lead attributed **"not even 10%"** of the result to multi-agent
  scaling.

### A falsifiable forecast

Allowing a six-month research-to-publication lag, Naam expects **no sustained acceleration in the Epoch
Capabilities Index through the first half of 2027**. The vault should revisit this page against
[[Epoch AI]] data rather than letting the forecast sit unchecked.

A first lab-internal reading arrived in November 2026.
[[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]] relays [[METR]]'s estimate
that [[Anthropic]]'s AECI, its internal version of the index, has grown 1.9x the pre-October 2025
rate (95% CI 1.5-2.8x). On its face this cuts against the forecast, but it is not a refutation:
- AECI is not the public index Naam named.
- The figure falls to 1.4x when other developers' models are included.
- Toby Ord and Peter Wildeford argue part of it may be a one-time jump or an RL catch-up rather than
  sustained acceleration.

Naam's 1.1x-25x spread predicts research pace, while METR's 1.9x is a growth rate of a capability
index, so the two numbers should not be matched directly. Public ECI through mid-2027 remains the
test.

### A matched-budget test of the speed-not-intelligence reading

[[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]] runs the kind of controlled measurement
Naam called for, at much smaller scale. Its evidence table lists his essay as finding a **penalty**
for swarms, records his λ as **0.75** below 30 agents and **0.33** below 100, and marks it as
lacking a matched-compute control: "No lone agent is given a longer clock", and his λ analysis takes
ten agents as its starting point.

Zanichelli's own teams, mostly of 2 to 8 agents, got the same weighted-token budget as one agent.
They scored about 7% worse in 54 of 70 comparisons while finishing several times sooner, which
supports Naam's split between speed and intelligence. The study also adds an explanation his three
mechanisms do not cover. On one task, teams beat a single long session, but a single agent restarted
into eight fresh sessions beat the teams, which the author attributes to stale context building up
in long sessions. A team premium measured against one long session can therefore reflect the single
agent's context management rather than collective intelligence. The study's recommended λ of 0.6 to
0.9 comes from that one task, and most settings ran three times.

## Related pages

- [[Recursive Self-Improvement]]
- [[Automated AI Research]]
- [[Agent Delegation]]
- [[Self-Replicating Agents]]
- [[Test-Time Scaling]]
- [[Benchmark Optimization]]
- [[Epoch AI]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]]
- [[METR]]
- [[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]]
- [[Multi-Agent Coordination]]
