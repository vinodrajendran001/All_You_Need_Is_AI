---
type: concept
created: 2026-08-24
updated: 2026-08-25
tags: [concept, inference, serving, llm-systems]
source_ids:
  - src-2026-08-24-bytebytego-ollama-vllm-sglang
  - src-2026-08-20-radixark-miles-v0-1
  - src-2026-06-26-nithin-llm-inference
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-25-jacob-peake-ai-chip-architectures
status: active
---

# Inference Serving Engines

## Definition

Inference serving engines load model weights, manage request scheduling and KV-cache memory, execute prefill and decode, and expose models to local applications or concurrent services.

## Workload-oriented selection

[[ByteByteGo - Ollama vs vLLM vs SGLang]] supplies a useful first-pass taxonomy:

- **Ollama** prioritizes easy local installation, model packaging, and developer workflows.
- **vLLM** prioritizes high-throughput GPU serving through paged KV memory and continuous batching.
- **SGLang** prioritizes structured generation and shared-prefix reuse for branching or multi-turn workloads.

These categories overlap and evolve. Selection should be benchmarked on the actual model, hardware, prompt-length distribution, output length, concurrency, latency objective, and deployment constraints.

[[RadixArk - Miles v0.1 Production-Level Post-Training]] shows why an engine also matters during post-training. Session-aware routing and RadixAttention reuse prefixes across multi-turn rollouts, while asynchronous rollout workers must receive updated weights without losing trajectory provenance.

## Decision principle

Developer convenience, single-request latency, throughput, structured execution, distributed operation, and training integration are different objectives. No engine is "fastest" independently of workload and measurement boundary.

## Related pages

- [[LLM Inference]]
- [[KV Cache]]
- [[Agentic Reinforcement Learning]]
- [[AI Agents in Production]]
- [[Software Performance Engineering]]

