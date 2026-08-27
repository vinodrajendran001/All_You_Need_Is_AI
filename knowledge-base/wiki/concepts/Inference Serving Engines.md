---
type: concept
created: 2026-08-24
updated: 2026-08-27
tags: [concept, inference, serving, llm-systems]
source_ids:
  - src-2026-08-24-bytebytego-ollama-vllm-sglang
  - src-2026-08-20-radixark-miles-v0-1
  - src-2026-06-26-nithin-llm-inference
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
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

## The mechanisms underneath the engine names

[[Wafer - AI Performance Engineering Resources]] supplies the primary papers for the techniques this page has so far described mainly by engine name:

- **Continuous batching** — Orca, which introduced iteration-level scheduling so finished sequences leave the batch and new ones join without waiting for the slowest member.
- **Paged KV memory** — PagedAttention/vLLM, which applies virtual-memory paging to the [[KV Cache]] and removes the fragmentation that forced conservative batch sizes.
- **Chunked prefill** — Sarathi-Serve, which slices long prefills so they interleave with decode instead of stalling it.
- **Prefix reuse** — SGLang/RadixAttention, which shares cached prefixes across requests that begin the same way — the dominant win for agent and chat workloads with repeated system prompts.
- **Splitting the phases entirely** — [[Prefill-Decode Disaggregation]], the architectural alternative to interleaving them on one pool.

Knowing which mechanism an engine implements is more durable knowledge than knowing which engine is currently fastest: benchmark leadership rotates, the mechanisms do not. Whether a given engine's advantage is real is a question for [[Serving Benchmarks and Goodput]], which supplies the evidence standard a serving comparison has to meet.

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
- Wafer - AI Performance Engineering Resources
- Prefill-Decode Disaggregation
- Serving Benchmarks and Goodput
- GPU Kernel Optimization
