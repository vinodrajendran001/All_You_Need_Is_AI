---
type: concept
created: 2026-07-06
updated: 2026-09-03
tags:
  - concept
  - inference
  - speculative-decoding
  - serving
  - efficiency
source_ids:
  - src-2026-07-06-mayank-pratap-singh-speculative-decoding
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-26-bytebytego-how-to-make-llms-3x-faster
  - src-2026-09-02-baseten-efficient-frontier-inference
status: active
---

# Speculative Decoding

## Definition

Speculative decoding is a lossless inference-acceleration technique: a small, cheap **draft** model proposes several future tokens, and the large **target** model verifies them all in a single parallel pass, committing the correct prefix and correcting the first mismatch. It produces text drawn from *exactly* the target model's distribution — it only changes speed, never output.

## Why it matters

It is the canonical answer to the central fact of [[LLM Inference]]: decode is **memory-bandwidth bound**, so the GPU's math units sit idle while it streams the whole model out of HBM once per token. That idle compute is free capacity, and one weight-load can verify many tokens for nearly the cost of producing one. Speculative decoding turns that asymmetry into a 2–3× latency win — but only under the right conditions, which is what makes it worth understanding precisely rather than switching on blindly.

## Current synthesis

[[Mayank Pratap Singh - Speculative Decoding in vLLM]] builds the technique end to end.

### The mechanism

- A draft model `M_q` cheaply proposes K tokens; the target `M_p` verifies them in one pass. Verification accepts the drafted prefix **until the first mismatch**, commits it, replaces the mismatched token with the target's own token, and discards the rest. Accepted tokens go into the [[KV Cache]]. Worst case (every guess wrong) still returns one correct token, so it is never slower than plain decoding *at the token level*.

### Why it is exact

- It is **not** an approximation. Rejection sampling (Leviathan 2023; Chen 2023) accepts a draft token with probability `min(1, p(x)/q(x))` and, on rejection, resamples from the normalized residual distribution — provably reconstructing the target distribution token for token. The draft is a **guesser, not a decider**: a wrong guess costs time, never correctness. This is what separates it from simply using a smaller (lossy) model.

### The economics: α, τ, K

- **α (acceptance rate)** — the probability a drafted token survives verification; the single most important efficiency number.
- **τ (accepted tokens per round)** — a geometric series `τ = (1 − α^{K+1}) / (1 − α)`. A weak drafter (α=0.30) commits ~1.43 tokens per expensive pass; a strong one (α=0.85) commits ~4.15. Acceptance compounds: slot 5 is only reached if slots 1–4 all land.
- **K (lookahead)** — how far to guess; a balance, not "bigger is better." Best set **adaptively** from the local entropy of the stream: draft far on predictable text, cautiously on uncertain text.

### When it wins and when it loses

- **Spare compute is the currency.** Speculation helps at **low batch size** (latency-bound), where the GPU is idle and drafting hides in that idle time. At **high batch** (throughput-bound) the GPU is saturated, extra drafting steals bandwidth, and the **straggler effect** (a batched step finishes only when its slowest, re-drafting member does) can make it a net loss. Serving stacks therefore toggle it **on at light load, off under saturation** — the same compute-vs-communication logic as [[GPU Execution Model]] and [[AI Accelerator Architecture]].
- **System tax vs token math.** Fixed per-step overheads (kernel launches, KV-cache lookups) drag a 2.5× token-math win down to ~1.8× measured. As batch grows, target verification's share of the step climbs (52%→74%) and the draft's collapses (24%→10%), so the recoverable headroom shrinks with batching.
- **Constraints:** the draft and target must share an **identical tokenizer** (usually a smaller sibling in the same family); the draft costs **VRAM** the KV cache or larger batches could use; and rejections trigger a **serial fallback**.

### The method families

Techniques differ mainly in *where drafts come from*: vanilla **draft-target** (two separate models); model-free **n-gram prompt lookup**; **Medusa** (extra heads predict multiple positions, verified together via tree attention); and **EAGLE** (drafts *features* rather than tokens to avoid token-level stalling; EAGLE3 is the vLLM-deployable version).

### It is a bet

- The honest lesson: on Llama-3.1-8B on a single saturated 48 GB Ada GPU, EAGLE3 came out **slower in both regimes** — acceptance length τ=1.81 was the one-glance tell. The win grows with **model size** and **acceptance**; a small model on a fast, saturated GPU is the losing case. Always A/B on your own hardware before shipping.

## Relationship to neighbouring levers

Speculative decoding is complementary to, not a substitute for, the other efficiency levers: [[Model Quantization and Efficiency|quantization]] cuts *bytes per weight*, [[KV Cache|KV-cache compression]] cuts the *other* growing object decode must read, and speculation cuts *weight-loads per token*. It is also the clean opposite of [[Test-Time Scaling]]: speculation makes the **same** output arrive faster, whereas test-time scaling spends extra compute to **change** the output (reason better).

