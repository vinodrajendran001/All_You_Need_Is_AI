---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-15-anshuman-mishra-baseten-2000tps
source_title: "I reverse engineered baseten’s 2000TPS inference engine"
source_author: "Anshuman Mishra (recovered from the site homepage; see Citations)"
source_url: "https://heyyanshuman.com/posts/baseten_2000tps"
tags:
  - source/summary
  - inference
  - serving
  - speculative-decoding
  - mixture-of-experts
  - roofline
source_ids:
  - src-2026-11-15-anshuman-mishra-baseten-2000tps
status: active
---

# I Reverse Engineered Baseten's 2000TPS Inference Engine

## Summary

A third-party, source-code reading of [[Baseten]]'s open-sourced "DeepSeek Ultrafast" engine, written
in Rust and CUDA for **DeepSeek-V4.1-Flash**. Baseten's own headline, relayed here, is about **2,060
tokens per second on eight B300 GPUs**, plus prefilling a million tokens "in roughly twelve seconds".
The author did not re-run anything: the closing section states "No independent GPU timing or
numerical-equivalence result is claimed here." The value of the piece is that it explains, from code
pinned to specific commits, which mechanisms could produce the number, and it is careful about what
the number does not show.

Three kinds of claim need to be kept apart when reading it:

- **Baseten's first-party figures** (the announcement and README rates and step times), which the
  author reports but does not reproduce.
- **Code-level facts** about what the pinned revision does, cited line by line.
- **The author's arithmetic and inferences**: rooflines, toy routing models, and back-of-envelope
  break-even points. These are labelled in the source as bounds or illustrations, not measurements.

## Key claims

### What 2,060 TPS decomposes into (Baseten-reported, author arithmetic)

Baseten's README gives **1,740 tokens/s at 3.30 ms per step on 4 × GB300 (TP4)** and **2,060 tokens/s
at 2.71 ms per step on 8 × B300 (TP8)**. TP means tensor parallelism: the GPUs cooperate on one
request, not four or eight independent copies. The author divides: 1000 / 2060 ≈ **0.485 ms per
emitted token**, 2060 × 0.00271 ≈ **5.58 tokens per step**, about **369 steps per second**. Each
step produces several tokens because it is a speculative step (draft, verify, commit). The request
logger's "average acceptance length" counts accepted draft tokens per step **plus one** extra token, so
**5.6 tokens/step ≈ 4.6 accepted drafts + 1**. Dividing 5.6 by the two step times gives about
**2,066 TPS** and **1,697 TPS**, "close to but not exactly" the headlines, so the README summaries are
approximate. The decode demo generated Tetris HTML with thinking disabled. The million-token prefill is
a separate result, and the author says it does not show that the decode rate held with a million
tokens in context.

### The draft, verify, commit step

- **Drafting.** DeepSeek's model-native drafter, DSpark, reads target features from layers 37-39 and
  runs three small "MTP layers" over the whole draft block at once. A rank-256 "Markov" correction then
  conditions each draft token on the previous one without a full drafter pass per position, sampling
  via Gumbel-max over a vocabulary sharded across GPUs. DSpark and the Markov head are model features,
  and SGLang implements the same head.
- **How many to verify.** On the SM103 (Blackwell Ultra) profile the draft limit is **six**, so the
  target verifies **seven** positions (anchor plus six drafts). A confidence kernel can shorten the
  block when cumulative confidence falls below **0.3 (TP4)** or **0.2 (TP8)**, which the author calls
  "profile choices, not universal optimal constants".
- **GPU-side branching.** The step is a captured CUDA graph containing one verification branch per
  supported length. The GPU selects the branch with `cudaGraphSetConditional`, so the CPU never reads
  the confidence score. The host still launches each step. SGLang has its own confidence-aware
  planner, so the author treats this as a difference in execution paths, not an exclusive feature.
- **Acceptance rule.** The server fixes temperature and top-p at one. Verification uses a **block
  sampler**: it computes cumulative log-ratios of target and draft probabilities, tests every candidate
  block length, and "chooses the **largest passing length**". This is neither a greedy argmax match nor
  the textbook per-token `min(1, p/q)` rule.
- **Precision.** A distribution-preserving sampler preserves the distribution its *numerical
  implementation* computes; it "does not make a quantized target identical to a higher-precision
  model". The TP4 profile can verify with an FP8 output head.
- **Break-even.** 2.71 / 5.6 ≈ **0.484 ms** is the plain-decoding time per token that speculation would
  have to beat. It is "a threshold, not a measured baseline or speedup", because no matched plain-decode
  time exists.

### Rooflines: why seven tokens share dense weights but not experts (author arithmetic)

For FP4 weights with a one-byte scale per 32 weights (17/32 bytes per weight), one token position
gives about **3.76 FLOPs per weight-byte** and seven positions about **26.35**. NVIDIA's datasheet puts
the HGX B300 at **7.7 TB/s** and a dense FP8 peak of **4.5 PFLOPS**, a balance point near **584
FLOPs/byte**, so even seven positions remain far on the memory side. For the fused `tg2_wqkv`
projection at seven positions, reading the FP8 weights ideally takes **1.19 µs** against **0.029 µs**
of arithmetic. Neither is a kernel-duration prediction.

Mixture-of-experts layers break the reuse argument. Each token picks **6 of 384** experts. If all seven
positions pick the same six, intensity stays at 26.35; if their choices are disjoint (42 experts), it
falls back to 3.76. A hypothetical uniform independent router touches about **40.08** experts, or
about **3.94** FLOPs/byte. Real routes can be correlated.

### Engine specialisation

