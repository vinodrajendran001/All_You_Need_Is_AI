---
type: concept
created: 2026-09-18
updated: 2026-10-27
tags: [concept, ai-agents, multi-tenancy, security, cost]
source_ids:
  - src-2026-09-12-cheruku-patel-multitenant-agentic-ai
  - src-2026-09-27-fd-agent-muse-compute-demand
  - src-2026-09-29-yoon-multiplayer-ai
  - src-2026-09-30-bytebytego-doordash-agent-gateway
  - src-2026-09-28-watson-nvidia-openshell-runtime-controls
  - src-2026-10-02-e2b-embed
  - src-2026-10-23-image-aware-agent-memory
  - src-2026-10-19-vercel-durable-harness
  - src-2026-10-25-rastogi-agentcore-enterprise
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

## Tool visibility, credentials, and runtime residence are different scopes

[[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]] supplies a gateway-level version of
hop-by-hop authority. Authentication identifies the caller, `tools/list` bundles select the visible
surface, `tools/call` authorizes execution, and credential injection selects the downstream identity.
A shared gateway must not turn curated discovery into permission or substitute a service principal
for a user's authorization. Short-lived user-agent-task-tool-scoped cryptographic identities are
planned improvements in this account, not existing guarantees.

[[Alex Watson - Add Runtime Controls to AI Agents with NVIDIA OpenShell]] puts the enforcement
plane outside the sandbox workload. Its modeled permission checks and credential substitution are
useful building blocks, but cross-agent composed-permission analysis remains ongoing. A protected
individual sandbox does not prove that every chain of cooperating agents preserves tenant scope.

[[E2B - Embed Runtime README]] describes single-node placement of runtime, storage, and telemetry.
It is an execution-residency choice, not evidence of per-tenant identity, memory, or authorization
isolation. Plain HTTP without built-in TLS also leaves transport protection to the deployment.
These cases strengthen component-by-component tiering: state explicitly which boundary each
component actually enforces.

[[Pranay Prakash and Eric Dodds - Making Every Harness Durable]] adds a serverless case in which the
function host itself is shared. On Vercel, many sessions can share the same function, and that
function's filesystem is not guaranteed to persist, so a harness's shell and files are not run directly
on the host. They move into a per-session `virtual()` workspace stored in the session log, whose
bash-compatible shell cannot reach the function's files or the network and runs "without starting an
entire sandbox", or into the session's own Vercel Sandbox. Developer-supplied tools such as database
queries and API calls stay in the developer's function, so "required credentials never have to enter the
sandbox." Claude Code and Codex always run in a sandbox because they "expect a real shell and filesystem,
and aren't safe for multi-tenant use", the second of which the article does not explain. The unit of
isolation described is the session. Authorization appears only as a developer-supplied `authorize` hook
on the chat route, and tenant identity is not discussed. This is runtime residence and credential
placement, not evidence of tenant isolation.

## Image search and original-byte retrieval are separate authorization hops

[[Image-Aware AI Agent Memory - Oracle 26.8]] describes user/agent-scoped image records,
metadata-filtered caption search, and explicit original-byte retrieval via
`include_bytes=True`. Its synthetic notebook filter selects the current demonstration
image; it is not an isolation test.

The clipping explicitly distinguishes scope filters from authorization. The application
must enforce who can write, search, and hydrate an image rather than treating a caller's
image ID or tenant metadata as authority. Default omission of binary bytes also does not
make descriptions and metadata safe for arbitrary readers. This extends the hop-by-hop
rule above to two views of the same persisted evidence, without claiming the tutorial
demonstrates tenant isolation.

## Per-session microVMs and per-user namespaces are building blocks, not a tenancy proof

[[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]] maps several
of this page's hops onto managed AgentCore services. Read against the topology table, compute is
dedicated per session while identity, tools, and memory use pooled-row mechanisms, which is
component-by-component tiering. The threat is stated in this page's terms: "If two users share a
process, a prompt injection in one session can be a lateral-movement path into the other." Each
session gets its own microVM with dedicated CPU, memory, and filesystem, and memory is sanitized when
it ends. As in the Vercel case above, the unit is the session, and the article discusses users, never
tenants.

Identity takes the delegated route of
[[Nithin Reddy Cheruku and Dhawal Patel - Multi-Tenant Agentic AI with Gemini Enterprise]]. A shared
service account means "every user effectively gets the service account’s access"; instead, the gateway
has a token vault exchange the user's token on-behalf-of (OBO) for one "scoped to that user and that
downstream API". The runtime's JWT authorizer validates custom claims such as group membership, but
the article never names a tenant claim, so deriving one from authentication, as this page requires,
is left to the deployer.

Memory is where the advice meets this page's warning. The requirement is that "A fact the agent learned
about Sarthak must never surface for anyone else", yet the recommendation is "one shared memory resource
with per-user namespaces, not one memory per agent", partly because "a shared store lets you reason
about retention and encryption once". That is the pooled design: isolation rests on namespace filters
holding on every read. Short-term memory is stored by user and session, which supplies the user dimension
this page asks session keys to carry but not the tenant one. This page also holds that deletion
guarantees depend on whether keys and storage are actually tenant-specific; the article lists
customer-managed keys but does not say they are scoped per namespace, so per-user deletion by key is not
established.

The article says each microVM has dedicated CPU but gives no physical-core ratio, and billing is per
second, with "CPU isn’t billed while the agent waits on I/O". That is a price, so it leaves open FD's
point above that a per-VM allocation may be an accounting unit rather than a boundary.

The author uses AgentCore at work and reports no isolation test or other measurement. The article's
own sections on where AgentCore falls short are image-only in the capture, and its timeouts and caps
are point-in-time product facts.

## Open questions

- Which tenant claims can be verified independently at every agent and tool boundary?
- How should traces expose tenant propagation without leaking tenant data into shared observability?
- What tests prove that tool discovery, memory retrieval, and delegated credentials fail closed?
- When does a hybrid topology become harder to audit than a full silo?
- Does the **~0.23-0.5 physical cores per live VM** range survive isolation hardening beyond microVM
  density, or does a stricter boundary move the ratio enough to change the topology choice?
- If users default to private scopes inside an organisation, what is the unit of tenancy that
  permissions and memory keys should bind to - the org, the Space, or the person?
  [[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]] binds memory
  namespaces, per-user tool lists, and delegated tokens to the individual user; group membership appears
  only as an example token claim, and no organisation-level unit is named.
- What re-derives the tenant claim when an artifact carries session state from one Space into another?
- Can a shared memory store with per-user namespaces honour one user's deletion without per-namespace
  keys? AgentCore's recommended design leaves key scope unstated.

## Related pages

- [[Pranay Prakash and Eric Dodds - Making Every Harness Durable]]
- [[Vercel]]
- [[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]
- [[Sarthak Rastogi]]
- [[Image-Aware AI Agent Memory - Oracle 26.8]]
- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[Alex Watson - Add Runtime Controls to AI Agents with NVIDIA OpenShell]]
- [[E2B - Embed Runtime README]]
- [[E2B]]
- [[Model Context Protocol]]
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
