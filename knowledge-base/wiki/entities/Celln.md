---
type: entity
entity_kind: open-source project
created: 2026-11-06
updated: 2026-11-06
tags:
  - entity
  - sandboxing
  - agent-infrastructure
source_ids:
  - src-2026-11-04-axjns-celln-deepseek-benchmark
  - src-2026-11-04-axjns-celln-execution-lease
  - src-2026-11-04-axjns-post-kubernetes-genai
status: active
---

# Celln

## What it is

Celln is an execution plane for agent-generated work. It is hosted in the GitHub repository
`sympozium-ai/celln` and described in a series of posts on axjns.dev.

It runs tasks inside isolated KVM microVMs called **cells**. A **mote** is "a warm substrate at rest";
a cell is "a live execution environment with a particular set of tools". The host lends each cell
the tools it may run. Each tool is identified by content, supplied read-only and recorded, and the
loan lasts only for the lifetime of the execution. Its builder describes this as a **lease on
capabilities**, not a mutable machine the agent assembles.

A cell's lifecycle runs through five stages:

1. build (the "forge");
2. sealing;
3. admission by a component called pilot;
4. execution;
5. teardown.

## Why it matters here

Celln is the execution half of a coordination/execution split that the series argues for.
[[axjns.dev - The Agent Environment Should Be a Lease]] places it beneath Sympozium, the coordination
system that is the intended setting for the synthetic-membrane proposal described in
[[Multi-Agent Coordination]]. The proposed contract is small:

- Sympozium submits an authorised request with a capability set, limits and an output destination.
- Celln returns the outcome, provenance and an enforcement verdict.
- Sympozium owns the workflow, and Celln enforces the authority it is given.

[[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]] frames the same split strategically.
Durable decisions (identity, policy, ownership) stay in a control plane. Short-lived execution takes a
faster launch path. Modal's vendor-reported million-sandbox result is cited as one example of that
direction, not as proof.

That makes Celln a concrete test case for [[Harness State Authority]]. The executor should not own the
workflow, and the workflow should not depend on how a cell starts.

The design rationale also yields several boundary statements that the vault uses in
[[Agent Security and Governance]] and [[LLM Application Resilience]]:

- "A model-written program remains untrusted after a successful build."
- Removing a tool from a catalogue does not revoke authority a running cell already holds.
- A timed-out execution must be resolved, by learning whether it ran, before it is resubmitted.

## Notes

- **Runtime evidence is one small demonstration.** [[axjns.dev - Testing Celln's Boundary]] reports
  four denials and one correct computation from five DeepSeek-generated Rust programs in a single
  retained run. The post itself says three things:
  - The `/etc/passwd` result was a missing file, not a Landlock denial.
  - The `whoami` denial does not identify which control fired, and seccomp cannot match the binary's
    name.
  - A vsock broker remains a channel out of the cell.

  It is "not a VM-escape benchmark", and the demo script's PASS/FAIL heuristic is unreliable.
- **Performance is unmeasured.** Its builder says the planned comparison against prebuilt containers
  and snapshot VMs has still to be run. The only timing is about 3.3 seconds from fork to dissolution,
  "one lifecycle observation".
- **Open design problems are stated, not solved:**
  - in-flight revocation;
  - dependency closure across languages;
  - long-lived services;
  - receipts and idempotency for retries.
- **Authorship.** The benchmark post carries an "Alex Jones" byline, but the other two Celln posts
  carry none.

## Related pages

- [[axjns.dev - The Agent Environment Should Be a Lease]]
- [[axjns.dev - Testing Celln's Boundary]]
- [[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]]
- [[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]]
- [[axjns.dev - Agents Need Somewhere to Share Their Work]]
- [[Harness State Authority]]
- [[Agent Security and Governance]]
- [[LLM Application Resilience]]
- [[Multi-Agent Coordination]]
- [[Multi-Tenant Agent Architecture]]
- [[AI Agents in Production]]
- [[DeepSeek]]
