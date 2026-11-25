---
title: "Designing LLM Inference Systems, Part 2: Six Layers to Investigate"
source: "https://medium.com/@wszjzhang/designing-llm-inference-systems-part-2-six-layers-to-investigate-e8992394f24f"
author:
  - "[[intelligentLearn]]"
published: 2026-11-14
created: 2026-11-25
description: "More"
tags:
  - "clippings"
---
Where the real trade-offs live, worked through with numbers you can check.

*Part 2 of 4 of the trade-offs article, from “Designing LLM inference systems”, the second half of a series on LLM inference serving.* [*Part 1*](https://medium.com/@wszjzhang/from-symptoms-to-fixes-the-trade-offs-inside-an-llm-inference-system-part-1-start-with-the-9aa825ca7969) *set up the three ledgers — operator, memory budget, request timeline — and the long-document running case; this part walks the six layers where a fix can land, in investigation order. Parts 3 and 4 follow on November 17 and 24; Appendix D is at the end of Part 4.*

When requests slow down, the usual first move, before naming which limit binds, is to turn the batch up or to switch on an optimization the engine already has. A larger batch helps the weight-reading linear layers; it does not help attention over each request’s own history, and it is still limited by the KV those requests keep in memory. The six sections below say which layer the limit sits on, and what a change at that layer costs.

**\[Upload figure 1: export/wechat-png/k6-investigation-order.png\]**

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*P-pCh_Hvo3yypyPJbl336A.png)

*Investigation order for Part II, not the framework’s L0-to-L5 order. Part IV walks L0 → L5 for reference.*

The six sections that follow are the spine of the article. Their teaching order is engine internals → replica composition → routing and admission → substrate → capacity → contract, rather than the framework’s L0-to-L5 order.

This is an investigation order, not a relay. Start from the symptom and the three ledgers, inspect the layer that can explain the binding constraint, and skip layers that the measurements rule out. A queueing problem may point straight to routing or admission; a burst that ends before a replica can start may point straight to the substrate. The six-layer map in Part 4 walks the framework in L0-to-L5 order for reference.

## 6\. Engine internals (L2): how time and memory on one GPU get divided

## What raising the batch size helps, and when

Raising the batch size helps the weight-reading linear layers, and only while two conditions hold. Those layers reuse one weight read across the requests in the batch, so their arithmetic intensity rises with B — about `B` FLOP/byte in BF16 when weight traffic dominates. On section 4's weight-only estimate they reach this hardware's 295 FLOP/byte ridge only around B ≈ 295; below that, a larger batch moves them up the roofline. The other condition is memory. Each added request keeps its own KV, so the larger batch helps only while that state still fits.

The long-document case fails both, and section 5 already computed where. The memory wall: long documents squeeze the memory-only concurrency ceiling from about 690 down to about 14, well short of the batch that reaches the ridge. The time wall: the same increase leaves attention that reads historical KV at about 8 FLOP/byte, unmoved by batch size.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*LJDTqC-fV55IEEFpWl3rWQ.png)

*Same numbers as sections 4–5; not measurements. Roofline detail stays in Part I (k4).*

This operator dichotomy is not this article’s invention. `he2024fastdecode` splits the transformer block into **S-Part** (the fully connected layers, which hold the weights, are shared across sequences and batch well) and **R-Part** (attention over the history, which holds the KV cache and contains no model parameters at all). The split matches the operator split in section 4 — the same conclusion, reached independently out of engineering necessity.

As for KV growing linearly in both context and batch: `kim2025scalable` explicitly names GPU memory **capacity** as the bottleneck it sets out to relieve. But **within that paper the linear growth is a motivating assertion cited from other work, not a measurement of its own**, so it cannot be cited here as measured. What this article rests that linear relationship on is the arithmetic in section 5. That follows directly from the definition of KV and never needed a paper to back it up.

## What else we can move on a single GPU

**Continuous batching.** Requests no longer wait for a full batch to depart; they join and leave at iteration boundaries. It changes both waiting and execution efficiency: requests wait less for a batch boundary, while filling vacated slots keeps useful work in later iterations when sequence lengths differ. It does not reduce the per-token operator work. (This is the one mechanism in the article whose source sits outside the corpus: it comes from Orca, see Appendix D.)

