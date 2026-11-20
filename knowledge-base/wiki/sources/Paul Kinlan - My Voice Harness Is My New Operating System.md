---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-17-paul-kinlan-voice-harness
source_title: "My voice harness is my new operating system"
source_author: "Paul Kinlan"
source_url: "https://aifoc.us/voice-harness/"
tags:
  - source/summary
  - voice-ai
  - coding-agents
  - webmcp
  - extensibility
  - agent-security
source_ids:
  - src-2026-11-17-paul-kinlan-voice-harness
status: active
---

# My Voice Harness Is My New Operating System

## Summary

Paul Kinlan describes Voicebox, a personal open-source project: an agent harness, "like Claude or
the pi-cli", that he drives by voice. He says the post is less about voice than about the web runtime
he built around it, which he increasingly treats as an operating layer, and about what the web
platform lacks for such a thing.

The design has three parts. A browser page (the "room") is the user interface. A small local Node
daemon runs the agent loop, holds the API key, keeps the live session open, and executes every tool
call. The third part is Gemini-3.8-live in the cloud, which he calls "a game-changer" because it
responds quickly, can be interrupted, and can write code. From that base the harness grew file
management, model-written mini-apps, screen sharing, declarative extensions, delegation to other
coding agents, and local shell commands. Kinlan is candid about the security gap: anything that
reaches the voice loop, including a shared screen or a web page carrying a prompt injection, can lead
to tool calls on harnesses with access to his email and machine, and "I don't have any safeguards
for this yet."

This is a single developer's account of his own prototype. No performance, latency, or reliability
figures are reported, and he notes that "this project can be pretty expensive to run".

## Key claims

### Files and project instructions

- A project can live in the browser's private storage (OPFS), a folder picked through the File System
  Access API, or a folder on disk. "The model doesn't know or care which." A router decides whether
  the daemon or the page performs a write. The page re-checks that the path stays inside the project
  and logs the write to the project's audit log. If neither side can reach the project, the call is
  refused with a reason "instead of failing quietly".
- The nearest `AGENTS.md`, walking up to the root, goes into the voice model's system prompt.

### Mini-apps: model-written software that stays

- A mini-app is a single HTML file the model writes and launches with `launch_mini_app`. The daemon
  saves it, so "next week I can say 'open the calculator' and it comes back."
- Because the code is model-written it runs "two iframes deep": a same-origin bridge frame checks
  every message, and the inner frame is sandboxed with an opaque origin (no cookies, no storage, no
  access to the daemon's API) and a content security policy that blocks the network by default.
- Mini-apps expose tools through WebMCP: an app calls `document.modelContext.registerTool()` with a
  name, input schema, and function, and the model calls it like any other tool. Kinlan's summary:
  "functionality built by the LLM being usable by the LLM in future interactions".

### Screen sharing

- Gemini-3.8-live accepts video, so the browser's `getDisplayMedia` screen capture lets the harness
  co-work on what is on screen. He reports UI issues and a bug in continuous screen capture.

### Extensions are data, not code

- An extension is a JSON descriptor over **six** daemon primitives: `http-get`, `read-file`,
  `write-file`, `list-files`, `now`, and `wasm`. The Brave Search extension says, in effect, make a
  GET to the API "at most 20 times a session"; its key placeholder is filled from the daemon's
  environment, "so the key never reaches the page or the model".
- Every extension, whether from the catalogue, sideloaded, or proposed by the model, passes the same
  admission check and then needs his approval. "The model can propose a tool, but the only thing a
  proposal can do is write a file."
- WASM tools are pinned by SHA-256, re-hashed on every call, have no imports, and run in a worker
  thread with memory and time limits.

### Delegation and local commands

- One tool, `delegate_task(agent, task)`, hands work to Claude Code, Agy, Pi, or Codex over ACP (the
  Agent Client Protocol), returning a handle at once so the voice can keep talking. Voicebox answers
  the delegate's permission requests from its declared tool list and whether every path stays inside
  the project. The folder is snapshotted before and after, so the result lists created, changed, and
  deleted files; Voicebox strips its own model keys from the delegate's environment.
- `run_command` runs a shell command in the project folder with a **20 second** deadline and **64
  KB** of output, and only for a session carrying "real room authority" (a paired bearer, the
  session cookie from a one-time URL the daemon prints at startup, or the room's token, "not just a
  local Origin header"). "What it isn't is a sandbox. It runs as me."

### What the web platform is missing

- What works: browser file storage APIs, WebMCP ("it just works"), and media APIs.
- What is missing: a secure "bridge to the system" (without one, people build their own daemons,
  "which could be a recipe for disaster"); a "bridge to harnesses" so a page can delegate to the
  user's preferred agent, since ACP runs over stdio and needs a local service; and real-time **local
  speech models**, for privacy and cost.
- His conclusion: "Agent Harnesses move more and more into Operating System territory."

## Why it matters

The vault's [[Real-Time Voice AI]] page is about transport and model architecture for spoken
conversation. This source puts a live voice model in front of a general agent harness and shows the
problem moving to authority: what a spoken request may cause on the user's machine. For
[[LLM-Native Extensible Software]] it is a worked example of Morrell's trusted-host split, with
model-written artifacts that persist, run isolated, and expose narrow capabilities. Its extensions,
declarative data over six primitives with digest-pinned WASM, are a stricter design than the
unsandboxed mods the page also records. For [[Agent Delegation]] it adds cross-harness delegation
over a protocol, with a before-and-after file snapshot as the receipt. For
[[Agent Security and Governance]] it is an honest statement of the confused-deputy risk that voice
and screen input add: the usual answer is per-action confirmation, and he has not worked out how to
do that by voice.

## Tensions / open questions

- **Sandboxed apps, unsandboxed commands.** Mini-apps and WASM tools are tightly isolated, while
  `run_command` and delegated harnesses run with the user's full rights. Untrusted input can still
  reach the unsandboxed parts through the voice loop or the screen.
- **Approval by voice.** The post names confirmation as the usual mitigation and leaves open how to
  make it work without a screen-and-click step.
- **No measurement.** Usefulness, cost, and the reliability of the voice model writing code are
  described, not measured.
- **Does the web layer earn its place?** Kinlan himself says "It's not clear to me that this needs to
  be at the web-layer"; much of the daemon exists because browsers cannot yet do these things.

## Affected pages

- [[Real-Time Voice AI]]
- [[LLM-Native Extensible Software]]
- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Paul Kinlan]]

## Raw capture

- [[knowledge-base/raw/sources/My voice harness is my new operating system]]

## Citations

- Canonical URL: <https://aifoc.us/voice-harness/> (the captured link carried a
  `utm_source=tldrnewsletter` parameter, removed here).
- By Paul Kinlan on aifoc.us, published November 17, 2026; captured November 18, 2026. The code is
  linked from the post as `PaulKinlan/voicebox` on GitHub.

## Related pages

- [[Real-Time Voice AI]]
- [[LLM-Native Extensible Software]]
- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[Paul Kinlan]]
- [[Paul Kinlan - My Chrome Extensions Are Just Prompts]]
- [[Model Context Protocol]]
- [[AI Builder Club - WebMCP Tutorial - How Agents Use Websites as Tools]]
- [[Generative User Interface]]
- [[Computer Use Agents]]
- [[Coding Agent Harness]]
