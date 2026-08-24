---
type: source-summary
created: 2026-08-24
updated: 2026-08-24
source_id: src-2026-08-19-bytebytego-inkling
source_title: The New American AI Model Designed to Be Customized
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/the-new-american-ai-model-designed
tags: [source/summary, models, mixture-of-experts, reasoning]
source_ids: [src-2026-08-19-bytebytego-inkling]
status: active
---

# ByteByteGo - The New American AI Model Designed to Be Customized

## Summary

ByteByteGo analyzes Thinking Machines' Inkling as a very large sparse MoE designed for customization. The article walks through expert routing, mixed local/global attention, positional choices, multimodality, and an exposed reasoning-effort control.

## Key claims

- Inkling has 952B stored parameters but activates six of 256 experts per layer, separating capacity from per-token compute.
- Mixed local and global attention reduces long-context cost while preserving periodic full-context communication.
- The architecture exposes an effort parameter that trades latency and token use for more reasoning.
- Apache 2.0 licensing and post-training orientation position the model as a base for adaptation.

## Why it matters

The source expands [[Mixture of Experts]] from sparse computation into a customization strategy and connects explicit reasoning effort to [[Test-Time Scaling]] and [[Model Routing]].

## Tensions / open questions

- Architecture details and benchmark claims are vendor- or publication-reported.
- The post-training recipe and rationale for several architectural choices are not disclosed.
- Stored parameter scale creates large memory and deployment requirements even with sparse activation.

## Affected pages

- [[Mixture of Experts]]
- [[Test-Time Scaling]]
- [[Model Routing]]
- [[Open Model Ecosystems]]

## Citations

- Raw capture: [[2026-08-19 ByteByteGo - The New American AI Model Designed to Be Customized]]

## Related pages

- [[Thinking Machines]]
- [[ByteByteGo]]
- [[Model Quantization and Efficiency]]

