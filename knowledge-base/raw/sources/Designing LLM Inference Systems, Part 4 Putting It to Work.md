---
title: "Designing LLM Inference Systems, Part 4: Putting It to Work"
source: "https://medium.com/@wszjzhang/designing-llm-inference-systems-part-4-putting-it-to-work-cd2b9f32805d"
author:
  - "[[intelligentLearn]]"
published: 2026-11-24
created: 2026-11-25
description: "More"
tags:
  - "clippings"
---
Where the real trade-offs live, worked through with numbers you can check.

*Part 4 of 4, the last part of the trade-offs article, from “Designing LLM inference systems”, the second half of a series on LLM inference serving. It walks the six layers once more in L0-to-L5 order, works the long-document case from* [*Part 1*](https://medium.com/@wszjzhang/from-symptoms-to-fixes-the-trade-offs-inside-an-llm-inference-system-part-1-start-with-the-9aa825ca7969) *end to end, and closes with the appendices the earlier parts refer to.*

## 15\. The six-layer map

Part 2 used one practical investigation order. Now walk the framework bottom-up, L0 → L5, for reference. In each layer below, the useful line is the signal that says to investigate it. The line before that says what may need checking after a change.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GcEX2rnqLcpnj471HHl1Vg.png)

*The right column measures this corpus’s coverage, not the layer’s importance.*

**Capacity (L0)** — what it decides: where GPUs come from and at what price; which constraint it relieves: none of them — it decides **how many** are available; main cost / what to check next: cost → **availability and state rebuilding**; what signal says investigate this layer: unit cost is unacceptable and interruption is tolerable

**Substrate (L1)** — what it decides: how GPUs get carved up and how replicas start; which constraint it relieves: the **waiting time** to start a replica; main cost / what to check next: prewarming **holds GPUs idle**; sharing brings **interference**; what signal says investigate this layer: scaling out cannot keep up with bursts, or GPU utilization is persistently low

**Engine internals (L2)** — what it decides: how time and memory on one GPU get divided; which constraint it relieves: **state footprint** and **data movement**; main cost / what to check next: scheduling and chunking overhead; **interconnect bandwidth** becomes the new bottleneck; what signal says investigate this layer: memory is the first wall you hit, or long prefills block decode

**Replica composition (L3)** — what it decides: what a replica is made of and how many instance types; which constraint it relieves: prefill/decode **interference** and **configuration coupling**; main cost / what to check next: **KV transfer across instances**; ratio imbalance; model copies per selected P:D composition; what signal says investigate this layer: chunking no longer holds the interference down and traffic is prefill-heavy

**Routing and admission (L4)** — what it decides: who a request goes to, and whether to accept it; which constraint it relieves: **waiting time**, and **repeated computation**; main cost / what to check next: load imbalance and queueing on hot instances; what signal says investigate this layer: replicas are no longer equivalent, or queue time starts to dominate TTFT

**Contract and failure semantics (L5)** — what it decides: what happens when it is not met; which constraint it relieves: relieves no resource constraint — it **defines who gets sacrificed**; main cost / what to check next: it takes a **product decision**, not only an engineering one; what signal says investigate this layer: you cannot answer “what gets sacrificed” when capacity is short

> ***A note on corpus coverage.*** *Paper counts measure* ***this corpus’s coverage and reading depth, not directly the credibility of a claim****; why L0 and L5 are so thin is in section 11 and Appendix A.*

## 16\. The case walkthrough

Start with execution feasibility. Using the unrounded FLOP counts in section 5, TP=4 would need ≈ **76%** of BF16 dense peak to fit this prefill into 2 s; at the uncited 40% teaching assumption it takes about **3.8 s**. First test isolated-request execution on an empty system, then investigate queueing and colocation interference. Chunked prefill can protect the token gap of requests already decoding, and P/D disaggregation can decouple interference and configuration, but neither reduces this cold request’s own prefill work.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*OwNYtiY8yiPwBiUUbkCGNw.png)

*Same estimate as section 5. The 40% is an uncited teaching assumption, and 3.8 s is what that assumption produces.*

The walkthrough produces three kinds of answer:

**Computed result — the capacity ceiling.** Each TP=4 replica has about 159 GB of KV capacity, and each long-document request consumes about 10.9 GB, so flooring to whole requests leaves **≈ 14 long-document requests**. This is a **capacity ceiling, not achievable concurrency**; SLOs, scheduling and bursts can only push the achievable value lower.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*sXffJr-Qerq_fZfktf65fw.png)

*Same derivation as section 5. Fourteen is a capacity ceiling, not achievable concurrency.*

**Conditional choice — an illustrative cache-affinity example.** These numbers are illustrative, **not measured**: if a hit saves 1.8 s of execution, the hot replica adds 0.6 s of queueing, and transfer adds 0.2 s, then 1.8 − 0.6 − 0.2 = **1.0 s**; choosing the hot replica has a net benefit. As extra wait rises, that benefit shrinks. Once queueing plus transfer exceeds the execution saved by the hit, the choice flips to the less-loaded replica.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*LbFwjbERkSGEzrm_lSO77g.png)

*Illustrative seconds from section 16, not a measurement. The choice flips when queueing plus transfer exceed the 1.8 s saved.*

**Concrete measurement plan — make each unknown resolve a decision.**

