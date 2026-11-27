---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-23-bas-nijholt-orchestrating-orchestrators
source_title: "I used to orchestrate agents. Now I orchestrate orchestrators. 🧵"
source_author: Bas Nijholt
source_url: https://www.nijho.lt/post/orchestrating-orchestrators/
tags:
  - source/summary
  - coding-agents
  - multi-agent
  - developer-workflow
  - agent-interfaces
source_ids:
  - src-2026-11-23-bas-nijholt-orchestrating-orchestrators
status: active
---

# I Used to Orchestrate Agents, Now I Orchestrate Orchestrators

## Summary

Bas Nijholt describes how his coding workflow moved from terminal tabs to a chat room. His tasks
now run "from an hour to more than a day" on their own, so he runs **fifteen** parallel sessions
comfortably and up to **forty** on a good day, each with sub-agents of its own. In every thread he
talks to one parent agent on Opus 5.5, which carries his skills, memories, and review standards,
picks a model per job, and delegates to minimal sub-agents. The interface that makes this workable
is MindRoom Chat, a client he built: one task is one thread, the thread is the agent's context
window, and every thread is sorted under **Needs you**, **Working**, **Later**, or **Done**. He says
"The real hard part is context management in my own head", so the post is mostly about routing
human attention. It is a first-person practitioner report by the author of the tool he praises,
with self-measured numbers and demos that stage some data.

## Key claims

### From thirty panes to one room

In August 2025 he ran 6 features at once and checked each tab every 10 to 15 minutes. In January,
`agent-cli dev` made each task a git worktree plus a terminal tab. At the peak, thirty terminal
windows covered five to eight tasks, each with a Codex pane and a Claude Code pane; "I was the
orchestrator myself". He then tried cmux (June 2026), the Codex desktop app (now the ChatGPT app,
adopted around GPT-5.2), and T3 Code, "the open-source control plane for coding agents", which he
calls "a harness for harnesses" because it wraps Claude Code, Codex, and OpenCode. Above twenty
concurrent sessions T3 Code struggled: database writes appeared to go through a single thread,
long threads took seconds to open, and threads with background tasks showed as idle. T3 Code is
MIT-licensed, so he ported its best ideas into MindRoom.

### The native harness bought little; request size mattered

He stayed with vendor harnesses because he believed a model works better in the harness it was
trained with. His own test, "Over more than 4,000 runs of short terminal tasks", found that native
harness tools made only one model clearly more efficient: Claude Opus 4.8 did **17%** less work and
used **19%** fewer tokens with Claude Code's tools, while GPT-6 Astra and Sol used **43 to 59%**
more tokens with their own harness tools. What mattered was how much the agent sends per request:
a minimal agent with one shell tool and a 12-line prompt used **58 to 76%** fewer tokens than
MindRoom's standard agent. Leaving the native harnesses let him mix Anthropic, OpenAI, and Google
models in one thread, with every sub-agent in minimal mode.

### Longer tasks come from models and skills

He credits Claude Opus 5.5 and Claude Fable 5.2 for handling larger scope, and his public skills,
baspowers: the agent writes a spec and a plan, works test-first, and cross-checks ambiguities with
another frontier model, such as GPT-6.2 Astra, before involving him. The `consulting-cross-model`
skill has Claude ask GPT-6 Astra and Codex ask Claude Opus 5.5. In one test, agents wrote a failing
test before fixing a bug in **0 of 32** runs without his test-driven development skill and **32 of
32** with it.

### One parent per thread, routed sub-agents

"forty sessions can easily mean a hundred agents in flight". The parent picks models by rules in
its system prompt:

