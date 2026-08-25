---
type: source-summary
created: 2026-08-03
updated: 2026-08-25
source_id: src-2026-07-28-bytebytego-delivery-llm-search
source_title: "Why DoorDash, Instacart, and Uber Eats Integrated LLMs Into Search Three Different Ways"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/why-doordash-instacart-and-uber-eats
tags: [source/summary, search, retrieval, production]
source_ids: [src-2026-07-28-bytebytego-delivery-llm-search]
status: active
---

# ByteByteGo - Three LLM Search Architectures for Delivery Platforms

## Summary

The article compares three ways to add LLMs to marketplace search without replacing the full retrieval stack. DoorDash constrains query parsing to its taxonomy, Instacart combines cached contextual rewriting with online handling for the long tail, and Uber Eats uses fine-tuned LLM embeddings in two-tower ANN retrieval.

## Why it matters

The durable pattern is **LLM augmentation under product constraints**, not generic chat search: use the model where it resolves ambiguity or representation mismatch, retain deterministic catalogs/rankers, and select a design based on traffic distribution, latency budget, and data assets.

## Raw capture

- `knowledge-base/raw/sources/Why DoorDash, Instacart, and Uber Eats Integrated LLMs Into Search Three Different Ways.md`

## Related pages

- [[Retrieval-Augmented Generation]]
- [[ML Systems at Scale]]
- [[Model Routing]]
- [[DoorDash]]
- [[ByteByteGo]]
