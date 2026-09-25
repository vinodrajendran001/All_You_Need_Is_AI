---
type: social-post
created: 2026-09-25
updated: 2026-09-25
tags:
  - post
platforms:
  - linkedin
  - x
pages_used:
  - "[[Just-in-Time Agentic OCR]]"
  - "[[Jerry Liu - Just-in-Time Agentic OCR]]"
  - "[[Prefill-Decode Disaggregation]]"
  - "[[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]]"
  - "[[Real-Time Voice AI]]"
  - "[[ByteByteGo - How OpenAI Built GPT-Live]]"
topics:
  - selective computation
  - agentic OCR
  - multimodal serving
  - full-duplex voice
covers_from: 2026-09-18
covers_through: 2026-09-25
status: ready
---

# 2026-09-25 Keep the Expensive Model On Call

## LinkedIn post

Three unrelated AI systems arrived at the same architecture: keep the expensive model on call, not on every case.

Jerry Liu/LlamaIndex reports that a cheap parser scanned 12,013 pages in 32 seconds. For one FinanceBench question, the agent sent only 2 pages to visual OCR.

NVIDIA reports a similar move in multimodal serving: separate vision encoding from prefill and decode. One heterogeneous setup served 70% more traffic at the same ITL-under-100-ms SLO.

ByteByteGo's account of OpenAI GPT-Live applies the pattern to time. The live voice loop keeps listening and speaking while slower reasoning and tools run asynchronously.

It is hospital triage for computation: use a cheap first pass, then call the specialist when the case warrants it. But triage creates its own failure mode. If the first pass misses the signal, the specialist never sees the case.

The caveat matters. These are vendor-authored or secondary reports, not universal benchmarks. In NVIDIA's test, as output length rose from 128 to 2,048, colocated EPD's end-to-end gain moved from +11.8% to -2.5%.

The practical rule: route expensive work on demand, then measure routing recall and fallback cost—not only specialist accuracy.

Where in your AI stack are you still paying specialist prices for routine cases?

(Sources: Jerry Liu/LlamaIndex; Tanya Lenz/NVIDIA; ByteByteGo reporting on OpenAI GPT-Live.)

#AIEngineering #AgenticAI #MultimodalAI #InferenceOptimization #DocumentAI

## X post

<!-- URLs count as 23 characters on X regardless of length; counts below include that. -->

**A) Standalone** (276 chars):

```
Don't run your most expensive model on every case.

Jerry Liu/LlamaIndex reports scanning 12,013 pages in 32s, then sending only 2 to visual OCR. But if the cheap pass misses a page, the specialist never sees it.

The new bottleneck is routing recall.

https://www.llamaindex.ai/blog/just-in-time-agentic-ocr
```

**B) Thread:**

1. (217 chars)
```
Three unrelated AI systems reached the same design: put the expensive stage on call, not on every case.

The useful optimization wasn't making every step cheaper. It was deciding when the costly specialist should run.
```

2. (212 chars)
```
Jerry Liu/LlamaIndex reports a cheap parser scanning 12,013 pages in 32 seconds. For one FinanceBench question, the agent sent only 2 pages to visual OCR.

That is a routing architecture, not merely an OCR trick.
```

3. (218 chars)
```
NVIDIA reports the same pattern in multimodal serving: split vision encoding from prefill/decode. One heterogeneous setup served 70% more traffic at the same ITL-under-100-ms SLO.

But the win depended on the workload.
```

4. (218 chars)
```
As output length rose from 128 to 2,048, colocated EPD's end-to-end gain moved from +11.8% to -2.5%.

And in query-time OCR, a bad cheap parse can hide the relevant page forever. Triage creates a new recall bottleneck.
```

5. (261 chars)
```
GPT-Live adds a third case: keep the live voice loop separate from slower reasoning and tools.

Rule: route expensive work on demand. Measure routing misses and fallback cost.

Sources: Jerry Liu/LlamaIndex, Tanya Lenz/NVIDIA, ByteByteGo
https://www.llamaindex.ai/blog/just-in-time-agentic-ocr
```

**Ship: B.** The thread carries all three systems, the EPD crossover, and the routing-recall caveat.
The standalone is the fallback: it teaches the mechanism through the OCR example without importing
the vendor benchmark. No hashtags on X.

## Hook variants

1. **The pattern.** "Three unrelated AI systems arrived at the same architecture: keep the expensive model on call, not on every case."
2. **The number.** "A document agent scanned 12,013 pages, then sent only 2 to visual OCR."
3. **The analogy.** "The next AI architecture pattern looks less like a bigger brain and more like hospital triage."

**Recommended:** 1 for LinkedIn because the cross-source convergence is the vault's contribution.
Variant 2 is stronger for X because it teaches the mechanism immediately. The analogy belongs in the
body, where its failure mode—missed triage prevents specialist review—does useful explanatory work.

## Why this topic

