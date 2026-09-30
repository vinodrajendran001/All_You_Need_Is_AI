---
type: concept
created: 2026-09-18
updated: 2026-09-30
tags: [concept, ai-agents, multi-tenancy, security, cost]
source_ids:
  - src-2026-09-12-cheruku-patel-multitenant-agentic-ai
  - src-2026-09-27-fd-agent-muse-compute-demand
  - src-2026-09-29-yoon-multiplayer-ai
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

## The isolation boundary has a price per live tenant, and users start private anyway

Two September 2026 sources add dimensions this page has not costed: what a tenant boundary costs per
live occupant at fleet scale, and which scope users actually choose when a shared one is on offer.

[[FD - Agent Muse Compute Demand]] is a bottom-up **scenario estimate**, not a measurement of Meta's
infrastructure, and its **100M DAU** premise is hypothetical. Under those assumptions the concurrency
chain runs 100M DAU x **two active hours per day** / 24 = **~8M average simultaneous VMs**; a **2.5x
peak-to-average ratio** gives **~20M peak**; **~20% headroom** gives **~25M provisioned live VMs**, or
roughly **25% of DAU live at once**. The per-user sandbox advertises **2 vCPUs, ~8 GB of RAM, and
~100 GB of persistent logical storage**, and the author's central move is to treat those as *logical*
allocations rather than physical reservations. Oversubscription is anchored on DeepSeek's DSec paper -
**~30,000 physical cores**, **250 TB of DRAM**, **~160 nodes**, peak concurrency above **380,000
sandboxes**, about **800 microVMs per node** on roughly **188 physical cores**, or **~0.23 physical
cores per live VM**. Muse is assumed *less* efficient, at **0.3-0.75** with a base case of **0.5**,
giving **12.5M physical cores** (**~50K CPUs** at 256 cores each, **~$800M**). Memory follows a single
observed instance using **~3 GB** of the exposed 8 GB: **75 PB**, with a range of **~75-100 PB** and a
**~$2B** estimate. Every input is assumed rather than measured, the memory figure rests on one
observation, DSec's workload may differ materially from Muse's, and the prices omit networking,
storage, orchestration, redundancy, facilities, cooling, depreciation, and operations.

For this page, the useful part is not the dollar totals but where they sit. The pooled/silo/hybrid
table above prices isolation in operational terms - more controls that must be simultaneously correct,
or more infrastructure per tenant. FD's estimate says the whole sandbox layer that carries that
isolation is **~0.1 GW** against **~1-2 GW** of total average power, because inference dominates
(**50 reasoning-equivalent events per DAU per day** x **5 Wh** = **25 GWh/day**, or **~1.0 GW**). If
that structure holds, the marginal compute cost of a stronger isolation topology is small next to the
model calls either topology makes. The same arithmetic cuts the other way for the isolation argument
itself: *if* the assumed 0.5 physical cores per live VM is anywhere near right, tenants would be
*sharing* cores, and the advertised 2 vCPU allocation would be an accounting unit rather than a
boundary. Component-by-component tiering has to say explicitly which of the two the compute tier is.

[[Jina Yoon - We're Building Multiplayer AI]] comes at tenancy from inside a single organisation, and
its observations are internal product reporting rather than a study. PostHog's Spaces hold people,
agents, and work objects in one container, and artifacts act as portable session-state snapshots - one
session's artifact becomes the next session's context. PostHog reports three recurring Space-**setup**
patterns *"even among just ~200 employees"*; separately, and without a stated population, its early
data says coding was mostly solo, collaboration happened more in GitHub than in the PostHog UI, and
users **overwhelmingly preferred starting tasks privately** despite the team expecting shared-Space
defaults. "Mostly solo" and "overwhelmingly" are unquantified, the context layer had been dogfooded
for only a few weeks at publication, and the findings may depend on PostHog's low-hierarchy culture.

That complicates this page's framing rather than extending it. The tenant boundary here has been drawn
between customers; the boundary users reached for was per-person, *inside* a tenant, which multiplies
scopes without changing the enforcement story - a memory key that carries tenant and user still has to
carry Space and visibility. And the artifact mechanism is exactly the cross-scope hop the page warns
about: a snapshot of one session's state becoming another session's context is a place where the
tenant claim must be re-derived rather than inherited. PostHog calls governance and permissions **one
of its biggest blind spots**, and says it is interviewing users to learn more - which is this page's
entire subject, so the finding is a problem statement rather than a design.

## Open questions

- Which tenant claims can be verified independently at every agent and tool boundary?
- How should traces expose tenant propagation without leaking tenant data into shared observability?
- What tests prove that tool discovery, memory retrieval, and delegated credentials fail closed?
- When does a hybrid topology become harder to audit than a full silo?
- Does the **~0.23-0.5 physical cores per live VM** range survive isolation hardening beyond microVM
  density, or does a stricter boundary move the ratio enough to change the topology choice?
- If users default to private scopes inside an organisation, what is the unit of tenancy that
  permissions and memory keys should bind to - the org, the Space, or the person?
- What re-derives the tenant claim when an artifact carries session state from one Space into another?

## Related pages

- [[Nithin Reddy Cheruku and Dhawal Patel - Multi-Tenant Agentic AI with Gemini Enterprise]]
- [[FD - Agent Muse Compute Demand]]
- [[Jina Yoon - We're Building Multiplayer AI]]
- [[Agent Security and Governance]]
- [[Agent Memory]]
- [[Agent Delegation]]
- [[Google Cloud]]
- [[Meta]]
- [[DeepSeek]]
- [[Inference Efficiency Frontier]]
- [[AI Agents in Production]]
- [[Institutional Knowledge Agents]]

