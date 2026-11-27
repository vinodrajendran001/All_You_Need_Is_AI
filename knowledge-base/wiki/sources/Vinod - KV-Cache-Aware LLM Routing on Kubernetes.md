---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-25-vinod-kv-cache-aware-routing-reproduction
source_title: "KV-cache-aware LLM routing on Kubernetes reproducing the Kinference benchmark inside a single pod"
source_author: Vinod
source_url: ""
tags:
  - source/summary
  - inference
  - kv-cache
  - benchmarks
  - kubernetes
source_ids:
  - src-2026-11-25-vinod-kv-cache-aware-routing-reproduction
status: active
---

# KV-Cache-Aware LLM Routing on Kubernetes

## Summary

An independent, self-reported reproduction of Buoyant's Kinference benchmarks
([[William Morgan - Distributed Inference Benchmarks Kinference vs Kubernetes]], with the launch post
[[William Morgan - Kinference Inference Control Plane for Kubernetes]]), written up as an
interview-portfolio project. The author's only access to a shared 8-GPU node was one
unprivileged-namespace pod, so he ran a nested k3s cluster inside it and deployed Kinference, the
Buoyant Gateway and two pools of three vLLM workers serving the blog's model. He then wrote a paired
harness with bootstrap statistics. Across **144 runs** with **0 request errors**, every headline result
reproduces in direction. Cache-aware routing cut median TTFT by **93.6%** on shared-prefix traffic
(blog: 95%) and **54.0%** on multiturn (blog: about 65%). The magnitudes diverge both ways: multiturn
peak goodput rose **4.1×** (blog 3.5×), while shared-prefix rose only **2.9×** (blog 7.4×). The author
traces the shortfall to a prefix working set of about **101%** of the pool's KV capacity. Two
extensions are the most useful new evidence: a skewed "agentic" prefix mix, and a pool-size sweep with
a one-pod negative control. The baseline is still random routing.

## Key claims

### Setup, and how it differs from the blog

- **8× RTX 6000 Ada 48 GB** (AD102, "the same die as the blog's L40S"), power-capped at **300 W**
  against the L40S's 350 W. GPU 6 belonged to another job, so the 3+3 pools used GPUs 0-5. The whole
  pod had **19.2 CPU cores / 76.8 GiB**.
- Pinned versions: vLLM 0.31.0, kinference 0.1.0-alpha.8, gateway 0.1.0-alpha.7, and the blog's
  `Qwen/Qwen3.8-27B-FP8`. GuideLLM 0.8.1 is pinned, but a custom client replaced it to get paired
  schedules and multiturn requests that carry their history.
- The nested cluster was confined against the host: cgroups, the shared kernel, the pod's Istio
  sidecar, a corporate TLS-intercepting proxy and a shared disk. Changes were recorded in a 14-entry
  teardown ledger and checked by 12 clean-up assertions. The sidecar mattered for validity, because its
  Envoy proxy would otherwise have load-balanced the "random" arm itself. The capture does not say
  whether the cluster's operators approved the setup.
- Method differences: arms ran **back-to-back on disjoint GPUs, alternating order**, because sharing one
  19-core CPU cgroup and one client event loop would let one arm distort the other. Every request used
  a new TCP connection, so kube-proxy re-rolled its random choice. A request counted if it was
  *scheduled* inside the window, and prefix caches were reset before every run.
- SLOs were recalibrated at 1.2× the idle uncached median TTFT: **10.0 s** for 16k prompts (idle
  8.21 s; blog 6.7 → 8 s) and **5.0 s** for 8k (idle 3.98 s; blog 3.3 → 4 s). Prefill is about 22%
  slower, which the author attributes to 300 W versus 350 W.
- Statistics follow the blog: a paired hierarchical bootstrap with 2,000 resamples. Verdicts are given
  only where the 95% CI excludes "no effect".

### How the router decides

For each request the gateway calls Kinference's `Pick` over gRPC with `failureMode: Closed`, so an
outage fails requests instead of silently falling back to random routing. Pick tokenizes the prompt
through vLLM's render endpoint, hashes it into blocks and walks a radix tree built from vLLM's KV
events (sent over ZMQ, with sequence numbers and replay for gaps). It reads load from a `/metrics`
scrape every 1 s and takes the argmin of a predicted wait: a 400 ms base, queued prefill, a linear plus
quadratic prefill term on uncached tokens, and decode contention. A new prefix is credited as
"dispatched" before its KV events arrive, so a burst does not scatter. A replication override
(threshold 10%, `warm_target` 2) can deliberately warm a second worker. The chart's default
coefficients predict about **33 s** for a 16k prefill against **8.2 s** measured, about 4× off, but
routing still worked because only the ranking matters.

