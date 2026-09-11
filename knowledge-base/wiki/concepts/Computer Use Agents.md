---
type: concept
created: 2026-09-11
updated: 2026-09-11
tags:
  - concept
  - topic/agents
  - topic/reinforcement-learning
source_ids:
  - src-2026-09-09-raschka-astra-looped-hidden-reasoning
status: active
---

# Computer Use Agents

## Definition

Agents that operate a general-purpose computer through its graphical interface — reading screenshots and
emitting mouse and keyboard actions — rather than through APIs or a tool schema. The distinguishing
property is that the action space is the one a human uses, so the agent inherits the entire installed
software base without needing an integration for each application.

## Why it matters

It is the capability [[Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]]
identifies as the substantive advance in GPT-6 Astra, against an architectural story (looped
transformers) that received most of the press attention and explains much less.

The training arrangement is the interesting part, and it is a procurement story as much as a research
one. OpenAI reportedly bought **tens of thousands of Mac Minis and Mac Studios — not for training
compute, but as reinforcement learning environments**. The loop has seven steps: give the model a prompt,
feed it screenshots, have it predict mouse and keyboard actions, execute them, capture new screenshots,
repeat, and let a verifier supply reward. Raschka frames it as the GUI analogue of RLVR — reinforcement
learning from verifiable rewards, with the verifiable outcome being a task completed on a real machine.
(The same model was separately reported by NVIDIA's CEO as trained on roughly **100,000 Grace Blackwell
GPUs**, a figure about the pretraining side rather than the environment fleet.)

That makes computer use the clearest instance to date of the pattern [[Synthetic Data Flywheel]]
documents from the data side: when capability is bounded by environments rather than by parameters, labs
buy environments. Here the environment is physical consumer hardware.

## Current synthesis

**The action space is the point, and so is its cost.** A tool-calling agent needs an integration per
capability; a computer-use agent needs none, but pays in tokens (screenshots are expensive), in latency
(every action is a round trip through a real UI), and in fragility (interfaces change without notice and
without a version number).

**Verification is what makes RL possible here.** The reward comes from a verifier checking whether the
task was actually completed on the machine, which places computer use on the favourable side of
Verifier's law — "the ease of training AI to solve a task is proportional to how verifiable the task is."
Many GUI tasks have checkable end states (a file exists, a form was submitted, a setting changed), which
is why this is trainable at all, and why the tasks that are *not* checkable will lag.

**It is a different axis from reasoning depth.** Astra's ARC-AGI-3 result (**99.9%, against 7.8% for
GPT-5.6 Sol**) sits alongside a much narrower lead on coding-agent indices. Computer use is the
capability the environment investment was aimed at; it is not obviously the same thing the reasoning
benchmarks measure.

**Agent configuration may now be a liability rather than an asset.** Raschka suggests archiving stale
`AGENTS.md` and `SKILL.md` content, since newer models "may be over-constrained by it" — instructions
written to compensate for a weaker model's limitations become a cage for a stronger one. That
generalises to the harness material under [[Coding Agent Harness]] and [[Agent Skill]]: harness
scaffolding has a shelf life tied to the model generation it was written against.

**Observability becomes harder, not easier.** A tool call produces a structured span with arguments and a
return value; a screenshot-and-click sequence produces neither. The permission-gate and
side-effect-tracing requirements in [[Agent Observability]] have no obvious analogue when the action is
"click at (840, 312)".

## Open questions

- No public evidence here on how well GUI skills transfer across operating systems, applications, or
  interface redesigns. A policy trained on macOS screenshots is an open question everywhere else.
- The environment fleet is physical hardware, which caps throughput by machine count rather than by GPU
  availability. How that scales, and whether virtualised environments substitute, is unaddressed.
- Safety surface is wide and largely unexamined: an agent with mouse and keyboard control has no natural
  allowlist, and the tool-roster and permission-mode controls described in [[Agent Delegation]] do not
  apply to a pointer.
- Screenshot-based observation is token-expensive, and none of the available material gives a cost per
  completed task.
- Nothing establishes whether computer use is complementary to tool calling or eventually replaces it for
  applications that expose both.

## Related pages

- [[AI Agents in Production]]
- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[Coding Agent Harness]]
- [[Agent Skill]]
- [[Agent Delegation]]
- [[Agent Observability]]
- [[RL Environment Design]]
- [[Agentic Reinforcement Learning]]
- [[Synthetic Data Flywheel]]
- [[Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]]
