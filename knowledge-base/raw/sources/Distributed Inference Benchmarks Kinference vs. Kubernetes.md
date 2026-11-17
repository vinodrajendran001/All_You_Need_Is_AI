---
title: "Distributed Inference Benchmarks: [K]inference vs. Kubernetes"
source: "https://www.buoyant.io/blog/distributed-inference-benchmarks-kinference-vs-plain-kubernetes"
author:
  - "[[William Morgan]]"
published: 2026-10-31
created: 2026-11-17
description: "Learn how [K]inference cuts TTFT by up to 95% and boosts Kubernetes inference capacity compared to plain vLLM deployments in our latest benchmark."
tags:
  - "clippings"
---
![](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6ae4c041c0e436d18a1ba0e5_Blog%20Banner%201000x225.webp)

[\[K\]inference](https://kinference.ai/) (“kay-inference") is an *inference control plane* for Kubernetes and [vLLM](https://vllm.ai/). \[K\]inference sits in front of a heterogeneous set of GPUs and models, each with different capabilities and levels of performance; takes inference requests from a set of heterogeneous clients, each with different requirements and competing demands; and figures out how to satisfy the clients without overloading the cluster. And it gives you declarative *policies* to determine exactly how that happens.

Part of how \[K\]inference delivers on its promise is by load balancing inference requests based on *predicted TTFT*. In other words, given an inference request (a “prompt”), \[K\]inference predicts the time-to-first-token (TTFT) for that request against each candidate endpoint, then sends it to the worker (e.g. vLLM pod) with the lowest predicted latency. TTFT is a good metric for this because it’s independent of the output size, and because load balancing here can make a tremendous difference–sometimes multiple orders of magnitude.

To make these TTFT predictions, \[K\]inference makes use of a variety of data about the underlying vLLM pods, including contents of their *KV cache*. The KV cache is where inference workers store intermediate results of the *prefill* phase of inference computation. These results may be reused on future requests–but only if they share a prefix. Since many inference requests share a substantial prefix (for example, successive turns in the same conversation), sending a request to a worker with a high KV cache overlap can save a tremendous amount of time.

In this benchmark, we attempt to quantify exactly how much \[K\]inference’s intelligent load balancing helps, by comparing inference requests to a multi-pod vLLM deployment with \[K\]inference against the same requests without \[K\]inference.

## Benchmarks

We look at two basic measures of distributed inference performance:

1. **Unloaded latency.** When the system is under light load and nothing is queuing, is \[K\]inference faster?
2. **Capacity.** When the system is under heavy load, how much more capacity can \[K\]inference provide while maintaining a given SLO?

Measuring unloaded latency demonstrates the value of KV-cache-aware load balancing in isolation, i.e. independent of queueing and other factors. Measuring capacity within an SLO, by contrast, demonstrates real-world performance: how does KV-cache-aware balancing improve a system’s overall ability to serve inference traffic?

## Experimental setup

To test our metrics, we created an AWS cluster where we deployed two identical pools of vLLM 0.31.0, running the [Qwen-3.8-27B-FP8](https://huggingface.co/Qwen/Qwen3.8-27B-FP8) open weight model. Each pool comprised 3 vLLM pods, each running on its own L40S GPU. The two arms of our test were two OpenAI chat-completion HTTP endpoints: one from \[K\]inference, pointing to the first vLLM pool, and one from the Kubernetes Service record pointing to the second vLLM pool.

Our null hypothesis was the two arms would perform the same. Our alternative hypothesis, of course, was that we would see lower latency from \[K\]inference on workloads whose requests share prefixes. We chose the primary metric for this comparison up front: median TTFT on two workloads, *shared-prefix* and *multiturn* (described below). The actual benchmarking was done with [GuideLLM](https://github.com/vllm-project/guidellm) 0.8.1, which we ran on its own node in the cluster.

There are a couple things worth noting about this setup:

1. This is a relatively modern Qwen model, running as a dense checkpoint on relatively old GPUs. It’s slow: we’re reporting reqs/min, below, a far cry from [our usual RPS fare with Linkerd](https://www.buoyant.io/blog/benchmarking-grpc-load-balancing-on-kubernetes-linkerd-vs-istio-vs-cilium). Similarly, our latency SLOs are relatively high–not appropriate for chat, but plausible for offline agentic workloads.
2. Different models and different hardware will deliver very different results, so the raw numbers here are less important as they are specific to these choices. The comparative numbers are the important ones.
3. For the service arm of our test, GuideLLM sent requests straight to the pool’s Kubernetes Service (ClusterIP). kube-proxy, in iptables mode, picks a random pod for each new connection, and GuideLLM opens a new connection for almost every request. Thus, the service arm saw requests distributed randomly across its three replicas.

## Workloads

For the *unloaded latency* benchmark, we used open-loop Poisson arrivals at a low rate which we empirically determined would not saturate the vLLM workers. For the *capacity* benchmark, we used closed-loop traffic at a fixed concurrency, i.e. each client sent traffic as quickly as it could. For each condition and trial within these benchmarks, both arms received identical prompts, and in the latency benchmarks requests were sent at identical times. Prompts and prefixes were new in every condition and trial.

Finally, each benchmark covered three types of inference traffic: a control workload, a shared-prefix workload, and a multiturn workload:

| Workload | Description | Request shape | Rate (latency benchmark only) |
| --- | --- | --- | --- |
| control | Totally independent prompts with no shared prefix | 16,256-token unique prompt, 256 output tokens | 6 req/min |
| shared-prefix | Many users of a few long, shared system prompts or documents | One of 24 shared 16,000-token prefixes + 256 unique tokens, 256 output tokens | 12 req/min |
| multiturn | Many users, each with a progressively growing conversation | 8-turn conversations: 8,000-token first prompt, then 400 new tokens per turn plus history; 200 output tokens | 18 req/min (all turns) |

We ran each workload with a 60 s warmup period and a 45 s cooldown period, and measured the results over 240 s. The rate column and these windows apply to the latency benchmark; the capacity benchmark used only shared-prefix and multiturn workloads at fixed concurrency (see [Results and analysis: Capacity benchmark](#results-and-analysis-capacity-benchmark)).

In total the latency benchmark had 3 workloads × 2 arms × 3 trials = 18 runs. The arms ran one after the other, and order alternated between conditions. A request was measured iff it started inside the measurement window.

## Results and analysis: Unloaded latency benchmark

Summary: In the shared-prefix workload, **\[K\]inference cut median TTFT by 95% and median E2E latency by 45%**. In the multiturn workload, **\[K\]inference cut median TTFT by about 65% and median E2E latency by about 32%**, versus standard Kubernetes load balancing.

![ong description: Kinference tracks which GPU has each prompt prefix cached and sends new requests there, redirecting them to another GPU only when that one is too busy.](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6aeb3c6af86e8f42c70d7f23_TTFT%20Chart%20Selection.webp)

\[K\]inference cache-aware routing sends requests that share a prefix to the GPU that already has it cached.

### Primary metric: TTFT

| Workload | Stat | N (svc / kinf) | Service | Kinference | Ratio \[95% CI\] | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| control | median | 68 / 68 | 6.92 s | 6.83 s | 0.987 \[0.644, 1.013\] | no difference |
| control | p95 | 68 / 68 | 21.46 s | **12.33** s | 0.575 \[0.468, 0.975\] | Kinference faster |
| shared-prefix | median | 122 / 122 | 6.88 s | **0.31** s | 0.045 \[0.042, 0.596\] | Kinference faster |
| shared-prefix | p95 | 122 / 122 | 18.32 s | **9.24** s | 0.505 \[0.338, 0.947\] | Kinference faster |
| multiturn | median | 247 / 248 | 1.70 s | **0.59** s | 0.350 \[0.166, 0.537\] | Kinference faster |
| multiturn | p95 | 247 / 248 | 12.82 s | **7.70** s | 0.601 \[0.268, 0.787\] | Kinference faster |

(Confidence intervals are 95% CIs from a paired hierarchical bootstrap with 2,000 resamples.)

In our control conditions, median TTFT is indistinguishable between the arms (6.92 s vs 6.83 s). Without reusable prefixes, \[K\]inference adds no measurable latency, and the two pools perform alike–as we expect. Interestingly, the control p95 is another matter: 21.5 s on the service arm vs 12.3 s with \[K\]inference. This is likely due to \[K\]inference’s usage of vLLM queue size as well as KV cache overlap to predict TTFT–even with prompts that share zero overlap, \[K\]inference can still make intelligent balancing decisions and reduce tail latencies.

In our shared-prefix workload, \[K\]inference cuts median TTFT by about 95% (6.88 s to 0.31 s) and p95 TTFT by about 50% (18.3 s to 9.2 s), a clear improvement over default Kubernetes load balancing.

In our multiturn workload, \[K\]inference cuts median TTFT by about 65% (1.70 s to 0.59 s) and p95 TTFT by about 40% (12.8 s to 7.7 s)–also a clear improvement. Note that the gain here is smaller than on shared-prefix because the first turn of every conversation has nothing to reuse.

### Secondary metrics: ITL, E2E latency

| Workload | p50 ITL: svc / kinf (ratio \[CI\]) | p50 E2E latency: svc / kinf (ratio \[CI\]) |
| --- | --- | --- |
| control | 47 / 40 ms (0.85 \[0.60, 1.00\]) | 23.5 / 17.1 s (0.73 \[0.70, 1.01\]) |
| shared-prefix | 44 / 42 ms (0.96 \[0.87, 0.99\]) | 20.5 / 11.3 s (0.55 \[0.47, 0.78\]) |
| multiturn | 47 / 43 ms (0.90 \[0.75, 0.94\]) | 13.4 / 9.1 s (0.68 \[0.59, 0.77\]) |

Turning to inter-token latency (ITL) and end-to-end (E2E) latency, we see a similar story. In our shared-prefix workload, \[K\]inference cuts median end-to-end latency by about 45% (20.5 s to 11.3 s) and median ITL by about 4% (44 ms to 42 ms). In our multiturn workload, it cuts median end-to-end latency by about 32% (13.4 s to 9.1 s) and median ITL by about 10% (47 ms to 43 ms). On control, neither difference is significant; both CIs reach 1.

Most of the end-to-end gain comes from the shorter TTFT, which is a component of E2E latency. The rest comes from faster token generation: \[K\]inference’s replicas recompute fewer uncached prefixes, so there is less work that competes with producing the remaining tokens.

Output throughput was about equal on every workload, with ratios of 0.98–1.05 per trial, as expected at a fixed arrival rate that both arms keep up with. No request failed or was left unfinished.

## Results and analysis: Capacity benchmark

Summary: At peak, \[K\]inference served about 7.4× the service arm’s goodput on shared-prefix and about 3.5× on multiturn. It was able to attain our chosen SLO at concurrency 32 (the highest measured) on our shared-prefix workload, and concurrency 8 on the multiturn workload, whereas the kube-proxy approach was not able to attain the SLO at any concurrency level.

![Kinference keeps far more requests within SLOs than standard routing as concurrency grows, because it sends requests that share a prefix to the GPU that already has them cached.](https://cdn.prod.website-files.com/679957f782f1eca8a9594edb/6aeb3d5f094e852bcc82d61c_Goodput%20Chart.webp)

\[K\]inference handles many more requests within their SLO as load rises.

In our *unloaded latency* benchmark, we sought to measure the effect of \[K\]inference’s KV-cache-aware load balancing in isolation. In our *capacity* benchmark, we ask a different question: with N users, each sending its next request as soon as the last answer finishes, how many requests per minute can each endpoint serve within a latency SLO?

Our null hypothesis was that at each concurrency, the two endpoints would have the same *goodput*: the number of requests per minute that met the SLO. Our alternative hypothesis was that \[K\]inference would have higher goodput, and would keep meeting the SLO at higher concurrency. As before, we chose the primary metric up front: the goodput difference (\[K\]inference − service) at each concurrency.

### Picking the SLO

What SLO do we use? Ideally, we’d pick one from first principles–for example, we might not want a user waiting on a live chat bot to have to wait more than 500ms for the first token. For this experiment, we instead opted to pick them empirically, so that we could measure comparative behavior against SLOs that would actually be attainable–an SLO that neither approach could attain on the model and hardware chosen would not make for a very interesting benchmark!

Thus, we set our SLOs based on the uncached TTFT measured on an idle deployment, plus some padding.

| Workload | SLO | Uncached TTFT on an idle deployment |
| --- | --- | --- |
| shared-prefix | 90% TTFT ≤ 8 s | 6.7 s (16,000-token prefix) |
| multiturn | 90% TTFT ≤ 4 s | 3.3 s (8,000-token first turn) |

Note, again, that these SLOs are relatively high due to the specifics of the hardware and model combination we tested–unlikely to be viable for interactive chat, but perhaps viable for human-out-of-the-loop agentic flows.

### Load

Unlike our *unloaded latency* benchmark, our *capacity* benchmark is a closed loop: at concurrency N, N requests are always in flight (for multiturn, N conversations of 8 turns each). This means a faster endpoint also receives more requests per minute.

We ran the shared-prefix and multiturn workloads at concurrencies of 4, 8, 16, 24 and 32, with three trials each and a 60 / 180 / 60 s warmup / measured / cooldown window: 2 workloads × 5 concurrencies × 2 arms × 3 trials = 60 runs.

The results are as follows.

| Workload | Conc. | Req/min (svc / kinf) | SLO Attainment (svc / kinf) | Goodput (svc / kinf) | Difference \[95% CI\] | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| shared-prefix | 4 | 11.1 / 16.9 | 70% / **97%** | 7.8 / **16.3** | +8.6 \[4.0, 12.6\] | Kinference higher |
| shared-prefix | 8 | 19.9 / 36.0 | 69% / **98%** | 13.7 / **35.1** | +21.4 \[18.3, 24.2\] | Kinference higher |
| shared-prefix | 16 | 25.6 / 68.4 | 55% / **98%** | 14.0 / **66.9** | +52.9 \[48.9, 56.3\] | Kinference higher |
| shared-prefix | 24 | 28.2 / 96.0 | 44% / **97%** | 12.4 / **93.6** | +81.1 \[74.1, 89.3\] | Kinference higher |
| shared-prefix | 32 | 30.8 / 109.7 | 30% / **94%** | 9.3 / **103.0** | +93.7 \[71.3, 112.6\] | Kinference higher |
| multiturn | 4 | 19.7 / 25.1 | 76% / **92%** | 14.9 / **23.0** | +8.1 \[6.4, 9.7\] | Kinference higher |
| multiturn | 8 | 33.3 / 44.8 | 71% / **92%** | 23.8 / **41.3** | +17.6 \[13.9, 22.1\] | Kinference higher |
| multiturn | 16 | 42.4 / 72.4 | 56% / 87% | 23.7 / **63.0** | +39.3 \[35.6, 42.9\] | Kinference higher |
| multiturn | 24 | 34.3 / 93.2 | 38% / 89% | 12.9 / **82.7** | +69.8 \[64.1, 75.0\] | Kinference higher |
| multiturn | 32 | 36.6 / 88.1 | 35% / 77% | 12.7 / **68.1** | +55.4 \[48.0, 62.1\] | Kinference higher |

Here, goodput and difference numbers are reported in requests per minute, and confidence intervals come from the same paired hierarchical bootstrap as in the latency benchmark.

\[K\]inference had higher goodput at every concurrency on both workloads, and in every one of the 30 paired trials. The gap grows with load: on shared-prefix, \[K\]inference’s goodput is 2.1× the service arm’s at concurrency 4 and about 7.5× at 24; on multiturn, 1.5× at 4 and about 6.4× at 24.

In fact, despite our methodology above, the service arm didn’t meet the SLO at any concurrency we tested. Its best attainment was 70% on shared-prefix and 76% on multiturn, both at concurrency 4. \[K\]inference met the shared-prefix SLO at every concurrency up to 32, and the multiturn SLO up to 8 (at 16 and 24 it reached 87% and 89%, just short of the target).

| Workload | Peak goodput: svc / kinf (req/min) | At concurrency (svc / kinf) | Highest concurrency meeting SLO (svc / kinf) |
| --- | --- | --- | --- |
| shared-prefix | 14.0 / 103.0 | 16 / 32 | none / 32 |
| multiturn | 23.8 / 82.7 | 8 / 24 | none / 8 |

## Conclusion

In both *unloaded latency* and *capacity* benchmarks, \[K\]inference outperformed standard Kubernetes load balancing by significant amounts:

- In the unloaded latency benchmark, **\[K\]inference cut median TTFT by 95% and median E2E latency by 45%** on the shared-prefix workload, and **cut median TTFT by 65% and median E2E latency by 32%** on the multiturn workload.
- In the capacity benchmark, \[K\]inference served **7.4× the goodput on shared-prefix and about 3.5× the goodput on multiturn**. It was able to attain our chosen SLO at concurrency 32 (the highest measured) on our shared-prefix workload, and concurrency 8 on the multiturn workload, whereas the kube-proxy approach was not able to attain the SLO at any concurrency level.

We often think of load balancing as “nice to have”. For inference workloads that have shared prefixes (such as chat and coding sessions), and which are served from multiple replicas, KV-cache-aware load balancing is arguably *essential*. The difference can be enormous: we were able to demonstrate a 95% drop in TTFT in one experiment and an almost 7.5× capacity improvement in another.

Of course, intelligent load balancing is just one part of what \[K\]inference provides, alongside inference policies, rate limiting, tenant tracking and cost estimation, and much more. \[K\]inference is open source and you can install it on your Kubernetes cluster in seconds–check out the [\[K\]inference getting started guide](https://kinference.ai/getting-started/) and give it a whirl!

## FAQ

### How does KV-cache-aware load balancing work for LLM inference?

\[K\]inference predicts time-to-first-token (TTFT) for each request against every vLLM pod, using KV cache contents and queue size, then routes it to the pod with the lowest prediction. Requests that share a prefix land where that prefix is already cached, unless that pod is already busy, then another GPU can be selected if it is predicted to respond faster.

### How much does \[K\]inference reduce TTFT compared to Kubernetes Service load balancing?

In our benchmark, \[K\]inference cut median TTFT by 95% on a shared-prefix workload (6.88 s to 0.31 s) and by about 65% on a multiturn workload (1.70 s to 0.59 s), compared to a plain Kubernetes Service in front of the same 3 vLLM pods.

### Does \[K\]inference add latency when prompts don’t share a prefix?

No. On prompts with no shared prefix, median TTFT was 6.92 s through the Kubernetes Service and 6.83 s through \[K\]inference. \[K\]inference also cut p95 TTFT from 21.5 s to 12.3 s, likely because it factors in vLLM queue size as well as cache overlap.

### Why does default Kubernetes load balancing perform poorly for vLLM inference?

kube-proxy in iptables mode picks a random pod for each new connection, ignoring which pod already holds the request’s prefix in its KV cache. Pods without that prefix have to recompute the prefill, which adds latency and competes with token generation.

[![X](https://cdn.prod.website-files.com/678194e4895761e109e855b5/67db1c17fed959de67fade66_X.svg)](https://twitter.com/intent/tweet?url=https%3A%2F%2Fwww.buoyant.io%2Fblog%2Fdistributed-inference-benchmarks-kinference-vs-plain-kubernetes&text=Distributed%20Inference%20Benchmarks%3A%20%5BK%5Dinference%20vs.%20Kubernetes) [![linkedin](https://cdn.prod.website-files.com/678194e4895761e109e855b5/67db1bae0007443929164dd3_LinkedinIcon.svg)](https://www.linkedin.com/feed/?shareActive=true&url=https%3A%2F%2Fwww.buoyant.io%2Fblog%2Fdistributed-inference-benchmarks-kinference-vs-plain-kubernetes)