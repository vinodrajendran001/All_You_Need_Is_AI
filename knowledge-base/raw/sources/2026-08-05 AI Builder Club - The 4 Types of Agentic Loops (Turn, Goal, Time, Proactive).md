---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-types-of-agentic-loops
title: The 4 Types of Agentic Loops (Turn, Goal, Time, Proactive)
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/types-of-agentic-loops
published: '2026-07-10'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# The 4 Types of Agentic Loops (Turn, Goal, Time, Proactive)

Ask a builder to "put the agent in a loop" and they'll usually reach for one thing, a `while` loop in a script or a `/loop` command, as if there were only one kind. There isn't. An agentic loop is defined by **which part of the cycle you hand off**, and there are four distinct handoffs. Get the type wrong and you either babysit an agent that could run itself, or unleash one that should have stayed on a leash.

If you're searching for the **types of agentic loops**, you're really asking a design question: *how much of the loop am I ready to give away, and what will stop it when I do?* This is the operational layer of [loop engineering](/blog/loop-engineering-guide-2026). The pillar covers *why* the loop (not the prompt) is the unit of work; this piece is the field guide to the four loop patterns you'll actually build, using primitives that already ship in tools like Claude Code.

## The one question that sorts every loop

Every loop does the same three things forever: something **starts** a turn, the agent **works**, and something **stops** it (or starts the next one). The four types differ only in which of those you delegate:

- **Turn-based**: you hand off *tool approval within a turn*.
- **Goal-based**: you hand off *the stop condition*.
- **Time-based**: you hand off *the trigger*, to a clock.
- **Proactive**: you hand off *the trigger*, to a schedule or an event, with no session open at all.

That's the whole taxonomy. Read left to right, each type hands off strictly more of the loop than the one before it, which is why they form a ladder rather than a menu. Here's each rung.

![The four types of agentic loops arranged as a ladder. Turn-based hands off tool approval, goal-based hands off the stop condition, time-based hands off the trigger to a clock, proactive hands off the trigger to a schedule or event. The verifier is marked as the gate between rungs](/images/blog/agentic-loop-types-diagram.png "The four types of agentic loops arranged as a ladder. Turn-based hands off tool approval, goal-based hands off the stop condition, time-based hands off the trigger to a clock, proactive hands off the trigger to a schedule or event. The verifier is marked as the gate between rungs")

## Type 1: Turn-based (hand off the approval)

The smallest handoff. In a turn-based loop you're still starting every turn by prompting, but you've stopped approving each individual tool call inside it. In Claude Code this is [Auto mode](/blog/agent-modes-plan-default-auto): it approves tool calls within a single turn so the agent can read, edit, and run without stopping to ask, but it *doesn't start a new turn on its own*. Per Anthropic's docs, the agent simply "stops when it judges the work done."

That last clause is the catch. A turn-based loop's stop condition is the model's own judgment, which is the weakest verifier there is. It's perfect for interactive work, since you're right there and you'll catch a wrong turn, but it's exactly the setup that produces a **doom loop** the moment you look away, because nothing outside the model's head decides when to quit. Turn-based is where you *start*; it's not where you leave the agent alone.

## Type 2: Goal-based (hand off the stop condition)

This is the pivotal rung, because it's the first one where the loop can close **without you**. A goal-based loop keeps starting new turns automatically and stops when an *external check* confirms you're done.

Claude Code's `/goal` command is the clean example. You set a completion condition, and, straight from the [official docs](https://code.claude.com/docs/en/goal), "after each turn, a small fast model checks whether the condition holds. If not, Claude starts another turn instead of returning control to you. The goal clears automatically once the condition is met." The evaluator defaults to Haiku and returns a yes/no plus a short reason that guides the next turn. Under the hood it's a session-scoped Stop hook: a fresh model, not the one doing the work, decides when to stop.

The entire quality of a goal-based loop lives in how you write that condition, because the condition *is* the verifier, and in loop engineering [the verifier is the bottleneck](/blog/loop-engineering-guide-2026). A good one, per the docs, has three parts:

1. **One measurable end state**: a test result, a build exit code, a file count, an empty queue.
2. **A stated check**: how the agent should prove it: `npm test exits 0`, `git status is clean`.
3. **Constraints that matter**: what must not change on the way there ("no other test file is modified").

There's a critical subtlety: the evaluator judges only what the agent has **surfaced in the conversation**. It doesn't run commands or read files itself. So "all tests pass" only works because the agent runs the tests and the result lands in the transcript. And you bound the whole thing with a clause like `or stop after 20 turns`, so a loop that can't reach its goal fails safe instead of burning your budget. This is the open-loop-to-closed-loop graduation from the [Karpathy generation-verification loop](/blog/loop-engineering-karpathy): you earn the right to walk away by making the check trustworthy first.

## Type 3: Time-based (hand off the trigger to a clock)

Goal-based loops react to *the agent's own output*. Time-based loops react to *the outside world*: a deploy that's still building, a PR collecting CI results, a queue filling up. You don't want to start each turn when the last finished; you want to start it when a clock says so.

