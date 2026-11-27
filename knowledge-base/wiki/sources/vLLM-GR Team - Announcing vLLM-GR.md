---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-24-vllm-gr-announcement
source_title: "Announcing vLLM-GR: Efficient Inference for Generative Recommendation"
source_author: vLLM-GR Team
source_url: https://vllm.ai/blog/2026-11-24-vllm-gr-announcement
tags:
  - source/summary
  - recommendation-systems
  - inference
  - serving
  - kv-cache
source_ids:
  - src-2026-11-24-vllm-gr-announcement
status: active
---

# Announcing vLLM-GR: Efficient Inference for Generative Recommendation

## Summary

The vLLM blog announces vLLM-GR, an open-source framework built on vLLM for serving **generative
recommendation** models, which generate item IDs from a user's history instead of text. The worked
example is OneRec-1.7B producing **128 candidate semantic IDs (SIDs)** for a video feed. The engine adds
a beam session, owned by EngineCore, that runs a whole beam search inside one request. It shares the
prompt's KV cache across beams, selects candidates on the accelerator, prepares each stage on the host
while the device runs the previous one, and can restrict generation to SIDs present in the item
catalog. The evidence is P99 latency charts on four NVIDIA GPUs and two Ascend NPUs, against SGLang
Beam, NVIDIA SID-GR and xLLM. vLLM-GR has the lowest P99 at beam width 256 and batch sizes 4 and 8 on all
six accelerators, but not at batch 1 or consistently at beam width 128. The post says its runs used
"different timing definitions, sample counts, and backend settings". It is first-party, with no
throughput or recommendation-quality results.

## Key claims

### The workload: few tokens, many paths

A recommendation service must turn a long interaction history into a set of candidates within one
request's latency budget. Generating each item ID "may take only a few tokens, yet the engine must
explore many paths and return items the application can serve". The post gives three goals: reuse
vLLM's model execution, scheduling and paged KV cache from offline evaluation to online serving; cut
the cost of wide candidate searches; and keep results aligned with the item catalog, with "support for
model and catalog updates". The overview names OneRec-1.7B, HSTU and OneTrans as model examples.

### Inside the engine

- **EngineCore owns each beam session** from admission to completion. At each stage the model runner
  scores the next token, and beam selection records the score and parent of each surviving path. The
  next decode uses those parent indices to read the right KV state.
- **Prompt KV is shared across beams**, which "avoids copying the viewer's history for each
  candidate". The architecture figure lists BeamAttn and suffix KV among the additions, and the second
  decode "inherits the selected parents' suffix KV".
- **Prefill-decode-decode (PDD) pipeline.** While the accelerator executes one stage, the host prepares
  the next, "reducing the wait between decode steps". Beam selection runs on the accelerator, cutting
  per-step coordination with the host.
- **Search modes.** Search runs over the full vocabulary or is restricted to SIDs in the item catalog.
  Per-stage beam widths and per-parent candidate limits let a service explore more partial IDs than it
  returns. In an illustrative example, beam widths of 2 → 3 → 2 return two SIDs, and the catalog
  rejects the prefix `A1 · B1` "because no item starts with that prefix".
- **Interfaces.** A complete beam search can be submitted through an offline Python interface,
  OpenAI-compatible HTTP or gRPC, and returns candidates and scores in one response. vLLM-GR 0.30.0 is
  built on vLLM 0.30.0 and supports NVIDIA GPUs and Ascend NPUs.

### Benchmarks: P99 latency under mixed protocols

- The overview charts hold input at **1,024 tokens** and compare beam widths **256** and **128** at
  batch sizes 1, 4 and 8, on H20, RTX PRO 6000, A100, L20, Ascend A2 and Ascend A5.
- Only the RTX PRO 6000 protocol is fully stated: OneRec-1.7B in BF16 generating three tokens from the
  same synthetic inputs, with catalog constraints disabled. Each point is whole-batch P99 over **48
  timed batches** after three warmups, including returning IDs and scores to the host but excluding
  HTTP. vLLM-GR and SID-GR used a candidate pool *K* equal to the beam width *W*; SGLang Beam used its
  native pool of *2W*.
- On A2 and A5, vLLM-GR and xLLM used a catalog constraint table, and SGLang's setting "was not
  recorded". L20 sample counts ranged from **100 to 1,000** timed batches per configuration. Backend
  revisions, and warmup counts outside the RTX PRO 6000 run, are not specified.

