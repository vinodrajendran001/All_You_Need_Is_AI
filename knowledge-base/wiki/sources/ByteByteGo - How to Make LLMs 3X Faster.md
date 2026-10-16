---
type: source-summary
created: 2026-08-27
updated: 2026-10-16
source_id: src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
source_title: "How to Make LLMs 3X Faster"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-to-make-llms-3x-faster
tags:
  - source/summary
  - inference
  - speculative-decoding
  - serving
  - efficiency
source_ids:
  - src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
status: active
---

# ByteByteGo - How to Make LLMs 3X Faster

## Summary

An explainer on speculative decoding, walking from why autoregressive generation is serial, through
what a GPU actually spends a forward pass doing, to the draft-and-verify loop, the acceptance rule
that makes it lossless, and the conditions under which the technique stops paying.

The vault already has a deep [[Speculative Decoding]] page built from a vLLM implementation
write-up and two hardware-side sources. This piece is a secondary explainer and repeats much of
that ground. Its value is concentrated in four places where it adds something the existing page did
not have: a **fourth draft-source family**, **production acceptance numbers from DeepSeek**,
**concurrency scaling measurements**, and — most usefully — a **partial answer to one of the
page's own standing open questions** about auto-tuning.

## Key claims

### The bandwidth argument

- A dense 70B model at 16-bit precision has roughly **140 GB of weights**. The article's
  per-token-read argument assumes low-batch dense decoding; batching amortizes weight traffic
  across sequences, and sharding changes the per-device boundary.
- The article quotes **90–95% compute utilization during prompt processing** and **20–40% during
  token generation** without a complete workload/hardware configuration. These illustrate the
  proposed contrast, not universal phase-utilization measurements.
- More bandwidth helps when memory traffic is the limiting resource. The October 9 lint scopes
  the earlier hardware-buying rule to that regime: a more compute-intensive or communication-bound
  workload need not benefit in the same way.

### Mechanism

- A transformer computes a next-token prediction at *every* position in a single pass, and causal
  masking keeps each of those predictions conditioned exactly as it would have been under
  step-by-step generation. Appending K candidates and running one pass therefore yields the target
  model's own opinion at each of the K positions.
- Verification and generation are **the same operation**; the saving comes purely from doing it at
  several positions per pass rather than one.
- Under **greedy matching**, the target's prediction supplies a correction at the first mismatch.
  Under sampling, the residual rule below is required instead. Even a round that commits just one
  token pays drafting and verification costs, so this progress guarantee does not bound latency
  below the plain-decoding baseline.
- Draft length K is commonly 3–5. Larger K raises the ceiling but lowers the odds later candidates
  survive, because the draft model conditions on its own unverified output as it goes.

### The lossless guarantee

- Under greedy decoding the rule is simply match-or-drop. Under sampling: keep the candidate if the
  target gave it at least as much probability as the draft did; keep it proportionally when the
  target gave it less; and on rejection, resample from an adjusted distribution with the draft's
  scores subtracted out first. Summing both paths reproduces the target's own odds exactly.
- Two honest qualifications the source makes: matching odds still allow different wording, since
  sampling remains random either way; and limited floating-point precision can flip the winner when
  two tokens sit nearly tied.

### Acceptance depends on the drafter and workload

- The article presents structured, repetitive output as favorable and open-ended output as harder.
  Those are heuristics: model pairing, prefix, and sampling matter as well as the task label.
- It also says higher temperature lowers acceptance and gives **roughly 50%** as a break-even
  threshold. Neither is universal: temperature changes the overlap of both distributions, and
  break-even depends on draft, verification, memory, and scheduling costs.
- **DeepSeek reported 80–90% acceptance for the second predicted token in production serving of
  DeepSeek-V3, worth roughly 1.8× generation throughput.**
- The consequence the source draws: two teams can deploy the identical configuration on identical
  hardware and get different results, because their users are asking different questions.

### Four places a draft can come from

1. **A separate small model** — 10–20× fewer parameters, same family, identical tokenizer. Costs a
   second checkpoint to deploy and version, plus VRAM taken out of the KV-cache budget, which
   reduces how many concurrent requests the server can hold.
2. **Extra prediction heads on the target** — lightweight heads predicting two or three positions
   ahead off the target's own internal representations. DeepSeek-V3 trained these during
   pretraining for quality and reused them at inference as the draft source. Creating new heads
   requires training access; deploying compatible released heads still needs internal-model/runtime
   integration but does not require the operator to train them from scratch.
