---
type: entity
entity_kind: publication
created: 2026-05-13
updated: 2026-06-10
tags: [newsletter, system-design, engineering]
source_ids:
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-05-21-bytebytego-batch
  - src-2026-05-28-bytebytego-airtable-search
  - src-2026-06-10-bytebytego-token-spend-routing
status: active
---

# ByteByteGo

A popular engineering newsletter and publication focused on system design, software architecture, infrastructure, and increasingly AI-in-production topics. It is known for clear visual explanations of complex engineering concepts using diagrams and step-by-step breakdowns.

## Why it matters to this vault

ByteByteGo now anchors two distinct branches in this knowledge base.

The first branch comes from [[ByteByteGo - Connecting LLMs to the Real World]], which serves as a primary source for understanding [[Tool Use and Function Calling]], [[Model Context Protocol]], and the [[Agentic Loop]].

The second branch comes from [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]], a composite batch of eight articles covering Netflix multimodal search, Snap’s Bento inference platform, Grab’s production AI agents, Figma’s MCP-backed design workflows, Amazon’s COSMO recommendation system, Instacart’s hybrid search stack, DoorDash’s modular onboarding architecture, and Alex Xu’s monolith-vs-microservices-vs-serverless comparison. Together they reinforce ByteByteGo as a continuing high-signal source for production system-design patterns rather than a one-off explainer source.

A third, newer standalone source, [[ByteByteGo - How Airtable Built the Search Layer]], extends ByteByteGo's coverage into vector infrastructure and semantic search operations, focusing on why Airtable combined one-partition-per-base isolation, hierarchical partition caps, HNSW indexing, and hot/cold memory tiering for AI retrieval.

A fourth standalone source, [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]], extends ByteByteGo's coverage into **agent economics and routing infrastructure**. Its key contribution is to treat model routing as production control logic rather than a pricing trick: gateways, decision layers, mode-based routing, tier selection, and budget-aware spend governance become first-class system design topics for agent loops.

## Related pages

- [[ByteByteGo - Connecting LLMs to the Real World]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[ByteByteGo - How Airtable Built the Search Layer]]
- [[ByteByteGo - Token Spend Out of Control - The Case for Smarter Routing]]
- [[ML Systems at Scale]]
- [[AI Agents in Production]]
- [[Model Routing]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[AI Knowledge Base Overview]]
