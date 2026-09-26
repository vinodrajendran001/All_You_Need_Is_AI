---
type: social-post
created: 2026-09-25
updated: 2026-09-26
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
topics:
  - selective computation
  - agentic OCR
  - multimodal serving
  - routing gates
covers_from: 2026-09-18
covers_through: 2026-09-25
status: ready
---

# 2026-09-25 Keep the Expensive Model On Call

## LinkedIn post

Imagine an AI has to answer one question hidden somewhere inside a 12,013-page financial archive.

The expensive approach is simple: send every page to a powerful visual model. That model can understand tables, charts, and messy scans—but most pages will not contain the answer, so you pay the highest cost 12,013 times.

Jerry Liu of LlamaIndex reports a two-stage alternative. A cheap parser scanned all 12,013 pages in 32 seconds. For one FinanceBench question, it shortlisted just two pages. Only those two went to the more expensive visual model for close inspection.

This pattern is called just-in-time visual reading: use a cheap scout for broad search, then call the specialist only when the evidence says it may be needed.

The key insight is not "small models are better." The saving comes from routing. The expensive model does less work because the first stage narrows the field.

NVIDIA reports a similar idea at the server level. A multimodal system has one stage that processes images and another that generates text. Running those stages on hardware suited to each one let a tested setup serve 70% more traffic while keeping the delay between generated tokens below 100 milliseconds.

But routing creates a new failure point. If the cheap parser misses the relevant page, the specialist never sees it. And the server split was not always faster: in one configuration, the end-to-end result moved from an 11.8% gain to a 2.5% loss as generated answers grew from 128 to 2,048 tokens.

So a complete design needs four things: a cheap first pass, a rule for deciding when confidence is low, a fallback that invokes the specialist, and end-to-end measurement of missed cases and total cost.

The lesson is not "always use the cheap model first." It is: put expensive computation behind evidence, then test the gate as rigorously as the specialist behind it.

Where in your AI system are you paying specialist prices before checking whether specialist work is needed?

(Sources: Jerry Liu/LlamaIndex, "Just-in-Time Agentic OCR" — https://www.llamaindex.ai/blog/just-in-time-agentic-ocr; Tanya Lenz/NVIDIA, "When to Use Encode-Prefill-Decode Disaggregation" — https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/)

#AIEngineering #AgenticAI #MultimodalAI #InferenceOptimization #DocumentAI

## X post

<!-- URLs count as 23 characters on X regardless of length; counts below include that. -->

**A) Standalone** (277 chars):

```
An AI searched 12,013 pages in 32s, then sent only 2 pages to a costly visual model for one question.

That saves work—but creates a risk: if the cheap first pass misses the right page, the expert never sees it.

Optimize the gate, not just the expert.

https://www.llamaindex.ai/blog/just-in-time-agentic-ocr
```

**B) Thread:**

1. (217 chars)
```
Imagine asking an AI one question about a 12,013-page financial archive.

The expensive approach sends every page to a powerful visual model. Most pages will not contain the answer, but you pay to inspect all of them.
```

2. (228 chars)
```
Jerry Liu/LlamaIndex reports a two-stage alternative: a cheap parser scanned all 12,013 pages in 32 seconds. For one question, it shortlisted 2 pages for the visual model to inspect closely.

This is just-in-time visual reading.
```

3. (215 chars)
```
Why it saves work: the cheap stage performs broad search; the expensive specialist handles only likely evidence.

The improvement comes from routing fewer cases to the costly model—not from making that model faster.
```

4. (251 chars)
```
NVIDIA reports the same principle at server level. It separated image processing from text generation and assigned each stage suitable hardware.

In one setup, that served 70% more traffic while keeping the delay between generated tokens below 100 ms.
```

5. (232 chars)
```
But the gate becomes the new failure point. If the cheap parser misses the relevant page, the visual model cannot recover.

And one NVIDIA configuration moved from +11.8% to -2.5% end-to-end as outputs grew from 128 to 2,048 tokens.
```

6. (238 chars)
```
Complete design: a cheap first pass, a confidence rule, a fallback for uncertain cases, and end-to-end measurement of misses and cost.

Put expensive compute behind evidence. Test the gate.

https://www.llamaindex.ai/blog/just-in-time-agentic-ocr https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/
```

**Ship: B.** The thread supplies the scenario before the numbers, explains why routing saves work, translates
the serving metric into plain language, and completes the design with a fallback and measurement rule. The
standalone remains a complete miniature of the same idea. No hashtags on X.

## Hook variants

1. **The situation.** "Imagine an AI has to answer one question hidden somewhere inside a 12,013-page financial archive."
2. **The result.** "An AI scanned 12,013 pages, then sent only two to its expensive visual model."
3. **The principle.** "The cheapest AI call is often the expensive model call you correctly decide not to make."

**Recommended:** 1 for LinkedIn. It gives a non-specialist reader the problem before asking them to care about
the architecture. Variant 2 is the better X opening because the number fits beside the mechanism. Variant 3 is
memorable but incomplete without explaining how the decision is made.

## Why this topic

Window: 2026-09-18 -> 2026-09-25. One ten-source ingest and its lint pass, taking the controlled set from
262 to 272 source IDs.