- Measure cold/hot-prefix and reusable-length distributions to determine the execution saved by a hit and whether affinity is worthwhile.
- Measure arrival and burst rates, plus per-replica queue wait and prediction error, to choose among joint balancing, admission and affinity.
- Measure KV transfer time and overlap to decide whether the movement introduced by P/D disaggregation or cross-replica reuse fits the TTFT budget.
- Measure the distribution from scale-out decision to replica readiness to decide whether scaling can catch a burst. The **\>40 s** cold start in HydraServe (Lou et al., 2025) is an example scoped to that paper’s environment, not a value to apply directly to this case.
- Compare the candidate policy with the current baseline, per workload class, on P95 TTFT, P95 token gap, SLO attainment, goodput, and timeout, rejection and quality outcomes. Adopt it only if those service-boundary results improve.

The four parts are one argument. Part 1 set up the operator, memory, and timeline ledgers, so a slow request has a name. Part 2 walked the six layers in the order a symptom points, and named what a change at that layer costs. Part 3 holds a reported improvement until the comparison, the service boundary, and the unmeasured variables are on the page. This part applies that to one long-document case: the ceiling is computed, the conditional choice stays labeled as arithmetic, and every remaining branch is a measurement. The appendices turn the same standard back on the reading.

## Appendix

## A. The bias in this reading list

It is not a neutral snapshot of the field but the product of one keyword search, with a budget per layer, a cap on each layer, and layer assignment done mostly from titles and abstracts. The figure below measures this article’s own bias.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*6yk6yXNtA5PFlrgukzTOZQ.png)

*The layer distribution of this corpus reflects the budget I gave each layer while collecting it every bit as much as it reflects the field itself.*

- **Half of how thin L5 is is my own doing.** It got the smallest budget (3 queries, capped at 70), and one of those three was `context compression long context agent LLM` — **which is not a contract-layer search term at all**. So "L5 has only 3 papers" is **first of all an artefact of how I searched**, and cannot be read as a finding about the field.
- **L0 is the opposite failure.** The cap was 150 and only 5 were admitted. Plenty of budget and almost nothing collected says the problem is that the query terms do not match this layer’s actual vocabulary, not that the allowance was too small.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*e47_uBM_FmXNA3J0lZyfog.png)

*The corpus is overwhelmingly recent, so what it captures is the current shape of the problem, not its history.*

So **this article is not the place to learn how the field evolved**: foundational work such as Orca and FlashAttention sits outside the corpus (Appendix D).

## B. The layers are only a conceptual framework

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*m0STgB-BobqbcOLFn5PNqw.png)

*Real systems straddle the layers; the layering is there to explain them, not to describe what they actually are.*

**108 of the 172 papers (about six in ten) carry a secondary-layer label.** That proportion is itself a reminder about the six-layer framework: it is a ruler for organizing an explanation, not a natural seam in the field. The most interesting mechanisms in the body — P/D disaggregation, cache-affinity routing — are precisely the ones straddling those seams.

Note the counting convention: **the primary layer is a single label and secondary layers are additional labels, so these numbers are not additive with the per-layer totals elsewhere.**

## C. Anchor papers (outside the corpus)

A few unavoidable works **were not captured by this search**, but the body needs them as background. They go in a separate background reference list, **are not counted in the 172**, and take part in no statistics: Orca (OSDI ’22, continuous batching), FlashAttention (2205.14135, the case for “operator byte counts ≠ actual HBM traffic”), Splitwise (2311.18677, P/D disaggregation).

**Orca’s status differs from the other two.** FlashAttention and Splitwise are mentioned in the body only as background, and the claims they support have deeply read sources of their own; continuous batching as a mechanism **has Orca as its only source**. That is the article’s one mechanism-level claim landing outside the deeply read set; Appendix C records the exception in the article’s evidence self-claim.

## D. Mechanism families this article does not develop

The body deep-dives into 12 mechanisms, filtered by whether the running case genuinely forces us into a trade-off. The following **have papers in the corpus but are not developed here**:

**Quantization and low precision (weights/activations/KV)** — the case does not force a precision trade-off, and it pulls on model quality, which is outside the scope of a serving-stack discussion

**Speculative decoding and multi-token prediction** — it changes the serial nature of token dependence itself, which deserves an article of its own

**Expert placement and routing for MoE** — the state structure differs substantially from a dense model; the body only notes the architectural boundary at L3 without developing it

**Cross-request reuse policies for prefix caching** — L4 covers only the one “affinity vs balance” trade-off; the design space of reuse policies itself is not developed

**Energy and frequency scaling** — it is in the corpus, but the case’s constraints are latency and capacity, not power

**Edge and on-device inference** — the input card is restricted to datacenter GPUs, and the constraint structure on-device is different

**Sparse/linear attention for long context** — it changes the linear-KV-growth constraint itself, which is the model side

**This is not a “future work” list, it is a statement of this article’s boundary.** Any one of them could change the body’s conclusions — if sparse attention became widespread, for instance, the shape of the memory budget in section 5 would change.

## E. Full table: the 172 in-scope papers

**172** papers in scope. The **evidence depth** label on each entry is the point of this list: it says, paper by paper, how far this article actually read.

- **deeply read** (15): read end to end, with every quote checked verbatim against the source. **The body’s mechanism-level claims rest on this tier alone, with one exception — continuous batching, whose source is an anchor paper outside the corpus; see Appendix D.**
- **full text** (146): fetched and available, used for placement and to re-check the layer assignment, but not to support mechanism detail.
- **abstract** (11): title and abstract only — enough for placement, no more.

The 8 excluded papers are not listed here: a list would itself be a way of discussing the papers this article left out.

