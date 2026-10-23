---
type: post-archive
created: 2026-08-29
updated: 2026-10-23
tags:
  - post
status: active
---

# Post Archive

Ledger of LinkedIn and X posts drafted from this vault. Each run produces **one idea in one file, written for both
platforms** — a long-form LinkedIn post plus an X standalone and thread. The **Post** workflow in the root `CLAUDE.md`
reads this page first, then the newest non-superseded ready/published post's `covers_through`
date, to work out which ingest window it should cover next. Editorial replacements reuse and
rescan the rejected draft's original window, including later same-day ingests.

Posts are derived output, not evidence. Concept, entity, and synthesis pages must never cite a post.
Posts carry no `source_id`s of their own, so they do not affect source-ID parity across index, log, and overview.

## Editorial source preferences

**Exclude ByteByteGo from Post runs (2026-10-23 onward).** Do not select its topics or use its
examples, claims, or attribution, including indirectly through shared concepts or roundups.
Check underlying author, publisher, URL, and citations. A mixed-source concept remains eligible
only for claims independently supported by non-ByteByteGo evidence read and cited directly.
Recheck old candidates against this preference before scoring. This does not remove ByteByteGo
from ingestion, wiki evidence, or historical posts.

## Cooldown rule

The **spine page** is the wiki page a post is built around — the first entry in its `pages_used`.
A spine page is in **cooldown for 6 weeks** after a post ships. It may be used again sooner only from a
materially different angle, and that post must say what is new.

## Posts