### Latency at light load

| Workload | Median TTFT svc → kinf | Δ (95% CI of ratio) | Blog |
| --- | --- | --- | --- |
| shared-prefix | 9.42 → 0.60 s | −93.6% (0.059-0.202) | −95% |
| multiturn | 1.53 → 0.70 s | −54.0% (0.30-0.62) | ≈ −65% |
| control | 9.35 → 8.53 s | −8.7% (0.88-0.95) | ≈ 0 (6.92 vs 6.83 s) |

Median end-to-end latency fell **31.4 → 17.9 s** (−43.2%; blog −45%) and **12.5 → 8.7 s** (−30.4%;
blog ≈ −32%). vLLM's own counters put per-pod prefix-hit rates at 52-60% versus 11-22% (shared-prefix)
and 78-81% versus 47-57% (multiturn).

### The control row has a hardware confound

On control, which has no shared prefixes, the Kinference arm was about 9% faster where the blog found
no difference. p95 fell from 19.7 to 10.0 s (blog 21.5 → 12.3 s). Telemetry showed pool A at
**~2,080 MHz** and pool B at **~1,225 MHz** at the same 299 W, with B hotter (56-70 °C against
~30 °C). A direct per-pod probe after all GPUs were heat-soaked gave **8.25 versus 8.35 s**, a ratio of
**1.012**. The author concludes that the gap mixes a transient thermal advantage with real load
awareness and cannot separate the two. Kinference spread control requests 35/36/39 across pods, while
kube-proxy produced 48/30/32, which also explains the Service arm's 71 versus 41 ms ITL.

### Capacity under closed-loop load

| Workload | c4 | c8 | c16 | c24 | c32 | Peak svc → kinf | Max conc. meeting SLO (svc / kinf) | Blog |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| multiturn | 1.6× | 3.6× | 8.6× | 3.4× | 0.1× | 15.5 → 64.4 (4.1×) | none / 16 | 3.5×; none / 8 |
| shared-prefix | 2.0× | 2.9× | 2.7× | 1.2× (n.s.) | 0× | 7.1 → 20.9 (2.9×) | none / 8 | 7.4×; none / 32 |

- **Crossover at c32.** With both arms saturated, Kinference's SLO attainment fell to 0 while random
  routing kept 6-21%, at the same throughput (30 versus 29 req/min on multiturn). The author's
  explanation is that even balancing makes every request queue about equally and miss together, while
  random unevenness leaves some requests fast. Goodput "rewards variance near the SLO cliff". The
  lesson: **operate below the knee**, with admission control or autoscaling.
- **The shared-prefix shortfall.** vLLM reports **126,976 tokens** of KV cache per pod at
  `gpu-memory-utilization=0.90`, about **381k** per pool. The 24 prefixes × 16k tokens make **384k**,
  about 101% of the pool before any running request. Kinference's hit counts fall toward random by c24,
  and preemptions appear from c16. The proposed mechanism is inferred, not traced per request: under
  load, spilling hot-prefix requests to less busy pods duplicates prefixes and causes LRU thrashing. The
  blog reports neither its memory fraction, nor its KV dtype, nor its KV cache size, so the gap with
  its 48 GB GPUs is unexplained. Suggested remedies: an FP8 KV cache ("roughly doubles capacity"), more
  replicas, or a less eager spill policy.

### Extensions

- **Agentic mix** (64 Zipf-distributed 8k prefixes, SLO 5.5 s): median TTFT fell from 4.36 to
  **0.54 s** (−87.6%, CI 0.12-0.28), and goodput at c8/c16/c32 rose **1.6× / 2.2× / 3.3×**. The gain
  grows with load. The author's reading is that the hot head of the distribution fits in cache, so the
  shared-prefix ceiling is a capacity limit, not a routing limit.
