---
type: source-summary
created: 2026-11-20
updated: 2026-11-27
source_id: src-2026-10-31-william-morgan-kinference-benchmarks
source_title: "Distributed Inference Benchmarks: [K]inference vs. Kubernetes"
source_author: "William Morgan"
source_url: "https://www.buoyant.io/blog/distributed-inference-benchmarks-kinference-vs-plain-kubernetes"
tags:
  - source/summary
  - inference
  - serving
  - benchmarks
  - kubernetes
  - kv-cache
  - vendor
source_ids:
  - src-2026-10-31-william-morgan-kinference-benchmarks
status: active
---

# Distributed Inference Benchmarks: Kinference vs. Kubernetes

## Summary

Buoyant's first-party benchmark of its own Kinference routing layer (see
[[William Morgan - Kinference Inference Control Plane for Kubernetes]]) against a plain [[Kubernetes]]
Service in front of identical vLLM pods. Kinference predicts time-to-first-token (TTFT) for each
request on each candidate pod, using KV-cache overlap and queue size, and sends the request to the
lowest prediction. The Service arm spreads requests randomly.

The design is unusually disciplined for a vendor post: hypotheses and primary metrics fixed in advance,
a control workload with no shared prefixes, three trials per condition, paired bootstrap confidence
intervals, and software versions stated. On workloads with shared prefixes, Kinference cut **median
TTFT by 95%** (shared-prefix) and **about 65%** (multiturn) at light load. Under heavy load it served
about **7.4×** and **3.5×** the **goodput** (requests per minute that met a latency target). The main
limit is the baseline. Random per-connection routing is Kubernetes' default, not a competing
inference-aware router, so the results measure the value of cache awareness over none at all, on
three relatively old L40S GPUs per arm, for one vendor's product.

## Key claims

### Setup

- AWS cluster with two identical pools of **vLLM 0.31.0** serving **Qwen-3.8-27B-FP8**. Each pool had
  **3 vLLM pods, each on its own L40S GPU**. Load came from **GuideLLM 0.8.1** on a separate node.
- Arm 1 used Kinference's endpoint for pool one. Arm 2 used the Kubernetes Service (ClusterIP) for pool
  two. kube-proxy in iptables mode picks a random pod for each new connection, and GuideLLM "opens a
  new connection for almost every request", so the Service arm was effectively random per request.
- Both arms got identical prompts, and in the latency test identical send times. "Prompts and prefixes
  were new in every condition and trial."
- The authors call the setup slow, a dense modern model "on relatively old GPUs". Results are in
  requests per minute, and the SLOs are "not appropriate for chat, but plausible for offline agentic
  workloads". They say "the comparative numbers are the important ones".

### Workloads

| Workload | Shape | Latency-test rate |
| --- | --- | --- |
| control | 16,256-token unique prompt, 256 output tokens | 6 req/min |
| shared-prefix | one of 24 shared 16,000-token prefixes + 256 unique tokens, 256 output | 12 req/min |
| multiturn | 8-turn conversations, 8,000-token first prompt, +400 tokens per turn, 200 output | 18 req/min |

The latency test used open-loop Poisson arrivals with a 60 s warmup, 240 s measurement and 45 s
cooldown: 3 workloads × 2 arms × 3 trials = **18 runs**. Arms ran one after the other, with order
alternated.

### Light-load latency (primary metric: median TTFT)

| Workload | Median TTFT svc / kinf | Ratio [95% CI] | p95 TTFT svc / kinf |
| --- | --- | --- | --- |
| control | 6.92 / 6.83 s | 0.987 [0.644, 1.013] | 21.46 / 12.33 s |
| shared-prefix | 6.88 / 0.31 s | 0.045 [0.042, 0.596] | 18.32 / 9.24 s |
| multiturn | 1.70 / 0.59 s | 0.350 [0.166, 0.537] | 12.82 / 7.70 s |

- On control, median TTFT shows "no difference", so the router adds no measurable latency. The p95
  drop from 21.5 s to 12.3 s is attributed, with "likely", to queue-size awareness.
- Median end-to-end latency fell from **20.5 to 11.3 s** (shared-prefix, about 45%) and **13.4 to
  9.1 s** (multiturn, about 32%). Median ITL fell from 44 to 42 ms and from 47 to 43 ms. The authors
  attribute most of the end-to-end gain to TTFT and the rest to replicas recomputing fewer prefixes.
- Output throughput ratios were **0.98-1.05** per trial; no request failed.

### Capacity under load (primary metric: goodput difference)

Closed-loop traffic at concurrency 4, 8, 16, 24 and 32, three trials each, 60 / 180 / 60 s windows,
**60 runs**. The SLOs were set empirically from uncached idle TTFT plus padding: **90% of TTFT ≤ 8 s**
for shared-prefix (idle uncached TTFT **6.7 s**), and **≤ 4 s** for multiturn (**3.3 s**).

- Kinference had higher goodput "at every concurrency on both workloads, and in every one of the 30
  paired trials".