Claude Code's `/loop` skill is the primitive here. `/loop 5m check whether the deploy finished` re-runs that prompt every five minutes. Omit the interval, as in `/loop check whether CI passed and address any review comments`, and per the [scheduled-tasks docs](https://code.claude.com/docs/en/scheduled-tasks), the agent *chooses* the interval each iteration: short waits while a build is active, longer waits when things go quiet. A bare `/loop` runs a built-in maintenance prompt (or your own `loop.md`).

The trade-off that defines this rung: `/loop` is **session-scoped**. It only fires while the session is open and idle, it's restored on `--resume`, and it expires after seven days. That's a feature for polling, since it's cheap and it inherits your session's permissions and tools, but it's a ceiling. A time-based loop still needs you (or at least your open terminal) in the picture. To cross that ceiling, you hand off the trigger one more time.

## Type 4: Proactive (hand off the trigger to a schedule or event)

The top rung. A proactive loop runs on its own schedule or reacts to events, **with no session open and no machine required**. This is the tier the community means by "proactive agents," and it's where an agent stops being a tool you drive and becomes a teammate that shows up.

Claude Code exposes three flavors, and the differences matter:

- **Routines** run on Anthropic-managed infrastructure. No open session, no machine on, autonomous, but a *fresh clone each run*, so no access to your local files, and a minimum interval of one hour. This is the rung for "run reliably whether or not my laptop is awake."
- **Desktop scheduled tasks** run locally on your machine, down to a one-minute interval, *with* access to local files and tools. This is the choice when the work needs your actual repo and secrets.
- **Event channels** flip the model entirely: instead of polling on a clock, your CI pushes a failure straight into the agent's context the moment it happens. Proactive doesn't have to mean scheduled. It can mean *event-driven*.

The docs frame the canonical use cases plainly: nightly tests, morning triage, an unattended agent that "wakes on schedule, pulls the top task off your backlog, ships a PR behind quality gates, and reports back." That last sentence is the whole point of proactive loops, and it only works if the rungs below it are solid.

## The failure mode that connects all four: the doom loop

Here's what ties the ladder together. The higher you climb, the more of the loop you've handed off, and the *less* a human is watching when something goes wrong. Hand off the trigger and the stop condition without a real verifier, and you don't get a productive agent; you get one **doom-looping**: retrying the same broken approach, [burning budget producing confident garbage](/blog/ai-agent-reliability-cost-control) at 3 a.m. while you sleep.

The community keeps building tools to "stop your AI coding assistant from doom-looping," but the root fix isn't a tool. It's a design rule that's identical at every rung: **the loop's stop condition must be a verifier the agent has to satisfy, not a vibe it's allowed to declare.** A measurable end state. A hard turn cap. A check that lives *outside* the model's own judgment. That's the same verifier the goal-based rung is built around, which is why goal-based is the rung you have to get right *before* you automate the trigger above it. Skipping it is how a proactive loop becomes an expensive way to generate noise.

## How to climb the ladder

The four types aren't alternatives to pick between. They're a progression, and the safe way to build is to climb one rung at a time, earning each handoff:

1. **Start turn-based, supervised.** Run the task in Auto mode with you watching. Learn where it goes wrong.
2. **Write the verifier and go goal-based.** Turn "make the auth flow better" into "the login test passes and no existing test breaks." Now the loop can close without you, and you can watch the evaluator catch the failures *you* would have caught.
3. **Put it on a clock if the world drives it.** Once the check is trustworthy and the trigger is external (a deploy, a PR), move to `/loop`.
4. **Hand off the trigger for real.** When it's proven out, promote it to a Routine or scheduled task so it runs whether or not you're there.

Every promotion up the ladder is one the verifier has to earn, the same rule as the [autonomy slider](/blog/loop-engineering-karpathy): you slide toward autonomy only as far as your ability to verify allows. This is the [open loop vs closed loop](/blog/loop-engineering-guide-2026) decision made concrete, rung by rung.

The ladder runs out at the top. All four types are still *one* loop with one trigger, so when a job needs several specialized steps running in parallel and routing between each other, climbing higher doesn't help. That's a different axis, and it's the one [graph engineering](/blog/graph-engineering-guide-2026) covers: nodes, edges, and shared state instead of a single cycle. Each node still sits on this ladder, so pick its type the same way.

![The automation ladder as a staircase from supervised turn-based work up to unattended proactive loops, with a verifier gate you must pass to climb each step and a warning that skipping a rung produces a doom loop](/images/blog/automation-ladder-diagram.png "The automation ladder as a staircase from supervised turn-based work up to unattended proactive loops, with a verifier gate you must pass to climb each step and a warning that skipping a rung produces a doom loop")

## FAQ

**What are the four types of agentic loops?**
Four ways to hand off part of the agent's cycle. Turn-based hands off tool approval within a single turn (Auto mode). Goal-based hands off the stop condition to an evaluator that checks a completion condition after every turn (`/goal`). Time-based hands off the trigger to a clock so the prompt re-runs on an interval (`/loop`). Proactive hands off the trigger to a schedule or event so work runs with no session open (Routines, scheduled tasks, channels). Each hands off more of the loop than the last.

