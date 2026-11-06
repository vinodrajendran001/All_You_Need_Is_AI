---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-10-29-raindrop-agent-swarm-leadership
source_title: The surprising leadership dynamics in agent swarms
source_author: Yun Chi, Ben Hylak, and Ryan D'Onofrio
source_url: https://www.raindrop.ai/blog/agent-swarm-leadership/
tags:
  - source/summary
  - multi-agent
  - agent-behavior
  - evaluation
source_ids:
  - src-2026-10-29-raindrop-agent-swarm-leadership
status: active
---

# The Surprising Leadership Dynamics in Agent Swarms

## Summary

[[Raindrop]] ran a large set of leaderless agent teams. Each team had **eight** agents drawn from
**four** models (Claude Sonnet 5.5, GPT-6.1 Sol, Gemini 3.1 Pro and Kimi K3). The teams had to repair
**four** simulated outages through a shared channel. All agents had equal permissions, and none was
assigned to lead. The study asked how often a leader emerges and what determines who leads.

Its method is the durable contribution. An agent counts as a leader only if replaying its teammates'
turns with and without its post shows that its orders actually changed their decisions. Issuing
instructions or being "followed" is not enough.

The results:

- Across **2,160** teams, only **105** (5%) produced such a leader, although plans were common.
- The underlying model affected who led.
- The order of names in the prompt affected who issued plans.
- In **42%** of the decisions that an order changed, the agent's own texts did not mention the order.

All of this is a first-party study with no external replication, and several key comparisons lack a
described baseline or denominator.

## Key claims

### The game

- Each room is a simulated store with **10** services and **4** concurrent outages.
  - Each outage has an alert service and a root service where a configuration change caused it.
  - A list of **15** changes includes decoys, so the timing of a change does not reveal the cause.
- Each agent may examine one service, and only that agent sees the resulting card.
- The team gets **4** filings in total, and a wrong filing uses one up.
- A game lasts at most **8** rounds. In each turn an agent writes a private note and may also:
  - write a post of at most **280** characters;
  - examine a service;
  - file a change.
- Names (Ada to Hana) were rotated across models. The prompt says "All 8 of you have the same
  permissions" and "Use the channel however you think helps".

### Leadership is measured counterfactually

- An **order** names one teammate and one service or change. "Gil: payments" is an order; "Someone
  take payments" is not.
- A teammate **obeys** an order if it makes that decision within its next two turns.
- Each obeyed order was replayed **four** times: twice with the post and twice without it.
  - The order's weight is A − B, the with-post rate minus the without-post rate, floored at 0.
  - A leader's total weight must be at least **2** and must exceed every other agent's.
  - A leader needs **two or more** followers with positive weight.

### Instructions are common, leaders rare

- In **86%** of experiments, at least one agent proposed a plan assigning two or more teammates. In
  more than half, multiple agents proposed plans.
- Only **105 of 2,160 (5%)** produced a leader. Of those, **73** led with a round-1 plan and **32**
  emerged later.
- Teams still coordinated without a leader. "Access to the shared communication channel reduced
  duplicated actions from an average of **4.4 to 0.3** per experiment."

### The model matters, but planning is not leading

- Claude Sonnet 5.5 and GPT-6.1 Sol were "approximately **1.7 times** as likely" to lead as Gemini
  3.1 Pro. Kimi K3 led in **one** of the 105 experiments that had a leader.
- Gemini 3.1 Pro and Claude Sonnet 5.5 sent the most plans, but GPT-6.1 Sol had the most obeyed
  orders.
- The **268** followers came from the four models "in almost equal parts".

### Name order changes who plans

- Ada, listed first in the system prompt, was "three times more likely to issue a plan" than the
  others. When the list was reversed, Hana became three times more likely. The model rotation rules
  out model identity as the cause.
- Only the name list changed; permissions were identical. The effect is reported for plans, not for
  measured leadership.

### Agents often do not say what changed their minds

- **1,798** obeyed orders with positive weight changed a decision. Two Claude Sonnet 5.5 readers
  classified each agent's note, post and, where available, reasoning text. They "agreed on **97%** of
  the texts".
