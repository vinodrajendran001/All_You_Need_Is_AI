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

## Engines dispatch on arithmetic intensity, not just on features

[[Changyi Yang - Why MLA and MTP Fight Each Other]] exposes a layer beneath the usual engine comparison. sglang's attention backend chooses between two **algebraically identical** MLA bracketings — expand the latent into K/V for a dense GEMM, or score directly against the wide latent — because their FLOP/byte profiles differ, with a crossover near 171 query tokens. Its DSA backend threshold defaults to exactly `index_topk = 2048`: below that, top-k selects everything and sparsity buys nothing, so the dense kernel wins.

Two implications for engine selection. First, an engine's real differentiator is often **how well its dispatch tracks the workload's position on the roofline** (see [[Arithmetic Intensity and the Roofline Model]]), which no feature checklist captures. Second, engine features interact rather than stack: speculative decoding and continuous batching both spend the compute a memory-bound decode leaves idle, so enabling both on an already high-intensity attention architecture can cost latency. That is a stronger form of this page's decision principle — configuration must be measured per workload, not per engine.

[[Jacob Peake - AI Chip Architectures]] extends the same point to hardware targets. Serving on SRAM-only accelerators ([[Cerebras]], [[Groq]]) inverts the usual assumptions: batching matters far less, KV cache competes directly with weights for the same scarce memory, and compiler constraints — static graphs, no dynamic shapes, no data-dependent control flow on the Cerebras stack — restrict which serving strategies are expressible at all.

## Related pages

- [[LLM Inference]]
- [[KV Cache]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Speculative Decoding]]
- [[Cerebras]]
- [[Groq]]
- [[Agentic Reinforcement Learning]]
- [[AI Agents in Production]]
- [[Software Performance Engineering]]