**1 · 2026** — layer: L0; secondary: L3; paper: `balamurugan2026omnipilot` — OmniPilot: An Uncertainty-Aware LLM Inference Advisor for Heterogeneous GPU Clusters; evidence depth: full text

**2 · 2026** — layer: L0; secondary: L3; paper: `shuntserve2026` — ShuntServe: Cost-Efficient LLM Serving on Heterogeneous Spot GPU Clusters; evidence depth: full text

**3 · 2025** — layer: L0; secondary: L2; paper: `kim2025costefficient` — Cost-Efficient LLM Serving in the Cloud: VM Selection with KV Cache Offloading; evidence depth: full text

**4 · 2025** — layer: L0; secondary: L4; paper: `mao2025skyserve` — SkyServe: Serving AI Models across Regions and Clouds with Spot Instances; evidence depth: full text

**5 · 2023** — layer: L0; secondary: L3; paper: `miao2023spotserve` — SpotServe: Serving Generative Large Language Models on Preemptible Instances; evidence depth: **deeply read**

**6 · 2026** — layer: L1; secondary: L3; paper: `liu2026foundry` — Foundry: Template-Based CUDA Graph Context Materialization for Fast LLM Serving Cold Start; evidence depth: full text

**7 · 2026** — layer: L1; secondary: L0; paper: `luo2026c2cserve` — C2CServe: Leveraging NVLink-C2C for Elastic Serverless LLM Serving on MIG; evidence depth: full text

**8 · 2026** — layer: L1; secondary: L2; paper: `taherin2026hydra` — Hydra: Phase-Aware Workload Characterization of LLM Inference across Edge SoC Generations, Backends, and Quantization Levels; evidence depth: full text

**9 · 2026** — layer: L1; secondary: L0; paper: `wang2026elastico` — ElastiCo: Elastic Configuration and Interference-Aware Orchestration for GPU Clusters; evidence depth: full text

**10 · 2026** — layer: L1; secondary: L4; paper: `wang2026energyaware` — Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs; evidence depth: full text

**11 · 2026** — layer: L1; secondary: L2; paper: `wang2026faasmoe` — FaaSMoE: A Serverless Framework for Multi-Tenant Mixture-of-Experts Serving; evidence depth: full text

**12 · 2025** — layer: L1; secondary: L4; paper: `darzi2025predictable` — Predictable LLM Serving on GPU Clusters; evidence depth: full text

**13 · 2025** — layer: L1; secondary: L0; paper: `dongare2025hybrid` — Hybrid Learning and Optimization-Based Dynamic Scheduling for DL Workloads on Heterogeneous GPU Clusters; evidence depth: full text

**14 · 2025** — layer: L1; secondary: L5; paper: `liu2025greenllm` — GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving; evidence depth: full text

**15 · 2025** — layer: L1; secondary: L0; paper: `lou2025hydraserve` — HydraServe: Minimizing Cold Start Latency for Serverless LLM Serving in Public Clouds; evidence depth: **deeply read**

**16 · 2025** — layer: L1; secondary: L3; paper: `lou2025warmserve` — WarmServe: Enabling One-for-Many GPU Prewarming for Multi-LLM Serving; evidence depth: full text

**17 · 2025** — layer: L1; secondary: L4; paper: `xu2025cloud` — Cloud Native System for LLM Inference Serving; evidence depth: full text

**18 · 2023** — layer: L1; secondary: L4; paper: `dhakal2023dstack` — D-STACK: High Throughput DNN Inference by Effective Multiplexing and Spatio-Temporal Scheduling of GPUs; evidence depth: full text

**19 · 2022** — layer: L1; secondary: L4; paper: `kim2022paris` — PARIS and ELSA: An Elastic Scheduling Algorithm for Reconfigurable Multi-GPU Inference Servers; evidence depth: full text

**20 · 2026** — layer: L2; paper: `bai2026alignedserve` — AlignedServe: Orchestrating Prefix-aware Batching to Build a High-throughput and Computing-efficient LLM Serving System; evidence depth: abstract

**21 · 2026** — layer: L2; secondary: L5; paper: `chen2026beyond` — Beyond Greedy Chunking: SLO-Aware Sliding-Window Scheduling for LLM Inference; evidence depth: full text

**22 · 2026** — layer: L2; paper: `delavande2026understanding` — Understanding Efficiency: Quantization, Batching, and Serving Strategies in LLM Energy Use; evidence depth: full text

**23 · 2026** — layer: L2; paper: `du2026c2kv` — C2KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference; evidence depth: abstract

**24 · 2026** — layer: L2; paper: `gusev2026fractal` — Fractal KV-Cache Archives: Lossless Symbolic Storage with In-Place Retrieval for Long-Context LLM Inference; evidence depth: abstract

**25 · 2026** — layer: L2; paper: `han2026kara` — KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression; evidence depth: full text

**26 · 2026** — layer: L2; paper: `kim2026tangram` — Tangram: Unlocking Non-Uniform KV Cache Compression for Efficient Multi-turn LLM Serving; evidence depth: full text

**27 · 2026** — layer: L2; paper: `ko2026vllm` — vLLM Hook v0: A Plug-in for Programming Model Internals on vLLM; evidence depth: full text

**28 · 2026** — layer: L2; paper: `kong2026an` — An Interpretable Latency Model for Speculative Decoding in LLM Serving; evidence depth: full text

**29 · 2026** — layer: L2; secondary: L4; paper: `li2026wisp` — WISP: Waste- and Interference-Suppressed Distributed Speculative LLM Serving at the Edge via Dynamic Drafting and SLO-Aware Batching; evidence depth: full text

