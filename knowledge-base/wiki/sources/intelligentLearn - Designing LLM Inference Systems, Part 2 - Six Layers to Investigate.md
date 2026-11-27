---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-14-intelligentlearn-inference-systems-part-2
source_title: "Designing LLM Inference Systems, Part 2: Six Layers to Investigate"
source_author: intelligentLearn
source_url: https://medium.com/@wszjzhang/designing-llm-inference-systems-part-2-six-layers-to-investigate-e8992394f24f
tags:
  - source/summary
  - inference
  - serving
  - disaggregation
  - routing
source_ids:
  - src-2026-11-14-intelligentlearn-inference-systems-part-2
status: active
---

# Designing LLM Inference Systems, Part 2: Six Layers to Investigate

## Summary

The second part of [[intelligentLearn]]'s series walks six layers where a serving fix can land, in
investigation order rather than stack order. The order is engine internals (L2), replica composition
(L3), routing and admission (L4), substrate (L1), capacity (L0), and contract and failure semantics
(L5). Each layer is argued from a coded paper corpus (Part 4 puts it at 172 papers). Each layer gets a cost
table, decision rules, and explicit "when this is enough" and "when to investigate another layer"
tests. The part is unusually careful about provenance. It separates what each paper measured from
what it only cited, what came from a simulator, and what the author inferred. Its recurring lesson is
cost displacement: paging trades memory for kernel time, offload moves pressure onto the
interconnect, disaggregation adds KV transfer, and cache affinity adds queueing.

## Key claims

### An investigation order, not a relay

- Start from the symptom and the three ledgers. Inspect the layer that can explain the binding
  constraint, and skip layers the measurements rule out. A queueing problem may point straight to L4.
  A burst that ends before a replica can start points to L1.

### L2 — engine internals

- Raising the batch size helps only weight-reading linear layers, and only while their KV still fits.
  The long-document case fails on memory (ceiling about **690 → 14**) and on time (historical-KV
  attention stays near **8 FLOP/byte**). FastDecode's split into S-Part (shared weights) and R-Part
  (per-sequence attention over KV) independently reaches the same operator split.
- **Continuous batching** lets requests join and leave at iteration boundaries. It changes waiting and
  slot use, not per-token work. It is the article's one mechanism sourced outside the corpus (Orca).
- **Paged KV** (PagedAttention/vLLM) found that existing systems used **only 20.4% to 38.2%** of KV
  memory for token state. Paging bounds allocation waste but "cannot move that ceiling by itself";
  prefix sharing changes the baseline instead. Its attention kernel is **20 to 26%** slower than
  FasterTransformer's, and the paper says static or compute-bound workloads "may rather degrade".
- **Chunked prefill** (Sarathi-Serve) interleaves a long prefill with decode. It is the first answer
  to the chunking-versus-disaggregation question and needs no change of deployment shape.
- **State out of HBM** has existence proofs. FastDecode moves R-Part and KV to off-node CPUs, but it
  needs extra whole CPU machines and a different-hardware baseline. At 128-token sequences its 13B
  strong-scaling efficiency from 1 to 8 sockets is **37.6%**, with 8 sockets slower than 4. CXL-PNM
  (kim2025scalable) reports only cycle-level simulator results, and can fall below baseline when PNM
  devices are comparable in number to GPUs. "It has to meet the latency budget for state access" is
  the author's own generalisation, not either paper's conclusion.

### L3 — replica composition

- DistServe says colocation "couples their resource allocation" and causes "severe interference". The
  case for splitting rests on **interference and configuration coupling**, not on labelling a whole
  phase compute- or memory-bound. Only operators can be labelled.
- DistServe has neither preemption nor fault tolerance: one failed decode instance "could potentially
  cripple the entire service and cluster". In offline, throughput-oriented settings the paper itself
  considers chunked prefill possibly more suitable.
- pdisagg2026 finds disaggregation pays most on prefill-heavy traffic and larger models, while
  colocation is "actually competitive" on decode-heavy, loose-latency traffic. The result is almost
  entirely simulated with no error data, real hardware goes only to 8B, and traffic is static, with
  no arrival process. The author treats it as "a directional hint, not a criterion".
- Disaggregation moves cost to KV transfer, the P:D ratio, and model copies. Architecture limits the
  KV formula: in the DUET Mamba-Transformer hybrid the SSM state is fixed-size and attention KV is
  the bottleneck. Diffusion-LLM serving (BlockServe) still faces batching heterogeneity.

### L4 — routing and admission

- Replicas stop being interchangeable because they hold **reusable state**, not because of
  disaggregation itself. Routing has to weigh reuse against queueing, migration, or recomputation.
- SGLang's longest-shared-prefix ordering reaches **96%** of the optimal hit rate, and it reports
  **74.1%** over a month on Chatbot Arena. Both results come from ordering inside one engine's queue,
  with one worker per model. Extending this to multi-replica routing is the author's extrapolation.
  The paper concedes the ordering can starve requests.
