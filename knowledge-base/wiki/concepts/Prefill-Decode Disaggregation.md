---
type: concept
created: 2026-08-26
updated: 2026-10-09
tags:
  - concept
  - inference
  - serving
  - distributed-systems
  - scheduling
source_ids:
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-06-26-nithin-llm-inference
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-09-02-baseten-efficient-frontier-inference
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-09-07-semianalysis-tpu-inferencex
  - src-2026-09-10-lenz-epd-multimodal-serving
  - src-2026-09-24-modal-quail-billion-tokens-per-minute
status: active
---

# Prefill-Decode Disaggregation

## Definition

**Prefill-decode disaggregation** runs prompt processing and autoregressive generation on separate
workers, potentially on separate machines, and transfers [[KV Cache|KV state]] between them.
Prefill and decode often have different compute, memory, and scheduling requirements, but their
bottlenecks depend on the model, batching, context, and hardware.

## Why it matters

This is one architectural response to the scheduling question on [[LLM Inference]], not a
replacement for workload-specific comparison with co-location and chunked prefill.

[[Arithmetic Intensity and the Roofline Model]] explains a common motivation: long-prompt prefill
can emphasize compute while low-batch dense decode emphasizes bandwidth. Long prefills can also
delay active decodes on a shared worker. Separate pools permit independent provisioning and reduce
that interference, but the benefit must exceed transfer and coordination cost. The October 9 lint
removes the earlier claim that co-location always mis-provisions one phase.

## The lineage

[[Wafer - AI Performance Engineering Resources]] traces a two-stage progression, and the distinction between the stages matters:

**Stage 1 — mitigate interference within one worker.** Sarathi-Serve splits a long prefill into chunks so decode steps can be interleaved between them. Orca's iteration-level scheduling and vLLM's paged KV allocation make this practical by letting the batch change composition every step. The phases still share a GPU; the scheduler simply stops letting prefill monopolize it.

**Stage 2 — separate the workers outright.**

| System | Contribution |
| --- | --- |
| DistServe | Separate prefill and decode workers, each optimized for goodput under latency constraints |
| Splitwise | Phase-specific hardware allocation and scheduling |
| Mooncake | A KV-centric disaggregated architecture with a distributed cache and data plane |
| NIXL | A transport layer for moving inference state across memory and network backends |
| Dynamo | A current production implementation of disaggregated serving |

The through-line is that **the KV cache becomes the unit of transfer**, which is why Mooncake is filed under both KV cache systems and disaggregation in the source, and why CacheGen's KV compression-for-transfer belongs to the same problem.

## The cost that replaces the benefit

Disaggregation does not remove the bottleneck; it relocates it. Once prefill and decode are on different machines, every request must ship its KV cache across an interconnect between phases. That makes the technique a bet:

- it wins when the interconnect is fast relative to the interference it removes — which is why it emerged alongside rack-scale coherent domains and rising NIC bandwidth (see [[NVIDIA]] and [[AI Accelerator Architecture]]);
- it degrades when KV state is large or the network is ordinary, which is what pushes teams toward smaller KV footprints via grouped-query or latent attention, and toward compressed transfer.

This is the same headroom trade recorded elsewhere in the vault: an optimization that looks free in isolation is competing for a shared resource, here the interconnect rather than idle decode compute.

## Why the two phases separate at all

[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]] uses a
pause-versus-typing metaphor for prefill and decode. It is pedagogical, not a bottleneck test:
time to first token includes other request-path work, and batching or attention design can change
decode's compute/memory balance.

[[Philip Kiely - The Efficient Frontier of LLM Inference]] classifies disaggregation as a **frontier-moving**
technique rather than a tradeoff: separating the phases lets each worker be tuned for its own characteristics,
and lets the **ratio between prefill and decode workers** be matched to actual input/output sequence lengths
and cache hit rates. Its observed effect in practice is *"increasing throughput while keeping latencies the
same or slightly better"* — which is what distinguishes it from a technique that merely buys one with the
other. See [[Inference Efficiency Frontier]].

## Disaggregation is a roadmap item on TPU, and comparing across it distorts benchmarks

[[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]] records TPU prefill-decode disaggregation arriving as **TPU-Sync** (formerly
TPU-raiden), a zero-copy transfer through native PJRTBuffer descriptors — still roadmap rather than
shipped at time of writing, alongside KV cache offloading to DRAM and Mooncake Store P2P pooling.

