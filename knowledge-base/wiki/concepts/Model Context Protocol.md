---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags: [mcp, protocol, tool-use, agents, anthropic]
source_ids:
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
status: active
---

# Model Context Protocol

An open standard introduced by Anthropic that defines a common protocol for connecting LLM applications to external tools, data sources, and services.

## The problem it solves

Before MCP, each LLM provider implemented function calling differently. Integrating *N* providers with *M* tools required *N×M* custom integrations. MCP reduces this to *N+M*: each provider implements the client side once, each tool implements the server side once.

## Architecture

MCP uses a client–server model with three components:

1. **MCP Host** — the AI application the user interacts with (e.g., Claude Desktop, an AI-powered IDE).
2. **MCP Client** — lives inside the host; handles communication with external servers.
3. **MCP Server** — a lightweight program that wraps an existing tool, database, or API and exposes it in MCP's standard format.

On startup, the client connects to available servers, asks each to describe its capabilities, and feeds those descriptions to the model as tool definitions. From there, the standard [[Tool Use and Function Calling|function calling]] mechanism takes over.

## Capabilities

- **Tools** — functions the model can invoke (the primary use case driving adoption).
- **Resources** — data the model can read (files, database records).
- **Prompt templates** — reusable prompt structures exposed by servers.

## Relationship to function calling

MCP does **not** replace function calling. Function calling is how the model signals it wants to use a tool. MCP standardises how tools are described, discovered, and invoked so that the same tool works across any compliant model. They are complementary layers.

## Adoption timeline

| Date | Event |
|---|---|
| Late 2024 | Anthropic introduces MCP as open standard |
| 2025 | OpenAI and Google DeepMind announce MCP support |
| Late 2025 | 10,000+ public MCP servers listed |
| Late 2025 | Protocol donated to Agentic AI Foundation (Linux Foundation), co-founded by Anthropic, Block, and OpenAI |

## Security concerns

- Every exposed tool expands the attack surface.
- September 2025: first supply-chain attack — a malicious npm package mimicked a legitimate Postmark email MCP server, silently forwarding emails to the attacker.
- The protocol initially prioritised adoption over security; authentication and governance specs matured through multiple revisions.
- Tool definitions consume context-window tokens — hundreds of tools degrade model reasoning.

## Related pages

- [[Tool Use and Function Calling]]
- [[Agentic Loop]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
- [[AI Knowledge Base Overview]]
