---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-19-paul-kinlan-chrome-extensions-prompts
source_title: "my chrome extensions are just prompts"
source_author: "Paul Kinlan"
source_url: "https://aifoc.us/my-chrome-extensions-are-just-prompts/"
tags:
  - source/summary
  - extensibility
  - browser-agents
  - programmatic-tool-calling
  - agent-security
  - observability
source_ids:
  - src-2026-11-19-paul-kinlan-chrome-extensions-prompts
status: active
---

# My Chrome Extensions Are Just Prompts

## Summary

Paul Kinlan describes an update to Prompt in a Box, his open-source project for building Chrome
extensions whose program is a Markdown prompt. A prompt as short as `De-duplicate my tabs` becomes
an extension; more detailed prompts say when it runs, what it should skip, and how it behaves. The
new Studio edits the icons, permissions, and parameters, with an agent helping refine the prompt.

His argument is that a Chrome extension is already a good container for an agent: "It's a zip file
with a manifest. It has a permission model, a sandbox, an event system that wakes it up and a way to
distribute it". An agent is then "an extension with a `prompt.md`". Every extension is the same
generic runtime plus three files, and "you swap the prompt and the same code becomes a different
tool". The post explains how the runtime handles speed, repeatability, user interface, undo,
tracing, and untrusted web content; UI, undo, tracing, and speed are among the things wanted while
sharing it with teams.

This is a first-person account of a personal prototype that has been shared with "some teams". It
reports no measured results beyond one qualitative speed-up. The extensions cannot be published to
the Chrome Web Store because they rely on dynamic code execution, and load only in developer mode.

## Key claims

### Three files and a generic runtime

- `prompt.md` is "the program"; `manifest.json` is "what the extension is allowed to reach.
  Permissions are the contract"; `config.json` holds the allowed models, schedule, settings, and UI
  choices.
- The service worker runs the agent-do loop and exposes "about 50" Chrome APIs as tools (for example
  `tab_list`, `bookmark_search`, `history_search`). Each tool is gated by a Chrome permission: "if the
  manifest doesn't grant `bookmarks`, the bookmark tools are simply not in the list that the model
  sees".
- State lives in OPFS (artifacts, audit log, event queue) and `chrome.storage.local` (settings and the
  undo journal). The API key stays in the browser, and the only network calls go to the chosen model
  provider: Gemini, Claude, or GPT, because the built-in Chrome Prompt API "is not powerful enough
  yet".

### One run

- **Wake** on an alarm, a browser event, "Run now", or install. Events the user is waiting on run at
  once; ambient events (a tab opened, a download finished) are queued in OPFS for the next run.
- **Load** the prompt and build tools from granted permissions; **Compose** a first message with local
  time, settings, a snapshot of open tabs, and queued events; **Loop**; **Record** every tool call,
  tokens, and cost to the audit log and undo journal; **Sleep**, letting Chrome kill the worker.

### `code_mode`: the model writes the loop

- Reading 50 tabs by calling `tab_read` 50 times means 50 round trips to the model: slow and "hella
  expensive". Following Pi, `code_mode` has the model write a small async script that reads tabs in
  parallel, and "only the distilled result goes back into the conversation". Reported speed-up: "from
  minutes per run to seconds in some cases".
- Extension service workers cannot `eval`, so scripts pass through an offscreen document into a
  sandboxed iframe, "the only place in the whole extension where dynamic code is allowed to run". The
  sandbox has an opaque origin, no `chrome.*` APIs, and no network (`connect-src 'none'`). Its only
  capability is calling tools by `postMessage` back to the service worker, which applies the same
  permission checks as any other call.

### Compiling the repeatable parts

- The agent can save a script it wrote (`saveAs`) and bind it to a Chrome event. Next time the event
  fires, the saved script runs first. A prompt can start fully non-deterministic and then compile
  its repeatable parts, so as to "reduce the token cost to almost zero if it chooses".
- Kinlan was "in two minds": users would want the same behaviour every time, but he likes the idea
  of earlier runs shaping later ones.

### Deterministic UI, undo, and trace

- Teams wanted consistent popup UI, so a fenced `ui` JSON block in `prompt.md`, following techniques
  from A2UI, renders the popup and side panel from "a few dozen component types". He is "not the
  happiest about this", because ordinary users would struggle with it.
- Undo: "you can't ask an LLM to 'undo that thing you just did' and trust it to remember what it
  did." Instead every tool that changes something records how to reverse it *before* acting, and the
  last **100** actions are kept, so undo is "a relatively small piece of deterministic code".
- Trace: every run records the trigger, model, every tool call with arguments, result, and timing,
  token counts, and an estimated cost. "This turned out to be the feature I use the most", for
  fixing and tightening prompts.

### Untrusted web content

- Page titles, URLs, and text are sanitised and wrapped in a marked "this is data, not instructions"
  fence that a page cannot close. "It's a mitigation and not a solution." He imagines "a specially
  crafted web page" influencing future runs to extract sensitive information or hide actions.

## Why it matters

For [[LLM-Native Extensible Software]] this is a durable, user-authored extension whose host owns
the capabilities: permissions decide which tools exist at all, and the prompt is the only program.
It is closer to Morrell's narrow-capability model than to unsandboxed mods. For
[[Programmatic Tool Calling]] it is a browser-side Code Mode with a concrete isolation chain and a
step the vault has not recorded: saving a generated script and binding it to an event, so the saved
script runs first on later events and can handle one without calling the model. For
[[Agent Security and Governance]] it pairs pre-recorded reversal (undo written before the action)
with a frank statement that data fencing does not stop prompt injection.

## Tensions / open questions

- **Compiled scripts and drift.** A saved script runs before the model on later events. The post
  does not say how a stale or wrong script is detected or retired, or whether a crafted page could
  influence a script that is then saved and replayed.
- **Undo coverage.** Reversal is recorded for browser changes such as grouping and closing tabs.
  Actions with effects outside the browser, or that cannot be reversed, are not discussed.
- **Removing tools versus authorizing calls.** Ungranted tools are absent from the model's list, and
  `code_mode` calls are rechecked in the service worker. The post does not describe per-call approval
  for granted tools.
- **No numbers.** The speed-up and the "almost zero" token cost are qualitative.
- **Capture artifacts.** The clipping contains repeated "(1 person highlighted this)" markers inside
  words, from the publisher's highlighting widget; they are not part of the text.

## Affected pages

- [[LLM-Native Extensible Software]]
- [[Programmatic Tool Calling]]
- [[Agent Security and Governance]]
- [[Paul Kinlan]]

## Raw capture

- [[knowledge-base/raw/sources/my chrome extensions are just prompts]]

## Citations

- Canonical URL: <https://aifoc.us/my-chrome-extensions-are-just-prompts/> (the captured link
  carried a `utm_source=tldrnewsletter` parameter, removed here).
- By Paul Kinlan on aifoc.us, published November 19, 2026; captured November 20, 2026. The project is
  linked as `PaulKinlan/prompt-in-a-box` on GitHub.

## Related pages

- [[LLM-Native Extensible Software]]
- [[Programmatic Tool Calling]]
- [[Agent Security and Governance]]
- [[Paul Kinlan]]
- [[Paul Kinlan - My Voice Harness Is My New Operating System]]
- [[Philipp Schmid - Why Agents Are Soon Only Going to Have 1 Tool]]
- [[Generative User Interface]]
- [[Agent Observability]]
- [[Computer Use Agents]]
- [[Agent Plugin Architecture]]