**30 · 2026** — layer: L2; paper: `liao2026zipage` — Zipage: Maintain High Request Concurrency for LLM Reasoning through Compressed PagedAttention; evidence depth: full text

**31 · 2026** — layer: L2; secondary: L1; paper: `lin2026kvdrive` — KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference; evidence depth: full text

**32 · 2026** — layer: L2; secondary: L3; paper: `luo2026smartgen` — SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer; evidence depth: full text

**33 · 2026** — layer: L2; secondary: L5; paper: `ma2026orbitflow` — OrbitFlow: SLO-Aware Long-Context LLM Serving with Fine-Grained KV Cache Reconfiguration; evidence depth: full text

**34 · 2026** — layer: L2; paper: `mamo2026comparative` — Comparative Characterization of KV Cache Management Strategies for LLM Inference; evidence depth: full text

**35 · 2026** — layer: L2; secondary: L5; paper: `mo2026serving` — Serving Hybrid LLM Loads with SLO Guarantees Using CPU-GPU Attention Piggybacking; evidence depth: abstract

**36 · 2026** — layer: L2; paper: `patel2026polykv` — PolyKV: A Shared Asymmetrically-Compressed KV Cache Pool for Multi-Agent LLM Inference; evidence depth: abstract

**37 · 2026** — layer: L2; paper: `qiang2026mosaickv` — MosaicKV: Serving Long-Context LLM with Dynamic Two-D KV Cache Compression; evidence depth: full text

**38 · 2026** — layer: L2; secondary: L1; paper: `ray2026an` — An Internet for the KV Cache: Rethinking Classical Infrastructure Boundaries in the LLM Inference Age; evidence depth: full text

**39 · 2026** — layer: L2; paper: `sekar2026rksc` — RKSC: Reasoning-Aware KV Cache Sharing and Confident Early Exit for Multi-Step LLM Inference; evidence depth: full text

**40 · 2026** — layer: L2; paper: `skis2026` — Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization; evidence depth: full text

**41 · 2026** — layer: L2; secondary: L4; paper: `wang2026calvo` — CALVO: Improve Serving Efficiency for LLM Inferences with Intense Network Demands; evidence depth: full text

**42 · 2026** — layer: L2; secondary: L3; paper: `woo2026prefillshare` — PrefillShare: A Shared Prefill Module for KV Reuse in Multi-LLM Disaggregated Serving; evidence depth: full text

**43 · 2026** — layer: L2; paper: `xu2026kv` — KV Cache Optimization Strategies for Scalable and Efficient LLM Inference; evidence depth: full text

**44 · 2026** — layer: L2; paper: `yang2026pagedweight` — PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization; evidence depth: full text

**45 · 2026** — layer: L2; secondary: L4; paper: `yao2026efficiency` — Efficiency and Cost Alignment in Batched LLM Serving via Resource-Fair Scheduling; evidence depth: full text

**46 · 2026** — layer: L2; paper: `yao2026vericache` — VeriCache: Turning Lossy KV Cache into Lossless LLM Inference; evidence depth: full text

**47 · 2026** — layer: L2; secondary: L3; paper: `ye2026crosspool` — CrossPool: Efficient Multi-LLM Serving for Cold MoE Models through KV-Cache and Weight Disaggregation; evidence depth: full text

**48 · 2026** — layer: L2; secondary: L5; paper: `yu2026superinfer` — SuperInfer: SLO-Aware Rotary Scheduling and Memory Management for LLM Inference on Superchips; evidence depth: full text

**49 · 2026** — layer: L2; paper: `zhu2026blockserve` — BlockServe: Block-Grained Continuous Batching for High-Throughput Diffusion LLM Serving; evidence depth: **deeply read**

**50 · 2026** — layer: L2; paper: `zou2026contiguouskv` — ContiguousKV: Accelerating LLM Prefill with Granularity-Aligned KV Cache Management; evidence depth: full text

**51 · 2025** — layer: L2; secondary: L4; paper: `chen2025tokenflow` — TokenFlow: Responsive LLM Text Streaming Serving under Request Burst via Preemptive Scheduling; evidence depth: full text

**52 · 2025** — layer: L2; paper: `dong2025accelerating` — Accelerating LLM Inference Throughput via Asynchronous KV Cache Prefetching; evidence depth: full text

**53 · 2025** — layer: L2; secondary: L1; paper: `fang2025accelerating` — Accelerating LLM Inference via Dynamic KV Cache Placement in Heterogeneous Memory System; evidence depth: full text

**54 · 2025** — layer: L2; secondary: L1; paper: `feng2025adaptcache` — AdaptCache: KV Cache Native Storage Hierarchy for Low-Delay and High-Quality Language Model Serving; evidence depth: full text

**55 · 2025** — layer: L2; paper: `feng2025evicpress` — EVICPRESS: Joint KV-Cache Compression and Eviction for Efficient LLM Serving; evidence depth: full text

**56 · 2025** — layer: L2; secondary: L4; paper: `gao2025aptserve` — Apt-Serve: Adaptive Request Scheduling on Hybrid Cache for Scalable LLM Inference Serving; evidence depth: abstract

**57 · 2025** — layer: L2; paper: `gao2025collaborative` — Collaborative Speculative Inference for Efficient LLM Inference Serving; evidence depth: full text

