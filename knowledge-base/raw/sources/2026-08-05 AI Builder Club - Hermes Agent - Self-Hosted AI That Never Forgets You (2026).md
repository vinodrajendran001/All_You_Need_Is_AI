---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-hermes-nous-research-self-improving-agent
title: 'Hermes Agent: Self-Hosted AI That Never Forgets You (2026)'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/hermes-nous-research-self-improving-agent
published: '2026-06-02'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Hermes Agent: Self-Hosted AI That Never Forgets You (2026)

**Hermes Agent** is a self-hosted, open-source autonomous AI agent built by Nous Research that accumulates memory across every session, runs scheduled tasks while you sleep, and writes its own reusable skills from experience. Released February 25, 2026, it crossed 175,000 GitHub stars in under four months - not because it is another chat wrapper, but because it solves the persistent memory and async scheduling problem that Claude Code, Cursor, and every other session-based AI tool still has.

Who this is for, upfront: Hermes is the right tool if you work across multiple projects, want an agent on your own infrastructure, and care about persistent memory and async scheduling. If your primary need is coding assistance within a single project, Claude Code is still better at that specific job. Read both sections before deciding.

Watch the full breakdown of how this agent self-evolves:

## What Is Hermes Agent?

Hermes Agent is a persistent daemon built by Nous Research (the team behind the Hermes, Nomos, and Psyche model families). It is not a chat interface wrapped around an API. It is an autonomous agent that:

- Runs on your server (or a $5 VPS) and remembers who you are across every session
- Fires scheduled cron jobs while you are offline and delivers results to your messaging apps
- Writes and saves its own skills automatically from operational experience
- Connects to 16+ messaging platforms (Telegram, Discord, Slack, Signal, email, and more)
- Works with any LLM provider: Anthropic, OpenAI, Google, DeepSeek, OpenRouter, GitHub Copilot, or local models via Ollama

