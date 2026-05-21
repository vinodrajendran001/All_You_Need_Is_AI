---
type: concept
created: 2026-05-21
updated: 2026-05-21
tags:
  - concept
  - ai-agents
  - production
  - productivity
source_ids:
  - src-2026-05-21-bytebytego-batch
  - src-2026-05-18-rag-architecture-comparison
status: active
---

# AI Agents in Production

Production AI agents are not just prompts wrapped around tools. They are controlled workflows that manage state, context budgets, tool boundaries, risk levels, and human review. The Grab and Figma articles are useful because they describe real agent deployments where the hard part is operational design rather than model novelty.

## Brain, hands, and orchestration

Grab describes a clean production pattern: **decouple the brain from the hands**. The LLM handles reasoning, while specialized agents and tools fetch metadata, trace data lineage, run SQL, inspect pipeline health, or prepare code changes. This is a concrete enterprise implementation of the [[Agentic Loop]]: the loop becomes a routed workflow across multiple specialists rather than a single model repeatedly calling a single tool.

The same pattern appears in Figma’s design workflows. The coding agent does not directly “understand Figma” on its own. It relies on an MCP server that exposes a carefully shaped set of tools and structured context. The agent reasons about which tool to call; the surrounding system defines what data is exposed and how it is transformed.

## Tool use only works when the interface is shaped for the model

Both Grab and Figma show that raw access is usually the wrong product surface.

- Grab learned that too many tools with verbose descriptions degrade both speed and quality.
- Figma learned that raw screenshots lack precision and raw JSON overwhelms the context window.

The production answer in both cases is the same: expose **fewer, better, more model-legible interfaces**. That is exactly the systems layer described by [[Tool Use and Function Calling]] and standardized, in Figma’s case, by [[Model Context Protocol]].

## Context management is a first-class production problem

Agents fail when context grows faster than the orchestration layer can compress it.

- Grab tracks token counts, summarizes older turns, and prunes tool outputs between agent handoffs.
- Figma explicitly recommends a **scan, then zoom in** workflow using `get_metadata` before `get_design_context` so agents do not blow through MCP response budgets.

This makes context shaping part of the product design. Production agents need not only the right tools but also the right amount of context at the right time.

## Risk-based autonomy beats one-size-fits-all automation

Grab splits read-only investigation from write-heavy enhancement work because the blast radius is different. Investigative flows can run with lighter oversight; code and schema changes stay human-gated. Figma’s design↔code roundtrip is similarly bounded: design structure moves between systems, but business logic and state do not automatically survive, which keeps a human developer in the loop.

This is the same principle that powers safer [[Retrieval-Augmented Generation|Agentic RAG]] systems: give the model more autonomy where the cost of a wrong intermediate action is low, and tighten control when actions mutate production state.

## Persistent memory and workflow state matter

Production agents usually need memory outside the model weights.

- Grab uses Redis for fast session needs and PostgreSQL for conversation history plus agent metadata.
- Figma externalizes design state into the Figma file itself and uses MCP tools as the access boundary.

In both cases, the agent is effective because the surrounding system remembers more than the immediate prompt.

## The main lesson

The common pattern is not “let the model do everything.” It is **design an environment where the model can do a few high-value things reliably**. That means specialized agents, narrow tools, token-aware context management, human review, and interfaces that encode domain structure instead of dumping raw data.

## Related pages

- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Retrieval-Augmented Generation]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
