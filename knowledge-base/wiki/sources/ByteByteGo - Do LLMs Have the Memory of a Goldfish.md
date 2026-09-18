---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-15-bytebytego-llm-memory-goldfish
source_title: "Do LLMs Have the Memory of a Goldfish?"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/do-llms-have-the-memory-of-a-goldfish
tags: [source/summary, memory, context-engineering, retrieval]
source_ids: [src-2026-09-15-bytebytego-llm-memory-goldfish]
status: active
---

# ByteByteGo - Do LLMs Have the Memory of a Goldfish

## Summary

This explainer separates trained knowledge, temporary context, and application-managed persistent
memory. Cross-session recall normally comes from external conversations, profiles, files, databases,
or vector stores that an application selects and inserts into a new prompt; server-managed
conversation IDs change who reconstructs the context, not the model's stateless invocation.

## Key claims

- Replaying a growing conversation creates cumulative input cost: if each round adds about 1,000
  tokens, ten requests process roughly **55K input tokens** for a visible 10K-token conversation.
- Prompt caching saves repeated computation but neither expands the context window nor creates memory.
- Sliding windows preserve recency; summaries compress but can distort under repeated
  summary-of-summary updates; structured extraction preserves fields; vector memory retrieves
  semantically similar records.
- Persistent profiles should retain stable, sourced, timestamped facts rather than transient remarks.

## Why it matters

Memory is a retrieval and context-insertion system with provenance, conflict, expiry, and selection
policies. Calling a large context window "memory" hides those application responsibilities.

## Tensions and caveats

The numerical budgets and 20-turn window are illustrations, not measurements. The article supplies no
original experiment and simplifies model-native recurrent or inference-time memory.

## Raw capture

- [[2026-09-15 ByteByteGo - Do LLMs Have the Memory of a Goldfish]]

## Affected pages

- [[Agent Memory]]
- [[Context Engineering]]
- [[ByteByteGo]]

## Related pages

- [[Retrieval-Augmented Generation]]
- [[KV Cache]]
- [[Persistent Wiki]]

