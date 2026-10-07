---
type: entity
entity_kind: organization
created: 2026-10-07
updated: 2026-10-07
tags: [entity, organization, ai-agents, sandbox, infrastructure]
source_ids:
  - src-2026-10-02-e2b-embed
status: active
---

# E2B

## What it is

E2B provides execution infrastructure for agents. The vault's captured source concerns **Embed**,
a single-machine deployment of the E2B runtime, rather than the language model driving an agent.

## Why it matters here

[[E2B - Embed Runtime README]] describes the cloud-compatible SDK/API with control plane, data
plane, storage, and telemetry on one host. It adds a self-hosted execution option to
[[Coding Agent Harness]] without changing the distinction between model, harness, and sandbox.

The README documents Apache-2.0 licensing and no required account/license key. Its Linux
virtualization requirement, single-node scope, and plain-HTTP/no-built-in-TLS transport are equally
important parts of the deployment contract.

## Boundaries

Local data residency is not an egress policy, API compatibility is not security equivalence, and a
single-node runtime does not implement tenant authorization by itself. The multi-node private-cloud
offering is described as in development. The vault has a README capture, not an executed deployment
or independent isolation assessment.

## Related pages

- [[E2B - Embed Runtime README]]
- [[Coding Agent Harness]]
- [[Multi-Tenant Agent Architecture]]
- [[Agent Security and Governance]]
- [[AI Agents in Production]]
