---
type: concept
created: 2026-08-26
updated: 2026-08-27
tags:
  - concept
  - benchmarks
  - serving
  - evaluation
  - inference
source_ids:
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-23-wafer-ai-perf-contributing-source-policy
  - src-2026-08-21-hume-ai-asr-benchmark-optimization
  - src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
  - src-2026-07-17-netflix-in-house-llm-serving
status: active
---

# Serving Benchmarks and Goodput

## Definition

**Goodput** is the rate of requests a serving system completes *while meeting per-request latency targets*, as opposed to throughput, which counts completions regardless of whether they were fast enough to be useful. Serving benchmarks are the instruments that measure it, together with the component latencies it decomposes into: **TTFT** (time to first token), **TPOT** (time per output token), and the service-level objectives layered on them.

## Why it matters

Throughput and latency are in direct tension in LLM serving: larger batches raise tokens per second and simultaneously lengthen the wait for every request in the batch. A system tuned purely for throughput can look excellent on a dashboard while failing most of its users, and one tuned purely for latency can be uneconomical. Goodput is the metric that refuses to let a system optimize one at the other's expense, which is why it is the target that [[Prefill-Decode Disaggregation]] systems explicitly optimize for.

This page also gives the vault its first vocabulary for *how serving systems are measured at all* — before this ingest the vault had no mention of goodput, Orca, or MLPerf.

## The instruments

[[Wafer - AI Performance Engineering Resources]] separates the benchmark stack into three jobs:

- **Defining the metric.** Etalon formalizes TTFT, TPOT, goodput, and latency SLOs for generative serving, and is cited both as the entry-level mental model and as the evaluation standard.
- **Reproducible scenarios.** MLPerf Inference supplies standardized scenarios and load generation; MLPerf Endpoints extends this to endpoint-level interactive generative AI.
- **Realistic load.** ServeGen generates workloads that preserve properties of real production traces, and BurstGPT is a public trace of bursty LLM traffic.

The last category is the one most often skipped. A serving system evaluated on uniform synthetic load can behave completely differently under the bursty, heavy-tailed request-size distributions that real deployments see — which is also why fair scheduling under unknown, unequal request sizes is treated as a first-class serving problem rather than an afterthought.

## The evidence standard

The source's `CONTRIBUTING.md` states the rule this page most wants to preserve: **a performance number requires hardware and software versions, workload shapes or request distribution, precision and algorithm, a baseline, and a correctness method — and if any item is missing, the number is omitted rather than reported.**

Two consequences follow that the vault should apply generally:

- **Vendor peak numbers are not measurements.** Peak FLOPs describe a ceiling under conditions no real workload meets; the source pairs every architecture brief with an ISA or tuning guide for this reason.
- **A speed result without a correctness method is not a result.** This is the same boundary [[Benchmark Optimization]] draws from the opposite direction: there, systems scored well by reproducing flawed reference transcripts; here, a kernel or engine can score well by computing something subtly wrong. Both failures are invisible to the headline number.

## Operational metrics are a curated subset, not the full emission

[[Netflix - In-House LLM Serving]] adds a practitioner counterweight to this page. vLLM emits a large
metric set; Netflix runs production off a **deliberately curated subset**.

The distinction matters because benchmarking and operating pull in opposite directions. A benchmark
wants every number it can get, to characterize behavior across regimes. An on-call rotation wants the
smallest set that reliably indicates whether the service is healthy and what to do about it — a
metric nobody acts on is a page nobody should receive.

So the instruments described above are the right toolkit for *choosing* and *tuning* a deployment,
but they are not the dashboard. Selecting which of them become alerting signals, and which stay
diagnostic, is a separate decision this page should not conflate with measurement.

## A speedup number without a batch size is not a measurement

[[ByteByteGo - How to Make LLMs 3X Faster]] supplies the sharpest illustration of this page's
evidence standard. One systematic evaluation of speculative decoding on a 70B model reported **up to
1.96× at batch size 1, declining to 1.21× at batch size 128**, and falling **below baseline**
entirely under higher concurrency.

The same technique, the same model, the same hardware, spanning "nearly 2× faster" to "actively
harmful" — with only the concurrency changing. Any speculative-decoding speedup quoted without its
batch size is therefore uninterpretable, and the marketing convention of reporting the batch-size-1
figure systematically describes the least representative operating point for a loaded server.

This generalizes past speculation to every optimization that spends idle compute. Such techniques are
measured at exactly the load where idle compute is most abundant, and their benefit decays toward
zero — or past it — as the server fills up. A benchmark that does not sweep concurrency cannot
distinguish an optimization that helps production from one that only helps benchmarks, which is the
same failure this page records under [[Benchmark Optimization]].

Note also that speculative decoding does not move **time to first token** at all, since it applies to
generation rather than prefill. A goodput definition keyed to TTFT will score it as no improvement
whatsoever, while one keyed to inter-token latency will score it as a large win. The metric choice
determines the verdict.

## Open questions

- Goodput requires a chosen SLO, and the SLO is a product decision. How should benchmarks compare systems whose users have genuinely different latency requirements?
- Public traces such as BurstGPT age as usage patterns shift, particularly as agent traffic replaces chat traffic. What keeps workload generators current?
- Agentic workloads have very different shapes — long tool-augmented sessions, bursty parallel sub-agent calls, heavy prefix reuse. The source lists session-aware and agentic scheduling as an unsettled frontier rather than a solved measurement problem.
- How should benchmarks account for prefix cache hit rates, which can dominate real performance but depend entirely on traffic locality?
- Can a benchmark meaningfully score a disaggregated system end to end, when its cost structure depends on interconnect properties the benchmark does not control?

## Related pages

- [[Netflix - In-House LLM Serving]]
- [[ByteByteGo - How to Make LLMs 3X Faster]]
- [[Wafer - AI Performance Engineering Resources]]
- [[Benchmark Optimization]]
- [[Inference Serving Engines]]
- [[Prefill-Decode Disaggregation]]
- [[LLM Inference]]
- [[Multi-Turn Evaluation]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[AI Agents in Production]]