**58 · 2025** — layer: L2; paper: `husom2025sustainable` — Sustainable LLM Inference for Edge AI: Evaluating Quantized LLMs for Energy Efficiency, Output Accuracy, and Inference Latency; evidence depth: full text

**59 · 2025** — layer: L2; secondary: L4; paper: `jaillet2025online` — Online Scheduling for LLM Inference with KV Cache Constraints; evidence depth: full text

**60 · 2025** — layer: L2; secondary: L1; paper: `kim2025scalable` — Scalable Processing-Near-Memory for 1M-Token LLM Inference: CXL-Enabled KV-Cache Management Beyond GPU Limits; evidence depth: **deeply read**

**61 · 2025** — layer: L2; secondary: L3; paper: `kolluru2025comparative` — Comparative Analysis of Large Language Model Inference Serving Systems: A Performance Study of vLLM and HuggingFace TGI; evidence depth: full text

**62 · 2025** — layer: L2; secondary: L5; paper: `li2025adaserve` — AdaServe: Accelerating Multi-SLO LLM Serving with SLO-Customized Speculative Decoding; evidence depth: full text

**63 · 2025** — layer: L2; secondary: L1; paper: `liu2025lmcache` — LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference; evidence depth: full text

**64 · 2025** — layer: L2; secondary: L5; paper: `ma2025memory` — Memory Offloading for Large Language Model Inference with Latency SLO Guarantees; evidence depth: full text

**65 · 2025** — layer: L2; paper: `meng2025understanding` — Understanding Bottlenecks for Efficiently Serving LLM Inference With KV Offloading; evidence depth: full text

**66 · 2025** — layer: L2; secondary: L5; paper: `pang2025optimizing` — Optimizing LLM Inference Throughput via Memory-aware and SLA-constrained Dynamic Batching; evidence depth: full text

**67 · 2025** — layer: L2; secondary: L5; paper: `shen2025accelgen` — AccelGen: Heterogeneous SLO-Guaranteed High-Throughput LLM Inference Serving for Diverse Applications; evidence depth: full text

**68 · 2025** — layer: L2; paper: `staniszewski2025kv` — KV Cache Transform Coding for Compact Storage in LLM Inference; evidence depth: full text

**69 · 2025** — layer: L2; paper: `tian2025keepkv` — KeepKV: Achieving Periodic Lossless KV Cache Compression for Efficient LLM Inference; evidence depth: full text

**70 · 2025** — layer: L2; paper: `wang2025accelerating` — Accelerating Mixture-of-Experts Inference by Hiding Offloading Latency with Speculative Decoding; evidence depth: full text

**71 · 2025** — layer: L2; paper: `wang2025fier` — FIER: Fine-Grained and Efficient KV Cache Retrieval for Long-context LLM Inference; evidence depth: full text

**72 · 2025** — layer: L2; secondary: L4; paper: `wang2025llm` — LLM Serving Optimization with Variable Prefill and Decode Lengths; evidence depth: full text

**73 · 2025** — layer: L2; paper: `wang2025moespeq` — MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts; evidence depth: full text

**74 · 2025** — layer: L2; paper: `xu2025moegen` — MoE-Gen: High-Throughput MoE Inference on a Single GPU with Module-Based Batching; evidence depth: full text

**75 · 2025** — layer: L2; paper: `ye2025flashinfer` — FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving; evidence depth: full text

**76 · 2025** — layer: L2; paper: `yu2025taming` — Taming Latency-Memory Trade-Off in MoE-Based LLM Serving via Fine-Grained Expert Offloading; evidence depth: full text

**77 · 2025** — layer: L2; secondary: L4; paper: `yuan2025cascadeinfer` — CascadeInfer: Length-Aware Scheduling of LLM Serving with Low Latency and Load Balancing; evidence depth: full text

**78 · 2025** — layer: L2; paper: `zeng2025mpcache` — MPCache: MPC-Friendly KV Cache Eviction for Efficient Private LLM Inference; evidence depth: full text

**79 · 2025** — layer: L2; paper: `zheng2025bucketserve` — BucketServe: Bucket-Based Dynamic Batching for Smart and Efficient LLM Inference Serving; evidence depth: full text

**80 · 2025** — layer: L2; secondary: L0; paper: `zhuge2025specoffload` — SpecOffload: Unlocking Latent GPU Capacity for LLM Inference on Resource-Constrained Devices; evidence depth: full text

**81 · 2025** — layer: L2; paper: `zuo2025windowkv` — WindowKV: Task-Adaptive Group-Wise KV Cache Window Selection for Efficient LLM Inference; evidence depth: full text

**82 · 2024** — layer: L2; paper: `agrawal2024taming` — Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve; evidence depth: **deeply read**

**83 · 2024** — layer: L2; secondary: L4; paper: `cheng2024slicelevel` — Slice-Level Scheduling for High Throughput and Load Balanced LLM Serving; evidence depth: full text

**84 · 2024** — layer: L2; paper: `guldogan2024multibin` — Multi-Bin Batching for Increasing LLM Inference Throughput; evidence depth: full text

**85 · 2024** — layer: L2; secondary: L3; paper: `he2024fastdecode` — FastDecode: High-Throughput GPU-Efficient LLM Serving using Heterogeneous Pipelines; evidence depth: **deeply read**

**86 · 2024** — layer: L2; paper: `lin2024qserve` — QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving; evidence depth: full text

**87 · 2024** — layer: L2; paper: `prabhu2024vattention` — vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention; evidence depth: full text

