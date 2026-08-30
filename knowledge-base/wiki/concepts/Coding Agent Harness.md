---
type: concept
created: 2026-07-03
updated: 2026-08-30
tags:
  - concept
  - coding-agents
  - local-llm
  - tooling
  - ai-agents
source_ids:
  - src-2026-07-03-sebastian-raschka-local-coding-agents
  - src-2026-07-06-alphasignal-self-improving-harnesses
  - src-2026-08-05-aibuilderclub-harness-six-components
  - src-2026-08-05-aibuilderclub-pi-agent-extensions-guide
  - src-2026-08-05-aibuilderclub-harness-engineering-agent-production-guide
  - src-2026-08-05-aibuilderclub-yc-qm-agent-harness-source-read
  - src-2026-08-07-paul-iusztin-bare-bones-coding-agent-loop
  - src-2026-08-07-zach-lloyd-computer-use-verification
  - src-2026-08-07-avi-chawla-claude-code-cost
  - src-2026-08-12-alyona-vert-agent-frameworks-sdks
  - src-2026-08-21-anthropic-ai-native-sdlc
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
  - src-2026-07-16-lilian-weng-harness-engineering
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
  - src-2026-08-30-addy-osmani-audit-agent-files
status: active
---

# Coding Agent Harness

## Definition

A coding agent harness is the operating environment wrapped around a language model that turns raw text generation into real software work: it lets the model read files, make edits, run commands, and verify changes, while enforcing an approval/permission model around those actions. The harness (e.g., Claude Code, Codex CLI, Qwen-Code, Cline) is a separate layer from the **engine** — the LLM that supplies reasoning and code generation.

## Why it matters

The harness/engine split reframes several practical questions. A capable model is necessary but not sufficient; the harness decides what the model can touch, how much context it re-feeds each turn, and how safe it is to run on your machine. Because open-weight models in the 30–35B range are now "good enough" for much coding work, the harness — not just the model — becomes the main design choice, and running one locally shifts the burden onto **serving, permissions, and evaluation** rather than API access.

## Current synthesis

[[Sebastian Raschka - Using Local Coding Agents]] is the vault's anchor source for building a fully local stack.

### The two layers

- **Engine (LLM):** reasoning and code generation. Locally this is an open-weight model — [[Mixture of Experts|MoE]] models such as Qwen3.6 35B-A3B, North Mini Code, or Nemotron 3 Nano — served by an inference runtime (Ollama, LM Studio, vLLM, SGLang, MLX). Ollama's OpenAI-compatible endpoint (`:11434/v1`) lets any OpenAI-style harness connect. This is the same [[Small Language Models|small/on-device model]] and [[On-Device Reasoning]] territory, viewed from the coding-agent side.
- **Harness:** the operating environment (read/edit/run/verify) plus an approval model. It is far more capable — and riskier — than the LLM alone because it touches files and the shell. This is the concrete, product-facing instance of the [[Agentic Loop]] and often hosts reusable [[Agent Skill|skills]], [[Tool Use and Function Calling|tool calls]], and [[Model Context Protocol|MCP]] integrations.

### Choosing and assessing a local setup

- **Speed and memory first:** agentic coding demands stable tokens/sec and bounded memory over *long* contexts (unlike chatbots). ~20–30 tok/sec is comfortable; a 30–35B model needs ~30 GB for a 50k-token context.
- **Capability with personal task packs:** small task sets that reflect your real work beat leaderboard numbers, whose weightings drift over time.
- **Model↔harness pairing matters less than assumed.** Models are nominally optimised for a sibling harness (Qwen ↔ Qwen-Code), but a model can perform *better* in another harness (Qwen3.6 under Codex), so muscle memory is a legitimate deciding factor.

### Token economics is a harness property

- Across models, **the harness dominates token usage**, not the LLM. Claude Code uses the most (mostly *input* tokens from re-feeding history and tool output across turns); Codex the least. Equal task success at half the tokens is roughly twice as fast — a practical extension of [[Model Routing]] and [[Context Engineering]] economics.

### Security posture for locally-run agents

- A harness can read data and manipulate files, so **audit before running**: install/lifecycle hooks, shell execution, file/secret boundaries, MCP/plugins, network calls/telemetry, and update mechanisms. Even with a local model, harnesses can send telemetry/metadata (session IDs, tool metadata) to remote endpoints unless disabled.
- **Reduce blast radius:** sandbox on separate hardware, a VM, or a dedicated user account; treat untrusted repos as hostile (prompt-injection surface via repo instructions and tool output); disable telemetry/auto-update in config. Proprietary harnesses (Claude Code) are harder to inspect than open-source ones (Codex, Qwen-Code).

### Self-improving harnesses

