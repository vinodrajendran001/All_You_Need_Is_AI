---
type: entity
entity_kind: organization
created: 2026-09-13
updated: 2026-09-13
tags:
  - entity
  - organization
  - cloud
  - ai-agents
source_ids:
  - src-2026-09-13-adedeji-multi-agent-code-review
  - src-2026-09-13-weinmeister-build-ai-agents-google-cloud
  - src-2026-09-13-nevsky-gemini-multi-agent-system
  - src-2026-09-13-rahmat-adk-gemini-enterprise
  - src-2026-09-13-prabhulal-production-rag-adk
  - src-2026-09-13-virinchi-google-cloud-mcp-security
  - src-2026-09-13-ranganathan-gke-inference-gateway
  - src-2026-09-13-tessier-gcp-model-armor
  - src-2026-09-13-rahman-quantizing-llms-gke
status: active
---

# Google Cloud

## What it is

Google Cloud is Google's cloud-computing platform. In this vault it matters as a vertically integrated
agent and model-serving stack: models, agent frameworks, managed runtimes, enterprise distribution,
retrieval, Kubernetes inference, tool protocols, identity, content inspection, observability, and
recovery are all represented in one vendor ecosystem.

## Why it matters here

The September 13 source cluster is useful less as a product catalogue than as a map of **separable
control planes**:

- [[Karl Weinmeister - Build AI Agents Your Way on Google Cloud]] maps framework, model, tools,
  grounding, interoperability, and runtime as independent choices.
- [[Ayo Adedeji - Agents That Prove, Not Guess]] demonstrates ADK orchestration over deterministic
  parsing, linting, and sandboxed testing rather than treating the framework as the evidence source.
- [[Alex Nevsky - Building a Multi-Agent AI System with Gemini 3 and Google Cloud]] adds typed
  handoffs, a sole action writer, bounded QA repair, and model-tier routing.
- [[Roushanak Rahmat - From ADK to Gemini Enterprise]] separates code in ADK, execution in Vertex AI
  Agent Engine, and employee discovery through Gemini Enterprise.
- [[Arjun Prabhulal - Production-Grade RAG with ADK and Vertex AI RAG Engine]] supplies deployment,
  identity, tracing, and managed-corpus scaffolding while leaving retrieval quality unevaluated.
- [[Virinchi T - Google Cloud MCP Security Framework]] joins MCP to IAM, tool inventory, tenant
  isolation, content inspection, PII controls, and recoverability.
- [[David Tessier - GCP Model Armor]] describes centrally enforced prompt/response inspection and
  organization-level floor settings.
- [[Rahul Ranganathan - Inference Gateway on GKE]] moves KV locality, queue pressure, adapter
  placement, and request priority into routing.
- [[Mofi Rahman - Quantizing LLMs on GKE]] gives a worked weight-capacity example and the crucial
  distinction between weight fit and runtime fit.

## Current synthesis

**The stack's integration is both its value and its lock-in surface.** Agent Engine can manage runtime
and state, Gemini Enterprise can publish agents, MCP servers can expose cloud services, Model Armor can
inspect both sides of model calls, and GKE can run model-aware routing. Each integration removes plumbing;
each also creates a policy, identity, telemetry, or resource model that must be migrated if the layer moves.

**A Google Cloud publication is not independent evidence about Google Cloud products.** The nine sources
above are tutorials and product-oriented architecture guides. Their mechanisms and configuration details
are useful; claims such as "production-grade", "secure", "significant improvement", or "weeks not months"
remain promotional unless tied to a disclosed workload and measurement.

**Managed does not mean governed.** The strongest sources repeatedly separate the managed component from
the deployer's responsibilities: Agent Engine does not define business authorization, Model Armor does not
replace IAM or sandboxing, RAG deployment does not establish retrieval quality, and backups must be
configured before they can make destructive tool use recoverable.

## Open questions

- Which state, trace, tool, and policy formats remain portable across Agent Engine, Cloud Run, and GKE?
- How should the Preview and Pre-GA status of MCP and inference components constrain production use?
- What independent benchmarks quantify Model Armor detection quality or Inference Gateway scheduling gains?
- Where should end-user authorization be enforced when Gemini Enterprise, Agent Engine, and a mutating tool
  each see a different identity?

## Related pages

- [[AI Agents in Production]]
- [[Agent Frameworks]]
- [[Agent Security and Governance]]
- [[Model Context Protocol]]
- [[Retrieval-Augmented Generation]]
- [[Inference Serving Engines]]
- [[Model Quantization and Efficiency]]
