---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-12-nathan-barry-detllm-integer-inference
source_title: "Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic"
source_author: "Nathan Barry"
source_url: "https://nathan.rs/posts/detllm/"
tags:
  - source/summary
  - inference
  - determinism
  - quantization
  - reproducibility
source_ids:
  - src-2026-11-12-nathan-barry-detllm-integer-inference
status: active
---

# Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic

## Summary

Nathan Barry describes **DetLLM**, a proof of concept that runs Qwen3-0.6B with **exact integer
arithmetic for every operation between the input ids and the int32 logits** — matmuls, normalization,
activations, softmax and rotary embeddings — so that greedy output is bit-identical across batch
sizes, prefill/decode splits, GPUs, CPUs and vendors. The post starts from
[[Thinking Machines]]' diagnosis of why temperature-0 decoding is not deterministic (relayed by Barry,
not read directly here), argues that their batch-invariant kernels fix the problem only on one GPU
with those kernels, and proposes removing floating point altogether, since integer addition is
associative.

The project began at a SpaceXAI hackathon and, per the author, became a paper at two NeurIPS 2026
workshops (ML for Systems and On-Device Intelligence). All results are the author's own.

## Key claims

### Why inference is nondeterministic

- **Float addition is not associative.** Every float add rounds, so `(a + b) + c` and `a + (b + c)`
  can differ; an LLM forward pass is mostly long sums.
- **Kernels are run-to-run deterministic but not batch invariant.** cuBLAS selects among kernels by
  shape; a small batch may split the reduction ("split-K") while a big batch reduces each row in one
  pass, so "your output depends on traffic you can't see or control". Prefill versus decode and
  different KV-cache chunking also change the summation order.
- **Thinking Machines' fix, secondhand.** Barry reports that their batch-invariant kernels fixed
  reduction order regardless of batch size "at about a 20% matmul slowdown", and that all 1,000
  completions of one prompt then came back identical (versus **80** different answers before). Across
  devices "there's nothing to pin": an A100, an H100 and a CPU each round their own way, and PyTorch's
  reproducibility notes "promise nothing across platforms".

### Integer storage is not integer arithmetic

Existing int8 methods (SmoothQuant, LLM.int8, OmniQuant) are "**simulated quantization**": matmuls run
in int8 but softmax, RMSNorm, SwiGLU and rotary embeddings drop back to float, and "every one of those
float steps is a place for reduction order to leak back in". DetLLM therefore makes the **entire**
forward pass integer.

### How DetLLM works

- Integer operators come from **I-LLM** (in the I-BERT / I-ViT / I-LLM line of efficiency-motivated
  integer-only transformers). At 8 bits it needs "no fine-tuning, just a calibration pass and two
  closed-form smoothing tricks".
- **Dyadic scales:** each tensor carries a scale `m / 2^k`, so rescaling is an integer multiply plus
  shift with one rounding rule; exp, softmax, RMSNorm and SwiGLU are shift-based integer algorithms,
  and RoPE uses precomputed int16 sine/cosine tables.
- **Batch invariance by construction:** each token is quantized from its own values. K and V use fixed
  scales calibrated offline, and a cached value is quantized once, so prefill and decode see the same
  bits.
- **One hardware-specific function:** only the int8 × int8 → int32 matmul dispatches on hardware
  (`torch._int_mm` on CUDA, a plain int32 matmul on CPU). A `TorchDispatchMode` guard errors on any
  float tensor in the forward pass, and argmax breaks ties toward the lowest token id.
- **Error fixes (footnote):** int8 quantization of QKᵀ was the dominant error; per-channel key ranges
  spanned "about 85×". Rescaling keys per channel and inversely scaling queries took perplexity from
  **44.9 to 25.2** on the ablation subset. DetLLM uses **15-bit** attention probabilities.

### Results

- **One hash versus nine.** The first 64 tokens of Sonnet 18, then 512 greedy tokens, with logits
  chain-hashed at every step, across nine configurations (batch 1; batch 8 with seven random
  co-prompts; split prefill then token-by-token; CPU-only) on A100, H100, AMD EPYC 7J13, Intel Xeon
  8480+ and Apple M1 Pro. All nine int8 runs produce `64430dd985f8`; the nine fp16 runs produce nine
  different hashes, "every pair disagreeing from the first token".