The harness is increasingly something the AI optimizes, not just something a developer writes. [[Alpha Signal - Why self-improving harnesses are the next frontier]] profiles two systems: **Self-Harness** (Shanghai AI Lab) mines execution traces for recurring failures, proposes rule/prompt edits, and keeps only changes that pass regression tests (33–60% gains on Terminal-Bench-2.0); **HarnessX** (Xiaomi) treats the harness as swappable "processor" modules and uses an RL optimizer (AEGIS) to search structural combinations while guarding against reward hacking and catastrophic forgetting (Qwen-3.5 9B: 33%→47% on GAIA, letting a small model punch above its weight). Both are **loop engineering** with strict verification gates — the durable point is that the leverage shifts from writing the harness to designing the instrumentation and gates that let it safely rewrite itself. This is [[Recursive Self-Improvement|workflow-level self-improvement]] (the procedure improves, not the base model) and it overlaps the skill-optimization loops on [[Agent Skill]].

### Six production responsibilities

[[AI Builder Club - The 6 Components of a Production Agent Harness]] decomposes the broad harness layer into context management, tools, orchestration, state and memory, evaluation and observability, and constraints and recovery. This makes the harness a failure-diagnosis map: repeated rediscovery points to memory, incomplete work to orchestration, silent wrongness to evaluation, and fragile retries to recovery.

The collection's source reads and extension guides reinforce a security tradeoff. Hooks, plugins, extensions, and MCP servers can improve the harness without changing the model, but each also becomes executable supply-chain input that needs versioning, permission limits, and regression checks.

### Steering boundaries, behavioral proof, and cost

[[Paul Iusztin - The Bare-Bones Coding Agent Loop]] adds implementation detail for an interactive harness: steering, follow-up, and abort inputs should be queued separately and injected only at safe model-request or would-stop boundaries. Typed events decouple tools from the terminal, approval requests pause and resume the loop, and append-only JSONL preserves inspectable session state.

[[Zach Lloyd - The computer use verification skill that every agent needs]] adds computer use as a harness capability shared by triage, implementation, and review skills. It turns acceptance criteria into behavioral evidence, while [[Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]] shows the economic cost of every harness choice: tool schemas, instruction files, results, memory, and prior turns are repeatedly reprocessed.

[[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]] maps this design space to concrete runtimes. The durable selection rule is to choose by control flow, durability, language, data plane, modality, governance, and abstraction cost—not by feature count alone. See [[Agent Frameworks]].

### The harness is also an organizational surface

[[Anthropic - The AI-Native SDLC Playbook]] adds a layer this page has not covered: what the harness looks like when a *company* rather than an individual owns it. The same primitives take on governance roles.

- `CLAUDE.md` stops being a convenience file and becomes **versioned institutional knowledge** — commands, conventions, architecture, and an explicit "things Claude gets wrong" section — reviewed and owned like any other artifact.
- **Hooks are enforcement, not ergonomics.** The same mechanism that enforces conventions at build time gates production deploys behind a named release authorization, which moves policy from review-time documentation into act-time execution.
- **Plan mode becomes the default entry point**, with the resulting `plan.md` (files that change, order of work, risks, proof) committed as the artifact that triggers implementation.
- **Subagents and parallel sessions** get a named verifier role (`.claude/agents/verifier.md`), separating the agent that produced work from the agent that checks it.
- **Review instructions are themselves a committed file.** A `REVIEW.md` defining passes, what "important" means, a nit cap, and a do-not-report list makes agentic review auditable and tunable rather than a prompt someone typed.

The consequence for harness selection: token efficiency and permission model are no longer the only differentiators. **Whether a harness can express policy as executable, version-controlled configuration** becomes decisive at organizational scale. See [[AI-Native Software Development Lifecycle]].

## The action space is an optimization surface

[[Alex L. Zhang - Speculative Programmatic Tool Calling]] adds a dimension this page has treated as fixed: what the harness *does with the tokens while they are still arriving*. Most harnesses wait for a complete generation before executing anything — a habit inherited from JSON tool calling, where the wait cost little. When the action space is code ([[Programmatic Tool Calling]]), a harness can parse tool calls out of the partial program and pre-launch them, so the calls have already run by the time the finished program reaches them.

The reported gains are modest, roughly 1–1.2×, and the author is candid that they depend entirely on tool latency and trajectory. The more durable point is architectural: **a harness that treats a generation as an opaque blob until it completes is leaving a compiler's worth of optimization on the table.** [[Speculative Tool Execution]] covers the mechanism, including the shadow-REPL design that keeps partial execution from mutating real state, and the governance gap it leaves open — purity is analysed, authority is not.

## Harnesses as training infrastructure

