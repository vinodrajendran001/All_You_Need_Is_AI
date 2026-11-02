---
title: "Droid 1.0: Building a Frontier Harness"
source: "https://factory.com/news/frontier-harness?utm_source=tldrai#methodology"
author:
  - "[[Factory Research]]"
published: 2026-10-29
created: 2026-11-02
description: "Over the past year, we have worked with hundreds of thousands of developers across some of the largest enterprises in th..."
tags:
  - "clippings"
---
![](https://factory.com/_next/image?url=%2Fimages%2Fresearch%2Ffield-studies-blue-gradient.webp&w=3840&q=75) ![](https://factory.com/_next/image?url=%2Fimages%2Fresearch%2Ffield-studies-ripples.webp&w=3840&q=75)

Over the past year, we have worked with hundreds of thousands of developers across some of the largest enterprises in the world. Working side by side with these teams, we've built and hardened a frontier agent harness that directly meets the demands of enterprise development: high-quality results on complex tasks, efficient use of resources, and strong safety controls.

Today, we introduce Droid 1.0: more accurate, efficient, and faster than ever before, powered by new design principles and a programmatic tool-calling engine.

Droid is our agent harness. An agent harness is everything around the model: the prompts, the tools, how tool results come back, and the loop that runs it all. Agents now work for hours or days across hundreds of turns, and every turn re-sends instructions, tools, and history.

Today's update to Droid is the largest one yet. On the same tasks, Droid outperforms the native harnesses built for their models up to 20% more efficiently. It's also designed for what comes next: when frontier models can plan whole workflows as code, Droid lets them run hundreds of tool calls in a single model request.

Factory is model-independent by design. We believe the best agent harness is one built for every model, so our users can choose the best model on the market or let Droid choose the most efficient mix using our auto model router, Factory Router.

Building a harness optimized for many models makes the harness better. When you tune against a single model, it's hard to separate real progress from adaptations to that model's quirks. Working across models ensures the strongest improvements generalize and hold up beyond the model that inspired them.

That's the idea behind our internal Agent Factory. Agents study benchmark failures alongside the friction our users hit in real sessions, propose changes, and test each one on every model family it affects. Our engineers review the evidence and decide what ships.

The result is the most efficient enterprise-ready coding agent tuned for every frontier model, whether open- or closed-weight.

The rest of this post covers the head-to-head results, the design principles behind the harness, how we built our internal Agent Factory, and the core changes that drove the most impact.

## The most efficient harness in the market

On the same tasks using the same models, Droid scores higher at a lower cost than every other harness we tested.

Fig. 1 Terminal-Bench 4

GPT-6.1 Sol

Cursor isn’t shown: it has no access to OpenAI models.

Opus 5.5

Terminal-Bench 4. With GPT-6.1 Sol, Droid scores 3.5 points higher than Codex at 12% lower cost, and 6.6 to 12.6 points higher than OpenCode and Devin. With Claude Opus 5.5, Droid scores 3.0 to 7.6 points higher than Cursor, OpenCode, Devin, and Claude Code, at up to 24% lower cost. [Methodology](#methodology)

This gap matters more as agents run longer. Over hundreds of steps, a better agent makes fewer mistakes for later steps to build on, and a cheaper one lets you run more agents on the same budget. Droid tunes its prompts, tool descriptions, and tool-calling mode for each model it supports, so every supported model gets these gains, including when you bring your own API keys.

The largest change behind these results was letting the model call tools from a program.

## Programmatic tool calling

In a standard agent loop, the model calls tools directly and every tool output is appended to its context. Programmatic tool calling (PTC) takes a different approach to long-horizon work: the agent writes a program that invokes the tools.

With PTC, the agent can reason up front, write the code for a tool-calling workflow, and then execute the entire program end to end in a single invocation. For example, it could write a workflow to read hundreds of files and find the few that mention a topic, triage dozens of Linear tickets, or run a tricky database migration in pieces following a deterministic process.

CodeAct (Wang et al., 2024) showed that acting through code beats JSON and text tool calls across 17 models. Cloudflare and Anthropic brought the idea to production in late 2025, and Codex brought it to coding agents this year.

We made PTC the default in Droid 1.0 for three reasons. First, it keeps the agent's context window clean, because all it receives is the output of its program. Ordinary tool outputs (raw files, search results, logs) stay inside the program as variables. Second, it cuts the number of model requests, because one program runs many calls, which makes complex tasks faster and cheaper. Third, it makes the agent more reliable: checks and loops run deterministically in code, eliminating the chance that a model could be lazy and drop a case despite originally planning it.

### Script mode

Droid implements PTC as a Script tool. The model writes JavaScript that runs in a sandbox with no file, network, or system access of its own.

A Script can make hundreds of tool calls in one model request, so the instructions and history are sent once rather than re-sent every few calls. Printed output is capped in size, and the full results are logged where the model can search them later. Calls that don't depend on each other run concurrently, so a batch takes as long as its slowest call.

Fig. 2 Programmatic tool calling

Direct tool calls

The model is called again after every one or two tool calls.

Model calls

10

Tool calls

15

Elapsed

56.8 s

Script tool

Each model call writes one program that runs its tool calls and returns one result.

Model calls

5

Tool calls

15

Elapsed

41.6 s

Model call Tool call Script Time saved

One common session pattern, fixing a failing unit test with GPT-6.1 Sol at high reasoning, replayed both ways on one clock. With **direct tool calls**, the model is called again after every one or two tool calls, 10 times in all. With the **Script tool**, each model call writes one program that runs its tool calls and returns one result, so the same 15 tool calls take 5 model calls. Time spent in model calls falls from 42.3 s to 28.0 s, and the task finishes in 41.6 s instead of 56.8 s. Tool durations are measured. The direct run places the same calls one or two per model call, with 0.15 s between a tool result and the next model call. Each tool call has its own row, as wide as the call took. Hover or tap a bar for its exact timing.

Because these calls are code, one result can influence the next call. For instance, a program can search, read every match, and filter the results in one pass. With direct calls, each step would cost a model request.

Compared to direct tool calling, Script mode cuts Droid's cost by 15% on Claude Opus 5.5. Most Scripts are small, and the per-task savings concentrate in the 12.5% of them that make six or more tool calls.

Two Scripts from that tail, taken from our own sessions (simplified, with names and identifiers changed), demonstrate the effect. For each, a Script and direct calls make the same tool calls. The difference is how many model requests they take: direct calls fit a few into each request and wait for the model between steps, while a Script runs them all in one program. Direct-call figures are estimates, assuming 3 to 10 calls per request.

The Linear cleanup moved 151 issues between queues and verified each move, 312 tool calls in all. With direct calls, every request re-sends the instructions and the growing history, so even at 10 calls per request the task would take 36 requests and read ~3.1M input tokens. The Script took 2 requests and ~61,000 tokens: one request to write the program, and one to read what it printed.

The CI sweep shows the other half of the savings: what the model reads. The Script checked 5,384 desktop jobs across 547 runs, 550 tool calls, 60 at a time, in 2 requests instead of an estimated 59 to 187. The model saw only a five-number summary, including 41 failed jobs. Under 0.1% of the tool results reached its context. The sweep ran in the background for about 8 minutes while the model worked on another task.

Fig. 3 Script vs direct

The Script, written in request 1text() prints to the model

A real Script from Factory’s own sessions, the Linear cleanup, simplified, with names changed. Both sides run on one illustrative clock. The direct side is a modeled estimate at 10 calls per request: each batch waits for the model to read the previous batch’s results. At 3 calls per request it would take 107 requests. With about 28,000 tokens of instructions re-sent on every request, the direct side reads ~3.1M input tokens; the Script reads 61,000. Result sizes are estimated from typical issue sizes.

### How it improves quality

- **A cleaner context.** Raw files, search results, and logs stay in the program, so the model reasons over less noise.
- **Loops and workflows run deterministically.** The Linear cleanup compared 15 fields before and after every write, kept exact counts, and was written to stop at the first issue that changed in any other way.
- **Planning happens up front.** The model works out the whole sequence in its reasoning, and the program it writes is the plan. Stronger models plan further ahead, so their Scripts are more complex and do more in a single request.

Frontier models already get the most out of programmatic tool calling, and we expect the gains to grow as the frontier does.

Script mode is on by default for GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Astra, GPT-6 Sol, GPT-5.6 Sol, Claude Fable 5.1, Claude Fable 5, Claude Opus 5.5, Claude Opus 5, and Kimi K3.

### Design choices

Programmatic tool calling is simple to add and easy to get wrong. These are the choices that mattered most.

| Choice | How it works | Why it matters |
| --- | --- | --- |
| **Programs get real data** | Whole files, and structured, typed search results. | Filtering and counting happen in code, at no token cost. |
| **Literal text travels raw** | File contents, patches, and commands go in raw input blocks, not escaped strings. | Fewer tokens and fewer malformed calls. |
| **Edits come back short** | An edit inside a program returns the same short summary as a direct edit. | The file isn't pasted back into context. |
| **Never blocked on a long job** | A program waits up to 5 minutes, then hands back its output so far. It can also start in the background and return at once. | The model keeps working. |
| **No polling** | A dedicated tool checks on, waits for, or stops a running program. Droid wakes the model when background work finishes. | No requests are spent asking whether a job is done. |

## The Agent Factory

Script mode, and the per-model choice of whether to use it, came out of the same loop that produces most of Droid's changes. New models and snapshots arrive every few weeks. No team can keep up by tuning a harness for each one by hand.

Fig. 4 How Droid is built

An engineer merges

The harness every model runs on, and the agent that runs this loop.

Each new model enters at step 1. Droid runs every step itself, and nothing ships until an engineer reviews and merges it. The improved Droid then runs the next loop.

The loop starts when a model first becomes accessible, often as an early-access snapshot. An automation that tracks more than 20 models adds it to Droid and checks it against our behavioral assertions. Passing those is the minimum, not the bar for release. From then on, every available model is evaluated through the product itself: in live environments, through QA, and on daily benchmark runs. Live error logs and the friction users hit are added to each model's results, so the agent reviewing them sees benchmark failures and real sessions side by side.

A single failure says little, so the agent looks for causes that repeat across tasks and models. It turns each finding into a proposed change that states its hypothesis, and a controlled experiment measures the change on every model it touches.

Because agents write most of these changes, the agent proposing a change and the engineer reviewing it need the same idea of what a good change looks like. Every turn re-sends the whole request, so a badly placed instruction or a stale tool output doesn't hurt just once. It distracts the model on every turn after it, costing quality, tokens, and time. Every proposal is held to the same principles:

- Budget every token, and keep large tool results in files.
- Grow the request by always maintaining the prompt cache.
- Profile the hot path to inference, and cache anything you can.
- Track background work, such as long commands and subagents, and wake the model when it finishes.
- When the agent gets stuck, always have a next step ready: nudge, retry, summarize, or stop.

The changes that Droid proposes depend on the goals it works toward. An added requirement is that each goal must hold on every model family. When we tuned Script mode on GPT-6.1 Sol, Claude Opus 5.5, GLM 5.3, and Kimi K3, one of our targets was that, given both Script and direct tools, models should choose Script. The loop produced changes to the prompt, the descriptions of tools called inside Script, and the structure of Script results. No single change moved every model, but together the three met the goal on all of them.

Another goal was that Script mode cost less than direct calls on every family. Numbering every line of every file read stopped Sol from re-reading files through the shell to get line numbers, and cut Opus's cost by 22% on one task. It also added about two tokens per line to every read, which raised cost by 8% on GLM and 32% on Kimi, models that had nothing to save. It shipped as an option the model asks for when it needs line numbers.

Engineers sit at the end of the loop. They read each proposal with its evidence, check it against these principles, and decide what ships. The result is a harness that keeps pace with that of the model providers.

## Beyond programmatic tool calling

Programmatic tool calling was the largest change the loop produced, but not the only one. The rest are smaller and spread across the harness: how much of each request the provider can reuse, what each request contains, how the loop recovers when a turn goes wrong, and how quickly each request goes out.

### Keeping the prompt cache warm

Providers cache requests by prefix, so any change invalidates everything after it. Droid's requests were already append-only, with one exception: tool discovery. Tool definitions sit near the top of the request, so loading an MCP or connector tool mid-session meant reprocessing the whole conversation. Droid now appends newly discovered tools to the end of the request, leaving the cached prefix untouched.

Fig. 5 Loading a tool

An illustrative request, both ways

Before · new tool inserted into the tool list

73,500 tokens processed fresh

28,000 reused from cache

Droid 1.0 · new tool appended at the end

1,500 tokens processed fresh

100,000 reused from cache

| Change during a session | Next request, read from cache |
| --- | --- |
| Git status changes  In testing · 19,976 tokens reused, 176 new | 99.1% |
| Session rolled back  In testing | 99.8% |
| Second subagent, same type  In testing | 96.5% |
| New tool loaded  Before-and-after test, Azure · All 26,400 tokens reused | 100% |

Read from cacheProcessed againNew tokens

Top: an illustrative request of about 100,000 tokens, with about 28,000 tokens of instructions and tools ahead of the conversation. A provider reuses the start of a request only up to the first change. Inserting a tool into the tool list changes the request near the top, so the whole conversation after it is processed again. Appended at the end, the tool is the only new part. Bottom: other changes during a session, and the share of the next request read from the cache, measured in testing; the tool load was a before-and-after test on Azure.

In production, the typical request reads 98% of its input from cache, and 98.6% of requests are strictly append-only. A monitor keeps it that way by comparing every request with the one before it and naming any part that broke the cache. These breaks are costly: a single changed token early in the request forces a full reprocess. They're also ideal work for the Agent Factory, which has shipped several prompt cache fixes. After a git status change, the next request now adds only 176 new tokens. A rollback reuses 99.8% of the cache, and a second subagent of the same type reuses 96.5%. Errors don't reset the cache either, because Droid retries a failed request on the provider that already holds it.

### Cutting the base prompt by 37%

The first request carries the instructions, tool definitions, and startup context that ride along on every turn after it, so it's the part of the harness we cut hardest. Between Droid 0.170.0 and 0.250.0, it shrank from 20,887 input tokens to 13,055 (37% reduction).

Most of the savings came from tools. Droid used to send 11 tool definitions up front. It now sends 2, and rarely used tools load on demand when the model needs them. Tool definitions fell by 45%, and the reminders Droid adds at startup fell by a third. The system prompt went the other way, growing 31%, even though most of the old prompt's rules were shortened. The growth comes from new guidance in two areas: how the agent talks to the user, and how it handles environment details such as images, connected apps, and personal data.

Fig. 6 Prompt budget

Measured

Tool definitions

15,798 → 8,528−46%

Startup reminders

3,463 → 2,362−32%

System prompt

1,618 → 2,155+33%

The message “hi”

8 → 10+2

Total

20,887 → 13,055−37%

0.170.0 on Opus 4.80.250.0 on Opus 5.5

Input tokens on the first request of a session, where the user types “hi”: Droid 0.170.0 on Claude Opus 4.8 against 0.250.0 on Claude Opus 5.5. These parts ride along on every turn after it. Droid used to send **11** tool definitions up front and now sends **2**; rarely used tools load when the model needs them. The two releases ran on different models, so the tokenizers differ; counted in characters, which don’t depend on the tokenizer, the request fell from 57,035 to 36,802 (−35%).

Much of the rewriting was done by the models themselves. An automation routinely gives a model Droid's instructions and asks it to find guidance that's repeated, contradictory, or unclear. Each finding becomes a proposed edit, tested like any other change.

### Bounded autonomy

The longer an agent runs on its own, the more ways it can get stuck, repeat work, or drop the task entirely. Droid detects each of these, and every case results in a defined next step: a nudge, a retry, or a stop. The rules live in the loop rather than the model, so they hold for every provider Droid supports, and a new model gets them on day 0.

Getting stuck usually shows up in the stream. On Factory-managed Anthropic streams, 4 minutes of silence counts as a dropped stream and is retried. A response that hits a hard time limit gets at most two attempts, and one that breaks partway through is removed before the retry, so the model builds only on complete answers.

Repeated work is caught by counting. Three turns in a row with no visible output, and Droid stops. Three identical tool calls get a nudge, and six stop the loop. Repeats that return new results, like polling a build, can continue.

Dropping the task most often happens when a long conversation is summarized. These compaction summaries now have room for 16,000 tokens, up from 8,000, because by our estimate a third or more were filling the old limit.

However, not every long wait is a failure. When the model starts work that will take a while, such as a subagent or a long-running command, it can move that work to the background and sleep. Droid wakes it with a reminder when the work finishes.

### Profiling the hot path

With requests cached and trimmed, the model's response time was mostly out of our hands. How quickly we got the request to it was not. Droid rebuilt its list of connected apps on every turn, and pre-flight tool lookups slowed down as session histories grew.

The first turn had the most overhead. Sign-in checks duplicated work and ran one after another. Startup requests waited for all of Droid's code to load, and the first model request waited for every MCP server to settle. Users bringing their own Amazon Bedrock credentials faced an additional delay while those credentials loaded.

In our latest update, each of those waits is gone or out of the way. Droid reuses its list of connected apps until a connection changes, cutting turn preparation to 24 ms. In a controlled test, that change alone made the median response finish 13% sooner. Droid now reads only the newest part of the session history, so pre-flight tool lookups take about a millisecond. Sign-in checks run in parallel without repeats, dropping from 101 ms to 59 ms median. `droid exec` sends its identity, feature-flag, org-policy, and connector requests together while its code is still loading, cutting median time to the first model request from 1,741 to 646 ms. MCP servers start alongside the first turn, so a server that takes 3 seconds to initialize no longer holds it up, and Bedrock credentials are ready before the first request. Beyond the user's machine, a routing fix in our inference proxy shaved 150 ms off every model call.

The results are evident in a real production agent turn. Droid took 124 ms from Enter to send the request: 97 ms to gather context and 27 ms to build it. This means the model request is responsible for 97% of the wait users experience for the first token.

### Fast from launch

Beyond the agent loop, Droid 1.0 cuts the latency users hit in the app itself: opening it, starting a session, running several at once, and quitting.

Faster first paint · 1,839 → 488 ms

Faster to the first prompt · 1,876 → 618 ms

Quit, production median · was 648 ms

Opening is the first wait in every session. Between the August 25 and October 20 releases, median time to first paint fell from 1,839 to 488 ms, and time until Droid accepted a prompt fell from 1,876 to 618 ms, cuts of roughly 70% each. Most of that came from doing less before the first frame. Droid now ships precompiled code, so about 6,000 modules are no longer parsed at launch. Keystrokes register while startup finishes, and CI fails any change that pushes first-keystroke p95 above 250 ms. Upgrading to Bun 1.4.2 cut p95 startup time by 13–22% across Linux, macOS, and Windows, and for the last, Droid now also skips console setup and caches the system certificate list.

Sessions on remote computers run in a daemon, so they can't start until the daemon is ready. The daemon used to wait for the login shell, certificates, locales, and skills to load first. Now each of these loads just in time. Median time from launch to ready fell from 1,956 to 392 ms on a developer's Mac, or from 887 to 376 ms with an empty shell config.

The deepest change was architectural. Running several sessions at once used to mean running several processes, each using about 350 MB of memory, so five parallel subagents and the main session took more than 2 GB. They now share the daemon's process, each session adds about 20 MB, and `/new` is instant.

Quitting is the last wait, and it used to depend on the network. Droid now hands the telemetry and session sync it still owes to a detached process and exits. Median quit time in production fell from 648 to 30 ms.

## Faster than ever before

The changes that save tokens can save time too: Script mode makes fewer requests, and each one that remains is smaller and mostly cached. On Claude Opus 5.5, Droid takes 26% less time per passed task than Claude Code and uses 17% fewer tokens. On GPT-6.1 Sol, it uses 12% fewer tokens than Codex, while taking 10% longer.

Fig. 7 Terminal-Bench 4

GPT-6.1 Sol

Cursor isn’t shown: it has no access to OpenAI models.

Opus 5.5

Terminal-Bench 4. With Opus 5.5, Droid takes 16% to 26% less time per passed task than every other harness. With GPT-6.1 Sol, it takes 10% longer than Codex at 12% lower cost, and 4% to 11% less time than OpenCode and Devin. [Methodology](#methodology)

These times cover only the task itself. Around each task, Droid opens, starts sessions, and quits in a fraction of the time it took in August, so starting a new session or switching between several costs almost nothing.

## Try Droid 1.0

Droid 1.0 is available today. [Download the desktop app](https://factory.com/product/desktop) for macOS and Windows, or [install the terminal UI](https://factory.com/product/cli).

To build on top of the same harness, use the [Droid SDK](https://github.com/Factory-AI/droid-sdk-typescript) (`@factory/droid-sdk`). It runs the same Droid as the CLI, so every change in this post ships with it. From Node, an application can start Droid, hold multi-turn sessions, stream its work, and give it custom tools over MCP. From another process or a local browser tool, it can connect to a running Droid daemon and manage sessions there.

## Methodology

- **Head-to-head.**
	- Versions used: `codex@0.163.0`, `claude-code@2.1.306`, `cursor-cli@2026.10.19-6bbf2c4`, `devin@3000.11.92`, `opencode@2.1.2`.
		- Models used: Claude Opus 5.5 (high reasoning) and GPT-6.1 Sol (high reasoning).
		- High reasoning was chosen as it is the most popular reasoning option on our platform, thus best representing the workloads delegated to Droid.
		- Benchmark: Terminal-Bench 4, all tasks, default time limits, run October 23–28, 2026.
		- Each harness ran three trials per task.
		- Trials that failed for reasons outside the harness were rerun: the eval failed to launch, a model request timed out, or the provider was out of capacity.
		- Anthropic's content moderation stopped some tasks on Claude Opus 5.5. For every harness that experienced this, those trials were rerun on Claude Opus 5 until no content moderation errors occurred. GPT models had no such blocks.
		- Devin has no way to turn off its tool for asking the user a question, so on some tasks using GPT-6.1 Sol it stopped to ask instead of finishing. To keep the comparison fair, a task where Devin stopped to ask was counted as passed if Codex passed it (an average of 4.7 tasks per trial). This affects accuracy only, not cost or time.
		- Cursor undercounts tokens when it reconnects mid-task, so for the two trials this occurred in we estimated the missing usage from the transcript.
		- Cost and time are per passed task, at each provider's list price. Charts run cost from most expensive on the left to cheapest on the right.
		- Droid is compared with one harness at a time, on the same model.
		- We only count tasks that both harnesses passed in all three trials, so both are measured on the same work.
		- Cost is based on tokens used, priced at list price.
		- Time is how long the agent spent working, not counting setup or grading.
- **Everything else.**
	- Every change described here runs in production Droid.
		- Production numbers come from Droid's own telemetry, with CI excluded: prompt reuse, launch medians for the newest release each week, quit times, and the first-turn trace.
		- Prompt reuse is measured per request: the share of input tokens read from the provider's cache, over 20.4M production Droid CLI requests in the 7 days to Oct 22, with CI and evals excluded. Weighted by tokens instead of by request, the share is 91.5%. Append-only is the share of requests the prompt-cache monitor did not flag.
		- Some metrics related to startup time come from controlled tests that compare the builds before and after a change on the same tasks and machine.
		- Modeled numbers are the direct-call side of the Script examples: 10 calls per request at the low end, 3 at the high end, and about 28,000 tokens of fixed instructions per request.

Cite as

Factory Research. "Droid 1.0: Building a Frontier Harness." Factory, October 2026. factory.ai/news/frontier-harness

Droid 1.0 runs everything on this page today.

[

Try Droid

](https://docs.factory.com/droid-cli/quickstart)