---
type: source-summary
created: 2026-09-03
updated: 2026-09-03
source_id: src-2026-08-31-bytebytego-chatbot-request-lifecycle
source_title: "What Happens Inside an AI Chatbot Between Enter and the First Word"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/what-happens-inside-an-ai-chatbot
tags:
  - source/summary
  - topic/inference
  - topic/context-engineering
source_ids:
  - src-2026-08-31-bytebytego-chatbot-request-lifecycle
status: active
---

# ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word

## Summary

A stage-by-stage trace of the roughly **twelve** things that happen between pressing Enter and seeing the
first token. The value of the source is that it puts numbers on stages the vault has treated separately —
document assembly, safety classification, tokenization, batching, prefill, decode, KV caching, streaming, and
the tool loop — and shows how the costs compose.

The organising observation is that the model is **stateless**: nothing persists between turns, so the entire
conversation is re-sent and re-processed every time, and most of the bill is input.

## Key claims

- **Two products on the same model give different answers**, because what reaches the model is an assembled
  document — system prompt, tool definitions, memory, retrieved documents, history, new message. This is
  [[Context Engineering]] stated as a serving fact.
- **Statelessness compounds quadratically-ish in practice.** The worked progression is
  **1,100 → 1,300 → 1,500 tokens**, reaching roughly **4,900 by turn 20**. Input dominates spend.
- **Safety classification has a measurable, published-generation price.** An earlier production generation of
  input classifier cost about **24% extra compute** and added **+0.38 percentage points of false refusals**;
  the cascade design that replaced it brings this to roughly **1% compute** and **0.05pp**.
- **Tokenization is not linguistically neutral.** Token counts for the same meaning differ by
  **up to 15×** across translations, so speakers of some languages get materially less usable context and pay
  more for it. Rule of thumb: about **¾ of a word per token**.
- **Continuous batching is worth up to 23× throughput** over naive fixed batching.
- **Temperature 0 does not give determinism.** Because numerics depend on batch composition, **1,000
  identical prompts produced about 80 distinct completions**.
- **Prefill and decode are different machines.** Prefill is parallel and **compute-bound** — it is the pause.
  Decode is sequential and **memory-bound** — it is the typing. Latency splits into **TTFT** and **TPOT**,
  with total ≈ TTFT + TPOT × length.
- **KV cache is the memory problem.** A 70B model with an 8k conversation needs **a few GB per request**.
  Naive contiguous reservation wasted **60–80%** of that memory; **paged blocks cut waste below 4%** and
  delivered **2–4× throughput**.
- **Prefix caching has a price and a layout consequence.** Cached prefixes are billed at roughly **1/10 of
  the input rate** and expire after minutes — which makes "**stable content at the top, changing content at
  the bottom**" a billing decision, not a style preference.
- **Streaming exists because reading is slow** (~6 tokens/second), but it forecloses retraction: an output
  guard cannot un-display a word already shown.
- **Tools turn the line into a loop, and the loop re-pays for everything.** Each tool result re-runs the
  pipeline; **20 calls means the earliest messages are paid for 20 times**, and a 2,000-token instruction
  block across 200 calls becomes **400,000 input tokens before any work is done**.

## Why it matters

Three items here are new to this vault and each is load-bearing.

**The classifier tax is a number for a cost the vault previously discussed only qualitatively.** Safety
filtering is usually argued about in terms of false refusals; this gives both axes at once, and shows a
cascade recovering most of both.

**Batch-composition nondeterminism** undercuts an assumption running through the vault's evaluation pages:
that temperature 0 gives a reproducible baseline. If identical prompts yield ~80 distinct completions, then
single-run evaluation is measuring the serving stack as much as the model. This connects directly to the
`pass@k` versus `pass^k` distinction in [[Paolo Perrone - What is Agentic Testing]].

**The tool-loop multiplier** reframes prompt bloat. A 2,000-token block is negligible once and ruinous 200
times, which makes instruction-block size an agent-architecture decision rather than a prompt-writing one.

## Tensions / open questions

- **Provenance is the weak point.** The post carries ByteByteGo's "based on publicly shared details"
  disclaimer, and several of the strongest numbers — 24% / 0.38pp, 23×, 60–80% → 4%, ~80 completions — are
  presented **without attribution to a specific paper, vendor or measurement**. They are consistent with
  published work the vault holds elsewhere, but should be treated as illustrative until traced.
- The 15× tokenization spread is given without naming the language pair or tokenizer, so the magnitude is
  unanchored even though the direction of the effect is well established.
- If nondeterminism is a function of batch composition, is it eliminable by batch-invariant kernels, or only
  reducible? The post raises the effect and not the remedy.
- Prefix-cache expiry "after minutes" is stated as a general property, but it is a per-provider policy.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[LLM Inference]]
- [[KV Cache]]
- [[Context Engineering]]
- [[Inference Serving Engines]]
- [[ByteByteGo]]

## Related pages

- [[Prefill-Decode Disaggregation]]
- [[Inference Efficiency Frontier]]
- [[Philip Kiely - The Efficient Frontier of LLM Inference]]
- [[Paolo Perrone - What is Agentic Testing]]
- [[Agentic Loop]]
- [[Serving Benchmarks and Goodput]]
- [[Multi-Turn Evaluation]]

## Citations

- Raw capture: [[2026-08-31 ByteByteGo - What Happens Inside an AI Chatbot Between Enter and the First Word]]
- Source: <https://blog.bytebytego.com/p/what-happens-inside-an-ai-chatbot>
