---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-rahmat-adk-gemini-enterprise
source_title: "From ADK to Gemini Enterprise: Building Production-Grade AI Agents on Google Cloud"
source_author: Roushanak Rahmat
source_url: https://medium.com/google-cloud/from-adk-to-gemini-enterprise-building-production-grade-ai-agents-on-google-cloud-e32f4977f05a
tags:
  - source/summary
  - ai-agents
  - enterprise
  - google-cloud
source_ids:
  - src-2026-09-13-rahmat-adk-gemini-enterprise
status: active
---

# Roushanak Rahmat - From ADK to Gemini Enterprise

## Summary

An architectural walkthrough that separates agent code, managed execution, and enterprise discovery/access into three layers: ADK, Vertex AI Agent Engine, and Gemini Enterprise. The AquaFlow field-technician scenario is illustrative rather than a reported production deployment.

## Key claims

- The proposed **3-layer architecture** separates programmatic agent logic, managed runtime orchestration, and an employee-facing presentation/access layer.
- The conceptual agent uses `gemini-2.5-flash`; listed dependencies include `google-cloud-aiplatform`, `google-auth`, `pydantic`, and `cloudpickle`.
- Deployment through `adk deploy agent-engine` is described as packaging dependencies, uploading artifacts to Cloud Storage, initializing Agent Engine, and returning a Reasoning Engine resource ID.
- Service-to-service access uses IAM, with `roles/aiplatform.user` named; end-user authorization is treated separately through Workforce Identity Federation and OAuth.
- Gemini Enterprise registers the deployed agent by resource ID, name, and description and can route employee queries to it.
- Agent Designer is the no-code path for simple prompt-based agents; ADK plus Agent Engine is the code-driven path for custom workflows and tools.

## Why it matters

The durable boundary is **execution versus distribution**. A production agent needs a runtime identity and lifecycle independently of the interface through which employees discover it. That separation helps avoid treating a chat surface as the security boundary.

## Tensions / open questions

- The case study is fictional and the function is explicitly conceptual ADK-style code.
- "Production-grade" and "highly secure" are not supported by reliability, latency, cost, evaluation, or threat-model measurements.
- IAM service identity, end-user identity, and tool-level authorization are distinct controls; configuring one does not imply the others.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[AI Agents in Production]]
- [[Agent Frameworks]]
- [[Agent Security and Governance]]
- [[Google Cloud]]

## Citations

- Roushanak Rahmat, "From ADK to Gemini Enterprise: Building Production-Grade AI Agents on Google Cloud", 2026-06-22.

## Raw capture

- [[2026-09-13 Roushanak Rahmat - From ADK to Gemini Enterprise]]

## Related pages

- [[Tool Use and Function Calling]]
- [[Agent Plugin Architecture]]
