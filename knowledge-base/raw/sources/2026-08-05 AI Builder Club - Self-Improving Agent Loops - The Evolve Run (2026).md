---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-self-improving-agent-loops
title: 'Self-Improving Agent Loops: The Evolve Run (2026)'
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/self-improving-agent-loops
published: '2026-07-16'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Self-Improving Agent Loops: The Evolve Run (2026)

It was midnight, and PRs were still landing in our codebase. Nobody was awake.

An agent wakes every 30 minutes, scans the codebase and the server logs, and ships a PR. A verifier agent tests it and attaches evidence. Low-risk fixes merge on their own. That has been running at [Superdesign](https://github.com/superdesigndev) for about a month, alongside a CRM loop and a support triage loop, and none of it is a demo.

Here is the part I did not expect. **The single best improvement to those loops in that entire month was not written by me. It was written by the loop, about itself.**

That is what this piece is about: the **evolve loop**, the meta-loop that periodically reads a loop's own config, state, and run logs, and rewrites the loop. If you want the foundations first, start with the pillar on [loop engineering](/blog/loop-engineering-guide-2026), which covers the verifier, open versus closed loops, and the contract. This is the layer that sits on top of all of it.

Prefer to watch? Here's the full walkthrough of what that month of running loops actually taught me:

---

## What is a self-improving agent loop?

A self-improving agent loop is a loop with a second, slower loop pointed at it. The fast loop does the work. The slow loop edits the fast loop.

The important word is *edits*. Not "learns" in some vague sense. It opens files and changes them.

Concretely, an evolve run can touch four things:

| What it rewrites | Why it matters | Example from our month |
| --- | --- | --- |
| **The contract** | Vague goals and boundaries produce vague work | Sharpened the SOP, tightened what can merge without review |
| **The state** | Stale hypotheses poison every future run | Deleted backlog items shipped three weeks ago |
| **The trigger** | The wrong trigger burns tokens on empty runs | Wrote a script that only wakes the agent when work exists |
| **The SOP steps** | Anything mechanical is cheaper as code | Folded repeated steps into deterministic scripts |

Note what is missing: the model. A self-improving agent is not one that retrains its own weights. It rewrites the artifacts around the model. That is a much smaller idea than the phrase suggests, and much more useful, because in production almost all of the loss lives in those artifacts and not in the model.

## Why most self-improving agent advice stops at the prompt

I went looking for prior art before writing this, and the pattern is consistent. Nearly everyone rewrites the prompt.

OpenAI's [self-evolving agents cookbook](https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining) is the cleanest version: four graders score a summarization output, and when the average falls below threshold, a metaprompt agent rewrites the instructions and tries again, up to three times. It works. It is also prompt-only, grader-triggered, and scoped to one task.

Addy Osmani's [self-improving coding agents](https://addyosmani.com/blog/self-improving-agents/) goes further and is honest about where it stops: agents accumulate discovered patterns in `AGENTS.md` and progress logs so the next iteration inherits the context. But as he documents it, the agents **do not rewrite their own instructions or config**. A human curates. He is also blunt that "there is no one-shot fully autonomous magic."

[BerriAI's self-improving-agent](https://github.com/BerriAI/self-improving-agent) adds the safety gate everyone eventually needs: the agent calls `writeImprovementProposal` with a minimal diff, and nothing ships until a human confirms in their most recent message.

Here is the gap. All three treat the agent's *reasoning* as the thing to improve.

**After a month in production, the reasoning was almost never the problem. The scaffolding was.** The agent was not thinking badly. It was waking up 48 times a day to discover there was nothing to do, carrying a hypothesis it had disproved two weeks earlier, and re-deriving the same five steps by hand every single run. None of that is fixed by a better prompt.

## The evolve run: what we actually feed it

After every 5 to 10 loop runs, we trigger a dedicated session. It is not a normal run. It does no work on the domain task at all.

We hand it three things:

1. **The existing loop config** - the contract, goal, boundaries, SOP.
2. **The past state and logs** - what it believed, and what actually happened, run by run.
3. **The raw conversation history** - so it can inspect how runs actually went, not just what they claimed.

Then we ask it to prioritise changes.

That third input is the one people skip, and it is the one that makes this work. State and logs tell you what the agent *concluded*. The raw history shows you where it flailed for eleven turns before concluding it. The flailing is the signal. It is where the cheap fixes are hiding.

The output is not a report. It is edits to the loop's own files, plus a short note on why. On [Loopany](https://github.com/superdesigndev/loopany-platform), the open-source tool we run this on, an evolve run shows up as a blue dot in the run history so you can tell it apart from real work. Its README describes the pass exactly as we use it: "a periodic pass that rewrites the loop itself (tighter contract, cheaper trigger, mechanical steps folded into scripts), so it gets sharper and cheaper the longer it runs."

In one evolve run on our doc loop, it sharpened the spec and SOP, cleaned out stale state, and updated the dashboard so we could actually see the loop's output over time. That last one is telling. We had not noticed we were flying blind.

## What the evolve run reads: state versus log

The evolve run is only as good as what it can read, which makes the state and log split load-bearing rather than housekeeping. The [pillar](/blog/loop-engineering-guide-2026) covers contracts and logs as an architecture. Here I only care about them as *inputs to the evolve pass*.

Two files, two jobs:

- **State** is a durable picture, kept small and on purpose. The current hypothesis. The open backlog. Things shipped that need follow-up. This is what the agent believes right now.
- **Log** is append-only, run by run. What happened, in order. Nobody edits it.

Why the split matters for evolve: the log is the *evidence*, and the state is the *claim*. An evolve run's most valuable move is noticing they disagree. State says "investigating whether the flaky test is a race condition." Log says that hypothesis died nine runs ago. Nothing else in the system will ever catch that, because every normal run trusts state by default.

**Without this split, every run rediscovers the same noisy errors and burns tokens chasing dead ends already tried.** That is the compounding tax, and it is invisible until you read a month of logs at once. If you want the general version of this problem, we wrote up [agent memory systems](/blog/agent-memory-systems-guide) separately.

## The proof: a trigger script we did not write

This is the part that convinced me the mechanism is real, rather than a nice diagram.

Our support inbox triage loop handles tickets automatically, in whatever language the user writes in. Early on, its trigger was the obvious thing: wake the agent on an interval, let it check Intercom, let it decide if there is anything to do.

That is expensive. Most wake-ups found nothing. We were paying an LLM to check whether an LLM was needed.

During an evolve run, the agent read its own logs, saw the pattern, and wrote a JavaScript trigger script: fetch recent Intercom updates from the last 30 minutes, and if there is real work, wake the agent. If not, skip the run entirely.

I did not design that. I did not ask for it. **The loop noticed it was wasting my money and wrote the fix.**

This is the combo trigger pattern: a ticker on an interval, but a cheap deterministic script standing between the clock and the agent, batching real work and refusing to wake anything otherwise. It drops cost hard, because the expensive component only runs when the cheap component says there is a reason. (For the full trigger taxonomy, and where this sits next to turn, goal, time, and proactive loops, see [the 4 types of agentic loops](/blog/types-of-agentic-loops). The cost logic behind it is in [agent reliability and cost control](/blog/ai-agent-reliability-cost-control).)

The generalisable lesson is not "use programmatic triggers." It is that **the loop had information I did not have.** I never read 400 run logs. It did.

## The rule that stops a self-improving loop inventing work

Now the failure mode, because this is the one that will bite you, and it is structural rather than a bug.

Our doc-maintainer loop is small and genuinely useful. Every day it checks what shipped in the last 24 hours, diffs it against the README, the setup guide, the examples, and the runbooks, verifies which side is actually true, and opens a small PR if the docs drifted. If nothing drifted, it should end the session.

It did not end the session. It rewrote accurate documentation. Repeatedly.

The fix was one line in the contract:

> **never rewrite accurate doc to look busy**

Because the default behavior we kept seeing is that **an agent will tend to do something even when nothing needs doing.** It has been asked to maintain docs. Returning "the docs are fine" feels, to a model optimizing for a helpful-looking turn, like failing the task.

Sit with what that means for self-improvement specifically. An evolve run is an agent asked to find improvements. If it finds none, the honest output is "this loop is fine, change nothing." How often do you think it says that unprompted?

**A loop that grades itself will invent work.** This is the same bias we documented in [how to evaluate AI agents](/blog/how-to-evaluate-ai-agents), where models grading their own output skew optimistic, except it is worse here, because the evolve run is not just scoring itself, it is holding the pen. An evolve run that manufactures changes to justify its existence will happily churn a working contract into a worse one and log it as progress.

So the anti-busywork rule is not a doc-loop quirk. It belongs in the evolve contract itself. Give the loop an explicit licence to do nothing, and make "no change needed" a first-class success state rather than a silent failure. If you write only one line of this article into your own system, write that one.

## What a month of this actually changed

Four loops, running roughly a month. What the evolve passes actually produced:

| Loop | What it does | What evolve changed |
| --- | --- | --- |
| **React Doctor scan-and-fix** | Runs the react-doctor CLI daily, fixes the top critical issue, opens a PR | Tightened which fixes auto-merge versus escalate |
| **CRM lifecycle** | Segments daily active users, then auto-outreach or draft-for-approval by risk | Pruned stale segment hypotheses from state |
| **Support inbox triage** | Handles tickets in any language | Wrote the programmatic Intercom trigger |
| **Doc drift sweep** | Diffs the last 24 hours of shipped code against the docs | Added the anti-busywork rule, cleaned stale state |

The honest summary: **evolve runs made our loops cheaper and tighter. They did not make them smarter.** Not one evolve pass produced a novel capability. Every win was a removal, a narrowing, or a mechanical step turned into code.

That is not a disappointment. It is the whole return. The loops were already capable. They were bleeding on scaffolding.

The CRM loop shows why this compounds rather than plateaus. Its risk boundaries decide what an agent may send to a real human without approval. Those boundaries got sharper every time an evolve run read a month of what actually happened. That is a class of judgment you cannot write correctly on day one, because on day one you have no logs.

## Where this breaks

Four honest limits from a month of running it.

1. **Evolve runs invent work.** Covered above. Unavoidable without an explicit contract rule, and worth re-checking, because the tendency comes back.
2. **State rot beats the pass.** If nothing prunes state, it grows until it is mostly noise, and then it poisons the evolve run too. This is Osmani's context bloat, one level up.
3. **A bad evolve compounds.** A normal bad run wastes a run. A bad evolve run makes every subsequent run worse, silently. Treat evolve output as a diff to review, not a result to trust. BerriAI's human-confirmation gate is the right instinct here.
4. **It cannot fix a loop that should not exist.** No evolve pass will tell you the loop is not worth running. It was hired to improve it. That call stays yours.

Sharpen your own knives, or an agent will re-derive them every morning at 3 a.m. and bill you for it.

## Your evolve loop checklist

- Split **state** (small, durable, on purpose) from **log** (append-only, never edited)
- Schedule a dedicated evolve session every **5 to 10 runs**, not every run
- Feed it all three: **config, state and logs, raw conversation history**
- Give it explicit permission to change the **contract, the state, and the trigger**, not just the prompt
- Put **"never rewrite accurate X to look busy"** in the contract, and make "no change needed" a success
- Mark evolve runs distinctly in your run history so they are not confused with real work
- Review the first several evolve diffs by hand before letting any of it apply itself
- Look first for the **empty wake-up**, the loop's cheapest and most common waste

## FAQ

**What is a self-improving AI agent?**
An agent that uses structured feedback from its past runs to change how it behaves, without a human re-engineering it by hand. It does not retrain its own weights. It reads its own config, state, and logs, then edits the files that drive it: the contract defining done, the state carried between runs, and the scripts deciding when it wakes.

**Can an AI agent improve itself?**
Yes, within the scope you give it. It cannot change its model, but it can rewrite the scaffolding around it, and that is where most production loss lives. Our support loop's evolve run wrote a script that polls Intercom for updates in the last 30 minutes and only wakes the agent when there is real work. No human designed it. The agent read its own logs, saw it was waking up to do nothing, and fixed the cause.

**How is a self-improving loop different from a self-evolving agent?**
Most published self-evolving work rewrites the prompt, triggered by grader scores. An evolve loop has a wider blast radius: contract, stale state, triggers, and mechanical SOP steps folded into scripts. The prompt is one of four targets, and usually the least valuable one.

**How often should you run an evolve pass?**
Every 5 to 10 loop runs. More often and there is not enough log history to see a pattern, so it invents changes. Much less often and stale state has been poisoning runs for weeks. For a daily loop, that lands at roughly weekly.

**Do agent loops actually get better over time?**
Only if something reads the logs. Without an evolve pass a loop repeats rather than compounds, rediscovering the same dead ends every run. After a month, our wins were cheaper triggers, tighter contracts, and mechanical steps turned into scripts.

**What is the biggest failure mode of a self-improving loop?**
Invented work. Agents do something even when nothing needs doing, so a loop grading its own usefulness will manufacture proof it was useful. Give it an explicit licence to do nothing.

**Do I need a special tool to run this?**
No. The whole pattern is a markdown file plus a scheduler, and you can hand that markdown to Claude Code or Codex and ask it to set up the loop. We built [Loopany](https://github.com/superdesigndev/loopany-platform) because we wanted contracts, state, logs, and triggers in one place across a team, with evolve built in. It is open source and runs locally, talking to your own agent with your own credentials.

## Related Content

- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)** - The pillar. The verifier as bottleneck, open versus closed loops, and the contract this evolve pass rewrites.
- **[The 4 Types of Agentic Loops](/blog/types-of-agentic-loops)** - Turn, goal, time, and proactive. Where the combo trigger fits and which handoff you are making.
- **[Agent Memory: Why Your AI Forgets Everything](/blog/agent-memory-systems-guide)** - The general version of the state and log split.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)** - Why models grading their own homework give themselves an A, and why evolve runs need the same guard.
- **[AI Agent Reliability and Cost Control](/blog/ai-agent-reliability-cost-control)** - What empty wake-ups actually cost and the levers that stop the bleeding.
- **[Crabbox: Parallel Agent Sandboxes](/blog/crabbox-parallel-agent-sandboxes)** - Remote sandboxes so your verifier is not capped by how many dev servers your laptop can run.
- **[Claude Code Worktrees](/blog/claude-code-worktree-parallel-agents)** - File isolation for the subagents an executor spawns in parallel.

---

## Start Here

Pick your oldest loop. Open its logs, not its output, and read the last twenty runs end to end.

Count how many woke up and found nothing to do. That number is your first evolve run, and you already know what it will write.

Want to build the full system, from the verifier that earns you the right to walk away up to loops that rewrite themselves? The [**Loop Engineering course**](/courses/loop-engineering) walks the whole ladder, layer by layer, until you have loops that ship while you are away and get cheaper the longer they run.

Open source · free

AI Builder Club Skills

The evolve-loop tooling is open-source. /new-loop scaffolds a loop that can run, grade itself, and improve without you sitting on it.

[View on GitHub →](https://github.com/AI-Builder-Club/skills)

It is an agent that uses structured feedback from its own past runs to change how it behaves next time, without a human re-engineering it by hand. It is not an agent that retrains its own model weights. In practice the agent reads its own configuration, its stored state, and its run logs, then edits the files that drive it: the contract that tells it what done means, the state it carries between runs, and the scripts that decide when it wakes up.

Yes, within the scope you give it. An agent cannot change its own model, but it can rewrite the artifacts around the model, and that is where most of the loss lives anyway. In our support inbox loop, an evolve run wrote a JavaScript trigger script that polls Intercom for updates in the last 30 minutes and only wakes the agent when there is real work. No human designed that. The agent read its own logs, saw it was waking up to do nothing, and fixed the cause.

Most published self-evolving agent work rewrites one thing: the prompt. OpenAI's cookbook is the clean example, where graders score an output and a metaprompt agent rewrites the instructions when scores drop. An evolve loop has a wider blast radius. It rewrites the contract, deletes stale state, and turns repetitive SOP steps into deterministic scripts, so the loop gets both sharper and cheaper. The prompt is one of four things it can touch, and usually not the most valuable one.

We run one dedicated evolve session after every 5 to 10 loop runs. More often than that and there is not enough log history for the agent to see a pattern, so it invents changes to look useful. Much less often and stale state has already been poisoning runs for weeks. The right cadence is whatever gives the evolve run enough evidence to argue from, which for a daily loop lands at roughly weekly.

Only if something reads the logs. A loop with no evolve pass does not compound, it just repeats, and every run rediscovers the same dead ends and burns the same tokens. The compounding comes from the state and log split plus a periodic pass that acts on them. After a month, the concrete wins we can point to were cheaper triggers, shorter contracts, and mechanical steps folded into scripts, not smarter agents.

Invented work. Agents default to doing something even when nothing needs doing, so a loop that grades its own usefulness will manufacture proof that it was useful. Our doc-maintainer loop rewrote perfectly accurate documentation until we put a rule in the contract: never rewrite accurate doc to look busy. Any self-improving system needs an explicit licence to do nothing, or it will optimize for visible activity.

Firsthand: every loop, number, and failure described here comes from running agent loops in production at Superdesign for roughly one month in June and July 2026 (the React Doctor scan-and-fix loop, the CRM lifecycle loop, the support inbox triage loop, and the doc-drift loop). Treat these as one team's results, not benchmarks - we have no controlled comparison. The evolve-run pattern and the anti-busywork contract rule are our own synthesis from those runs, described in AI Jason's video below. Loopany's behavior (local execution, stored contracts/state/logs, the evolve pass) is verified against its public repository, linked below. The contrasting approaches from Addy Osmani, OpenAI's cookbook, and BerriAI were each read in full before being characterized here. See our [editorial standards](/about).
