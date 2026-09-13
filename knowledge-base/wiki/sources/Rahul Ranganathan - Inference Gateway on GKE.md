---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-ranganathan-gke-inference-gateway
source_title: "Inference Gateway: Intelligent Load Balancing for LLMs on GKE"
source_author: Rahul Ranganathan
source_url: https://medium.com/google-cloud/inference-gateway-intelligent-load-balancing-for-llms-on-gke-6a7c1f46a59c
tags:
  - source/summary
  - inference
  - serving
  - google-cloud
source_ids:
  - src-2026-09-13-ranganathan-gke-inference-gateway
status: active
---

# Rahul Ranganathan - Inference Gateway on GKE

## Summary

An explanation of why LLM load balancing needs model-aware signals rather than ordinary round robin or IP stickiness. GKE Inference Gateway combines queue pressure, KV-cache locality, model identity, adapter placement, and request priority through the Kubernetes Gateway API Inference Extension.

## Key claims

- Routing a continuation away from the replica holding its KV cache forces prefix recomputation, increasing time to first token and consuming accelerator capacity.
- KV caches can consume **several gigabytes per sequence** and may exceed weight memory under long contexts or large batches.
- IP stickiness can overload one replica when many sessions share a NAT or orchestrator IP; cookie stickiness is awkward for programmatic clients.
- The gateway uses `InferencePool`, `InferenceModel`, and `TargetModel` resources to represent serving pools, model identities, and routing mappings.
- Endpoint selection considers KV-cache utilization, queue length, and active LoRA adapters. This is a trade between locality and queue delay, not unconditional cache affinity.
- Backends can expose request-cost metrics through **ORCA** response headers.
- Requests can be **Critical, Standard, or Sheddable**; under pressure, lower-priority work may be delayed and Sheddable work dropped.
- Multiple LoRA adapters can share replicas holding one base model.
- Traffic splitting, mirroring, OpenAI-style body routing, observability, and Model Armor integration are also described.

## Why it matters

The gateway makes inference state part of routing policy. It also shows why "least loaded" is not a single metric: the best endpoint may already hold the prefix, already hold the adapter, or have the shortest queue, and these can disagree.

## Tensions / open questions

- The Gateway API Inference Extension was experimental/alpha and GKE Inference Gateway was Preview/Pre-GA.
- Claimed improvements in TTFT, throughput, utilization, and cost are not quantified.
- Cache affinity can worsen latency when the cached endpoint is overloaded.
- The post sometimes calls inference stateful; the durable issue is performance locality, not necessarily application-session correctness.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Inference Serving Engines]]
- [[KV Cache]]
- [[ML Systems at Scale]]
- [[Google Cloud]]

## Citations

- Rahul Ranganathan, "Inference Gateway: Intelligent Load Balancing for LLMs on GKE", 2025-04-26.

## Raw capture

- [[2026-09-13 Rahul Ranganathan - Inference Gateway on GKE]]

## Related pages

- [[LLM Inference]]
- [[Serving Benchmarks and Goodput]]
- [[Model Routing]]

