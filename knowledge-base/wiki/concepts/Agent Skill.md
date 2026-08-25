---
type: concept
created: 2026-06-22
updated: 2026-08-25
tags:
  - concept
  - ai-agents
  - skills
  - orchestration
  - optimization
source_ids:
  - src-2026-06-05-pguso-agents-from-scratch
  - src-2026-06-22-djfarrelly-agent-loop-architecture
  - src-2026-06-22-alphasignal-agent-skill-optimization
  - src-2026-06-18-alyona-vert-recursive-self-improvement
  - src-2026-07-06-alphasignal-self-improving-harnesses
  - src-2026-08-05-aibuilderclub-agent-skills-best-practices-guide
  - src-2026-08-05-aibuilderclub-google-skills-official-agent-skills-library
  - src-2026-08-05-aibuilderclub-last30days-skill-real-time-research
  - src-2026-08-07-zach-lloyd-computer-use-verification
  - src-2026-08-07-mahesh-sathiamoorthy-rl-environments-agents
  - src-2026-08-17-google-cloud-agent-plugins
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-22-grok-bot-systems-engineering-working-note
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

[[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] sharpens the boundary around "self-improving" language. Optimizing a skill file is workflow-level self-improvement: the agent's procedure improves, but the model-building process has not necessarily improved. Stronger [[Recursive Self-Improvement]] would feed into future AI system creation itself, including training data, model design, evaluation, and post-training recipes.

[[Alpha Signal - Why self-improving harnesses are the next frontier]] extends this from *skill files* to the whole *harness*. **Self-Harness** (Shanghai AI Lab) runs the same trainable-external-state loop at the level of the agent's operating rules — mine execution traces for recurring failures, propose harness/prompt edits, and accept a change only if regression tests confirm it doesn't break previously-passing tasks (33–60% gains on Terminal-Bench-2.0). **HarnessX** (Xiaomi) goes structural: it treats the harness as a pipeline of swappable "processor" modules and uses an RL optimizer (AEGIS) to search combinations while guarding against reward hacking and catastrophic forgetting (Qwen-3.5 9B: 33%→47% on GAIA). Both succeed precisely because they enforce **strict verification gates** rather than "loopmaxxing" — unguided inference in a loop — which is the same discipline the skill-optimization frameworks above rely on. This is the harness-level face of [[Coding Agent Harness]].

### Progressive disclosure and portability

The AI Builder Club skill cluster treats skills as context-efficient packages whose short metadata is always discoverable while full procedures load only when relevant. This progressive disclosure is the main advantage over permanently exposing every instruction or integration.

The collection also cautions against collapsing skills and MCP into one winner. Skills encode procedures and context; MCP standardizes executable tool access. A portable skill can still depend on host-specific hooks, permissions, or tool names, so portability claims need runtime tests rather than file-format compatibility alone.

### Skills need operational verifiers

[[Zach Lloyd - The computer use verification skill that every agent needs]] is a concrete procedural skill with two observable modes—reproduce and verify—and explicit evidence artifacts. [[Mahesh Sathiamoorthy - RL Environments Are All You Need]] supplies the scaling complement: reusable environments and held-out scores can evaluate or optimize skill instructions without trusting the skill's own report.

### From skill file to plugin package

[[Google Cloud - Agent Plugins Are the Future of Agent Skills]] adds a distribution layer above progressive disclosure. An Agent Plugin can bundle several `SKILL.md` procedures, MCP servers, static assets, and client-specific configuration behind one manifest. The useful distinction is:

- a **skill** is a discoverable procedure;
- an **MCP server** exposes executable capabilities;
- a **plugin** packages both for installation and transport.

The draft keeps component failure boundaries separate and distinguishes read-only packaged assets from client-managed persistent state. Portability remains incomplete because authentication and several client extension formats are not standardized; see [[Agent Plugin Architecture]].

### What a high-quality skill contains

[[Grok Bot Systems Engineering Working Note]] is the vault's most specific answer to "what makes a skill good," and it reads as an authoring checklist rather than a definition:

- a **narrow activation condition**, so the skill is not invoked everywhere;
- ordered steps with tool choices and **stop conditions**;
- positive examples demonstrating the desired artifact;
- **anti-patterns** showing common but unacceptable shortcuts;
- acceptance tests the agent can execute without subjective guessing;
- a version number, owner, and date of last verified run.

Its authoring loop — observe failures, write, evaluate, version, deploy — supplies the operational discipline the page's self-improvement section leaves open, and its triage rule is the sharpest formulation in the vault of *when* to reach for a skill at all: when a bot fails, do not add a longer conversational reminder; decide whether the failure belongs in the **skill** (method), the **environment** (access or path), the **verifier** (quality), or a **hard policy** (risk). Only the first is a skill problem. The stated goal is an accumulating operating system rather than a growing pile of prompt history. See [[Agent Workflow Maturity]].

[[Anthropic - The AI-Native SDLC Playbook]] shows the same object doing governance work in an enterprise setting: a `.claude/skills/secure-api-review/SKILL.md` encodes a compliance procedure as a versioned repository artifact, which makes the review reproducible and auditable rather than dependent on who happened to run it. Both sources converge on the same claim — **a skill's value is that it survives the run that produced it**.

## Open questions

- Should "skill" mean the text procedure, the executable workflow, or the bundle of both?
- What governance is needed before agents can safely write, deploy, and revise their own skills?
- How should teams evaluate skill edits so they improve one task without regressing another?
- Can skill libraries become portable across models and harnesses, or will they remain tightly coupled to a specific runtime?
- When is skill optimization merely workflow tuning, and when does it become part of a broader recursive self-improvement loop?
- How many skills can coexist before narrow activation conditions start colliding and retrieval of the right skill becomes its own problem?

## Related pages

- [[Grok Bot Systems Engineering Working Note]]
- [[Anthropic - The AI-Native SDLC Playbook]]
- [[Agent Workflow Maturity]]
- [[AI-Native Software Development Lifecycle]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Agent Planning]]
- [[Context Engineering]]
- [[Tool Use and Function Calling]]
- [[Agent Memory]]
- [[djfarrelly - The Agent Loop Architecture]]
- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[Recursive Self-Improvement]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[pguso - Agents From Scratch]]
- [[Coding Agent Harness]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]
- [[Inngest]]
- [[AI Builder Club - Build AI Agents]]
- [[Loop Engineering]]
- [[Agent Security and Governance]]
- [[Zach Lloyd - The computer use verification skill that every agent needs]]
- [[Mahesh Sathiamoorthy - RL Environments Are All You Need]]
- [[Google Cloud - Agent Plugins Are the Future of Agent Skills]]
- [[Agent Plugin Architecture]]
