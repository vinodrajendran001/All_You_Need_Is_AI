---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-prabhulal-production-rag-adk
source_title: "How to Build Production-Grade RAG with ADK and Vertex AI RAG Engine"
source_author: Arjun Prabhulal
source_url: https://medium.com/google-cloud/how-to-build-a-production-grade-rag-with-adk-vertex-ai-rag-engine-via-the-agent-starter-pack-7e39e9cfe856
tags:
  - source/summary
  - rag
  - ai-agents
  - google-cloud
source_ids:
  - src-2026-09-13-prabhulal-production-rag-adk
status: active
---

# Arjun Prabhulal - Production-Grade RAG with ADK and Vertex AI RAG Engine

## Summary

A deployment tutorial combining Google Agent Starter Pack, ADK, Gemini, Vertex AI Agent Engine, and Vertex AI RAG Engine. It demonstrates infrastructure assembly and connectivity, not retrieval quality or production reliability.

## Key claims

- Agent Starter Pack scaffolds API serving, infrastructure as code, CI/CD, logging, tracing, monitoring, Vertex AI Evaluation, IAM, connectors, vector stores, and a UI playground.
- The source calls the architecture **4 pillars**: ADK orchestration, Gemini, Agent Engine deployment, and RAG Engine retrieval/grounding.
- Agent Engine provides a managed runtime and lists Quality/Evaluation, Example Store, Sessions, Memory Bank, and Code Execution as Preview services at publication.
- RAG Engine's managed database reportedly uses Cloud Spanner, with **Basic = 100 processing units** and **Scaled = 1,000 processing units**.
- The tutorial requires **Python 3.10+**, enables Vertex AI, Discovery Engine, and Cloud Build APIs, and configures RAG Engine through Vertex rather than the ML Dev backend.
- The Agent Engine service account needs `aiplatform.ragCorpora.query`; deployed resource metadata is written to `deployment_metadata.json`.
- Cloud Trace is used to inspect the deployed run, with each session ID corresponding to one span.

## Why it matters

The article usefully distinguishes **deployment completeness** from model logic: a RAG agent needs identity, infrastructure, evaluation hooks, traces, and a managed corpus as well as retrieval code. But the label "production-grade" remains unearned until retrieval quality, leakage, latency, cost, and failure behavior are measured.

## Tensions / open questions

- "Weeks, not months" is promotional and unbenchmarked.
- Default chunking and embedding settings are accepted without evaluation.
- Several services were Preview; the IAM command shown appears malformed and needs validation.
- Successful deployment says nothing about grounding precision, hallucination rate, freshness, or cross-tenant access.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Retrieval-Augmented Generation]]
- [[AI Agents in Production]]
- [[Agent Observability]]
- [[Google Cloud]]

## Citations

- Arjun Prabhulal, "How to Build Production-Grade RAG with ADK and Vertex AI RAG Engine", 2025-11-03.

## Raw capture

- [[2026-09-13 Arjun Prabhulal - Production-Grade RAG with ADK and Vertex AI RAG Engine]]

## Related pages

- [[Agent Frameworks]]
- [[Agentic Testing]]
- [[Agent Security and Governance]]