| Date | Post | Window covered | Spine page | Platforms | Status |
|------|------|----------------|------------|-----------|--------|
| 2026-08-29 | [[2026-08-29 KL Should Follow the Reward]] | 2026-08-26 → 2026-08-29 | [[Reward Design for RL]] | LinkedIn, X | ready |
| 2026-09-05 | [[2026-09-05 Nobody Tests the Instructions]] | 2026-08-29 → 2026-09-05 | [[Context Engineering]] | LinkedIn, X | ready |
| 2026-09-11 | [[2026-09-11 The Benchmark Changed Its Mind]] | 2026-09-05 → 2026-09-11 | [[Serving Benchmarks and Goodput]] | LinkedIn, X | ready |
| 2026-09-18 | [[2026-09-18 Memory Has Two Bills]] | 2026-09-11 → 2026-09-18 | [[Agent Memory]] | LinkedIn, X | ready |
| 2026-09-25 | [[2026-09-25 Keep the Expensive Model On Call]] | 2026-09-18 → 2026-09-25 | [[Just-in-Time Agentic OCR]] | LinkedIn, X | ready |
| 2026-10-03 | [[2026-10-03 The Weakest Layers Aren't the Ones to Remove]] | 2026-09-25 → 2026-10-03 | [[Model Quantization and Efficiency]] | LinkedIn, X | ready |
| 2026-10-09 | [[2026-10-09 The Model Can Read Without Writing]] | 2026-10-03 → 2026-10-09 | [[Semantic Recommendation Systems]] | LinkedIn, X | ready |
| 2026-10-16 | [[2026-10-16 The Next Model Can Skip the Reread]] | 2026-10-09 → 2026-10-16 | [[KV Cache]] | LinkedIn, X | ready |
| 2026-10-23 | [[2026-10-23 The Skyline Was the Message]] | 2026-10-16 → 2026-10-23 | [[Chain-of-Thought Monitoring]] | LinkedIn, X | ready |

## Superseded drafts

- [[2026-10-23 A Safe Query Is Not a Correct Answer]] - rejected editorially and replaced
  on 2026-10-23 by [[2026-10-23 The Skyline Was the Message]]. Retained as `draft` for
  historical log links; not published and excluded from active topics and spine cooldown.
- [[2026-10-16 The Correction Did Not Reach the Report]] - rejected editorially and replaced
  on 2026-10-16. Retained as `draft` so the append-only log link remains valid; not published
  and excluded from spine cooldown.

## Topics covered

<!-- Running list, newest first. Checked during candidate selection to avoid repeating an angle. -->

- 2026-10-23 - messages in images, visual information channels, multimodal evaluation
- 2026-10-16 - cross-model cache handoffs, context transfer, model routing, internal state portability
- 2026-10-09 - language models without text generation, catalog ranking, bounded output, product output design
- 2026-10-03 - model pruning, component interactions, system optimization, model compression
- 2026-09-25 - selective computation, agentic OCR, multimodal serving, routing gates
- 2026-09-18 - agent memory, cumulative context cost, memory evaluation, selective retrieval
- 2026-09-11 - benchmark normalization, inference economics, latency-throughput tradeoffs, accelerator comparison
- 2026-09-05 - agent context files, instruction bloat, negative results, evaluating prompts
- 2026-08-29 - reward design, KL divergence, verifiable vs preference rewards, post-training recipes

## Unposted candidates worth revisiting

<!-- Strong angles that lost a scoring round. Not a commitment; just don't rediscover them from scratch. -->

- An AI supervisor can spend the attention it is meant to save: McAteer reports skimming checks triggered on 99 of 111 turns; frequency is not a false-positive rate or measured usefulness. Scored 28/30 in the October 23 replacement round - [[Coding Agent Harness]], [[Dan McAteer - Claude Mods and the Attention Interface]]
- Teach a decision model that the correct answer may be absent: Base Labs describes adding abstention options and sometimes removing the correct choice during training; reliability gains from this ingredient are not isolated. Scored 25/30 in the October 23 replacement round - [[Typed Probabilistic Decision Models]], [[Base Labs - Mammoth-1 and Elephant-1 Decision Models]]
- Acceptance is not end-to-end speed: speculative-decoding gains depend on draft cost and serving conditions. Reframed after the October 16 lint; the earlier 1.21×–2× cap reading is withdrawn - [[Speculative Decoding]], [[Serving Benchmarks and Goodput]]
- Reasoning traces as an unsanitisable secrets surface: 328 of 6,708 scanned trajectories leaking - [[Reasoning Trace Privacy]], [[Context Engineering]]
- Speculative tool execution gates on purity but not authority - [[Agent Security and Governance]], [[Speculative Tool Execution]]
- **Unsolvable eval tasks teach misbehaviour** - 198 of 898 ExploitGym tasks were unsolvable and generated 93% of the illicit coordination, while a different lab independently built the judge-must-solve gate. Scored 17/20 on 2026-09-05, losing only on freshness because it neighbours the KL post's territory - [[RL Environment Design]], [[Agent Security and Governance]]
- pass@k is the wrong metric (pass@3 = 0.6 vs pass^3 = 0.4), and temperature 0 is not deterministic - [[Multi-Turn Evaluation]], [[Agentic Testing]]
- The local metric trap: GitHub cut per-response tokens and raised total cost, because agents reopened what was removed - [[Benchmark Optimization]], [[Harness Optimization]]
- Agentic kernel optimization pays inversely to prior human effort (42.3% / 15.2% / ~5.5%) - [[Inference Efficiency Frontier]]
- Prose summaries score 4/45 on behavioural questions where source code scores 27/45 - [[Context Engineering]], [[Addy Osmani - Audit your Agent files]]
- A weaker model is a stronger teacher: QwQ-32B beat DeepSeek-R1 across 1,000+ controlled distillation experiments - [[Knowledge Distillation]], [[Multi-Teacher On-Policy Distillation]]
- The obvious megakernel scheduling optimization made serving 1-2% slower, with no causal explanation - [[Megakernels]]
- Training loss measures downstream accuracy without labels: ~85% rank correlation, rising to ~99% after normalization - [[Joint-Embedding Predictive Architecture]]
- LLM failures frequently return HTTP 200, so agent operations need attribution rather than transport-level detection - [[Agent Observability]], [[LLM Application Resilience]]
- Weight fit is not runtime fit: Gemma 3 27B drops from at least 54 GB in BF16 to about 13.5 GB at 4-bit, but that does not establish one-L4 deployment once KV cache, activations, workspace, and runtime overhead are included - [[Model Quantization and Efficiency]]
- Models synthesize while deterministic tools produce evidence: one generated solution failed 13 cases, a sandboxed suite reached 19/20, and bounded repair reached 20/20 - [[Agentic Testing]]
- Tenant scope must survive every hop across identity, memory, tools, data, model context, and traces - [[Multi-Tenant Agent Architecture]]
- Typed probabilistic output removes invalid shapes, not semantic hallucinations - [[Typed Probabilistic Decision Models]]
- Quantization can make encoder disaggregation more valuable by moving the bottleneck - [[Model Quantization and Efficiency]], [[Prefill-Decode Disaggregation]]
- Build the parity harness before asking agents to translate legacy code - [[Legacy Code Modernization with AI Agents]]
- AI changed optimization search cost, not the optimization techniques - [[Software Performance Engineering]]
- Precompute fixed choices: four cached candidate actions reduce each decision from five model passes to one, with the method reported 13x faster around 1,000 candidates - [[Typed Probabilistic Decision Models]], [[Inference Efficiency Frontier]]
- Improve an AI application one tested change at a time: held-out cases, a revert rule, a noise floor, and a warning to change objectives when the evaluation is ~95% saturated - [[Agentic Testing]], [[Harness Optimization]]
- Agents can pay through ordinary web requests, but payment proof does not solve identity, reputation, abuse, refunds, or disputes - [[Agent Payment Protocols]], [[Agent Security and Governance]]
- Check the quantity before setting a decision threshold: Jev Choice's confidence field describes concentration, not the winning option's probability - [[Typed Probabilistic Decision Models]], [[Sebastian Raschka - Language Models for Text Classification - From Bag-of-Words to Jev]]
- Replit's reported coordination configuration is more accurate and costlier than its one-worker sidekick; a useful quality/cost tradeoff is not a win on both axes - [[Graph Engineering]], [[Replit - Free the Models - Harness Design at the Frontier]]
- Test detection before trusting a quiet monitor: embedded-evaluation principles are a proposal, not evidence that a live regime has already worked - [[Embedded Evaluation]], [[Apollo Research - Principles for Embedded Evaluations]]
- A generated interface surviving a redraw does not establish durable application state; separate runtime continuity from storage guarantees - [[Generative User Interface]], [[@rabi_guha - How ChatGPT Intelligent UI Works]]

## Spine pages in cooldown

<!-- Page - post date - cooldown ends. Prune entries once expired. -->

- [[Agent Memory]] - posted 2026-09-18 - cooldown ends 2026-10-30
- [[Just-in-Time Agentic OCR]] - posted 2026-09-25 - cooldown ends 2026-11-06
- [[Model Quantization and Efficiency]] - posted 2026-10-03 - cooldown ends 2026-11-14
- [[Semantic Recommendation Systems]] - drafted 2026-10-09 - cooldown ends 2026-11-20
- [[KV Cache]] - drafted 2026-10-16 - cooldown ends 2026-11-27
- [[Chain-of-Thought Monitoring]] - drafted 2026-10-23 - cooldown ends 2026-12-04

## Related pages

- [[AI Knowledge Base Overview]] - orientation page for the vault these posts draw from
- [[log|Knowledge Base Log]] - the dated ingest record that defines each post's candidate window