- **Pool-size sweep** (goodput ratio at c8, multiturn / shared-prefix): **1.10× / 0.97×** at 1+1 (both
  n.s.), **3.25× / 1.97×** at 2+2 and **3.61× / 2.93×** at 3+3. Only Kinference's hit rates rise with N.
  One pod per pool leaves no routing choice, so it serves as a negative control, and the rise with N is
  a dose-response. The author calls this the cleanest evidence in the project.

### Routing overhead

The router added about **9 ms** at idle and **35 ms** at concurrency 4 in a 0.5B smoke test, and
**+29 ms** (0.644 versus 0.615 s, +5% of a warm TTFT) with the real model at 1+1. Kinference's own pick
duration averaged **103 ms** over 9,360 picks (87% ≤ 100 ms). Most of that is render tokenization,
"part of it overlaps with work vLLM would do anyway". Kinference is alpha and ran as one replica.

## Why it matters

This is the vault's first independent replication of a vendor serving benchmark. It confirms the
mechanism recorded in [[KV Cache]] and [[ML Systems at Scale]]: cache location is routing state, and
generic replicas need workload-aware policy. It also adds the limit those pages lacked. Routing can
exploit only the locality the cache can hold, so capacity planning compares the distinct prefix working
set with the pool's KV tokens. For [[Serving Benchmarks and Goodput]], it shows a reproduction that
agrees on direction but misses one magnitude by a wide margin, that "identical hardware" has to be
measured, and that a goodput SLO can make the better router look worse past saturation.
[[Inference Serving Engines]] gains the internals of one endpoint picker. [[Kubernetes]] gains a second
measurement of the kube-proxy baseline, and a service-mesh sidecar that could have silently replaced
it.

## Tensions / open questions

- **Self-reported and unpublished.** There is no frontmatter, URL or byline beyond "Vinod", and the
  results files it cites are not in the vault. It is framed as interview preparation, and the pitch
  picks favourable numbers: "4.1× peak goodput (the blog reported 3.5×)" is multiturn only, while
  shared-prefix fell short (2.9× against 7.4×). The pitch's "1.1× to 3.3× to 3.6×" is also the
  multiturn column of the sweep.
- **The baseline is still random.** A Q&A argues against ClientIP session affinity ("pins *clients*,
  not *prefixes*") and against consistent hashing, but tests neither. The vault's open question about a
  session-affine baseline is unchanged.
- **The two accounts of arm ordering conflict.** This capture says "The blog fired both arms
  simultaneously". The blog's own text, in the vault, says "The arms ran one after the other, and order
  alternated", but also that latency requests "were sent at identical times". Either the capture
  misreads the blog or the blog is ambiguous.
- **Overhead tension.** Pick time (mean 103 ms; histogram median 50-100 ms) exceeds the +29 ms measured
  TTFT increase. The overlap explanation is asserted, not measured.
- **One node, nested cluster, different GPUs.** The lower power cap, the nested network hop, the custom
  client and sequential arms all differ from the blog. The shared-prefix mechanism is inferred, because
  the harness did not log which pod served each request.
- No cost or energy measurement. The evidence for the mechanism is vLLM's `cached_tokens` counters,
  not output checks.

## Affected pages

- [[Serving Benchmarks and Goodput]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[ML Systems at Scale]]
- [[Kubernetes]]

## Raw capture

- [[knowledge-base/raw/sources/KV-cache-aware LLM routing on Kubernetes reproducing the Kinference benchmark inside a single pod]]

## Citations

- Canonical URL: none. The capture has no frontmatter, no source URL and no title heading. The title
  above is the capture's filename.
- In-text byline: "Author: Vinod · Date: Nov 2026 · Project: `kinference-bench/`". The source ID's
  date (2026-11-25) is the capture's first Git-tracked date, not a publication date.
- It reproduces two Buoyant posts linked in the capture, "Distributed Inference Benchmarks:
  [K]inference vs. Plain Kubernetes" and "Introducing [K]inference". Blog figures in the tables above
  are as the capture states them.

## Related pages

- [[William Morgan - Distributed Inference Benchmarks Kinference vs Kubernetes]]
- [[William Morgan - Kinference Inference Control Plane for Kubernetes]]
- [[Rahul Ranganathan - Inference Gateway on GKE]]
- [[Serving Benchmarks and Goodput]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[ML Systems at Scale]]
- [[Kubernetes]]
- [[Model Routing]]
- [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]
- [[ML Research Interview Preparation]]
- [[vLLM-GR Team - Announcing vLLM-GR]]
