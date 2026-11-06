---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-02-anil-compute-islands
source_title: The Hitchhiker’s Guide to Training on Compute Islands
source_author: Rohan Anil
source_url: https://www.coreauto.com/hitchhikers-guide-to-training-on-compute-islands
tags:
  - source/summary
  - distributed-training
  - training-infrastructure
  - mixture-of-experts
  - compute-capacity
source_ids:
  - src-2026-11-02-anil-compute-islands
status: active
---

# The Hitchhiker's Guide to Training on Compute Islands

## Summary

Rohan Anil, writing on the Core Automation blog, argues that frontier training should stop
assuming one large, contiguous, uniform cluster. Available capacity increasingly arrives as
"compute islands": scattered clusters "from a few hundred to a few thousand GPUs", held under
different contracts, accelerator generations, and providers. The post combines a market argument
(power, grid equipment, and land, not chips, are the binding constraint), a literature map of
low-communication training from DiLoCo onward, and a first-party case study. In that study a sparse
mixture-of-experts model of roughly **32B** total parameters trained across **160 B300** GPUs in the
US and **160 GB300** GPUs in Asia, roughly **9,000 miles** apart over a **25 Gbps** bidirectional
link, and reached about **1%** lower bits per byte than standard training at equal compute. A
second, single-site experiment replaced the all-reduce with pairwise butterfly exchanges among eight
learners. The post is a position paper with a hiring pitch, not an independently reproduced result.

## Key claims

### The bottleneck is physical, the fragmentation is architectural

- The post says the scarce input for accelerated compute is "power, grid equipment and land", and
  that this will hold "until 2028". It quotes Satya Nadella on chips "sitting in inventory that I
  can't plug in" and Elon Musk on X (October 25, 2026) expecting "stranded compute in partially
  complete data centers".
- Supporting market claims are cited to third parties: gas turbines spoken for through 2028,
  large transformers taking more than three years, local opposition stopping at least **20**
  projects in one quarter, and a Goldman Sachs expectation that **50–60%** of scheduled US
  capacity for the next one to two years comes online on time, against a historical **72%**. A site
  under **20 MW** "often plugs into the grid that's already there".
- The author separates a **physical problem** software cannot fix from an **architectural problem**
  it can: training stacks assume a single uniform cluster, so capacity that does not fit that shape
  goes unused for frontier runs.

### Capacity comes in tiers, so the training method should be fungible

- The post sorts the market into committed multiyear capacity (Nebius and CoreWeave deals with
  Microsoft and Meta "worth up to $19.4 billion"), reservable capacity (AWS, Lambda, Together AI,
  "from a single node to hundreds of GPUs, for hours to months"), and spot or resale capacity (SF
  Compute, National Compute Grid).
- Its position has three parts: use the fast interconnect inside an island; across islands,
  exchange updates on a slower schedule and codesign the optimizer with the networking layer; and
  measure progress as **training goodput** plus final model quality.

### Low-communication training is a lineage, not one trick

- The history draws on local updates, compression, gossip, and fault-tolerant averaging, with
  federated learning contributing the pseudo-gradient and outer optimizer.
- It separates **data-parallel** methods (DiLoCo, DisTrO, DeMo), where each site holds a full replica,
  from **model-parallel** methods (SWARM, Node0, Agora), which split the model across machines. The
  two families address different constraints "and can be combined together".
- The literature table is the author's own characterization. Highlights: DiLoCo (November 2023)
  with **8** workers matched fully synchronous training while communicating **500×** less, at up to
  **400M** parameters, using AdamW inside and Nesterov momentum outside; INTELLECT-1 trained **10B**
  parameters on **1T** tokens across five countries on up to **112** H100s; Streaming DiLoCo cut
  bandwidth by about two orders of magnitude; DiLoCoX ran a modified Qwen1.5-107B over an emulated
  1 Gbit/s link "with a measurable quality gap"; Decoupled DiLoCo matched data-parallel quality up to
  **9B** under simulated failures and ran a real **12B** job with eight learners across four US
  regions; Agora/Pluralis-8B trained **8.6B** parameters on **500B** tokens over **40** days on
  **330** nodes. A cross-facility HPC run is the cautionary row: perplexity **34.7** against
  **28.2** for the centralized baseline.

### Case study: one MoE model across two continents

- **Model:** about 32B total parameters, 32x sparsity, an MoE layer in every block, **256**
  experts with top-**8** routing, no shared experts.
