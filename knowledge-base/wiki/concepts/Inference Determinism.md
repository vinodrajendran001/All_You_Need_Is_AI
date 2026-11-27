---
type: concept
created: 2026-11-20
updated: 2026-11-27
tags:
  - concept
  - inference
  - determinism
  - reproducibility
  - evaluation
source_ids:
  - src-2026-11-12-nathan-barry-detllm-integer-inference
  - src-2026-10-20-gupta-deepseek-deepinfer
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-11-11-cam-pedersen-derive-kernels
  - src-2026-11-20-ankit-gupta-vibecoding-inference-chip
status: active
---

# Inference Determinism

## Definition

**Inference determinism** is the property that the same model, prompt and decoding settings produce the
same output bits. It has at least three levels, which the vault's sources keep separate:

1. **Run-to-run determinism** — the same kernel on the same input returns the same bits. Most inference
   kernels already have it.
2. **Batch invariance** — a request's output does not depend on what else is batched with it, on how
   prefill is chunked, or on how the KV cache is split.
3. **Cross-device reproducibility** — the same output on different GPUs, CPUs and vendors.

Temperature 0 (greedy decoding) guarantees none of these; it only removes sampling randomness.

## Why it matters

Evaluation, debugging and RL all assume a re-run is the same experiment. The vault records that **1,000
identical prompts at temperature 0 produced roughly 80 distinct completions**
([[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]; attributed by
[[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]] to
[[Thinking Machines]], Horace He et al., 2025 — secondhand in both cases). If the serving stack injects
that variance, a single-run score partly measures the stack; see [[Agentic Testing]] and
[[Multi-Turn Evaluation]]. Barry also relays Thinking Machines' point that a bitwise-identical sampler and
trainer makes RL "truly on-policy".

## Current synthesis

**The main cause is reduction order, not thread races.** Atomic adds can race, but that is "mostly not
what goes on in an LLM forward pass". Floating-point addition is not associative. Libraries such as
cuBLAS select kernels by shape, so a small batch may split a reduction that a large batch performs in
one pass; prefill versus decode and KV-cache chunking change the order too. Barry:
"your output depends on traffic you can't see or control."

**Three ways to buy determinism, at different prices.**

- *Pin the order (batch-invariant kernels).* Thinking Machines' kernels made all 1,000 completions
  identical "at about a 20% matmul slowdown" (secondhand via Barry). This works on one GPU with those
  kernels only. DeepSeek's DeepInfer exposes batch invariance as an engine setting, and in its stated
  NVIDIA deterministic configuration **variable-length MTP decoding is disabled**
  ([[Mehul Gupta - What is DeepSeek DeepInfer]]; see [[Speculative Decoding]] and
  [[Inference Serving Engines]]). The size of that trade is unmeasured.
- *Change the arithmetic.* DetLLM runs every operation of Qwen3-0.6B in exact integer arithmetic, with
  only the int8 × int8 → int32 matmul hardware-specific. Nine configurations across A100, H100 and three
  CPUs give **one** logit hash for int8 and **nine** for fp16. WikiText2 perplexity is **20.7170** against
  **20.9549** for fp16. The guarantee is per prepared artifact, and the evidence is one 0.6B model.
- *Gate on it as an engineering check.* [[Cam Pedersen - Don't Write Kernels, Derive Them]] treats
  "bitwise-identical batched decode" as one of its engine's accuracy gates. It reports that a block-split
  RMSNorm sum of squares split **256** ways pushed KL divergence at 3k tokens over the engine's bar, while
  a **1,024**-way split came in lower than the serial sum's — "Precision is a schedule here too."
- *Make it the contract for a whole optimization campaign.* [[Ankit Gupta - Vibecoding an Inference Chip]]
  had a coding agent optimize an FPGA decoder for a ternary-weight model under a bit-exact rule against
  a pinned CPU reference. The rule cost speed: the agent rejected all five numerics shortcuts in an
  outside design, among them lower-precision activations, an 8-bit KV cache and online softmax, because
  each changes the output bits, which is "where their design got its efficiency". On one 8-chat ×
  3-turn benchmark the final FPGA image matched the reference on 24/24 turns. Two cheaper T4 GPU ports
  matched 1/24 and 0/24, though the author says they "are pretty close in practice". Exactness here
  means agreement with one reference implementation for one model, not determinism across hardware in
  general.

**Integer storage is not integer arithmetic.** Standard int8 quantization (SmoothQuant, LLM.int8,
OmniQuant) is "simulated": the float steps between matmuls reintroduce order dependence. See
[[Model Quantization and Efficiency]].

**Nondeterminism is often latent.** In DetLLM's demo, eight of nine fp16 runs still produced the same 512
tokens because the drift stayed below the top-two gap at every step. At step 0 batch composition
shifted logits by at most **0.094** against a gap of **2.66**, a cushion Barry calls "unusually
generous": **45** of 512 steps had a gap under **0.5**, and one run forked at step **457** on an exact
tie. Longer generations give more chances to fork.

## Open questions

- What does batch invariance cost end to end, rather than per matmul, and on which workloads is it worth
  paying — evaluation, regulated decisions, incident reproduction, RL rollouts?
- Can integer-only inference scale beyond a 0.6B model with acceptable quality and prefill speed?
  DetLLM's int8 prefill still runs at about 0.13× fp16.
- How often do near-ties change outputs on real workloads, as opposed to one prompt?
- Is variable-length speculation fundamentally incompatible with batch invariance, or only in
  DeepInfer's configuration?
- DetLLM's float-to-int conversion is not itself reproducible, so its guarantee is tied to one
  prepared artifact. Who owns the canonical artifact?

## Related pages

- [[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[Speculative Decoding]]
- [[Model Quantization and Efficiency]]
- [[Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[Thinking Machines]]
- [[Mehul Gupta - What is DeepSeek DeepInfer]]
- [[Cam Pedersen - Don't Write Kernels, Derive Them]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- [[Reinforcement Learning]]
- [[Ankit Gupta - Vibecoding an Inference Chip]]
