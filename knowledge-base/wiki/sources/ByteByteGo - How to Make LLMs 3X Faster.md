---
type: source-summary
created: 2026-08-27
updated: 2026-08-27
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

- A 70B model at 16-bit precision means reading roughly **140 GB of weights per token**. On a
  modern datacenter GPU that transfer takes tens of milliseconds while the arithmetic applied to
  those weights is comparatively trivial.
- Compute utilization is **90–95% during prompt processing** but falls to **20–40% during token
  generation**. The difference is how much work each weight read supports: prefill applies the
  weights to thousands of positions at once, decode applies them to exactly one.
- The practical consequence: a GPU with higher memory bandwidth improves generation speed more than
  one with more raw compute.

### Mechanism

- A transformer computes a next-token prediction at *every* position in a single pass, and causal
  masking keeps each of those predictions conditioned exactly as it would have been under
  step-by-step generation. Appending K candidates and running one pass therefore yields the target
  model's own opinion at each of the K positions.
- Verification and generation are **the same operation**; the saving comes purely from doing it at
  several positions per pass rather than one.
- On mismatch, the verification pass has already computed the target's prediction at that position,
  so that token is used directly. This bounds the downside: even with every candidate rejected you
  still get the one token plain decoding would have produced.
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

### Acceptance is a property of the workload

- Structured, repetitive output — code generation, summarization, extraction, RAG answers — reuses
  large amounts of input text and drafts well. Open-ended output such as creative writing and open
  conversation diverges from a small model far more often and drafts badly.
- Higher sampling temperature flattens the distribution, increases mismatches, and pushes acceptance
  down. Below roughly **50% acceptance the extra work outweighs the savings**.
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
   pretraining for quality and reused them at inference as the draft source. Costs training access,
   so it is unavailable unless you control the model.
3. **A cheaper version of the same model** — the draft runs the same weights under a reduced compute
   budget via quantization, layer skipping, or a compressed KV cache. **QuantSpec** drafts with
   4-bit weights and a 4-bit KV cache while verifying at higher precision, reporting **above 1.78×
   with acceptance above 90%**. Costs implementation complexity, since draft and target share
   hardware and cache structures.
4. **A search over existing text** — scan prompt and prior output for a recent matching sequence and
   propose whatever followed last time. Zero memory cost, single model, but contributes only when
   output repeats input, where it reaches **2×–4×** on document editing and summarization.

- Tokenizer compatibility constrains pairing more tightly than model quality does: a stronger small
  model with a different vocabulary is unusable as a draft without extra machinery.

### Concurrency is the real limit

- Speculative decoding spends capacity that would otherwise go unassigned. As concurrent requests
  accumulate, one weight read serves many requests, compute approaches saturation, and verification
  starts competing with real work.
- One systematic evaluation reported **up to 1.96× on a 70B model at batch size 1, declining to
  1.21× at batch size 128**, and the technique can fall **below baseline** under higher concurrency.
- **vLLM exposes a flag disabling speculation above a configurable batch size, and supports dynamic
  adjustment where draft length shrinks as concurrency rises and reaches zero under heavy load.**
  The source frames this as routine operational tuning rather than an edge case.
- **Time to first token is unchanged**, since speculation applies to generation and not prompt
  processing. Workloads with long prompts and short outputs have little to gain.
- DeepSeek documented the tradeoff directly: multi-token prediction slightly *reduces* throughput
  while significantly improving end-to-end generation latency.

## Why it matters

Most of this restates what [[Speculative Decoding]] already carries. Three items do not.

The **self-drafting-by-degradation family** (QuantSpec and relatives) is a genuinely fourth
category alongside draft-target, extra heads, and n-gram lookup. It is interesting because it
sidesteps the standing objection to speculation — a second checkpoint to serve, version, and keep
aligned — without needing training access the way Medusa-style heads do.

The **DeepSeek production figures** matter because nearly everything else in this vault about
acceptance rates comes from benchmarks or single-GPU experiments. An 80–90% acceptance rate
sustained in production serving is a different class of evidence.

Most importantly, **vLLM's dynamic draft-length control partially answers an open question this
vault had already posed**. The [[Speculative Decoding]] page asked how serving stacks could predict
acceptance online well enough to auto-tune K and the on/off switch per request. The answer in
shipped code turns out to sidestep prediction: rather than estimating acceptance, vLLM keys draft
length to *observed concurrency*, which is a directly measurable proxy for whether spare compute
exists. That is a weaker mechanism than the question imagined, and it addresses the "is there
headroom" half while leaving the "will this request draft well" half open.

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

- [[Speculative Decoding]]
- [[Mayank Pratap Singh - Speculative Decoding in vLLM]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
