---
type: concept
created: 2026-06-29
updated: 2026-08-27
tags:
  - concept
  - llm
  - inference
  - serving
  - efficiency
source_ids:
  - src-2026-06-26-nithin-llm-inference
  - src-2026-06-29-maarten-grootendorst-visual-guide-quantization
  - src-2026-06-29-siddhant-rai-turboquant
  - src-2026-06-30-alisa-liu-book-of-llms
  - src-2026-07-03-bytebytego-thinking-machines-interaction
  - src-2026-07-03-fergus-finn-cuda-kernel
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-06-30-onur-sirin-local-llm-memory-hardware
  - src-2026-07-06-mayank-pratap-singh-speculative-decoding
  - src-2026-08-24-bytebytego-ollama-vllm-sglang
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
status: active
---

# LLM Inference

## Definition

LLM inference is the runtime process of turning a prompt into generated tokens. Its defining property is that it is **two workloads, not one**: a compute-bound **prefill** phase that processes the whole prompt at once, and a memory-bound **decode** phase that emits one token at a time. Optimizing inference means optimizing these two phases separately, because they hit opposite hardware limits.

## Why it matters

Most efficiency techniques in the vault only make sense once this split is clear. Quantization, KV-cache compression, and serving-engine design are all responses to the fact that decode is throttled by memory bandwidth, while prefill is throttled by arithmetic throughput. This page is the hub that ties [[KV Cache]], [[Model Quantization and Efficiency]], and production serving together at the runtime level.

## Current synthesis

### The two phases

[[Nithin - What Actually Happens During LLM Inference]] gives the clearest statement:

- **Prefill** — the engine processes the entire prompt in parallel as a large matrix-matrix multiply (**GEMM**). It is **compute-bound**: speed is set by how many FLOPS the accelerator can run. Prefill's job is setup — it computes and stores the prompt's attention states into the [[KV Cache]] so they are never recomputed.
- **Decode** — the engine generates one token at a time as a matrix-vector multiply (**GEMV**). To produce a single token it must re-read the entire multi-gigabyte weight file from VRAM plus the growing KV cache. It is **memory-bandwidth-bound**: the math finishes instantly and the cores starve waiting on High Bandwidth Memory (HBM).

This is why per-token latency in long generations is governed by *bytes moved*, not *operations done*. It is the same memory-bound framing that [[Dwarkesh Patel - Reiner Pope Flashcards]] expresses as "per-token latency is the max of compute time and memory time."

### Why the split drives every optimization

- **Weight compression** (see [[Model Quantization and Efficiency]] and [[Maarten Grootendorst - A Visual Guide to Quantization]]) shrinks the bytes that decode must move per token. The source lists AWQ and EXL2 (4-bit GPU serving, important weights kept higher-precision), FP8 (Hopper default) and NVFP4 (Blackwell) as native low-precision formats the cores compute on directly, and GGUF for consumer/split CPU-GPU running.
- **KV-cache compression** ([[KV Cache]], [[Siddhant Rai - TurboQuant - Online Vector Quantization]]) attacks the *other* growing object decode must read — the cache itself, which at long context can exceed model weights.
- **Loading format** matters: `mmap` maps the weight file into virtual memory and lazily loads pages on demand, giving near-zero startup and shared physical memory across processes.
- [[Onur Sirin - How Local LLMs Run]] adds the most concrete **local hardware pipeline** version of this story. It breaks local inference into eight stages — cold load, tokenize, prefill, hold KV cache, decode one token, sample, repeat the generation loop, detokenize/stream — and maps each stage to its bottleneck. The durable refinement is that **capacity** and **bandwidth** are separate questions: a model may fit in memory, but decode speed depends on the bandwidth of the memory tier that actually holds the active weights and KV cache.

### Serving multiple users

Production engines must serve many concurrent requests:

- **vLLM and SGLang** focus on dynamic memory via **PagedAttention**, slicing the KV cache into pages and treating VRAM like OS virtual memory to stop fragmentation.
- **TensorRT-LLM and TGI** lean on graph compilation and custom kernels for raw throughput.
- **Continuous batching** injects new prefill tasks directly into ongoing decode loops to keep utilization high. Because prefill saturates the tensor cores, active users' decode briefly pauses while a new prompt's prefill runs — a direct consequence of the compute-bound/memory-bound conflict.

[[ByteByteGo - Ollama vs vLLM vs SGLang]] adds a workload-level serving taxonomy. Ollama optimizes low-friction local packaging and use; vLLM optimizes concurrent GPU serving through paged KV management and continuous batching; SGLang adds prefix-tree reuse and structured execution suited to repeated or branching agent contexts. The labels are not permanent feature boundaries, so [[Inference Serving Engines]] treats them as starting hypotheses to test against representative prompts, concurrency, latency targets, and hardware.

### Connections

- The decode/memory-bound view is why [[Reasoning Compression]] treats reasoning tokens as a systems cost: more tokens means more memory-bound decode steps and a larger KV cache.
- [[Small Language Models]] and [[On-Device Reasoning]] inherit this page's constraints in their most extreme form, where every token competes for memory and power.
- [[Alisa Liu - Book of LLMs]] adds an interview-oriented checklist of the inference toolbox that complements this hub: **batching & packing**, **speculative decoding** (a small draft model proposes tokens a large model verifies), **KV cache** and how to reduce its size, sampling strategies, and **Flash Attention** (IO-aware exact attention). It is a good rapid-review companion for the inference questions described in [[ML Research Interview Preparation]].
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]] supplies the layer *beneath* prefill/decode: the [[GPU Execution Model]]. Its arithmetic-intensity argument (a low-FLOP kernel runs at ~80% DRAM bandwidth but ~5% issue activity) is exactly why decode — one GEMV re-reading gigabytes per token — is memory-bound, and why "bytes moved" is the right currency for reasoning about tokens/sec.
- **Streaming, not just batching, is now a serving axis.** [[ByteByteGo - Inside Thinking Machines Interaction Models]] shows real-time [[Real-Time Voice AI|interaction models]] served as 200 ms streaming sessions (a feature contributed to SGLang) with a fast interaction model paired with a slower background reasoning model. This adds a latency-anchored, continuous-input regime to the prefill/decode picture, where the scheduler must sustain sub-second responsiveness while a second model does deep work asynchronously.
- **Inference compute is also a *reasoning* scaling axis.** [[Test-Time Scaling]] (from [[Akhil Arora et al - Current Advances in LLM Reasoning]]) spends extra decode — longer traces, more samples, explicit search, verifiers — to get better answers from a fixed model. That directly stresses this page's constraints: more reasoning tokens mean more memory-bound decode steps and a larger KV cache, which is why the field pairs it with [[Reasoning Compression|budget control]] and with systems work on parallel/speculative decoding and batched-inference determinism (CacheSaver, Parallel-R1).
- **Local hardware adds a topology axis.** [[Onur Sirin - How Local LLMs Run]] distinguishes **flat/uniform memory** (Apple unified memory: one pool, one speed), **tiny-but-fast VRAM** (RTX 5090: very high GDDR bandwidth but little capacity), and **tiered coherent memory** (GB300: HBM fast tier plus LPDDR slow tier). This turns "does it fit?" into "does the active working set sit in the fast pool?"
- **Speculative decoding is the canonical decode-latency fix.** [[Speculative Decoding]] ([[Mayank Pratap Singh - Speculative Decoding in vLLM]]) exploits exactly the memory-bound property above: because verifying many tokens in parallel costs about the same weight-load as producing one, a small draft model can propose tokens the target verifies in a single pass — losslessly (same output distribution). It is a **low-load latency optimization** that serving stacks toggle off under saturation, and it is complementary to weight and KV compression (it cuts *weight-loads per token* rather than *bytes*).
- **The decode headroom is finite and shared.** [[Arithmetic Intensity and the Roofline Model]] is now the page that quantifies the framing above. Every optimization here — batching, speculation, multi-token prediction, cache-sharing attention — is a move along the same roofline, spending the compute a memory-bound decode leaves idle. [[Changyi Yang - Why MLA and MTP Fight Each Other]] shows the collision: DeepSeek-style MLA already sits at ~256 FLOP/B at a single query, above the H200 balance point of ~206, so stacking speculation on top pushes the workload past the knee where extra arithmetic costs latency instead of being free. [[Jacob Peake - AI Chip Architectures]] adds the hardware-side corollary that continuous batching does not escape this either: each user still reads their own cache, so long-context decode shifts from **weight-bandwidth-bound to KV-bandwidth-bound**, which is a different bottleneck than the one batching was introduced to fix.
- **The two phases can be split onto separate hardware entirely.** [[Prefill-Decode Disaggregation]] ([[Wafer - AI Performance Engineering Resources]]) takes the asymmetry above to its architectural conclusion: because prefill is compute-bound and decode is memory-bound, co-locating them forces one configuration — one batch policy, one parallelism strategy, one chip choice — to serve two opposite workloads badly. Splitting them lets each pool be sized and scheduled for its own regime, at the cost of transferring the KV cache between them, which converts a scheduling problem into an interconnect problem. The same source supplies the metric the trade-off is judged on: [[Serving Benchmarks and Goodput]], where success is completions *under a latency SLO* rather than raw tokens per second.