Window: 2026-09-18 → 2026-09-25. The window contains one ten-source ingest and its lint pass, taking
the controlled source set from 262 to 272 IDs.

| Candidate | Surprise | Concrete | Reach | Fresh | Total |
|---|---:|---:|---:|---:|---:|
| **Keep the expensive stage on call: selective compute across OCR, serving, and voice** | 5 | 5 | 5 | 5 | **20** |
| Quantization can make encoder disaggregation more valuable by moving the bottleneck | 5 | 5 | 4 | 5 | 19 |
| Build the parity harness before asking agents to translate legacy code | 4 | 5 | 5 | 5 | 19 |
| AI changed optimization search cost, not the optimization techniques | 4 | 5 | 5 | 5 | 19 |
| Typed output removes invalid shapes, not semantic errors | 4 | 4 | 5 | 3 | 16 |

The winning angle is derived across three sources. None states the general pattern across document
retrieval, multimodal serving, and live voice. It also avoids all active cooldown spines. The typed
decision angle scored lower on freshness because it already appears in the archive's unposted
candidates; the serving-normalization neighbourhood is also still in cooldown.

## Fact check

| Claim in post | Traced to | Verdict |
|---|---|---|
| 12,013 pages parsed in 32 seconds; 2 pages sent to VLM OCR for one question | [[Jerry Liu - Just-in-Time Agentic OCR]], Key claims; [[Just-in-Time Agentic OCR]], Current synthesis | Verbatim author-reported FinanceBench example |
| A cheap-pass miss can hide the relevant page from the stronger parser | Same pages, caveats/current synthesis | Preserved as the central failure mode |
| EPD separates vision encoding from prefill/decode | [[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]], Summary | Verbatim mechanism |
| Heterogeneous EPD served 70% more traffic at the same ITL-under-100-ms SLO | Same, Key claims; [[Prefill-Decode Disaggregation]], multimodal section | Verbatim tested condition |
| OSL 128→2,048 changed colocated E2E gain from +11.8% to -2.5% | Same pages | Verbatim; workload dependency retained |
| GPT-Live separates the live voice loop from asynchronous reasoning and tools | [[ByteByteGo - How OpenAI Built GPT-Live]], Summary/Key claims; [[Real-Time Voice AI]] | Attributed to ByteByteGo's secondary account |
| Sources are vendor-authored or secondary rather than universal benchmarks | All three source summaries, Tensions and caveats | Stated explicitly in LinkedIn; thread uses “reports” and includes the EPD reversal |
| Attribution | Source-summary `source_author` and `source_url` fields | Verified |

**Cut during fact-check:**

- "The agent reduced OCR cost by 99.98%" was cut. Two pages were visually parsed for one question,
  but the source does not report a comparable all-pages VLM cost or establish that every page would
  otherwise have been processed.
- "EPD is 70% faster" was cut. The source reports 70% more traffic at a shared inter-token-latency
  SLO, not a 70% latency reduction.
- "GPT-Live proves the pattern in production" was cut. ByteByteGo reports the architecture but
  supplies no public production latency, concurrency, quality, or reliability dataset.
- "Selective compute is always cheaper" was cut. EPD regressed for one longer-output condition, and
  routing adds its own recall and fallback costs.

**Compression check (X variant):**

- Standalone attributes the OCR figures to Jerry Liu/LlamaIndex and retains the first-pass miss.
- Thread post 3 says NVIDIA "reports" the result and keeps the shared SLO beside the 70% figure.
- Thread post 4 carries the negative EPD crossover and OCR recall failure; neither qualifier was
  dropped for brevity.
- Thread post 5 attributes all three sources and states the operational rule without claiming a
  universal speedup.
- Character counts were computed with URLs at X's fixed 23 characters. All six blocks are at or below 280.

## Attribution

- **Jerry Liu**, *Just-in-Time Agentic OCR* -
  https://www.llamaindex.ai/blog/just-in-time-agentic-ocr
- **Tanya Lenz**, *When to Use Encode-Prefill-Decode Disaggregation to Accelerate Multimodal Model Serving* -
  https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/
- **ByteByteGo**, *How OpenAI Built GPT-Live* -
  https://blog.bytebytego.com/p/how-openai-built-gpt-live

## Hashtags

**LinkedIn:** `#AIEngineering #AgenticAI #MultimodalAI #InferenceOptimization #DocumentAI`

**X:** none.

## Related pages

- [[Just-in-Time Agentic OCR]] - spine page; query-time routing of expensive visual parsing
- [[Jerry Liu - Just-in-Time Agentic OCR]] - source for the FinanceBench example
- [[Prefill-Decode Disaggregation]] - workload-dependent serving topology
- [[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]] - source for the EPD figures
- [[Real-Time Voice AI]] - continuous live path separated from asynchronous work
- [[ByteByteGo - How OpenAI Built GPT-Live]] - source for the GPT-Live architecture
- [[Post Archive]] - post ledger and cooldowns
