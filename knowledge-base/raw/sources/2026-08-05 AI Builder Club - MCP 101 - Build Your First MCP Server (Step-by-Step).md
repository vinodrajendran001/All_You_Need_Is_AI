---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-mcp-101-build-mcp-servers
title: 'MCP 101: Build Your First MCP Server (Step-by-Step)'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/mcp-101-build-mcp-servers
published: '2026-04-16'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# MCP 101: Build Your First MCP Server (Step-by-Step)

## What You'll Learn

By the end of this course, you will:

- **Understand what MCP is** and why it exists — the "USB-C for AI tools" standard
- **Know the 3 component types** — Tools, Resources, and Prompts — and when to use each
- **Build a working MCP server** from scratch in Python (~60 lines)
- **Connect it to Claude Desktop and Cursor** — see your tool called live
- **Use Claude Code to generate MCP servers** — 10-minute workflow for any integration
- **Know which community servers** to install for instant productivity

**Prerequisites:** Basic Python. `pip install mcp requests`. A Claude Desktop or Cursor installation to test with.

**Time:** ~20 minutes to read, ~45 minutes if you build and connect the weather server.

---

## The Problem MCP Solves

Every AI tool used to solve the integration problem differently. Claude had one plugin format. ChatGPT had another. Cursor had its own. If you wanted your database connected to multiple AI tools, you had to build the same integration three times.

**MCP (Model Context Protocol)** is Anthropic's answer to this: a single open standard that any AI client can speak, and any server can implement. Build once, connect everywhere.

Think of it like USB-C for AI tools. One standard connector, infinite devices.

And MCP isn't just an integration standard — it's a business opportunity. Watch how builders are monetizing MCP servers:

---

## What MCP Actually Is

MCP is a protocol — a defined way for an AI client (like Claude Desktop, Cursor, or your own agent) to communicate with an MCP server (a process that exposes tools, data, or prompts).

The architecture is simple:

- **MCP Client**: The AI application (Claude Desktop, Cursor, your agent)
- **MCP Server**: A lightweight process you write that exposes capabilities
- **Transport**: How they communicate (stdio for local servers, HTTP/SSE for remote)

When the AI needs to call a tool — search the web, query a database, read a file — it sends a JSON-RPC message to the MCP server. The server executes the action and returns the result. The AI sees the result and continues reasoning.

---

## The 3 MCP Component Types

Every MCP server exposes its capabilities through three primitive types:

### 1. Tools

Functions the AI can call. This is the most common type.

Examples:

- `search_web(query: str)` — run a web search
- `query_database(sql: str)` — execute a SQL query
- `send_email(to: str, subject: str, body: str)` — send an email

Tools are the core of most MCP servers. They're what the AI actually *does*.

### 2. Resources

Data the AI can read. Think of these as virtual files.

Examples:

- `file://documents/report.pdf` — a document in your filesystem
- `db://customers/recent` — a dynamic view of database records
- `api://github/issues` — live issue list from GitHub

Resources are read-only. The AI can fetch them and use them as context.

### 3. Prompts

Reusable prompt templates the AI can invoke by name.

Examples:

- `code-review-template` — a structured prompt for reviewing PRs
- `bug-report-format` — a template for filing bug reports

Prompts let you standardize how the AI approaches common tasks.

---

## Build a Weather MCP Server in Python

Let's build a real MCP server. This one exposes a `get_weather` tool that fetches current conditions for any city.

### Step 1: Install dependencies

bash

```
pip install mcp requests
```

### Step 2: Write the server

python