**88 · 2024** — layer: L2; secondary: L5; paper: `shen2024econoserve` — EconoServe: Maximizing Multi-Resource Utilization with SLO Guarantees in LLM Serving; evidence depth: full text

**89 · 2024** — layer: L2; paper: `zheng2024batchllm` — BatchLLM: Optimizing Large Batched LLM Inference with Global Prefix Sharing and Throughput-oriented Token Batching; evidence depth: full text

**90 · 2024** — layer: L2; paper: `zhu2024nanoflow` — NanoFlow: Towards Optimal Large Language Model Serving Throughput; evidence depth: full text

**91 · 2023** — layer: L2; paper: `kwon2023efficient` — Efficient Memory Management for Large Language Model Serving with PagedAttention; evidence depth: **deeply read**

**92 · 2023** — layer: L2; paper: `liu2023cachegen` — CacheGen: KV Cache Compression and Streaming for Fast Large Language Model Serving; evidence depth: full text

**93 · 2023** — layer: L2; paper: `zheng2023sglang` — SGLang: Efficient Execution of Structured Language Model Programs; evidence depth: **deeply read**

**94 · 2026** — layer: L3; secondary: L1; paper: `basit2026dualscale` — DualScale: Energy-Efficient Disaggregated LLM Serving via Phase-Aware Placement and DVFS; evidence depth: full text

**95 · 2026** — layer: L3; secondary: L4; paper: `chen2026freebalance` — FreeBalance: Pre-Routing Online Moe Load Balancing via Residual Workload Prediction; evidence depth: full text

**96 · 2026** — layer: L3; paper: `cho2026llmservingsim` — LLMServingSim 2.0: A Unified Simulator for Heterogeneous and Disaggregated LLM Serving Infrastructure; evidence depth: full text

**97 · 2026** — layer: L3; secondary: L4; paper: `cui2026opscale` — OpScale: Operator-level Provisioning and Autoscaling for LLM Serving; evidence depth: full text

**98 · 2026** — layer: L3; paper: `forys2026when` — When Does Disaggregation Pay? Simulating Prefill--Decode--Attention--FFN Specialization for Agentic LLM Inference; evidence depth: full text

**99 · 2026** — layer: L3; secondary: L5; paper: `gao2026prompttuner` — PromptTuner: SLO-Aware Elastic System for LLM Prompt Tuning; evidence depth: full text

**100 · 2026** — layer: L3; secondary: L2; paper: `he2026efficient` — Efficient Multi-round LLM Inference over Disaggregated Serving; evidence depth: full text

**101 · 2026** — layer: L3; secondary: L5; paper: `kamahori2026voxserve` — VoxServe: Streaming-Centric Serving System for Speech Language Models; evidence depth: full text

**102 · 2026** — layer: L3; paper: `kanani2026duet` — DUET: Disaggregated Hybrid Mamba-Transformer LLMs with Prefill and Decode-Specific Packages; evidence depth: **deeply read**

**103 · 2026** — layer: L3; secondary: L4,L2; paper: `kumar2026streamserve` — StreamServe: Adaptive Speculative Flows for Low-Latency Disaggregated LLM Serving; evidence depth: full text

**104 · 2026** — layer: L3; paper: `lee20263dls` — 3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving; evidence depth: abstract

**105 · 2026** — layer: L3; paper: `li2026not` — Not All Prefills Are Equal: PPD Disaggregation for Multi-turn LLM Serving; evidence depth: full text

**106 · 2026** — layer: L3; secondary: L5; paper: `li2026sloaware` — SLO-Aware Compute Resource Allocation for Prefill-Decode Disaggregated LLM Inference; evidence depth: full text

**107 · 2026** — layer: L3; secondary: L5; paper: `ma2026tropical` — Tropical: Enhancing SLO Attainment in Disaggregated LLM Serving via SLO-Aware Multiplexing; evidence depth: full text

**108 · 2026** — layer: L3; secondary: L5; paper: `nitsum2026` — Nitsum: Elastic Tensor Parallelism for LLM Serving; evidence depth: full text

**109 · 2026** — layer: L3; paper: `pdisagg2026` — Pragmatic Exploration of Prefill-Decode Disaggregation in Large Scale Inference; evidence depth: **deeply read**

**110 · 2026** — layer: L3; secondary: L2; paper: `servinginthewild2026` — LLM Serving in the Wild: An Empirical Study of Frameworks, Methods, and System Designs; evidence depth: full text

**111 · 2026** — layer: L3; secondary: L4; paper: `she2026laps` — LAPS: A Length-Aware-Prefill LLM Serving System; evidence depth: full text

**112 · 2026** — layer: L3; secondary: L0; paper: `wei2026hbm` — HBM Is Not All You Need: Efficient Disaggregated LLM Serving across Memory-heterogeneous Accelerators; evidence depth: full text

**113 · 2026** — layer: L3; secondary: L2; paper: `yin2026vllmomni` — vLLM-Omni: Fully Disaggregated Serving for Any-to-Any Multimodal Models; evidence depth: full text

**114 · 2025** — layer: L3; paper: `chen2025amoeba` — Amoeba: Runtime Tensor Parallel Transformation for LLM Inference Services; evidence depth: full text

**115 · 2025** — layer: L3; paper: `chen2025towards` — Towards High-Goodput LLM Serving with Prefill-decode Multiplexing; evidence depth: full text

**116 · 2025** — layer: L3; secondary: L4; paper: `du2025ecoserve` — EcoServe: Enabling Cost-effective LLM Serving with Proactive Intra- and Inter-Instance Orchestration; evidence depth: full text