**Paged KV.** `kwon2023efficient` (PagedAttention / vLLM) allocates KV in fixed-size blocks on demand, like operating-system virtual memory, instead of reserving for the maximum length, so each request wastes at most one partially filled block. That paper profiled how large the fragmentation it targets actually is in existing systems — **only 20.4% to 38.2% of KV memory was actually holding token state**, the rest being reservation and fragmentation. But be precise about its range: it bounds allocation waste rather than eliminating fragmentation, and can push achievable concurrency towards the independent-sequence ceiling calculated in section 5. It **cannot move that ceiling by itself**, which is pinned by the linear growth of KV; prefix sharing is different because it changes how much state those otherwise independent sequences need and therefore changes the baseline.

**Chunked prefill (colocated).** `agrawal2024taming` (Sarathi-Serve) cuts a long prefill into chunks and runs them in the same batch as decode, so a long prefill no longer monopolizes a whole iteration at once. For question 2 of the case this is the first answer: without changing the deployment shape, it holds down the blocking that "one 32k prefill occupying about 3.8 s of GPU busy time" inflicts on decode.

**Move state out of HBM.** Two different routes are both in the corpus. `he2024fastdecode` moves R-Part together with the KV wholesale onto off-node CPU machines, sending only Q/K/V/O activations over the network. `kim2025scalable` adds capacity with CXL-PNM and puts KV outside the GPU (**all of that paper's performance results for the system it proposes come from a cycle-level simulator, not measured silicon**; one failure case it states about itself is that when the number of PNM devices is comparable to the number of GPUs, throughput can fall below the baseline).

What the two jointly refute is the universal claim that “KV has to live in GPU memory”, and both back that up with an existence proof, which makes it solid. As for what standard should replace it, **my formulation is “it has to meet the latency budget for state access”, but that is my generalisation, not a conclusion of these two papers**: neither of them gives a latency threshold for deciding the placement tier. So the accurate conclusion stops at “the fast path is not the same thing as GPU HBM”.

## What that moving costs

**Continuous batching** — cost: scheduling overhead; long and short requests in one batch affect each other; when it breaks: when request lengths are extremely uneven, a long request still raises the latency of the short ones batched with it

**Paged KV** — cost: indirection overhead; block size has to be tuned; when it breaks: relieves fragmentation, **does not relieve KV growing linearly with context**; `kwon2023efficient` measures its own attention kernel as **20 to 26%** slower than FasterTransformer's

**Chunked prefill** — cost: chunking has its own overhead; chunk size is a new knob; when it breaks: once total prefill volume exceeds what one replica can absorb, colocation has no room left to manoeuvre

**State out of HBM** — cost: interconnect bandwidth becomes the new bottleneck; when it breaks: `he2024fastdecode` needs **extra whole CPU machines**, and its comparison baseline is not the same hardware; at sequences as short as 128 tokens, the 13B model's **strong-scaling efficiency from 1 to 8 sockets is only 37.6%**, and 8 sockets are in fact slower than 4

The paged-KV row is worth a second look, because it demonstrates cost displacement very cleanly: what is saved is memory, what is paid is kernel time. `kwon2023efficient` draws the boundary itself — it says plainly that for workloads with static shapes or compute-bound ones, all that indirection "may rather degrade the performance due to the extra overhead of memory indirection and non-contiguous block memory". In other words, **it is a design aimed at a memory-access bottleneck, not a universally better design.**

The last row is the article’s most glaring example of cost displacement. Move the KV memory-access pressure off the GPU and the pressure reappears intact on the interconnect and the CPU side. Shorten the sequences and S-Part becomes the bottleneck again, flipping the sign on the whole design’s benefit. **This example is only used to refute “it has to be on the GPU”. It does not support “putting KV on CPU works in general”.**

## Which knob to turn first

- Which wall do we hit first, memory or time? The former is the memory budget, the latter the operator ledger.
- Prefill is blocking decode but the replica still has headroom → turn on chunked prefill first, no need to touch the deployment shape.
- State does not fit and the interconnect is plentiful → only then consider moving KV out of HBM, and measure interconnect bandwidth first, then the sequence-length distribution.

**When this is enough.** Stay at L2 when the replica fits the target concurrency and continuous batching, paging or chunking brings queue time and token gaps inside budget without changing the deployment shape. Moving state out of HBM is enough only when measured interconnect and CPU-side latency still satisfy that budget.

**When to investigate another layer.** If phase interference or a shared parallel configuration is binding, cost out L3. If queueing dominates despite usable replica headroom, inspect L4 directly; if replicas cannot start within the burst or GPUs are unavailable, skip to L1 or L0.

## 7\. Replica composition (L3): put the two kinds of work in separate places

## Why colocation couples two phases

This one thing is left: prefill and decode have different typical resource demands and latency targets. Colocation produces interference, and it also ties the two phases’ resource allocation and parallelism strategy together.

This is the problem `zhong2024distserve` (DistServe) states about itself. It says colocation "couples their resource allocation, and prevents implementing different parallelism strategies more suited to meeting the specific latency requirements of each phase"; reviewing existing systems, it adds that they "all employ a colocation approach for prefill and decoding processing, thus leading to severe interference". So a system can only favour TTFT or TPOT, one or the other, or over-provision GPUs to satisfy both.

Note that what actually makes disaggregation an option is **interference and configuration coupling**, not a “compute-bound vs memory-bound” framing that labels a whole phase. By the conclusion of section 4, what we can label is an operator, not a phase.

## Pulling prefill and decode apart

**Prefill/decode disaggregation.** This is what `zhong2024distserve` does: the two kinds of instance each hold their own copy of the weights and each pick their own parallel degree. Prefill instances produce the first token and the KV, and decode instances take over. The immediate benefit is that each phase can pick its configuration against its own SLO, without the two constraining each other. (Splitwise, from the same period, is another system that arrived at this independently; it sits outside the corpus, see Appendix D.)

**Let traffic shape decide whether to disaggregate.** `pdisagg2026` systematically swept this design space and concluded that disaggregation pays most on prefill-heavy traffic (input far longer than output) and on larger models, while on decode-heavy traffic with loose latency targets colocation is actually competitive.

**That conclusion has to carry a label: it comes almost entirely from the paper’s own simulator.** The paper says the simulator “has been exhaustively validated against silicon performance” measurements, but **gives no error data whatsoever**, and its real-hardware measurements only go up to 8B. So it is a **simulator result**, not a measured one.

And there is one further limitation that lands exactly where we want to use it: **the paper’s traffic model is static**. Input and output lengths take fixed values (by the paper’s own account, power-of-two approximations of the P50), with **no dynamic arrival process**, and yet judging “traffic shape” is precisely what I am using it for. So what it gives is a directional hint, not a criterion we can take over as-is.

Applied to the case: long documents are textbook prefill-heavy traffic (32k in, 512 out), landing exactly on the side where disaggregation pays most. That is the second answer to question 2 of the case.

## What disaggregation must account for

Disaggregation moves the cost to three new places: **KV has to be transferred across instances** (the handover after the first token), the ratio between the two instance types has to match the arrival rate (get the ratio wrong and one side idles), and every selected prefill or decode instance needs its own model weights. The running case already has two colocated TP=4 replicas, so its model-weight memory footprint rises only if the chosen P:D composition carries more than those two model copies. Disaggregation does not make that increase automatic.

The failure condition is decode-heavy traffic. There, prefill interference was not significant to begin with, so no amount of tuning on the prefill side improves end to end.

DistServe’s self-stated limitations are heavier still, and worth copying across. It **implements neither preemption nor fault tolerance**. The prefill→decode dependency manufactures fault propagation: in the paper’s own words, one failed decode instance “could potentially cripple the entire service and cluster”. In resource-constrained settings with only a few GPUs, or even one, its design space is significantly compressed. And in offline, throughput-oriented settings, **the paper itself considers chunked prefill possibly more suitable than disaggregation**. Remember that last one in particular: it shows that “disaggregation vs colocation” is not a matter of new versus old, but of which side of the objective function we are on.

There is also a boundary that is easy to miss: state does not look the same in every architecture. In the Mamba-Transformer hybrid of `kanani2026duet`, the paper explicitly states that the SSM layers' state is fixed-size (no sequence-length term), and it is the attention layers' KV that is the capacity bottleneck. In other words the KV formula in section 5 has a range of validity: it is bound to standard autoregressive MHA/GQA and cannot be applied directly to every architecture.

**But do not over-read that boundary either.** A non-autoregressive architecture does not mean “no state to manage”. `zhu2026blockserve` is about the batching heterogeneity that comes from requests converging in different numbers of steps in diffusion-LLM serving. Change the architecture and the shape of the state changes, but the scheduling trouble does not disappear, it just takes a different form.

## Which traffic is worth splitting

- Measure the input/output length ratio first. Prefill-heavy → disaggregation is worth costing out; decode-heavy → leave it alone for now.
- Then measure how stable the arrival rate is. The ratio is only easy to hold when the arrival rate is stable.
- After disaggregation, KV transfer and ratio imbalance are new failure surfaces and need observables of their own.

**When this is enough.** L3 is enough when independent prefill and decode configurations meet TTFT and token gap targets after measured KV-transfer cost, and the observed arrival mix supports a stable P:D ratio.

**When to investigate another layer.** If reusable prefixes or uneven queues make replicas non-equivalent, inspect L4. If the measured problem is instead replica startup latency or unavailable capacity, skip routing and inspect L1 or L0.

## 8\. Routing and admission (L4): state makes “who to send it to” hard

## Why replicas stop being interchangeable

Because they hold different reusable state. Question 3 of the case comes from this.

**What has to be stated precisely: what makes replicas non-equivalent is “reusable state”, not disaggregation itself.** The input card already assumes reusable prefixes between long-document requests, so even colocated, with no disaggregation at all, replicas are already non-equivalent. Not one of the three mechanisms in this section is specific to disaggregation. What disaggregation genuinely adds is two things: KV has to be transferred across instances, and there is one more routing hop.

That is not a licence to jump to “routing must chase the cache”. The precise version: replicas hold reusable state, so routing has to weigh the benefit of reusing state against the cost of queueing, migration or recomputation.

## Choosing between reuse and balance

**Cache-affinity routing.** Send requests that share a prefix to the same instance, maximizing KV reuse. `zheng2023sglang` (SGLang / RadixAttention) is the most complete system on this path: rather than discarding the KV when a request finishes, it keeps it in a radix tree and reuses it by longest common prefix, and it orders the queue by longest-shared-prefix-first. The paper measures that ordering reaching **96% of the optimal hit rate**.

**But be precise about the scope of that evidence.** SGLang’s scheduling happens **inside one engine’s waiting queue**, not across replicas; and the production hit rate it reports (**74.1%** over a month on Chatbot Arena) was explicitly obtained with only one worker serving each model. So what it establishes is that ordering by prefix really does get the hit rate close to optimal, **while “route requests sharing a prefix to the same replica” is my extrapolation of it to the multi-replica case — that step is my own inference, not a conclusion of the paper.** The paper also concedes that this greedy ordering can starve requests, and lists fair scheduling as future work.

**Trade affinity off against balance.** This is the head-on answer to question 4 of the case. `yuan2026dualmap` is blunt about it: affinity scheduling "often conflicts with load-balancing scheduling", and "improvements in one often come at the expense of the other" (in the original, that second phrase is aimed at existing unified schedulers, not at the trade-off itself, and the quote should carry that scope with it). What matters is that this is not just an assertion in the introduction: the paper measured this trade-off on the same testbed.

It also describes a very instructive failure shape: **oscillating back and forth between the two objectives, which actually raises cache misses.** But be precise about the provenance. **This is what the paper gives when analysing the Min TTFT baseline that it rejects, argued through a request-by-request walkthrough, not a general observation about approaches like “joint affinity/balance scheduling”**, and DualMap’s own rules are designed precisely to avoid it. So it is a mechanism to watch out for, not a regularity that has been generally established.

Worth noting that DualMap does not fully get both either: the paper concedes that load cannot always be balanced, and on the Conversation workload the cache hit rate only reaches **62.5%** of the upper bound.

**Set the objective end to end, not per-layer optimal.** The shape of `du2026goodserve` is clean: a single global end-to-end objective, with the whole request path (queueing + prefill discounted for cache hits + decode) modelled in one place at the proxy router, **with no per-component sub-budgets and no component maximizing a local objective of its own**, and with the instance-level engine explicitly excluded from that objective.

But “a single global objective” is a statement about how the objective is written, not about how the problem is solved. The paper states that the exact problem is NP-hard, and what it actually uses is a greedy feasibility test run on each arrival against that request’s own deadline, **with no joint re-optimisation across pending requests**. This does not weaken the conclusion above, but the word “global” applies to the objective function only.

Which is exactly the point: “a system can optimize goodput” and “every scheduler maximizes its own local goodput” are two different things.

## When affinity turns negative

**Cache-affinity routing** — cost: load can become unbalanced; queues lengthen on hot instances; when it breaks: when **the execution saved by a hit < the extra queueing and transfer costs**, affinity is a net loss; `zheng2023sglang` concedes its greedy prefix ordering can starve requests

**Joint affinity/balance scheduling** — cost: needs estimates of prefix length and instance load; when it breaks: watch out for oscillating between the two objectives and actually raising the miss rate — that shape comes from DualMap’s analysis of the baseline it rejects, **not a regularity that has been generally established**

**End-to-end objective** — cost: the whole path has to be modelled in one place; when it breaks: whether components excluded from the objective (the instance-level engine, for one) respect the budget is **guaranteed by no one**

The answer to question 4 of the case is therefore a comparison, not a threshold. What we compare is **the execution saved by a hit** against the extra queueing and transfer cost, not the hit rate on its own. That comparison depends on your specific arrival rate and prefix-reuse distribution, so it **belongs to the branch that needs measurement to decide.**

## Which layer should hold the objective

- High prefix reuse, and even load → affinity is almost free money.
- High prefix reuse, but spiky load → joint scheduling is mandatory, and be ready for the oscillation problem.
- Which layer is the objective function written at? Write it end to end, and do not let every scheduler go its own way.

**When this is enough.** L4 is enough when routing or admission keeps end-to-end queueing inside the SLO and the measured execution saved by cache hits exceeds the extra queueing and transfer cost.

**When to investigate another layer.** If every eligible replica is saturated and new replicas arrive too late, inspect L1; if no acceptable capacity is available, inspect L0. If overload is unavoidable and the service has no explicit rejection, degradation or timeout policy, inspect L5 directly.

## 9\. Substrate (L1): how GPUs get carved up

## Where cold-start time actually goes

Routing can use only replicas that are ready, so a burst that requires **scaling out** exposes the time needed to materialize another replica.

**Shorten cold start.** The production cold start `lou2025hydraserve` measured is **\>40 s**, of which **host-to-GPU weight transfer accounts for only about 2 s**. The main bottleneck by the paper's own account is pulling the model from remote storage. The network on a serverless GPU instance is deliberately narrow to save cost (16 Gbps per server) and it also contends for bandwidth with colocated containers. Container creation has appreciable overhead too, with an 8.31 GB image.

(A note on accounting: **the per-stage seconds are in a figure; the prose gives only the >40 s total and the roughly 2 s for that one step**. So “pulling the model is the main bottleneck” is quotable, **but the ranking among the stages is not**, and I do not rank them here.)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*91OKvnLEUvvVPsOQACcWPw.png)

