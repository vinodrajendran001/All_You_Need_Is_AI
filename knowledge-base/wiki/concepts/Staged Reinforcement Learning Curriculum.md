---
type: concept
created: 2026-08-27
updated: 2026-08-27
tags:
  - concept
  - reinforcement-learning
  - post-training
  - ai-agents
  - training
source_ids:
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
status: active
---

# Staged Reinforcement Learning Curriculum

## Definition

A staged RL curriculum treats post-training as a **chain of independent reinforcement-learning
runs** rather than a single optimization. Each stage targets one capability, carries its own reward
signal and hyperparameters, and warm-starts from the checkpoint the previous stage exported. The
curriculum is the ordering of those stages, not a schedule inside one run.

## Why it matters

Multi-objective RL is the default situation for any modern model: it needs to be good at math,
code, instruction following, tool use, agentic task completion, and safety, and those objectives
have incompatible reward shapes. Some are verifiable by a unit test, some need an LLM judge, some
are a single bit at the end of a hundred-turn trajectory.

Blending them into one reward function forces a weighting problem with no principled answer and no
way to attribute a regression. Sequencing them instead makes the problem **debuggable**: each stage
has one objective, one reward, and a clean checkpoint boundary, so a stage that fails can be re-run
or re-weighted without discarding the ones before it.

This is a different axis from the curricula already described on [[Agentic Reinforcement Learning]].
ScalingInter-RL growing an interaction budget over phases, or LIMR selecting learnable examples, are
curricula *within* a run — they change the data the optimizer sees. A staged curriculum changes
which optimizer run you are in at all.

## The worked example

[[IBM Granite Team - Granite 4.2 LLMs How They're Built]] is the clearest published instance in this
vault, because it gives the whole ladder with its numbers:

```
SFT ─▶ RLVR ─▶ Skill boosters ─▶ SWE agent ─▶ Terminal ─▶ Search ─▶ RLHF
      └──────── foundational RL ────────┘   └────── agentic RL (8B / 30B) ──────┘
```

Every stage is a separate GRPO run. When it finishes, the policy is exported to Hugging Face format
and becomes the base model for the next stage. The hyperparameter backbone stays fixed — GRPO with
no value network, ratio clip 0.2/0.28, micro-batch 1, tensor-parallel 2–4 — and what changes per
stage is the *shape*: prompts per step, generations per prompt, sequence length, rollout turns, KL,
and learning rate.

## Ordering principle: verifiable first, preference last

The stages are not in arbitrary order. Granite front-loads **verifiable** rewards — exact match,
unit tests, format checkers — because they are objective and hard to game. Judge- and
preference-based rewards come later, handling open-ended qualities no checker can express. Agentic
outcome rewards, the sparsest of all, sit between them and depend on the skills the earlier stages
installed.

The reasoning is that a stage can only be as trustworthy as its reward. Building capability against
signals that cannot be gamed, then shaping tone and safety against signals that can, limits how much
of the final model's behavior rests on a corruptible objective.

## The KL schedule should follow the reward type

The most transferable rule this pattern produces is that **the KL coefficient is not a global
tuning knob — it should be keyed to what the stage is optimizing**.

Granite runs KL = 0 on RLVR and on the long-horizon SWE stage, letting the policy roam freely,
because those rewards are objective and verifiable: if the tests pass, the behavior is good
regardless of how far it drifted from the reference. It uses KL = 0.05, the pipeline's highest, on
RLHF and on the code booster, because those optimize preference, safety, or a narrow skill graft —
objectives where drift is indistinguishable from reward hacking, and where the reference policy's
general competence is the thing worth protecting.

Stated generally: **if you can verify the answer, let the model explore; if you are optimizing taste,
safety, or one narrow skill, hold it near the reference.** A "booster" stage is exactly the case for
a light KL penalty, since the goal is to nudge one capability without moving general behavior.

## What makes staging affordable

A chain of stages is only practical if adding a stage is cheap, and that depends on the environment
interface. Granite's NeMo-Gym exposes verifiers, tools, sandboxes, and reward models as
interchangeable **Resources** behind a uniform interface, so — in the source's own framing — a
booster's rule-based checker and a full containerized SWE sandbox present the same interface to
GRPO.

This is the fourth independent convergence on modular environment interfaces recorded in this vault,
after AgentGym-RL's unified HTTP services, Agent-R1's Tool/ToolEnv abstractions, and AgentRL's
function-call environment API (see [[Agentic Reinforcement Learning]]). Granite states the payoff
most directly: interface uniformity is what turns a curriculum from a research project into a
configuration change.

The second enabler is the asynchronous training loop. Generation and policy updates live on separate
GPU pools, so the expensive generation fleet — including live agentic environments — stays busy
instead of idling through optimizer steps. A staged curriculum multiplies the number of RL runs, so
per-run efficiency compounds across the chain.

## Capability can be gated by position on the ladder

Granite's three sizes share one method and one infrastructure; what differs is how far up the ladder
each goes. The 3B model takes a shortened path — foundational RL and alignment, no agentic block —
while 8B and 30B run the full chain and learn to act with tools in real environments.

This gives a clean way to think about capability tiers in a model family: rather than training
different models differently, train them identically and stop at different rungs. It also means the
3B model's absence from SWE-Bench and Terminal-Bench is a **scope decision rather than a measured
limitation** — the source does not establish that a 3B model could not have learned agentic
behavior, only that it was not given the stages. See [[Small Language Models]].

## Costs and unknowns

- **Nothing is ablated.** The staged chain is presented as what was done, never against a
  single-run baseline. The pattern's advantages described above are engineering arguments, not
  measured results.
- **Stages can undo each other.** Granite's own RLHF stage applies a reasoning-length penalty
  specifically to remove verbosity that earlier stages induced, which is direct evidence that
  capability stages leave behavioral residue the alignment stage has to clean up. Whether later
  stages also erode earlier capabilities is not reported.
- **Order is asserted, not derived.** No evidence is given that SWE → Terminal → Search beats any
  other permutation.
- The chain multiplies infrastructure cost: every stage needs its own reward plumbing, environment
  fleet, and checkpoint validation.

## Open questions

- Does a staged chain actually beat a single blended-reward run at matched compute, or is its real
  advantage debuggability rather than final quality?
- How much of an earlier stage's capability survives to the end of the chain, and does that decay
  bound how long a curriculum can usefully get?
- Is there a principled way to order stages, or does it reduce to putting verifiable rewards first
  and preference last?
- If a stage regresses a capability, is re-running it cheaper than re-weighting a blended reward
  would have been — the central practical claim, and the one with no published evidence?

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[Agentic Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[Reinforcement Learning]]
- [[Small Language Models]]
- [[IBM]]
- [[AI Knowledge Base Overview]]
