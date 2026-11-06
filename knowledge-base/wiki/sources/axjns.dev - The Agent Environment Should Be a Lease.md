---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-axjns-celln-execution-lease
source_title: The Agent Environment Should Be a Lease
source_author: Unattributed in capture
source_url: https://axjns.dev/blog/celln-execution-plane
tags:
  - source/summary
  - sandboxing
  - agent-infrastructure
  - capability-leasing
source_ids:
  - src-2026-11-04-axjns-celln-execution-lease
status: active
---

# The Agent Environment Should Be a Lease

## Summary

The post is subtitled "Why I built Celln, and where I hope it fits beneath Sympozium". It is the
builder's design rationale for [[Celln]]. The thesis is that an agent's execution environment should
be a **lease on capabilities**, not a mutable machine the agent assembles for itself. Under such a
lease, the host lends a task the tools it may run. Each tool is identified by content, supplied
read-only and recorded, and the lease lasts for the lifetime of the execution.

The post places Celln as an execution plane beneath Sympozium, the coordination system developed in
[[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]]. The
contract is small: Sympozium sends an authorised execution request, and Celln returns the outcome,
provenance and an enforcement verdict.

Most of the post lists hard problems, not achievements. These are revocation of authority already
held, dependency closure, long-lived services, and retries. It ends by saying that the performance
claims still have to be earned against prebuilt containers and snapshot VMs.

## Key claims

### Environment preparation is the cost being attacked

- An agent often starts work by finding tools, downloading packages, resolving dependencies and
  discovering its permissions. "Even when the sandbox starts quickly, preparing the environment can
  dominate a short task."
- "Prebuilt images and caches already reduce that work." Celln's question is how to make the
  permitted executable and its dependencies "the unit an operator can inspect, lend, and withdraw".

### Motes, cells and content-identified tools

- A **mote** is "a warm substrate at rest". A **cell** is "a live execution environment with a
  particular set of tools". The host identifies tools by content, supplies them read-only and records
  what each cell received.
- "A path is convenient for finding a program; the content and policy behind it determine what the
  host is authorising."
- The goal is an explainable account of each run:
  - which tools the task received;
  - where it could write;
  - which external permissions it had;
  - what it produced.

  The post adds that this creates obligations to verify bytes, enforce policy and make failures
  visible.

### Reproducible does not mean trusted

- "A model-written program remains untrusted after a successful build." Repeated matching builds are
  evidence of reproducibility. They do not show that the source is benign, that the compiler is
  trustworthy, or that the program "should inherit the permissions of a host-provided tool".
- Generated code runs in a sealed KVM cell with a writable workspace and restricted filesystem and
  network access. "The boundary is the scope of that authority, not a claim that the guest has no
  writable memory or files at all."
- The post calls the boundary demonstration in [[axjns.dev - Testing Celln's Boundary]] "a small
  engineering check, not a complete security evaluation".

### Coordination durable, execution short-lived

- Kubernetes' desired-state model and reconciliation loops remain valuable for coordination. "A pod
  remains a reasonable choice for many workloads", and pods can use read-only root filesystems. The
  concern is narrow: "for bursts of small, generated tasks", a pod per task may be more machinery
  than needed.
- In the proposed integration, Sympozium submits a capability set, limits and an output destination.
  Celln returns the outcome, provenance and enforcement verdict. "Sympozium owns the workflow; the
  executor validates the authority it is given and enforces it locally."

### Where the lease gets difficult

- **Revocation.** Removing a tool from a catalogue prevents future grants. Stopping a running cell
  from using authority it already holds is "a different guarantee". No design can undo an external
  effect that has already happened.
- **Dependencies.** A capability should cover a verified dependency closure, without forcing one
  language. Compatibility, patching and storage still cost something.
- **Long-lived services.** These need stable identity, state, upgrades and availability. They need
  "an explicit lifecycle rather than simply extending a timeout".
- **Retries.** "If an execution request times out, the control plane must learn whether the work ran
  before resubmitting it. A retained receipt and an idempotency contract are as important as a fast
  start."

### Performance must still be earned

- The planned comparison covers cold and warm startup, dependency preparation, memory sharing, total
  task time and revocation behaviour. The baselines are prebuilt containers and snapshot-based VMs.
  "A faster fork is useful only if the rest of the lifecycle preserves the gain."

## Why it matters

- [[Harness State Authority]] gets a concrete seam between durable coordination state and disposable
  execution, with a typed request and response across it.
- [[LLM Application Resilience]] gets the rule that a timed-out execution must be resolved, by
  learning whether it ran, before it is retried.
- [[Agent Security and Governance]] gets two distinctions: reproducibility versus trust, and catalogue
  revocation versus in-flight revocation.

## Tensions / open questions

- This is a first-party design essay by the system's builder. It reports no performance measurement,
  and the only cited evidence is the author's own small demonstration.
- The post concedes that prebuilt images, caches and read-only pods already address much of the
  problem. The advantage claimed is explicitness, and that is still a hypothesis.
- The post names the revocation semantics for in-flight cells and the long-lived-service lifecycle as
  open problems. It specifies neither.

## Affected pages

- [[Celln]]
- [[Harness State Authority]]
- [[LLM Application Resilience]]
- [[Agent Security and Governance]]

## Raw capture

- [[knowledge-base/raw/sources/The Agent Environment Should Be a Lease]]

## Citations

- Canonical URL: https://axjns.dev/blog/celln-execution-plane
- Site: axjns.dev. The capture names no author and gives no publication date. The post is written in
  the first person by Celln's builder, and the repository is `sympozium-ai/celln`. The sibling
  benchmark post carries an Alex Jones byline, but this capture does not, so no author is assigned.
- Captured: 2026-11-04.

## Related pages

- [[axjns.dev - Testing Celln's Boundary]]
- [[axjns.dev - Post-Kubernetes Infrastructure for GenAI Workloads]]
- [[axjns.dev - The Synthetic Membrane - A Coordination Layer for Multi-Agent AI Systems]]
- [[axjns.dev - Agents Need Somewhere to Share Their Work]]
- [[axjns.dev - The Sticky-Note Problem]]
- [[Celln]]
- [[Harness State Authority]]
- [[LLM Application Resilience]]
- [[Agent Security and Governance]]
- [[Multi-Tenant Agent Architecture]]
