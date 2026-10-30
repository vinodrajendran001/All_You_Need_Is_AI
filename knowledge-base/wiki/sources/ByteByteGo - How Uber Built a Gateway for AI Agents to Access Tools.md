---
type: source-summary
created: 2026-10-30
updated: 2026-10-30
source_id: src-2026-10-28-bytebytego-uber-mcp-gateway
source_title: How Uber Built A Gateway For AI Agents To Access Tools
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-uber-built-a-gateway-for-ai-agents
tags:
  - source/summary
  - mcp
  - ai-agents
  - security
source_ids:
  - src-2026-10-28-bytebytego-uber-mcp-gateway
status: active
---

# How Uber Built a Gateway for AI Agents to Access Tools

## Summary

ByteByteGo relays Uber's MCP Gateway architecture: a registry governs the catalog and its
configuration, while a proxy authorizes and translates live calls. Existing service contracts
can become tools without each service implementing MCP. The important boundary is that
automatic discovery does not automatically grant execution authority.

## Key claims

- **The control plane owns discovery and approval.** A Cadence-powered AutoCrawler reads
  existing interface/service definitions, derives request and response schemas, and uses an
  LLM for descriptions. Native MCP servers are discovered through heartbeats and `listTools`.
- **New discoveries start disabled.** Owners review and enable tools or servers; later changes
  use approved diffs and rollback. A generated schema or description is a proposal to the
  catalog, not authorization to run it.
- **The data plane uses refreshed configuration.** The Proxy Gateway periodically loads
  registry state into memory and presents virtual MCP servers. It translates JSON arguments
  into the relevant HTTP, gRPC/Protobuf, or TChannel/Thrift service request and translates the
  response back.
- **Identity, permission, and credentials remain separate.** Policies can apply to the caller,
  server, or tool; response redaction is another control. Third-party services use a separate
  credential-exchange service, rather than treating internal gateway identity as an external
  API credential.
- **Three controls reduce different context costs.** Omni MCP progressively discovers servers,
  tools, and full schemas through `discover_server`, `discover_tools`, and `get_tool_schema`.
  Response projection selects returned fields. Code Mode permits file/shell processing instead
  of putting every intermediate result into model context.

## Why it matters

The design extends [[Model Context Protocol]] from a connection standard into a governed
enterprise integration layer. It also sharpens [[Tool Roster Economics]]: catalog size, resident
schemas, and returned-result volume are separate budgets. [[Agent Security and Governance]]
needs approval at discovery/change time as well as policy at invocation time.

## Tensions / open questions

- This is a secondary architecture account of Uber's engineering post. It supplies no
  quantified latency, context savings, adoption, or security-effectiveness result.
- Periodic proxy refresh leaves the propagation time of a disable or policy change unspecified.
  A central registry alone does not establish immediate revocation.
- LLM-generated descriptions enter the agent's decision context and still require review.
  Reduced context volume is not evidence that the agent selects the right tool.
- The sponsored introduction is not evidence about the gateway. The source's unusual expansion
  of IDL is not repeated as terminology; this summary uses service/interface definitions.

## Affected pages

- [[Model Context Protocol]]
- [[Agent Security and Governance]]
- [[Tool Roster Economics]]
- [[Uber]]
- [[ByteByteGo]]

## Raw capture

- [[knowledge-base/raw/sources/How Uber Built A Gateway For AI Agents To Access Tools]]

## Citations

- Canonical URL: <https://blog.bytebytego.com/p/how-uber-built-a-gateway-for-ai-agents>
- Underlying engineering post linked by the source: <https://www.uber.com/in/en/blog/designing-mcp-gateway/>
  (not independently captured in this ingest).
- Published October 28, 2026; captured October 29, 2026.

## Related pages

- [[Uber]]
- [[ByteByteGo]]
- [[Model Context Protocol]]
- [[Agent Security and Governance]]
- [[Tool Roster Economics]]
- [[Programmatic Tool Calling]]
- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]
