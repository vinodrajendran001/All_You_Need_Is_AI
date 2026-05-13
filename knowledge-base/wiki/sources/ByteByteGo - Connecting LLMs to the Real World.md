---
type: source-summary
source_id: src-2026-05-04-bytebytego-llm-tool-use-mcp
source_title: "Connecting LLMs to the Real World: Tool Use, Function Calling, and MCP"
source_author: ByteByteGo
source_url: "https://blog.bytebytego.com/p/connecting-llms-to-the-real-world"
created: 2026-05-13
updated: 2026-05-13
tags: [tool-use, function-calling, mcp, agents, llm]
status: active
---

# Connecting LLMs to the Real World: Tool Use, Function Calling, and MCP

## Summary

A ByteByteGo article (published 2026-05-04) tracing the evolution from LLMs as isolated text predictors to systems that interact with external tools. It covers three layers: basic tool use, structured function calling, and the Model Context Protocol (MCP) as an industry-wide standard.

## Key claims

1. **LLMs are text-prediction engines** — they have no built-in ability to call APIs, query databases, or perform real-world actions. External capabilities come from the application layer surrounding the model.

2. **Function calling** formalised tool use in mid-2023 when OpenAI added it as a first-class API feature. The model generates a structured JSON request; the application layer validates and executes it; results are fed back for the model to compose a final answer.

3. **ChatGPT Plugins failed** — launched early 2023, deprecated by April 2024 due to poor discoverability, inconsistent quality, and immature security.

4. **The N×M fragmentation problem** — each LLM provider implemented function calling differently (OpenAI, Anthropic, Google all had distinct schemas), requiring custom integrations per provider-tool pair.

5. **MCP solves N×M → N+M** — introduced by Anthropic as an open standard, MCP defines a common protocol with three components: Host (the AI application), Client (communication handler), and Server (lightweight tool wrapper). Each side implements once.

6. **MCP complements function calling** — MCP standardises tool discovery and invocation; function calling is the mechanism by which the model signals intent to use a tool. They are complementary layers.

7. **Adoption was rapid** — OpenAI announced MCP support in 2025, Google DeepMind followed. By late 2025, 10,000+ public MCP servers existed. Anthropic donated the protocol to the Agentic AI Foundation under the Linux Foundation.

8. **Security is the main cost** — every exposed tool expands the attack surface. The first supply-chain attack on MCP servers occurred in September 2025 (a rogue npm package mimicking Postmark).

9. **Context window pressure** — each tool definition consumes tokens, and dozens or hundreds of tools degrade the model's reasoning ability.

10. **Core architectural principle** — the model reasons about what should happen; the application layer controls whether it actually does. This boundary is where security, reliability, and control live.

## Timeline extracted from source

| Date | Event |
|---|---|
| Early 2023 | OpenAI launches ChatGPT Plugins |
| Mid-2023 | OpenAI introduces function calling API |
| April 2024 | OpenAI deprecates ChatGPT Plugins |
| Late 2024 | Anthropic introduces MCP as open standard |
| 2025 | OpenAI, Google DeepMind announce MCP support |
| Sept 2025 | First malicious MCP server supply-chain attack |
| Late 2025 | MCP donated to Agentic AI Foundation (Linux Foundation) |

## Affected pages

- [[Tool Use and Function Calling]] — new concept page
- [[Model Context Protocol]] — new concept page
- [[Agentic Loop]] — new concept page
- [[ByteByteGo]] — new entity page
- [[AI Knowledge Base Overview]] — updated with new domain area

## Raw capture

- `knowledge-base/raw/sources/Connecting LLMs to the Real World Tool Use, Function Calling, and MCP.md`

## Related pages

- [[AI Knowledge Base Overview]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[ByteByteGo]]
