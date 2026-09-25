---
type: source-summary
created: 2026-09-25
updated: 2026-09-25
source_id: src-2026-09-21-liu-just-in-time-agentic-ocr
source_title: "Just-in-Time Agentic OCR"
source_author: Jerry Liu
source_url: https://www.llamaindex.ai/blog/just-in-time-agentic-ocr
tags: [source/summary, retrieval, vision-language, document-processing]
source_ids: [src-2026-09-21-liu-just-in-time-agentic-ocr]
status: active
---

# Jerry Liu - Just-in-Time Agentic OCR

## Summary

Jerry Liu proposes a two-pass document-agent pipeline: run cheap layout-aware extraction over the
whole data room, retrieve candidate pages, then invoke expensive vision-language OCR only where the
task needs it.

## Key claims

- On **84 FinanceBench filings / 12,013 pages**, LiteParse reportedly completed the first pass in
  **32 seconds** on a laptop; targeted VLM OCR then processed **2 pages**.
- A complexity scan flagged **2,605 pages (21.7%)**, including 253 image pages and 75 with no text layer.
- The pattern targets ad-hoc collections of roughly **10-100 documents**; large offline corpora or
  mandatory batch extraction favor up-front processing and caching.
- Vendor-reported ParseBench results put LlamaParse at **87.0 and 1.25 cents/page**; those comparisons
  are not independent evidence.

## Why it matters

Document agents can allocate visual parsing by query rather than by corpus. The first pass becomes a
recall-sensitive routing layer whose misses can prevent the accurate second pass from ever running.

## Tensions and caveats

This is first-party LlamaIndex advocacy. Performance, pricing, and benchmark comparisons are
vendor-reported, and the FinanceBench run is not independently reproduced. The method fails when
cheap extraction makes the relevant page unretrievable.

## Raw capture

- [[2026-09-21 Jerry Liu - Just-in-Time Agentic OCR]]

## Affected pages

- [[Just-in-Time Agentic OCR]]
- [[Retrieval-Augmented Generation]]
- [[Vision-Language Grounding]]

## Related pages

- [[Approximate Nearest-Neighbor Search]]
- [[Search-Augmented Language Models]]
- [[Agent Planning]]
