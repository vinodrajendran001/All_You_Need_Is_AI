---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-05-intelligentlearn-inference-trade-offs-part-1
source_title: "From symptoms to fixes: the trade-offs inside an LLM inference serving system — Part 1: Start with the machine"
source_author: intelligentLearn
source_url: https://medium.com/@wszjzhang/from-symptoms-to-fixes-the-trade-offs-inside-an-llm-inference-system-part-1-start-with-the-9aa825ca7969
tags:
  - source/summary
  - inference
  - kv-cache
  - roofline
  - serving
source_ids:
  - src-2026-11-05-intelligentlearn-inference-trade-offs-part-1
status: active
---

# From Symptoms to Fixes: The Trade-Offs Inside an LLM Inference Serving System — Part 1: Start with the Machine

## Summary

The first of four Medium parts by [[intelligentLearn]] on "Designing LLM inference systems" builds
the machine-level background that the later parts use. A chat service that starts taking long
documents is diagnosed with three ledgers: operator work, memory budget, and request timeline. The
part explains prefill and decode, the two limits the KV cache creates, one H100 roofline, why
batching helps only weight-reading operators, and how precision and tensor parallelism move the
numbers. It ends with a fully specified running case: a 70B-class model on two TP=4 replicas of an
8×H100 node. Long documents cut the memory-only concurrency ceiling from about 690 requests to about
14. A cold 32K prefill misses a 2 s first-token target unless the replica sustains about 76% of
dense peak. The author states that every number is a teaching assumption or a vendor constant, and
none is a measurement.

## Key claims

### Read every request three times

- **Operator ledger:** how much compute is done and how many bytes move. **Memory budget:** how much
  weight and state, and therefore how many concurrent requests, fit. **Request timeline:** whether
  wall-clock time is spent waiting, executing, transferring, or blocked.
- Each ledger alone misleads. "Counting only operators misses queueing and admission effects;
  counting only memory misses latency." Plausible fixes (a larger batch, splitting prefill from
  decode, reusing a cached prefix) answer different questions, so the binding constraint has to be
  found first.

### Prefill, decode, and the two limits the KV cache creates

- In the unchunked, non-speculative baseline, **prefill** is one large matrix-matrix pass that
  produces the first token. Decode is **N−1** thin steps, each consuming the latest token.
- The KV cache "trades storing and reading historical state for repeated computation". It does not
  remove attention's growth with context. Generation therefore inherits two limits: **time to read
  history** and **capacity to store it**. The formula holds for standard MHA/GQA, not for every
  architecture or cache policy.

### One ridge, and why batching helps only some operators

- From vendor H100 SXM5 constants (**3.35 TB/s** HBM, **≈989 TFLOPS** dense BF16), the ridge is
  about **295 FLOP/byte**. "There is one ridge, not one per phase": prefill and decode operators sit
  at different points on the same roofline. Below the ridge a kernel can still be limited by too
  little parallelism, launch overhead, or synchronization, which NVIDIA's guide calls
  latency-limited.
- "Do not add operator inputs and outputs and call the sum actual HBM traffic." Fusion, tiling,
  caching, and register reuse change real traffic. FlashAttention is the canonical case. Hopper's
  WGMMA reads operands from shared memory and keeps accumulators in registers.
- Weight-reading linear layers reach about **B FLOP/byte** in BF16 and touch the ridge only near
  **B ≈ 295**. Attention over historical KV stays near **8 FLOP/byte** under GQA 8:1 (about **1** for
  MHA), "about **37x** below the ridge", and does not move with B because each request reads its own
  history. Calling all of decode compute-bound after batching is too broad.
- The 295 counts weight bytes only. Counting activations and outputs, an 8192 × 2048 TP=4 weight
  shard reaches about **250 FLOP/byte at B = 295** and crosses nearer **B = 360**.

### Precision and parallelism move different terms

- FP8 for weights, activations, and matmuls roughly doubles FLOP/byte and peak (**1979 TFLOPS**).
  The ridge rises to about **591** and the crossing batch barely moves. FP8 weights with BF16 compute
  keep the ridge at 295 and roughly halve the crossing batch, to **148**. INT4 weights take about a
  quarter of FP16 bytes, "but attention, communication, sampling and framework overhead do not become
  four times faster".
- BF16 weights for a 70B model are about **141 GB**. Tensor parallelism splits operators, not
  requests, and every layer pays collective communication. At TP=4 each GPU reads about **35 GB** per
  step, an idealized lower bound of about **10.5 ms** that excludes KV reads, communication, and
  kernel overhead.

### The running case

- **Model and deployment:** 80 layers, d_model 8192, 64 query heads and 8 KV heads, head_dim 128,
  BF16, on one 8× H100 SXM5 node with two TP=4 replicas.