- Code is written by Gemini 4 Neon by default ("only came out a couple of days ago", "pretty
  expensive").
- GPT-6.2 Sol, GPT-6.2 Astra, and Opus 5.5 review the full diff in parallel; "no model reviews its
  own code". After a fix round, a fresh reviewer checks the whole diff.
- Fable 5.2 writes code only for very complicated tasks, or when two review rounds still find
  major issues.
- Simple lookups go to Claude Haiku 5.5.

### The room routes attention

The room view went through six versions: first messages, AI-generated titles, resolve, sort and
filter, one-card Compact view, and then sections. **Needs you** means the agent finished or asked
something and nothing is running; **Working** includes a running sub-agent or background job;
**Later** is snoozed or scheduled; **Done** is resolved. Counting background jobs as Working fixes
the T3 Code confusion. Finished turns fold behind one row, as in T3 Code's "Worked for" row, but
the folded text remains the model's own output. The client is keyboard-first, has a model picker
with an Effort column and pull-request cards with a diff panel, and hides test files "because I no
longer read them". Threads get their own worktree and linked pull requests. He works from one
meta-repo checkout, using screen recordings and voice, and has an Apple Watch app.

### Plugins and canvases

The pull-request panel and worktree support live in plugins, "building real features as plugins
is how I know the plugin interface is strong enough". An error-notifier plugin posts errors into a
room; an agent triages and opens a pull request. Agents proposing UI changes can send an
interactive HTML canvas into the thread, where he clicks through variants and sends a choice back.
MindRoom Chat is Apache-2.0.

### Review, output, and cost

Rigid "software factories" with strict harnesses feel "very anti-Bitter Lesson" to him. He no
longer reads code line by line; three other models review each pull request, "always at least two
models different from the one that wrote the code", and his own review is mostly questioning the
agent. He reports spending "$50,000 to $100,000 a month in model usage", which he does not pay. He
"couldn't think of a recent run that went badly wrong", and his earlier hooks "barely matter".

Counted by his trueloc tool on November 20, 2026, his merged pull requests went from about **1.4
million** lines in **848** pull requests (November 2024 to October 2025) to about **10 million**
lines in **5,148** pull requests over the next twelve months, with about two thirds in code files.
He says lines of code are "not a measure of quality" and should be read "as the amount of work in
flight". The September 2026 jump coincides with GPT-6 Astra and Claude Opus 5.5.

## Why it matters

- [[Agent Delegation]]: a concrete parent-plus-minimal-sub-agent pattern with per-job model rules
  and a no-self-review rule.
- [[Coding Agent Harness]] and [[Context Engineering]]: a self-run test against the belief that a
  model needs its native harness, and evidence that request size dominated.
- [[Agent Workflow Maturity]]: a practitioner who moved past terminal orchestration and argues
  against rigid factory pipelines.
- [[AI-Native Software Development Lifecycle]]: model-only review before a human sees a pull
  request, and a human who reads trade-offs rather than code.
- [[Agent Plugin Architecture]] and [[Generative User Interface]]: features shipped as plugins, and
  HTML canvases that return a decision to the agent.
- Proposed for [[Agent Skill]], [[Model Routing]], and [[AI Code Review]].

## Tensions / open questions

- He built the tool he praises, and says so: "I built the tool I'm praising"; he also wrote that
  "most new AI tooling is not very good, and MindRoom may well be included".
- The native-harness numbers come from a separate post that is linked but not captured; task mix,
  models per run, and success rates are not given here.
- The demos replay real thread text but stage tool calls, background jobs, and their numbers;
  canvases use placeholder data.
- Line counts include churn, generated files, and rewritten agent code; he disclaims them as a
  quality measure, and the September jump coincides with new models, so the chart cannot credit
  MindRoom.
- "No recent run went badly wrong" is recall, not an incident log, at **$50,000 to $100,000** a
  month in model usage paid by someone else.
- The parent's rules apply to his own repositories; no review accuracy or defect rate is reported.
- The TDD figure (0 of 32 vs 32 of 32) measures whether a test was written first, not code quality.
- He expects the workflow "to look different in a few months".

## Affected pages

- [[Agent Delegation]]
- [[Agent Workflow Maturity]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Plugin Architecture]]
- [[Generative User Interface]]
- [[Agent Skill]]
- [[Model Routing]]
- [[AI Code Review]]

## Raw capture

- [[knowledge-base/raw/sources/I used to orchestrate agents. Now I orchestrate orchestrators. 🧵]]

## Citations

- Canonical URL: https://www.nijho.lt/post/orchestrating-orchestrators/
- Byline: Bas Nijholt (personal blog, nijho.lt).
- Published: 2026-11-23. Captured: 2026-11-25 (newsletter-tracked URL; tracking parameter removed).
- An inline SVG chart of monthly lines was skipped; only figures stated in prose and footnotes are
  reported.

## Related pages

- [[Agent Delegation]]
- [[Agent Workflow Maturity]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[AI-Native Software Development Lifecycle]]
- [[Agent Plugin Architecture]]
- [[Generative User Interface]]
- [[Agent Skill]]
- [[Model Routing]]
- [[AI Code Review]]
- [[Loop Engineering]]
- [[William Hu - Building Always-On Agents]]
- [[Frank Rousseau - Agentic Coding on an Open-Source Project]]
- [[@L1vsun - Prompt, Context, Harness, Loop, Graph - The 5 Levels of AI Engineering]]