- **Heterogeneity:** B300 hosts with eight GPUs and GB300 hosts with four GPUs, different
  parallelism schemes, and different total batch sizes. Each site trained on its own data shard
  with local expert parallelism; microbatch and gradient-accumulation settings were tuned so step
  times were similar.
- **Synchronization:** fragment by fragment, staggered across each **50-step** window, borrowing
  fragment-wise, overlapped, asynchronous updates from Streaming and Decoupled DiLoCo. A
  late-arriving update can still be committed.
- **Optimization and communication:** each site used a variant of Distributed Shampoo; transfers
  used stochastic rounding with error feedback; MoE routing statistics were synchronized
  separately at every step.
- **Result:** about 1% lower bits per byte at the same compute as the largest standard run:
  **0.2525** versus **0.2549** on a general-coding eval and **0.1995** versus **0.2017** on a
  systems-and-kernels eval.

### Tail latency is the transport problem

Citing "The Tail at Scale", the post lists four transport tactics: spread demand (stagger, pace
total traffic, cap per-socket send rates, keep control messages independent); keep connections
warm and verified (heartbeats, reconnect with jitter, preallocated memory); chunk every transfer
so any healthy connection can claim a chunk; and repair only what is missing, with a bounded
number of duplicate sends. Redundant transfers launched at a deadline "cut tail latency".

### Butterfly mixing replaces the all-reduce

At one site, **64** GB300 GPUs were split into eight eight-GPU cells, each training its own copy of
the 32B MoE. Cells exchanged updates pairwise; after three rounds every update had reached all
eight, "with no all-reduce", following Zhao and Canny's butterfly mixing. Pairings differed by
fragment. Each fragment was exchanged six times every 50 steps (two full butterflies), and two steps
after sending, a cell blended the pair's result at equal weight. The post states only that
"Training quality matched the baseline".

### Implications and risk

The author expects fungible runs that tolerate preemptible capacity and mixed accelerator
generations or vendors, and a larger set of actors able to train. It also concedes that "one faulty
or compromised site can quietly degrade or tamper with the model". Google's Project Suncatcher and
an October 30, 2026 orbital Gemma 4 haiku are cited as the extreme version; that was inference on
one satellite, not distributed training.

## Why it matters

[[Distributed Training Parallelism]] has so far described lockstep collectives inside one
high-bandwidth fabric. This source adds the cross-island tier, where synchronization frequency
becomes a design variable. [[ML Systems at Scale]] gains a capacity-shape argument: hardware that a
uniform-cluster job cannot use is effectively stranded. [[GPU Fleet Reliability]] gains a
tolerate-rather-than-wait design in which late updates commit and redundant transfers absorb tails.
[[Mixture of Experts]] gains a training-side case where routing statistics need tighter
synchronization than the expert weights.

## Tensions / open questions

- First-party evidence from a company that ends the post with "We're hiring". One run per
  configuration, no error bars, and no independent replication.
- The post recommends measuring training goodput but reports no goodput, throughput, wall-clock,
  utilization, or communication-volume figures for the case study.
- The gain is not isolated. The comparison changes the optimizer (a Distributed Shampoo variant),
  communication, and data sharding at once, so the 1% cannot be attributed to distribution itself.
- The butterfly experiment ran inside one site, without a slow link, and reports no numbers.
- Market and literature claims are the author's summaries of cited work; this ingest did not
  verify those papers or reports.
- The integrity risk is named but not addressed with a mechanism.

## Affected pages

- [[Distributed Training Parallelism]]
- [[ML Systems at Scale]]
- [[GPU Fleet Reliability]]
- [[Mixture of Experts]]

## Raw capture

- [[knowledge-base/raw/sources/The Hitchhiker’s Guide to Training on Compute Islands]]

## Citations

- Canonical URL: <https://www.coreauto.com/hitchhikers-guide-to-training-on-compute-islands>
- Byline: Rohan Anil. Publisher: Core Automation (BibTeX journal field "Core Automation Blog").
- Published November 2, 2026; captured November 4, 2026. The `utm_source` tracking parameter is
  omitted from the summary URL; the raw capture is unchanged.

## Related pages

- [[Distributed Training Parallelism]]
- [[ML Systems at Scale]]
- [[GPU Fleet Reliability]]
- [[Mixture of Experts]]
- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]]
- [[Netflix - Reliable GPU Compute for Training and Inference]]
- [[LLM Training Pipeline]]
- [[Ali Zahid Raja - Your Model Doesn't Have to Fit in Your GPU Anymore]]
- [[ByteByteGo - How Nvidia's New Nemotron Model Works]]
