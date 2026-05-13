---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags: [agents, llm, tool-use, loop]
source_ids:
  - src-2026-05-04-bytebytego-llm-tool-use-mcp
status: active
---

# Agentic Loop

The iterative cycle by which an LLM-powered application plans, acts, observes, and responds — potentially over multiple rounds of tool calls within a single user request.

## How it works

1. **User prompt** arrives with a list of available tool definitions.
2. The **model reasons** about whether it can answer directly or needs external information.
3. If it needs a tool, it generates a **structured function call** (JSON) instead of a final answer.
4. The **application layer** validates and executes the call, returning results as a new message.
5. The model **incorporates the result** and either produces a final response or issues another tool call.
6. Steps 3–5 repeat as needed.

This multi-step looping is the foundation of **AI agents** — systems where the model autonomously plans and executes complex tasks by chaining multiple tool calls in sequence.

## Example

A user asks: *"Find me flights to Tokyo and check the weather there."*

1. Model calls `search_flights(destination="Tokyo")` → gets flight options.
2. Model calls `get_weather(location="Tokyo")` → gets current conditions.
3. Model synthesises both results into a single natural-language response.

## Why the separation matters

The model decides *what* should happen. The application layer decides *whether* it happens. This boundary allows:
- **Access control** — restrict which tools are available.
- **Validation** — check arguments before execution.
- **Human-in-the-loop** — require approval for high-stakes actions.

## Related pages

- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[ByteByteGo - Connecting LLMs to the Real World]]
