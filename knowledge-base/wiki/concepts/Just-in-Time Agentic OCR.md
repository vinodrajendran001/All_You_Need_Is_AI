---
type: concept
created: 2026-09-25
updated: 2026-09-25
tags:
  - document-processing
  - retrieval
  - vision-language
source_ids:
  - src-2026-09-21-liu-just-in-time-agentic-ocr
status: active
---

# Just-in-Time Agentic OCR

## Definition

Just-in-time agentic OCR uses a cheap first-pass parser across a document collection, retrieves pages
relevant to the current task, and applies expensive visual document understanding only to that subset.

## Why it matters

Uniform VLM parsing spends maximum cost before the query reveals which pages matter. Query-time
escalation can retain visual accuracy where needed while making ad-hoc data rooms interactive.

## Current synthesis

[[Jerry Liu - Just-in-Time Agentic OCR]] reports a first pass over 84 FinanceBench filings and 12,013
pages in 32 seconds, followed by VLM parsing of only two pages for one question. The architecture is
a cascade: extraction, retrieval, complexity or relevance decision, visual parse, and optional cache.

The first pass is not merely preprocessing. It is a recall-sensitive router. If a missing text layer,
bad table extraction, or mangled layout makes the relevant page unretrievable, the accurate second
pass never runs. Complexity signals—images, absent text layers, dense tables—can supplement semantic
retrieval but do not prove task relevance.

This pattern best fits ad-hoc collections where only a small fraction of pages will be inspected.
Offline corpora, repeated workloads, compliance archives, or mandatory field extraction may justify
up-front visual parsing and durable caching instead.

## Open questions

- How should first-pass recall be measured when the second pass is selectively invoked?
- Which layout signals predict that text extraction will be insufficient?
- When does repeated query-time OCR become more expensive than batch preprocessing?

## Related pages

- [[Retrieval-Augmented Generation]]
- [[Vision-Language Grounding]]
- [[Approximate Nearest-Neighbor Search]]
- [[Search-Augmented Language Models]]
- [[Jerry Liu - Just-in-Time Agentic OCR]]
