---
type: source-summary
created: 2026-09-03
updated: 2026-09-03
source_id: src-2026-09-02-baseten-efficient-frontier-inference
source_title: "The efficient frontier of LLM inference"
source_author: Philip Kiely
source_url: https://www.baseten.co/blog/the-efficient-frontier-of-llm-inference/
tags:
  - source/summary
  - topic/inference
  - topic/serving
source_ids:
  - src-2026-09-02-baseten-efficient-frontier-inference
status: active
---

# Philip Kiely - The Efficient Frontier of LLM Inference

## Summary

A short taxonomy piece from [[Baseten]] that proposes a single question for sorting every inference
optimization: **does this technique move a deployment along the efficient frontier, or does it push the
frontier out?**

The frontier is borrowed from economics. In inference it is most often latency against throughput (which
determines cost), but the post notes two further exchange axes: **quality for throughput** (quantization,
distillation, pruning) and **intelligence for speed** (reasoning level). The worked setting is an agentic
coding deployment of GLM-5.3 or Kimi K3 with KV-cache reuse and KV-aware routing already enabled.

## Key claims

- **Two classes of technique, both valuable.** Tradeoff techniques let you *target* a point; frontier-moving
  techniques create efficiency that can then be *allocated* to latency, throughput, or a mix.
- **The frontier is jagged, not smooth.** Small configuration changes produce large outcome changes, and
  **the cutoff points are unintuitive and must be found empirically through sweeps**. This is the post's most
  practically useful claim: there is no analytic shortcut to the operating point.
- **Batch sizing is the canonical tradeoff.** Continuous batching removes queueing delay, but the *configured*
  batch size still sets per-user latency against tokens-per-GPU, and therefore cost per token.
- **Parallelism strategy is a tradeoff, and the choice is directional.** **Tensor Parallelism** lowers latency
  — its all-to-all communication is expensive but fast over NVLink. **Expert Parallelism** cuts both ways: low
  EP degree tends toward latency, wide EP (up to a full rack) toward throughput. **Attention Data
  Parallelism** replicates attention layers to raise system throughput at the cost of per-request speed.
- **Quantization sits in both categories, and this is the subtle point.** It pushes out the *serving* frontier
  — better latency *and* throughput together — while introducing a **new quality-versus-efficiency frontier**.
  That second frontier is described as *particularly* jagged: large serving gains for little or no quality
  loss are available, especially with microscaling formats **MXFP4** and **NVFP4**.
- **Frontier-moving techniques compound multiplicatively.** Doubling from hardware and doubling from software
  gives **4×** to allocate.
- **Kernel and runtime optimization** reduces the resources per token, and the gain propagates through the
  whole stack.
- **Speculative decoding has changed category.** It used to be a tradeoff technique — expensive speculation,
  short sequences, low acceptance rates, viable only at small batch sizes. **EAGLE-3, DSpark and DFlash** now
  deliver efficiency from **skipped forward passes** on top of raw latency reduction, though they still
  compete with the main loop for resources and so still cap maximum batch size. Code generation benefits most,
  because output sequences are relatively predictable.
- **Disaggregation** lets prefill and decode workers be tuned independently and the ratio between them matched
  to real traffic; in practice it is **most useful for raising throughput while holding latency flat or
  slightly better**.

## Why it matters

The vault documents most of these techniques individually and in more depth than this post does — see
[[Speculative Decoding]], [[Prefill-Decode Disaggregation]], [[GPU Kernel Optimization]],
[[Model Quantization and Efficiency]], [[Distributed Training Parallelism]]. What was missing was a
**classifier**, and that is what this source contributes: a way to say what a given optimization actually buys
you, and therefore whether two techniques are alternatives or complements.

The reclassification of speculative decoding is the most substantive claim. The vault's existing page records
speculation as spending headroom that could be spent elsewhere — a tradeoff framing. This source argues the
category boundary has moved with EAGLE-3-class methods, because skipped forward passes are a real reduction in
work rather than a reallocation of it. Both readings are now on record; see [[Inference Efficiency Frontier]].

"The frontier is jagged" also has a governance consequence: if operating points must be discovered by sweeps,
then published single-configuration benchmark numbers describe a point someone chose, not a capability.

## Tensions / open questions

- **The author is a vendor.** [[Baseten]] sells inference, the post links its own EAGLE-3 and DFlash work
  throughout, and it closes by promoting the author's book. The taxonomy is sound independent of that, but the
  claims about which techniques are winning are commercially interested.
- **No measurements.** Every claim is directional — "improves latency", "supports higher throughput" — with no
  numbers, hardware, or model attached. The compounding 4× example is illustrative arithmetic, not a result.
- Does quantization genuinely belong in both categories, or is calling it frontier-moving an artifact of
  choosing latency-throughput as *the* frontier while treating quality as an externality?
- If cutoffs must be found by sweeps, what is the cost of the sweep, and who can afford to run one?

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Inference Efficiency Frontier]]
- [[LLM Inference]]
- [[Speculative Decoding]]
- [[Prefill-Decode Disaggregation]]
- [[Baseten]]
- [[Philip Kiely]]

## Related pages

- [[Model Quantization and Efficiency]]
- [[GPU Kernel Optimization]]
- [[Distributed Training Parallelism]]
- [[Mixture of Experts]]
- [[KV Cache]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Serving Engines]]
- [[Reasoning Effort Control]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]

## Citations

- Raw capture: [[2026-09-02 Philip Kiely - The efficient frontier of LLM inference]]
- Source: <https://www.baseten.co/blog/the-efficient-frontier-of-llm-inference/>
