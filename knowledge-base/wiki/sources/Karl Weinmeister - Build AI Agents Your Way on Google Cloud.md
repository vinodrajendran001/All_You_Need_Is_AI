---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-weinmeister-build-ai-agents-google-cloud
source_title: "Build AI Agents your way on Google Cloud"
source_author: Karl Weinmeister
source_url: https://medium.com/google-cloud/build-ai-agents-your-way-on-google-cloud-7e64e76550bc
tags:
  - source/summary
  - ai-agents
  - frameworks
  - google-cloud
source_ids:
  - src-2026-09-13-weinmeister-build-ai-agents-google-cloud
status: active
---

# Karl Weinmeister - Build AI Agents Your Way on Google Cloud

## Summary

A product map for assembling an agent stack on Google Cloud: framework, model, tools and grounding, interoperability, then runtime. Its useful contribution is the separation of these choices. ADK, Gemini, MCP, A2A, Agent Engine, Cloud Run, and GKE are not one indivisible platform; they occupy different layers and can be substituted independently.

## Key claims

- Framework choices include Google ADK, CrewAI, and LangGraph; the article presents ADK as an open-source Python framework with orchestration, guardrails, and bidirectional audio/video streaming.
- Models can be reached through the Gemini API, Vertex AI, or LiteLLM. Gemini is positioned for multimodal and long-context workloads, Gemma for open-weight flexibility and efficiency.
- MCP standardizes tool and data access. MCP Toolbox for Databases supports services including Cloud SQL, Spanner, and BigQuery.
- Apigee API Hub can turn existing APIs into tools; Application Integration advertises **100+ connectors**.
- Grounding and retrieval options include Vertex AI Search, Vector Search, AlloyDB, Google Search, partner data, and experimental Google Maps APIs.
- A2A, described as backed by Google and **over 50 industry partners**, targets cross-framework communication. Agents inside one ADK application can instead share state or use `AgentTool` and `transfer_to_agent`.
- Agent Engine is the managed serverless runtime with managed state; Cloud Run accepts arbitrary containers but leaves persistence to the application; GKE provides the most control and operational burden.

## Why it matters

The stack is best read as a decision matrix rather than a prescribed architecture. Framework lock-in, model choice, tool protocol, grounding system, agent protocol, and deployment runtime are separate portability boundaries. That is more durable than the product catalogue itself.

## Tensions / open questions

- This is a broad vendor-authored map, not a benchmark or independent comparison.
- A2A's lock-in benefits depend on interoperable implementations and adoption, not protocol publication alone.
- Managed state reduces operational work but increases platform dependence; Cloud Run and GKE invert that trade.
- Product names, maturity, and experimental integrations can change quickly.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Agent Frameworks]]
- [[AI Agents in Production]]
- [[Model Context Protocol]]
- [[Agent Delegation]]
- [[Google Cloud]]

## Citations

- Karl Weinmeister, "Build AI Agents your way on Google Cloud", 2025-04-14.

## Raw capture

- [[2026-09-13 Karl Weinmeister - Build AI Agents Your Way on Google Cloud]]

## Related pages

- [[Agent Memory]]
- [[Retrieval-Augmented Generation]]
- [[Tool Use and Function Calling]]