- **Workloads:** short chat (about 500 tokens in, 200 out) and long document (about 32,768 in, 512
  out). **SLO:** TTFT P95 ≤ 2 s and P95 inter-token gap ≤ 50 ms. Prefixes are reusable, but the
  estimates use a cold-cache baseline.
- **KV per token:** 2 × 8 × 128 × 2 B × 80 = **327,680 B = 320 KiB**.
- **KV room per replica:** 80 GB less **35.25 GB** of weights and about 5 GB of overhead leaves
  **39.75 GB** per GPU, or about **159 GB** per replica in decimal GB. Treated as GiB, the
  long-document ceiling becomes 15 instead of 14.
- **Ceilings:** about **0.229 GB** per short chat gives a ceiling of about **690** (693 floored).
  About **10.9 GB** per long document gives about **14**. Context grows **47.5x**, and the ceiling
  falls about **49x** after flooring. This is "only a capacity ceiling": scheduling, latency targets,
  and bursts push real concurrency lower.
- **Prefill cost:** a 32,768-token prefill costs about **4.6 PFLOP** of weight work plus **1.4 PFLOP**
  of attention, about **6.0 PFLOP** in total, against a TP=4 BF16 peak near **3.96 PFLOPS**. At an
  assumed 40% of peak, which the author flags as uncited, it takes about **3.8 s**, about 15
  GPU-seconds. Meeting 2 s would need about **76%**. Attention's share of prefill compute rises from
  about **0.5%** at 512 tokens to about **23%** at 32,768.
- **The four questions handed to Parts 2–4:** why turning up batch size is not enough; when
  colocated chunked prefill suffices and when P/D disaggregation is worth it; why disaggregation
  forces routing to be reconsidered; and when a cache hit saves less execution than the queueing it
  adds.

## Why it matters

The part works through one cluster end to end, with every step checkable, in a form the vault has
otherwise only in pieces. It ties [[LLM Inference]] phase behaviour to
[[Arithmetic Intensity and the Roofline Model]]. Its 295 FLOP/byte ridge and GQA intensity of 8
match the roofline page's existing figures. It adds the byte-count-is-not-traffic warning and the
latency-limited regime to [[GPU Execution Model]]. It also gives [[Model Quantization and Efficiency]]
a precise statement of which bottleneck FP8 and INT4 do and do not move. The ledger discipline
(name the binding constraint before choosing a fix) strengthens
[[Software Performance Engineering]], and the asymmetry between batching weights and batching
history supports [[Inference Efficiency Frontier]].

## Tensions / open questions

- Every number is a teaching assumption or a vendor datasheet constant. The author says "none of
  them is my own measurement", and the 40% efficiency figure is explicitly uncited.
- The ceilings are memory-only ceilings with a cold-cache baseline. Prefix sharing, which the case
  assumes, is deferred to later parts.
- The series' scheduling is inconsistent. This part says Parts 2 to 4 follow on November 10, 17, and
  24, but the captured Parts 2 and 3 were published on November 14 and 19.
- This part's title differs from the later "Designing LLM Inference Systems, Part N" naming. Its
  internal references use "Part II" style numbering.
- A figure placeholder ("Upload figure 7 … k3-kv-budget.png") was left in the published text. The
  capture's description field is only "More".
- The part builds on three earlier essays (promises and measurements, a serving primer, and a
  six-layer map) that the vault has not captured. Its statement that "the primer derives the same
  320 KiB and 159 GB" cannot be checked here.

## Affected pages

- [[LLM Inference]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[GPU Execution Model]]
- [[Model Quantization and Efficiency]]
- [[Inference Efficiency Frontier]]
- [[Software Performance Engineering]]
- [[intelligentLearn]]
- [[KV Cache]]

## Raw capture

- [[knowledge-base/raw/sources/From symptoms to fixes the trade-offs inside an LLM inference serving system — Part 1 Start with the machine]]

## Citations

- Canonical URL: https://medium.com/@wszjzhang/from-symptoms-to-fixes-the-trade-offs-inside-an-llm-inference-system-part-1-start-with-the-9aa825ca7969
- Byline: intelligentLearn (Medium handle @wszjzhang; no personal name in the capture).
- Published: 2026-11-05. Captured: 2026-11-25. Publisher: Medium.
- Hardware constants are cited by the author to the NVIDIA H100 SXM5 80GB datasheet (checked
  2026-09-14).

## Related pages

- [[intelligentLearn - Designing LLM Inference Systems, Part 2 - Six Layers to Investigate]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 3 - How to Evaluate a Change]]
- [[intelligentLearn - Designing LLM Inference Systems, Part 4 - Putting It to Work]]
- [[intelligentLearn]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[GPU Execution Model]]
- [[Model Quantization and Efficiency]]
- [[Inference Efficiency Frontier]]
- [[Software Performance Engineering]]
- [[Prefill-Decode Disaggregation]]
- [[Jacob Peake - AI Chip Architectures]]
- [[ByteByteGo - How to Make LLMs 3X Faster]]
