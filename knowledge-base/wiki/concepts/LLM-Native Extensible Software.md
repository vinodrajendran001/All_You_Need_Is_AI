---
type: concept
created: 2026-08-24
updated: 2026-11-27
tags: [concept, software-architecture, ai-agents, extensibility]
source_ids:
  - src-2026-08-20-jeremy-morrell-extensible-software
  - src-2026-08-17-google-cloud-agent-plugins
  - src-2026-09-02-can-boluk-harness-playbook
  - src-2026-10-09-rabi-guha-intelligent-ui
  - src-2026-10-21-mcateer-claude-mods
  - src-2026-11-17-paul-kinlan-voice-harness
  - src-2026-11-19-paul-kinlan-chrome-extensions-prompts
  - src-2026-11-25-frank-rousseau-agentic-coding-open-source
  - src-2026-11-25-goofyfish-make-your-own-game
status: active
---

# LLM-Native Extensible Software

## Definition

LLM-native extensible software lets users generate durable application extensions from natural-language intent while a trusted host constrains their execution through stable capabilities and isolated runtimes.

## Architecture

[[Jeremy Morrell - Extensible Software in the Age of LLMs]] separates:

- a **trusted shell** that owns identity, data, routing, and privileged APIs;
- **generated UI** that is stored and inspectable;
- **generated server code** executed in isolated workers;
- a narrow RPC interface that exposes only approved capabilities.

The generated artifact should survive the conversation, be versioned, and remain understandable as code. Server-side workers provide a stronger isolation point than unrestricted browser execution, although sandboxing, dependency control, schema migration, and debugging remain difficult.

[[Agent Plugin Architecture]] is the distribution counterpart: once an extension or capability is durable, it needs a manifest, assets, state boundaries, and portable tool definitions.

## Configuration and language choice as parts of the extension surface

[[Can Bölük - The Harness Playbook]] extends this page in two directions that extension-API discussions usually
skip.

**Configuration is part of the extension surface.** The proposed model is the Source Engine **convar**: a typed
variable declared once at its definition site with a name, default, help string, and a flag bitfield — the flags
carrying persistence, ownership, scope, replication, and replay-honesty. Because the declaration site owns those
properties, an extension adds a setting without touching a central settings object, and a spawned child session
seeds every variable from the parent's live values with no inheritance setting required. Compare the status quo,
where compatibility axes are literally named after the models that caused them (`qwen-preserve-thinking`,
`strip-deepseek-special-tokens`) and three files totalling over 3,600 lines encode model quirks by hand. The
proposed replacement is a declarative taxonomy, and the stated goal is not fewer quirks: *"The win is not fewer
quirks. It is one owner for each fact, explicit precedence, and an `unknown` state."*

**Implementation language acts as a prior on generated code.** The blunt version — *"TypeScript is an awful
choice at the moment"* — rests on the argument that when agents write most of the extension code, the language's
defaults shape what gets generated. The proposed split is a Rust engine with Python extensions, Python chosen
partly because it can inspect its own AST, which makes decorators like `@remote` implementable rather than
aspirational.

The state-model half of the same argument — why extension state must live in one authoritative place — is in
[[Harness State Authority]], along with the audit finding that **only 2 of 17 stateful reference extensions were
correct.**

## Streamed interface code is a narrower case than a durable extension

[[@rabi_guha - How ChatGPT Intelligent UI Works]] adds an observed instance of the trusted-host
split: generated DIL compiles to JavaScript and data, an isolated worker emits reconciliation
operations, and the host renders known components. Stable keys reportedly preserve interaction
state across recompilations while failed revisions can leave the last working program active.

That is evidence for [[Generative User Interface]] continuity, not the cross-session durability,
versioning, storage, and migration contract in Morrell's extension proposal. It is also
third-party web reverse engineering, not OpenAI's specification or a sandbox audit.

The separate AppBlock HTML/JavaScript iframe path and raw-CSS-capable properties limit any
claim that a native catalog constrains every output. Generated-artifact design therefore
needs explicit authority and diagnostics on each path, including what users see when the
requested revision fails rather than silently mistaking retained old state for success.

## Programmable interfaces do not imply isolated extensions

