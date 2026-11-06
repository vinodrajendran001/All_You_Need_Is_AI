---
type: entity
entity_kind: organization
created: 2026-11-06
updated: 2026-11-06
tags:
  - entity
  - organization
  - multi-agent
source_ids:
  - src-2026-10-29-raindrop-agent-swarm-leadership
status: active
---

# Raindrop

## What it is

Raindrop publishes research on its blog at raindrop.ai, under a "Model Behavior" category. It is the
publisher of [[Yun Chi et al - The Surprising Leadership Dynamics in Agent Swarms]], written by Yun Chi,
Ben Hylak and Ryan D'Onofrio. That article refers to an earlier Raindrop experiment, *huggingworld*,
in which agents followed instructions from other agents although no leader had been assigned. The
huggingworld post is not captured in the vault.

## Why it matters here

Raindrop supplies the vault's largest controlled study of leaderless agent teams: **2,160** teams of
eight agents drawn from four models, solving simulated outages through a shared channel. Its method is
more reusable than its headline numbers. Raindrop counted an agent as a leader only if replaying its
teammates' turns with and without its post showed that its orders changed their decisions.

That replay design separates three things that are easy to conflate:

- issuing instructions;
- being followed;
- actually changing a decision.

It is what exposed the finding that in **42%** of order-driven decisions, the agent's own texts never
mentioned the order. See [[Multi-Agent Coordination]].

The study also used a third-party classifier, Jev from [[TypeSafe AI]], as a measurement instrument.
Jev extracted orders from posts. That gives the vault an independent use of Jev outside its vendor's
own materials, with a small validation against Claude-produced labels.

## Notes

- All findings are first-party and unreplicated. The capture does not describe the no-channel
  condition behind the reported fall in duplicated actions, and the name-order effect has no
  denominators.
- **Provenance.** The original clipping attributed the article to "Raindrop AI" and held only a
  truncated abstract. The recapture carries the three-author byline and the full appendices.

## Related pages

- [[Yun Chi et al - The Surprising Leadership Dynamics in Agent Swarms]]
- [[Multi-Agent Coordination]]
- [[Agent Delegation]]
- [[TypeSafe AI]]
- [[Chain-of-Thought Monitoring]]
