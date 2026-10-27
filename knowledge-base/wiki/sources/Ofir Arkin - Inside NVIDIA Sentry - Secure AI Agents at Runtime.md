---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-21-nvidia-sentry-runtime
source_title: "Inside NVIDIA Sentry: Secure AI Agents at Runtime"
source_author: Ofir Arkin
source_url: https://developer.nvidia.com/blog/inside-nvidia-sentry-secure-ai-agents-at-runtime/
tags: [source/summary, ai-agents, security, observability, nvidia]
source_ids:
  - src-2026-10-21-nvidia-sentry-runtime
status: active
---

# Ofir Arkin - Inside NVIDIA Sentry - Secure AI Agents at Runtime

## Summary

An NVIDIA Developer Blog post, published 21 October 2026, describing NVIDIA Sentry: a security
framework that monitors AI agents and enforces their access policies from a BlueField-4 data
processing unit (DPU) instead of from the host the agent runs on. Sentry is part of the NVIDIA
OpenShell reference architecture. The premise is the post's first argument: "Monitoring and enforcement
need to operate outside the agent’s reach so that it can’t alter or disable them." Its contribution to
this vault is a concrete placement for that principle: a separate hardware trust domain that sits on the
agent's network path, inspects its traffic, reads host memory from outside, and keeps the activity
record where the agent cannot edit it.

This is a vendor architecture description of a product that has not shipped. The post closes by pointing
readers to existing DOCA libraries "ahead of NVIDIA Sentry’s planned availability early next year." It
reports no evaluation: no detection rate, false-positive rate, latency distribution, or overhead.

## Key claims

**Enforcement sits on the network path, outside the host.** In the reference architecture, agents run
on NVIDIA Vera CPUs "while BlueField-4 sits on the node’s only path to the model". Agent traffic reaches
the DPU "through a direct network I/O path that bypasses host OS/hypervisor packet processing." Sentry is
described as "Trusted even when host resources can’t be trusted".

**A firewall, a proxy, then a policy engine.** DOCA Flow implements a per-agent layer-4 firewall that
blocks unauthorized destinations and forwards permitted traffic to DOCA Tower, an Envoy-based transparent
proxy that performs layer-7 inspection and authorization. Tower terminates TLS, but decryption applies
"For connections configured for inspection". Open Policy Agent (OPA), using the Rego policy language,
evaluates access requests; the vendor says OPA "can evaluate requests in under a millisecond, depending
on policy complexity and configuration." No measurement accompanies that figure.

**Runtime context comes from reading host memory.** DOCA Argus uses "live memory introspection to
analyze selected regions of volatile host memory" without software installed on the host. It maps
containers to pods and sandboxes to microVMs, and records processes, threads, file access, network
connections, and loaded libraries, tracking containers, processes, and libraries by hash. A network
policy can then require, for example, that a container's hash be on an approved list and that the
initiating process appear in the container's software bill of materials (SBOM) with an approved execution
path and command-line arguments.

**Containment is claimed, not measured.** Warning signs include unapproved tools, `ptrace` attacks,
excessive outbound traffic, unauthorized file access, CPU spikes, excessive writes to temporary folders,
and large-scale deletion. On a deviation, Sentry "can request millisecond-scale in-silicon containment";
elsewhere it "can contain and quarantine agents within milliseconds" without the agent's or host's
cooperation. Neither statement comes with a test setup or result.

**Content controls apply in both directions.** Tower applies IP, URL, and protocol restrictions; governs
agent-to-agent (A2A) and Model Context Protocol (MCP) traffic; detects and redacts personal data and
secrets such as API keys, tokens, and passwords; and blocks content prohibited by policy. Specialized
models running locally or on separate GPU systems classify behavior "using tool calls and available
reasoning traces", either inline, where they can block, or out of band, where they trigger a response
afterwards.

**The record is kept where the agent cannot change it.** Tower records inspected communications and
policy decisions on the DPU, Argus adds independently observed runtime signals, and BlueField-4 attests
the telemetry: "An agent that changes a log inside its own environment cannot make the same change to the
protected record maintained on BlueField-4." Workload identity comes from SPIFFE/SPIRE, and the telemetry
can be exported to XDR and SIEM platforms and security data lakes.

**A second layer, not a replacement.** "Software runtime boundaries remain essential." OpenShell governs
what an agent can do; Sentry adds an out-of-band safeguard, with the claim that "Even if an agent escapes
its sandbox, NVIDIA Sentry retains its monitoring and enforcement capabilities".

## Why it matters

[[Agent Security and Governance]] already records OpenShell's rule that enforcement must sit outside the
workload it governs. Sentry pushes the same rule one level lower, outside the host's software altogether,
and makes the precondition visible: the guarantee holds only while the DPU really is the agent's only
path to models and the outside world.

[[Agent Observability]] gains a property it rarely discusses: who can edit the trace. A log written inside
the agent's environment can be altered by a compromised agent. Keeping the record on separate hardware,
with attested provenance, is the vendor's answer for incident investigation.

## Tensions / open questions

- **No evaluation of any kind.** The sub-millisecond policy evaluation and the millisecond containment are
  vendor statements without a test setup, latency distribution, or baseline. There is no detection rate,
  false-positive rate, attack corpus, or resource overhead.
- **Not yet available.** Availability is planned for "early next year"; for now, only DOCA building
  blocks (DOCA Argus, DOCA Flow, and OVS-DOCA) are offered for experimentation.
- **The only-path guarantee is a topology claim.** It holds in the reference architecture. The post does
  not discuss deployments in which an agent has another route out, nor a threat model in which the DPU,
  its firmware, or the policy engine is compromised.
- **Visibility is partial by design.** Argus reads "selected regions" of memory, TLS is decrypted only for
  configured connections, and reasoning traces are analyzed only where "available". The plugin that
  exposes communications for reasoning-trace analysis is planned, not shipped.
- **Classifiers judge intent without published accuracy.** Behavioral drift is classified by unnamed
  specialized models. Their errors decide both missed attacks and blocked legitimate work, and neither
  rate is given.

## Affected pages

- [[Agent Security and Governance]]
- [[Agent Observability]]
- [[NVIDIA]]

## Raw capture

- [[Inside NVIDIA Sentry Secure AI Agents at Runtime]]

## Citations

- Canonical URL: https://developer.nvidia.com/blog/inside-nvidia-sentry-secure-ai-agents-at-runtime/
  (email tracking parameters removed).
- Published 21 October 2026 on the NVIDIA Developer Blog; the byline comes from the clipping's
  frontmatter. Figures are image-only, and only their captions were captured.

## Related pages

- [[Agent Security and Governance]]
- [[Agent Observability]]
- [[Multi-Tenant Agent Architecture]]
- [[Model Context Protocol]]
- [[AI Agents in Production]]
- [[Alex Watson - Add Runtime Controls to AI Agents with NVIDIA OpenShell]]
- [[NVIDIA]]
- [[AI Knowledge Base Overview]]
