---
type: entity
created: 2026-11-20
updated: 2026-11-20
entity_kind: person
tags:
  - entity
  - person
  - web-platform
  - agent-harness
source_ids:
  - src-2026-11-17-paul-kinlan-voice-harness
  - src-2026-11-19-paul-kinlan-chrome-extensions-prompts
status: active
---

# Paul Kinlan

## What it is

Paul Kinlan is a developer who writes about AI and the web platform on his blog, aifoc.us. Both posts
in the vault describe open-source personal projects he built and published on GitHub: **Voicebox**
(`PaulKinlan/voicebox`), a voice-driven agent harness with a browser interface and a local daemon, and
**Prompt in a Box** (`PaulKinlan/prompt-in-a-box`), which turns a Markdown prompt into a Chrome
extension. Prompt in a Box runs agent-do, an agent loop he has written about on his blog, as its
loop.

## Why it matters here

His posts are first-person engineering accounts of putting agents inside browser primitives: OPFS
storage, the File System Access API, sandboxed iframes, WebMCP, Chrome permissions and events. They
are useful to [[LLM-Native Extensible Software]] and [[Agent Security and Governance]] because he
states where his own isolation stops, and to [[Programmatic Tool Calling]] for a browser-side Code
Mode that can save generated scripts for later runs.

## Notes

- [[Paul Kinlan - My Voice Harness Is My New Operating System]] (2026-11-17): Voicebox with
  Gemini-3.8-live; model-written mini-apps, declarative extensions over six primitives, delegation
  to other coding agents over ACP, and an open admission that voice and screen input have no
  injection safeguard yet. See [[Real-Time Voice AI]] and [[Agent Delegation]].
- [[Paul Kinlan - My Chrome Extensions Are Just Prompts]] (2026-11-19): extensions as `prompt.md`
  plus manifest and config over one generic runtime; permissions decide which of "about 50" tools
  exist; `code_mode`, saved scripts, pre-recorded undo, and per-run traces.
- Both are prototypes described by their author. Neither reports measured performance; both name
  prompt injection from web content as unsolved.
- The posts do not state his employer, and the vault has not recorded one.

## Related pages

- [[LLM-Native Extensible Software]]
- [[Agent Security and Governance]]
- [[Programmatic Tool Calling]]
- [[Real-Time Voice AI]]
- [[Agent Delegation]]
- [[Paul Kinlan - My Voice Harness Is My New Operating System]]
- [[Paul Kinlan - My Chrome Extensions Are Just Prompts]]
