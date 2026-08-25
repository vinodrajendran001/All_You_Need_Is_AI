---
type: entity
created: 2026-08-25
updated: 2026-08-25
entity_kind: organization
tags:
  - entity
  - organization
  - open-models
  - platform
  - evaluation
source_ids:
  - src-2026-08-21-hume-ai-asr-benchmark-optimization
  - src-2026-08-18-hugging-face-state-open-models-summer-2026
status: active
---

# Hugging Face

## What it is

The dominant open model and dataset hub, and increasingly a publisher of ecosystem research and leaderboards in its own right.

## Why it matters here

Hugging Face plays two distinct roles in this vault, and they pull in interesting directions.

**As infrastructure**, it is the substrate almost every open-model source assumes. Model cards, config files, and dataset pages are the citations used throughout — [[Changyi Yang - Why MLA and MTP Fight Each Other]] reads head counts straight out of `config.json` files on the hub to ground its arithmetic, and [[Open Model Ecosystems]] is largely a description of activity that happens there.

**As a measurement authority**, it operates the leaderboards that decide what "state of the art" means for open models — which makes [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]] notable. Rather than defending its leaderboard, Hugging Face co-authored the work showing that leading ASR models reproduce benchmark reference errors and detect which benchmark they are being tested on, then shipped the findings back into the product as a "Benchmark fitting" tab on the Open ASR Leaderboard with open-sourced scripts and un-normalised outputs. It also maintains the held-out private-data evaluations that the paper recommends as the remedy.

That combination — hosting the models, hosting the benchmarks, and publishing evidence that the benchmarks are being gamed — is what makes it a useful node rather than just a URL prefix. See [[Benchmark Optimization]].

## Notes

- [[Hugging Face - State of Open Models Summer 2026]] is the vault's ecosystem-survey source; its rankings inherit whatever measurement error [[Benchmark Optimization]] describes.
- Relevant properties: the Open ASR Leaderboard, the Far-field ASR Leaderboard, and the hosting of Real World VoiceEQ.

## Related pages

- [[Hugging Face - State of Open Models Summer 2026]]
- [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]]
- [[Benchmark Optimization]]
- [[Open Model Ecosystems]]
- [[Real-Time Voice AI]]
- [[Hume AI]]
- [[AI Knowledge Base Overview]]