- Peak goodput was **14.0 vs 103.0** req/min (shared-prefix; service peak at concurrency 16,
  Kinference at 32) and **23.8 vs 82.7** (multiturn; at 8 and 24).
- The Service arm never met either SLO; its best attainment was 70% and 76%, both at concurrency 4.
  Kinference met the shared-prefix SLO up to concurrency 32 and the multiturn SLO up to 8, reaching
  87% and 89% at 16 and 24.

## Why it matters

This is the vault's first measured, interval-qualified comparison of cache-aware against cache-blind
request routing. The GKE gateway account in [[Rahul Ranganathan - Inference Gateway on GKE]] described
the same mechanism with no numbers. It turns a claim recorded in [[KV Cache]] ("cache location is
routing state") into figures, and it supports the rule in [[ML Systems at Scale]] that generic scaling
primitives need workload-aware policy. Against [[Serving Benchmarks and Goodput]]'s evidence standard
it scores well on disclosure and pre-registration and poorly on baseline choice.

## Tensions / open questions

- **Baseline fairness.** The only comparison is random routing. There is no session-sticky Service, no
  Gateway API Inference Extension, and no other prefix-aware router. "Kinference versus Kubernetes"
  really means "cache-aware versus random". The random behaviour also depends on GuideLLM opening a new
  connection per request; the post does not test clients that reuse connections.
- **Workload favours the mechanism.** 24 hot 16,000-token prefixes on 3 replicas, fresh prefixes per
  trial, and 240 s or 180 s windows. *Reviewer inference:* short runs give random routing few chances
  to warm every replica's cache, and production prefix popularity, cache eviction and replica counts
  could widen or narrow the gap. The post does not test this.
- **Headline compression.** "7.4×" compares peaks reached at different concurrencies (16 versus 32). The
  conclusion's "almost 7.5×" matches neither exactly; the same-concurrency ratio at 24 is "about 7.5×".
  Ratios at concurrency 4 were only 2.1× and 1.5×. The launch post's "up to 95%" is the best of three workloads; control showed no median
  change.
- **The SLO choice backfired as stated.** SLOs were picked so both arms could plausibly attain them,
  yet the Service arm attained neither at any concurrency. That is informative about random routing,
  but it means the goodput ratios partly reflect where the threshold sits.
- **Statistical reporting quirks.** The shared-prefix median ratio is 0.045 with a CI reaching 0.596.
  The control end-to-end ratio of 0.73 is called non-significant because its CI [0.70, 1.01] reaches
  1. Multiturn ITL 47→43 ms is described as "about 10%" (ratio 0.90), slightly more than the rounded
  values imply.
- **No cost, energy or correctness measures**, though routing should not change outputs. The vendor ran
  both arms.
- **An independent reproduction agrees on direction, not magnitude (added 2026-11-27).**
  [[Vinod - KV-Cache-Aware LLM Routing on Kubernetes]] reran all three workloads on 8× RTX 6000 Ada
  GPUs (the L40S's die, capped at 300 W) inside a single Kubernetes pod. Median TTFT fell 93.6% on
  shared-prefix (here 95%) and 54.0% on multiturn (here about 65%). Peak goodput rose 4.1× on multiturn
  (here 3.5×) but only 2.9× on shared-prefix (here 7.4×). The reproduction traces that shortfall to 24
  × 16k prefixes filling about 101% of its pool's KV cache; this post reports no KV cache size. Its
  baseline is still random routing. It also states that "The blog fired both arms simultaneously",
  which conflicts with this post's "The arms ran one after the other, and order alternated between
  conditions" (alongside requests "sent at identical times"); the reproduction itself ran its arms
  back-to-back on disjoint GPUs.

## Affected pages

- [[Serving Benchmarks and Goodput]]
- [[KV Cache]]
- [[ML Systems at Scale]]
- [[Kubernetes]]
- [[Inference Serving Engines]]

## Raw capture

- [[knowledge-base/raw/sources/Distributed Inference Benchmarks Kinference vs. Kubernetes]]

## Citations

- Canonical URL:
  <https://www.buoyant.io/blog/distributed-inference-benchmarks-kinference-vs-plain-kubernetes>
- By William Morgan (Buoyant), published 2026-10-31; captured 2026-11-17. It was published before the
  2026-11-03 launch post that links it.
- Confidence intervals, per the source, are 95% CIs from a paired hierarchical bootstrap with 2,000
  resamples.

## Related pages

- [[William Morgan - Kinference Inference Control Plane for Kubernetes]]
- [[Rahul Ranganathan - Inference Gateway on GKE]]
- [[Serving Benchmarks and Goodput]]
- [[KV Cache]]
- [[Kubernetes]]
- [[ML Systems at Scale]]
- [[Inference Serving Engines]]
- [[Model Routing]]
- [[Prefill-Decode Disaggregation]]
- [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]
- [[Sunita Nadampalli and Nicolò Lucchesi - Push-Based KV Transfer in vLLM]]
- [[Vinod - KV-Cache-Aware LLM Routing on Kubernetes]]
