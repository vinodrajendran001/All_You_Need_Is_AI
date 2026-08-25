---
type: concept
created: 2026-07-03
updated: 2026-08-25
tags:
  - concept
  - coding-agents
  - local-llm
  - tooling
  - agents
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

## Open questions

- How should local harness evaluation move beyond task-success rate to capture code quality and readability, which are hard to score automatically?
- As open-weight models keep improving, does the harness become the dominant differentiator — and will harness token efficiency matter more than model choice?
- What is the right default sandboxing and permission model for agents that run untrusted repositories?

## Related pages

- [[Sebastian Raschka - Using Local Coding Agents]]
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
