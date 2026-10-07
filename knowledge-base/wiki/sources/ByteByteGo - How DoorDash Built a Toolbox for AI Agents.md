---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-09-30-bytebytego-doordash-agent-gateway
source_title: "How DoorDash Built a Toolbox for AI Agents"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-doordash-built-a-toolbox-for
tags: [source/summary, mcp, tool-use, security, observability]
source_ids: [src-2026-09-30-bytebytego-doordash-agent-gateway]
status: active
---

# ByteByteGo - How DoorDash Built a Toolbox for AI Agents

## Summary

ByteByteGo explains DoorDash's Agent Gateway as shared infrastructure for discovering, governing,
and invoking tools. A registry/control plane describes capabilities and ownership; proxy/data
planes enforce calls. The article is secondary reporting, not a DoorDash-authored evaluation or an
independently measured account of adoption.

## Key claims

- Internal and external proxy planes have different trust boundaries. A common client interface
  does not erase the difference between company services and third-party tools.
- Authentication, authorization, and credential injection are separate steps. The four credential
  patterns are internal identity, gateway-held tokens, per-user OAuth, and service principals.
- Tool bundles and filters curate `tools/list` for a task. Visibility in that list is **not**
  authorization to execute: `tools/call` must recheck policy.
- Clients supporting elicitation can pause and resume a workflow for OAuth. Other clients receive a
  structured authorization-required result with a connection URL; unavailable authorization is
  not represented as a successful empty tool response.
- Gateway events retain agent, user, tool, bundle, and owner identity, along with the policy
  decision, error origin, timing, and payload sizes. Those fields help distinguish a denied call
  from an upstream tool failure.
- The account reports **200+ servers**, **30+ agents/services**, **thousands of employees**, and
  **millions of weekly tool calls**. These are attributed adoption figures, not a controlled
  measure of productivity or reliability.
- Cryptographic per-agent identities with short-lived user-agent-task-tool-scoped delegation,
  dynamic discovery, and stronger redaction/evaluation are presented as planned improvements.
  They should not all be described as shipped protections.

## Why it matters

The gateway separates three questions often collapsed into "tool access": what the model sees,
what this caller may execute, and which credential the destination receives. That makes roster
curation compatible with a shared integration catalogue without making the catalogue itself an
authorization boundary.

## Tensions / open questions

Centralization creates an enforcement point and a dependency whose failure can affect many agents.
The article does not provide a latency budget, outage analysis, authorization test matrix, or
independent validation of its scale figures. The opening CodeAF advertisement is separate from the
DoorDash case and supplies no evidence about the gateway.

## Affected pages

- [[Model Context Protocol]]
- [[Tool Roster Economics]]
- [[Agent Observability]]
- [[Agent Security and Governance]]
- [[Multi-Tenant Agent Architecture]]
- [[DoorDash]]
- [[ByteByteGo]]

## Raw capture

- [[How DoorDash Built a Toolbox for AI Agents]]

## Citations

- Canonical URL: <https://blog.bytebytego.com/p/how-doordash-built-a-toolbox-for>
- Published September 30 and captured October 1, 2026.

## Related pages

- [[Tool Use and Function Calling]]
- [[Agent Delegation]]
- [[Alex Watson - Add Runtime Controls to AI Agents with NVIDIA OpenShell]]
- [[Adam Faik - How to Build an AI-Native Software Factory]]
