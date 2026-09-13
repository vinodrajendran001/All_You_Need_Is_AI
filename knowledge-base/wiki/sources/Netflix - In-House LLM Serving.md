---
type: source-summary
created: 2026-08-03
updated: 2026-09-13
source_id: src-2026-07-17-netflix-in-house-llm-serving
source_title: "In-House LLM Serving at Netflix"
source_author: Netflix Technology Blog
source_url: https://netflixtechblog.com/in-house-llm-serving-at-netflix-a5a8e799ea2c
tags: [source/summary, serving, vllm, netflix]
source_ids: [src-2026-07-17-netflix-in-house-llm-serving]
status: active
---

# Netflix - In-House LLM Serving

## Summary

Netflix describes an internal LLM-serving platform built around vLLM and Triton, exposing both OpenAI-compatible and gRPC interfaces. The production work is less about hosting a model once than managing model artifacts, API/schema evolution, constrained output, and useful observability.

## Key claims

- Version-pinned deployments and compatibility boundaries prevent model/API changes from silently breaking clients.
- An FSx-based model cache reduces repeated model-download overhead across worker startup.
- Triton's bridge exposed only **9 of more than 40 vLLM metrics**, omitting token throughput,
  KV-cache utilization, and prefix-cache hits. Netflix added a proxy that merges Triton HTTP metrics
  with vLLM's on-disk metrics into one `/metrics` endpoint.
- Netflix uses batched C++ constrained decoding for structured output.

## Why it matters

The observability fix is the opposite of metric curation: the platform restored metrics hidden by an
integration boundary. A serving wrapper that exposes the expected API while dropping engine telemetry
is operationally incomplete.

## Tensions / open questions

- This is Netflix's account of its own platform rather than a comparative serving benchmark.
- A unified endpoint restores visibility but does not decide which metrics should page an operator.
- Version-pinned models, cache design, and constrained decoding remain workload-specific choices.

## Affected pages

- [[Inference Serving Engines]]
- [[ML Systems at Scale]]
- [[Serving Benchmarks and Goodput]]

## Citations

- Netflix Technology Blog, "In-House LLM Serving at Netflix", 2026-07-21.

## Raw capture

- [[2026-07-21 Netflix Technology Blog - In-House LLM Serving at Netflix|In-House LLM Serving at Netflix]]

## Related pages

- [[LLM Inference]]
- [[KV Cache]]
