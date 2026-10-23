---
type: entity
created: 2026-10-23
updated: 2026-10-23
entity_kind: person
tags:
  - entity
  - ai-agents
  - forecasting
source_ids:
  - src-2026-10-19-naam-million-agents-superintelligence
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

## Related pages

- [[Recursive Self-Improvement]]
- [[Automated AI Research]]
- [[Agent Delegation]]
- [[Self-Replicating Agents]]
- [[Test-Time Scaling]]
- [[Benchmark Optimization]]
- [[Epoch AI]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