| Candidate | Clarity | Complete | Surprise | Concrete | Reach | Fresh | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Route expensive work only after a cheap evidence pass** | 5 | 5 | 5 | 5 | 5 | 5 | **30** |
| Quantization can make encoder disaggregation more valuable | 3 | 4 | 5 | 5 | 3 | 5 | 25 |
| Build the parity harness before translating legacy code | 5 | 5 | 4 | 5 | 5 | 5 | 29 |
| AI changed optimization search cost, not the techniques | 5 | 4 | 4 | 5 | 5 | 5 | 28 |
| Typed output removes invalid shapes, not semantic errors | 5 | 4 | 4 | 4 | 5 | 3 | 25 |

The original draft stacked document OCR, multimodal serving, and live voice into 250 words. Each example was
accurate, but the reader had to understand three systems and several unexplained metrics before reaching the
takeaway. That is precisely the feedback this revision addresses.

The public post now uses document search as the primary worked example and NVIDIA serving as one supporting
example. The voice system was removed. The selected angle passes the new clarity and completeness gates because
the reader sees the problem, mechanism, failure mode, and complete operational design in sequence.

## Reader check

1. **Problem:** An AI system is paying a powerful visual model to inspect many pages that are irrelevant to one question.
2. **Single claim:** A cheap first pass can route only likely cases to expensive computation, reducing unnecessary work.
3. **Example:** A reported 12,013-page scan shortlisted two pages for visual inspection; NVIDIA reports a supporting server-level result.
4. **Why it happened:** The expensive stage processes fewer cases; it was not made intrinsically faster.
5. **Failure boundary:** A routing miss hides evidence from the specialist, and split serving can regress on different workloads.
6. **Action:** Build a confidence rule, fallback path, and end-to-end measurement of misses and total cost.

**Terminology check:** "visual model" is explained by function; "multimodal" is immediately unpacked as image
processing plus text generation. EPD, ITL, SLO, OCR, prefill, and decode do not appear unexplained in the public
body. FinanceBench appears only as the name of the reported question, and understanding it is unnecessary.

**Narrative check:** situation -> worked example -> mechanism -> supporting example -> limitation -> complete
design -> takeaway. The conclusion is complete before the engagement question.

## Fact check

| Claim in post | Traced to | Verdict |
|---|---|---|
| 12,013 pages parsed in 32 seconds; two pages sent to visual OCR for one question | [[Jerry Liu - Just-in-Time Agentic OCR]], Key claims; [[Just-in-Time Agentic OCR]], Current synthesis | Verbatim author-reported FinanceBench example |
| A cheap-pass miss can hide the relevant page from the stronger parser | Same pages, caveats/current synthesis | Preserved as the central failure mode |
| Multimodal serving separates image encoding from text generation | [[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]], Summary | Mechanism translated into plain language |
| One heterogeneous setup served 70% more traffic at an inter-token delay under 100 ms | Same, Key claims; [[Prefill-Decode Disaggregation]], multimodal section | Condition retained; metric translated rather than abbreviated |
| Output length 128 -> 2,048 changed one configuration's end-to-end result from +11.8% to -2.5% | Same pages | Verbatim; scoped to one configuration |
| Sources are author/vendor reports rather than universal benchmarks | Both source summaries, tensions/caveats | Public prose consistently says "reports" and "in one setup/configuration" |
| Attribution and URLs | Source-summary metadata | Verified |

**Cut during the clarity revision:**

- The GPT-Live example was removed. It was relevant but forced a third architecture into a post that only needed
  one primary and one supporting example.
- EPD, ITL, SLO, prefill, and decode were removed from public prose. Where the underlying detail mattered, it was
  translated into image processing, text generation, and delay between generated tokens.
- "Hospital triage" was removed. It was a reasonable analogy, but the revised cheap-scout/specialist explanation
  does the causal work more directly.

**Previously cut during fact-check:**

- "The agent reduced OCR cost by 99.98%" was unsupported because the source gives no all-pages visual-model baseline.
- "EPD is 70% faster" confused throughput at a shared latency target with latency reduction.
- "Selective compute is always cheaper" was contradicted by the negative longer-output condition.

**Compression and comprehension check (X):**

- Post 1 supplies the full situation before any architecture claim.
- Posts 2 and 3 separate what happened from why it saves work.
- Post 4 translates the serving condition rather than using ITL/SLO abbreviations.
- Post 5 carries both routing failure and the negative workload result.
- Post 6 completes the design; the thread does not end at the caveat.
- All links and attributions survive, and all seven blocks remain at or below 280 characters.

## Attribution

- **Jerry Liu**, *Just-in-Time Agentic OCR* -
  https://www.llamaindex.ai/blog/just-in-time-agentic-ocr
- **Tanya Lenz**, *When to Use Encode-Prefill-Decode Disaggregation to Accelerate Multimodal Model Serving* -
  https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/

## Hashtags

**LinkedIn:** `#AIEngineering #AgenticAI #MultimodalAI #InferenceOptimization #DocumentAI`

**X:** none.

## Related pages

- [[Just-in-Time Agentic OCR]] - spine page; query-time routing of expensive visual parsing
- [[Jerry Liu - Just-in-Time Agentic OCR]] - source for the primary example
- [[Prefill-Decode Disaggregation]] - supporting server-level architecture
- [[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]] - source for the serving figures
- [[Post Archive]] - post ledger and cooldowns
