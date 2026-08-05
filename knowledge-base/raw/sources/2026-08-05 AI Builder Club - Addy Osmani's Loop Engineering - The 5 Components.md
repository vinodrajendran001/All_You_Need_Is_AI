---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-loop-engineering-addy-osmani
title: 'Addy Osmani''s Loop Engineering: The 5 Components'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/loop-engineering-addy-osmani
published: '2026-07-13'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Addy Osmani's Loop Engineering: The 5 Components

If you searched **"addy osmani loop engineering"**, you're probably looking for one of two things: the essay itself, or a straight answer to what it actually says and whether it changes how you should work. His essay is linked right here - [Loop Engineering: Designing loops that prompt coding agents](https://addyosmani.com/blog/loop-engineering/). This article is the second thing: what Osmani argued, the five components he says every real loop needs, the three debts he warns about, and the follow-up rule he added a month later that most summaries miss.

Osmani didn't invent the practice - he did something arguably more useful. He caught an idea moving fast through the builder community in June 2026, gave it a name, and gave it a parts list. For the discipline that grew around that name, our [loop engineering guide](/blog/loop-engineering-guide-2026) is the pillar. This piece is the Osmani-shaped door into it.

## The Essay That Named the Discipline

The timeline matters, because the phrase and the practice arrived within days of each other.

In early June 2026, Peter Steinberger (creator of OpenClaw) posted the sentence that lit the fuse: **"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."** Boris Cherny, who created Claude Code, described his own day the same way: "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

