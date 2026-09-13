---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-tessier-gcp-model-armor
source_title: "Leveraging GCP Model Armor for Robust LLM and Agentic AI Security"
source_author: David Tessier
source_url: https://medium.com/google-cloud/leveraging-gcp-model-armor-for-robust-llm-and-agentic-ai-security-777558c6cee2
tags:
  - source/summary
  - ai-agents
  - security
  - google-cloud
source_ids:
  - src-2026-09-13-tessier-gcp-model-armor
status: active
---

# David Tessier - GCP Model Armor

## Summary

A product-oriented walkthrough of Google Cloud Model Armor, a managed service that inspects prompts before model invocation and responses before release. Its durable architectural contribution is the two-sided inspection point plus centrally enforced floor settings; it is not evidence that content filtering alone secures an agent.

## Key claims

- Model Armor exposes a REST API independent of the chosen LLM and screens both user prompts and model responses.
- Reported filters cover prompt injection/jailbreaks, malicious URLs, sensitive data, PDF text, and four harmful-content classes: hate, dangerous content, harassment, and sexually explicit content.
- Sensitive-data detection integrates with Sensitive Data Protection; findings can surface in Security Command Center.
- Templates define filters, thresholds, triggers, and custom errors. The example sets all four harmful-content categories to **MEDIUM_AND_ABOVE**.
- Applications call `SanitizeUserPromptRequest` before the model and `SanitizeModelResponseRequest` before returning output.
- Floor settings enforce minimum requirements at organization, folder, or project scope. The source says project-level settings override conflicting folder settings.
- Floor-setting findings require Security Command Center **Premium or Enterprise**.
- Cloud Logging can audit the service through `protoPayload.serviceName="modelarmor.googleapis.com"`.

## Why it matters

Central floor settings turn content inspection from an application convention into organization policy. The pre/post placement is also useful: input and output have different threat surfaces. But it remains one probabilistic layer inside a larger authority model.

## Tensions / open questions

- "Universal", "low-latency", and "comprehensive" are unmeasured vendor claims.
- Confidence thresholds trade misses against false positives; neither rate is reported.
- Model Armor does not replace IAM, sandboxing, least privilege, action authorization, or recovery.
- The sample code creates `ml_armor_client` but invokes `client`, so it should not be copied without correction.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Agent Security and Governance]]
- [[AI Agents in Production]]
- [[Google Cloud]]

## Citations

- David Tessier, "Leveraging GCP Model Armor for Robust LLM and Agentic AI Security", 2025-03-26.

## Raw capture

- [[2026-09-13 David Tessier - GCP Model Armor]]

## Related pages

- [[Agent Observability]]
- [[Model Context Protocol]]
- [[LLM Application Resilience]]