**117 · 2025** — layer: L3; paper: `gao2025duetserve` — DuetServe: Harmonizing Prefill and Decode for LLM Serving via Adaptive GPU Multiplexing; evidence depth: full text

**118 · 2025** — layer: L3; secondary: L2; paper: `kim2025ador` — ADOR: A Design Exploration Framework for LLM Serving with Enhanced Latency and Throughput; evidence depth: full text

**119 · 2025** — layer: L3; secondary: L0; paper: `kong2025ppipe` — PPipe: Efficient Video Analytics Serving on Heterogeneous GPU Clusters via Pool-Based Pipeline Parallelism; evidence depth: full text

**120 · 2025** — layer: L3; secondary: L4; paper: `lai2025tokenscale` — TokenScale: Timely and Accurate Autoscaling for Disaggregated LLM Serving with Token Velocity; evidence depth: full text

**121 · 2025** — layer: L3; paper: `li2025optpipe` — OptPipe: Memory- and Scheduling-Optimized Pipeline Parallelism for LLM Training; evidence depth: full text

**122 · 2025** — layer: L3; paper: `li2025revisiting` — Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications; evidence depth: full text

**123 · 2025** — layer: L3; secondary: L0; paper: `liu2025cronus` — Cronus: Efficient LLM inference on Heterogeneous GPU Clusters via Partially Disaggregated Prefill; evidence depth: full text

**124 · 2025** — layer: L3; secondary: L4; paper: `liu2025trinity` — Trinity: Disaggregating Vector Search from Prefill-Decode Disaggregation in LLM Serving; evidence depth: full text

**125 · 2025** — layer: L3; secondary: L0; paper: `mo2025hetis` — Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism; evidence depth: abstract

**126 · 2025** — layer: L3; secondary: L4; paper: `patke2025hierarchical` — Hierarchical Autoscaling for Large Language Model Serving with Chiron; evidence depth: full text

**127 · 2025** — layer: L3; paper: `ruan2025dynaserve` — DynaServe: Unified and Elastic Execution for Dynamic Disaggregated LLM Serving; evidence depth: full text

**128 · 2025** — layer: L3; paper: `shi2025nexusproactive` — Nexus:Proactive Intra-GPU Disaggregation of Prefill and Decode in LLM Serving; evidence depth: full text

**129 · 2025** — layer: L3; paper: `wang2025prefilldecode` — Prefill-Decode Aggregation or Disaggregation? Unifying Both for Goodput-Optimized LLM Serving; evidence depth: full text

**130 · 2025** — layer: L3; secondary: L4; paper: `yang2025latent` — Latent Prototype Routing: Achieving Near-Perfect Load Balancing in Mixture-of-Experts; evidence depth: full text

**131 · 2025** — layer: L3; secondary: L2; paper: `yin2025specpipe` — SpecPipe: Accelerating Pipeline Parallelism-based LLM Inference with Speculative Decoding; evidence depth: full text

**132 · 2025** — layer: L3; paper: `zhang2025spad` — SPAD: Specialized Prefill and Decode Hardware for Disaggregated LLM Inference; evidence depth: full text

**133 · 2025** — layer: L3; paper: `zhang2025tdpipe` — TD-Pipe: Temporally-Disaggregated Pipeline Parallelism Architecture for High-Throughput LLM Inference; evidence depth: full text

**134 · 2024** — layer: L3; paper: `cho2024llmservingsim` — LLMServingSim: A HW/SW Co-Simulation Infrastructure for LLM Inference Serving at Scale; evidence depth: abstract

**135 · 2024** — layer: L3; secondary: L4; paper: `huang2024enova` — ENOVA: Autoscaling towards Cost-effective and Stable Serverless LLM Serving; evidence depth: full text

**136 · 2024** — layer: L3; secondary: L1; paper: `mei2024helix` — Helix: Serving Large Language Models over Heterogeneous GPUs and Network via Max-Flow; evidence depth: full text

**137 · 2024** — layer: L3; secondary: L1; paper: `oliaro2024flexllm` — FlexLLM: Token-Level Co-Serving of LLM Inference and Finetuning with SLO Guarantees; evidence depth: full text

**138 · 2024** — layer: L3; secondary: L2; paper: `qin2024mooncake` — Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving; evidence depth: full text

**139 · 2024** — layer: L3; secondary: L0,L2; paper: `zhao2024llmpq` — LLM-PQ: Serving LLM on Heterogeneous Clusters with Phase-Aware Partition and Adaptive Quantization; evidence depth: full text

**140 · 2024** — layer: L3; paper: `zhong2024distserve` — DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving; evidence depth: **deeply read**

**141 · 2026** — layer: L4; secondary: L5; paper: `adnan2026cascade` — Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving; evidence depth: full text

**142 · 2026** — layer: L4; secondary: L3; paper: `arun2026towards` — Towards Load-Aware Prefill Deflection for Disaggregated LLM Serving; evidence depth: full text

**143 · 2026** — layer: L4; secondary: L3; paper: `bu2026tackling` — Tackling the Data-Parallel Load Balancing Bottleneck in LLM Serving: Practical Online Routing at Scale; evidence depth: full text

**144 · 2026** — layer: L4; secondary: L3; paper: `choi2026eldr` — ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving; evidence depth: full text

**145 · 2026** — layer: L4; paper: `da2026routebalance` — RouteBalance: Fused Model Routing and Load Balancing for Heterogeneous LLM Serving; evidence depth: full text