- **Agent harnesses can hide inference latency behind their own tool calls.** [[Speculative Tool Execution]] ([[Alex L. Zhang - Speculative Programmatic Tool Calling]]) overlaps tool execution with the generation that requests it, by parsing calls out of a partially streamed program. When the tools are themselves sub-LLM calls, this turns two serial waits — generate, then execute — into one, and on a locally served model it spends decode compute that was otherwise idle. Measured gains are modest (1–1.2×) and highly workload-dependent, but the framing matters for this page: **for agent workloads, the latency that users feel is the harness's, not the engine's**, and the two are optimizable independently.

## Open questions

- Where exactly is the prefill↔decode crossover for a given model/hardware? [[Prefill-Decode Disaggregation]] now covers the architectural answer, but the *scheduling* answer — when chunked prefill inside one pool beats splitting across two — still depends on interconnect bandwidth and traffic mix.
- Which weight + KV compression combinations give the best end-to-end tokens/sec without unacceptable quality loss?
- As context windows grow, does decode become so memory-bound that KV-cache compression matters more than weight quantization?
- Should serving stacks measure a workload's arithmetic intensity at runtime and gate batching, speculation, and attention-kernel dispatch on it, rather than configuring each independently?

## Related pages

- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[Nithin - What Actually Happens During LLM Inference]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Maarten Grootendorst - A Visual Guide to Quantization]]
- [[Siddhant Rai - TurboQuant - Online Vector Quantization]]
- [[Alisa Liu - Book of LLMs]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[Reasoning Compression]]
- [[AI Accelerator Architecture]]
- [[GPU Execution Model]]
- [[Real-Time Voice AI]]
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]]
- [[ByteByteGo - Inside Thinking Machines Interaction Models]]
- [[Test-Time Scaling]]
- [[LLM Reasoning]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[Onur Sirin - How Local LLMs Run]]
- [[Speculative Decoding]]
- [[Mayank Pratap Singh - Speculative Decoding in vLLM]]
- [[Transformer Architecture]]
- [[AI Knowledge Base Overview]]
- [[Inference Serving Engines]]
- [[ByteByteGo - Ollama vs vLLM vs SGLang]]
- [[Prefill-Decode Disaggregation]]
- [[Serving Benchmarks and Goodput]]
- [[Wafer - AI Performance Engineering Resources]]
- [[Speculative Tool Execution]]
- [[Programmatic Tool Calling]]