*Per-stage seconds are in the paper’s figure; this drawing does not rank unnamed stages.*

The conclusion is already counterintuitive enough: **the bottleneck is not the GPU and not PCIe, it is getting the weights onto the machine.**

The key implication: this cost is per replica, not amortised per request. (**The paper does not state this explicitly; this step is my own inference** — pulling weights is part of starting an instance, independent of how many requests that instance goes on to serve.) So the shorter the burst, the less adding replicas pays.

## What warm pools and sharing cost

Prewarming or keeping instances resident trades cold start away, at the cost of holding GPUs idle. Multi-tenant device sharing (MIG, time slicing) raises utilization, at the cost of interference and isolation.

## When scaling out cannot arrive in time

Look at the ratio of two quantities: **burst duration** ÷ **cold-start time**. Below 1, scaling out cannot arrive in time, and what should move is admission control or degradation, not the replica count.

**When this is enough.** L1 is enough when warm capacity or faster materialization starts replicas within the measured burst duration, and any device sharing still meets interference and isolation requirements.

**When to investigate another layer.** If GPUs cannot be obtained at an acceptable price or availability, inspect L0. If capacity exists but queues dominate before scaling can react, inspect L4 admission directly; if overload behaviour is undefined, inspect L5.

## 10\. Capacity (L0): where the GPUs come from and at what price

