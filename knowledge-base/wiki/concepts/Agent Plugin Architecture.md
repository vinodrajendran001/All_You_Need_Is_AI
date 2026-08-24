---
type: concept
created: 2026-08-24
updated: 2026-08-24
tags: [concept, agents, plugins, interoperability]
source_ids:
  - src-2026-08-17-google-cloud-agent-plugins
  - src-2026-08-20-jeremy-morrell-extensible-software
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

## Related pages

- [[Agent Skill]]
- [[Model Context Protocol]]
- [[Tool Use and Function Calling]]
- [[Agent Security and Governance]]
- [[LLM-Native Extensible Software]]