3. **A cheaper version of the same model** — the draft runs the same weights under a reduced compute
   budget via quantization, layer skipping, or a compressed KV cache. **QuantSpec** drafts with
   4-bit weights and a 4-bit KV cache while verifying at higher precision, reporting **above 1.78×
   with acceptance above 90%**. Costs implementation complexity, since draft and target share
   hardware and cache structures.
4. **A search over existing text** — scan prompt and prior output for a recent matching sequence and
   propose whatever followed last time. No separate draft-model weights, not zero auxiliary memory:
   lookup state and verification workspace can still cost memory. The source reports **2×–4×**
   on repetitive document-editing and summarization workloads.

- Tokenizer compatibility constrains pairing more tightly than model quality does: a stronger small
  model with a different vocabulary is unusable as a draft without extra machinery.

### Concurrency is one operating-condition limit

- Speculative decoding spends capacity that would otherwise go unassigned. As concurrent requests
  accumulate, one weight read serves many requests, compute approaches saturation, and verification
  starts competing with real work.
- One systematic evaluation reported **up to 1.96× on a 70B model at batch size 1, declining to
  1.21× at batch size 128**, and the technique can fall **below baseline** under higher concurrency.
- The article describes **vLLM batch-size-based disabling and concurrency-dependent draft length**.
  This is its account of an available control, not a check of every current engine version or a
  rule that large batches always lose; newer cache-bound cases qualify that heuristic.
- The raw says time to first token stays **roughly** the same because speculation does not directly
  accelerate prefill. That is not an invariant: draft initialization, queueing, and resource
  competition can change TTFT. Long prompts and short outputs limit the generation work available
  to accelerate.
- DeepSeek documented the tradeoff directly: multi-token prediction slightly *reduces* throughput
  while significantly improving end-to-end generation latency.

## Why it matters

Most of this restates what [[Speculative Decoding]] already carries. Three items do not.

The **self-drafting-by-degradation family** (QuantSpec and relatives) is a genuinely fourth
category alongside draft-target, extra heads, and n-gram lookup. It is interesting because it
sidesteps the standing objection to speculation — a second checkpoint to serve, version, and keep
aligned — without needing training access the way Medusa-style heads do.

The **DeepSeek production figures** add a reported serving operating point beyond a local
single-GPU experiment. The 80–90% figure is for the **second predicted token**, not a mean
acceptance rate across every draft position or a guarantee for another deployment.

The described concurrency controller partially answered the vault's earlier auto-tuning question
by observing load rather than predicting request-specific acceptance. It should not remain the
current answer to the whole question: [[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]]
later describes **DSpark's acceptance predictions plus profiled engine costs**. That newer
controller is not evidence that every vLLM deployment implements it.

## Tensions / open questions

- This is a secondary explainer. Its figures belong to other work — the DeepSeek-V3 report, the
  QuantSpec paper, and an unnamed "one systematic evaluation" for the batch-size scaling — and the
  post carries its own disclaimer that it is assembled from publicly shared details.
- The batch-scaling result (1.96× → 1.21×) is cited without naming the study, hardware, draft
  configuration, or workload, so it cannot be compared cleanly against the vault's existing
  EAGLE3-on-Ada measurement.
- The claim that acceptance below ~50% makes speculation a net loss is given as a round number with
  no derivation, and it must in fact depend on the draft/target cost ratio rather than being a
  universal threshold.
- The article reports both roughly 1.8× DeepSeek generation throughput and a separate statement
  that multi-token prediction slightly reduces throughput while improving end-to-end latency.
  Their measurement boundaries are not aligned here; do not combine them as one operating point.
- The October 16 lint restores the raw's "roughly" TTFT qualifier and narrows its greedy
  walkthrough, zero-memory shorthand, training-access requirement, and load/temperature rules.
  Distributional exactness does not imply seed-identical text or factual correctness.
- The article's headline "3X" is not supported by any figure in its own body; the measurements it
  reports are 1.21×–2×, with 2×–4× only for the narrow prompt-lookup case on repetitive text.

## Affected pages

- [[Speculative Decoding]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[Model Quantization and Efficiency]]
- [[Serving Benchmarks and Goodput]]
- [[KV Cache]]
- [[ByteByteGo]]

## Raw capture

- [[2026-08-26 ByteByteGo - How to Make LLMs 3X Faster]]

## Related pages

- [[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]]
- [[Speculative Decoding]]
- [[Mayank Pratap Singh - Speculative Decoding in vLLM]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
