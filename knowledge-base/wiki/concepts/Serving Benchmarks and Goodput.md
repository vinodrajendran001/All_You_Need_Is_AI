---
type: concept
created: 2026-08-26
updated: 2026-10-07
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
  - src-2026-09-07-semianalysis-tpu-inferencex
  - src-2026-09-08-cohere-megakernel-serving
  - src-2026-09-14-li-long-context-latency
  - src-2026-09-10-lenz-epd-multimodal-serving
  - src-2026-09-28-inferact-tpu-megakernels-kimi-k3
  - src-2026-09-24-modal-quail-billion-tokens-per-minute
  - src-2026-10-02-epoch-agent-population
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

## Integration boundaries can erase operational metrics

[[Netflix - In-House LLM Serving]] adds a practitioner counterweight to this page. vLLM emits a large
metric set, but Triton's built-in bridge surfaced only **9 of more than 40 metrics** and omitted token
throughput, KV-cache utilization, and prefix-cache hits. Netflix built a proxy that combines Triton's
HTTP metrics with vLLM's on-disk metrics into one `/metrics` endpoint.

The lesson is not that production needs fewer measurements. It is that wrappers and compatibility
layers can silently discard the engine telemetry needed to interpret a benchmark or diagnose a
regression. Metric selection for alerting remains a separate operational decision, but the raw signals
must first survive the serving stack.

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

## One accelerator, four normalisations, results from +96% to -30%

[[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]] is the vault's clearest worked example of why the normalisation axis has to travel
with the result. Every figure below describes the **same silicon on the same model** (Qwen3.5 397B, FP8).

- **Normalised by interactivity, at 100 tok/s/user:** Ironwood costs **$0.181/M tokens** against B200's
  **$0.222** and B300's **$0.276** — 19% and 34% lower.
- **At 20 tok/s/user** Ironwood also leads on raw throughput — **9,364 tok/s/chip** versus 8,903 (B200)
  and 8,925 (B300) — giving **50.4% more tokens per dollar than B200 and 96.0% more than B300**.
- **At Google's internal TCO ($1.03/chip-hour), concurrency 256:** the advantage rises to **76.7% and
  130.2%** — but TPU mean TTFT is **5.41s against 3.75s (B200) and 2.40s (B300)**. SemiAnalysis states
  the limit itself: the figure "applies to this datapoint specifically, rather than every latency target."
- **Normalised by end-to-end response time the advantage compresses sharply.** At a 20-second median,
  Ironwood is **$0.098/M against $0.106 and $0.132** — 8% and 25% lower, not 50%. **Around the 30-second
  median point B200 wins outright.**
- **Against a disaggregated competitor it reverses**: GB300 NVL72 disaggregated versus aggregated TPUv7
  gives GB300 roughly **30% better perf/$ in the middle of the curve.**

**50% better, 8% better, or 30% worse, from one article.** The article is careful about this; downstream
citation of it will not be, which is the failure mode this page exists to prevent.

Two provenance caveats belong with the numbers: results are from an **Official Preview** on a single
bring-up model, and Google was presumably involved in the tuning while the NVIDIA configurations may not
have received equivalent attention.

## Synthetic uniform MoE routing understates real-traffic performance

[[Cohere - North Mini Code Megakernel Serving Engine]] inverts a standard MoE benchmarking assumption. Measured with **real expert
distributions the megakernel speedup is 1.32x at batch 8, against 1.14x under uniform synthetic routing**
— the opposite of the usual direction, where synthetic traffic flatters a system.

The mechanism is specific but the lesson is general: real requests concentrate on the same experts,
leaving sparser MoE work and therefore **more scheduling bubbles for the megakernel to absorb**. Uniform
routing removes exactly the load imbalance the technique is good at. Anyone benchmarking an MoE serving
path with synthetic uniform traffic is measuring the wrong distribution.

## Long-context latency needs a functional form

[[Jason Li - Latency Scaling Differences for GPT and Claude Models]] fits the same quadratic-capable
model to four APIs. Terra and Sol strongly favor curvature (`p=8.87e-19` and `1.48e-10`), while
Sonnet and Opus do not. The useful benchmark lesson is methodological: a few context-length points
cannot establish linear scaling, and a ten-million-token extrapolation is not a measurement.

Because TTFT includes the entire service path, the result should be reported as provider behavior
under the stated cache and request setup, not as an inferred attention implementation.

## Topology comparisons need a shared SLO

[[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]] compares aggregated, colocated, and
heterogeneous EPD at an ITL-under-100-ms goodput SLO. The detailed results show crossover behavior:
TTFT can improve while end-to-end latency regresses as decode grows. Reporting only the vendor's
5x/7x maxima would erase the workload surface that determines the winner.

## The headline is the best point on a curve the vendor usually published too

Two vendor posts ingested in September 2026 show the same pattern from opposite directions, and both
supply the correcting number themselves.