## The headroom speculation depends on can already be spent

The strongest constraint on this page comes from [[Changyi Yang - Why MLA and MTP Fight Each Other]], and it is not about acceptance rate at all. Speculation works because a memory-bound decode leaves GPU compute idle; verifying K drafted tokens in one pass costs arithmetic that was going to waste. Formally, HBM traffic barely grows with the number of verified query positions S while QK/PV compute scales nearly linearly, so `AI(S) ≈ S · AI(S=1)` — speculation is a device for climbing the roofline (see [[Arithmetic Intensity and the Roofline Model]]).

That only pays while there is roofline left. **Attention architectures that maximise cache reuse have already spent it.** DeepSeek-style MLA reaches ~256 FLOP/B at a single query and Kimi K3's MLA layer ~192 FLOP/B, against balance points of ~206 FLOP/B on H200 and the two-to-three-hundred range on H100/B200. Taking S to 2 gives 512 and 384 — past the knee, where the extra verification arithmetic stops being free and **starts costing real latency**. On a low-intensity MQA workload at AI ≈ 70–100 the same speculation is nearly free.

Two corollaries:

- MLA and multi-token prediction are **not independent optimisations**. Both are compute-for-bandwidth trades drawing on one finite pool, which is a different failure mode from the VRAM competition between draft model and cache described above — and it applies even to self-drafting MTP, which borrows no memory at all.
- Typical speculation windows of 2–8 (at most a few dozen) stay well below the S ≈ 171 crossover at which the dense-GEMM attention algorithm would take over, so speculation does not change which attention kernel is dispatched.

[[Jacob Peake - AI Chip Architectures]] describes the same mechanism from the hardware side: speculative decoding and multi-token prediction exist to promote decode GEMVs back into GEMMs, alongside continuous batching — which means batch size and speculation are also competing for the same headroom, not stacking on it.

## Where the technique comes from

[[Wafer - AI Performance Engineering Resources]] supplies the lineage this page has been describing through a single vLLM implementation write-up. The method was introduced independently by Leviathan et al. (*Fast Inference from Transformers via Speculative Decoding*) and Chen et al. (*Accelerating Large Language Model Decoding with Speculative Sampling*), both establishing the property that makes it safe to deploy: the accept/reject rule preserves the target model's output distribution exactly.

Later work removes the separate draft model. **Medusa** attaches multiple decoding heads to the target model itself; **EAGLE** speculates in feature space rather than token space, which raises acceptance rates. Both matter because the standing objection to speculation — that you now have to serve, tune, and keep a second model aligned with the first — is an operational cost rather than a mathematical one, and self-drafting removes it.

## The same idea, one layer up

[[Speculative Tool Execution]] ([[Alex L. Zhang - Speculative Programmatic Tool Calling]]) applies this page's pattern above the token level: a harness parses tool calls out of a *partially generated* program and pre-launches them, so that if the finished program invokes them they return from cache. Guessing actions instead of tokens.

The structural analogy is close — cheap speculative work overlapped with an expensive serial process, discarded when wrong — but two properties do not carry over. There is **no distributional guarantee**: token speculation is provably lossless because the accept/reject rule preserves the target distribution, while a speculated tool call is either used or wasted, and a wasted one has already consumed money, tokens, and rate limit. And the wrong-guess cost is external rather than internal: a mispredicted draft token costs idle compute, a mispredicted sub-agent call clogs a serving engine other requests are waiting on.

Both techniques exploit the same underlying slack, though, which is worth noting: on a locally served model the engine is memory-bound decoding the main context, so speculative sub-calls consume compute that would otherwise sit idle — the argument on [[Arithmetic Intensity and the Roofline Model]], applied to agent harnesses.

## A fourth draft family, and what production actually reports

[[ByteByteGo - How to Make LLMs 3X Faster]] adds a draft source the taxonomy above does not cover:
**a degraded copy of the target model itself**. The draft runs the same weights under a reduced
compute budget — quantization, layer skipping, or a compressed KV cache — while verification runs
at full precision. QuantSpec drafts with 4-bit weights and a 4-bit KV cache and reports above
**1.78× with acceptance above 90%**.

This sits between the two families already described. Like Medusa and EAGLE it needs no second
checkpoint to serve, version, and keep aligned; unlike them it needs no training access, since it
reuses weights you already have. The cost moves to implementation complexity, because draft and
target now share hardware and cache structures. It also makes [[Model Quantization and Efficiency|quantization]]
do double duty: the same 4-bit machinery that cuts bytes per weight becomes the mechanism for
generating cheap drafts.

