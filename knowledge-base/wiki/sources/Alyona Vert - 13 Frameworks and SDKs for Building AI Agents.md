---
type: source-summary
created: 2026-08-12
updated: 2026-08-26
source_id: src-2026-08-12-alyona-vert-agent-frameworks-sdks
source_title: 13 Frameworks and SDKs for Building AI Agents
source_author: Alyona Vert
source_url: https://www.turingpost.com/p/frameworks-sdks
tags:
  - source/summary
  - ai-agents
  - frameworks
  - sdks
source_ids:
  - src-2026-08-12-alyona-vert-agent-frameworks-sdks
status: active
---

# Alyona Vert - 13 Frameworks and SDKs for Building AI Agents

## Summary

Alyona Vert distinguishes four layers: a model supplies capability, an API exposes it, an SDK wraps common API operations, and an agent framework adds runtime architecture for tools, memory, state, workflows, tracing, human approval, and multi-agent coordination. The guide compares 13 projects ranging from minimal code-oriented libraries to graph runtimes, data-centric stacks, complete agent platforms, and real-time voice systems.

Its durable value is not a ranking but a capability map. Framework selection should follow the workload, language ecosystem, state and durability needs, data plane, interaction modality, governance requirements, and desired abstraction level.

## Key claims

- SDK and framework are overlapping rather than strict categories; many products combine both.
- LangGraph, Google ADK, and Microsoft Agent Framework emphasize explicit stateful graph workflows.
- Pydantic AI emphasizes typed Python interfaces, validation, dependency injection, and observability.
- CrewAI and CAMEL-AI emphasize role-based multi-agent composition and research.
- LlamaIndex centers data ingestion, retrieval, and document agents.
- smolagents favors a lightweight code-action loop, while Mastra serves TypeScript-native application stacks.
- LiveKit Agents specializes in low-latency voice and multimodal sessions with WebRTC and telephony.
- There is no universally best framework; minimizing unnecessary abstraction remains a legitimate choice.

## Why it matters

The source seeds [[Agent Frameworks]] and places the abstract [[Coding Agent Harness]] and [[Graph Engineering]] concepts against concrete ecosystem options. It gives production teams a selection taxonomy without implying that framework adoption solves evaluation, security, or context design.

## Tensions / open questions

- Feature lists, language support, stars, provider compatibility, and project maturity change quickly.
- Vendor descriptions do not establish reliability, interoperability, or production quality.
- Framework comparisons should include migration cost, lock-in, debugging ergonomics, security boundaries, and total context overhead.
- The guide does not benchmark equivalent tasks across the 13 options.
- Categories blur as SDKs add runtimes and frameworks expose lower-level primitives.

## Affected pages

- [[Agent Frameworks]]
- [[Coding Agent Harness]]
- [[Graph Engineering]]
- [[AI Agents in Production]]
- [[Real-Time Voice AI]]

## Citations

- Raw capture: [[2026-08-12 Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]]
- Canonical URL: https://www.turingpost.com/p/frameworks-sdks

## Raw capture

- [[2026-08-12 Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]]

## Related pages

- [[Alyona Vert]]
- [[Agentic Loop]]
- [[Agent Memory]]
- [[Model Context Protocol]]