- The pinned code logs `"sgl moe: {} layers on SGLang's low-batch MoE chain"` and enables that path for
  the SM103 TP4/TP8 profiles. Router, two expert GEMMs and the following communication step are designed
  together. At the pinned SGLang revision the comparable specialised MXFP4 decode-MoE switch
  **defaults to false**, and SGLang's speculative algorithm defaults to `None`. That identifies
  configuration differences, "not a measured TPS gap".
- Splitting each expert across more GPUs pads storage: about **7.6%** overhead at TP4 and **26.4%**
  at TP8 (allocated bytes, not bytes read per token).
- Communication is fused into neighbouring kernels (NVLink multicast, mailbox publishing,
  programmatic dependent launch, side streams), rather than treated as an isolated library call.
- TP8 over TP4 is **2060 / 1740 ≈ 1.184**, but "not a clean strong-scaling experiment": platform,
  thresholds, MoE path and output head differ between the profiles.
- Kernels support a narrow range of token counts and reject unsupported verification shapes, partly
  to avoid silently switching numerics.

### The million-token prefill is a shorter schedule, and approximate

DeepSeek-V4.1-Flash is a 20-layer encoder plus 20-layer decoder whose global KV comes from the encoder
side. The engine streams the whole prompt through the first 20 layers, then replays the decoder only
over the last **128** tokens. At one million tokens that is **20,002,560** layer-token evaluations
against **40,000,000** for a full pass, a ratio of about **0.500064**. The author says this does not
prove a twofold FLOP or time reduction. The paper's own Section 3.2.2 calls bounded replay an
**approximation** of local state; DeepSeek reports "little quality degradation" in its evaluations, but the output is not
mathematically identical to a full decoder pass. SGLang has similar decoder-tail replay machinery.

### What the headline cannot tell you

The worker loop "serves one shared generation job at a time", so the rate says nothing about aggregate
throughput, queueing latency, or cost per token under concurrent load. SGLang and vLLM (an opt-in
`latency_specialized` backend) contain many of the same techniques but do not enable them by default.
Without matched measurements the code "does not establish a TPS ranking".

## Why it matters

The vault's [[Speculative Decoding]] page treats acceptance length, verification rules and draft
budgets mostly through surveys and secondary engine accounts. This is the first code-level trace of a
production-grade speculative step, and it surfaces details those accounts lack: a block-level
acceptance rule, GPU-chosen verification lengths, and an explicit precision caveat on "exact"
speculation. It also gives [[Arithmetic Intensity and the Roofline Model]] a worked counter-case:
verification blocks raise intensity on dense projections but not necessarily in expert layers. For
[[Serving Benchmarks and Goodput]] it is a model of reading a vendor headline: decompose it, find what
it was measured on, and say which questions it cannot answer. For [[Inference Serving Engines]] it
documents what a single-model, single-hardware engine gives up for speed.

## Tensions / open questions

- **No independent timing.** Every throughput, step time and prefill figure is Baseten's. The author's
  numbers are derived from them, not measured.
- **Rounding inconsistencies are recorded in the source itself**: 5.6 tokens/step implies about 2,066
  and 1,697 TPS, not 2,060 and 1,740. The break-even figure appears as both 0.485 ms (1000/2060) and
  0.484 ms (2.71/5.6).
- **Draft limit six versus DeepInfer's default five.** [[Mehul Gupta - What is DeepSeek DeepInfer]]
  reports a maximum draft length defaulting to five for DeepSeek's own engine. Both engines serve the
  same model family, so the draft budget is an engine profile choice, not a model constant.
- **"Exact" speculation under quantization.** The block sampler preserves the distribution computed by
  an FP4/FP8 implementation, not that of a higher-precision reference. No numerical-equivalence test is
  reported.
- **Approximate prefill.** The million-token figure depends on bounded replay that DeepSeek itself
  calls approximate, so it is not a like-for-like prefill comparison with a full-pass engine.
- **Code origin.** The MoE chain is labelled with SGLang's name, and Baseten's README says optimising
  agents could read SGLang and FlashInfer. The author declines to say which lines came from where.
- **Consistency check (reviewer inference).** The prefill schedule runs prompt tokens through about
  half the layers that generated tokens use. That fits the 2:1 ratio of active parameters per generated
  versus per input token that [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]
  reports. Neither source makes this link.

## Affected pages

- [[Speculative Decoding]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Baseten]]
- [[DeepSeek]]

## Raw capture

- [[knowledge-base/raw/sources/I reverse engineered baseten’s 2000TPS inference engine]]

## Citations

- Canonical URL: <https://heyyanshuman.com/posts/baseten_2000tps>
- Author: the capture's `author` field is empty and the body has no byline. On 2026-11-20 a read-only
  fetch of the site homepage (`heyyanshuman.com`) identified the site owner as **Anshuman Mishra**. The
  post is attributed to him as the site's author; the post page itself shows no separate byline.
- Publication date: the capture has no `published` field. The same read-only fetch of the post page
  showed "Published November 15, 2026", which sets the `source_id` date. The capture was created
  2026-11-17. No web-only figures were imported.
- Pinned revisions studied, per the source: Baseten DeepSeek Ultrafast `76766a9…`, SGLang `a56dbcf…`,
  vLLM `9bc16ae…` (targeted inspection only), DeepSeek model repository `314113f…`.

## Related pages

- [[Speculative Decoding]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Mixture of Experts]]
- [[Baseten]]
- [[DeepSeek]]
- [[Sparse Attention]]
- [[KV Cache]]
- [[LLM Inference]]
- [[GPU Kernel Optimization]]
- [[Megakernels]]
- [[Mehul Gupta - What is DeepSeek DeepInfer]]
- [[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]]
- [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]
- [[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]
- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