```
# weather_server.py
import asyncio
import json
import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

app = Server("weather-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_weather",
            description="Get current weather conditions for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g. 'London', 'New York')"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "get_weather":
        city = arguments["city"]

        # Using wttr.in — free, no API key required
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        weather_summary = {
            "city": city,
            "temp_c": current["temp_C"],
            "temp_f": current["temp_F"],
            "description": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
            "wind_kmph": current["windspeedKmph"]
        }

        return [types.TextContent(
            type="text",
            text=json.dumps(weather_summary, indent=2)
        )]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

That's a complete MCP server. 60 lines of Python.

---

## Connect It to Claude Desktop

Find or create your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add your server:

json

```
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/absolute/path/to/weather_server.py"]
    }
  }
}
```

Restart Claude Desktop. You'll see a hammer icon in the chat interface — that means MCP tools are available. Ask Claude: *"What's the weather in Tokyo?"* and it will call your server automatically.

---

## Connect It to Cursor

In Cursor, go to **Settings → MCP** and add a new server entry:

json

```
{
  "weather": {
    "command": "python",
    "args": ["/absolute/path/to/weather_server.py"]
  }
}
```

Cursor will now be able to call your weather tool in the Composer and chat interfaces.

---

## Use Claude Code to Write MCP Servers

Here's a workflow that saves hours: use Claude Code to write your MCP servers for you.

Open your terminal and run:

bash

```
claude
```

Then describe what you want:

> "Write a Python MCP server that exposes a tool to query a SQLite database. The tool should take a SQL query string and return results as JSON. Use the mcp pip package with Server, list\_tools, and call\_tool. Add proper error handling for SQL errors."

Claude Code will generate the full server, including imports, error handling, and the stdio transport boilerplate. Review it, run it, iterate. This cuts initial MCP server development from an hour to under 10 minutes.

---

## Community MCP Servers Worth Installing

You don't have to build everything yourself. The official MCP servers repository has production-ready servers for the most common integrations:

**[github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)**

Highlights:

- **Filesystem** — Read/write local files with configurable allowed directories
- **GitHub** — Create issues, open PRs, search code, manage repositories
- **Postgres** — Run SQL queries against your database with schema inspection
- **Brave Search** — Web and local search via Brave's API (free tier available)
- **Slack** — Read channels, post messages, search history
- **Google Maps** — Geocoding, directions, place search

Each one ships with an install command and config snippet you can drop straight into Claude Desktop or Cursor.

---

## What You Can Build With MCP

A few directions worth exploring:

- **Personal knowledge base**: MCP server over your Obsidian vault or Notion workspace — Claude can search and reference your notes in any conversation
- **Dev environment agent**: Filesystem + GitHub + terminal MCP servers wired together so Claude can read your codebase, run tests, and open PRs
- **Data analysis assistant**: Postgres/SQLite MCP server so Claude can query your product database directly, no BI tool required
- **Customer support agent**: CRM + ticketing system MCP server so Claude can look up account history and create tickets mid-conversation

---

## Try These Now (3 Exercises)

**Exercise 1 — Build the Weather Server (20 min):** Copy the code above, save it as `weather_server.py`, install dependencies, and connect it to Claude Desktop or Cursor. Ask the AI "What's the weather in Tokyo?" and verify it calls your server. Bonus: add a `get_forecast` tool that returns the 3-day forecast from the same API.

**Exercise 2 — Build a Custom Tool (30 min):** Think of one thing you do repeatedly — look up a Jira ticket, query a database, check a service's status. Build an MCP server that exposes it as a tool. Use the weather server as your template. You'll be surprised how fast it goes once you have the boilerplate.

**Exercise 3 — Use Claude Code to Generate One (10 min):** Open Claude Code in your terminal and describe an MCP server you want: "Write a Python MCP server that exposes a tool to search my local Markdown files by keyword." Review what it generates. Compare the structure to the weather server. This teaches you the generation workflow for rapid MCP development.

---

## Key Takeaways

- **MCP is a protocol, not a framework** — JSON-RPC messages between a client (Claude, Cursor) and a server (your code)
- **Tools, Resources, Prompts** are the three primitives — Tools are the most common (functions the AI can call)
- **A working MCP server is ~60 lines of Python** — the barrier is low
- **stdio transport** for local servers, **HTTP/SSE** for remote — start with stdio
- **Community servers exist** for most common integrations — GitHub, Postgres, Filesystem, Slack
- **Claude Code can generate MCP servers for you** — describe what you want, review, ship

---

## What's Next

You now know what MCP is, how it works, and how to build and connect your first server. The next step is connecting multiple servers together and building agents that use several tools in a single reasoning chain.

**Recommended next reads:**

- [AI Agents 101 — Part 1: What Is an AI Agent?](/blog/ai-agents-101-part-1) — build the agent loop that calls tools like MCP servers
- [AI Agents 101 — Part 2: Give Your Agent Real Tools](/blog/ai-agents-101-part-2) — add web search, code execution, and error recovery
- [5 Levels of Coding Agents](/blog/5-levels-of-coding-agents) — see how MCP fits into progressively autonomous systems

**Go deeper with our courses:**

- [MCP 101 Course](/courses/mcp-course) — full hands-on course: build and deploy MCPs with fastMCP, Cloudflare, auth, and Stripe
- [AI Agent 101](/courses/ai-agent-course) — build research agents with tool use, web scraping, and deep search

If you want to go further — with hands-on sessions, working code, and a community of builders:

👉 [Join AI Builder Club](https://www.aibuilderclub.com/pricing?utm_source=blog&utm_medium=article&utm_campaign=mcp-101-build-mcp-servers)

MCP is an open protocol Anthropic released in late 2024 that lets any LLM (Claude, GPT-4, Gemini, local models) call external tools, query databases, and read resources through a standard interface. Think "USB-C for AI tools" — instead of writing custom integrations for every model, you build one MCP server and any MCP-compatible client can use it. As of 2026, Claude Desktop, Claude Code, Cursor, Continue, Cody, and Zed all support MCP natively.

Function calling is a feature of one specific model API (OpenAI, Anthropic, etc.) — you define functions in your code and the model calls them. MCP is a **transport protocol** that lives between the model and the tools — it standardizes how tools are discovered, described, and called across different clients and models. Practical effect: write a function-calling tool and it only works with that one API. Write an MCP server and it works with every MCP client (Claude Desktop, Cursor, Claude Code, etc.) without changes.

A working MCP server in Python takes ~60 lines of code and roughly 30 minutes from `pip install mcp` to seeing it called from Claude Desktop. Connecting to a real API (Stripe, Linear, your own DB) typically takes another 1–2 hours. The fastest workflow we've seen: ask Claude Code to scaffold an MCP server for an API, paste the API's OpenAPI spec, and it generates the full server in under 10 minutes.

**Tools** are functions the LLM can call (e.g. `create_invoice`, `search_database`). **Resources** are read-only data the LLM can pull into context (e.g. a Notion page, a database schema). **Prompts** are reusable prompt templates the user can invoke (e.g. `/summarize-pr`). Most servers only need Tools. Add Resources when you have static or query-able data the model should reference. Add Prompts when you have repeatable workflows your team uses.

No — official SDKs exist for Python, TypeScript, and (community) Go, Rust, Java, C#. Python is the fastest to prototype because the ecosystem (`mcp`, `fastmcp`) is most mature. TypeScript is a strong choice if you're already in a Node.js stack. The protocol itself is JSON-RPC over stdio (or HTTP/SSE), so you can implement it in any language that can read/write JSON.

Claude Code reads MCP server configs from `~/.claude/mcp.json` (global) or `.claude/mcp.json` in your project (per-project, version-controlled). Add a server to that file, restart Claude Code, and the new tools are available in every session. This is how teams give Claude Code access to internal tools (Linear, Notion, internal APIs) without modifying CLAUDE.md or the codebase. See our [Claude Code beginner tutorial](/blog/claude-code-tutorial-beginners) for the setup workflow.

Yes — MCP servers run with the permissions of whatever process launched them. A malicious server could read files, call APIs, exfil secrets. Three rules: (1) **Only install MCP servers from sources you trust** — official Anthropic/community list or your own code, (2) **Scope credentials tightly** — give each server its own API key with minimum permissions, (3) **Review the server's tools list** before enabling it; the tool descriptions tell you exactly what the model can call.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
