---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-12-cheruku-patel-multitenant-agentic-ai
source_title: "Building Multi-tenant Agentic AI systems using Gemini Enterprise Agent Platform for B2B SaaS"
source_author:
  - Nithin Reddy Cheruku
  - Dhawal Patel
source_url: https://medium.com/google-cloud/building-multi-tenant-agentic-ai-systems-using-gemini-enterprise-agent-platform-for-b2b-saas-5075a8dfd1db
tags: [source/summary, multi-tenancy, ai-agents, security]
source_ids: [src-2026-09-12-cheruku-patel-multitenant-agentic-ai]
status: active
---

# Nithin Reddy Cheruku and Dhawal Patel - Multi-Tenant Agentic AI with Gemini Enterprise

## Summary

This Google Cloud architecture guide argues that agentic B2B SaaS must carry verified tenant context
through every dynamically chosen hop: planner, sub-agent, memory, tool, database, model call, and trace.
It distinguishes user, agent, delegated, and tenant identities, then maps three deployment topologies:
pooled infrastructure for standard tenants, sovereign per-tenant silos, and a hybrid bridge.

## Key claims

- Tenant identity should be bound to the authenticated subject in signed claims; untrusted tenant
  headers should be stripped and replaced.
- RFC 8693 token exchange can produce target-specific, downscoped credentials with an actor claim;
  DPoP or workload identities can bind credentials to a runtime.
- A pooled runtime's shared workload identity does **not** enforce tenant isolation. Exact memory
  scopes, composite session keys, dynamic tool pruning, delegated credentials, gateway policy, and
  database row-level security must carry the boundary.
- The pool/silo decision is component-specific. Compute can be shared while memory, tools, data, or
  encryption keys remain dedicated.

## Why it matters

Multi-tenancy is not one platform switch once an agent chooses its own path. Isolation becomes an
invariant propagated across identity, state, tools, storage, context, credentials, policy, and
observability.

## Tensions and caveats

- This is vendor-authored prescriptive architecture, not measured evidence of zero leakage,
  compliance, latency, or unit economics.
- The source appears inconsistent on whether pooled managed memory can provide tenant-specific CMEK:
  it describes tenant-isolated partitions, then says true per-tenant key isolation requires a
  dedicated project and Agent Engine resource.
- Product capabilities and pre-GA boundaries need current documentation before implementation.

## Raw capture

- [[2026-09-12 Nithin Reddy Cheruku and Dhawal Patel - Multi-Tenant Agentic AI with Gemini Enterprise]]

## Affected pages

- [[Multi-Tenant Agent Architecture]]
- [[Agent Security and Governance]]
- [[Agent Memory]]
- [[Google Cloud]]

## Related pages

- [[AI Agents in Production]]
- [[Agent Delegation]]
- [[Model Context Protocol]]

