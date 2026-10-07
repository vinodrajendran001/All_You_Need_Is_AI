---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-10-04-ben-tovim-ai21-kueue-gpu-fleet
source_title: "From manual negotiation to automated scheduling: How AI21 manages its GPU fleet with Kueue"
source_author: Asaf Ben-Tovim
source_url: https://www.ai21.com/blog/how-ai21-manages-its-gpu-fleet-with-kueue/
tags: [source/summary, distributed-training, gpu, systems]
source_ids: [src-2026-10-04-ben-tovim-ai21-kueue-gpu-fleet]
status: active
---

# Asaf Ben-Tovim - How AI21 Manages Its GPU Fleet with Kueue

## Summary

AI21 describes replacing manual negotiations over one shared GKE cluster of roughly **10,000 GPUs**
with Kueue workload admission. The main problem is not distributing a tensor computation; it is
deciding which complete jobs may start, where their resources fit, and when lower-priority work
must yield. This is a first-party operations case study.

## Key claims

- Gang/all-or-nothing admission prevents a large job from holding a partial allocation indefinitely
  while waiting for the rest. Priority and preemption alone do not solve fragmentation or starvation.
- Total free GPUs are insufficient information. Eight free GPUs split **1+1+4+2 across four nodes**
  cannot host a job that requires eight GPUs on one node.
- AI21's v0.15 deployment redesign enables Admission Fair Sharing (AFS) alongside
  topology-aware scheduling (TAS). TAS was already available but **unused in its v0.10 setup**;
  this is not a claim that both features first appeared in the same Kueue release. AFS uses
  historical chip-hours to order admission; preemption fair sharing is a separate mechanism.
- TAS and `LeastFreeCapacity` packing help avoid admissions that cannot be placed and preemptions
  that would free the wrong shape of capacity.
- Guaranteed, opportunistic/preemptible, and on-demand capacity have different operating contracts.
  A queue guarantee against scheduler preemption does not prevent the cloud provider from
  reclaiming spot capacity.

The reported before/after figures are:

| Measure | Before | After |
| --- | --- | --- |
| Manual interventions per week | 20 | 0 |
| Fragmentation | 15% | 8% |
| Hero-job starvation time | 72 hours | 12 hours |

The article's **83% time-to-start reduction** refers to the last comparison. It is not an 83%
reduction in training time or a measured improvement across all jobs.

## Why it matters

A good parallelism plan still needs a schedulable allocation. This case adds admission order,
historical fairness, topology, and priority to the model-factory record, separating queue time from
training throughput and chip utilization from useful progress.

## Tensions / open questions

The source does not disclose a detailed measurement window, sample, or controlled comparison.
Near-100% reserved-fleet utilization is an operating target, not a demonstrated universal optimum.
Some prose blends admission fairness with preemption fairness; they should remain distinct in the
wiki. The capture's description metadata contains unrelated verifier/8B-model copy, while the body
is about GPU scheduling. The raw capture is preserved rather than silently corrected.

## Affected pages

- [[Distributed Training Parallelism]]
- [[Model Factory]]
- [[ML Systems at Scale]]
- [[Google Cloud]]

## Raw capture

- [[From manual negotiation to automated scheduling How AI21 manages its GPU fleet with Kueue]]

## Citations

- Canonical URL: <https://www.ai21.com/blog/how-ai21-manages-its-gpu-fleet-with-kueue/>
- Published October 4 and captured October 6, 2026.

## Related pages

- [[AI Accelerator Architecture]]
- [[Serving Benchmarks and Goodput]]
- [[Jason Li - How Many AI Agents Could We Run]]
