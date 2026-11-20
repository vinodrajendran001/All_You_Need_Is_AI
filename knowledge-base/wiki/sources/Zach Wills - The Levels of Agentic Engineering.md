---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-11-wills-levels-agentic-engineering
source_title: "The levels of agentic engineering (from someone who's led the climb twice)"
source_author: "Zach Wills"
source_url: "https://zachwills.net/levels-of-agentic-engineering/"
tags:
  - source/summary
  - coding-agents
  - agent-adoption
  - software-factory
  - opinion
source_ids:
  - src-2026-11-11-wills-levels-agentic-engineering
status: active
---

# Zach Wills - The Levels of Agentic Engineering

## Summary

Zach Wills writes from experience leading two AI transformations. The first was "a 100-person R&D
team inside a 700-person company", starting last August; the second is at his current company,
where "We're not done, but we're shipping". He proposes seven levels of agentic engineering. He
deliberately frames them as answers to one question, "**What are you still doing yourself?**", not as
a ladder of tools to buy. Each level removes the next part of the loop a person still does by hand.

This is an **experience-based opinion essay**. It names tools (Claude Code, Cursor cloud agents,
Cursor BugBot, Macroscope, Linear) but reports no metrics, team outcomes, cost figures, or failure
rates. Wills dates his own advice: "Skills I wrote a year ago are now too prescriptive. Indexes I
built are mostly redundant because the models can find things themselves. I expect half the specifics
in this post to look dated by next summer."

## Key claims

### Method: ship it yourself to find the wall

Wills argues that the next level is found "by shipping, not by mandating it". He ships a **greenfield prototype**
first, which shows the bar when nothing is in the way. He then ships a **real backlog ticket** in the
existing product. "The difference between those two is the map" of where friction lives. At every
company the wall "has usually been infrastructure" (CI jobs, deploy pipelines, environments), with
**policies** as the other wall: "How many humans have to review a change? Does an automated review
count?" Architecture is easy by comparison: "if the API endpoints stay the same, the agent can rework
what's behind them."

The second transformation differed from the first. Everyone already used Claude, so basic training
was no longer where the value was. He also arrived with "less social capital and maybe more formal
authority, which doesn't buy you nearly as much."

### The seven levels

| Level | What you were still doing | What you do instead |
| --- | --- | --- |
| 1. Hand it the ticket | Writing the code | Give it outcomes, not instructions |
| 2. Make the codebase explain itself | Explaining the architecture | Leave lean pointers and short skills |
| 3. Let it prove its work | Testing every change | Decide which tests and checks matter |
| 4. Get it off your laptop | Starting every run | Let messages, alerts and tickets trigger it |
| 5. Close the loop | Checking it worked in production | Define "done" as business value |
| 6. Make it multiplayer | Running the factory alone | Let the whole team feed and improve it |
| 7. Decide what's next | Waiting on the backlog | Work out what to build |

The mechanisms behind the table:

- **Level 2, context.** Use AGENTS.md (or CLAUDE.md) only for "high-level pointers", not for things
  the agent can discover itself. Put lean files in the relevant directories, because harnesses "load
  these files progressively". Skills "tend to get too restrictive". A prescriptive skill helps an
  older or cheaper model, but "on a frontier model like Opus 5.5, you often don't need the skill at
  all, or it should be short and goal-oriented". A stronger model can plan while cheaper ones build.
- **Level 3, verification.** Give agents what an engineer has: complete log access and the ability to
  run, debug and QA the app end to end, so they can hand back "irrefutable proof". Ask for a video of
  the feature working. Chain agents in CI. A missing end-to-end test should trigger an agent to write
  it, not just fail the check. CI is "the best enforcement point you have" because every change
  passes through it, whatever people do locally. Agents "will happily generate filler unit tests that
  don't protect anything", so he pushes toward end-to-end tests.
- **Level 4, cloud.** At his last company they built their own cloud runner "because nobody had
  productized it yet". Now he uses Cursor's cloud agents and CI agents. The runner is commoditized,
  but triggers, environment and access still need design. Work can start from a channel message, an
  email, an alert, a log line, or a Linear ticket.
- **Level 5, release.** An agent watches each release and puts the work back on the board if it did
  not behave as expected in production. "'Merged to prod' and 'mission complete' are two different
  things."
- **Level 6, multiplayer.** A one-person factory becomes a shared one. Product, support and engineers
  feed it, and engineers improve loops instead of running them. Quality becomes "the system's job too"
  (end-to-end checks, QA agents, architectural reviews), whether bought or built.
- **Level 7.** With the backlog exhausted, the bottleneck moves to product.

### Where teams stall

"Every team can get to level one or two." Most stall at getting work into the cloud, running
autonomous loops, and making them multiplayer. Teams usually have "a few individual superstars" far up
the ladder. The real work is making that the norm.

## Why it matters

The vault's [[Agent Workflow Maturity]] page treats levels as evidence-gated assurance. Wills gives a
practitioner's version keyed to which human task is removed, and his "wall" (infrastructure and
review policy) is an organisational constraint that page's ladder does not name. His level 2 advice
supports the [[Context Engineering]] finding that hand-written guidance decays as models improve.
Levels 3 and 5 turn [[Loop Engineering]]'s verifier into concrete triggers: CI-spawned agents,
recorded proof, and a production release watcher that defines done as business value.

## Tensions / open questions

- **Ladder or graph?** Wills presents a sequence, while
  [[AI-Native Software Development Lifecycle]] argues adoption "is a dependency graph, not a ladder".
  His own framing (other lists "read like a ladder of tools"; his asks what people still do by hand) is closer to that view than the numbered levels suggest.
- "Developers shouldn't be writing code by hand anymore" is asserted, not supported by evidence.
- A release watcher needs a measurable definition of business value. The essay does not say how one
  is specified or who checks the watcher.
- Level 7's empty backlog is a projection. The essay does not show any team reaching it.
- Opus 5.5 needing short or no skills is one practitioner's observation, with no comparison reported.

## Affected pages

- [[Agent Workflow Maturity]]
- [[Context Engineering]]
- [[Loop Engineering]]

## Raw capture

- [[knowledge-base/raw/sources/The levels of agentic engineering (from someone who's led the climb twice)]]

## Citations

- Raw capture: Zach Wills, "The levels of agentic engineering (from someone who's led the climb
  twice)", published 2026-11-11 (source ID date), captured 2026-11-20. The canonical URL drops the
  newsletter `utm_source` parameter.
- The summary filename shortens the title. The exact title is in `source_title`.
- The essay links an earlier Wills post on where the bottleneck goes when agents write the code. It
  was not read.

## Related pages

- [[Agent Workflow Maturity]]
- [[Context Engineering]]
- [[Loop Engineering]]
- [[AI-Native Software Development Lifecycle]]
- [[Agentic Testing]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
