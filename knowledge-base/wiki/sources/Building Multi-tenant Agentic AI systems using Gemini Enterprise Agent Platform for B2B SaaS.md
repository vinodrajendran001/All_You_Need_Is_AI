
---
title: "Building Multi-tenant Agentic AI systems using Gemini Enterprise Agent Platform for B2B SaaS"
source: "https://medium.com/google-cloud/building-multi-tenant-agentic-ai-systems-using-gemini-enterprise-agent-platform-for-b2b-saas-5075a8dfd1db"
author:
  - "[[Nithin Reddy Cheruku]]"
published: 2026-09-12
created: 2026-09-13
description: "More"
tags:
  - "clippings"
---
Authors: [Nithin Reddy Cheruku](https://medium.com/@meetnithin) & [Dhawal Patel](https://medium.com/@dhawalpatel_30637)

## Overview

Independent software vendors are moving agents out of pilots and into production. The engineering question is no longer whether an agent can complete a task, but whether one platform can serve thousands of customers with agents without leaking data across accounts, eroding gross margin, or failing an enterprise security review.

That is a multi-tenancy problem, and it is not the multi-tenancy problem ISVs have already solved. In conventional SaaS, isolation is enforced at a small number of predictable choke points: an authenticated request, a scoped query, a row filter. The code path is deterministic, so it can be enumerated, tested, and demonstrated to an auditor. An agent removes that guarantee. It decides at runtime which tools to call, what to retrieve, how many turns to take, and which sub-agents to spawn. The execution path is generated rather than written, and every architectural assumption that depended on knowing the path in advance has to be re-established somewhere else.

This post sets out the components where that work happens, and how Gemini Enterprise Agent Platform (GEAP) implements each one.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*o93FluNkEBACotK4ekvgBQ.png)

## Challenges

The first challenge is that the isolation boundary moves inward. Tenant identity can no longer be validated once at the edge and then assumed for the remainder of the request. It has to survive every hop the agent takes, through the planner, into each sub-agent, across every tool call and retrieval, and down to the model invocation itself. It also has to be immutable once set, because an agent that can rewrite its own tenant context is an agent with no tenancy at all. Isolation stops being a perimeter and becomes a property that each hop has to carry.

The untrusted input now reaches the control path. In deterministic software, user input is data that code acts upon. In an agentic system it is partly instruction, which makes the model a legitimate attack surface rather than a passive component. An agent compromised through its prompt is a confused deputy that already holds valid credentials and is already inside the boundary, so it does not need to escalate privilege to cause damage.

In addition, the cost becomes a runtime property rather than a planning assumption. Traditional SaaS enjoyed stable per-tenant infrastructure costs that could be modeled in a spreadsheet. Agentic workloads do not behave that way. Turn counts vary per request, recursive delegation multiplies calls, and retrieval expands context unpredictably, so one tenant can consume orders of magnitude more than another on an identical price plan.

The one that shapes the architecture most directly, is that isolation stops being a single decision. Memory, tools, data, model context and the runtime each carry their own pooled-versus-siloed answer, and each answer carries different compliance obligations, blast radius and unit cost. There is no single multi-tenancy switch to flip. Every component in the stack independently answers one question: is this shared across tenants, or dedicated per tenant? Answering it well lets a platform serve thousands of self-serve tenants alongside a handful of regulated enterprises on one control plane. Answering it poorly means either paying for isolation nobody asked for, or discovering the gap during a customer security review.

The diagram below shows the ten components where that question has to be answered, and the two planes that cut across all of them.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HUZ_5Gh_ZNg_MS4BNV9Abg.png)

Each component below covers what it does, the tenancy decision it forces, and the GEAP service that implements it. Implementation depth for each follows later in this post.

## Foundational components for building multi-tenant agents

### 1\. Identity:

Agentic applications carry four distinct identities, and conflating them is the most common source of multi-tenant authorization bugs.