**What's the difference between a goal-based and a time-based agent loop?**
A goal-based loop starts the next turn the moment the last finishes and stops when a model confirms your condition is met. It is driven by a verifier. A time-based loop starts the next turn when an interval elapses and runs until you stop it. It is driven by a clock. Use goal-based for a checkable end state; use time-based to poll something that changes on its own, like a deploy or a PR.

**How do you stop an AI agent from doom-looping?**
Give the loop a verifier it must satisfy to stop: a measurable end state (a passing test, a clean build, an empty queue) instead of a vague instruction, plus a hard bound like "or stop after 20 turns" so a bad run can't spin forever. The stop condition has to live outside the model's own judgment.

**Which loop type should I use to run an agent overnight?**
A proactive loop, either a Routine or a scheduled task, because it runs with no session open and (for cloud Routines) no machine on. But only promote a task to that rung after it works as a goal-based loop with a trustworthy verifier; automating the trigger before the stop condition is solid is exactly how overnight runs go wrong.

## Related Content

- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)**: The pillar discipline: the verifier as bottleneck, open vs closed loops, and the starting checklist every loop type sits inside.
- **[Loop Engineering, Karpathy-Style](/blog/loop-engineering-karpathy)**: The autonomy slider that governs how far up this ladder you're allowed to climb.
- **[How to Evaluate AI Agents](/blog/how-to-evaluate-ai-agents)**: How to build the verifier a goal-based loop depends on: generator-evaluator, eval sets, LLM-as-judge.
- **[AI Agent Reliability and Cost Control](/blog/ai-agent-reliability-cost-control)**: What a doom loop actually costs, and the levers that stop an unattended loop burning budget.
- **[Loop Engineering vs Harness Engineering](/blog/loop-engineering-vs-harness-engineering)**: The loop is the choreography; the harness is the stage that lets these loop types run at all.
- **[Graph Engineering: The 2026 Guide](/blog/graph-engineering-guide-2026)** - The axis this ladder doesn't cover: several specialized nodes with routing and shared state, instead of one loop.

---

## Start Here

Take one task you currently babysit and find its rung. Can you write a one-line completion condition a fresh model could check from the transcript? If yes, you're ready for a goal-based loop today. Set that condition, bound it with a turn cap, and watch it close by itself. If no, that missing verifier is the only thing standing between you and an agent that runs while you're away.

Not sure how to write that condition? The [AI Agent Loop Builder](/tools/agent-loop-builder) gives you a starting kit for your task type in seconds. Pick your task and you get a verifier checklist, a stop condition with a round cap, a budget cap, and doom-loop tripwires you can paste straight into your loop prompt.

Want to build the full ladder end to end? The [**Loop Engineering course**](/courses/loop-engineering) walks you up it layer by layer: feedback gates that earn the right to walk away, a sandbox that bounds the blast radius, the unattended loop, an issue backlog that doubles as the agent's memory, and the scheduled automation ladder. By the end you have a proactive loop that wakes on schedule, ships a PR behind quality gates, and reports back. It's these four loop types, engineered into one system that ships while you're away.

Open source · free

AI Builder Club Skills

The loop tooling for all four types is open-source. /new-loop scaffolds one with a verifier and a stop condition, ready to run.

[View on GitHub →](https://github.com/AI-Builder-Club/skills)

They're four ways to hand off part of the agent's cycle. Turn-based hands off tool approval within a single turn (Auto mode). Goal-based hands off the stop condition to an evaluator that checks a completion condition after every turn (the /goal command). Time-based hands off the trigger to a clock so the prompt re-runs on an interval (the /loop skill). Proactive hands off the trigger to a schedule or event so work runs independent of any open session (Routines, scheduled tasks, event channels). Each hands off more of the loop than the last.

A goal-based loop starts the next turn the moment the last one finishes and stops when a model confirms your completion condition is met. It is driven by a verifier. A time-based loop starts the next turn when an interval elapses and keeps going until you stop it or the work is done. It is driven by a clock. Use goal-based when you have a checkable end state; use time-based when you're polling something that changes on its own, like a deploy or a PR.

A doom loop happens when an agent keeps working without a real stop condition, so it burns budget producing confident, wrong output. The fix is the same across every loop type: give the loop a verifier it must satisfy to stop. That means a measurable end state (a passing test, a clean build, an empty queue) rather than a vague instruction, plus a hard bound like 'or stop after 20 turns' so a bad run can't spin forever.

The four-type taxonomy here is our synthesis: it organizes Claude Code's documented agent primitives (Auto mode, the /goal command, the /loop scheduled skill, and Routines / scheduled tasks) by which part of the loop you hand off. The builder community began converging on a turn / goal / time / proactive split in mid-2026; we've mapped that split onto the primitives and verified every product behavior described (evaluator model, completion conditions, intervals, scheduling scope) against Anthropic's official Claude Code documentation linked below. The decision framework and the doom-loop framing are drawn from our own loop-engineering guide, not benchmarks. See our [editorial standards](/about).
