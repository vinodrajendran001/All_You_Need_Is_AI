---
type: concept
created: 2026-08-24
updated: 2026-09-03
tags: [concept, inference, serving, llm-systems]
source_ids:
  - src-2026-08-24-bytebytego-ollama-vllm-sglang
  - src-2026-08-20-radixark-miles-v0-1
  - src-2026-06-26-nithin-llm-inference
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
  - src-2026-07-17-netflix-in-house-llm-serving
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
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

## Speculation is a runtime control surface, not a deploy-time flag

[[ByteByteGo - How to Make LLMs 3X Faster]] documents how vLLM actually operates speculative
decoding, and it is more dynamic than an on/off setting. The engine exposes a flag that disables
speculation above a configurable batch size, and supports **dynamic adjustment in which draft length
shrinks as concurrency rises and reaches zero under heavy load**.

This is worth recording as an engine capability rather than a speculative-decoding detail, because it
shows the class of control a serving engine is expected to provide: continuously re-deciding how much
spare capacity exists and re-shaping the workload to match, per step, without operator intervention.
The source frames it as routine operational tuning.

The design also reveals what engines can and cannot observe. Batch size is a cheap, directly measured
proxy for whether headroom exists. Whether a *given request* will draft well depends on its content —
structured output drafts well, open-ended prose does not — and no engine described in this vault
inspects that. Engines currently tune the supply side of speculation and ignore the demand side.

## Running an engine in-house is mostly not about the engine

[[Netflix - In-House LLM Serving]] describes a production platform built on vLLM and Triton, exposing
both OpenAI-compatible and gRPC interfaces. What makes it useful here is how little of the reported
work concerns engine selection, which is what this page otherwise spends its attention on.

The load-bearing problems were:

- **Version-pinned deployments and explicit compatibility boundaries**, so a model or API change
  cannot silently break clients. Once an engine serves many internal teams, the model is a versioned
  dependency and needs the release discipline of one.
- **An FSx-backed model cache**, removing repeated model-download cost at worker startup. Cold-start
  weight transfer is a real operational cost that benchmark comparisons of engines never surface.
- **A curated operational metric surface** distilled from vLLM's much larger metric set — the
  observability question is which handful of numbers an on-call engineer should act on, not how many
  the engine can emit.
- **Batched C++ constrained decoding** for structured output, treating schema conformance as a
  serving-layer capability rather than something to retry in application code.

The pattern worth carrying is that the engine-selection question this page answers is the *first*
decision and not the expensive one. Artifact management, schema evolution, and observability dominate
the ongoing cost, and none of them appear in a throughput comparison.

## What the engine is actually doing

[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]] gives the serving layer's
contribution in numbers: **continuous batching is worth up to 23× throughput** over naive fixed batching, and
**paged KV-cache blocks cut memory waste from 60–80% to under 4%**, yielding **2–4× throughput**. These are
the two mechanisms that separate a production engine from a loop calling `model.generate()`.

The consequential side effect is that **the engine's scheduling decisions reach the output**. Because numerics
depend on batch composition, **1,000 identical prompts at temperature 0 produced roughly 80 distinct
completions**. Determinism is not a sampling setting; it is a property of how the engine batched the request
that day. Anyone using an engine as a reproducible evaluation substrate is measuring the engine too — see
[[Multi-Turn Evaluation]] and [[Agentic Testing]].

## Related pages

- [[Netflix - In-House LLM Serving]]
- [[ByteByteGo - How to Make LLMs 3X Faster]]
- [[Speculative Decoding]]
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
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- [[Agentic Testing]]
- [[Inference Efficiency Frontier]]