[[IBM Granite Team - Granite 4.2 LLMs How They're Built]] shows coding harnesses being used for
something this page has not covered: **generating and executing training data**, not just serving
users at inference time.

Granite's agentic SFT trajectories were deliberately produced across a wide spread of harnesses —
OpenHands, OpenCode, Terminus-2, SWE-agent, OpenResearcher, MiniSWE, OpenSeeker, EnvScaler, Gemini
CLI, Hermes, Codex, and Goose — rather than standardizing on one. Harness diversity is treated as a
form of data augmentation: a model trained on trajectories from a dozen scaffolds should be less
overfit to any single one's prompt conventions, tool schemas, and turn structure.

The agentic RL stages then run *inside* harnesses too. The SWE stage drives OpenHands over real
repositories in per-repo container images, rewarded on hidden tests; the terminal stage runs Harbor /
Terminus-2 over a live shell with rollouts spanning up to 64 environment turns.

This inverts the usual relationship. This page has treated the harness as the layer that adapts a
fixed model to a task; here the harness is the environment the model is *shaped by*. It also raises a
coupling question the source does not address: a model post-trained through OpenHands has been
optimized against that harness's specific action space and observation format, so harness-diverse
training data may be less about robustness than about avoiding a dependency that would otherwise be
baked in at RL time.

## The harness as an optimization ladder

[[Lilian Weng - Harness Engineering for Self-Improvement]] recasts the harness as a search space with
five rungs, ordered by how much of the system an optimizer may rewrite: **prompts, structured context,
workflow, harness code, optimizer code**. Each rung subsumes the ones below and enlarges the space,
so higher rungs promise more headroom while making evaluation and safety harder. Her operating-system
analogy is the compact version: the model is the CPU, the harness is the OS deciding what the CPU sees
and what it is allowed to do. [[Harness Optimization]] develops the ladder in full.

Three recurring design patterns fall out of it: **workflow automation** (turning a repeated manual
sequence into a durable procedure), **the file system as persistent memory** (writing state to disk
rather than holding it in context), and **sub-agents or backend jobs** (isolating work so it does not
contaminate the parent context).

## How much of itself should a harness let an agent rewrite?

[[Philipp Schmid - Recursive Self-Improvement]] ranks current harnesses by rewritable surface, and the
ranking doubles as a risk ladder:

| Posture | Systems | What the agent may change |
| --- | --- | --- |
| **Conservative** | Claude Code, Codex, Cursor | Skills, hooks, and plugins extend a fixed core |
| **Minimal core** | Pi | Four built-in tools (`read`, `write`, `edit`, `bash`) and a system prompt under 1,000 tokens; everything else is a TypeScript extension auto-discovered from `.pi/extensions/`, writable and reloadable mid-session |
| **Plugin kernel** | DeepSeek Harness (Cordis) | Models, tools, sessions, sandboxes, and the control loop itself are swappable; plugin side effects unwind on unload so the runtime can replace parts of itself without dying |

Schmid's shorthand for the DeepSeek position is `Agent = Model + Harness`. The trade is explicit: more
rewritable surface means capability the developers did not predict, and more ways to break
compatibility or quietly weaken a permission boundary. It also makes failures persistent — a bad edit
survives the session that made it. See [[Agent Plugin Architecture]].

A second, quieter benefit of code-extensible harnesses: code can run a sequence of operations
**without filling the context window with every intermediate result**, which is the same argument
[[Programmatic Tool Calling]] makes from the tool side.

## The instructions in the harness may not be doing much

[[Addy Osmani - Audit your Agent files]] is the strongest counter-evidence in this vault to the
assumption that a richer harness configuration is a better one. A study of **288 runs across 17
tasks** found that the presence of `AGENTS.md` / `CLAUDE.md` made **no clear difference to
correctness** — it changed *how* agents worked (more targeted tests) without moving the outcome.
Anthropic removed **more than 80%** of Claude Code's system prompt with **no measurable eval loss**.
A survey of 100 repositories found lint leakage in 62%, context bloat in 42%, and skill leakage in 35%.

Osmani's framing is that agent configuration **has a half-life**: rules written for a model that
needed them survive into a model that does not, consuming context and constraining behaviour without
anyone re-testing them. The operational consequence for harness design is that instruction files need
the same regression discipline as harness code — justify against an eval, and delete what cannot be
justified.

## Open questions

- How should local harness evaluation move beyond task-success rate to capture code quality and readability, which are hard to score automatically?
- As open-weight models keep improving, does the harness become the dominant differentiator — and will harness token efficiency matter more than model choice?
- What is the right default sandboxing and permission model for agents that run untrusted repositories?
- If hooks and skills encode policy, who reviews the guardrails, and what prevents an agent from editing the file that constrains it?

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[Agentic Reinforcement Learning]]
- [[Sebastian Raschka - Using Local Coding Agents]]
- [[Anthropic - The AI-Native SDLC Playbook]]
- [[AI-Native Software Development Lifecycle]]
- [[Anthropic]]
- [[Agentic Loop]]
- [[Agent Skill]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[Mixture of Experts]]
- [[Model Routing]]
- [[Context Engineering]]
- [[AI Agents in Production]]
- [[Agent Skill]]
- [[Recursive Self-Improvement]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]
- [[Sebastian Raschka]]
- [[AI Knowledge Base Overview]]
- [[Loop Engineering]]
- [[Graph Engineering]]
- [[Agent Security and Governance]]
- [[AI Builder Club - Build AI Agents]]
- [[Paul Iusztin - The Bare-Bones Coding Agent Loop]]
- [[Zach Lloyd - The computer use verification skill that every agent needs]]
- [[Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]]
- [[Agent Frameworks]]
- [[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]]
- [[Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[Harness Optimization]]
- [[Lilian Weng]]
- [[Philipp Schmid]]
- [[Addy Osmani]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Addy Osmani - Audit your Agent files]]
