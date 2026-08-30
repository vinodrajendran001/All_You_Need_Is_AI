---
type: concept
created: 2026-08-24
updated: 2026-08-30
tags: [concept, ai-agents, plugins, interoperability]
source_ids:
  - src-2026-08-17-google-cloud-agent-plugins
  - src-2026-08-20-jeremy-morrell-extensible-software
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
status: active
---

# Agent Plugin Architecture

## Definition

Agent plugin architecture is a packaging and isolation pattern for distributing agent instructions, executable tools, assets, and client configuration as one installable unit while retaining explicit component boundaries.

## Current synthesis

[[Google Cloud - Agent Plugins Are the Future of Agent Skills]] proposes a portable directory containing:

- a manifest for identity, discovery, and compatibility;
- one or more [[Agent Skill|skills]] expressed as `SKILL.md` procedures;
- [[Model Context Protocol|MCP]] server definitions for executable tools;
- read-only packaged assets and client-managed persistent data;
- optional configuration for hosts that have not standardized their extension points.

This resolves a layer mismatch: skills describe how to work, while MCP exposes what can be executed. A plugin transports both. Robust implementations should validate the manifest strictly but isolate failures so one invalid server does not erase valid skills.

[[Jeremy Morrell - Extensible Software in the Age of LLMs]] generalizes the same idea to generated application extensions. A trusted host owns identity, storage, routing, and privileged capabilities; generated workers run behind a narrow RPC boundary. The common principle is capability-oriented composition under zero trust.

## Limits

Portability remains partial. Authentication, browser extensions, hooks, commands, and permission semantics still vary by client. A common folder layout does not prove behavioral compatibility or security.

## How far the plugin boundary can move

[[Philipp Schmid - Recursive Self-Improvement]] ranks three harness postures by how much of the system
is expressed as a plugin, and the ranking is effectively a spectrum from "extension points" to "there
is no core."

- **Fixed core with extension points** — Claude Code, Codex, Cursor. Skills, hooks, and plugins extend
  a core the agent cannot reach.
- **Minimal core** — Pi ships four built-in tools (`read`, `write`, `edit`, `bash`) and a system
  prompt under 1,000 tokens. Everything else is a TypeScript extension auto-discovered from
  `.pi/extensions/`, which **an agent can write, reload, and continue with mid-session**. Amp takes a
  related path by storing project plugins with the codebase.
- **Plugin kernel** — DeepSeek Harness, built on the Cordis kernel, treats models, tools, sessions,
  sandboxes, and **the control loop itself** as replaceable. Its key engineering property is that
  **plugin side effects unwind on unload**, so the runtime can swap parts of itself without dying.

That unload-safety property is what makes the extreme position viable at all: hot-swapping the control
loop is only survivable if partially-applied changes can be reversed cleanly.

The cost is symmetric with the benefit. An agent that can author its own extensions can build
capabilities its developers did not predict — and can break compatibility or weaken a permission
boundary, with effects that persist past the session that introduced them. This is the same tension
[[Harness Optimization]] records between search-space size and safety.

## Related pages

- [[Agent Skill]]
- [[Model Context Protocol]]
- [[Tool Use and Function Calling]]
- [[Agent Security and Governance]]
- [[LLM-Native Extensible Software]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Philipp Schmid]]
- [[Philipp Schmid - Recursive Self-Improvement]]
