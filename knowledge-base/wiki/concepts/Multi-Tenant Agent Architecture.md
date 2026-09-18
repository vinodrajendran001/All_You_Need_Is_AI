---
type: concept
created: 2026-09-18
updated: 2026-09-18
tags: [concept, ai-agents, multi-tenancy, security]
source_ids:
  - src-2026-09-12-cheruku-patel-multitenant-agentic-ai
status: active
---

# Multi-Tenant Agent Architecture

## Definition

Multi-tenant agent architecture applies tenant isolation to systems whose execution paths are chosen
at runtime. Unlike deterministic SaaS, an agent can select tools, spawn sub-agents, retrieve state,
and vary the number of model calls, so tenant identity and authorization must survive every hop.

## Why it matters

Validating a tenant once at ingress is insufficient when a model becomes a confused deputy carrying
valid credentials. Memory, tool selection, database access, delegated credentials, context assembly,
tracing, and cost controls each need an independently testable tenant boundary.

## Current synthesis

[[Nithin Reddy Cheruku and Dhawal Patel - Multi-Tenant Agentic AI with Gemini Enterprise]] separates
four identities: the end user, the agent workload, a delegated/on-behalf-of identity, and the tenant.
The trusted tenant claim should be derived from authentication and signed; a user-supplied tenant
header should never become authority merely because it reached the agent.

The source's three topologies expose the main trade:

| Topology | Isolation mechanism | Main cost |
| --- | --- | --- |
| Pooled | Logical scope, dynamic tool pruning, RLS, delegated credentials | Most controls must be correct at once |
| Sovereign silo | Dedicated runtime, project, memory, tools, data, and keys | Infrastructure and operations per tenant |
| Hybrid bridge | Shared control plane with selected dedicated resources | More routing and policy complexity |

The durable design rule is **component-by-component tiering**. Compute may be pooled while data and
encryption keys are siloed; a dedicated runtime can still use shared ingress and registries. A
platform-wide "tenant mode" is too coarse.

Memory is especially dangerous because scope and lifecycle interact. Session keys need tenant and
user dimensions; retrieved records need the same enforced filter; deletion guarantees depend on
whether encryption keys and storage are actually tenant-specific.

## Open questions

- Which tenant claims can be verified independently at every agent and tool boundary?
- How should traces expose tenant propagation without leaking tenant data into shared observability?
- What tests prove that tool discovery, memory retrieval, and delegated credentials fail closed?
- When does a hybrid topology become harder to audit than a full silo?

## Related pages

- [[Nithin Reddy Cheruku and Dhawal Patel - Multi-Tenant Agentic AI with Gemini Enterprise]]
- [[Agent Security and Governance]]
- [[Agent Memory]]
- [[Agent Delegation]]
- [[Google Cloud]]

