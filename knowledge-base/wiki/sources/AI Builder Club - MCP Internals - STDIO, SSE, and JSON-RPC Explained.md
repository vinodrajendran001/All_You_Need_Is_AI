---
type: source-summary
created: 2026-08-05
updated: 2026-08-26
source_id: src-2026-08-05-aibuilderclub-mcp-internals-client-server
source_title: "MCP Internals: STDIO, SSE, and JSON-RPC Explained"
source_author: AI Builder Club
source_url: https://www.aibuilderclub.com/blog/mcp-internals-client-server
tags: [source/summary, ai-agents, ai-builder-club]
source_ids:
  - src-2026-08-05-aibuilderclub-mcp-internals-client-server
status: active
---

# AI Builder Club - MCP Internals: STDIO, SSE, and JSON-RPC Explained

## Summary

This article demystifies MCP by tracing what happens between a client configuration and a completed tool call. A local server configuration is described as a command line represented in JSON: the client starts a child process, discovers its tools, sends the tool catalog with the user request to the model, translates the model's structured intent into a JSON-RPC call, appends the result to the conversation, and repeats until the model can answer.

It contrasts STDIO for local child processes with SSE over HTTP for remote servers and explains the shared JSON-RPC 2.0 request/response format. It also identifies two ways clients expose tools to models: native function-calling APIs or a system-prompt convention that asks the model to emit parseable text. The latter expands model compatibility but can consume substantial context and be more fragile.

## Key claims

- An MCP server is an ordinary process or remote endpoint; the protocol's value comes from standard messages and discovery, not hidden runtime magic.
- JSON-RPC request IDs connect responses to calls, while methods such as `tools/list` and `tools/call` implement the common tool path.
- The model proposes an action, but the client routes and executes it; this separation is central to safety and observability.
- Multi-step agent behavior is repeated model-call → tool-call → observation cycles.
- Native function calling is generally more structured, while prompt-encoded tool protocols work with more models at the cost of tokens and format reliability.
- Pinning or running a reviewed local server copy can improve reproducibility and reduce supply-chain drift.

## Why it matters

The source gives [[Model Context Protocol]] a wire-level explanation and directly connects it to [[Agentic Loop]] and [[Tool Use and Function Calling]]. It also shows why client and harness design affect model compatibility, context cost, error handling, and security even when the underlying MCP server is unchanged.

## Tensions / open questions

- Transport support is evolving, so the article's STDIO/SSE framing may not cover newer protocol transports or deprecations.
- The quoted context overhead for prompt-based clients is an observed example, not a universal benchmark.
- “Process isolation” is not a sufficient security model when the child process inherits broad filesystem and network permissions.

## Affected pages

- [[AI Builder Club - Build AI Agents]]
- [[Model Context Protocol]]

## Citations

- Raw capture: [[2026-08-05 AI Builder Club - MCP Internals - STDIO, SSE, and JSON-RPC Explained]]
- Canonical URL: [https://www.aibuilderclub.com/blog/mcp-internals-client-server](https://www.aibuilderclub.com/blog/mcp-internals-client-server)

## Raw capture

- [[2026-08-05 AI Builder Club - MCP Internals - STDIO, SSE, and JSON-RPC Explained]]

## Related pages

- [[Model Context Protocol]]
- [[Agentic Loop]]
- [[Context Engineering]]
- [[AI Builder Club - MCP 101 - Build Your First MCP Server (Step-by-Step)]]
- [[AI Builder Club - MCP Security - 6 Attack Vectors and a 5-Step Audit]]
- [[Coding Agent Harness]]
- [[Tool Use and Function Calling]]

