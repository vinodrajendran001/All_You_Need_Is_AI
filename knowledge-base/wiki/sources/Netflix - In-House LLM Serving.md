---
type: source-summary
created: 2026-08-03
updated: 2026-08-03
source_id: src-2026-07-17-netflix-in-house-llm-serving
source_title: "In-House LLM Serving at Netflix"
source_author: Netflix Technology Blog
source_url: https://netflixtechblog.com/in-house-llm-serving-at-netflix-a5a8e799ea2c
tags: [source-summary, serving, vllm, netflix]
source_ids: [src-2026-07-17-netflix-in-house-llm-serving]
status: active
---

# Netflix - In-House LLM Serving

## Summary

Netflix describes an internal LLM-serving platform built around vLLM and Triton, exposing both OpenAI-compatible and gRPC interfaces. The production work is less about hosting a model once than managing model artifacts, API/schema evolution, constrained output, and useful observability.

## Key claims

- Version-pinned deployments and compatibility boundaries prevent model/API changes from silently breaking clients.
- An FSx-based model cache reduces repeated model-download overhead across worker startup.
- Netflix curates a smaller operational metric surface from vLLM's large metric set and uses batched C++ constrained decoding for structured output.

## Affected pages

- [[LLM Inference]]
- [[ML Systems at Scale]]
- [[KV Cache]]

## Citations

- Raw capture: `knowledge-base/raw/sources/In-House LLM Serving at Netflix.md`

## Related pages

- [[LLM Inference]]
- [[ML Systems at Scale]]
- [[KV Cache]]
