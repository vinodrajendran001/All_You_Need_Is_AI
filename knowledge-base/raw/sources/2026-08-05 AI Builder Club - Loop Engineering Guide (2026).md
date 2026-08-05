---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-loop-engineering-guide-2026
title: Loop Engineering Guide (2026)
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/loop-engineering-guide-2026
published: '2026-06-17'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Loop Engineering Guide (2026)

**Loop engineering is the discipline of designing the loop an agent runs inside - what it does between tool calls, when it checks its own work, and how it decides it's finished - instead of hand-writing each prompt.** It's the 2026 successor to prompt engineering. The model writes the prompts now. The scarce skill is defining what "good" and "done" mean, and the part almost every explainer skips is this: in any loop, the **verifier** is the bottleneck, not the model.

A few mornings ago I typed one sentence into Claude Code and went to make coffee. By the time I got back, something like forty agents had spun up, written code, checked each other's work, thrown away the bad attempts, and left me three pull requests to review.

I didn't write forty prompts. I wrote one loop.

If you've felt the ground shift under "prompt engineering" lately, this is why. Here's the decode - not the hype version, the version you can use this afternoon.

AI Jason breaks down the same shift in his "Loop Engineer: Systemization and Artifacts" video - what the term actually means, the four core ingredients, and how his team designs loops that compound:

---

## How Did We Get From Prompt Engineering to Loop Engineering?

It helps to see the line this sits on:

| Year | Era | What you do | Your role |
| --- | --- | --- | --- |
| 2024 | **Prompt engineering** | Write a good prompt, get a good output | Operator |
| 2025 | **Parallel agents** | Stop babysitting one chat, run several at once | Manager |
| 2026 | **Loop engineering** | Build the loop that runs the agents for you | System designer |

The people behind Claude Code have said the quiet part out loud: some mornings they aren't really writing the prompts anymore - another model is - and they're managing hundreds, even thousands, of agents at a time. That sounds like a flex until you see what it implies: **if you're not in the loop pressing enter between every step, something else has to decide when the work is good enough.** That something else is the whole game.

---

## What Is a Loop, Exactly?

Strip the jargon and a loop is four moves on repeat:

> **discover → plan → execute → verify → (repeat until a condition is met)**

You used to *be* the loop. You were the thing standing between the agent's steps, reading the output, catching the mistake, deciding what happens next, telling it to try again. Loop engineering is the discipline of stepping *out* of that inner cycle and *up* to designing the track the agent runs on.

Here's the simplest possible version. Give the agent a goal and a stopping condition, and let it run:

text

```
Goal: get the test suite passing.
Loop: run the tests, read the failures, fix the most likely cause, run again.
Stop when: all tests green, or you've tried 6 rounds (then summarize what's left).
```

That's a loop. And it genuinely works on a simple task. But point a loop at something open-ended - "improve this app," "make this page better," "research X and write it up" - and it either produces something great or it quietly turns into a very expensive slop machine. The difference between those two outcomes is the part nobody talks about.

---

## Loops Nest: Andrew Ng's Three-Loop Model