- DualMap says affinity "often conflicts with load-balancing scheduling" and measured the trade-off.
  Its Conversation hit rate reaches only **62.5%** of the upper bound. Its oscillation failure comes
  from a rejected Min TTFT baseline, not a general regularity.
- GoodServe writes one end-to-end objective at the proxy router. The exact problem is NP-hard, it
  solves it with a greedy per-arrival feasibility test, and the engine is excluded from the
  objective. "Global" describes the objective, not the solution.
- The cache question becomes a comparison: compare execution saved by a hit against the added
  queueing and transfer. Hit rate alone does not settle it.

### L1, L0, and L5

- **L1 (substrate):** HydraServe measures cold start at **>40 s**, of which host-to-GPU transfer is
  only about **2 s**. Pulling weights from remote storage over a **16 Gbps** network is the main
  bottleneck, and the container image is **8.31 GB**. The stage ranking is not quotable, and the
  claim that this cost is per replica is the author's inference. Rule: if burst duration ÷ cold-start
  time is below 1, change admission or degradation, not the replica count.
- **L0 (capacity):** only **5** corpus papers. SpotServe shows preemption endangers in-flight state.
  The claim that long-context requests are costlier to rebuild is the author's derivation, so the
  question stays "pending measurement".
- **L5 (contract):** only **3** papers. SLO-Guard turns out to be an offline autotuner with zero
  crashes across **150** trials. A production-incident study (ranganathan2025incidents) finds HTTP
  500s in **74%** of incidents and "No action/monitor only" as the most common response, at **48%**.
  Long requests tripped a front-end **408** idle timeout although the backend eventually returned 200.
  A 2.72%→0.47% fix figure is labelled illustrative and outside the study window. Who gets sacrificed
  under overload is "a product decision, not an engineering one". Leaving it undefined lets timeouts
  and status codes decide.

## Why it matters

This is the vault's most explicit layer-by-layer decision procedure for serving, with stopping
rules at each layer. It qualifies [[Prefill-Decode Disaggregation]] with DistServe's own limitations
and with pdisagg2026's colocation result. It turns prefix-cache affinity in [[Semantic Caching]] into
a saved-execution-versus-queueing comparison. It connects cold start, spot capacity, and missing
failure policy to [[GPU Fleet Reliability]]. It sharpens [[LLM Inference]] and
[[Inference Efficiency Frontier]] by tying each mechanism to the cost it moves. It also extends
[[Arithmetic Intensity and the Roofline Model]] to the batching decision.

## Tensions / open questions

- The evidence is a single author's reading of papers, with no new measurements. The author marks
  several steps as their own extrapolation or derivation: multi-replica cache routing, per-replica
  cold-start cost, the long-context rebuild cost, and the state-access latency budget.
- Several cited results are simulator-only or measured on different hardware: pdisagg2026,
  kim2025scalable, and FastDecode's baseline.
- Cross-references conflict. The part says Orca and Splitwise are "see Appendix D", but in Part 4
  they appear in Appendix C (anchor papers), and Appendix D lists mechanisms not developed.
- The schedule is inconsistent: this part says Parts 3 and 4 follow on November 17 and 24, but Part 3
  was published on November 19.
- A figure placeholder ("Upload figure 1 … k6-investigation-order.png") was left in the text.
- Corpus thinness at L0 and L5 is partly the author's search budget (see Part 4), not evidence about
  the field.
- The incident paper `ranganathan2025incidents` is cited only by key. No connection to the vault's
  [[Rahul Ranganathan - Inference Gateway on GKE]] author is established.

## Affected pages

- [[LLM Inference]]
- [[Prefill-Decode Disaggregation]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Inference Efficiency Frontier]]
- [[Semantic Caching]]
- [[GPU Fleet Reliability]]
- [[intelligentLearn]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[LLM Application Resilience]]

## Raw capture

- [[knowledge-base/raw/sources/Designing LLM Inference Systems, Part 2 Six Layers to Investigate]]

## Citations

- Canonical URL: https://medium.com/@wszjzhang/designing-llm-inference-systems-part-2-six-layers-to-investigate-e8992394f24f
- Byline: intelligentLearn (Medium handle @wszjzhang; no personal name in the capture).
- Published: 2026-11-14. Captured: 2026-11-25. Publisher: Medium.
- Papers are cited by BibTeX-style keys (for example `zhong2024distserve`, `kwon2023efficient`); the
  full list is in Part 4's Appendix E.

## Related pages

- [[intelligentLearn - From Symptoms to Fixes - Part 1 - Start with the Machine]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 3 - How to Evaluate a Change]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 4 - Putting It to Work]]
- [[intelligentLearn]]
- [[Prefill-Decode Disaggregation]]
- [[KV Cache]]
- [[Inference Serving Engines]]
- [[Semantic Caching]]
- [[GPU Fleet Reliability]]
- [[LLM Application Resilience]]
- [[LLM Inference]]
- [[Inference Efficiency Frontier]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Serving Benchmarks and Goodput]]
- [[Rahul Ranganathan - Inference Gateway on GKE]]
- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
