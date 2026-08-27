---
type: source-summary
created: 2026-07-06
updated: 2026-08-26
source_id: src-2026-07-06-mayank-pratap-singh-speculative-decoding
source_title: "Speculative Decoding: Theory and Implementation in vLLM"
source_author: Mayank Pratap Singh
source_url: https://vizuara.substack.com/p/speculative-decoding-theory-and-implementation
tags:
  - source/summary
  - inference
  - speculative-decoding
  - serving
  - vllm
source_ids:
  - src-2026-07-06-mayank-pratap-singh-speculative-decoding
status: active
---

# Mayank Pratap Singh - Speculative Decoding in vLLM

## Summary

This Vizuara post builds speculative decoding from first principles and then deploys it, ending on an unusually honest note: a real EAGLE3-on-vLLM run where speculation was **slower** than baseline. It starts from why decode is slow (memory-bandwidth bound, not compute bound), derives the draft-then-verify mechanism, proves it produces the *exact* target distribution via rejection sampling, works through the economics (α, τ, K), catalogues the method families (n-gram lookup, Medusa, EAGLE), and finishes with a benchmark that reads the speedup off a real GPU.

Its central framing: generation loads the model's entire multi-hundred-GB weights from HBM once per token (~140 GB/token for a 70B model) while the math units sit idle — so there is **spare compute to burn**, and one weight-load can verify many tokens in parallel for almost the same cost as producing one. Speculative decoding pries open exactly that asymmetry. But it is a **bet**: it pays off with a well-aligned draft and a lightly loaded GPU, and quietly loses when those fail.

## Key claims

- **Decode is memory-bandwidth bound.** Each token requires streaming all weights out of HBM; a 70B model moves ~140 GB per token while ALUs idle. That idle compute is the currency speculation spends, and verifying many tokens in parallel costs about the same as generating one (this is the same prefill/decode split as [[LLM Inference]]).
- **Draft, then verify.** A small draft model `M_q` proposes K tokens cheaply; the big target `M_p` verifies them in a single parallel pass. Verification accepts the drafted prefix **until the first mismatch**, commits it, replaces the mismatched token with the target's own, and discards the rest — so the worst case still returns one correct token and is never slower than plain decoding (at the token level).
- **It is exact, not approximate.** Rejection sampling (Leviathan 2023, arXiv:2211.17192; Chen 2023, arXiv:2302.01318) accepts a draft token with probability `min(1, p(x)/q(x))` and, on rejection, resamples from the normalized residual distribution — provably rebuilding the target distribution `p` token for token. The draft model is a *guesser, not a decider*: a wrong guess costs time, never correctness.
- **Three economics knobs.** **α** (acceptance rate) is the key efficiency number; **τ** (expected accepted tokens per round) follows a geometric series `τ = (1−α^{K+1})/(1−α)` (α=0.30 → ~1.43 tokens/pass; α=0.85 → ~4.15); **K** (lookahead) is a balance, best tuned **adaptively** from the local entropy of the stream (draft far on predictable text, cautiously on uncertain text).
- **System limitations.** The two models run in **lockstep** (bubble time); it only helps when the GPU has **spare compute** (low batch); the draft and target must share an **identical tokenizer/vocabulary** (usually a smaller sibling in the same family); the draft costs **VRAM** you can't give the KV cache or bigger batches; and a rejection triggers a **serial fallback**.
- **Method families differ by where drafts come from:** vanilla draft-target (two models); **n-gram prompt lookup** (model-free); **Medusa** (multiple heads predict multiple positions, verified together with tree attention); **EAGLE** (drafts *features*, not tokens, to avoid token-level stalling).
- **The system tax and batch size decide the real speedup.** Fixed per-step overheads (kernel launches, KV-cache lookups) turn a 2.5× token-math win into ~1.8× measured at batch 1. As batch grows, target verification's share of the step climbs (52%→74%) and the draft's collapses (24%→10%); at batch 128 the GPU is saturated, drafting steals bandwidth, and the slowest request (**straggler**) stalls the batch — effective speedup lands between roughly −5% and +10%. Production stacks therefore toggle speculation **on at light load, off under saturation**.
- **The honest benchmark:** Llama-3.1-8B, single 48 GB Ada GPU, baseline vs EAGLE3 — **slower in both regimes**, with acceptance length **τ=1.81** as the one-glance tell. A small model on a fast, saturated GPU is the hard case; the win grows with model size and acceptance. "Measure your own A/B before you ship it."

## Why it matters

This is the vault's most complete treatment of a single decode-latency technique and seeds the new concept [[Speculative Decoding]]. It slots directly under [[LLM Inference]] (it is the canonical answer to memory-bound decode) and complements [[KV Cache]] (accepted drafts are committed to the cache; the draft model competes with it for VRAM) and [[Model Quantization and Efficiency]] (a *different* lever on the same bytes-moved bottleneck — speculation cuts weight-loads-per-token instead of bytes-per-weight). It also sharpens the [[GPU Execution Model]] "arithmetic intensity / spare compute" story with a concrete exploit, and is a clean contrast for [[Test-Time Scaling]] (speculation makes the *same* output faster; test-time scaling spends compute to change the output). Third Vizuara explainer from [[Mayank Pratap Singh]].

## Tensions / open questions

- The headline "2–3× faster" is real but **conditional**; the author's own run lost, which is the post's most valuable, least-marketed lesson.
- Several figures are labelled "illustrative numbers," so the exact 1.8×/52%→74%/straggler figures are pedagogical, not measured.
- The tokenizer-match constraint limits draft choices to same-family models; cross-tokenizer speculation is out of scope.

## Affected pages

- [[Arithmetic Intensity and the Roofline Model]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Mayank Pratap Singh]]
- [[Speculative Decoding]]

## Citations
- Source URL: [vizuara.substack.com](https://vizuara.substack.com/p/speculative-decoding-theory-and-implementation)
- Code: [LLM-Inference-Playbook](https://github.com/Mayankpratapsingh022/LLM-Inference-Playbook)
- Foundational: Leviathan et al. 2023 (arXiv:2211.17192); Chen et al. 2023 (arXiv:2302.01318).

## Raw capture

- [[2026-07-06 Mayank Pratap Singh - Speculative Decoding Theory and Implementation in vLLM|Speculative Decoding Theory and Implementation in vLLM]]

## Related pages

- [[Speculative Decoding]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[GPU Execution Model]]
- [[Test-Time Scaling]]
- [[Mayank Pratap Singh]]
- [[Vizuara]]
- [[AI Knowledge Base Overview]]