The discover → plan → execute → verify cycle above is the *inner* loop. Zoom out and you'll find it wrapped inside slower loops. Andrew Ng laid this out cleanly in a [June 2026 Batch letter](https://x.com/AndrewYNg/status/2071988145667928442) - and the fact that *he* wrote it is itself the signal: "'Loop engineering' is a hot buzzphrase after mentions of it by Boris Cherny (Claude Code's creator) and Peter Steinberger (OpenClaw's creator) went viral." When Andrew Ng devotes a whole letter to a term, it has left buzzword territory.

His model is three loops running at different speeds:

| Loop | Cadence | Who runs it | What it decides |
| --- | --- | --- | --- |
| **Agentic coding loop** | Every few minutes | The agent | Write code, test it, iterate until it's bug-free and meets the spec (and evals, if you have them) |
| **Developer feedback loop** | Tens of minutes and hours | You | Review the product, steer the agent, update the spec |
| **External feedback loop** | Rarely less than hours; sometimes days or weeks | The world | Alpha testers, A/B tests, production data - feeds your vision back into the spec |

code

```
  ┌──────────────────────────────────────────────────────┐
  │  EXTERNAL FEEDBACK LOOP (rarely < hours; days/weeks) │
  │  alpha testers · A/B tests · production data          │
  │   ┌────────────────────────────────────────────────┐ │
  │   │  DEVELOPER FEEDBACK LOOP  (tens min/hours)     │ │
  │   │  you review · steer · update the spec          │ │
  │   │   ┌──────────────────────────────────────────┐ │ │
  │   │   │  AGENTIC CODING LOOP  (every few minutes)│ │ │
  │   │   │  generate → test → verify → repeat       │ │ │
  │   │   └──────────────────────────────────────────┘ │ │
  │   └────────────────────────────────────────────────┘ │
  │              vision ──► spec ──► agent                 │
  └──────────────────────────────────────────────────────┘
```

Watch what changes as you move outward: the loop gets slower, and the verifier gets more human. The inner loop can verify itself with tests. The outer loops can't - they need you. Ng makes the sharpest point right here, and it's a friendly amendment to the "taste is the reward function" idea coming up next. People call the human contribution "taste," he writes, but he prefers "context advantage": "So long as the human knows something the AI does not, human-in-the-loop is needed to inject that knowledge." Taste sounds innate and unteachable. "Context advantage" tells you exactly what to encode into the loop: the things you know about your users and your problem that the model doesn't. That's your verifier, written down.

And here's his tell for when to graduate from eyeballing output to a real verifier: "If you find that the system repeatedly runs into certain problems, building a set of evals for the agent becomes useful." Same lesson as the landing-page example below - the moment you're checking the same thing twice, write it into the loop.

---

## Why Is the Verifier the Bottleneck, Not the Generator?

Every loop has two halves. The **generator** produces work - that's the model, and models are now extremely good. The **verifier** judges whether that work is good. Put it plainly: a loop is just a generator wired to a verifier, and the generator was never the bottleneck. The verifier is.

For two years we obsessed over the generator. We tuned prompts, swapped models, argued about temperature. But in a loop, the generator runs over and over for nearly free. The thing that decides whether all that motion produces *value* is the verifier.

And the freer you let the loop run, the more everything rides on the verifier. A loop with a weak "good enough?" check doesn't fail loudly. It succeeds at producing garbage, confidently, hundreds of times.

This is the same shift [Addy Osmani](https://addyo.substack.com/p/code-review-in-the-age-of-ai) keeps pointing at: the bottleneck moved from writing code to proving it works - it's the through-line of [the essay that named loop engineering](/blog/loop-engineering-addy-osmani), and of his follow-up rule that agents run the inner loop while you own the outer one. [Karpathy lands on the same place](/blog/loop-engineering-karpathy) from his generation-verification loop: generation got cheap, so the loop spins only as fast as its verification half. Review, judgment, taste, knowing what "correct" looks like - that's now the most leveraged skill an engineer has. It's the same lesson [agent evaluation](/blog/how-to-evaluate-ai-agents) teaches at the production layer: a model grading its own homework always gives itself an A. In a loop-engineering world, your taste isn't a soft skill anymore. **It's the reward function.**

---

## Open Loop vs Closed Loop: Which Should You Build?

Once you accept that the verifier is the point, the engineering decision gets clear. Every loop sits somewhere between two poles.

|  | Open loop | Closed loop |
| --- | --- | --- |
| **What it is** | Give a goal and loose conditions, let it explore a wide space | Pin success criteria in advance, evaluate every step, define an explicit stop |
| **Upside** | Genuinely novel output. Surprising solutions live here | Runs on a normal budget. Predictable. Safe to leave alone |
| **Downside** | Burns tokens. Degrades into slop fast with loose criteria | Won't surprise you. Does what you specified, not more |
| **Lives or dies by** | The verifier (even more so) | The verifier |

The actual *engineering* is two decisions:

1. **Choose open or closed for this specific task.** Roughly: how much do I need novelty, and how much budget am I willing to risk?
2. **Write the verifier that matches.** A closed loop needs hard, checkable passes. An open loop needs an *even better* verifier, because it's the only thing standing between exploration and slop.

---

## What Does a Loop With a Weak Verifier Actually Produce?

The most useful thing isn't a loop that works. It's the same task run two ways.

TAKE 1 - OPEN LOOP, WEAK VERIFIER

"Make this landing page better. Keep iterating." No definition of "better." It rewrites the hero eight times, each version different, none clearly better, all plausible. It reports success. You spent real money to get motion without progress. That's the slop machine - and almost everyone's first agent loop is exactly this.

TAKE 2 - CLOSED LOOP, EXPLICIT VERIFIER

Same task, but every iteration has to clear a bar you defined. Motion can only happen in the direction of "better." The loop converges instead of wandering.

Here's Take 2 written out:

text

```
Goal: improve landing-page conversion clarity.
Done when ALL pass:
  - Lighthouse accessibility score >= 95
  - Exactly one primary CTA above the fold
  - Hero headline states the value prop in <12 words
  - No layout shift (CLS < 0.1)
Loop: propose a change -> run the checks -> keep it only if every check still passes
      -> stop when all green or after 5 rounds.
```

Now the loop converges, because every iteration clears a bar *you* defined. Then comes the trick that rescues open loops too: keep those hard checks as the floor, and add one open instruction ("surprise me with the headline"). Now you get exploration *that can't degrade below your standard.*

The lesson isn't "closed loops are better." It's: **the verifier is what makes either kind ship.**

---

## What Tools Can Run the Loop For You?

You don't have to build the loop machinery from scratch. There's a clear lineage, from rigid to autonomous:

| Tool / pattern | How it decides "done" | Best for |
| --- | --- | --- |
| **"Ralph" loop** | A bare shell `while` loop re-fires the same prompt until you stop it - no smart "done," you are the stop button | Mechanical, repetitive tasks. Crude but bulletproof |
| **Claude Code [`/goal`](https://code.claude.com/docs/en/goal)** | A small fast model judges the stop condition after every turn | Fuzzy "done" that still needs evaluating |
| **Goal-tracking setups** | Agent tracks its own progress in files, defines "done" up front | Long runs that need to stay oriented |
| **Self-hosted agents (Hermes-style)** | Runs continuously on its own infrastructure, keeps state across sessions | [Always-on agents you set up once and leave running](/blog/hermes-nous-research-self-improving-agent) |

`/goal` is the cleanest entry point: you type a completion condition once, and after each turn a Haiku-class evaluator reads the transcript and decides yes or no, looping until it holds (or you hit your turn cap). One catch worth knowing - the evaluator only sees what Claude already printed, so your condition has to be provable from the agent's own output.

Pick the least autonomous tool that does the job. Autonomy is not the goal. **A shipped result is the goal.** This table is really a ladder - each rung hands off one more part of the cycle, from approving tool calls to owning the trigger itself - and we map every rung, with when to climb and when not to, in [The 4 Types of Agentic Loops](/blog/types-of-agentic-loops). For how the team that builds these primitives runs its own loops in production, see [Loop Engineering: The Anthropic Playbook](/blog/loop-engineering-anthropic-playbook). When the work fans out wide and repetitive, push the loop into a script with [dynamic workflows](/blog/claude-code-dynamic-workflows) instead of babysitting it.

---

## What Does a Real Loop System Look Like?

A single loop is useful. A *system* of loops that share a brain is where the leverage compounds. This is what AI Jason runs inside his own company.

Start with the simplest one: a **support loop**. Every 30 minutes a cron wakes an agent. It pulls every support ticket, replies to the ones it can answer, and logs the frictions and product ideas it spots into a shared folder called `signals`. That loop alone earns its keep.

Now make it compound. The same loop doesn't just *log* a bug - it spawns a coding agent to fix it, monitors whether the fix held, and tells the customer it shipped. If people still hit the issue, that means it wasn't fixed at the root, so the loop tries again.

The real trick is that every loop reads *and* writes the same shared folders. Jason runs several at once:

| Loop | Trigger | What it does | What it writes |
| --- | --- | --- | --- |
| **Support** | Every 30 min | Answer tickets, spot friction | `signals`, engineer tasks |
| **SEO** | Daily, 9am | Pull data, research topics, publish pages | pages, conversion-gap `signals` |
| **Product growth** | Daily | Prioritize experiments from analytics + signals | tasks |
| **Reddit** | Scheduled | Draft on-brand comments | comment artifacts |

Because they share one file system, the SEO loop's "this keyword converts but we have no organic content" signal feeds the content loop. The support loop's repeated-bug signal gets picked up by the product loop. Each loop runs every hour or every day, reading what the others learned. **The shared brain is what makes it compound** - and Jason's quoted output from this setup is 20 to 40 high-quality pages a day driving traffic without him looking at it.

Which one do you build first, though? That question is the whole migration, and it has a defensible answer: start where the output is frequent, measurable, reversible and not customer-facing, then earn autonomy function by function. We walk the full sequence, with a real loop spec, the shared-state schema, the per-run costs and the failures, in [how to become an AI-native company](/blog/how-to-become-an-ai-native-company).

---

## The 4 Ingredients of a Loop That Compounds

Jason's framework boils down to four parts. Most people nail the first three and skip the fourth - which is the one that actually decides whether autonomous work is possible.

1. **Triggers.** What wakes the agent. A cron job, a webhook, another agent, a server incident. The point is the agent runs *without you* pressing enter.
2. **File structure.** The most important design decision. Where artifacts, contracts, and logs live (covered below).
3. **Tools and connectors.** The skills and scripts that let the agent do real work - Intercom to fetch tickets, Stripe to check subscriptions, Supabase to debug, Playwright to test.
4. **An agent-ready codebase.** The setup that lets many agents work in parallel and verify their own output. This is the one everyone misses.

---

## How Do You Make a Codebase Agent-Ready?

Before any loop works, the environment has to let an agent operate solo. Three properties:

**Legible** - the agent can find where to change what. Keep `AGENTS.md` / `CLAUDE.md` as a ~100-line index that points to deeper docs (OpenAI keeps theirs around 100 lines). Then bake rules into **custom lints** so the agent gets a warning automatically instead of you hoping it reads the right doc. Example: lint-fail any import from a legacy folder you don't want touched.

**Executable** - the agent starts work with the dev server already up, at near-zero token cost. Write a `dev local` script so it doesn't burn 3-5 minutes booting the app every run. Make the repo worktree-friendly so five parallel agents each spin up their own server without colliding. Add scripts that jump to a specific state to test scenarios fast.

**Verifiable** - give the agent tools to test and *prove* it worked. The Playwright CLI is the standout: it drives the browser and records a video clip you can attach to the GitHub PR, so review takes seconds. Back it with end-to-end tests on the flows you never want broken - sign-up, upgrade, core action.

One hard rule from the video, and it lines up exactly with the verifier point above: **don't let an agent self-verify.** It doesn't work well. Jason's PR skill always spawns a separate read-only verifier agent with the detailed spec. Generator and verifier stay different agents.

---

## The File System: Artifacts, Contracts, Logs

This is ingredient #2, and it's the heart of the system. Three file types, three jobs:

**Artifacts** - the shared knowledge layer. The output of each loop's work. Types include `docs`, `signals`, `tasks`, `tickets`, even `campaigns` for an ads loop. Each artifact type gets its own folder with a `README` defining what goes in, what doesn't, the process for adding an item, and the schema. Each artifact file carries front-matter metadata, a body, and a timeline of every change.

> A **signal** is the unit that makes loops compound. It captures a product idea, a friction, or a missed opportunity, links to its raw sources (a support ticket, a customer quote), and any loop can read or write it.

**Contracts** - one per loop, usually a `README` in the loop's folder. It states the goal, the workflow, the boundaries, the outstanding backlog, and a timeline. Every time the loop fires, it reads its contract first - goal, workflow, what happened last time - then takes the next best action.

**Logs** - a single global work-log file. Different from the timelines because your day mixes reviewing loop output with hands-on copilot work. Before an agent starts a big task it reads the last 5-10 entries; when it finishes it appends what it did. That's how cross-domain context survives between sessions.

The workflow to stand one up: run the loop manually once as a test, calibrate the workflow with the agent, then ask it to write the contract and register the trigger. Test run first, loop second.

---

## Why Writing a Verifier Is Like Defining a Reward Function

If you've touched reinforcement learning, this clicks instantly. In RL you don't tell the agent every move - you define the *reward*, and the agent iterates toward it on positive and negative signal.

That's exactly what you're doing here. You are not training the model. You are **defining the reward**: the end goal, and what counts as good. Your domain knowledge - knowing what correct looks like in *your* problem - is the moat. The model is a commodity. The reward function is yours.

This is also why the field keeps drifting toward [harness engineering](/blog/harness-six-components): the leverage isn't in the phrasing anymore, it's in the system around the model - context, tools, state, and the evaluation loop that decides when to stop. Loop engineering is that same move, named from the loop's point of view.

And watch where the vocabulary goes next. Once you accept that the verifier is the point, the natural follow-up question is *how do you write a good one* - which is exactly the ground "evals" cover. Ng's own advice ("build a set of evals when the system keeps hitting the same problems") points straight at it, and the term already circulating for this next layer is **eval engineering**: formalizing the verifier into a versioned dataset you can measure against. If loop engineering is designing the loop, eval engineering is designing the bar the loop clears. Same lineage, one level deeper.

Which is why I keep saying it: **writing the verifier is the new prompt engineering.**

---

## Is Loop Engineering Just a New Buzzword?

I'd be doing you a disservice not to flag the counter-take, because in the three weeks after the term went viral, the skeptic case grew real teeth. The strongest version has four distinct arguments, not one:

- **The vocabulary mockery.** One widely-shared post maps the whole lexicon back to CS primitives - "a while loop becomes 'loop engineering'... unit tests become 'evals'" - and it's now a genre: a 1,800-comment Hacker News thread arguing agents are "just a while loop with an LLM call," and an entire site (extra-steps.dev) dedicated to the bit, both rounded up in [PostHog's "WTF is loop engineering"](https://posthog.com/newsletter/loops). Anyone who's written a CI pipeline or a Kubernetes reconciliation loop has been "designing loops" for years.
- **The autonomy check.** [The Register's June 24 take](https://www.theregister.com/ai-and-ml/2026/06/24/loop-engineering-latest-ai-buzzword-still-needs-humans-in-the-loop/5261735): the latest AI buzzword "still needs humans in the loop." The demos hide how much steering real work still takes.
- **The economic critique.** Ed Zitron's version: the trend amounts to "celebrating and evangelizing autonomous token consumption" - spending the model vendors would very much like to stimulate. And he has a live exhibit: Uber reportedly capped engineers at $1,500/month for agent tooling after burning through its annual AI budget in four months. An unattended loop with a weak verifier doesn't fail loudly; it fails *at token prices, all night*.
- **The sampling-bias point.** The subtlest one, from developer [@*kboy* on X](https://x.com/_kboy_/status/2072169280150327436): Claude Code solving "writing software" is real, but that doesn't "give anyone the evidence to start defining how everyone should develop software" - the vendors' data comes from people already using their product.

Both things are still true at once, and that's the honest read. The word is riding a wave *and* the shift under it is real. The tell is who's using it seriously: Boris Cherny (Claude Code's creator), Peter Steinberger (OpenClaw's creator), and Andrew Ng - who wrote an [entire letter](https://x.com/AndrewYNg/status/2071988145667928442) mapping out his three loops - are not chasing a hashtag. When the people building the tools and the person who taught half the industry machine learning independently converge on the same frame, the frame is load-bearing. (And the wave is still rising: three weeks in, "Loop Engineer" is already a module title in GenAI bootcamp curricula, and Jensen Huang was echoing "prompt engineering is dead" on stage.)

So here's your filter. Ignore the *word*. Look at whether the underlying shift is real:

- Are you increasingly designing systems that run agents, instead of prompting agents directly? **Yes.**
- Is the scarce, valuable part now defining "done" and "good," rather than phrasing the request? **Yes.**
- Does a loop with a weak verifier reliably produce expensive garbage? **Also yes - see Uber's invoice.**

Here's the thing to notice: every serious criticism above attacks *weak loops*, not the discipline. Loops that still need un-budgeted human steering. Loops that burn tokens with no [halt condition or spend cap](/blog/ai-agent-reliability-cost-control). Loops graded on the vendor's own telemetry. The skeptics aren't refuting loop engineering - they're describing what happens when you skip the verifier, which is the entire argument of this guide. The label is optional. The shift is not. Whether you call it loop engineering or just "building agents that don't waste my money," the move is the same: **stop perfecting prompts, start writing verifiers.**

---

## Is Loop Engineering Dead?

No. A layer grew above it.

In July 2026 Peter Steinberger posted nine words - ["Are we still talking loops or did we shift to graphs yet?"](https://x.com/steipete/status/2078277297791189132) - and the timeline ran with it. Within days Hamel Husain published "Loop Engineering Is Dead. Enter Graph Engineering," Carlos Perez followed with "From Loop Engineering to Graph Engineering?", and by July 21 the framing had hardened into headlines like "Forget About Loop Engineering, Think About Graph Engineering." Good headline. Wrong read.

Loops did not die. A graph is what you reach for when one loop is not the whole job.

The cleanest distinction going around came from Shann Holmberg, who framed it as a question of [who decides the path, the agent or you](https://x.com/shannholmberg/status/2079096565344739643): a loop still starts with you. You set the goal, the brief, and the bar the work has to clear, and the agent owns the iteration inside those rails. A graph makes the control flow and the shared state between steps explicit instead. Edges and routing functions choose which node runs next, and a node can be a one-shot call, a tool call, a human checkpoint, another agent, or an inner loop. Some nodes loop. Others run once. The graph is the wiring; the loop is one kind of node inside it.

So the progression is not loop replaced by graph. It is:

- **One call** when the task is one shot.
- **A loop** when the task needs iteration against a bar you set. This is most agent work today.
- **A graph** when you are wiring multiple steps together, branching on what the agent finds, handing off between agents, or needing the run to pause for a human and resume durably.

Reach for a plain loop when there is a single objective, a single verifier, and no mid-run handoff. Move up to a graph when the path has to branch, route between agents, or survive a human in the middle. For the full decision guide, see [when to use an agent graph vs a loop](/blog/agent-graph-vs-loop-when-to-use) and [graph engineering vs loop engineering](/blog/graph-engineering-vs-loop-engineering).

Notice what does not change when you move up. Every node that produces work still needs a bar, and the run still needs a stop condition, or you have built a more elaborate way to burn tokens. Loop engineering is the craft of the node. [Graph engineering](/blog/graph-engineering-guide-2026) is the craft of the wiring between nodes. You need both, and the order matters: the [Loop Engineering course](/courses/loop-engineering) builds the node craft first, because a graph of unverified nodes is just a bigger mess running in parallel.

---

## Your Loop Engineering Starting Checklist

If you build one loop this week, run it through this:

1. **Define "done" in measurable terms** before you write a single instruction.
2. **Pin the passes** - the tests, the rubric, the eval - *up front*, not after.
3. **Choose open vs closed** by `need-for-novelty x budget-you'll-risk`.
4. **Always attach the run data** to whatever you hand back to a human.
5. **Use the least autonomous harness** that gets the result.
6. **Set the trigger** - cron, webhook, or another agent - so it runs without you.
7. **Give it shared folders** - artifacts, a loop contract, a global log - so the next run, and every other loop, can build on this one.

Do that and you've crossed the line from someone who *prompts* AI to someone who *engineers the system that does the work.* That's the whole skill. The rest is reps.

---

## Get This Guide as a PDF: The Loop Engineering Playbook

If you want this as a **loop engineering PDF** you can save, print, or drop in your team's Slack, we've condensed the discipline into an 8-page field manual - **The Loop Engineering Playbook**. It's not a copy of this page: the genealogy, loop anatomy, open-vs-closed decision table, and the four verifier grades each get one tight page, and it adds something this article doesn't have - a field-data page with 30 days of real Search Console numbers from the loops that run our own content, including the run that shipped nothing and the measurement bug that cost us two days.

It's free - enter your email in the signup box on this page and we'll send it over (you'll also get our builder newsletter, unsubscribe anytime).

---

## Related Content

- **[Graph Engineering: When Your Agent Outgrows the Loop](/blog/graph-engineering-guide-2026)** - The layer above loops: wiring specialized agents into a graph of nodes, edges, and shared state - and when the extra complexity is actually worth it.
- **[The 4 Types of Agentic Loops](/blog/types-of-agentic-loops)** - Turn-based, goal-based, time-based, proactive: which part of the cycle each hands off, and the doom-loop failure mode that connects them.
- **[Addy Osmani's Loop Engineering](/blog/loop-engineering-addy-osmani)** - The essay that named the discipline: the five components, the three debts, and "own the outer loop."
- **[Loop Engineering, Karpathy-Style](/blog/loop-engineering-karpathy)** - The generation-verification loop, the autonomy slider, and keeping AI on a leash.
- **[Loop Engineering: The Anthropic Playbook](/blog/loop-engineering-anthropic-playbook)** - Five Anthropic engineering essays distilled into one loop playbook.
- **[Loop Engineering vs Harness Engineering](/blog/loop-engineering-vs-harness-engineering)** - The boundary between the two disciplines, the failure modes of each, and which to build first.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)** - The generator-evaluator pattern, traces, and why self-evaluation skews optimistic. The production version of "write a verifier."
- **[Harness: The 6 Components](/blog/harness-six-components)** - Context, tools, orchestration, state, evaluation, recovery. The system around the loop.
- **[Dynamic Workflows: Orchestrate Subagents at Scale](/blog/claude-code-dynamic-workflows)** - Move the loop into a script and run up to 1,000 subagents without flooding context.
- **[From Prompts to Loops: The 4 Shifts](/blog/prompt-context-harness-evolution)** - Why AI engineering moved from phrasing to information to control to loops that run without you.
- **[Hermes: Self-Hosted, Never Forgets](/blog/hermes-nous-research-self-improving-agent)** - The "runs while you sleep" autonomous-agent pattern taken to its end.
- **[Claude Code for Data Scientists](/blog/claude-code-for-data-scientists-skills-guide)** - A concrete thing to point a loop at: wire the EDA, model retrain, and report into one chain, then schedule it to rerun every night while you sleep.

---

## Start Here

Pick one repetitive task this week. Before you write a single instruction, write down what "done" means in measurable terms. Then pin the checks, choose open or closed, and let the loop run against *your* bar instead of the model's.

Want the full build, layer by layer? The [**Loop Engineering course**](/courses/loop-engineering) takes you from "you are the for loop" to a loop that wakes on schedule, pulls the top task off your backlog, ships a PR behind quality gates, and reports back - with a copy-paste practice on your own repo every lesson.

For closed-loop templates, verifier checklists, and teardowns of loops that shipped (and loops that burned money), join the AI Builder Club - come ship something real.

Open source · free

AI Builder Club Skills

The loop tooling from this guide is open-source. /new-loop scaffolds a real loop with a verifier and a stop condition, ready to run.

[View on GitHub →](https://github.com/AI-Builder-Club/skills)

[Join AI Builder Club](/pricing?utm_source=blog&utm_medium=article&utm_campaign=loop-engineering-guide-2026)

Yes - The Loop Engineering Playbook is a free 8-page PDF field manual condensing this guide: the prompt-to-loop genealogy, loop anatomy, the open-vs-closed decision table, the four verifier grades, the artifacts/contracts/logs file system, and a first-loop checklist - plus 30 days of real Search Console data from the loops that run our own content. Enter your email in the signup box on this page and we'll send it over.

Loop engineering is the practice of designing the loop an AI agent runs inside - the discover, plan, execute, verify cycle - and defining its stop condition, instead of hand-writing each prompt. The human moves from operator to system designer. The core skill is writing the verifier that decides whether the agent's output is good enough.

Prompt engineering optimizes a single request to a model. Loop engineering optimizes the system that runs the model repeatedly: what it does between tool calls, when it checks its work, and when it stops. As models got good enough to write their own prompts, the leverage moved up a level - to defining "good" and "done" rather than phrasing the ask.

The verifier is the half of a loop that judges whether produced work meets the bar. The generator (the model) produces; the verifier decides if it ships, retries, or stops. In a loop the generator runs cheaply over and over, so the verifier - not the model - is the bottleneck that determines whether all that motion produces value.

In a June 2026 letter, Andrew Ng described building software as three nested loops running at different speeds: the *agentic coding loop* (every few minutes, run by the agent - write code, test, iterate until it meets the spec), the *developer feedback loop* (tens of minutes and hours, run by you - review the product, steer the agent, update the spec), and the *external feedback loop* (rarely taking less than hours and sometimes taking days or even weeks, run by the world - alpha testers, A/B tests, and production data that feed your vision back into the spec). The further out the loop, the more the verification depends on human context rather than automated tests.

No. In July 2026 a viral post asked whether the field had moved from loops to graphs, and several widely read essays declared loop engineering dead in favor of graph engineering. What actually happened is that a layer grew above it. A graph makes the control flow and shared state between steps explicit, and a node inside that graph can be a one-shot call, a tool call, a human checkpoint, another agent, or a loop. Reach for a plain loop when there is one objective, one verifier, and no mid-run handoff. Move up to a graph when the path has to branch, route between agents, or survive a human in the middle. Either way every node that produces work still needs a bar and the run still needs a stop condition.

Partly, and it doesn't matter. Skeptics rightly note the mechanics aren't new (a while loop with an LLM call) and that real runs still need human steering. But the shift underneath is load-bearing: Claude Code's creator, OpenClaw's creator, and Andrew Ng independently converged on the same frame within a month. The real risk isn't the vocabulary - it's unattended loops with weak verifiers burning budget, which is why the verifier and the stop condition are the whole discipline.

Eval engineering is the emerging next step after loop engineering: formalizing the verifier into a versioned set of evals - a dataset and rubric you can measure the agent against - instead of judging output by eye. If loop engineering is designing the loop the agent runs, eval engineering is designing the bar that loop has to clear. Andrew Ng's guidance is to reach for it once the system keeps hitting the same class of problem.

A closed loop pins success criteria in advance, checks every step, and has an explicit stop condition - predictable, budget-friendly, won't surprise you. An open loop is given a goal and loose conditions and allowed to explore - it produces novel output but burns tokens and degrades into slop without a strong verifier. Choose based on how much novelty you need versus how much budget you'll risk.

Because models are now strong and interchangeable, while the definition of "correct" for your specific problem is not. A weak verifier doesn't fail loudly - it confidently produces garbage hundreds of times. The verifier encodes your domain knowledge and taste, which is the part the model can't supply. It functions like a reward function: define it well and the loop converges on value.

Pin an explicit stop condition and a bound. Use measurable passes (tests green, an exit code, a score threshold) plus a hard cap like "or stop after 5 rounds." In Claude Code, the `/goal` command sets a completion condition that a fast model checks after each turn; adding a turn or time clause prevents infinite loops.

Triggers (what wakes the agent - cron, webhook, or another agent), a file structure (artifacts, contracts, and logs the agent reads and writes), tools and connectors (skills and scripts to do real work), and an agent-ready codebase (so many agents can run in parallel and verify their own output). The fourth is the one most people skip and the one that decides whether autonomous work is even possible.

Artifacts are the shared knowledge layer - the output of each loop (docs, signals, tasks, tickets), each in its own folder with a README and schema. A contract is one README per loop stating its goal, workflow, backlog, and timeline; the loop reads it before every run. Logs are a single global work-log file the agent appends to after big tasks and reads before starting, so context survives across sessions. Signals are the unit that lets separate loops compound by reading each other's findings.

Firsthand: the workflow and the two-take landing-page example come from running real agent loops in Claude Code in mid-2026, not synthetic benchmarks - treat them as one builder's results, not guarantees. The compounding-loop system, four ingredients, and artifact/contract/log architecture are drawn from AI Jason's 'Loop Engineer: Systemization and Artifacts' video below. The nested three-loop model and the 'context advantage' framing come from Andrew Ng's June 30, 2026 Batch letter (linked below). Product behavior (the /goal command and how it evaluates a stop condition) is verified against Anthropic's official docs below. See our [editorial standards](/about).
