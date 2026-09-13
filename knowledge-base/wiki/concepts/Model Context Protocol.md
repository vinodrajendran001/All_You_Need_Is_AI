---
type: concept
created: 2026-05-13
updated: 2026-09-13
tags: [concept, mcp, protocol, tool-use, ai-agents, anthropic]
source_ids:
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
  - src-2026-05-21-bytebytego-batch
  - src-2026-08-05-aibuilderclub-mcp-101-build-mcp-servers
  - src-2026-08-05-aibuilderclub-mcp-internals-client-server
  - src-2026-08-05-aibuilderclub-mcp-security-attack-vectors
  - src-2026-08-05-aibuilderclub-webmcp-complete-guide
  - src-2026-09-02-can-boluk-harness-playbook
  - src-2026-09-13-weinmeister-build-ai-agents-google-cloud
  - src-2026-09-13-virinchi-google-cloud-mcp-security
status: active
---

# Model Context Protocol

An open standard introduced by [[Anthropic]] that defines a common protocol for connecting LLM applications to external tools, data sources, and services.

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

## Production example: Figma’s design↔code workflow

Figma’s MCP server is a concrete production example of why the protocol matters. The useful part is not just that tools like `get_design_context`, `get_metadata`, `generate_figma_design`, and `use_figma` can be called from coding agents; it is that the server transforms raw design JSON into a token-efficient representation that better matches how developers think.

That example highlights an important point: a good MCP server is not merely an API wrapper. It chooses what context to expose, how to compress it, and which workflows deserve dedicated tools. Figma’s documented **scan first, then zoom in** pattern also shows how MCP server design is inseparable from context-window management.

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

The AI Builder Club MCP cluster adds protocol-level detail around JSON-RPC over local STDIO and remote HTTP transports, then sharpens the trust model. Tool descriptions and returned content enter model context, so one malicious server can influence how the agent uses another server's capabilities.

Practical controls include source review, exact-version pinning or vendoring, least-privilege credentials and paths, network and filesystem sandboxing, and re-audit after tool changes. Static review remains incomplete when dependencies, remote configuration, or later updates can alter behavior.

## Residency, not the protocol, is the cost

[[Can Bölük - The Harness Playbook]] supplies the missing cost side of MCP adoption. Every connected server's tools land in the model's roster, and roster size is measurable in wall clock: a harness
carrying its full roster ran **almost twice as slow as Codex**, and cutting it to **five essential tools gave
36.6s**, ahead of Codex's 42.2s and Pi's 37.0s. Constrained decoding — not just description tokens — is named as
the mechanism.

The design response is not to abandon the protocol but to change what stays resident. The rule offered is
**"bounded operation set: schema; open-ended operation set: code surface"**, with the concrete proposal being a
single discoverable CLI behind the Bash tool (a `dyn` command) so an integration exposes **zero** additional
tools and its surface is discovered on demand. MCP's value as a shared integration standard is untouched by
this; what is being questioned is the default of mounting every capability as a permanently visible tool.

See [[Tool Roster Economics]] for the full argument and the counter-consideration — that a discoverable CLI
still costs turns to discover, which nobody has measured.

## Remote MCP makes recovery part of protocol security

[[Karl Weinmeister - Build AI Agents Your Way on Google Cloud]] places MCP in a wider agent stack:
the protocol standardizes tool and data access, while A2A addresses agent-to-agent communication and
the runtime remains a separate choice. Its examples include MCP Toolbox for Databases over Cloud
SQL, Spanner, and BigQuery.

[[Virinchi T - Google Cloud MCP Security Framework]] makes the consequence boundary concrete.
Remote servers can expose mutating and destructive operations, not only retrieval. Google Cloud
distinguishes Human-in-the-Middle from Agent-Only operation and recommends dedicated identities,
least-privilege IAM, recurring tool inventories, allowlists, deny policies, state isolation, content
inspection, and PII masking. Dynamic servers make a one-time approval insufficient because the tool
surface can change later.

The source adds a control this page previously underweighted: **recovery is part of MCP security**.
Cloud SQL point-in-time recovery, BigQuery time travel, and Cloud Storage versioning do not stop a
bad call, but they change whether the call is irreversible. These are source recommendations for
Preview Google Cloud MCP servers, not measured evidence that the stack defeats prompt injection.

## Related pages

- [[Tool Use and Function Calling]]
- [[Agentic Loop]]
- [[AI Agents in Production]]
- [[Search-Augmented Language Models]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Coding Agent Harness]]
- [[AI Knowledge Base Overview]]
- [[Agent Security and Governance]]
- [[AI Builder Club - Build AI Agents]]
- [[Tool Roster Economics]]
- [[Can Bölük - The Harness Playbook]]
- [[Can Bölük]]
- [[Karl Weinmeister - Build AI Agents Your Way on Google Cloud]]
- [[Virinchi T - Google Cloud MCP Security Framework]]
- [[Google Cloud]]