The community-maintained [Hermes WebUI](https://github.com/nesquena/hermes-webui) adds a browser-based three-panel interface: sessions on the left, chat in the center, workspace file browser on the right. Access it via SSH tunnel or Tailscale from anywhere, including your phone.

## How Does Hermes Memory Work?

Hermes uses a three-tier memory architecture designed to run anywhere from a $5 VPS to a GPU cluster, without requiring an external vector database or RAG pipeline.

Here is what the memory problem looks like in practice with most AI coding tools:

- **Session 1:** You explain your project structure, naming conventions, current sprint goals, preferred testing approach, and the fact that your staging database is read-only.
- **Session 2:** You explain all of it again.
- **Session 20:** You are still explaining the same things.

Claude Code has CLAUDE.md for project context, which helps within a single project. But that context does not follow you across projects, and it does not accumulate new knowledge automatically from what you actually do.

**Hermes solves this with three tiers:**

| Tier | Mechanism | What It Stores | Constraint |
| --- | --- | --- | --- |
| 1 - High-Signal State | USER.md + MEMORY.md | Your profile, preferences, project conventions, environment quirks | 1,375 + 2,200 chars (guaranteed immediate context) |
| 2 - Cross-Session Search | SQLite + FTS5 | Full conversation history, searchable with keyword + LLM summarization | No hard limit |
| 3 - External Integration | Optional providers | mem0, custom vector stores, or external knowledge bases | Provider-dependent |

A concrete example: you spend two hours on a Tuesday debugging a specific infrastructure issue - unusual nginx config interacting with a Docker network. Hermes logs that in Tier 2. On Thursday, when you hit a related issue on a different project, you say "remember that nginx Docker bug from Tuesday" and Hermes retrieves the context. No re-explaining. No hunting through old chat history.

The Tier 1 files (USER.md and MEMORY.md) are loaded into every single session with zero retrieval latency. The agent nudges itself to persist important observations there. This is fundamentally different from probabilistic vector search - it is guaranteed context every time.

## Self-Improving Skills: What It Actually Means

Most agents use skills you define. Hermes writes skills from what it observes. Skills are stored as readable Markdown files on your machine - no proprietary format, no cloud dependency.

If you repeatedly ask Hermes to do the same complex multi-step task - say, pulling GitHub issue summaries, formatting them, and sending a daily digest to Slack - it encodes that process as a reusable skill after seeing the pattern. The next time you need it, it is already there. Nous Research's internal benchmarks claim agents with 20+ self-created skills complete similar tasks 40% faster than fresh instances (40% less token consumption and wall-clock time, not "40% better output").

This is meaningfully different from Claude Code's skill system. Claude Code's .claude/skills/ loads skills you authored and committed to your repo. Hermes generates skills from its own operational history. One is explicit engineering; the other is emergent automation.

**Our take:** Self-improving skills sound impressive but are also where you should apply the most skepticism. An agent that writes its own procedures needs human review before those procedures run in production. Treat auto-generated skills as drafts that need your approval, not trusted automation. The feature is genuinely useful - just not a reason to give Hermes unreviewed access to anything sensitive.

## Scheduled Tasks: The Use Case That Separates Hermes From Claude Code

Hermes has a built-in scheduler with cron syntax. You define recurring autonomous tasks, and Hermes executes them on your server 24/7, delivering results to your messaging app of choice.

Here is a real workflow you can set up in under 10 minutes:

You want a daily Telegram message at 8am with: new GitHub issues opened overnight, any PRs sitting in review for more than 24 hours, and the top Hacker News post mentioning your product name.

In Hermes, you register that via the `/api/jobs` endpoint with cron syntax. It runs while you sleep. You wake up to a summary in Telegram. No manual check. No separate n8n workflow. No Zapier subscription.

Claude Code cannot do this. It executes tasks you initiate in a session. Hermes handles the monitoring, scheduling, and async delivery layer that most builders currently string together from three separate tools.

## How Hermes Compares to Claude Code

These tools are not direct competitors. They solve adjacent problems. Use this table to decide which fits your workflow:

| Capability | Claude Code | Hermes Agent |
| --- | --- | --- |
| Code editing and generation | Excellent (purpose-built) | Good (delegates to Claude Code or Codex) |
| Persistent memory across projects | Partial (CLAUDE.md, project-scoped) | Yes (three-tier, cross-session, cross-project) |
| Scheduled background tasks | No | Yes (built-in cron on your server) |
| Mobile access via messaging apps | Limited | Yes (16+ platforms) |
| LLM provider choice | Claude only | Any provider (Anthropic, OpenAI, Google, DeepSeek, local) |
| Self-improving skills | No | Yes (with human review recommended) |
| Orchestrating other agents | Limited | Yes (can spawn Claude Code sessions as subagents) |
| Self-hosted / data sovereignty | No (cloud-managed) | Yes (runs on your infrastructure) |
| Open source | No | Yes (MIT license) |

**The most interesting integration pattern:** Hermes receives a task via Telegram, spawns a Claude Code session to do the actual coding work, and returns the result to you - all while you are away from your desk. Each tool doing what it is actually good at.

## How to Get Started With Hermes Agent

The official one-line installer handles setup in about 15 minutes:

code

```
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
```

The setup command walks you through connecting your preferred LLM provider:

| Provider | Best For | Setup Method |
| --- | --- | --- |
| Nous Portal | Zero-config start | OAuth via hermes model |
| OpenRouter | Multi-model experimentation | API key |
| Anthropic | Claude models | OAuth or API key |
| GitHub Copilot | Existing subscription | OAuth via hermes model |
| Custom Endpoint | Local models (Ollama/vLLM) | Base URL + API key |

For the web interface, the community-maintained Hermes WebUI:

code

```
git clone https://github.com/nesquena/hermes-webui.git
cd hermes-webui
python3 bootstrap.py
```

The bootstrap detects and installs Hermes Agent if missing, sets up the web server, and opens an onboarding wizard. For a persistent server setup:

code

```
./ctl.sh start    # background daemon
./ctl.sh status   # PID, uptime, port, health
./ctl.sh logs --lines 100
./ctl.sh stop
```

Docker (pre-built amd64 + arm64 images):

code

```
cp .env.docker.example .env
docker compose up -d
# Open http://localhost:8787
```

Requires Linux, macOS, or WSL2.

## Who Should Use Hermes Agent

Hermes is the right tool if:

- You work across multiple projects and want one agent that tracks context across all of them
- You want scheduled monitoring and async task execution delivered to your phone
- You want to stay on your own infrastructure with full data sovereignty
- You use multiple AI providers and want a provider-agnostic interface
- You want an agent that gets measurably better at your specific workflows over time

Hermes is probably not the right tool if:

- Your primary need is coding assistance within a single project (Claude Code is purpose-built for this)
- You prefer managed infrastructure over self-hosting
- You do not want to maintain a server process

## Is Hermes Ready for Production?

For personal workflows - daily summaries, monitoring, cross-project memory, async task delivery to your phone - yes, it is stable enough. 390+ contributors, 175K+ stars, latest release v2026.5.29.2, actively maintained with CI across Python 3.11/3.12/3.13.

For mission-critical automation or anything touching sensitive data - treat it as maturing, not mature. Review auto-generated skills before enabling them. Use password auth and keep it behind a tunnel or VPN. Do not expose the web UI publicly without authentication.

## The Open Source Signal

175,000+ stars in under four months reflects genuine demand for persistent, self-hosted agents that accumulate knowledge over time. The category is real. Hermes is the most complete open-source implementation of it available today.

MIT license. 390+ contributors. Actively maintained with a public roadmap. The Hermes WebUI community project adds another 11,500+ stars and 140 contributors building the browser interface.

For builders combining Hermes with Claude Code for async workflows, that is an active discussion thread in the AI Builder Club community.

Hermes Agent is a self-hosted, open-source autonomous AI agent built by Nous Research (the team behind the Hermes, Nomos, and Psyche model families). Released February 25, 2026, it runs as a persistent daemon on your own infrastructure, accumulates memory across sessions, runs scheduled cron tasks, connects to 16+ messaging platforms, and writes its own reusable skills from experience. It works with any LLM provider including Anthropic, OpenAI, Google, DeepSeek, and local models via Ollama.

Claude Code excels at coding tasks within a single project session. Hermes solves a different problem: persistent memory across all projects and sessions, scheduled background tasks (cron) that run while you sleep, delivery to 16+ messaging apps, and self-improving skills that the agent writes from its own experience. The most interesting integration pattern is using both together: Hermes receives a task via Telegram, spawns a Claude Code session to handle the coding, and returns results to you asynchronously.

Yes. Hermes Agent is MIT-licensed and free to install. You pay only for the LLM tokens you consume from your chosen provider (Anthropic, OpenAI, Google, DeepSeek, OpenRouter) or use a local model via Ollama at zero cost. There is no subscription fee. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure.

Hermes uses a three-tier memory architecture. Tier 1: USER.md (1,375 chars) and MEMORY.md (2,200 chars) - high-signal state files loaded into every session with guaranteed immediate context. Tier 2: SQLite with FTS5 keyword search and LLM summarization for cross-session historical recall. Tier 3: Optional external provider integration. This means you can say "remember that bug we fixed last Tuesday" and the agent retrieves that context without re-explaining.

Yes. Hermes has a built-in scheduler with cron syntax via the /api/jobs endpoint. You define recurring tasks (check GitHub issues, run standup summaries, monitor URLs) and Hermes executes them on schedule, delivering results to your messaging app of choice (Telegram, Discord, Slack, Signal, and 12+ others). This runs 24/7 on your server while you are offline.

Run: curl -fsSL <https://hermes-agent.nousresearch.com/install.sh> | bash. Then run hermes setup to configure your LLM provider. For a web interface, use the community-maintained Hermes WebUI (github.com/nesquena/hermes-webui) which adds a browser-based chat with session list and file browser. Docker images are available for both amd64 and arm64.

Hermes connects to 16+ messaging platforms including Telegram, Discord, Slack, Signal, email, and more. You can talk to your agent from your phone while it works on a cloud VM. The agent identity, skills, and memory are the same regardless of which messaging surface you use.

For personal workflows (daily summaries, monitoring, cross-project memory, async task delivery) - yes, it is stable. 390+ contributors, 175K+ stars, latest release v2026.5.29.2, actively maintained. For mission-critical automation or sensitive data - treat it as maturing. Review auto-generated skills before enabling them, use authentication, and keep it behind a VPN or SSH tunnel.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
