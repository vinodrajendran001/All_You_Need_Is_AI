---
type: entity
entity_kind: tool
created: 2026-05-13
updated: 2026-05-13
tags: [copilot, cli, github, llm, agent]
source_ids:
  - src-2026-05-12-vinod-expert-workshop-copilot-cli
status: active
---

# GitHub Copilot CLI

An interactive terminal assistant built by GitHub that brings LLM-powered coding help directly into the command line. It runs inside a shell session and supports multi-turn conversation, file editing, code search, and command execution.

## Key characteristics

- **Installation**: Distributed as an npm package (`@github/copilot`), typically installed globally inside a WSL or Linux environment.
- **Authentication**: Uses GitHub's device-code OAuth flow via `/login`. Users authenticate at `github.com/login/device` with a generated one-time code.
- **Model selection**: The `/model` command allows switching between available LLMs (e.g., Claude Sonnet, GPT-4o, Claude Opus) during a session.
- **Capabilities**: File reading/editing, shell command execution, code search (grep/glob), sub-agent delegation, and web fetching.
- **Environment**: Designed for WSL/Linux terminals; integrates with VS Code's integrated terminal.

## Why it matters

Copilot CLI represents GitHub's push to make LLM assistance available outside of IDE extensions — directly in the terminal where many developers already work. It bridges the gap between chat-based AI assistants and hands-on coding workflows.

## Related pages

- [[May Expert Workshop - Copilot CLI Setup]]
- [[AI Knowledge Base Overview]]