[[Dan McAteer - Claude Mods and the Attention Interface]] supplies a contrasting design:
user/agent-authored JavaScript or TypeScript runs inside Claude Code and can intercept
events or change their rendering. That makes human attention programmable, but the account
explicitly says mods are **not sandboxed** and can access files, prompts, and usage under
the user's permissions. Built-ins reportedly remain active in safe mode.

These mods therefore illustrate malleability, not the narrow-capability isolation in
Morrell's proposal above or proof of the observed Intelligent UI sandbox's properties.
Before reusing an extension pattern, specify its execution privileges, host-owned state,
review/update policy, and interruption behavior. The author's supervisor ran on **99 of
111 turns**, an example of programmability creating attention cost rather than automatically
improving interaction. This personal report supplies no controlled effectiveness measure.

## Model-written apps that persist, and extensions that are data

[[Paul Kinlan - My Voice Harness Is My New Operating System]] is a worked case of the trusted-host
split. In Voicebox the model writes a mini-app as a single HTML file, and the daemon saves it so "next
week I can say 'open the calculator' and it comes back." Because the code is model-written it runs "two
iframes deep": a same-origin bridge checks every message, and the inner frame has an opaque origin, no
storage, and a content security policy that blocks the network by default. Mini-apps register tools
through WebMCP, which Kinlan calls "functionality built by the LLM being usable by the LLM in future
interactions".

Extensions are stricter still. Each is a JSON descriptor over **six** daemon primitives, with keys
filled from the daemon's environment "so the key never reaches the page or the model", and WASM tools
pinned by SHA-256 and re-hashed on every call. "The model can propose a tool, but the only thing a
proposal can do is write a file." This is the opposite pole from the unsandboxed mods above. The same
harness, though, runs shell commands with the user's full rights: "What it isn't is a sandbox. It runs
as me."

[[Paul Kinlan - My Chrome Extensions Are Just Prompts]] applies the same host-owns-capabilities idea
to Chrome. In Prompt in a Box an extension is a generic runtime plus three files: `prompt.md` is "the
program", `manifest.json` is "what the extension is allowed to reach. Permissions are the contract",
and `config.json` holds models, schedule, and settings. "You swap the prompt and the same code becomes
a different tool." The runtime exposes "about 50" Chrome APIs as tools, but "if the manifest doesn't
grant `bookmarks`, the bookmark tools are simply not in the list that the model sees". The extension
is durable and user-authored, with a browser-native permission model, so it sits close to Morrell's
narrow-capability design. The catch is distribution: because the runtime relies on dynamic code
execution, the extensions cannot be published to the Chrome Web Store and load only in developer
mode. Both are single-developer prototypes by [[Paul Kinlan]], with no measured results.

## When contributors' agents write the extensions

[[Frank Rousseau - Agentic Coding on an Open-Source Project]] reports that Kitsu's new plugin system
let studios build and share plugins, that other studios shared integrations they built with LLMs,
and that contributors now also propose changes to core components. Studios want more customization,
while Kitsu's philosophy is a common interface across studios: "We haven't arbitrated on the topic
yet." [[Goofy Fish - Make Your Own Game]] goes further. A visitor describes a game to Claude Code
through a `/game` command shipped in the site's repository, the agent builds and tests it in the
site's style, and the result arrives as a pull request that the maintainers play before publishing.
Both keep a human gate at intake; neither reports how many extensions were accepted, rejected, or
later broke.

## Open questions

- How can generated extensions be upgraded without breaking user state?
- What review and provenance should be required before permissions expand?
- Can narrow capability APIs remain useful without recreating a full operating system?

## Related pages

- [[Dan McAteer - Claude Mods and the Attention Interface]]
- [[@rabi_guha - How ChatGPT Intelligent UI Works]]
- [[Generative User Interface]]
- [[Agent Plugin Architecture]]
- [[Agent Security and Governance]]
- [[Coding Agent Harness]]
- [[Tool Use and Function Calling]]
- [[AI Agents in Production]]
- [[Harness State Authority]]
- [[Tool Roster Economics]]
- [[Can Bölük - The Harness Playbook]]
- [[Can Bölük]]
- [[Paul Kinlan - My Voice Harness Is My New Operating System]]
- [[Paul Kinlan - My Chrome Extensions Are Just Prompts]]
- [[Paul Kinlan]]
- [[Programmatic Tool Calling]]
- [[Frank Rousseau - Agentic Coding on an Open-Source Project]]
- [[Goofy Fish - Make Your Own Game]]
