---
type: source-summary
created: 2026-10-30
updated: 2026-10-30
source_id: src-2026-10-29-decagon-autoresearch-inference
source_title: Building an inference stack that improves itself
source_author: Pavi Dhiman and Cyrus Asgari
source_url: https://x.com/DecagonAI/status/2115511110120120437
tags:
  - source/summary
  - inference
  - evaluation
  - self-improvement
source_ids:
  - src-2026-10-29-decagon-autoresearch-inference
status: active
---

# Building an Inference Stack That Improves Itself

## Summary

Decagon describes AutoResearch campaigns that optimize inference configurations, GPU layouts,
engine patches, and speculative draft models against production-shaped replay. A persistent
Devin Cloud orchestrator coordinates specialists, while Modal runs GPU experiments. Humans
initiate campaigns and approve production changes. The durable contribution is an experiment
contract that makes plausible optimization proposals comparable and falsifiable.

## Key claims

### Preserve the workload, not just its average request rate

Redacted production replay retains token-length distributions, prefix/cache reuse, timing, and
concurrency. An open-loop Rust runner continues issuing scheduled requests when the server
slows, exposing queues instead of quietly reducing arrivals. Capacity sweeps warm the server
and reset prefix cache at each load step; production-shaped replays separately include bursts,
evolving cache state, autoscaling, and scale-up/down delays.

Candidates use the same request pool, schedule, and latency/error constraints. Repeated
baselines establish a noise floor. The optimization target is **requests per second per GPU
within each endpoint's production latency limits**, not unconstrained token throughput.

### Delegate proposals, centralize scored experiments

Subagents return an **explanation, intervention, prediction, and falsification condition**.
Only the orchestrator executes scored experiments through the common harness. Verdicts are
**Better, Same, Worse, or Invalid**; an invalid run is not evidence against the hypothesis.
A confirmed win becomes the working baseline, while the original configuration remains the
campaign reference. Combined changes still need ablations.

GPU count, elapsed time, GPU-hours, and training variants are bounded. Recipes and checkpoints
are pinned; CPU checks and a **50-step GPU rehearsal** precede expensive training. Lossless
changes and lossy quality tradeoffs follow different acceptance paths, with human approval
before production promotion.

### Draft-model agreement is only an intermediate objective

The starting DFlash2 drafter had about **17% higher served acceptance length** than the
production multi-token-prediction (MTP) drafter. Workload adaptation added about **14% relative
to that starting DFlash2 model**. These are different denominators, not throughput gains or
percentages to add.

Training experiments target the drafter's own rejection positions, refresh rollout checkpoints,
and vary sampling density and loss weighting. Better acceptance must still survive draft cost,
verification cost, and the workload's prefill/decode mix. The serving request pool is said to
be excluded from training and checkpoint selection, but repeated optimization against that
replay is not independent prospective validation.

### The reported gains belong to separate endpoints and configurations

The results table spans **1.05x to 2.50x** across configuration/intervention rows, without
full per-row model, hardware, and workload details. Examples include **1.65x** for a
prefill-decode-interval change, **1.34x** for DFlash2 adaptation, and **2.50x** for FP8 plus
NGRAM. The DFlash2 row compares
with the production drafter, not merely the unadapted DFlash2 checkpoint used in the acceptance
experiment.

The baseline wording is inconsistent: the lead-in permits **SGLang defaults or an already
tuned production configuration**, while the following paragraph describes each starting point
as the **production configuration**. Do not silently choose one interpretation, pool rows,
compound their gains, or call the range an all-in cost saving.

### Keep the conditions and failures in durable memory

Shared versioned Markdown and structured records retain unsuccessful trials, recipes, plots,
and conditions such as model, hardware, workload, and engine version. Contradictory results
across endpoints are preserved rather than turned into one universally good setting. Future
campaigns can reuse this record without inheriting an unqualified conclusion.

## Why it matters

[[Automated AI Research]] gains a concrete production-oriented loop with a human-defined
objective. [[Loop Engineering]], [[Agent Delegation]], and [[Persistent Wiki]] explain its
control, authority, and memory structures. [[Serving Benchmarks and Goodput]],
[[Inference Serving Engines]], [[Speculative Decoding]], and [[Software Performance Engineering]]
explain why the measured serving result, rather than an attractive local proxy, decides promotion.

## Tensions / open questions

- This is a first-party report, not independent replication or evidence of a global optimum.
  It does not publish an all-in accounting of agent, training, experiment, and serving costs.
- Agent-initiated campaigns and more novel self-generated training recipes are future plans.
  The current loop does not autonomously choose its business objective or authorize deployment.
- Replay fidelity and baseline discipline reduce confounding but do not prevent overfitting to
  a repeatedly consulted workload. Future-traffic validation remains a separate requirement.
- The write-up identifies useful safeguards but does not isolate the causal contribution of
  orchestration, subagents, the wiki, or any single training-recipe component.

## Affected pages

- [[Automated AI Research]]
- [[Loop Engineering]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Serving Engines]]
- [[Speculative Decoding]]
- [[Software Performance Engineering]]
- [[Agent Delegation]]
- [[Persistent Wiki]]
- [[Recursive Self-Improvement]]
- [[Decagon]]

## Raw capture

- [[knowledge-base/raw/sources/Building an inference stack that improves itself]]

## Citations

- Canonical URL: <https://x.com/DecagonAI/status/2115511110120120437>
- By Pavi Dhiman and Cyrus Asgari, published through DecagonAI on October 29, 2026;
  captured October 30, 2026. The account is the publisher, not the personal byline.

## Related pages

- [[Decagon]]
- [[Automated AI Research]]
- [[Loop Engineering]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Serving Engines]]
- [[Speculative Decoding]]
- [[Software Performance Engineering]]
- [[Agent Delegation]]
- [[Persistent Wiki]]
- [[Recursive Self-Improvement]]
- [[Knowledge Distillation]]