**User Identity (ID-1 | Who is asking)**: The authenticated human principal initiating the session, verified at ingress by [Google Cloud Identity Platform Multi-Tenancy](https://docs.cloud.google.com/identity-platform/docs/multi-tenancy-quickstart) (or [Workforce Identity Federation](https://docs.cloud.google.com/iam/docs/workforce-identity-federation) for direct cloud federations) federating external enterprise IdPs (e.g., Okta, Microsoft Entra ID, Ping Identity) and attaching verified tenant context.

**Agent Identity (ID-2 | What is running)**: The platform-issued workload identity (e.g., SPIFFE, mTLS, API keys, Signed JWT, X.509 certificates) that uniquely identifies the running agent runtime and authorizes its access to infrastructure-level services (such as IAM policies, BigQuery, and Cloud Audit Logs).

**On-Behalf-Of / Delegated Identity** **(ID-3 | Whose permissions apply downstream)**: The user-delegated credential (e.g., OAuth 2.0 access token) brokered via explicit consent, allowing the agent to perform actions against external systems (such as Slack or Google Workspace) strictly within the user’s personal permission envelope.

**Tenant Identity (Optional | ID-4 | Which boundary governs isolation)**: The verified organizational boundary (tenant\_id) that enforces data segregation, memory partitioning, telemetry routing, and row-level security across shared execution tiers.

### 2\. Binding Tenant Identity to User Identity

To prevent spoofing and eliminate forgeable client-side signals, tenant identity is cryptographically bound to the user identity at ingress within a signed JSON Web Token (JWT). By embedding the validated tenant\_id claim directly alongside the user principal (sub) and authorized scopes (tenant:tenant\_1), the platform produces an immutable security context. Downstream planners, sub-agents, memory stores, and database RLS engines inherit this unified token across every execution hop without relying on ambient parameters. However, In mature enterprise environments with existing multi-tenant services, upstream microservices often generate and propagate tenant context dynamically in-flight via custom HTTP headers (e.g., X-Tenant-ID, Tenant-ID, or path prefixes). To safely support these workflows without introducing confused-deputy risks, make sure the Ingress proxies / Agent Gateways intercept in-flight headers, validate them against the user’s authenticated directory entitlements or tenant catalog (e.g., checking if User\_A belongs to Tenant\_1), and strip untrusted raw headers and the gateway mints or enriches the downstream signed JWT/intent token with the verified tenant claim before dispatching to the agent runtime, bridging legacy header-driven routing with zero-trust cryptographic enforcement.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*t7KGg9t4HCCcanDUJ8nX9Q.png)

Gemini Enterprise Agent Platform treats all three as first-class primitives rather than application concerns. [Agent Identity](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity) issues every agent a unique, lifecycle-bound [SPIFFE](https://spiffe.io/) ID backed by an auto-provisioned X.509 certificate, and that ID acts directly as an IAM principal — usable in [Principal Access Boundary](https://cloud.google.com/iam/docs/principal-access-boundary-policies) policies and [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview), and recorded against every call in [Cloud Audit Logs](https://cloud.google.com/logging/docs/audit). Unlike service accounts, these identities cannot be impersonated, issue no long-lived keys, and retire with the agent runtime, which removes the orphaned-credential problem that shared service accounts create at scale. Access tokens are cryptographically bound to the certificate through mTLS and [DPoP](https://datatracker.ietf.org/doc/html/rfc9449) so a stolen token cannot be replayed outside its authorized runtime. For delegated access, the [Agent Identity auth manager](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-identity) brokers the three-legged OAuth flow, manages consent, and decrypts credentials inside the [Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-gateway) so the agent never handles a raw secret. For an ISV, the practical effect is that the tenant boundary is enforced by platform-issued cryptographic identity rather than by application code remembering to pass a tenant ID.

### 3\. Identity Propagation and tenant isolation

When an AI agent interacts with downstream tools and data custodians, how identity and tenant context are propagated determines the system’s security posture. Enterprise agent architectures typically encounter three propagation patterns:

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zdq7klCJffuX0YdVQzDo5A.png)

