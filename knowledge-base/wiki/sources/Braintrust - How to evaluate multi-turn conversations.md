---
type: source-summary
created: 2026-06-02
updated: 2026-06-02
source_id: src-2026-05-29-braintrust-multi-turn-scoring
source_title: How to evaluate multi-turn conversations
source_author: Braintrust Team
source_url: https://www.braintrust.dev/blog/multi-turn-scoring
tags:
  - source/summary
  - llm-evaluation
  - conversations
  - traces
  - braintrust
source_ids:
  - src-2026-05-29-braintrust-multi-turn-scoring
status: active
---

# Braintrust - How to evaluate multi-turn conversations

## Summary

This Braintrust article argues that conversation quality cannot be captured by scoring isolated responses alone. Multi-turn products need at least two layers of evaluation: turn-level scoring for local response quality and conversation-level scoring for whether the interaction actually resolved the user's problem. To make that possible, the application must log the whole conversation as a structured trace rather than a pile of unrelated single-turn events.

The article then turns that principle into an operational recipe: instrument grouped traces, score individual turns and whole conversations with LLM-as-a-judge, run those scorers asynchronously in production, and cluster results to spot failure patterns at scale. The durable idea is that evaluation for conversational systems is not a single metric but a stacked measurement system over turns, traces, and aggregated traffic patterns.

## Key claims

- Single-turn scoring misses failures such as repeated questions, contradictions, circular exchanges, and unresolved conversations.
- Multi-turn products need both per-turn quality metrics and per-conversation outcome metrics.
- Trace structure matters: if turns are not grouped into a single conversation object, conversation-level evaluation is impossible.
- LLM-as-a-judge is practical for both turn-scoped and trace-scoped scoring when the criteria are explicit.
- Online scoring should run asynchronously so evaluation does not add user-facing latency.
- Pattern discovery over large volumes of scored conversations needs clustering or topic extraction, not just manual trace review.

## Why it matters

This source gives the vault a concrete implementation pattern for conversation-level evaluation. It complements the DoorDash flywheel by showing what the logging, scoring, and analysis substrate looks like when multi-turn evaluation moves into everyday production use.

## Tensions / open questions

- How many trace-level metrics can teams maintain before the evaluation stack becomes as hard to manage as the product itself?
- Which conversation-level outcomes are robustly judgeable by LLMs and which still require domain-specific human review?
- How much scoring coverage is enough before sampling and cost constraints start hiding meaningful failures?

## Affected pages

- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[Braintrust]]
- [[ML Systems at Scale]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/How to evaluate multi-turn conversations - Blog.md`

## Related pages

- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[Braintrust]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[ML Systems at Scale]]
- [[AI Knowledge Base Overview]]
