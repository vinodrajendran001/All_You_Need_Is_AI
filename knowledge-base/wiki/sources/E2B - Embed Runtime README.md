---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-10-02-e2b-embed
source_title: "E2B Embed runtime README"
source_author: E2B
source_url: https://github.com/e2b-dev/runtime/tree/main/embed#readme
tags: [source/summary, ai-agents, sandbox, infrastructure, security]
source_ids: [src-2026-10-02-e2b-embed]
status: active
---

# E2B - Embed Runtime README

## Summary

E2B documents Embed as a single-machine deployment of its agent runtime, including control plane,
data plane, storage, and telemetry. The organizational attribution comes from the repository owner;
the clipping has no named author or publication date. The source ID uses its October 2 capture date.
This is a captured README, not an installation report or security assessment.

## Key claims

- Embed exposes the same SDK/API as E2B Cloud while placing the runtime components on one machine.
  The README describes an Apache-2.0 license with no required account or license key.
- Deployment options include Docker Compose, Terraform for GCP/AWS, and Kubernetes.
- Linux hardware virtualization is required. The documented Mac route uses a Linux VM on Apple
  silicon **M3 or later with macOS 15 or later**; it is not a native no-virtualization Mac runtime.
- The service uses **plain HTTP and has no built-in TLS**. The intended environment is inside a
  network, not an unprotected public endpoint.
- The single-node boundary is a design limit. A multi-node private-cloud product is described as
  in development; BYOC and hosted Cloud are separate deployment modes.
- Local storage and telemetry residency do not establish that arbitrary agent workloads make no
  external calls. The README's "nothing leaves the node" framing is an architectural/vendor claim,
  not an independently verified egress guarantee.

## Why it matters

The source adds an execution-placement choice to the harness/engine split: a local sandbox runtime
can retain familiar APIs without being a local language model, a tenant authorization system, or a
complete security perimeter. API compatibility and security equivalence are different properties.

## Tensions / open questions

The capture points at a moving `main` branch rather than a pinned commit. No commands were run,
deployments inspected, or isolation/egress properties tested during ingest. Transport protection,
authentication at exposure boundaries, backups, capacity limits, and workload permissions remain
deployment responsibilities; self-hosting alone does not satisfy them.

## Affected pages

- [[Coding Agent Harness]]
- [[Multi-Tenant Agent Architecture]]
- [[Agent Security and Governance]]
- [[AI Agents in Production]]
- [[E2B]]

## Raw capture

- [[run time embed]]

## Citations

- Canonical URL: <https://github.com/e2b-dev/runtime/tree/main/embed#readme>
- Captured October 2, 2026; publication date unavailable.

## Related pages

- [[Alex Watson - Add Runtime Controls to AI Agents with NVIDIA OpenShell]]
- [[Harness State Authority]]
- [[Agent Observability]]