1. **Impersonation (Raw “God Token” Pass-Through):** The user’s inbound token (Token A) containing broad permissions (order:\*, promo:\*, admin:\*) is forwarded verbatim by the agent to every downstream tool. Because there is no attenuation or actor attribution, every tool receives ambient, over-privileged access, introducing critical **Privilege Escalation** and confused-deputy risks if the agent prompt or a tool is compromised.
2. **Delegation / On-Behalf-Of (RFC 8693 Token Exchange):** The agent exchanges the user’s inbound token for individual, downscoped tokens tailored per target system (Token 1 with order:read for the Order Tool; Token 2 with promo:write for the Promotions Tool). By embedding an **actor claim** (“act”: {“sub”: “Agent\_1”}) alongside the user subject and tenant boundary (tenant\_id: “Tenant\_A”), this pattern enforces **Least Privilege** and ensures end-to-end auditability.
3. **Batch / Autonomous Workload (SPIFFE Workload & Vault Exchange):** For non-human or scheduled tasks initiated by background triggers, the agent runs under its own cryptographic workload identity (e.g., **SPIFFE SVID**). To interact downstream, the agent either presents its SPIFFE token directly to service-mesh-aware systems or leverages a Credential Vault to exchange it for **tenant-scoped 2LO OAuth tokens or API keys** for legacy/3P APIs — maintaining strict **Workload Isolation** with zero user PII exposure.

## Agent Deployment Models

Architecting multi-tenant agent platforms forces ISVs to navigate the **Agentic Trilemma** — the inherent architectural tension between **Tenant Isolation**, **Cost Efficiency**, and **Operational Simplicity**. The **Silo Model** dedicates separate infrastructure (projects, runtimes, and memory) to each tenant, delivering zero blast radius and effortless compliance at the expense of high idle costs and fleet sprawl. The **Pool Model** runs all tenants across a shared runtime fleet, maximizing compute density and simplifying operations through logical JWT/RLS partitioning, but introducing noisy-neighbor and confused-deputy risks. To resolve this tension, most enterprise ISVs adopt a **Hybrid Model**, routing high-volume standard tiers to a cost-effective shared pool while dynamically dispatching premium or regulated enterprise workloads to dedicated, physically isolated silo perimeters.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*cgx1HhjkpIu8qGzeBrIlyw.png)

Balancing compliance, manageability, and SaaS gross margins.

### Architectural Foundation: Gemini Enterprise Agent Platform (GEAP)