## When even the number of GPUs is a variable

One layer further down, even “how many GPUs are available” stops being a given. **The corpus has only 5 papers at this layer**, which is an empty cell in this search, not a gap in the field.

## Trading interruptible GPUs for a lower price

**Trade cost for preemptible/spot capacity.** This is exactly what `miao2023spotserve` handles: instances can be preempted, in-flight request state is therefore at risk of being lost, and recovery relies on migration or recomputation.

**Two statements have to be kept apart here, because they come from different sources:**

1. **Preemption endangers in-flight state, and recovery requires migration or recomputation** — from `miao2023spotserve`.
2. **A preempted long-context request has more state to rebuild** — **derived from KV growing linearly with context, not a conclusion of that paper.** It never writes recovery cost as a function of in-flight request length, and runs no sequence-length sweep.

So the step to “therefore spot instances pay less well under long-document workloads” **can only stop at pending measurement; this article does not assert it**.

## When the savings stop covering the rebuild

Cheap capacity is not guaranteed to be available, and the cost moves from money to availability and state rebuilding. The failure condition is the state a single request carries growing large enough that the cost of rebuilding it exceeds the cost saved. **That crossover point has to be measured**: what an in-flight request is worth varies with context length, and this article does not assert by how much.

**When this is enough.** L0 is enough when the measured interruption and state-rebuild cost remains below the savings from preemptible capacity and the resulting availability still meets the service objective.

