---
type: concept
created: 2026-07-06
updated: 2026-08-26
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

## Open questions

- How can serving stacks predict α online well enough to auto-tune K and the on/off switch per request?
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