The [Gemini Enterprise Agent Platform (GEAP)](https://cloud.google.com/products/gemini-enterprise-agent-platform) is Google Cloud’s unified, enterprise-grade platform designed to build, scale, govern, and optimize autonomous agents. For multi-tenant SaaS ISVs, GEAP functions as a managed control and data plane over existing cloud infrastructure.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*HuB81xlmUMhNDKnRCP3WgQ.png)

Gemini Enterprise Agent Platform (GEAP) Architectural Pillars

### Why B2B ISVs Build Multi-Tenancy on GEAP

- Build (Open & Framework-Agnostic): Supports [ADK 2.0](https://google.github.io/adk-docs/) alongside third-party (3P) agent frameworks ([LangGraph](https://github.com/langchain-ai/langgraph), [CrewAI](https://www.crewai.com/), [AutoGen](https://microsoft.github.io/autogen/)). Integrates frontier Gemini models and open models via [Model Garden](https://cloud.google.com/model-garden), coupled with open standard protocols ([A2A](https://github.com/google/agent-to-agent), [Stateless MCP](https://modelcontextprotocol.io/), [A2UI](https://github.com/google/a2ui), and enterprise connectors).
- Scale (Managed Compute & State Isolation): [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-runtime) provisions sub-second warm-start execution with [Agent Sandbox](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-sandbox) backed by [gVisor](https://gvisor.dev/) microVMs. [Agent Sessions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-sessions) and [Agent Memory Bank](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/memory-bank) provide managed multi-tenant hierarchical memory with tenant-isolated [Customer-Managed Encryption Key (CMEK)](https://cloud.google.com/kms/docs/customer-managed-encryption-keys) partition boundaries.
- Govern (End-to-End Enterprise Perimeter Security): [Agent Gateway (PEP)](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-gateway) and [Agent Registry](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-registry) enforce tenant-scoped agent authorization and dynamic tool entitlements. [Model Armor](https://cloud.google.com/vertex-ai/generative-ai/docs/model-armor/overview) protects against prompt injection and Data Loss Prevention (DLP) leaks, while [Agent Identity (SPIFFE)](https://spiffe.io/) and [Agent Policy](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-policy) enforce Natural Language Constraints (NLCs) and anomaly detection.
- Optimize (Continuous Quality & Tokenomics): [Agent Evaluation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-evaluation) (LLM-as-a-judge scoring), [Agent Simulation](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-simulation), and [Agent Observability](https://docs.cloud.google.com/gemini-enterprise-agent-platform/docs/agent-observability) feed telemetry directly into [BigQuery](https://cloud.google.com/bigquery/docs) Agent Analytics, providing granular per-tenant COGS attribution and automated agent tuning.

## The Three Core Tenancy Topologies

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*JS1HMzHpTQlEa7HAgSND7g.png)

The Three Multi-Tenant Tenancy Topologies (Pool, Bridge, Silo) with Control, Compute, and Data Planes

### Pattern A: Pooled Architecture (Standard Tier)

In the **High-Density Pooled Architecture**, standard-tier SaaS tenants share a unified, highly scalable Google Cloud infrastructure across the control, compute, and data planes. Tenant isolation is enforced end-to-end through **cryptographic tokens, request-scoped in-container boundaries, exact-match memory scoping, and policy-driven egress gating** — ensuring zero cross-tenant data leakage while maximizing resource efficiency.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*3_a9EoEHseWYEXupCTXoDg.png)

Pattern A: Pooled Architecture (Standard Tier)

### End-to-End flow

### 1\. Inbound Authentication & Identity Federation (Tenant Realms)

- **Corporate SSO:** Users from different enterprise realms (e.g., Tenant A with Okta, Tenant B with Google Identity, Tenant C with Ping) authenticate directly against their native Enterprise IdPs.
- **Ingress authentication & Identity Federation (WIF):** The SaaS Ingress API Gateway leverages [Google Cloud Identity Platform Multi-Tenancy](https://docs.cloud.google.com/identity-platform/docs/multi-tenancy-quickstart) (or Workforce Identity Federation with federated IdP mapping for bespoke enterprise tiers) to authenticate external SaaS users against their native enterprise IdPs. Identity Platform handles project-level tenant routing at scale, minting signed JWTs that automatically embed cryptographically verified claims (tenant\_id, sub/user\_id, and tenant scopes) without requiring cross-organization directory sync or hitting workforce pool provider limits.

### 2\. Perimeter SaaS Ingress & Policy Enforcement (Ingress Gateway)

- **Pooled SaaS Ingress API Gateway:** Acts as the shared edge entry point handling tenant onboarding, metering, cost attribution, rate limiting, and tenant-aware routing.
- **Token Validation & Header Propagation:** The gateway validates the inbound token signature against IdP/WIF JWKS, extracts verified tenant context, and forwards an immutable **Tenant & user context in JWT** downstream.

### 3\. Execution, Orchestration & Memory Partitioning (Agent Runtime)

- **In-Container Turn Isolation:** The **Pooled Agent Runtime** executes turns inside isolated, request-scoped container contexts in the Google ADK fleet.
- The Agent Runtime operates under a **single shared SPIFFE workload identity** across all tenants, meaning infrastructure-level identity alone cannot serve as your tenant boundary. Developers must treat application-level tenant isolation as the critical line of defense exercising utmost rigor in scoping execution state, sanitizing ephemeral tokens, dynamically pruning tools, and enforcing exact memory dictionaries on every turn. Without uncompromising, tenant-aware application code, a single logic oversight in shared compute can compromise multi-tenant confidentiality.
- **Dynamic Tool Pruning:** Before invoking the model, the runtime excises unauthorized tools from the request schema based on tenant entitlement policies.
- **Schema Discovery & Attestation:** The runtime queries the **Pooled Agent Registry** to discover and attest JSON-RPC tool schemas and MCP definitions.
- **Memory Bank Exact-Match Scoping:** Long-term memory retrieval and event consolidation in **Memory Bank (Agent Engine)** enforce strict exact dictionary matching using Memory scope={“tenant\_id”, “user\_id”}
- **Session Persistence:** Session turns are written to **Pooled Sessions (Agent Engine)** keyed by composite composite identifiers ({tenant\_id}:{user\_id}:{session\_id}).

### 4\. Credential Delegation & Identity Exchange (Auth Manager)

- **Pooled Auth Manager & Identity:** Holds delegated user credentials and OAuth refresh tokens.
- **OBO & 3LO Delegation:** Exchanges the inbound user token for downscoped, tool-specific short-lived tokens bound with **RFC 9449 DPoP** proofs for On-Behalf-Of (OBO) execution.
- **Auth Provider Isolation & Credential Management:** Each Auth Manager instance (auth provider) requires an OAuth client ID and client secret. SaaS providers face a design tradeoff regarding tenant isolation:

**→ Shared Multi-Tenant App Registration:** Provision a single, centralized client ID/secret pair managed by the SaaS application.

**→ Customer-Managed App Registration (BYO-Credentials):** Require each customer tenant to supply their own enterprise client ID and secret.

### 5\. Egress Authorization, Safety & Tool Execution (Egress Gateway)

- **Pooled Egress Agent Gateway (PEP Proxy):**
- **Policy Resolution:** Queries the **Pooled Agent Registry** to resolve tenant-specific tool access policies.
- **Service Extensions:** Executes custom WebAssembly/gRPC callouts for fine-grained access control (FGAC) governing which tenant can invoke specific tools.
- **Identity-Aware Proxy (IAP) & Semantic Policies:** Enforces IAM and semantic guardrails.
- **Content Safety:** Runs **Model Armor & Cloud DLP** to filter prompt injections, screen payloads, and redact sensitive PII/SSNs.
- **Authorized Downstream Execution:**

**Pooled MCP Server:** Validates OBO JWTs and DPoP proofs before executing tool microservices.

**A2A Multi-Agent Collaboration:** Dispatches delegated sub-tasks while strictly propagating tenant context across agent boundaries.

**Pooled Enterprise APIs & Databases:** Calls IAM-protected downstream services and databases with Row-Level Security

## Pattern B: Sovereign Multi-Tenant Silo Architecture (Enterprise Tier)

For regulated enterprises (healthcare, finance, defense), logical pooling may be unacceptable. The Sovereign Multi-Tenant Silo Architecture isolates each tenant into a dedicated and isolated deployment in a Google Cloud project (ex: tenant-acme-prod) enclosed by a VPC Service Controls (VPC-SC) perimeter with dedicated agent runtime compute, sessions, memory, egress gateway talking to dedicated/siloed MCP servers, datastores with (Cloud KMS CMEK options).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*jn8VS4bZYFXc7xddtjpv_w.png)

Pattern B: Sovereign Multi-Tenant Silo Architecture (Enterprise Tier)

1. Global Ingress Gateway: Similar to Pattern 1, incoming traffic terminates at a shared Global External ALB and Cloud Armor WAF with enterprise IdP federation (SAML/OIDC).
2. Global SaaS Dispatcher & Regional Routing: Decoupled Saas ingress API authenticates callers, checks enterprise tier, resolves the tenant’s dedicated regional silo project, and forwards the request over Private Service Connect (PSC) without minting tool credentials upstream.
3. Dedicated GEAP Agent Runtime & Frontier Models: Inside VPC-SC, the dedicated GEAP Agent Runtime leveraging dedicated Agent sessions (VertexAiSessionService), Agent memory bank. Reasoning runs on frontier models with dedicated context caches and zero data retention, while Agent sandboxes isolate untrusted code. While the tenant config and storing tenant specific data like skills, tools, policies are still loaded into session context and used when sending egress requests by agent.
4. In Vertex AI and the Gemini Enterprise Agent Platform, CMEK encryption is bound at the project and regional Agent Engine resource level, meaning all tenants sharing a pooled Agent Runtime fleet share the same underlying KMS encryption key. True **per-tenant CMEK isolation and cryptographic erasure** is exclusive to the **Sovereign Silo model**, where each tenant is provisioned a dedicated Google Cloud project and Agent Engine instance encrypted under their own customer-managed KMS key
5. Dedicated Egress Agent Gateway & JIT Token Downscoping: When the model calls a tool, the outbound request passes through an Egress Agent Gateway acting as a security checkpoint. It enforces Natural Language Constraints (NLCs)guardrail policies (e.g., blocking unauthorized transactions over $50k) and Model Armor data loss prevention. To enforce least privilege, the agent performs Just-In-Time (JIT) token downscoping via Cloud STS, minting short-lived tokens restricted to that specific tool.
6. Dedicated MCP & Physical Database Isolation: Dedicated stateless MCP servers connect to a single-tenant DB cluster. What changes vs. Pattern 1: Zero Row-Level Security (RLS) is required every record belongs exclusively to this tenant. Revoking the tenant’s Cloud KMS CMEK key achieves instantaneous cryptographic erasure.

## Pattern C: The Hybrid Bridge Pattern)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ulVfAb3b2Dg94mKaEqPEoQ.png)

Pattern C: The Hybrid Bridge Pattern

In production B2B SaaS, multi-tenancy is not a rigid binary choice between high-density pooling (Pattern A) and sovereign silos (Pattern B). Enterprise deals demand dedicated compute guarantees (zero noisy neighbors, guaranteed Provisioned Throughput), isolated conversational sessions, memory, and Customer-Managed Encryption Keys (Cloud KMS CMEK), while standard self-serve tiers must run on shared infrastructure to preserve high gross margins, low operational overhead.

The Hybrid Bridge Architecture unifies these requirements by decoupling multi-tenancy across two orthogonal axes:

1. Compute Tiering (Runtime Decoupling): Enterprise tenants execute on dedicated Silo Agent Runtimes with isolated sessions and memory, while standard tenants share an autoscaling Pooled Agent Runtime fleet.
2. Data & Tool Sovereignty (Layer Decoupling): Outbound tool invocations from all runtimes transit a centralized Pooled Egress Agent Gateway that routes requests with authorized tenant claims either into dedicated Silo MCP Tools & CMEK Databases (via Private Service Connect) or into shared Pooled MCP Tools (enforcing database Row-Level Security).

### Key Architectural Components & Subsystems:

1. Pooled Identity & Edge Ingress: Google Cloud Armor WAF and External Application Load Balancers (ALB) terminate edge TLS. Ingress API Gateways leverage [Identity Platform Multi-Tenancy](https://docs.cloud.google.com/identity-platform/docs/multi-tenancy-quickstart) (or [Workforce Identity Federation](https://docs.cloud.google.com/iam/docs/workforce-identity-federation) with federated IdP mapping for bespoke enterprise tiers) to federate external SAML/OIDC assertions from Okta, Google Workspace, or Microsoft Entra ID. This exchanges incoming assertions into verified short-lived tokens containing tenant\_id, sub, and enterprise tier claims with zero directory synchronization.
2. SaaS Control Plane & Dynamic Tier Dispatcher: A decoupled API service on Cloud Run/GKE paired with Cloud Memorystore like Redis. It evaluates caller claims, validates tenant licensing, checks token quotas and resolves the tenant’s execution target: dispatching directly to dedicated Silo Agent Runtimes or forwarding to the pooled runtime fleet.
3. Hybrid Agent Execution Layer (Bifurcated Runtimes):

a) Silo Agent Runtimes (Enterprise Tier): Dedicated GEAP Agent Runtime instances deployed in tenant-dedicated project perimeters. Workflows execute on frontier reasoning models with guaranteed Provisioned Throughput (PTU) to eliminate noisy-neighbor jitter, backed by isolated Agent sandboxes.

b) Pooled Agent Runtime Fleet (Standard Tier): A shared, horizontally autoscaled GEAP Agent Runtime fleet running lower cost frontier models with prompt-prefix context caching to maximize unit economics.

4\. Bifurcated Session & Memory Architecture:

a) Enterprise Silo session & Memory: Dedicated Agent Engine Session instances and dedicated VertexAiMemoryBankService datastores provisioned in the enterprise tenant’s project and encrypted with Cloud KMS CMEK.

b) Standard Pooled Memory: Centralized Agent Engine Session ({tenant\_id}:{user\_id}:{session\_id}) and Memory Bank partitioned logically via deterministic composite keys ({tenant\_id}:{user\_id}) directly within shared compute.

