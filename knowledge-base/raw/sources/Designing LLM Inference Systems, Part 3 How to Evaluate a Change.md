---
title: "Designing LLM Inference Systems, Part 3: How to Evaluate a Change"
source: "https://medium.com/@wszjzhang/designing-llm-inference-systems-part-3-how-to-evaluate-a-change-d528f7d5b9c9"
author:
  - "[[intelligentLearn]]"
published: 2026-11-19
created: 2026-11-25
description: "More"
tags:
  - "clippings"
---
Where the real trade-offs live, worked through with numbers you can check.

*Part 3 of 4 of the trade-offs article, from “Designing LLM inference systems”, the second half of a series on LLM inference serving.* [*Part 1*](https://medium.com/@wszjzhang/from-symptoms-to-fixes-the-trade-offs-inside-an-llm-inference-system-part-1-start-with-the-9aa825ca7969) *and Part 2 covered the machine and the six layers; this part asks how to judge a reported improvement before adopting it. Part 4, with the running case worked end to end and the appendices, follows on November 24.*

A mechanism is not yet a decision. Before accepting a reported improvement, ask three questions in order: whether the comparison stayed comparable, whether the metric represents the service outcome, and which workload variables remain unknown. The answers turn the three ledgers from an explanatory device into an evaluation method.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*7eCj62N65d2QDT6O5QwgUg.png)

*Ask these three in order. A pass on an earlier question does not answer a later one.*

## 12\. Did the comparison basis change?

First hold the basis still. Compare at the **same GPU count and hardware**, or account explicitly for added CPUs, interconnects and model copies. Keep **model precision** fixed unless quality and hardware throughput at the new precision are part of the result. Replay the same **request distribution**, not just the same mean input length. And keep the same **target and SLO**: optimizing offline throughput is not evidence that P95 TTFT or token gaps improved.

FastDecode is the useful warning. Its state-offload result uses extra whole CPU machines, and its comparison baseline is not the same hardware; at 128-token sequences, the 13B model’s strong-scaling efficiency from one to eight sockets is only 37.6%, with eight sockets slower than four. That does not invalidate the mechanism. It means the claim being tested is not “same service, same resources, faster.” Section 7 applies the same discipline to model copies under P/D disaggregation.

A comparison is usable when its denominator is explicit: GPUs and auxiliary hardware, precision and model quality, the joint input/output-length and prefix-reuse distribution, and the SLO under which requests count as successful.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Mn9k1_AgVxIM0b-jPWWQVw.png)

*Same facts as section 12. 37.6% is FastDecode’s reported strong-scaling efficiency, not a result for this article’s running case.*

## 13\. Did a local metric improve, or did the service improve?

Next separate a mechanism metric from the target request. A faster kernel, a higher cache hit rate or higher mean throughput can all coexist with a worse service:

- PagedAttention’s own attention kernel is 20–26% slower than FasterTransformer’s, yet the memory it saves can admit more requests. Kernel speed alone therefore misses the capacity effect.
- SGLang reaches 96% of the optimal hit rate for ordering inside one engine, and reports a 74.1% production hit rate with one worker per model. Neither number by itself establishes lower multi-replica TTFT; the routing step is an extrapolation, and extra queueing can consume the saved execution.
- DualMap measures the affinity/balance conflict, but its oscillation example belongs to a rejected baseline, and its Conversation hit rate reaches only 62.5% of the upper bound. Hit rate is evidence about reuse, not the end-to-end result.
- The disaggregation design-space result in `pdisagg2026` is a directional simulator result: hardware measurements stop at 8B, no simulator error is reported, and the traffic model has no dynamic arrivals. A mean-throughput win under that model is not yet evidence for a bursty target service.

Read the request timeline after the local metric. For the target request distribution, did P95 TTFT fall? Did the P95 token gap stay within budget? Did **goodput** — throughput counting only requests that met their objective, with rejected and timed-out requests counted as misses — rise, and did SLO attainment for that workload class rise with it? Did timeout, rejection, retry or quality outcomes move? The service improved only if the answer is visible at that boundary, not merely inside one kernel, cache or scheduler.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nvV3xFaDFofiNd7GyquwkA.png)

*The service boundary in section 13. The percentages in the bullets stay in the bullets.*

## 14\. What remains unmeasured?

Finally list the variables that could reverse the result. For this case, at least these remain:

- **cold versus hot prefixes**: what fraction arrives without reusable state, and how much of a hot prefix is actually reusable;
- **arrival rate and burstiness**: both the sustained rate and the burst duration that queues and autoscaling must absorb;
- **long/short request mix**: the joint input/output-length distribution, not one representative request;
- **transfer overlap**: how much KV or weight movement is hidden behind useful execution rather than added to the critical path;
- **queue prediction error**: how far the router’s estimate of waiting time differs from what the request experiences;
- **startup time**: the distribution from scale-out decision to a ready replica, not only one reported mean.

These measurements define the experiment that the running case needs. The case can now use the six-layer map to choose candidate interventions, while treating any branch whose comparison basis or service outcome is still missing as a measurement task rather than a conclusion.