---
type: source-summary
created: 2026-08-24
updated: 2026-08-26
source_id: src-2026-08-17-google-cloud-agent-plugins
source_title: Agent Plugins Are the Future of Agent Skills
source_author: Google Cloud
source_url: https://x.com/GoogleCloudTech/status/2087733334617063503
tags: [source/summary, ai-agents, plugins, mcp]
source_ids: [src-2026-08-17-google-cloud-agent-plugins]
status: active
---

# Google Cloud - Agent Plugins Are the Future of Agent Skills

## Summary

Google Cloud presents Agent Plugins as a vendor-neutral packaging standard that places agent skills, MCP servers, assets, and client-specific configuration in one portable directory. A small manifest provides identity and discovery while components retain separate failure boundaries.

## Key claims

- Skills are discovered one directory below `skills/`, with each skill defined by `SKILL.md`.
- MCP servers can use stdio, streamable HTTP, or SSE transports.
- `${PLUGIN_ROOT}` addresses packaged read-only assets; `${PLUGIN_DATA}` addresses persistent client-managed state.
- A malformed manifest rejects the plugin, while a broken MCP configuration or individual server need not disable valid skills.
- Credentials remain client-managed; the draft does not define portable authentication.

## Why it matters

The proposal extends [[Agent Skill]] from reusable instructions into a distribution unit that bundles instructions and executable tools. It also makes [[Model Context Protocol]] one component of a broader [[Agent Plugin Architecture]] rather than the whole portability story.

## Tensions / open questions

- The specification is a working draft and has no mature conformance validator.
- Partial client implementations and silent skill-discovery failures weaken portability claims.
- Existing plugin formats and credential systems still require client-specific handling.

## Affected pages

- [[Agent Plugin Architecture]]
- [[Agent Skill]]
- [[LLM-Native Extensible Software]]

## Citations

- Raw capture: [[2026-08-17 Google Cloud - Agent Plugins Are the Future of Agent Skills]]
- Specification: https://agent-plugins.org/specification

## Raw capture

- [[2026-08-17 Google Cloud - Agent Plugins Are the Future of Agent Skills]]

## Related pages

- [[Tool Use and Function Calling]]
- [[Coding Agent Harness]]
- [[Google Cloud - Agent Plugins Are the Future of Agent Skills]]
- [[Agent Frameworks]]
- [[Agent Security and Governance]]
- [[Model Context Protocol]]