5\. Centralized Pooled Agent Registry: A unified capability and tool discovery catalog. Both Silo and Pooled runtimes dynamically discover available skills and MCP tools from the shared registry.

6\. Pooled Egress Agent Gateway (PEP): The managed, Envoy-based GEAP Agent Gateway acting as the centralized outbound Policy Enforcement Point (PEP). It authenticates outbound calls from all runtimes via SPIFFE mTLS, validates Semantic policies, coordinates JIT token downscoped and inspects payloads inline with Model Armor and DLP.

7\. In the Hybrid Bridge model, Auth Manager instances must align with the tenant’s chosen isolation level. SaaS architects can configure a single SaaS-wide client ID/secret or allow enterprise tenants to submit their own dedicated OAuth credentials (BYO-credentials). Regardless of credential ownership, provisioning dedicated auth provider configurations per customer ensures that token exchanges (OBO/3LO) and credential stores remain completely siloed as requests transition from pooled/silo runtimes across the shared egress gateway.

8\. Hybrid Data & Tools Layer (Silo Spokes vs. Pooled Engines):

a) Agent runtime when calling egress gateway sends TenantID, userID, OBO token as part of headers which is then passed through egress gateway as a pass through. Backend systems(MCP servers, APIs, DBs) have to do their own federated authorization using those credentials decoupling and treating those systems independently.