| Accelerator | Configuration | Reported P99 |
| --- | --- | --- |
| H20 | BW256, B8 | vLLM-GR **369.4 ms**; SGLang 1,280.1 ms; SID-GR 428.1 ms |
| H20 | BW256, B4 | vLLM-GR and SID-GR both about 191 ms |
| RTX PRO 6000 | BW256, B1 | SID-GR **28.25 ms**; vLLM-GR 29.21 ms |
| A100 | BW128, B8 | SID-GR **199.0 ms**; vLLM-GR 209.7 ms |
| A100 | BW256, B8 | vLLM-GR **274.5 ms**; SID-GR 451.5 ms |
| L20 | BW256, B8 | vLLM-GR **474.3 ms**; SID-GR 790.7 ms |
| A2 | BW256, B8, constraints on | vLLM-GR **312.69 ms**; xLLM 324.60 ms |
| A5 | B8 | vLLM-GR 128.2 ms (BW128) and 151.7 ms (BW256) |

At beam width 128, "the lowest-latency backend varies by accelerator and batch size". SID-GR had the
lowest P99 at batch 1 on RTX PRO 6000 for both overview widths. On A5, vLLM-GR was lowest at all three
batch sizes for both widths. Some A2 curves end where runs exceeded device memory; at 8,192 input
tokens and batch 8, vLLM-GR completed the beam-width sweep through 1,024.

### Roadmap, not shipped

The roadmap lists candidate scoring for HSTU, MTGR and RankMixer, native OneTrans serving, and MoE
models. It also lists value-aware selection and variable-length generation that stops individual beams
at EOS and releases their slots and KV. Further items: an online batching scheduler, prefill for
histories of **10,000 tokens or more**, linear or sparse attention, reuse of an unchanged history
prefix's KV **across requests**, a distributed KV cache, and closer integration with upstream vLLM.

## Why it matters

[[Semantic Recommendation Systems]] records YouTube PLUM's generated semantic IDs and the
invalid-ID and catalog-update problems they bring. vLLM-GR is a serving engine for that generation
path, and its catalog constraint is a concrete, partial answer to invalid IDs. In
[[Inference Serving Engines]], it is the opposite design from Netflix GenRec's prefill-only catalog
scoring: the engine keeps a short decode loop but makes it wide, and owns the whole search. For
[[KV Cache]], prompt sharing across beams is prefix reuse within one request; reuse across requests is
still roadmap. For [[Serving Benchmarks and Goodput]], it is a chart family whose own text disclaims
comparability across panels.

## Tensions / open questions

- **First-party, with unequal comparators.** The framework's developers ran the benchmarks. SGLang
  Beam used a 2W candidate pool, constraints were on for some backends on Ascend and unrecorded for
  SGLang, and only one platform's protocol is fully specified.
- **Best slice as headline.** "Lowest P99 at batch sizes 4 and 8 on all six accelerators" holds at
  beam width 256. At batch 1 and at beam width 128 the winner varies.
- **What is not shown:** throughput, candidate recall or recommendation quality, cost, a
  constraints-on comparison on NVIDIA, and HTTP or gRPC overhead.
- **Catalog freshness is asserted, not shown.** The post claims support for model and catalog updates
  but describes no update mechanism or refresh latency.
- **Deployment claims are unquantified.** The acknowledgements thank teams including TikTok-Global
  E-commerce and ByteDance-Commerce & Advertising for "experience and feedback from large-scale
  production deployments". No deployment is described or measured.
- The RTX PRO 6000 run generated three tokens per SID; how latency scales with deeper SID hierarchies is
  listed as roadmap.

## Affected pages

- [[Semantic Recommendation Systems]]
- [[Inference Serving Engines]]
- [[KV Cache]]
- [[Serving Benchmarks and Goodput]]

## Raw capture

- [[knowledge-base/raw/sources/Announcing vLLM-GR Efficient Inference for Generative Recommendation]]

## Citations

- Canonical URL: <https://vllm.ai/blog/2026-11-24-vllm-gr-announcement> (the capture's `utm_source`
  parameter removed).
- Byline "vLLM-GR Team" on the vLLM blog; published 2026-11-24; captured 2026-11-26. The capture links
  the project repository, `vllm-project/vllm-gr` on GitHub.

## Related pages

- [[Semantic Recommendation Systems]]
- [[Inference Serving Engines]]
- [[KV Cache]]
- [[Serving Benchmarks and Goodput]]
- [[ByteByteGo - How Netflix Taught an LLM to Recommend Movies]]
- [[ByteByteGo - How to Fight Clickbait - Meta, LinkedIn and YouTube Case Studies]]
- [[ML Systems at Scale]]
- [[Mixture of Experts]]
- [[Vinod - KV-Cache-Aware LLM Routing on Kubernetes]]
