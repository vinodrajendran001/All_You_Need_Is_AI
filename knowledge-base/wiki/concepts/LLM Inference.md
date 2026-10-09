---
type: concept
created: 2026-06-29
updated: 2026-10-09
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
  - src-2026-09-02-baseten-efficient-frontier-inference
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-09-08-cohere-megakernel-serving
  - src-2026-09-14-li-long-context-latency
  - src-2026-09-21-bytebytego-big-model-cheap-hardware
  - src-2026-09-10-lenz-epd-multimodal-serving
  - src-2026-10-08-bytebytego-netflix-genrec
status: active
---

# LLM Inference

## Definition

LLM inference runs a trained language model to produce representations, scores, or generated tokens.
For autoregressive generation, the key split is **two workloads, not one**: prompt-processing
**prefill** and token-by-token **decode**, often limited by compute and memory bandwidth respectively.
Those bottlenecks depend on workload and batching. A task-specific scoring head can stop after
prompt processing without a text-generation loop.

## Why it matters

Quantization, KV-cache compression, and serving-engine design address different sources of inference
cost. Long-prompt prefill often emphasizes arithmetic; low-batch dense decode often emphasizes memory
traffic. Neither is an invariant. This page connects [[KV Cache]], [[Model Quantization and Efficiency]],
and production serving by workload rather than by assuming one bottleneck for every deployment.

## Current synthesis

### The two phases of autoregressive generation

[[Nithin - What Actually Happens During LLM Inference]] gives a simplified starting model:

- **Prefill** processes prompt positions together, reusing weights across large matrix-matrix operations (**GEMMs**) and building [[KV Cache|KV state]] for later reuse. Sufficiently large operations are often compute-bound, but prompt/chunk size, attention implementation, and memory traffic still matter.
- **Decode** generates one new token per active sequence in an ordinary autoregressive iteration. Dense, low-batch execution has narrow matrix-vector work (**GEMV**) and often becomes memory-bandwidth-bound. Batched execution reuses weights across sequences, and attention architecture, sparse activation, and communication can change the limiting resource.

The roofline comparison is compute time versus memory-transfer time, not a rule that bytes always
win. [[Dwarkesh Patel - Reiner Pope Flashcards]] uses that lower-bound framing, while
[[Arithmetic Intensity and the Roofline Model]] also tracks regimes where decode arithmetic matters.
The October 9 lint removes the older unconditional bottleneck claims.

### Why the split drives every optimization

- **Weight compression** (see [[Model Quantization and Efficiency]] and [[Maarten Grootendorst - A Visual Guide to Quantization]]) shrinks the bytes that decode must move per token. The source lists AWQ and EXL2 (4-bit GPU serving, important weights kept higher-precision), FP8 (Hopper default) and NVFP4 (Blackwell) as native low-precision formats the cores compute on directly, and GGUF for consumer/split CPU-GPU running.
- **KV-cache compression** ([[KV Cache]], [[Siddhant Rai - TurboQuant - Online Vector Quantization]]) attacks the *other* growing object decode must read — the cache itself, which at long context can exceed model weights.
- **Loading format** matters: `mmap` can defer file reads and share file-backed pages. Mapping quickly does not remove cold-page I/O, first-use latency, or GPU transfer costs.
- [[Onur Sirin - How Local LLMs Run]] adds the most concrete **local hardware pipeline** version of this story. It breaks local inference into eight stages — cold load, tokenize, prefill, hold KV cache, decode one token, sample, repeat the generation loop, detokenize/stream — and maps each stage to its bottleneck. The durable refinement is that **capacity** and **bandwidth** are separate questions: a model may fit in memory, but decode speed depends on the bandwidth of the memory tier that actually holds the active weights and KV cache.

### Serving multiple users

Production engines must serve many concurrent requests:

- **vLLM and SGLang** focus on dynamic memory via **PagedAttention**, slicing the KV cache into pages and treating VRAM like OS virtual memory to stop fragmentation.
- **TensorRT-LLM and TGI** lean on graph compilation and custom kernels for raw throughput.
- **Continuous batching** admits and retires requests between iterations. Long prefills can interfere with active decodes on a shared worker; chunked prefill or separate workers can mitigate that contention. Pausing every decode for an entire new prompt is not inherent to the batching policy.