b) Silo MCP Tools & Data Spokes (Enterprise Tier): Tool calls transit Private Service Connect (PSC) to dedicated customer spoke projects. A dedicated MCP Tool Server executes tool logic against single-tenant DB clusters (zero Row-Level Security required) and in-perimeter Tenant Knowledge Graphs / Vector Search (Vertex AI Search / pgvector), fully encrypted under customer-managed CMEK keys.

c) Pooled MCP Tools (Standard Tier): Shared MCP servers execute against multi-tenant databases enforcing Row-Level Security Unified Observability & Metering: Granular OpenTelemetry instrumentation tagging every span with tenant\_id, turn\_id, user\_id, and runtime\_tier (silo vs pooled), streaming into BigQuery Agent Analytics for real-time COGS accounting and SLA tracking.

Choosing the right pattern — whether maximizing density with Pooled, isolating sensitive compute/data with Hybrid Bridge, or meeting strict regulatory mandates with Sovereign Silo — gives SaaS builders the flexibility to balance unit economics with enterprise-grade compliance.

## What’s Coming in Part 2

Multi-tenancy in the agentic era cannot be treated as an afterthought or bolted on at the API layer. It must be designed into the foundational control, compute, and data planes of your platform. In Part 2 of this series, Building the High-Density Pooled Tier: An End-to-End Implementation *Blueprint*, we take a deep dive into implementing the Pooled architecture pattern with production-grade code samples, reference configurations, and deployment blueprints using the Gemini Enterprise Agent Platform (GEAP) across all core subsystems.

**About the Authors:**

[**Dhawal Patel**](mailto:dhawalpatel@google.com)**:** I lead the Forward Deployed Engineering (FDE) team across North America at Google Cloud, where we work hand-in-hand with top enterprises and ISVs to operationalize Gemini and generative AI. Prior to Google, I spent over seven years at AWS leading Gen AI GTM teams. At heart, I am a hands-on builder passionate about distributed systems, agentic architectures, and helping developers solve real-world problems with AI.

Follow on [medium](https://medium.com/@dhawalpatel_30637) | connect on [Linkedin](https://www.linkedin.com/in/dhawalpatel1981/)

[**Nithin Reddy Cheruku**](mailto:nrcheruku@google.com) Nithin Reddy Cheruku leads Agentic AI and Generative AI architecture for strategic Enterprise SaaS ISVs at Google Cloud. Operating at the intersection of enterprise strategy and advanced distributed AI systems, Nithin advises product and engineering executives on translating frontier AI capabilities into resilient, enterprise-grade software products built on Google Cloud Well-Architected AI frameworks.

Follow on [medium](https://medium.com/@meetnithin) | connect on [Linkedin](https://www.linkedin.com/in/nithinrcheruku/)