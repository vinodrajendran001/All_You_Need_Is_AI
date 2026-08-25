---
type: concept
created: 2026-08-24
updated: 2026-08-24
tags: [concept, software-architecture, ai-agents, extensibility]
source_ids:
  - src-2026-08-20-jeremy-morrell-extensible-software
  - src-2026-08-17-google-cloud-agent-plugins
status: active
---

# LLM-Native Extensible Software

## Definition

LLM-native extensible software lets users generate durable application extensions from natural-language intent while a trusted host constrains their execution through stable capabilities and isolated runtimes.

## Architecture

[[Jeremy Morrell - Extensible Software in the Age of LLMs]] separates:

- a **trusted shell** that owns identity, data, routing, and privileged APIs;
- **generated UI** that is stored and inspectable;
- **generated server code** executed in isolated workers;
- a narrow RPC interface that exposes only approved capabilities.

The generated artifact should survive the conversation, be versioned, and remain understandable as code. Server-side workers provide a stronger isolation point than unrestricted browser execution, although sandboxing, dependency control, schema migration, and debugging remain difficult.

[[Agent Plugin Architecture]] is the distribution counterpart: once an extension or capability is durable, it needs a manifest, assets, state boundaries, and portable tool definitions.

## Open questions

- How can generated extensions be upgraded without breaking user state?
- What review and provenance should be required before permissions expand?
- Can narrow capability APIs remain useful without recreating a full operating system?

## Related pages

- [[Agent Plugin Architecture]]
- [[Agent Security and Governance]]
- [[Coding Agent Harness]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]