The same source supplies the first **production** acceptance figure on this page. DeepSeek reported
**80–90% acceptance for the second predicted token when serving DeepSeek-V3**, worth roughly 1.8×
generation throughput. Everything else here comes from benchmarks or single-GPU experiments, so a
sustained production number is a different class of evidence — and it lands near the top of the α
range the economics section models, which is what makes self-drafting MTP heads attractive despite
their training cost.

## Acceptance is a property of the workload, not the configuration

The α discussion above treats acceptance as something you measure and tune around. The sharper
framing is that **α is mostly determined by what your users are asking**, not by what you deployed.

Structured, repetitive output drafts well — code generation, summarization, extraction, and
retrieval-augmented answers all reuse large amounts of text already in the context, which makes the
next token easy for a small model to guess. Open-ended output drafts badly, because creative writing
and open conversation generate genuine variety that a small model diverges from quickly. Sampling
temperature compounds this: higher temperature flattens the distribution and pushes acceptance down.

The operational consequence is uncomfortable. Two teams can deploy the identical configuration on
identical hardware and get different results, because their traffic differs. Speculative decoding is
therefore not a setting that can be validated once and shipped as a default; it has to be measured
against the actual request distribution, and re-measured when that distribution shifts.

## Prefill is untouched

Speculation applies to generation, not prompt processing, so **time to first token is unchanged**.
Workloads with long prompts and short outputs — classification, extraction over large documents,
routing — have almost nothing to gain no matter how well they draft. DeepSeek stated the tradeoff in
the same direction: multi-token prediction *slightly reduces* throughput while significantly
improving end-to-end generation latency. Speculation buys perceived responsiveness, and pays for it
in aggregate capacity.

## Partial answer to the auto-tuning question

This page has stood with an open question about whether serving stacks could predict α online well
enough to auto-tune K and the on/off switch per request. Shipped code gives a partial answer, and it
works by **sidestepping prediction entirely**.

vLLM exposes a flag that disables speculation above a configurable batch size, and supports dynamic
adjustment in which **draft length shrinks as concurrency rises and reaches zero under heavy load**.
Rather than estimating acceptance, it keys draft length to *observed concurrency* — a directly
measurable proxy for whether spare compute exists at all. [[ByteByteGo - How to Make LLMs 3X Faster]]
frames this as routine operational tuning rather than an edge case.

That resolves half the question. Concurrency tells you whether there is headroom to spend; it says
nothing about whether *this particular request* will draft well. The workload-dependence of α above
means a code-completion request and a creative-writing request at the same batch size deserve
different K, and no serving stack described in this vault distinguishes them. The measured shape of
the headroom half is stark: one systematic evaluation reported **up to 1.96× on a 70B model at batch
size 1, declining to 1.21× at batch size 128**, and falling below baseline under higher concurrency.

## Has speculation changed category?

This page frames speculation as spending headroom that could be spent elsewhere — a tradeoff. [[Philip Kiely -
The Efficient Frontier of LLM Inference]] argues the category boundary has moved, and the disagreement is
worth keeping visible rather than resolving.

The historical framing is granted: speculation *was* a tradeoff technique, because it was expensive, sequences
were short, acceptance rates were low, and it was viable only at small batch sizes. The claim is that
**EAGLE-3, DSpark and DFlash** changed this, because their strength yields efficiency from **skipped forward
passes** in addition to raw latency reduction — a genuine reduction in work rather than a reallocation of it.
That would make speculation **frontier-moving**: gains that can be allocated to latency or throughput at will.

The qualification is retained in the same source: these methods still **compete with the main model loop for
resources**, and so still cap maximum batch size. Code generation benefits most, because output sequences are
relatively predictable — which is also why it is the case most likely to overstate the general result.

Whether skipped forward passes count as *new* efficiency or as *better-spent* headroom depends on whether the
drafting cost is counted against the budget, so the two readings are not fully reconcilable. See
[[Inference Efficiency Frontier]].

## Open questions

- Can a serving stack estimate per-request draftability — from prompt features, task type, or
  temperature — rather than only inferring global headroom from batch size, which is all vLLM's
  dynamic draft length currently does?
- Can cross-tokenizer or tokenizer-free speculation relax the same-family constraint?
- Where is the model-size/batch crossover at which speculation reliably pays, and how does it shift with EAGLE-style feature drafting?
- Should a serving stack disable speculation automatically for high-arithmetic-intensity attention architectures, and can the balance point be probed at runtime rather than assumed from the datasheet?

## Related pages

- [[Mayank Pratap Singh - Speculative Decoding in vLLM]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[GPU Execution Model]]
- [[Test-Time Scaling]]
- [[Small Language Models]]
- [[AI Knowledge Base Overview]]
- Wafer - AI Performance Engineering Resources
- Serving Benchmarks and Goodput
- [[Speculative Tool Execution]]
- [[Programmatic Tool Calling]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[ByteByteGo - How to Make LLMs 3X Faster]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Efficiency Frontier]]
- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
