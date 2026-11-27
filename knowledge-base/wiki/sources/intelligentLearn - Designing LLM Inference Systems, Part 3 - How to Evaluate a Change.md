---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-19-intelligentlearn-inference-systems-part-3
source_title: "Designing LLM Inference Systems, Part 3: How to Evaluate a Change"
source_author: intelligentLearn
source_url: https://medium.com/@wszjzhang/designing-llm-inference-systems-part-3-how-to-evaluate-a-change-d528f7d5b9c9
tags:
  - source/summary
  - inference
  - evaluation
  - goodput
source_ids:
  - src-2026-11-19-intelligentlearn-inference-systems-part-3
status: active
---

# Designing LLM Inference Systems, Part 3: How to Evaluate a Change

## Summary

The short third part of [[intelligentLearn]]'s series turns the three ledgers from Part 1 into an
evaluation method. "A mechanism is not yet a decision". Before adopting a reported serving
improvement, ask three questions in order. Did the comparison basis stay fixed? Did a local metric
improve, or did the service? Which workload variables remain unmeasured? A pass on an earlier
question does not answer a later one. Each question is illustrated with the same papers Part 2 read
in depth, now used as warnings about what their headline numbers do and do not establish.

## Key claims

### 1. Hold the comparison basis still

- Compare on the **same GPU count and hardware**, or account explicitly for added CPUs,
  interconnects, and model copies. Keep **model precision**, the **request distribution** (not only
  the mean input length), and the **target SLO** fixed. Offline throughput gains are not evidence
  that P95 TTFT or token gaps improved.
- FastDecode is the warning case. Its offload result uses extra whole CPU machines and a baseline on
  different hardware, and its 13B strong-scaling efficiency from one to eight sockets at 128-token
  sequences is **37.6%**. The mechanism survives, but the claim tested is not "same service, same
  resources, faster".
- A comparison is usable when its **denominator** is explicit. That means hardware, precision and
  quality, the joint input/output-length and prefix-reuse distribution, and the SLO under which a
  request counts as successful.

### 2. Separate the mechanism metric from the service boundary

- PagedAttention's kernel is **20–26%** slower than FasterTransformer's, yet the memory it saves
  can admit more requests. Kernel speed alone misses the capacity effect.
- SGLang's **96%** of optimal hit rate and **74.1%** production hit rate do not by themselves
  establish lower multi-replica TTFT. DualMap's hit rate reaches only **62.5%** of the upper bound,
  and hit rate is evidence about reuse, not outcome. pdisagg2026 is a directional simulator result
  with no dynamic arrivals.
- The service improved only if the change is visible at the request boundary: P95 TTFT, P95 token
  gap, SLO attainment, and **goodput** (throughput counting only requests that met their objective,
  "with rejected and timed-out requests counted as misses"), plus timeout, rejection, retry, and
  quality outcomes.

### 3. List what could reverse the result

- Cold versus hot prefixes and how much of a hot prefix is reusable; the arrival rate and burst
  duration; the joint long/short length mix; how much KV or weight transfer overlaps useful work;
  the router's queue-prediction error; and the full distribution of time from a scale-out decision
  to a ready replica, not only its mean.

## Why it matters

The part gives [[Software Performance Engineering]] a compact serving-specific checklist for
judging a claimed speedup. It gives [[Prefill-Decode Disaggregation]] and [[Semantic Caching]] the
rule that local wins (hit rate, kernel time, mean throughput) are not service results. It also
supplies [[LLM Inference]] and [[Inference Efficiency Frontier]] with a goodput definition that
counts rejections and timeouts as misses.

## Tensions / open questions

- The part presents no new data. It re-reads Part 2's papers, and the 37.6% figure is FastDecode's
  own result, not one for the running case.
- It says Part 4 "follows on November 24" while Part 1 had announced Part 3 for November 17. The
  capture is dated November 19.
- The unmeasured-variable list is specific to the running case. The author does not say how to rank
  the variables when measurement budget is limited.

## Affected pages

- [[LLM Inference]]
- [[Prefill-Decode Disaggregation]]
- [[Inference Efficiency Frontier]]
- [[Semantic Caching]]
- [[Software Performance Engineering]]
- [[intelligentLearn]]
- [[Serving Benchmarks and Goodput]]

## Raw capture

- [[knowledge-base/raw/sources/Designing LLM Inference Systems, Part 3 How to Evaluate a Change]]

## Citations

- Canonical URL: https://medium.com/@wszjzhang/designing-llm-inference-systems-part-3-how-to-evaluate-a-change-d528f7d5b9c9
- Byline: intelligentLearn (Medium handle @wszjzhang; no personal name in the capture).
- Published: 2026-11-19. Captured: 2026-11-25. Publisher: Medium.

## Related pages

- [[intelligentLearn - From Symptoms to Fixes - Part 1 - Start with the Machine]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 4 - Putting It to Work]]
- [[intelligentLearn]]
- [[Serving Benchmarks and Goodput]]
- [[Software Performance Engineering]]
- [[Prefill-Decode Disaggregation]]
- [[Semantic Caching]]
- [[LLM Inference]]
- [[Inference Efficiency Frontier]]
- [[Wafer - AI Performance Engineering Resources]]