The benchmarking consequence is the durable lesson. SemiAnalysis's most favourable NVIDIA comparison is
explicitly labelled **"apples-to-bananas": a GB300 NVL72 disaggregated configuration against an aggregated
TPUv7 one**, and it **reverses the headline result** — GB300 comes out roughly **30% ahead on perf/$ in
the middle of the curve**, against the up-to-50% TPU advantage claimed elsewhere in the same article.
Whether the competitor is disaggregated is not a detail; here it is worth more than the hardware
difference.

## Multimodal serving adds an encoder placement decision

[[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]] separates vision encoding from
prefill/decode. In one NVIDIA setup, heterogeneous EPD served 70% more traffic at an ITL-under-100-ms
SLO, but colocated E2E gain fell from +11.8% to -2.5% as output length rose. Disaggregation helps
only while recovered encoder contention exceeds embedding-transfer and coordination overhead.

## Delete one phase and the whole design space has nothing left to arbitrate

Disaggregation presupposes two phases worth separating. [[Modal - Hitting a Billion Tokens per Minute on One GPU]] is a boundary
case, because its workload has only one. Quail serves AI-SQL — prompts built from database rows,
returning a relation — and the queries are Boolean filters and classifications that need **a single
output token**. Modal is explicit about what follows: **no separate prefill and decode phases, no
prefill-decode disaggregation, no sampling, no CUDA Graph capture and no speculative decoding**.

This inverts the page's cost analysis rather than contradicting it. Here the KV cache is not the unit
of transfer between phases; **suffix KV is never written at all**, and what caching exists serves
cross-request reuse of shared join anchors within a known query plan. With no decode to protect,
chunked prefill has nothing to interleave, DistServe-style worker separation has nothing to separate,
and the interconnect bet described above is never placed. The device can instead be provisioned
for the remaining scoring workload.

The useful generalisation is narrow and should stay narrow. Nothing here argues against
disaggregating chat or agent serving; Modal in fact reports Quail **falling behind vLLM on an
agent-trace benchmark**, and its headline of **over a billion tokens processed per minute per H100
with more than 10x vLLM** belongs to **one multi-join query**, against **1.84x geometrically
averaged** across
the released benchmark. What the case complicates is the habit of treating the prefill/decode split
as an invariant of LLM serving. Classification, filtering, reranking and judging are prefill-dominant
workloads, and [[Philip Kiely - The Efficient Frontier of LLM Inference]]'s point above — that the
**ratio** of prefill to decode workers should match actual input/output lengths — already implies
that ratio can run to its limit. At the limit, the technique's premise disappears.

Caveats belong with it: the workload is unusually favourable by Modal's own description (known
structure, shared prefixes, zero decode, structured outputs reduced to an **8-option output
vocabulary**, low latency sensitivity), full SQL execution support was not yet implemented, and all
figures are vendor-reported.

## Open questions

- What is the crossover point at which KV transfer cost exceeds the interference cost it avoids, and how does it move with model size, context length, and attention variant?
- Does disaggregation favour heterogeneous fleets — cheaper high-bandwidth parts for decode, dense compute for prefill — and is that economical outside the largest deployments?
- How should prefix caching and cache reuse work when the cache lives on a different machine from the decoder that needs it?
- Chunked prefill and full disaggregation solve overlapping problems; when is the simpler single-worker mitigation sufficient?
- How does disaggregation interact with expert parallelism in [[Mixture of Experts]] serving, where routing already imposes its own communication pattern?
- What share of production LLM calls emit only a handful of tokens — classification, filtering, judging, routing — and does the disaggregation literature's benchmark mix represent them at all?
- When a fleet mixes prefill-only classification with long-decode chat, is the right answer disaggregated workers or two separate pools running different engines?

## Related pages

- [[Wafer - AI Performance Engineering Resources]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Serving Benchmarks and Goodput]]
- [[Distributed Training Parallelism]]
- [[Mixture of Experts]]
- [[AI Accelerator Architecture]]
- [[Inference Efficiency Frontier]]
- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- [[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]]
- [[SemiAnalysis]]
- [[Modal - Hitting a Billion Tokens per Minute on One GPU]]