[[ByteByteGo - Ollama vs vLLM vs SGLang]] adds a workload-level serving taxonomy. Ollama optimizes low-friction local packaging and use; vLLM optimizes concurrent GPU serving through paged KV management and continuous batching; SGLang adds prefix-tree reuse and structured execution suited to repeated or branching agent contexts. The labels are not permanent feature boundaries, so [[Inference Serving Engines]] treats them as starting hypotheses to test against representative prompts, concurrency, latency targets, and hardware.

### Connections

- [[Reasoning Compression]] treats extra reasoning tokens as a systems cost: more sequential generation work and usually a larger KV cache, whether a particular decode is memory- or compute-limited.
- [[Small Language Models]] and [[On-Device Reasoning]] inherit this page's constraints in their most extreme form, where every token competes for memory and power.
- [[Alisa Liu - Book of LLMs]] adds an interview-oriented checklist of the inference toolbox that complements this hub: **batching & packing**, **speculative decoding** (a small draft model proposes tokens a large model verifies), **KV cache** and how to reduce its size, sampling strategies, and **Flash Attention** (IO-aware exact attention). It is a good rapid-review companion for the inference questions described in [[ML Research Interview Preparation]].
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]] supplies the layer beneath prefill/decode: the [[GPU Execution Model]]. Its low-arithmetic-intensity kernel example motivates measuring bytes moved and achieved bandwidth. It is an analogy for memory-bound decode, not a measurement of every LLM generation workload.
- **Streaming, not just batching, is now a serving axis.** [[ByteByteGo - Inside Thinking Machines Interaction Models]] shows real-time [[Real-Time Voice AI|interaction models]] served as 200 ms streaming sessions (a feature contributed to SGLang) with a fast interaction model paired with a slower background reasoning model. This adds a latency-anchored, continuous-input regime to the prefill/decode picture, where the scheduler must sustain sub-second responsiveness while a second model does deep work asynchronously.
- **Inference compute is also a reasoning scaling axis.** [[Test-Time Scaling]] (from [[Akhil Arora et al - Current Advances in LLM Reasoning]]) spends longer traces, more samples, search, and verification to seek better answers from a fixed model. That adds generation and state-management cost, motivating [[Reasoning Compression|budget control]] and work on parallel/speculative decoding and batched-inference determinism.
- **Local hardware adds a topology axis.** [[Onur Sirin - How Local LLMs Run]] distinguishes **flat/uniform memory** (Apple unified memory: one pool, one speed), **tiny-but-fast VRAM** (RTX 5090: very high GDDR bandwidth but little capacity), and **tiered coherent memory** (GB300: HBM fast tier plus LPDDR slow tier). This turns "does it fit?" into "does the active working set sit in the fast pool?"
- **Speculative decoding is the canonical decode-latency fix.** [[Speculative Decoding]] ([[Mayank Pratap Singh - Speculative Decoding in vLLM]]) exploits exactly the memory-bound property above: because verifying many tokens in parallel costs about the same weight-load as producing one, a small draft model can propose tokens the target verifies in a single pass — losslessly (same output distribution). It is a **low-load latency optimization** that serving stacks toggle off under saturation, and it is complementary to weight and KV compression (it cuts *weight-loads per token* rather than *bytes*).
- **The decode headroom is finite and shared.** [[Arithmetic Intensity and the Roofline Model]] is now the page that quantifies the framing above. Every optimization here — batching, speculation, multi-token prediction, cache-sharing attention — is a move along the same roofline, spending the compute a memory-bound decode leaves idle. [[Changyi Yang - Why MLA and MTP Fight Each Other]] shows the collision: DeepSeek-style MLA already sits at ~256 FLOP/B at a single query, above the H200 balance point of ~206, so stacking speculation on top pushes the workload past the knee where extra arithmetic costs latency instead of being free. [[Jacob Peake - AI Chip Architectures]] adds the hardware-side corollary that continuous batching does not escape this either: each user still reads their own cache, so long-context decode shifts from **weight-bandwidth-bound to KV-bandwidth-bound**, which is a different bottleneck than the one batching was introduced to fix.
- **The two phases can use separate workers.** [[Prefill-Decode Disaggregation]] ([[Wafer - AI Performance Engineering Resources]]) allows phase-specific hardware and scheduling when their requirements differ. It trades reduced interference for KV transfer and coordination cost; co-location is not inherently inferior. [[Serving Benchmarks and Goodput]] measures the trade by completions under a latency SLO rather than raw tokens per second.

