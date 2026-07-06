---
type: concept
created: 2026-07-06
updated: 2026-07-06
tags:
  - concept
  - inference
  - speculative-decoding
  - serving
  - efficiency
source_ids:
  - src-2026-07-06-mayank-pratap-singh-speculative-decoding
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

## Open questions

- How can serving stacks predict α online well enough to auto-tune K and the on/off switch per request?
- Can cross-tokenizer or tokenizer-free speculation relax the same-family constraint?
- Where is the model-size/batch crossover at which speculation reliably pays, and how does it shift with EAGLE-style feature drafting?

## Related pages

- [[Mayank Pratap Singh - Speculative Decoding in vLLM]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[GPU Execution Model]]
- [[Test-Time Scaling]]
- [[Small Language Models]]
- [[AI Knowledge Base Overview]]
