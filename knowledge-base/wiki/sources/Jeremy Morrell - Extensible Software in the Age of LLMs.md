---
type: source-summary
created: 2026-08-24
updated: 2026-08-26
source_id: src-2026-08-20-jeremy-morrell-extensible-software
source_title: Extensible Software in the Age of LLMs
source_author: Jeremy Morrell
source_url: https://www.jeremymorrell.dev/blog/extensible-software
tags: [source/summary, software-architecture, ai-agents, extensibility]
source_ids: [src-2026-08-20-jeremy-morrell-extensible-software]
status: active
---

# Jeremy Morrell - Extensible Software in the Age of LLMs

## Summary

Jeremy Morrell argues that LLMs make application-specific software generation cheap enough for extension to become an everyday runtime primitive. His proposed architecture splits a trusted host shell from generated UI and server-side code running in isolated workers, with a narrow RPC interface between them.

## Key claims

- Generated extensions should be durable, inspectable artifacts rather than ephemeral chat output.
- The host application should own identity, storage, routing, and privileged capabilities.
- Generated code needs independent sandboxing and explicit capability boundaries.
- Server-side execution is easier to isolate reliably than arbitrary browser code.
- Cloudflare Dynamic Workers demonstrate one possible deployment substrate, but the pattern is platform-independent.

## Why it matters

The proposal defines [[LLM-Native Extensible Software]] as a distinct architecture: natural-language generation coupled to durable plugins, stable interfaces, and zero-trust execution.

## Tensions / open questions

- Prompt injection, dependency supply chains, schema migration, debugging, and generated-code review remain unresolved.
- Strong sandboxing and a narrow API constrain what extensions can do.
- The article is an exploratory architecture and demo rather than production evidence.

## Affected pages

- [[Agent Plugin Architecture]]
- [[LLM-Native Extensible Software]]

## Citations

## Raw capture

- [[2026-08-20 Jeremy Morrell - Extensible Software in the Age of LLMs]]

## Related pages

- [[Coding Agent Harness]]
- [[AI Agents in Production]]
- [[Agent Security and Governance]]
- [[Tool Use and Function Calling]]