- **Agent harnesses can hide inference latency behind their own tool calls.** [[Speculative Tool Execution]] ([[Alex L. Zhang - Speculative Programmatic Tool Calling]]) overlaps tool execution with the generation that requests it, by parsing calls out of a partially streamed program. When the tools are themselves sub-LLM calls, this turns two serial waits — generate, then execute — into one, and on a locally served model it spends decode compute that was otherwise idle. Measured gains are modest (1–1.2×) and highly workload-dependent, but the framing matters for this page: **for agent workloads, the latency that users feel is the harness's, not the engine's**, and the two are optimizable independently.

## What the bandwidth wall looks like in utilization terms

[[ByteByteGo - How to Make LLMs 3X Faster]] uses a dense 70B model at 16-bit precision:
roughly **140 GB of weights**. Its weight-read-per-token argument describes low-batch execution;
batching amortizes weight traffic across sequences, and sharding changes the per-device quantity.

The article quotes **90–95% compute utilization during prompt processing** and **20–40% during
generation** without a complete configuration. These are illustrative source claims, not fixed
utilization ranges or a measured budget of arithmetic available to every optimization.

In a memory-bound regime, bandwidth can matter more than peak compute. Batching, speculation, and
multi-token prediction can compete for the same spare capacity, but their actual gains require
measurement. Neither the hardware-buying rule nor additive speedups follow for every workload.

## A classifier for the techniques on this page

[[Philip Kiely - The Efficient Frontier of LLM Inference]] proposes one question that sorts every optimization
here: does it move a deployment **along** the latency-throughput frontier, or **push the frontier out**?

Tradeoff techniques — batch sizing, parallelism strategy — are allocation decisions requiring you to know what
the traffic values. Frontier-moving techniques — kernel optimization, disaggregation, and now speculative
decoding — are investments that can combine, but speedups need not multiply when they share a bottleneck. The frontier is also **jagged**: cutoff
points are unintuitive and must be found by empirical sweeps rather than derived. See
[[Inference Efficiency Frontier]] for the full treatment.

## The request path, end to end

[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]] walks the roughly twelve
stages between Enter and the first token, and fixes several numbers this page previously carried only
qualitatively.

**Prompt processing and generation contribute different costs.** Time to first token (**TTFT**)
also includes routing, queueing, and other work; time per output token (**TPOT**) summarizes the
later inter-token intervals. For `N >= 1` output tokens and mean TPOT, end-to-end latency is
approximately `TTFT + (N - 1) * TPOT`. The phases' bottlenecks depend on the workload rather than
being determined by the visible pause-versus-typing metaphor.

**Continuous batching is worth up to 23× throughput** over naive fixed batching.

**Temperature 0 is not deterministic.** Because numerics depend on batch composition, **1,000 identical
prompts produced roughly 80 distinct completions**. Reproducibility is a property of the serving
configuration, not of the sampling parameter — with direct consequences for evaluation; see
[[Multi-Turn Evaluation]] and the pass^k discussion on [[Agentic Testing]].

**Safety classification has a price on both axes.** An earlier production generation of input classifier cost
about **24% extra compute** and **+0.38 percentage points of false refusals**; the cascade design that
replaced it brings this to roughly **1%** and **0.05pp**.

**Tokenization is not neutral.** Roughly ¾ of a word per token on average, but token counts for the same
meaning differ by **up to 15×** across translations — so speakers of some languages get materially less usable
context and pay more for it.

These figures come from an explainer that attributes none of them to a specific paper or vendor; treat them as
illustrative of well-established effects rather than as citable measurements.