- **Test suite:** a zero-tolerance suite comparing token ids and full int32 logits for exact equality
  (repeats, batches of 2/8/32, prefill vs token-by-token, CUDA vs CPU, a 4k-token context). "All 79
  tests pass on both GPU machines."
- **Divergent logits, matching tokens.** Eight of nine fp16 runs still produce the same 512 tokens. At
  step 0, batch composition shifts logits by at most **0.094** against a top-two gap of **2.66**, "a
  28× cushion". But **45** of 512 steps have a gap under **0.5**, and at step **457** " introduces"
  leads " is" by **0.03** on the A100 while the M1 Pro lands on an exact tie and forks. "Float
  nondeterminism is usually latent, not absent."
- **Quality:** WikiText2 perplexity **20.7170** (int8) vs **20.9549** (fp16, A100); C4 **31.6966** vs
  **31.5696**, "0.4% worse".
- **Speed:** after fusing integer ops, adding CUDA graphs and writing a fused Triton attention kernel,
  A100 batch-1 decode went from **0.8** to **106.3** tok/s (fp16 eager **29.3**); A100 batch 8 reached
  **783.3** (fp16 eager **233.8**). The author flags this as "Not an apples-to-apples comparison": the
  fp16 baseline has no compile or CUDA graphs, and int8 prefill "still runs at about 0.13× fp16".

## Why it matters

The vault repeats the "1,000 prompts, ~80 completions" finding on [[LLM Inference]],
[[Inference Serving Engines]], [[Agentic Testing]] and [[Multi-Turn Evaluation]], and records
batch-invariant execution as an engine setting that conflicts with variable-length speculation on
[[Speculative Decoding]]. This source adds three things: a mechanism-level account that separates
run-to-run determinism from **batch invariance** and from **cross-device reproducibility**; a
secondhand cost figure for batch invariance (about 20% on matmul); and a demonstration that cross-device
bit-exactness is reachable by changing the arithmetic rather than pinning kernel order. It also refines
[[Model Quantization and Efficiency]]'s storage-versus-execution distinction: integer weights do not
imply integer execution, and only the latter buys determinism.

## Tensions / open questions

- **Scale.** One 0.6B model, one prompt for the hash demo, perplexity on two corpora. Larger models,
  other architectures, integer sampling, prefill speed and NPU hardware are listed as open.
- **The guarantee is per artifact.** "The float-to-int conversion isn't itself reproducible", so
  determinism holds for one prepared checkpoint, not for re-quantizing the same weights.
- **Latent versus practical nondeterminism.** On this prompt float drift changed tokens in one of
  nine runs; how often near-ties occur on real workloads is not measured.
- **Secondhand numbers.** The 80-of-1,000 and ~20% slowdown figures are relayed from Thinking Machines
  (Horace He et al., 2025); the original post is not in the vault.
- **Speed baseline.** Final int8 numbers are compared with eager fp16; no optimized fp16 serving
  baseline is shown.
- **Novelty is self-assessed.** The claim to be "the first pipeline built and verified end-to-end" for
  batch, prefill/decode and cross-device invariance is "to my knowledge".
- **Test coverage wording.** The 79 tests are reported as passing "on both GPU machines"; the CPU rows
  rest on the hash table rather than the stated suite.

## Affected pages

- [[Inference Determinism]]
- [[LLM Inference]]
- [[Model Quantization and Efficiency]]
- [[Inference Serving Engines]]
- [[Thinking Machines]]
- [[Multi-Turn Evaluation]]

## Raw capture

- [[knowledge-base/raw/sources/Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]]

## Citations

- Canonical URL: <https://nathan.rs/posts/detllm/> (captured link carried a `utm_source=tldrai`
  parameter, removed here).
- **Author recovered from the capture.** The frontmatter `author` field is empty; the post's own
  citation block reads "Barry, Nathan. ... nathan.rs (Nov 2026)". No web fetch was needed.
- Published November 12, 2026 per the capture; captured November 20, 2026. `source_id` uses the
  publication date.
- Code: <https://github.com/nathanrs/detllm> (linked in the capture; not inspected).

## Related pages

- [[Inference Determinism]]
- [[LLM Inference]]
- [[Model Quantization and Efficiency]]
- [[Inference Serving Engines]]
- [[Thinking Machines]]
- [[Speculative Decoding]]
- [[Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[KV Cache]]
- [[Qwen]]
- [[Mehul Gupta - What is DeepSeek DeepInfer]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