**146 · 2026** — layer: L4; secondary: L0; paper: `du2026goodserve` — GoodServe: Towards High-Goodput Serving of Agentic LLM Inferences over Heterogeneous Resources; evidence depth: **deeply read**

**147 · 2026** — layer: L4; secondary: L5; paper: `du2026latencyprism` — LatencyPrism: Online Non-intrusive Latency Sculpting for SLO-Guaranteed LLM Inference; evidence depth: full text

**148 · 2026** — layer: L4; secondary: L0; paper: `kasnavieh2026routerwise` — RouterWise: Joint Resource Allocation and Routing for Latency-Aware Multi-Model LLM Serving; evidence depth: full text

**149 · 2026** — layer: L4; secondary: L0; paper: `ni2026chimera` — Chimera: Latency- and Performance-Aware Multi-agent Serving for Heterogeneous LLMs; evidence depth: full text

**150 · 2026** — layer: L4; secondary: L0; paper: `peng2026hexagent` — HexAGenT: Efficient Agentic LLM Serving via Workflow- and Heterogeneity-Aware Scheduling; evidence depth: full text

**151 · 2026** — layer: L4; secondary: L5; paper: `quartz2026` — QUARTZ: Quantile-Aware Routing and Queueing for TTFT SLOs in LLM Serving; evidence depth: abstract

**152 · 2026** — layer: L4; secondary: L2; paper: `sunesh2026requestrouter` — RequestRouter: Request-Boundary Routing for Efficient Single-GPU LLM Inference; evidence depth: full text

**153 · 2026** — layer: L4; secondary: L5; paper: `wang2026smetric` — SMetric: Rethink LLM Scheduling for Serving Agents with Balanced Session-centric Scheduling; evidence depth: full text

**154 · 2026** — layer: L4; secondary: L3; paper: `wang2026taming` — Taming Request Imbalance: SLO-Aware Scheduling for Disaggregated LLM Inference; evidence depth: full text

**155 · 2026** — layer: L4; secondary: L2; paper: `yuan2026dualmap` — DualMap: Enabling Both Cache Affinity and Load Balancing for Distributed LLM Serving; evidence depth: **deeply read**

**156 · 2025** — layer: L4; secondary: L5; paper: `chen2025slosserve` — SLOs-Serve: Optimized Serving of Multi-SLO LLMs; evidence depth: full text

**157 · 2025** — layer: L4; secondary: L5; paper: `chow2025slice` — SLICE: SLO-Driven Scheduling for LLM Inference on Edge Computing Devices; evidence depth: full text

**158 · 2025** — layer: L4; secondary: L2; paper: `da2025astrolabe` — Astrolabe: Balancing Load in LLM Serving with Randomized Prediction-Guided Scheduling; evidence depth: abstract

**159 · 2025** — layer: L4; secondary: L5; paper: `goel2025niyama` — Niyama: Breaking the Silos of LLM Inference Serving; evidence depth: full text

**160 · 2025** — layer: L4; secondary: L0; paper: `he2025freesh` — FREESH: Fair, Resource- and Energy-Efficient Scheduling for LLM Serving on Heterogeneous GPUs; evidence depth: full text

**161 · 2025** — layer: L4; secondary: L5; paper: `huang2025proserve` — ProServe: Unified Multi-Priority Request Scheduling for LLM Serving; evidence depth: full text

**162 · 2025** — layer: L4; secondary: L5; paper: `huang2025sloaware` — SLO-Aware Scheduling for Large Language Model Inferences; evidence depth: full text

**163 · 2025** — layer: L4; secondary: L2; paper: `li2025semiclairvoyant` — Semi-Clairvoyant Scheduling of Speculative Decoding Requests to Minimize LLM Inference Latency; evidence depth: full text

**164 · 2025** — layer: L4; secondary: L5; paper: `tang2025scorpio` — Scorpio: Serving Right Requests at the Right Time for Heterogeneous SLOs in LLM Inference; evidence depth: full text

**165 · 2025** — layer: L4; secondary: L0; paper: `xia2025skywalker` — SkyWalker: A Locality-Aware Cross-Region Load Balancer for LLM Inference; evidence depth: full text

**166 · 2025** — layer: L4; secondary: L1,L3; paper: `yu2025voltanallm` — VoltanaLLM: Energy-Efficient and SLO-Aware Disaggregated LLM Serving via Adaptive Frequency Control and State-Space Routing; evidence depth: full text

**167 · 2025** — layer: L4; secondary: L5; paper: `zhang2025jitserve` — JITServe: SLO-aware LLM Serving with Imprecise Request Information; evidence depth: full text

**168 · 2024** — layer: L4; secondary: L3; paper: `he2024uellm` — UELLM: A Unified and Efficient Approach for LLM Inference Serving; evidence depth: full text

**169 · 2024** — layer: L4; secondary: L5; paper: `patke2024queue` — Queue management for slo-oriented large language model serving; evidence depth: full text

**170 · 2026** — layer: L5; secondary: L4; paper: `lian2026humanless` — Human-Less LLM Serving: Quantifying the Human Tax on Throughput; evidence depth: full text

**171 · 2026** — layer: L5; secondary: L3; paper: `lysensten2026sloguard` — SLO-Guard: Crash-Aware, Budget-Consistent Autotuning for SLO-Constrained LLM Serving; evidence depth: **deeply read**

**172 · 2025** — layer: L5; paper: `ranganathan2025incidents` — Enhancing Reliability in AI Inference Services: An Empirical Study on Real Production Incidents; evidence depth: **deeply read**