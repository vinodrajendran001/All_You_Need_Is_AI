---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-09-28-watson-nvidia-openshell-runtime-controls
source_title: "Add Runtime Controls to AI Agents with NVIDIA OpenShell"
source_author: Alex Watson
source_url: https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/
tags: [source/summary, ai-agents, security, governance]
source_ids: [src-2026-09-28-watson-nvidia-openshell-runtime-controls]
status: active
---

# Alex Watson - Add Runtime Controls to AI Agents with NVIDIA OpenShell

## Summary

NVIDIA's first-party account of OpenShell 0.1.0 places enforceable policy outside the agent workload.
The agent may choose a plan, but the surrounding runtime constrains filesystem access, processes,
network operations, and credential use. The useful contribution is a concrete separation between
proposing an action and possessing authority to execute it.

## Key claims

- The **gateway** manages sandbox lifecycle and policy. A **supervisor outside the workload** checks
  outbound traffic. The **sandbox** enforces filesystem/process restrictions and routes network
  traffic through that supervisor.
- Configured application-layer inspection can distinguish operations sharing an endpoint, including
  HTTP reads versus writes, GraphQL operations, and MCP calls. An allowed host is not automatically
  permission for every operation on that host.
- YAML policy is compiled into OPA/Rego rules, with audit events in Open Cybersecurity Schema
  Framework (OCSF) format.
- Workloads use placeholder credentials; real credentials are substituted outside the workload for
  allowed endpoints. Both network policy and the credential binding must permit the request.
- Network policy can be updated live. Filesystem and process-policy changes require a new sandbox;
  "dynamic policy" does not mean every boundary can change in place.
- Agent-proposed policy changes are pending human review by default. The requesting agent cannot
  approve its own expansion of authority.
- A formal prover checks modeled permissions against an operator-defined boundary. It establishes
  properties of that model, not universal safety of an agent or all reachable services.
- NVIDIA reports no protected-repository writes during adversarial tests lasting up to two hours.
  The article gives no trial count, so this cannot be converted into a general zero-failure rate.

## Why it matters

OpenShell makes the vault's "policy outside the component it constrains" principle concrete. It also
shows why credential injection, network authorization, and process isolation are distinct controls
that must agree, rather than alternative ways of expressing one permission.

## Tensions / open questions

This is vendor documentation and vendor-reported testing, not an independent containment audit.
Proof strength depends on the modeled boundary and the implementation matching it. Composed
permissions across cooperating agents are described as ongoing work, not a solved property of
OpenShell 0.1.0. The clipping damages some YAML and command formatting; examples were not executed
and should not be copied as verified configuration.

## Affected pages

- [[Agent Security and Governance]]
- [[Coding Agent Harness]]
- [[Multi-Tenant Agent Architecture]]
- [[NVIDIA]]

## Raw capture

- [[Add Runtime Controls to AI Agents with NVIDIA OpenShell]]

## Citations

- Canonical URL: <https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/>
- Published September 28 and captured October 5, 2026.

## Related pages

- [[Tanya Lenz - Building a Memory-Driven Agent with NVIDIA NemoClaw]]
- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[E2B - Embed Runtime README]]
- [[Agent Delegation]]
