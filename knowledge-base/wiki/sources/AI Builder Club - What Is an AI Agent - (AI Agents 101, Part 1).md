---
type: source-summary
created: 2026-08-05
updated: 2026-08-05
source_id: src-2026-08-05-aibuilderclub-ai-agents-101-part-1
source_title: 'What Is an AI Agent? (AI Agents 101, Part 1)'
source_author: AI Builder Club
source_url: https://www.aibuilderclub.com/blog/ai-agents-101-part-1
tags:
  - source/summary
  - ai-agents
  - ai-builder-club
source_ids:
  - src-2026-08-05-aibuilderclub-ai-agents-101-part-1
status: active
---

# AI Builder Club - What Is an AI Agent? (AI Agents 101, Part 1)

## Summary

This introductory tutorial defines an agent as a goal-directed think-act-observe loop and contrasts it with a chatbot that produces one response and stops. It decomposes an agent into a language model, tools, memory, and an orchestrator, then implements a small file-inspection agent using native Anthropic or OpenAI tool calling. The lesson emphasizes visible mechanics over frameworks so that readers can understand tool execution, message history, and stopping behavior before adopting larger abstractions.

## Key claims

- The same model can power either a chatbot or an agent; the operational difference is the loop and access to actions.
- The model proposes actions, but ordinary application code executes them, preserving a separable security and audit boundary.
- Tool results must be appended to the conversation or the model cannot observe outcomes and may repeat actions.
- Every loop needs a hard step cap and tool-call logging.
- Tools should be atomic, have clear schemas, and use providers’ native structured calling rather than parsing action strings from prose.
- In-context memory is sufficient for a first agent; persistence and orchestration should be added after the core loop works.

## Why it matters

The tutorial makes agent behavior inspectable. Its sample implementation exposes the control flow that frameworks often hide and gives readers a basis for debugging repeated calls, missing context, unsafe tools, and provider-specific message formats.

## Tensions / open questions

- The source’s product and platform landscape is dated to 2026 and should be checked against primary announcements.
- The example’s filesystem access is intentionally simple; production authorization, sandboxing, cancellation, and prompt-injection defenses require additional design.
- The source calls the architecture stable while provider APIs, tool semantics, and orchestration products continue to change.

## Affected pages

- [[Agentic Loop]]
- [[Tool Use and Function Calling]]
- [[Agent Memory]]
- [[Agent Planning]]
- [[Coding Agent Harness]]

## Citations

- Raw capture: [[2026-08-05 AI Builder Club - What Is an AI Agent - (AI Agents 101, Part 1)]]
- Canonical URL: https://www.aibuilderclub.com/blog/ai-agents-101-part-1

## Related pages

- [[AI Agents in Production]]
- [[Context Engineering]]
- [[Multi-Turn Evaluation]]

