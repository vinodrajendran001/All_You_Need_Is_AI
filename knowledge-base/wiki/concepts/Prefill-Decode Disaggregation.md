---
type: concept
created: 2026-08-26
updated: 2026-08-26
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
status: active
---

# Prefill-Decode Disaggregation

## Definition

**Prefill-decode disaggregation** is the practice of running the two phases of autoregressive inference on separate workers — or separate machines — instead of interleaving them on the same GPU. Prefill processes the whole prompt in one compute-bound pass; decode emits one token at a time and is memory-bandwidth-bound. Disaggregation treats them as two different workloads that happen to share a model, and moves the [[KV Cache]] between them.

## Why it matters

This concept answers a question the vault had previously only *posed*. [[LLM Inference]] listed "how should schedulers exploit the prefill↔decode crossover" as an open question; disaggregation is the architectural answer that production systems converged on.

The motivation follows directly from [[Arithmetic Intensity and the Roofline Model]]. Prefill sits far above the roofline ridge and wants maximum FLOPs; decode sits far below it and wants maximum memory bandwidth and batch size. Colocating them means one phase always runs on hardware tuned for the other, and — worse — a long prefill blocks decode steps for every other request sharing the GPU, inflating tail latency. That interference is the specific pain the technique removes.

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

## Open questions

- What is the crossover point at which KV transfer cost exceeds the interference cost it avoids, and how does it move with model size, context length, and attention variant?
- Does disaggregation favour heterogeneous fleets — cheaper high-bandwidth parts for decode, dense compute for prefill — and is that economical outside the largest deployments?
- How should prefix caching and cache reuse work when the cache lives on a different machine from the decoder that needs it?
- Chunked prefill and full disaggregation solve overlapping problems; when is the simpler single-worker mitigation sufficient?
- How does disaggregation interact with expert parallelism in [[Mixture of Experts]] serving, where routing already imposes its own communication pattern?

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