[[Modal - Hitting a Billion Tokens per Minute on One GPU]] leads with **over a billion tokens
processed per minute per H100** and **more than 10x faster than the vLLM baseline**, at **under 6
cents per billion tokens** on Modal's own service. Read one paragraph further and those figures belong
to **one multi-join query**. The cross-workload number from the same release is **1.84x faster than
vLLM, geometrically averaged** over the published AI-SQL benchmark — and Modal states that Quail
*falls behind* vLLM on an agent-trace benchmark, with two benchmark queries deliberately designed to
expose future weaknesses. Publishing your own loss is the behaviour this page's evidence standard
asks for and rarely gets; the 10x is still the number that will be quoted.

[[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]] shows the same compression in the
title. "Over 700 tokens/s" is **709 vs 452 tokens/s (1.57x) at acceptance length 6 with speculative
decoding at batch 8**, on a **~8.5 ms decode step evaluating 1 anchor and 7 proposed continuations
per launch**; at acceptance length 3 the same configuration gives **350 vs 229 (1.53x)**. The "nearly
2x" claim is a different configuration again — **batch 1 with no speculation, 249 vs 127 tokens/s
(1.96x)** — and without speculation the margin decays monotonically to **1.36x (865 vs 636) by batch
8**. Three numbers, one post, three operating points.

Note a collision worth avoiding: Inferact's batch-1 figure of 1.96x is a **hardware-plus-kernel
comparison**, while the 1.96x recorded in the section above is **speculative decoding's own batch-1
speedup** from a different source. They are unrelated, and the coincidence is a reminder that a ratio
is meaningless without its two terms.

Against the `CONTRIBUTING.md` standard this page adopts, both reports are incomplete in instructive
ways. Inferact supplies no confidence interval, no energy or cost-per-token figure, no full
methodology and no independent reproduction, and its baseline is a **hand-written TPU kernel against a
published vLLM GB200 recipe** — the same asymmetry the SemiAnalysis section above labels
"apples-to-bananas," where the configuration difference was worth more than the hardware difference.
Its correctness method is a numerical-regression check (**0.944 on GPQA-Diamond, 0.972 on GSM8K**
under greedy decoding at maximum reasoning effort), which clears the "a speed result needs a
correctness method" bar only in its weakest form. Modal describes its **own cost model as crude and
based on peak hardware rates**, noting that it "errs on the side of over-estimating peak performance"
— this page's rule that vendor peak numbers are not measurements, applied by a vendor to itself.

## Concurrent agents are defined by the latency and activity denominator

[[Jason Li - How Many AI Agents Could We Run]] reports DeepSeek V4 Pro reference deployments at
**31.4 sessions per GPU at P90 50 output tokens/second/user**, versus **14.4 at 100**.
Those are alternative streaming targets, not a single throughput figure. Output rate also omits
time to first token: selected Kimi K3 configurations meeting 50, 100, and 200 TPS targets report
P90 first-token delays of **39.8, 12.4, and 4.6 seconds**, respectively. Different deployment
configurations prevent reading that sequence as a one-variable scaling law.

The workload denominator matters just as much. Epoch combines **3,390 session/model groups from
3,382 sessions**; an AgentX root includes its subagent tree, while TraceLab may not capture the full
tree. Adjusted active time excludes identified human waits, caps other gaps at five minutes, and
retains tool waits. These are not counts of unique users or independent workers.

Retained-cache, frozen-price estimates are not observed bills, and capable output per second is
not task acceptance. Carry these definitions into any supply model instead of converting
sessions/GPU directly into productive people/GPU.

## Open questions

- Goodput requires a chosen SLO, and the SLO is a product decision. How should benchmarks compare systems whose users have genuinely different latency requirements?
- Public traces such as BurstGPT age as usage patterns shift, particularly as agent traffic replaces chat traffic. What keeps workload generators current?
- Agentic workloads have very different shapes — long tool-augmented sessions, bursty parallel sub-agent calls, heavy prefix reuse. The source lists session-aware and agentic scheduling as an unsettled frontier rather than a solved measurement problem.
- How should benchmarks account for prefix cache hit rates, which can dominate real performance but depend entirely on traffic locality?
- Can a benchmark meaningfully score a disaggregated system end to end, when its cost structure depends on interconnect properties the benchmark does not control?
- When a vendor publishes both a single-query maximum and a geometric mean over its benchmark suite, should the geometric mean be treated as the citable headline by default — and what would make that convention stick outside the vendor's own post?
- TTFT, TPOT and goodput all presuppose per-request latency targets. What metric applies to a prefill-only workload with one output token per request, where the requests are generated by a planner rather than waited on by a user?

## Related pages

- [[Jason Li - How Many AI Agents Could We Run]]
- [[Epoch AI]]
- [[AI Agents in Production]]
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
- [[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]]
- [[Accelerator Software Externalization]]
- [[SemiAnalysis]]
- [[Cohere - North Mini Code Megakernel Serving Engine]]
- [[Megakernels]]
- [[Cohere]]
- [[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]
- [[Modal - Hitting a Billion Tokens per Minute on One GPU]]
- [[Speculative Decoding]]
