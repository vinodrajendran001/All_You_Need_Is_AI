---
type: entity
entity_kind: organization
created: 2026-05-29
updated: 2026-10-07
tags:
  - entity
  - organization
  - delivery
  - search
  - llm-evaluation
source_ids:
  - src-2026-05-28-doordash-llm-judge
  - src-2026-05-21-bytebytego-batch
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-09-30-bytebytego-doordash-agent-gateway
status: active
---

# DoorDash

DoorDash is a delivery platform whose engineering writing appears in this vault as both systems architecture and applied search/ML evaluation work.

## Why it matters to this vault

In [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]], DoorDash appears as the subject of a modular onboarding architecture that enabled rapid country launches through thin orchestration and reusable workflow steps. In [[DoorDash - LLM-as-a-Judge for Search Evaluation]], DoorDash's own engineering team describes how it evaluates natural-language search with facet-based rubrics, calibrated LLM judges, and continuous regression monitoring. In [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]], DoorDash appears again as a support-chatbot case study built around a simulation-and-evaluation flywheel for multi-turn conversations.

Together these sources make DoorDash relevant here not only as a marketplace company, but as a recurring source of practical engineering patterns for workflow modularity, search relevance, chatbot testing, and ML evaluation. Its engineering writing is therefore worth treating as a substantive source of production architecture and evaluation ideas.

## Shared tool access complements the evaluation flywheel

[[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]] reports a registry/control plane and
separate internal/external proxy planes serving **200+ MCP servers**, **30+ agents or services**,
and **millions of weekly tool calls**. These are attributed adoption figures, not independent
performance or security measurements.

The reusable design is the separation of tool discovery, call authorization, and downstream
credentials. Task bundles curate `tools/list`; invocation still requires authorization. OAuth
can pause/resume on capable clients or return a structured authorization-required result.
Per-call trace attribution connects this access layer to the existing testing story.

Cryptographic delegation identities, dynamic discovery, and stronger redaction/evaluation are
roadmap items in the source. Do not infer that every proposed control is already deployed merely
because the gateway has broad adoption.

## Related pages

- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[Model Context Protocol]]
- [[Tool Roster Economics]]
- [[Agent Observability]]
- [[Agent Security and Governance]]

- [[DoorDash - LLM-as-a-Judge for Search Evaluation]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[ML Systems at Scale]]
- [[AI Knowledge Base Overview]]