**When to investigate another layer.** If queueing, not supply price, dominates, inspect L4 admission; if GPUs exist but model startup misses the burst, inspect L1. If demand still cannot be served, inspect L5 to define who is rejected, degraded or allowed to time out.

## 11\. Contract and failure semantics (L5): what happens when the promise is not met

## Why the evidence is thinnest at this layer

The corpus has only 3 papers here, and **one of the three does not live up to its billing**. `lysensten2026sloguard` was assigned here, but read end to end it is an **offline autotuner**: it tunes the knobs of a single-replica engine and has no runtime behaviour for "what happens when the SLO is missed" at all, and infeasible configurations are simply scored out during the tuning phase. Despite "crash-aware" as its selling point, there were zero crashes across 150 trials.

So the thinness of this layer is twofold: few papers, and among the few one does not live up to its billing.

Thin here means few papers whose main subject is the contract itself. Targets are not rare: in this corpus, 12 L4 papers also touch L5 (Appendix B), and in the coded snapshot behind the six-layer map, latency targets and goodput are among the most common mechanisms. What is thin is work on what happens when a target is missed.

## Writing down what happens when the promise is missed

**Define the failure behaviour explicitly.** `ranganathan2025incidents` is an empirical study of production incidents, and the picture is clear. Requests keep getting routed to engines that cannot serve them at all, and it surfaces to customers as HTTP errors, with **500s accounting for 74% of incidents**, which the paper itself attributes to a monitoring gap. The most common incident response is the category the paper labels "No action/monitor only", at **48%**.

