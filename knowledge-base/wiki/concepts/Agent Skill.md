---
type: concept
created: 2026-06-22
updated: 2026-06-22
tags:
  - concept
  - agents
  - skills
  - orchestration
  - optimization
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-06-22-djfarrelly-agent-loop-architecture
  - src-2026-06-22-alphasignal-agent-skill-optimization
status: active
---

# Agent Skill

## Definition

An agent skill is a reusable capability artifact that helps an agent perform a family of tasks more reliably than a one-off prompt. The current sources use "skill" in two related but distinct ways: as a **markdown operating procedure** that shapes model behavior, and as a **durable workflow** that executes a multi-step task with retries, checkpoints, and observability.

## Why it matters

Skills are how agent capability becomes persistent infrastructure. A conversation disappears; a skill can remain callable, testable, versioned, optimized, and reused by later loops. That is why skills matter for production agents: they turn model behavior into an asset that can compound across runs, users, and model upgrades.

## Current synthesis

The vault now has three useful layers for thinking about skills:

1. **Instruction skill** — [[Alpha Signal - How your agents can write and optimize their own skills]] describes skills as standalone `.md` files: task procedures containing instructions, tool-use guidelines, output formats, and failure-recovery logic.
2. **Execution skill** — [[djfarrelly - The Agent Loop Architecture]] describes skills as durable workflows: multi-step, retryable, composable functions that can be triggered by loops or other agents.
3. **Action substrate** — [[pguso - Agents From Scratch]] provides the lower-level mechanics: structured outputs, tool request/execute separation, explicit state, plans as data, atomic actions, dependency graphs, evals, and telemetry.

The tension is that "skill" is not yet a stable industry term. One source says a skill is not a prompt; another says it is a markdown file. The most useful synthesis is to treat a production skill as having **both** a policy layer and an execution layer:

- the policy layer says what the agent should do and how it should use tools;
- the execution layer runs the procedure durably, checkpoints progress, enforces concurrency, stores run history, and handles failures.

Skill optimization is the next layer. Alpha Signal's source frames SkillOpt, GEPA, and EvoSkill as text-space optimizers for skill files:

- run tasks and record trajectories;
- score them with verifiers;
- reflect on failure patterns;
- propose bounded add/delete/replace edits;
- validate on held-out tasks;
- keep rejected-edit buffers or Pareto frontiers to avoid regressions.

This makes a skill file look like "trainable external state." It is not trained by gradients, and it does not change model weights, but it can still improve through a controlled optimization loop.

Durable orchestration makes those optimized skills operational. [[djfarrelly - The Agent Loop Architecture]] argues that a skill must survive restarts, avoid duplicate side effects, expose run history, retry only failed steps, and remain callable by scheduled or event-driven loops. Without that layer, a skill may be a useful instruction document but not dependable production infrastructure.

## Open questions

- Should "skill" mean the text procedure, the executable workflow, or the bundle of both?
- What governance is needed before agents can safely write, deploy, and revise their own skills?
- How should teams evaluate skill edits so they improve one task without regressing another?
- Can skill libraries become portable across models and harnesses, or will they remain tightly coupled to a specific runtime?

## Related pages

- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Agent Planning]]
- [[Context Engineering]]
- [[Tool Use and Function Calling]]
- [[Agent Memory]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[pguso - Agents From Scratch]]
- [[Inngest]]
