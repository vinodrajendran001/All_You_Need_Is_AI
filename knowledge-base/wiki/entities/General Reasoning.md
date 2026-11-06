---
type: entity
created: 2026-11-06
updated: 2026-11-06
entity_kind: organization
tags:
  - entity
  - organization
  - reinforcement-learning
  - multi-agent
source_ids:
  - src-2026-11-04-general-reasoning-train-swarm
status: active
---

# General Reasoning

## What it is

General Reasoning (gr.inc) is the research organisation behind RLCR, a published recipe for
training agent collectives with reinforcement learning, and behind the Avalon-M1 model trained
with it. In this vault it is the publisher of [[General Reasoning - How to Train a Swarm]]. The
post is bylined to the "General Reasoning team". Its suggested citation for the Avalon-M1
technical report lists Iliyan Zarov, Henry Course, Anthony Hartshorn, Ran Achiron, Louis Roche,
Akshit Sinha, Chengxi Taylor and Ross Taylor.

## Why it matters here

Most multi-agent material in the vault concerns systems assembled at inference time: prompted
teams, orchestrators and harness topologies. General Reasoning is the first source of a training
recipe in which every agent shares one policy and one collective reward. Latency pressure comes
from a wall-clock cap that rises over training, and the environments can report progress at any
moment. That makes it a reference point for [[Multi-Agent Coordination]],
[[Agentic Reinforcement Learning]] and the latency side of [[Test-Time Scaling]].

Its design stance is also distinctive. It treats any imposed team structure as a prior, whether
Kimi's trained orchestrator, its own CEO that can hire and fire, or OpenAI's island split, and it
argues that communication primitives should stay simple enough for the policy to discover better
organisation itself. See [[Agent Delegation]].

## Evidence boundary

All Avalon-M1 results are first-party, and the captured charts state no values in text; scores can
only be estimated from SVG geometry. The headline claim is that, at a matched-token budget, a
single-agent baseline takes **4x** as long as the collective. That claim lacks a stated benchmark
set, budget or variance in the capture. The training collectives had at most **9** agents. The
organisation itself names the gap to deployed swarms of hundreds or thousands, together with
flat-advantage credit assignment and the absence of credit for shared public goods, as open
problems. A full paper is promised "in the coming weeks once training finishes".

## Related pages

- [[General Reasoning - How to Train a Swarm]]
- [[Multi-Agent Coordination]]
- [[Agentic Reinforcement Learning]]
- [[Test-Time Scaling]]
- [[Reward Design for RL]]
- [[RL Environment Design]]
- [[Long-Horizon Credit Assignment]]
- [[Agent Delegation]]
- [[OpenAI]]
