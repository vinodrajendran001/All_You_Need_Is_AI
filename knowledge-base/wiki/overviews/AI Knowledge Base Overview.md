---
type: overview
created: 2026-05-08
updated: 2026-05-13
tags:
  - overview
  - ai
  - knowledge-base
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-05-08-murphy-reinforcement-learning-overview
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
status: active
---

# AI Knowledge Base Overview

## Scope

This wiki is the persistent knowledge layer for the `All_You_Need_Is_AI` vault. It is meant to accumulate sources, syntheses, and durable answers about AI instead of rediscovering them from scratch on every query.

## Current picture

The workspace now implements Karpathy's three-layer pattern:

- Raw sources live under `knowledge-base/raw/`.
- Curated wiki pages live under `knowledge-base/wiki/`.
- The operating schema lives in the root `CLAUDE.md` note.

The first source in the system is [[Andrej Karpathy - LLM Wiki]], which establishes the baseline operating model for future ingests. The second source, [[Kevin Murphy - Reinforcement Learning - An Overview]], seeds the first domain-specific branch of the wiki around [[Reinforcement Learning]]. The third source, [[ByteByteGo - Connecting LLMs to the Real World]], opens the **LLM tooling and agents** branch covering [[Tool Use and Function Calling]], [[Model Context Protocol]], and the [[Agentic Loop]].

## Key pages

- [[knowledge-base/wiki/index|Knowledge Base Index]] - main entry point into the wiki
- [[Persistent Wiki]] - the central idea behind the whole system
- [[Schema-Driven Knowledge Base]] - how the schema keeps maintenance disciplined
- [[Ingest Query Lint Loop]] - the repeating maintenance cycle
- [[Index and Log]] - control files that help the LLM navigate the vault
- [[Reinforcement Learning]] - first domain hub page seeded from an ingested paper
- [[Tool Use and Function Calling]] - how LLMs request real-world actions
- [[Model Context Protocol]] - open standard for universal tool integration
- [[Agentic Loop]] - the iterative cycle powering multi-step tool use

## Gaps

- Existing notes elsewhere in the workspace have not yet been ingested into this structure.
- Reinforcement learning has a top-level hub page now, but its subtopics are not yet broken into dedicated notes.
- The `queries/` folder is now active, but `syntheses/` and `lint/` are still at seed-stage and need more accumulated work before they become genuinely useful.
- No search tooling has been added yet because the index is enough at the current scale.

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Obsidian]]
- [[Reinforcement Learning]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
