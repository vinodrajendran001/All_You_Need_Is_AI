---
type: concept
created: 2026-08-24
updated: 2026-09-04
tags: [concept, software-architecture, ai-agents, extensibility]
source_ids:
  - src-2026-08-20-jeremy-morrell-extensible-software
  - src-2026-08-17-google-cloud-agent-plugins
  - src-2026-09-02-can-boluk-harness-playbook
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

## Configuration and language choice as parts of the extension surface

[[Can Bölük - The Harness Playbook]] extends this page in two directions that extension-API discussions usually
skip.

**Configuration is part of the extension surface.** The proposed model is the Source Engine **convar**: a typed
variable declared once at its definition site with a name, default, help string, and a flag bitfield — the flags
carrying persistence, ownership, scope, replication, and replay-honesty. Because the declaration site owns those
properties, an extension adds a setting without touching a central settings object, and a spawned child session
seeds every variable from the parent's live values with no inheritance setting required. Compare the status quo,
where compatibility axes are literally named after the models that caused them (`qwen-preserve-thinking`,
`strip-deepseek-special-tokens`) and three files totalling over 3,600 lines encode model quirks by hand. The
proposed replacement is a declarative taxonomy, and the stated goal is not fewer quirks: *"The win is not fewer
quirks. It is one owner for each fact, explicit precedence, and an `unknown` state."*

**Implementation language acts as a prior on generated code.** The blunt version — *"TypeScript is an awful
choice at the moment"* — rests on the argument that when agents write most of the extension code, the language's
defaults shape what gets generated. The proposed split is a Rust engine with Python extensions, Python chosen
partly because it can inspect its own AST, which makes decorators like `@remote` implementable rather than
aspirational.

The state-model half of the same argument — why extension state must live in one authoritative place — is in
[[Harness State Authority]], along with the audit finding that **only 2 of 17 stateful reference extensions were
correct.**

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
- [[Harness State Authority]]
- [[Tool Roster Economics]]
- [[Can Bölük - The Harness Playbook]]
- [[Can Bölük]]
