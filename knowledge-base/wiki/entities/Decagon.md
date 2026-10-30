---
type: entity
created: 2026-10-30
updated: 2026-10-30
entity_kind: organization
tags:
  - entity
  - inference
  - ai-agents
source_ids:
  - src-2026-10-29-decagon-autoresearch-inference
status: active
---

# Decagon

## What it is

Decagon is represented here as an inference-stack operator using agents to run bounded
optimization campaigns, in
[[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]].
The post's byline is Pavi Dhiman and Cyrus Asgari; DecagonAI is the publishing account.

## Why it matters here

Its AutoResearch design combines a persistent Devin Cloud orchestrator, specialist subagents,
Modal GPU experiments, and shared versioned research records. Specialists propose falsifiable
interventions; only the orchestrator runs scored experiments through the common harness.
Humans initiate campaigns and approve production promotion.

The target is **requests per second per GPU within an endpoint's production latency limits**.
Replay preserves lengths, prefixes, timing, and concurrency; repeated baselines establish
noise, and the original campaign reference remains available after a win becomes the working
baseline. This makes Decagon a case study in [[Serving Benchmarks and Goodput]] and
[[Automated AI Research]], not merely an example of adding agents to performance work.

## Evidence boundary

Reported endpoint/configuration gains range from **1.05x to 2.50x**, with inconsistent wording
about whether the baseline is SGLang defaults or an existing production configuration. The
rows cannot be pooled or compounded into one fleet speedup. Draft acceptance improvements
are a different metric from serving throughput, and no all-in savings accounting or independent
replication is supplied.

Agent-initiated campaigns are future work. The current system improves serving artifacts and
some draft-model weights under human-defined objectives; it does not demonstrate autonomous
recursive invention of a better research process.

## Related pages

- [[Pavi Dhiman and Cyrus Asgari - Building an Inference Stack That Improves Itself]]
- [[Automated AI Research]]
- [[Loop Engineering]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Serving Engines]]
- [[Speculative Decoding]]
- [[Agent Delegation]]
- [[Persistent Wiki]]
- [[Recursive Self-Improvement]]
