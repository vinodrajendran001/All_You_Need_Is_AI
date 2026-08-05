---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-karpathy-agents-md-framework
title: 'Karpathy''s agents.md: What It Is and Why It Matters'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/karpathy-agents-md-framework
published: '2026-06-09'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Karpathy's agents.md: What It Is and Why It Matters

People are already searching for "karpathy agents.md" - even though Andrej Karpathy hasn't published one yet.

That tells you something. His `claude.md` guidelines - four rules for how he runs Claude Code - became the most-cited CLAUDE.md template in the ecosystem. The [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) repo that packages them sits at 111K stars as of May 2026. Now people are anticipating the next one.

So: what would Karpathy's agents.md look like? And what can we learn from thinking through it?

## Why agents.md Would Be Different From claude.md

Karpathy's `claude.md` was about *using* an AI coding assistant. Four principles for how you interact with Claude during development:

| Principle | Addresses |
| --- | --- |
| **Think Before Coding** | Wrong assumptions, hidden confusion, missing tradeoffs |
| **Simplicity First** | Overcomplication, bloated abstractions |
| **Surgical Changes** | Orthogonal edits, touching code you shouldn't |
| **Goal-Driven Execution** | Leverage through tests-first, verifiable success criteria |

An `agents.md` would be about *building* agents - autonomous systems that take actions in the world without a human in the loop. That's a fundamentally different challenge. The failure modes are different. The trust boundaries are different. The prompting philosophy is different.

## The AGENTS.md Standard Today

Before we speculate on Karpathy's version, it's worth noting that `AGENTS.md` already exists as a formal standard. It's the [cross-tool open standard](https://agents.md) stewarded by the Linux Foundation's Agentic AI Foundation.

These tools read `AGENTS.md` natively:

- OpenAI Codex
- Cursor
- Windsurf
- GitHub Copilot
- Aider
- Devin
- Amp
- opencode
- RooCode

Claude Code reads `CLAUDE.md`. Gemini CLI reads `GEMINI.md`. The recommended approach: write one `AGENTS.md` and symlink the tool-specific filenames to it.

## What We Know About Karpathy's Thinking on Agents

Karpathy has been more public about agentic engineering than almost any other researcher. From his talks and writing, clear themes emerge:

### 1. Agents fail at the boundaries, not the center

Most agent tasks fail not because the core capability doesn't work, but because of what happens at the edges: handoffs between tools, ambiguous instructions, unexpected input formats, permission boundaries. An agents.md would likely focus heavily on defining these boundaries explicitly before building.

### 2. Human oversight scales with stakes, not with complexity

Karpathy has talked about agentic systems that run with different levels of autonomy depending on what they're doing. Low-stakes actions (reading files, running tests) can be fully autonomous. High-stakes actions (deploying to production, sending emails) need a human checkpoint.

### 3. Memory is the core unsolved problem

In every discussion of agentic systems, Karpathy returns to memory. How does an agent maintain context across long tasks? How does it know what it's already tried? How does it update its internal model when it discovers it was wrong? The emerging category of [agent memory tools](https://www.aibuilderclub.com/blog/ai-coding-agent-memory-agentmemory) is tackling this.

### 4. Tools are where agents go wrong

Every tool an agent can use is a failure surface. Bad tool definitions, missing error handling, tools with overlapping capabilities - these cause the majority of real-world agent failures.

## What a Karpathy agents.md Would Contain

Based on his public writing, talks, and the existing repos that package his philosophy, here's our best reconstruction:

### Rule 1: Define the permission boundary before you write a line of code

What can this agent read? What can it write? What can it never touch? Make this explicit in the system prompt and in the code. Karpathy's philosophy has always been: be concrete before you're clever.

code

```
# Permission Boundary
READ: src/**, tests/**, docs/**
WRITE: src/**, tests/**
NEVER: .env*, credentials/**, production configs
HUMAN_CHECKPOINT: deploy/**, email/**, billing/**
```

### Rule 2: Every tool call should be reversible or auditable

If an agent takes an action you can't undo, that action needs a human checkpoint. If it can be undone, log it thoroughly enough that you could replay or reverse the sequence. This is the agentic version of his spec-first philosophy.

### Rule 3: Fail loudly and stop

Agents that fail silently and continue are more dangerous than agents that fail loudly and stop. Build in explicit failure states: if the agent encounters something outside its defined scope, it should surface that to a human rather than improvising. Improvisation in agents scales the wrong way.

### Rule 4: The memory file is the agent's source of truth

Just as `claude.md` is a living skills file that captures what Claude knows about your codebase, an agents.md would prescribe a memory file - a structured document that the agent reads at the start of every session and writes to at the end of every session. Not hallucinated context. Not ephemeral state. A real file.

## The agents.md Gap That Exists Right Now

The principles above aren't hypothetical. Builders who ship production agents have converged on most of them independently. The [FerroxLabs/agents-md](https://github.com/FerroxLabs/agents-md) repo ("Drop-in AGENTS.md that makes every coding agent behave like a senior engineer") already synthesizes Karpathy's four principles and Boris Cherny's Claude Code workflow into a single file.

But these are scattered across repos, Discord threads, and private Slack channels. Karpathy's claude.md worked because it took implicit best practices and made them explicit in a shareable, citable format.

That gap is what people are searching for when they type "karpathy agents.md" into Google.

## What to Do Right Now

If you're building agents, here's a practical framework based on what we think agents.md would recommend:

1. **Write a permission boundary document first.** Before any code, write one page: what this agent can read, write, call, and never touch. Review it with someone else.
2. **Make every significant action auditable.** Log inputs, outputs, and the reasoning for every tool call. You should be able to reconstruct exactly what the agent did and why.
3. **Build in human checkpoints at the edges.** The start of a task (is this the right task?), at major decision points (is this the right approach?), and before irreversible actions (are you sure?).
4. **Maintain a memory file.** A simple markdown file the agent reads and writes. What it learned about your project. What it tried that didn't work. What patterns it's found useful. Not in the model's context window - in a file.

When Karpathy actually publishes an agents.md, it will be shareable, specific, and immediately actionable. Until then, these four rules are the closest approximation we have - and they're already being used by production agent builders today.

AGENTS.md is a cross-tool standard for AI agent instructions, stewarded by the Linux Foundation's Agentic AI Foundation. It is read natively by Codex, Cursor, Windsurf, Copilot, Aider, Devin, Amp, opencode, and RooCode. Claude Code reads CLAUDE.md, and Gemini CLI reads GEMINI.md - you can symlink all three to share the same file.

Not yet. Karpathy posted observations about LLM coding pitfalls on X in late 2025. Jiayuan Chang turned those into a four-principle CLAUDE.md (multica-ai/andrej-karpathy-skills) which reached 111K stars. People are now searching for a Karpathy agents.md, anticipating he will publish guidelines for building agents.

CLAUDE.md is Claude Code-specific instructions loaded at session start. AGENTS.md is the cross-tool equivalent supported by most other AI coding agents. Both serve the same purpose: giving the agent behavioral guidelines and project context. You can symlink them to use one file for all tools.

Think Before Coding (avoid wrong assumptions), Simplicity First (no overcomplication), Surgical Changes (only touch what needs changing), and Goal-Driven Execution (tests-first, verifiable success criteria). These address the most common LLM coding failure modes.

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
