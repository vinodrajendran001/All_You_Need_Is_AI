---
type: concept
created: 2026-09-03
updated: 2026-09-03
tags:
  - concept
  - inference
  - serving
  - efficiency
source_ids:
  - src-2026-09-02-baseten-efficient-frontier-inference
  - src-2026-08-29-baseten-agentic-kernels-production
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
  - src-2026-09-01-bytebytego-shrink-language-model
status: active
---

# Inference Efficiency Frontier

## Definition

An efficient frontier, borrowed from economics, is the set of optimal combinations available when trading two
valuable outcomes under fixed resources. In inference the usual pair is **latency against throughput** (which
determines cost). [[Philip Kiely - The Efficient Frontier of LLM Inference]] uses it to sort every optimization
by a single question:

- **Tradeoff techniques** move a deployment *along* the frontier — they let you target a point.
- **Frontier-moving techniques** push the whole frontier *out* — they create efficiency that can then be
  allocated to latency, throughput, or both.

Two further exchange axes are named: **quality for throughput** (quantization, distillation, pruning) and
**intelligence for speed** (reasoning level).

## Why it matters

This vault documents most inference techniques in more depth than any single overview does — see
[[Speculative Decoding]], [[Prefill-Decode Disaggregation]], [[KV Cache]], [[GPU Kernel Optimization]],
[[Model Quantization and Efficiency]], [[Distributed Training Parallelism]]. What was missing was a
**classifier**: a way to say what a given optimization actually buys, and therefore whether two techniques are
alternatives or complements.

The distinction has a direct planning consequence. Tradeoff techniques are **allocation decisions** — they
require knowing which outcome the traffic values. Frontier-moving techniques are **investments**, and they
**compound multiplicatively**: doubling from better hardware alongside doubling from better software gives 4×
to spend anywhere.

## Which techniques fall where

**Tradeoffs.** *Batch sizing* is canonical — continuous batching removes queueing delay, but the configured
batch size still sets per-user latency against tokens per GPU and therefore cost per token. *Parallelism
strategy* is directional: Tensor Parallelism favours latency, its expensive all-to-all traffic being fast over
NVLink; Expert Parallelism cuts both ways, with low degree tending to latency and rack-wide EP to throughput;
Attention Data Parallelism replicates attention layers to raise system throughput at the cost of per-request
speed.

**Frontier-moving.** *Kernel and runtime optimization* reduces resources per token and propagates through the
stack. *Disaggregation* lets prefill and decode workers be tuned separately and their ratio matched to real
traffic; in practice it mostly raises throughput while holding latency flat or slightly better.

**Quantization sits in both, and this is the subtle case.** It improves latency *and* throughput together, so
it moves the serving frontier out — while introducing a **new quality-versus-efficiency frontier**. What was a
frontier-moving technique on one axis is a tradeoff on another. The vault's fuller account of the mechanism is
[[ByteByteGo - How to Shrink a Language Model Without Making it Too Dumb]] and
[[Model Quantization and Efficiency]].

## The frontier is jagged

The most practically useful claim in the source, and the least headline-worthy: the frontier is **not a smooth
curve**. Small configuration changes produce large outcome changes, and **the cutoff points are unintuitive
and must be discovered empirically through sweeps**.

The quality-versus-efficiency frontier is described as *particularly* jagged — large serving gains for little
or no quality loss are available, especially with the microscaling formats **MXFP4** and **NVFP4**.

Two consequences. Operationally, there is no analytic shortcut to an operating point; you sweep or you guess.
Epistemically, a published single-configuration benchmark number describes **a point someone chose**, which is
a serving-side instance of the concern on [[Serving Benchmarks and Goodput]] and [[Benchmark Optimization]].

## A technique can change category

Speculative decoding is the documented case. It used to be a tradeoff technique — speculation was expensive,
sequences were short, acceptance rates were low, and it was viable only at small batch sizes. With
**EAGLE-3, DSpark and DFlash**, it now yields efficiency from **skipped forward passes** on top of raw latency
reduction, which is a genuine reduction in work rather than a reallocation of it. It still competes with the
main loop for resources and so still caps maximum batch size. Code generation benefits most, because output
sequences are relatively predictable.

This partially revises the framing on [[Speculative Decoding]], which records speculation as spending headroom
that could be spent elsewhere. Both readings are now on record, and the disagreement is real rather than
terminological: whether skipped forward passes count as new efficiency or as better-spent headroom depends on
whether the drafting cost is counted against the budget.

## Headroom depends on how mature the domain already is

[[Baseten - Agentic Kernels in Production]] supplies a clean natural experiment on how much frontier-moving is
actually available. The same agentic framework delivered **42.3% end-to-end latency reduction on Qwen-Image**
and **15.2% on FLUX.2**, but only about **5.5% more tok/s** when applied to LLMs — because, in the authors'
words, LLM *"kernel implementations are considerably more mature and leave less headroom for improvement."*

This is the best predictor the vault has for where optimization effort pays: **inversely to how much human
optimization a domain has already absorbed**. It also cautions against reading a large percentage gain as
evidence of a strong method, since the size of the win is mostly a fact about the baseline.

## The frontier is not the whole bill

Frontier reasoning optimizes the cost of a token, which is necessary and not sufficient.
[[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]] shows the demand side
moving faster than the supply side: because the model is stateless, history is re-sent every turn, and in an
agent loop **each tool result re-runs the whole pipeline** — 20 tool calls means the earliest messages are
paid for 20 times, and a 2,000-token instruction block across 200 calls becomes **400,000 input tokens before
any work happens**.

No position on the serving frontier survives a 200× multiplier on the input. Prefix caching is the lever that
straddles both worlds — cached prefixes bill at roughly **1/10 of the input rate**, which makes "stable content
at the top, changing content at the bottom" an economic layout rule. See [[KV Cache]] and
[[Context Engineering]].

## Open questions

- The primary source is a **vendor** post with no measurements — every claim is directional, and the 4×
  compounding example is illustrative arithmetic rather than a result.
- Does quantization genuinely belong in both categories, or is calling it frontier-moving an artifact of
  treating latency-throughput as *the* frontier and quality as an externality?
- If operating points must be found by sweeps, what does the sweep cost, and who can afford one? This
  advantages large serving operators in a way nobody quantifies.
- Where is the boundary between the frontier and the workload? Reasoning effort and context layout are neither
  tradeoff nor frontier-moving in the serving sense, yet they dominate real bills.
- Does the maturity-headroom relationship hold outside kernels?

## Related pages

- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
- [[Baseten - Agentic Kernels in Production]]
- [[ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- [[LLM Inference]]
- [[Speculative Decoding]]
- [[Prefill-Decode Disaggregation]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[GPU Kernel Optimization]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[Distributed Training Parallelism]]
- [[Mixture of Experts]]
- [[Reasoning Effort Control]]
- [[Baseten]]