On **June 7, 2026**, Osmani published [the essay](https://addyosmani.com/blog/loop-engineering/) that turned those one-liners into a discipline, and gave it the name that stuck: *loop engineering*. O'Reilly Radar [republished it on June 22](https://www.oreilly.com/radar/loop-engineering/), which is how it reached most of the industry. We covered that naming moment in our [history of the prompt-to-loop shift](/blog/prompt-context-harness-evolution); this article is about what's actually *in* the essay.

Osmani's definition is disarmingly plain. Loop engineering means replacing yourself as the person who prompts the agent: **you build a small system that finds the work, hands it out, checks it, writes down what is done, and then decides the next thing** - and you let that system poke the agents instead of you. A loop is "a recursive goal": define a purpose, and the AI iterates until it's complete.

That's the same claim our pillar makes from the other direction - that [the leverage moved from writing prompts to writing verifiers](/blog/loop-engineering-guide-2026) - but Osmani's contribution is the bill of materials.

## The Five Components (Plus the One That Makes Them Stick)

Osmani's essay is tool-agnostic, but every component maps onto a concrete primitive you already have. Here's his parts list, with the mapping (the mapping is our synthesis, not his).

![Addy Osmani's five loop components - automations, worktrees, skills, plugins and connectors, and subagents - arranged around a central external-state element that persists progress between runs](/images/blog/osmani-loop-components-diagram.png "Addy Osmani's five loop components - automations, worktrees, skills, plugins and connectors, and subagents - arranged around a central external-state element that persists progress between runs")

**1. Automations.** Scheduled discovery and triage tasks that run on their own. This is the component Osmani is most insistent about: automations are *what make a loop an actual loop* and not just one run you did once. His reference point is OpenAI's internal use - daily issue triage, summarizing CI failures, writing commit briefings, hunting for bugs somebody introduced last week. In Claude Code terms this is Routines and scheduled agents; in our vocabulary it's [the trigger that closes the loop](/blog/loop-engineering-guide-2026) without a human pressing go.

**2. Worktrees.** Isolated parallel working directories so multiple agents can work the same repo without colliding. Git worktrees are the boring, load-bearing enabler of parallelism - we've documented the same pattern in [running parallel agents with worktrees](/blog/claude-code-worktree-parallel-agents).

**3. Skills.** Codified project knowledge in `SKILL.md` files - conventions, build steps, the context you'd otherwise re-explain every session. Osmani has walked this talk: his own [agent-skills repo](https://github.com/addyosmani/agent-skills) ships 23 production-grade engineering skills with verification gates, which we break down in our [agent skills best-practices guide](/blog/agent-skills-best-practices-guide). Skills attack what he calls *intent debt* (more on that below).

**4. Plugins and connectors.** MCP-based integrations that let the loop touch your actual tools: the issue tracker, Slack, databases, APIs. A loop that can't read the bug tracker can't find its own work; a loop that can't post a PR can't finish any.

**5. Subagents.** Separate agents for generating versus verifying, so the model doesn't grade its own homework. This is the component where Osmani's essay and our pillar converge exactly: a [generator with an independent verifier](/blog/loop-engineering-guide-2026) is the difference between a loop that ships and a loop that confidently loops on garbage. For the deeper mechanics, see [how to evaluate AI agents](/blog/how-to-evaluate-ai-agents).

**The sixth element: external state.** Models forget everything between runs, so the loop needs memory that lives outside the model - Osmani suggests markdown files or a Linear board that record what's done and what's next. Every run reads the state, does work, writes the state. It's the least glamorous component and the one that makes the other five compound instead of reset.

Notice what the list is *not*: it's not prompting technique. All five components live in the system around the model - which is why the practice needed a new name instead of being "advanced prompt engineering." If you're sorting out how this layer relates to the adjacent one, we've mapped [loop engineering vs harness engineering](/blog/loop-engineering-vs-harness-engineering) - Osmani's components span both.

## The Three Debts: What Osmani Warns Will Bite You

The second half of the essay is a warning label, and it's the part that separates it from the hype cycle around the term. Osmani names the costs in the order they'll hit you.

**Intent debt.** When context is missing, agents don't stop - they fill the gap with confident guesses. Every piece of intent you never wrote down becomes a recurring tax: the loop re-guesses it, sometimes differently, every cycle. Skills and state files are the repayment plan.

**Comprehension debt.** Loops ship code faster than you can understand it, and the gap compounds. The codebase grows; your mental model doesn't. Osmani's blunt framing: the code exists, and nobody on the team has read it.

**Cognitive surrender.** The most dangerous one, because it feels like success: you stop forming independent judgments and start accepting whatever the loop returns. The loop runs, tests are green, you press merge. Osmani's term for the end state is worth pinning above your desk.

He also flags two operational realities: **token costs** (loops consume budget very differently depending on whether you're token-rich or token-poor - a theme we quantify in [agent reliability and cost control](/blog/ai-agent-reliability-cost-control)) and **weak verification** - unattended loops make unattended mistakes, and a verifier subagent reduces but does not eliminate the human review burden.

His closing line is the thesis in one sentence: **"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."**

## Own the Outer Loop: The July Follow-Up Most Summaries Miss

A month after naming the discipline, Osmani published the piece that tells you where *you* go once the loop runs without you. [Own the Outer Loop](https://addyo.substack.com/p/own-the-outer-loop) (Elevate, **July 9, 2026**) answers the question the first essay leaves open: if agents prompt themselves now, what exactly is your job?

His answer splits the system in two:

- **The inner loop** belongs to the agent: investigate, implement, verify, repeat. This is the cycle the five components industrialize.
- **The outer loop** belongs to you, and it is not optional. It's the accountability boundary, held up by three pillars: **quality** (verification that produces evidence before anything ships), **verdict** (a human decides ship, block, or modify), and **answerability** (you can justify the decision when someone asks why).

![Osmani's two-loop model - the agent runs the inner loop of investigate, implement, verify, repeat, while the human owns the outer loop of quality, verdict, and answerability at the accountability boundary](/images/blog/osmani-outer-loop-diagram.png "Osmani's two-loop model - the agent runs the inner loop of investigate, implement, verify, repeat, while the human owns the outer loop of quality, verdict, and answerability at the accountability boundary")

The follow-up also upgrades the essay's warnings into named costs of delegation: cognitive surrender returns, joined by **cognitive debt** (your understanding erodes through over-reliance) and the **orchestration tax** (human oversight doesn't parallelize the way agents do - review is the new bottleneck). That last one is the same conclusion our pillar reaches from first principles: [the verifier is the bottleneck](/blog/loop-engineering-guide-2026), and in Osmani's frame *you* are the final verifier.

Read together, the two essays make one argument: **delegate the inner loop as aggressively as your verification allows; never delegate the outer loop.** Loop engineering without outer-loop ownership isn't leverage - it's abdication with good tooling.

The orchestration tax is also the cost that pushes teams to the next structure. Once the inner loop splits into several specialized agents running at once, you're no longer designing a cycle, you're designing a [graph engineering](/blog/graph-engineering-guide-2026) system: nodes, edges, and shared state. Osmani's outer loop doesn't go away there. It gets harder, because now you're the verifier for a whole graph rather than one loop.

## How to Build Osmani's Loop This Week

The essay is a parts list; here's a build order. Four moves, smallest first.

**1. Give the loop memory before you give it autonomy.** Start with the sixth element: a single markdown state file - `done`, `in-progress`, `next`. Have the agent read it at the start of every session and update it at the end. This costs ten minutes and immediately makes runs compound instead of reset.

**2. Codify the thing you explained twice.** The second time you re-explain a convention or a build step, it becomes a `SKILL.md`. That's intent debt being repaid at the cheapest possible moment. (Steal the structure from [Osmani's own skills repo](https://github.com/addyosmani/agent-skills) - the verification gates are the part worth copying.)

**3. Split the grader from the generator.** Before you scale anything, add the subagent that checks the work - a reviewer with its own context that sees the diff, not the generator's reasoning. Pair it with a testable done-condition and you have the [generator-verifier core](/blog/loop-engineering-guide-2026) every other component amplifies.

**4. Only then, put it on a schedule.** Automations turn your supervised loop into an actual loop - triage that runs every morning, a CI-failure summary that's waiting when you sit down. Schedule it only after steps 1-3, because an automation without state, skills, and a verifier is just a mistake generator on a timer.

At every step, keep Osmani's outer-loop rule: the loop produces evidence, *you* produce the verdict.

## FAQ

**What is Addy Osmani's loop engineering essay?**
"Loop Engineering: Designing loops that prompt coding agents," published on addyosmani.com on June 7, 2026 and republished by O'Reilly Radar on June 22. It named and structured the practice of designing systems that prompt agents - finding work, handing it out, checking it, recording progress, deciding what's next - instead of prompting them by hand.

**What are the five components of a loop, according to Osmani?**
Automations (scheduled tasks that make it a real loop), worktrees (isolated parallel working copies), skills (codified project knowledge in SKILL.md), plugins and connectors (MCP integrations to real tools), and subagents (independent verification). Plus a sixth element: external state - markdown files or a board - so progress survives between runs.

**What does "own the outer loop" mean?**
The thesis of his July 9, 2026 follow-up: agents run the inner loop (investigate, implement, verify, repeat), but humans must own the outer loop - verifying quality, issuing the ship/block verdict, and staying answerable for the result. Delegating the inner loop is leverage; delegating the outer loop is abdication.

## Related Content

- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)** - The full discipline Osmani's essay named: verifier as bottleneck, open vs closed loops, and the starting checklist.
- **[Loop Engineering vs Harness Engineering](/blog/loop-engineering-vs-harness-engineering)** - Osmani's components span two layers; here's where the seam is.
- **[The Prompt → Context → Harness → Loop Evolution](/blog/prompt-context-harness-evolution)** - The naming moment in context: Steinberger, Cherny, Osmani, and Ng inside one month.
- **[Agent Skills Best Practices](/blog/agent-skills-best-practices-guide)** - Osmani's own 23-skill repo, and how to write skills that repay intent debt.
- **[Graph Engineering: The 2026 Guide](/blog/graph-engineering-guide-2026)** - Where the orchestration tax leads: several specialized nodes with routing and shared state, not one inner loop.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)** - The subagent-verifier component in depth: generator-evaluator, eval sets, LLM-as-judge.

---

## Start Here

Osmani's essay gives you the parts list; the fastest way to internalize it is to build one loop end to end. Take one recurring task you did manually this week, write its state file, codify one skill, add a verifier subagent, and put it on a schedule - in that order.

Want the guided version? The [**Loop Engineering course**](/courses/loop-engineering) builds exactly this stack layer by layer - feedback gates, a sandbox that bounds the blast radius, scheduled automations, and the unattended loop that ships a PR behind quality gates while you're away. It's Osmani's five components, assembled in the order that keeps you the engineer and not just the person who presses go.

'Loop Engineering: Designing loops that prompt coding agents' is the essay Osmani published on addyosmani.com on June 7, 2026 (republished by O'Reilly Radar on June 22). It named and structured a practice builders were converging on: instead of prompting an agent by hand, you design a small system that finds work, hands it to agents, checks the output, records what's done, and decides what's next.

Automations (scheduled tasks that make it a loop rather than a one-off run), worktrees (isolated parallel working copies so agents don't collide), skills (codified project knowledge in SKILL.md files), plugins and connectors (MCP integrations to your real tools), and subagents (separate agents for verification so the generator doesn't grade its own work). He adds a sixth element that makes the other five stick: external state, like markdown files or a Linear board, so progress survives between runs.

It's the thesis of Osmani's July 9, 2026 follow-up: agents can run the inner loop (investigate, implement, verify, repeat), but the human must own the outer loop - the accountability boundary where you verify quality, issue the ship/block verdict, and remain answerable for the result. Delegating the inner loop is leverage; delegating the outer loop is abdication.

Osmani's positions are drawn from two primary sources linked below: his 'Loop Engineering' essay (addyosmani.com, June 7, 2026, republished by O'Reilly Radar on June 22) and his 'Own the Outer Loop' follow-up (Elevate, July 9, 2026). Quotes attributed to Peter Steinberger and Boris Cherny are as quoted in Osmani's essay. The mapping from Osmani's components to specific Claude Code primitives (Routines, worktrees, SKILL.md, MCP, subagents) is our synthesis, cross-checked against our own loop-engineering guide - Osmani's essay is tool-agnostic. See our [editorial standards](/about).
