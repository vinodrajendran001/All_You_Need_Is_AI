---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-pi-agent-extensions-guide
title: 'Pi Agent Extensions: Change the Harness, Not Just the Prompt (2026)'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/pi-agent-extensions-guide
published: '2026-07-16'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Pi Agent Extensions: Change the Harness, Not Just the Prompt (2026)

Ask which coding agent is better, Claude Code or Codex, and the honest 2026 answer is that it stopped mattering. They converged. Whatever gap existed closed sometime last year, and the two now trade features on a lag measured in weeks.

So the interesting question moved. It isn't *which agent is smarter*. It's **whether you can change the thing you're driving.**

That's the question [Pi](https://pi.dev/) answers differently from everyone else, and it's why OpenClaw is built on it rather than on the Claude Code SDK. Pi ships four tools and almost nothing else. Everything past that core is an extension, written by you or by the agent itself, running inside the harness rather than shouting at it from outside.

Here's the decode, including the one part of my own pitch that doesn't survive contact with Anthropic's docs.

Prefer to watch? Here's the original video this piece expands on. The hooks claim I correct below is in it, stated exactly as I got it wrong:

---

## What is Pi?

Pi is an open-source terminal coding agent from Mario Zechner (badlogic), living at [earendil-works/pi](https://github.com/earendil-works/pi). As of 2026-07-16 the repo sits at roughly 71,500 stars with commits landing daily.

Its official line is the whole product strategy in one sentence: *"There are many agent harnesses but this one is yours."*

The defaults are aggressively small:

|  | Pi | Claude Code |
| --- | --- | --- |
| Built-in tools | 4 (`read`, `bash`, `edit`, `write`) | 10+ including sub-agents, MCP, web search |
| System prompt | ~1,000 tokens | ~14,000 tokens |
| Models | 15+ providers, hundreds of models | Anthropic only |
| Sub-agents | Not included, install a package | Built in |
| Plan mode | Not included, write plans to files | Built in |
| MCP | Not included, install an adapter | Built in |
| Customization | In-process TypeScript extensions | Out-of-process hooks |
| Source | Open | Closed |

Pi's docs don't apologize for any of those omissions. Ask about sub-agents and it says: spawn Pi instances via tmux, build your own with extensions, or install a package that does it your way. Ask about MCP and it says: build CLI tools with READMEs, or write an extension.

**That is not a smaller Claude Code. It's a different bet: that a harness you can rewrite beats a harness that arrives finished.**

Be clear-eyed about the cost of that bet, which I'll come back to at the end. You are assembling what other tools hand you on install.

Install is one line:

bash

```
curl -fsSL https://pi.dev/install.sh | sh
```

One naming trap before we go further. "Pi" is a badly overloaded term: Inflection's chatbot, the constant, Raspberry Pi. This is none of those. And the npm scope was renamed from `@mariozechner/*` to `@earendil-works/*`, which quietly breaks a lot of tutorials written before the change. Current packages are at 0.80.7.

## Where do hooks actually hit their ceiling?

This is the part I got wrong, in my own video, two days ago.

I said that Claude Code's hooks can only *append* information to a tool call and cannot modify a tool call's **result**, and that this is why result-compression tricks are effectively Pi-only. It's a clean story. I believed it when I said it. It's also wrong.

Anthropic's [hooks documentation](https://code.claude.com/docs/en/hooks) specifies a `PostToolUse` field called `updatedToolOutput`, described plainly: it "replaces the tool's result." Claude Code hooks can rewrite tool output. `PreToolUse` can rewrite tool *input* via `updatedInput`. The docs even name redaction and transformation as intended use cases.

The claim is true of `PreToolUse` alone. I generalised it to hooks as a whole, and the generalisation doesn't survive the docs.

So I'm not going to repeat it here to make Pi look better. The argument has to stand somewhere else, and the honest version is more interesting than the one I made up: **the real ceiling isn't what hooks can edit. It's where they run.**

Hooks run as **separate processes**. A shell command, an HTTP endpoint, an MCP call. Claude Code hands them JSON on stdin and reads JSON off stdout. That process boundary is the actual constraint, and it produces a hard list of things no hook can ever do:

| Capability | Claude Code hooks | Pi extensions |
| --- | --- | --- |
| Block or allow a tool call | Yes | Yes |
| Rewrite tool input | Yes (`updatedInput`) | Yes (`tool_call`) |
| Rewrite tool output | Yes (`updatedToolOutput`) | Yes (`tool_result`) |
| Inject context before a turn | Yes (`additionalContext`) | Yes (`before_agent_start`) |
| Register a new tool the model can call | **No** | Yes (`pi.registerTool`) |
| Add a slash command | **No** | Yes (`pi.registerCommand`) |
| Register a model provider | **No** | Yes (`pi.registerProvider`) |
| Redraw the terminal UI | **No** | Yes (renderers, `ctx.ui`) |
| Change compaction | **No** | Yes (`session_before_compact`) |
| Change session management | **No** | Yes |
| Runs where | Separate process, JSON contract | In-process, TypeScript, harness API |

Hooks are lifecycle observers with a permission ballot. Excellent ones. Our [complete guide to Claude Code hooks](/blog/claude-code-hooks-complete-guide) covers how far you can push them, and it's further than most builders bother to go. Further than I gave them credit for.

But they observe a harness. They are not part of one. A hook can veto a tool call and rewrite what comes back, and still cannot add a fifth tool, put a widget on your screen, or change how your context gets compacted when it fills. Those aren't events Anthropic chose to expose, so they don't exist for you.

Pi's extensions get handed the harness's own API object and run in the same process. The surface isn't a fixed menu of events. It's the harness.

## What does a Pi extension look like?

Extensions are TypeScript modules that export a default factory function receiving Pi's `ExtensionAPI`. Pi auto-discovers them from four locations:

code

```
~/.pi/agent/extensions/*.ts          # global
~/.pi/agent/extensions/*/index.ts    # global, directory form
.pi/extensions/*.ts                  # project-local
.pi/extensions/*/index.ts            # project-local, directory form
```

The smallest useful one injects context. Say you want the agent permanently aware of your git state, branch, worktrees, unstaged changes, recent commits, without ever spending a tool call to look it up:

typescript

```
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("before_agent_start", async (event, ctx) => {
    const summary = await buildGitSummary(ctx.cwd);
    // append the git context after the predefined system prompt
  });
}
```

Now ask it "what branch am I on, use no tools" and it answers. The information was there before the turn started. That's [context engineering](/blog/context-engineering-guide) applied at the harness level rather than the prompt level: the cheapest tool call is the one that never happens.

Registering a genuinely new tool is the move hooks can't make at all:

typescript

```
pi.registerTool({
  name: "read_clipboard",
  label: "Read Clipboard",
  description: "Read the current contents of the system clipboard",
  parameters: Type.Object({}),
  async execute(toolCallId, params, signal, onUpdate, ctx) {
    // return clipboard contents to the model
  },
});
```

Your agent now has a fifth tool. No fork, no vendor, no waiting.

The event list is where the ambition shows. `context` rewrites messages before the model sees them. `tool_call` intercepts and can block. `tool_result` modifies results after execution. `session_before_compact` customizes summarization. `input` intercepts user text before expansion. `before_provider_request` lets you touch the HTTP call itself.

The sharpest thing I've built with those is a **permission gate**. Instead of trusting the agent to enforce access rules, the extension intercepts every user message, runs a cheap fast model against a `permission.md` policy file, and returns allow or deny with a reason. Denied requests never reach the main agent. The session just stops with a block message on screen. That's a policy layer a company could actually defend, written in one file, and it needs both the `@earendil-works/pi-coding-agent` extension API and `@earendil-works/pi-ai` for the gate model call.

Try building that with hooks. You can block the call. You cannot draw the block message, and you cannot ship the whole thing as one installable unit.

## Can the agent write its own extensions?

This is the part that reframes the tool, and it follows directly from everything above.

Pi knows its own extension API. It ships with awareness of what the API exposes and what's currently loaded. So you don't write extensions so much as ask for them.

In the video I tell Pi I want the weather in the prompt input. Pi reads its own extension docs, writes the extension, and I run `/reload`. The harness restarts with the widget above the input. Extensions in the auto-discovered directories hot-reload, so the loop is genuinely tight.

**A harness that knows its own extension API is a harness that can be edited by talking to it.**

That's the philosophical gap with hooks. You cannot say "Claude Code, add plan mode to yourself." The harness isn't in the conversation. In Pi it is.

## What's in the package catalog?

Extensions, skills, prompts and themes bundle into **Pi packages**, shared over npm or git:

bash

```
pi install npm:@foo/pi-tools
pi install git:github.com/badlogic/pi-doom
```

The [catalog](https://pi.dev/packages) already rebuilds most of what Pi deliberately left out. Verified names:

| Package | What it adds |
| --- | --- |
| `pi-mcp-adapter` | MCP support |
| `pi-subagents` | Task delegation, chains, parallel execution |
| `@quintinshaw/pi-dynamic-workflows` | Claude-Code-style dynamic workflows |
| `pi-web-access` | Web search, URL fetch, repo cloning, PDF and video extraction |
| `pi-agent-browser-native` | Browser automation as a native tool |
| `@hypabolic/pi-hypa` | Keeps noisy tool output out of the context window |
| `oh-my-pi` | Turns Pi into a multi-agent orchestration system |

Install dynamic workflows, `/reload`, and you get an experience close to the Claude Code feature it copies. There are packages whose entire purpose is making Pi behave like Claude Code or Codex. The convergence argument, executed as a plugin.

`@hypabolic/pi-hypa` is the one worth studying. It rewrites shell commands through a local deterministic compressor so the noise never reaches your context. `git log` returns hash, author, date, body and diff when the agent needed a fraction of that, and the extension strips it in flight.

Numbers, honestly: percentages in the 80-96% range get quoted for this class of package. The package's own catalog listing states no benchmark figures, so I'm not printing one. Directionally the savings on chatty commands are large. Treat the specific number as unverified until someone publishes a methodology.

And note what pi-hypa is *not*: proof that Claude Code couldn't do this. This is exactly where my original claim fell over. `updatedToolOutput` exists. What Pi gives you is that the compressor ships as one installable package that also touches the tool definitions and the UI, instead of a subprocess you wire up per machine. That's a real difference. It just isn't the difference I said it was.

Now the honest part. **Extension quality varies wildly, the ecosystem is young, and every extension runs with your full system permissions and can execute arbitrary code.** Pi's own docs say so. `pi install` from a stranger is `curl | sh` with extra steps. A catalog of community packages that can each register tools and intercept your context is a real supply-chain surface, and Pi's answer is that you should only install from sources you trust. That's a design position, not a safety feature.

## Why did OpenClaw build on Pi?

[OpenClaw](/blog/openclaw-guide-2026) is the reason most builders heard the name Pi at all, and it's the best available evidence for the argument.

OpenClaw's actual product is the gateway: Slack, web, messaging. It needed an agent runtime underneath, and it needed to change that runtime substantially, adding its own memory, sub-agents, MCP and ACP.

So it doesn't spawn Pi as a subprocess or drive it over RPC. It imports Pi and instantiates `createAgentSession()` directly. Then it uses extensions for exactly the things hooks can't reach: context pruning that silently trims oversized tool results, and a compaction safeguard that replaces Pi's default summarization with a multi-stage pipeline preserving file-operation history and tool-failure data.

Read that last one again. **OpenClaw replaced the harness's compaction strategy.** Not configured it. Replaced it. There is no version of that on the Claude Code SDK or the Codex CLI, because compaction isn't an event either of them exposes. That one is worth more than the tool-result claim I opened with, and unlike that claim, it holds.

That's the whole thesis in one shipped product, and it's why this is [harness engineering](/blog/harness-engineering-agent-production-guide) rather than prompt engineering.

## Can you build a product on the Pi SDK?

The layered packages are the actual reason to care. Pi is five packages, all at 0.80.7:

| Package | Layer | Comparable to |
| --- | --- | --- |
| `@earendil-works/pi-ai` | Unified LLM API, provider config, OAuth | Vercel AI SDK |
| `@earendil-works/pi-agent-core` | Agent loop, tool calling, state | `streamText` with a loop |
| `@earendil-works/pi-coding-agent` | Tools, sessions, compaction, extensions, SDK | Claude Agent SDK |
| `@earendil-works/pi-tui` | Terminal UI with differential rendering | - |
| `@earendil-works/pi-orchestrator` | Scheduled jobs, delegation across processes | Experimental |

Take them at whatever layer you need. `pi-ai` alone is a reasonable Vercel AI SDK substitute with OAuth, so your users connect their existing Claude or Codex subscriptions instead of pasting keys. The orchestrator is labeled "experimental orchestrator package for pi" in its own package.json, so treat it accordingly.

The comparison that matters: `pi-coding-agent` is roughly the Claude Agent SDK, except it's open, model-agnostic, and every layer is replaceable. That's the [six components of a harness](/blog/harness-six-components) with the lid off.

**Local products get most of what they need for free. Hosted products do not, and it's worth knowing why before you commit.**

The SDK assumes a local filesystem. On a hosted product your agent runs on shared infrastructure while each user needs their own sandbox, so two things break:

1. **Sessions.** The default `SessionManager` writes to disk. You store sessions in your own database and manage compaction yourself. `SessionManager.inMemory()` gets you off the filesystem to start.
2. **Tools.** The default `bash`, `read`, `write` and `edit` touch the local machine. You wrap them so they execute in the calling user's sandbox.

Skills, extensions and working directory get passed per session through `DefaultResourceLoader`, so you can vary what each session is allowed to do. Then `createAgentSession()` takes your custom tools and your loader, and you render off the event stream.

This is where being fair matters more than being loud: **the sandboxing problem is not a Pi weakness.** You handle the same thing on the Claude Agent SDK. Any SDK built for a local coding agent makes local assumptions. Pi's advantage is only that the session manager and the tools are replaceable parts rather than internals.

I rebuilt Posia on this, a hosted system meant to launch and run a business: 11 agents, an orchestrator built around a task entity, persisted state and context, and a tools proxy. The architecture is standard [multi-agent orchestration](/blog/open-source-ai-company-multi-agent). The notable thing is that the runtime under it is one you can open.

## Should you switch to Pi?

Not necessarily. The pitch has a real cost and the anti-hype version is short.

| Choose Pi when | Stay on Claude Code / Codex when |
| --- | --- |
| You need to change harness behavior the vendor didn't expose | The defaults are fine and you'd rather ship features |
| You're building a product on an agent runtime | You're using an agent to build products |
| You need model-agnostic or self-hosted routing | You're happy inside one model family |
| Context budget is tight and you'll engineer it | You want context managed for you |
| Your team writes TypeScript comfortably | Nobody wants to maintain harness code |
| Auditable open source is a requirement | A polished closed product is fine |

That 14,000-token Claude Code system prompt everyone mocks is doing work. It quietly handles context management, compaction, file-reading strategy and a dozen other decisions you never think about. Pi's ~1,000-token prompt means those decisions are now yours. Some of them you'll get wrong.

The correct read for most builders is that this isn't a switch. Pi for control, multi-model work, and anything you're building a product on. Claude Code for fast daily driving. The [loop is the choreography, the harness is the stage](/blog/loop-engineering-vs-harness-engineering), and you're allowed different stages for different work.

What Pi changes is that the stage stopped being someone else's.

## FAQ

**What is the Pi agent?**
An open-source terminal coding agent by Mario Zechner (badlogic), best known as the runtime powering OpenClaw. Four built-in tools (read, bash, edit, write), a ~1,000-token system prompt, no sub-agents, no plan mode, no MCP by default. Everything else is an extension. Not Inflection's Pi chatbot, and nothing to do with Raspberry Pi.

**Is Pi free and open source?**
Yes, and free to run. You pay for model usage instead, with your own keys across 15+ providers, or via an existing Anthropic, OpenAI or GitHub Copilot subscription over OAuth.

**What's the difference between Pi extensions and Claude Code hooks?**
Hooks are out-of-process callbacks at vendor-chosen events, exchanging JSON. They're more capable than commonly claimed, including by me: `PostToolUse` can replace a tool result via `updatedToolOutput`. But they can't register a tool, add a command, register a provider, redraw the UI, or change compaction. Pi extensions are in-process TypeScript holding the harness's API, so they can. The line isn't what fires when. It's inside the harness or outside it.

**Does Pi support MCP?**
Not by default, on purpose. Pi's docs suggest CLI tools with READMEs, or an extension. `pi-mcp-adapter` adds it if you want it.

**Can you build a product on top of Pi?**
Yes, via `createAgentSession` in the coding-agent SDK. Local products get most of what they need out of the box. Hosted products need session storage in your own database and tool wrappers that run inside each user's sandbox, because the SDK assumes a local filesystem. The Claude Agent SDK makes you do the same work.

**Are Pi extensions safe to install?**
Treat them like any npm dependency with shell access, because that's what they are. Pi's docs state extensions run with your full system permissions and can execute arbitrary code. The ecosystem is young and quality varies. Read the source of anything you install.

## Related Content

- **[OpenClaw: What It Is and How to Use It](/blog/openclaw-guide-2026)** - The product that proved the argument, and the best case study for why a modifiable runtime was worth it.
- **[Claude Code Hooks: The Complete Guide](/blog/claude-code-hooks-complete-guide)** - How far hooks actually go before you need something like Pi.
- **[The 6 Components of a Production Agent Harness](/blog/harness-six-components)** - The anatomy Pi splits into five packages.
- **[Harness Engineering: What OpenAI and Anthropic Changed](/blog/harness-engineering-agent-production-guide)** - Why the harness, not the model, became the thing worth engineering.
- **[Context Engineering: The 100:1 Ratio](/blog/context-engineering-guide)** - The discipline behind tool-result compression and why it pays.
- **[From Prompts to Loops: The 4 Shifts](/blog/prompt-context-harness-evolution)** - Where "modify the harness" sits in the arc of AI engineering.

---

## Start Here

Pick the one thing your coding agent does that annoys you every single day. The tool result that's 90% noise. The context it never has. The check nobody enforces.

Then ask which side of the line it falls on. If a subprocess reading JSON could fix it, write the hook and move on, you don't need a new harness. And check the docs before you decide it can't, which is advice I'm giving myself as much as you. If the fix requires a tool that doesn't exist, a command that isn't there, or a compaction strategy the vendor never exposed, you've found your ceiling.

That ceiling is the entire reason Pi exists. Install it, ask it to extend itself, and run `/reload`. Five minutes to see whether a harness you can rewrite is worth what you give up to get one.

Pi is an open-source terminal coding agent created by Mario Zechner (badlogic), best known as the runtime under OpenClaw. It ships deliberately small: four built-in tools (read, bash, edit, write), a system prompt around a thousand tokens, no sub-agents, no plan mode, and no MCP by default. Everything past that core is an extension you install or write. Its official framing is 'There are many agent harnesses but this one is yours.' Note the name is ambiguous: this is not Inflection's Pi chatbot and has nothing to do with Raspberry Pi.

Yes. Pi is open source and free to run. You pay for model usage instead, either with your own API keys across 15+ providers, or with an existing Anthropic, OpenAI or GitHub Copilot subscription connected through OAuth. That bring-your-own-key design is why Pi is model-agnostic in a way Claude Code is not.

Hooks are out-of-process callbacks that fire at a fixed set of vendor-chosen events and exchange JSON over stdin/stdout. They are more capable than commonly claimed - PostToolUse can replace a tool's result via updatedToolOutput. But they cannot register a new tool, add a slash command, register a model provider, redraw the terminal UI, or change compaction. Pi extensions are in-process TypeScript handed the harness's own API object, so they can do all of those. The difference is not what fires when. It's whether your code is inside the harness or outside it.

Not out of the box, and that is on purpose. Pi's docs tell you to build CLI tools with READMEs instead, or add MCP through an extension. If you want it, pi-mcp-adapter in the package catalog provides it. This is the whole Pi trade in one example: nothing is bundled, everything is available, and the assembly is your job.

Yes, through the coding-agent SDK's createAgentSession. Local agent products that run on a user's own machine get most of what they need out of the box. Web-hosted products need real work, because the SDK assumes a local filesystem: you store sessions in your own database rather than using the default SessionManager, and wrap the bash, read and write tools so they execute inside each user's sandbox. That sandboxing work is not a Pi flaw. You do the same thing on the Claude Agent SDK.

This piece expands on my video 'Why I switched to Pi' and corrects it. My synthesis is the hooks-vs-extensions argument: that the meaningful ceiling on Claude Code and Codex customization is process boundary and fixed event surface, not the inability to rewrite a tool result. Every technical identifier here was verified against primary sources before publishing, not transcribed from secondary coverage: the five package names and the orchestrator's experimental status against the earendil-works/pi repo and the npm registry (all at 0.80.7 on 2026-07-16); the ExtensionAPI methods (pi.on, pi.registerTool), the event names (before\_agent\_start, tool\_call, tool\_result, context), and the .pi/extensions discovery paths against Pi's official extensions doc; createAgentSession, DefaultResourceLoader, and SessionManager against Pi's official SDK doc. One claim did NOT survive that check, and it was mine: in the video I said Claude Code hooks cannot modify a tool's result, and that this is why result-compression is effectively Pi-only. That is false as stated - Anthropic's hooks documentation specifies a PostToolUse field, updatedToolOutput, that replaces the tool result. The claim holds for PreToolUse only; I generalised it to hooks as a whole. I have corrected it here rather than repeat it, and rebuilt the argument on ground that survives. I also declined to publish the token-savings percentages circulating for @hypabolic/pi-hypa because the package's own catalog listing states no benchmark numbers; I describe the mechanism and attribute the savings claim without a figure I cannot source. Star count and version numbers were pulled live from the GitHub and npm APIs on 2026-07-16 and will drift. See our [editorial standards](/about).
