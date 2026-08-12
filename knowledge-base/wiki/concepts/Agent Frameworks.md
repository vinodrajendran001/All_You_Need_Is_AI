---
type: concept
created: 2026-08-12
updated: 2026-08-12
tags:
  - concept
  - agents
  - frameworks
  - sdks
source_ids:
  - src-2026-08-12-alyona-vert-agent-frameworks-sdks
  - src-2026-06-05-systemdesign42-system-design-academy
status: active
---

# Agent Frameworks

## Definition

Agent frameworks are reusable runtimes and architectural toolkits for coordinating model calls, tools, state, memory, workflows, human approval, tracing, and deployment. They sit above model APIs and often overlap with SDKs, which primarily simplify access to lower-level platform operations.

## Why it matters

A framework can remove large amounts of plumbing, but it also establishes state models, context behavior, failure semantics, security boundaries, and migration costs. Framework selection is therefore an architectural choice, not merely a package preference.

## Current synthesis

### Selection dimensions

Choose based on the system being built:

- **Control-flow model:** free loop, event workflow, state machine, or graph.
- **Durability:** in-memory turns versus checkpointed long-running execution.
- **Language and type system:** Python, TypeScript, .NET, and structured validation needs.
- **Data plane:** general tools versus document/RAG-centered processing.
- **Interaction modality:** text, computer use, or real-time voice/multimodal sessions.
- **Multi-agent needs:** explicit handoffs, role-based crews, simulations, or fan-out/fan-in.
- **Operations:** tracing, evaluations, human approval, deployment, storage, and access control.
- **Abstraction cost:** context overhead, debugging opacity, lock-in, and migration surface.

### Ecosystem families

[[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]] maps representative families:

- stateful graph runtimes such as LangGraph, Google ADK, and Microsoft Agent Framework;
- typed general-purpose runtimes such as Pydantic AI;
- role-based multi-agent systems such as CrewAI and CAMEL-AI;
- data-centric systems such as LlamaIndex;
- lightweight code-action libraries such as smolagents;
- TypeScript-native stacks such as Mastra;
- voice/multimodal infrastructure such as LiveKit Agents.

### Frameworks do not remove core design work

A framework supplies mechanics, not a trustworthy objective or verifier. Teams still need [[Context Engineering]], [[Agent Security and Governance]], [[Multi-Turn Evaluation]], and explicit failure handling. A hand-written loop remains preferable when the task is small and framework features would add more state and context than value.

## Open questions

- Which framework behaviors can be compared under equivalent end-to-end tasks?
- How portable are traces, state, tools, and workflows across runtimes?
- When should teams build on a framework versus extract a small internal harness?
- How should rapidly changing feature claims and project maturity be evaluated?

## Related pages

- [[Coding Agent Harness]]
- [[Graph Engineering]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Real-Time Voice AI]]
- [[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]]

