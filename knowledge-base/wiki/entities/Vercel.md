---
type: entity
entity_kind: organization
created: 2026-10-27
updated: 2026-10-27
tags: [entity, organization, ai-agents, agent-harness, durable-execution, infrastructure]
source_ids:
  - src-2026-10-19-vercel-durable-harness
status: active
---

# Vercel

## What it is

Vercel is a cloud platform; in the vault's captured source, agent turns run on its shared serverless
function hosts. That source concerns Vercel's agent-hosting stack: the open-source `durable-harness`
adapters, the Workflow SDK they build on, Vercel Sandbox, and the Agent Runs trace view.

## Why it matters here

[[Pranay Prakash and Eric Dodds - Making Every Harness Durable]] is the vault's first account of
making **existing, unmodified** coding-agent harnesses (Pi, OpenCode, Codex, and Claude Code) crash-safe
from the outside. It contributes three reusable ideas:

- an intent-before, outcome-after log around every model and tool call, which
  [[Harness State Authority]] can treat as an externally applied journal;
- a per-tool replay declaration (`'safe'` versus `'never'`) for interrupted calls, which addresses the
  retry-versus-idempotency tension in [[LLM Application Resilience]];
- a split between the developer's function, which holds credentials and runs custom tools, and a
  per-session virtual workspace or sandbox, which is relevant to [[Multi-Tenant Agent Architecture]].

The Workflow SDK's *World* interface puts storage, a queue, and a stream behind one abstraction, so the
same agent can run on Vercel, local files, Postgres, MongoDB, Redis, or Turso. [[Inngest]] is the vault's
other durable-execution platform for agent loops.

## Boundaries

The capture is a vendor announcement with no measured recovery time, logging overhead, or
failure-injection result. Claude Code and Codex are described as not safe for multi-tenant use, so they
always run in a sandbox; that is a deployment constraint, not evidence of tenant isolation. The
`durable-harness` repository was not inspected.

## Related pages

- [[Pranay Prakash and Eric Dodds - Making Every Harness Durable]]
- [[Harness State Authority]]
- [[LLM Application Resilience]]
- [[Multi-Tenant Agent Architecture]]
- [[Coding Agent Harness]]
- [[AI Agents in Production]]
- [[Inngest]]
- [[E2B]]
