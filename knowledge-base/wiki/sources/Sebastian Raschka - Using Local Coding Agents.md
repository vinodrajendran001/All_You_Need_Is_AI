---
type: source-summary
created: 2026-07-03
updated: 2026-07-03
source_id: src-2026-07-03-sebastian-raschka-local-coding-agents
source_title: "Using Local Coding Agents"
source_author: Sebastian Raschka
source_url: https://magazine.sebastianraschka.com/p/using-local-coding-agents
tags:
  - source/summary
  - coding-agents
  - local-llm
  - open-weight
  - tooling
source_ids:
  - src-2026-07-03-sebastian-raschka-local-coding-agents
status: active
---

# Sebastian Raschka - Using Local Coding Agents

## Summary

This tutorial walks through building a **fully local coding-agent stack** — an open-weight LLM served locally as the "engine," wrapped in a coding **harness** that reads files, edits, runs commands, and verifies changes — as an alternative to Claude Code / Codex subscriptions. The two-layer mental model (LLM = reasoning/generation; harness = operating environment) organises the whole piece. Motivations are cost predictability, privacy, reproducibility, offline use, and control over an inspectable, modifiable setup.

The concrete path: serve `Qwen3.6 35B-A3B` (or Cohere's North Mini Code) via **Ollama** (OpenAI-compatible endpoint at `:11434/v1`), sanity-check **speed** (>20–30 tok/sec is fine; comparable to GPT-5.5 "high") and **memory** (~30 GB for 50k context) and **capability** (small personal task packs, not just leaderboards), then connect the model to Qwen-Code, Codex CLI, or Claude Code. A recurring theme is **security posture**: audit the harness before running it (data egress, file/secret boundaries, prompt-injection surface), sandbox it, and disable telemetry.

## Key claims

- **Harness vs. engine.** The LLM provides reasoning and code generation; the surrounding harness provides the operating environment (read/edit/run/verify). Harnesses are far more capable — and riskier — than the LLM alone because they touch your files and shell.
- **Local is increasingly viable.** Open-weight MoE models in the 30–35B range (Qwen3.6 35B-A3B, North Mini Code, Nemotron 3 Nano) are "very capable" and often sufficient; they run at GPT-5.5-like token speed on a Mac Mini M4 or DGX Spark. GLM 5.2 is the strongest open-weight model but too large for consumer hardware.
- **Serve with Ollama** for plug-and-play setup across OSes; prefer `*-mlx` model variants on Apple Silicon. Ollama exposes an OpenAI-compatible API, so any OpenAI-style harness can point at it.
- **Assess before committing:** tokens/sec and memory must stay stable over long contexts (agentic workflows, not chatbots); run a small personal task set because standardized benchmark weightings drift over time.
- **Model↔harness pairing matters less than assumed.** Qwen models are optimised for Qwen-Code, but in the author's small benchmark Qwen3.6 actually did *better* under Codex — so sticking with the harness you have muscle memory for is reasonable.
- **Token usage is driven by the harness, not the model.** Claude Code uses by far the most tokens (mostly *input* tokens from re-feeding history/tool-output across turns — one run: ~578k input vs ~4.5k output over 25 turns); Codex the least. Equal task success at half the tokens ≈ roughly twice as fast.
- **Audit locally-run harnesses.** Have a trusted agent review the repo for install/lifecycle hooks, shell execution, file/secret boundaries, MCP/plugins, network calls/telemetry, and update mechanisms. Qwen-Code follows standard practice but can still send telemetry to Alibaba/Aliyun endpoints unless disabled via `~/.qwen/settings.json`; Codex and Claude Code have similar defaults, and Claude Code is proprietary (harder to inspect, sends data to Anthropic and Datadog).
- **Remote model, local harness** works via an SSH tunnel (`ssh -N -L 11434:127.0.0.1:11434 user@DGX`), letting a trusted harness on a Mac use a model hosted on a DGX Spark as if local.

## Why it matters

This is the vault's most concrete treatment of running agents on open-weight models and seeds the [[Coding Agent Harness]] concept — the harness/engine split, local serving, security posture, and harness-driven token economics. It ties the local-model thread ([[Small Language Models]], [[On-Device Reasoning]], [[Mixture of Experts]]) to the agent-tooling thread ([[Agentic Loop]], [[Agent Skill]], [[Tool Use and Function Calling]], [[Model Context Protocol]]). Its "token usage is a harness property" finding is a practical extension of [[Model Routing]] and [[Context Engineering]] economics, and it introduces [[Sebastian Raschka]] as an entity.

## Tensions / open questions

- The benchmarks are deliberately small personal task packs (5-task sets), so success-rate comparisons between models and harnesses are directional, not definitive.
- Task correctness does not measure code quality or readability, which the author flags as hard to assess automatically.
- Model/version names (Qwen3.6, GPT-5.5, GLM 5.2, North Mini Code, Nemotron 3 Nano) and the Polar RL paper are near-future references captured mid-2026; specifics will age quickly even as the workflow stays valid.

## Affected pages

- [[Coding Agent Harness]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[Agentic Loop]]
- [[Model Routing]]
- [[Sebastian Raschka]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/Using Local Coding Agents.md`
- Source URL: [https://magazine.sebastianraschka.com/p/using-local-coding-agents](https://magazine.sebastianraschka.com/p/using-local-coding-agents)

## Related pages

- [[Coding Agent Harness]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[Mixture of Experts]]
- [[Agentic Loop]]
- [[Agent Skill]]
- [[Tool Use and Function Calling]]
- [[Sebastian Raschka]]
- [[AI Knowledge Base Overview]]
