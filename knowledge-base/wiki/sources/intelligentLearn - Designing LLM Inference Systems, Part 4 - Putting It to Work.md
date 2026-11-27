---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-24-intelligentlearn-inference-systems-part-4
source_title: "Designing LLM Inference Systems, Part 4: Putting It to Work"
source_author: intelligentLearn
source_url: https://medium.com/@wszjzhang/designing-llm-inference-systems-part-4-putting-it-to-work-cd2b9f32805d
tags:
  - source/summary
  - inference
  - serving
  - evaluation
  - literature-review
source_ids:
  - src-2026-11-24-intelligentlearn-inference-systems-part-4
status: active
---

# Designing LLM Inference Systems, Part 4: Putting It to Work

## Summary

The final part of [[intelligentLearn]]'s series has three sections. It restates the six-layer
framework in stack order (L0 to L5) as a reference table. It works Part 1's long-document case to a
conclusion, and that conclusion is deliberately mostly a measurement plan. It closes with appendices
that audit the article's own evidence. Each layer is reduced to what it decides, which constraint it
relieves, what it costs, and the signal that says to look there. The case yields one computed
result (a memory ceiling of about 14 long documents per replica) and one conditional choice (when a
cache hit justifies a hot replica's queue). Every other branch becomes something to measure. The
appendices disclose search bias, layer-label overlap, out-of-corpus anchor papers, mechanism
families left out, and a 172-paper table with a per-paper reading-depth label.

## Key claims

### The six-layer map as a reference

- **L0 capacity** decides how many GPUs exist and at what price; its cost is availability and state
  rebuilding. **L1 substrate** decides how GPUs are carved up and replicas start; prewarming holds
  GPUs idle, and sharing brings interference. **L2 engine internals** divides time and memory on one
  GPU and relieves state footprint and data movement. Its signal is that memory is the first wall or
  long prefills block decode.
- **L3 replica composition** relieves phase interference and configuration coupling, at the cost of
  KV transfer, ratio imbalance, and model copies. Its signal is that chunking no longer holds the
  interference down and traffic is prefill-heavy. **L4 routing and admission** relieves waiting and
  repeated computation, at the cost of hot-instance queues.
- **L5 contract and failure semantics** "relieves no resource constraint — it defines who gets
  sacrificed", and that takes a product decision.

### The case, worked through

- **Execution feasibility first.** TP=4 would need about **76%** of BF16 dense peak to fit the cold
  32K prefill into 2 s; at the uncited 40% teaching assumption it takes about **3.8 s**. Chunked
  prefill can protect the token gap of requests already decoding. P/D disaggregation can decouple
  interference and configuration. "Neither reduces this cold request's own prefill work."
- **Computed result.** About **159 GB** of KV room per replica divided by about **10.9 GB** per long
  document gives **≈14** requests. That is "a capacity ceiling, not achievable concurrency".
- **Conditional choice (illustrative, not measured).** If a hit saves **1.8 s**, the hot replica adds
  **0.6 s** of queueing, and transfer adds **0.2 s**, the net benefit is **1.0 s**. Once queueing plus
  transfer exceeds the execution saved, the choice flips to the less-loaded replica.
- **Measurement plan.** Each unknown is tied to a decision. Prefix-reuse distributions decide
  affinity. Arrival, burst, and queue-prediction error choose among balancing, admission, and
  affinity. KV transfer time and overlap decide whether disaggregation fits the TTFT budget. The
  scale-out-to-ready distribution decides whether scaling can catch a burst. HydraServe's **>40 s**
  cold start is scoped to that paper's environment. Adopt a policy only if P95 TTFT, P95 token gap,
  SLO attainment, goodput, and timeout, rejection, and quality outcomes improve per workload class.
- "The four parts are one argument": ledgers, layers, evaluation, then application.

### The appendices audit the reading

- **Bias (A).** The corpus comes from one keyword search with per-layer budgets and caps, and layers
  were assigned mostly from titles and abstracts. L5 got the smallest budget (3 queries, capped at
  70), and one of those queries was about context compression, "not a contract-layer search term at
  all". L0 had a cap of 150 but only 5 papers were admitted, a vocabulary mismatch. The corpus is
  overwhelmingly recent, so it is "not the place to learn how the field evolved".
- **Overlap (B).** **108 of the 172** papers carry a secondary-layer label. The layers are "a ruler
  for organizing an explanation, not a natural seam in the field", and the counts are not additive.
- **Anchors (C).** Orca (continuous batching), FlashAttention, and Splitwise sit outside the 172.
  Continuous batching is the one mechanism-level claim whose only source is outside the deeply read
  set.
- **Not developed (D).** Quantization, speculative decoding and multi-token prediction, MoE expert
  placement, prefix-cache reuse policies, energy and frequency scaling, edge inference, and
  sparse/linear attention are left out. The author calls this "a statement of this article's
  boundary", not future work. Sparse attention, for example, would change the memory budget.
- **The table (E).** It labels each of the 172 papers by primary and secondary layer and evidence
  depth: **15** deeply read (quotes checked verbatim), **146** full text (used for placement only),
  and **11** abstract only. The body's mechanism claims rest on the deeply read tier alone. **8**
  excluded papers are deliberately not listed. Read row by row, most primary labels fall in engine
  internals (L2) and replica composition (L3). The three L5 rows are SLO-Guard, the incident study,
  and a full-text-only paper on the "human tax" on serving throughput.

## Why it matters

The part makes the series reusable. The reference table and the measurement plan can be applied to
any serving change, and the appendices model how a literature-backed engineering essay can label its
own evidence depth. This pairs naturally with the evidence standard in
[[Serving Benchmarks and Goodput]]. It anchors the decision rules in [[Prefill-Decode Disaggregation]]
and [[Semantic Caching]]. It puts the L0/L1 availability layers into [[GPU Fleet Reliability]]. It
gives [[Software Performance Engineering]] a worked example of ending an analysis at "needs
measurement". It also records, for [[Model Quantization and Efficiency]], that precision is
deliberately outside this serving analysis. [[LLM Inference]] gains the end-to-end case.

## Tensions / open questions

- Appendix cross-references conflict. The anchor papers are in Appendix C, but Appendix E and Part 2
  say "see Appendix D" for Orca. Appendix C says "Appendix C records the exception" about itself.
- Only 15 of 172 papers were read end to end. The table's breadth should not be mistaken for depth
  of support, as the author stresses.
- The cache-affinity seconds are illustrative arithmetic, not measurements.
- The corpus counts reflect the author's search budget as much as the field. Thin L0 and L5 coverage
  is an artefact by the author's own account.
- The 8 excluded papers are unlisted by design, so the exclusion cannot be audited.

## Affected pages

- [[LLM Inference]]
- [[Prefill-Decode Disaggregation]]
- [[Model Quantization and Efficiency]]
- [[Semantic Caching]]
- [[GPU Fleet Reliability]]
- [[Software Performance Engineering]]
- [[intelligentLearn]]
- [[Serving Benchmarks and Goodput]]

## Raw capture

- [[knowledge-base/raw/sources/Designing LLM Inference Systems, Part 4 Putting It to Work]]

## Citations

- Canonical URL: https://medium.com/@wszjzhang/designing-llm-inference-systems-part-4-putting-it-to-work-cd2b9f32805d
- Byline: intelligentLearn (Medium handle @wszjzhang; no personal name in the capture).
- Published: 2026-11-24. Captured: 2026-11-25. Publisher: Medium.
- Appendix E's 172-paper table is summarized, not reproduced.

## Related pages

- [[intelligentLearn - From Symptoms to Fixes - Part 1 - Start with the Machine]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 3 - How to Evaluate a Change]]
- [[intelligentLearn]]
- [[Serving Benchmarks and Goodput]]
- [[Prefill-Decode Disaggregation]]
- [[Semantic Caching]]
- [[GPU Fleet Reliability]]
- [[Software Performance Engineering]]
- [[Model Quantization and Efficiency]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[Speculative Decoding]]