## Parallel transformer layers make a decode step easier to pack

[[Cohere - North Mini Code Megakernel Serving Engine]] surfaces an architecture/implementation coupling that is usually invisible.

**North Mini Code uses parallel transformer layers** — attention and MoE are computed from the same
normalised input and rejoined by a fused residual add plus RMSNorm. Because the two branches are
independent, there is **always unrelated work available to backfill a partial wave**, which is what makes
the megakernel's wave-quantisation win large: "200 tiles on 132 SMs means two waves for 1.5 waves of
work," and that waste is only recoverable if independent work exists to fill it.

The model's structure was chosen for modelling reasons; it turns out to determine how well the serving
path packs. That is the software-side analogue of the tile-geometry constraint in
[[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]], where head dimension determines MXU
utilisation.

**A second coupling runs through routing.** With **real expert distributions the megakernel speedup is
1.32x at batch 8 versus 1.14x under uniform routing**, because real requests concentrate on the same
experts, leaving sparser MoE work and therefore more bubbles to fill. The conclusion generalises beyond
megakernels: **"synthetic uniform routing therefore understates megakernel speedup on real traffic."**

## TTFT can change shape with context length

[[Jason Li - Latency Scaling Differences for GPT and Claude Models]] measures API-level TTFT up to
roughly 900K tokens. Three estimators find strong upward curvature for GPT-5.6 Terra and Sol, while
Claude Sonnet 5 is near-linear and noisy Opus 5 remains consistent with little curvature. This is
evidence about observed service behavior, not direct architecture: TTFT includes network, routing,
queueing, cache lookup, prefill, generation, and return latency.

The consequence is that one "milliseconds per input token" coefficient is insufficient. Long-context
benchmarks need a curve, cache conditions, and the provider/model version.

## Inference optimization is workload placement

[[ByteByteGo - How to Run a Big Model on Cheap Hardware]] separates weight bytes, active compute,
memory tiers, cache, and runtime kernels. [[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]]
adds a multimodal encoder stage whose independent placement helps image-heavy, short-output workloads
but can regress when decode or transfer dominates.

## A bounded output head can eliminate text decoding

[[ByteByteGo - How Netflix Taught an LLM to Recommend Movies]] describes GenRec as
**prefill-only inference**: an adapted LLM processes verbalized viewing context, then a learned
head scores catalog embeddings from a pooled hidden state. Top-K is computed from those scores,
not generated as item-name tokens.

This removes the autoregressive output loop, not the cost of the LLM or of scoring candidates.
The described vLLM deployment still benefits from shorter inputs and reusable prefixes; its
roughly one-third context length and similar serving-cost reduction are a reported workload
result, not a universal linear cost law.

The comparison boundary changes with the output interface. Generated tokens per second does not
measure this ranker's useful output; ranking quality, completed requests, and end-to-end latency
are the relevant quantities. Nor does a normalized score distribution establish calibration.
See [[Semantic Recommendation Systems]] and [[Serving Benchmarks and Goodput]].

## Open questions

- Where exactly is the prefill↔decode crossover for a given model/hardware? [[Prefill-Decode Disaggregation]] now covers the architectural answer, but the *scheduling* answer — when chunked prefill inside one pool beats splitting across two — still depends on interconnect bandwidth and traffic mix.
- Which weight + KV compression combinations give the best end-to-end tokens/sec without unacceptable quality loss?
- As context windows grow, does decode become so memory-bound that KV-cache compression matters more than weight quantization?
- Should serving stacks measure a workload's arithmetic intensity at runtime and gate batching, speculation, and attention-kernel dispatch on it, rather than configuring each independently?

## Related pages

- [[ByteByteGo - How Netflix Taught an LLM to Recommend Movies]]
- [[Semantic Recommendation Systems]]
- [[Netflix]]
- [[ByteByteGo - How to Make LLMs 3X Faster]]
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
- [[Inference Efficiency Frontier]]
- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- [[Agentic Testing]]
- [[Cohere - North Mini Code Megakernel Serving Engine]]
- [[Megakernels]]
- [[Cohere]]