What has to be stated precisely: the system was not without automatic mechanisms. The load balancer already came with health probes, capacity-aware routing, request batching and token caps, and the paper’s recommendation is to **expand** the coverage of those existing capabilities. What was genuinely **retrofitted afterwards** were admission and degradation policies: per-customer rate limiting, caps on pending tokens, per-endpoint isolation. In other words, what was missing was not automation but **an established policy for who gets sacrificed when capacity is short**.

The conclusion, then: when capacity is not enough to satisfy every request at once, the system will sacrifice something — queueing, rejection, degradation or timeout. **That choice is either defined explicitly or decided implicitly by implementation details.** It is the fifth part of a promise, its failure behaviour, which the promises article writes down for each workload class.

This layer also lands a direct counter-punch on the case: **long requests run into timeouts on their own.** The paper records long-running requests tripping a front-end HTTP **408** idle timeout **while the backend did in fact eventually return 200**; the fix is “connection liveness” — streaming responses plus request batching and a cap on pending tokens. (The paper gives a figure of one customer’s 408 rate falling from 2.72% to 0.47%, but **labels it explicitly as illustrative and outside the study window**.)

## What it costs not to define this

Defining failure behaviour explicitly has a cost too: we have to choose who gets sacrificed, **and that is a product decision, not an engineering one**. Not defining it lets timeouts, retries and HTTP status codes decide for us, and we only find out in the incident review. One question is enough: what do we intend to sacrifice when capacity runs short? If we cannot answer it, it has already been decided implicitly.

**When this is enough.** L5 is enough when overload and failure cases have explicit, tested outcomes — rate limits, rejection, degradation, timeout and connection-liveness behaviour — and those outcomes match the product promise.

**When to investigate another layer.** L5 defines failure; it does not repair the constraint. If the policy fires too often, return to the symptom and inspect the layer indicated by measurements: L4 for queueing and admission, L1 for startup delay, L0 for supply, L2 for per-replica execution or memory, or L3 for phase interference.