- Where the agent's texts placed the cause:

  | What the texts showed | Share |
  | --- | --- |
  | Author named in a post | **18%** |
  | Author named only in a note | **17%** |
  | Author named only in a reasoning text | **11%** |
  | A plan, but not its author | **12%** |
  | Only causes that are not orders | **42%** |

- For orders issued by the 105 leaders, **63%** of agents named the leader.

### Jev classified the orders

- A small classifier, Jev from [[TypeSafe AI]], extracted orders from every post. Jev is not one of
  the four models in the rooms.
- The test set was **60** random posts: **40** from round 1 and **20** from later rounds.
  - Two Claude copies, blind to Jev's answers, found **35** orders in only **9** posts.
  - Jev found all 35, for **100%** recall. It also found **4** incorrect orders, for **90%**
    precision.

## Why it matters

- [[Multi-Agent Coordination]] gets direct evidence that peers with equal authority still change one
  another's decisions. Effective leadership is rarer than plan-issuing. Prompt layout and model mix
  are configuration choices that shift influence.
- [[Agent Delegation]] gets a peer-to-peer counterpart to its zone-of-indifference material. Agents
  act on teammates' orders without any authority to issue them, and often without recording that
  they did.
- [[Chain-of-Thought Monitoring]] (proposed) gets a measured gap: an agent's own text often omits the
  cause that counterfactual replay shows was operative.
- [[TypeSafe AI]] (proposed) gets a third-party use of Jev as a measurement instrument, with a small
  validation.
- [[Raindrop]] is the publisher.

## Tensions / open questions

- This is a **first-party** study with no external replication. The figures' chart values were not
  transcribed, so the per-model leader counts behind "1.7 times" cannot be checked.
- **Duplicated actions (4.4 to 0.3).** The no-channel condition is not described anywhere in the
  capture, including how many such runs there were.
- **Name order.** "Three times" has no denominators. The effect is on plans; the study does not show
  it on leadership.
- **Leader weights are coarse.** With four replays per order, an order's weight can take only a few
  values. The study does not report how sensitive the 105-leader count is to that noise.
- **Jev's validation is small, and its labels came from Claude, not humans.** The 60 posts contained
  only 9 with orders. The Claude version is unspecified, and "the first test" is not defined.
- **The 42% reading.** It relies on Claude Sonnet 5.5 readers, and Claude Sonnet 5.5 is also a model
  under test. The 97% figure is reader agreement, not accuracy.
- The capture uses "teams", "experiments" and "mixed rooms" interchangeably for the 2,160 runs.

## Affected pages

- [[Multi-Agent Coordination]]
- [[Agent Delegation]]
- [[Raindrop]]
- [[TypeSafe AI]]
- [[Chain-of-Thought Monitoring]]

## Raw capture

- [[knowledge-base/raw/sources/2026-10-29 Yun Chi, Ben Hylak, and Ryan D'Onofrio - The surprising leadership dynamics in agent swarms]]
- [[knowledge-base/raw/sources/The surprising leadership dynamics in agent swarms]]. This is the
  original November 2 clipping. It holds only the truncated TL;DR abstract and lists the author as
  "Raindrop AI". It is kept for provenance and is not cited as evidence here.

## Citations

- Canonical URL: https://www.raindrop.ai/blog/agent-swarm-leadership/ (tracking parameters removed).
- Byline: Yun Chi, Ben Hylak, and Ryan D'Onofrio. Publisher: Raindrop.
- Published: 2026-10-29. The page is in the "Model Behavior" category, with a 17-minute reading time.
- Recaptured: 2026-11-06. The original clipping was captured 2026-11-02.

## Related pages

- [[Multi-Agent Coordination]]
- [[Agent Delegation]]
- [[Raindrop]]
- [[TypeSafe AI]]
- [[Chain-of-Thought Monitoring]]
- [[Siddhant Rai - Jev - Models Built for Decisions Rather Than Text]]
- [[Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost]]
- [[Ethan Mollick - The Dot and the Swarm]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[axjns.dev - The Sticky-Note Problem]]
