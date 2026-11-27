---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-10-31-l1vsun-five-levels-ai-engineering
source_title: "Prompt → Context → Harness → Loop → Graph: The 5 Levels of AI Engineering"
source_author: "@L1vsun"
source_url: https://x.com/L1vsun/status/2116519560631205914
tags:
  - source/summary
  - ai-engineering
  - coding-agents
  - loop-engineering
  - graph-engineering
source_ids:
  - src-2026-10-31-l1vsun-five-levels-ai-engineering
status: active
---

# Prompt, Context, Harness, Loop, Graph - The 5 Levels of AI Engineering

## Summary

This X article by @L1vsun presents AI engineering as a five-floor ladder. Each level "answers the
same question with a bigger answer: what does the model get to work with?" The answers are a
sentence, then a window, an environment, a schedule, and finally the shape of the job, run by a
fleet. "The levels don't move. Each floor wraps the one below it," so the ladder is meant to outlast
model releases. For each level the post names what it is, its ceiling, and the move to the next
floor, ending with a "30-second test" and "5 things to build this week". The concrete mechanisms are
a Claude Code Stop hook that blocks "done" until tests pass, four brakes for scheduled loops, and a
split, fan-out, verify, merge "diamond" for graphs. The evidence is relayed rather than original. It
quotes Tobi Lütke, Andrej Karpathy, Addy Osmani, Peter Steinberger, and Boris Cherny, and cites an
OpenAI post and a Fudan and Peking University paper without links. The post has no measurements of
its own and is written in a promotional, roadmap style.

## Key claims

### Level 1, prompt engineering: "you are the loop"

The human writes, judges, and rewrites, so "the slowest part of the system is you". The tell is a
"magic phrase" such as "Think step by step." The move up: when an answer is wrong, ask "what did the
model need to SEE to get this right?"

### Level 2, context engineering: budget the window

The post relays Tobi Lütke (June 2025) preferring "context engineering" as "the art of providing
all the context for the task to be plausibly solvable by the LLM", and Andrej Karpathy's "+1" with
"the delicate art and science of filling the context window with just the right information for the
next step". It budgets the window as five items: unchanging rules (system prompt, CLAUDE.md), tools
described so the model can tell them apart, memory, retrieved material ("the 3 files that matter,
not the 300 that exist"), and the task last. The ceiling: one call at a time, assembled by hand.

### Level 3, harness engineering: "the model is the engine, the harness is the car"

A harness is the tool-result loop, tools, permissions, sandbox, memory files, event hooks, and
traces; "Put the same model inside two of them and you get two different agents." Two relayed
results:

- OpenAI's February post "Harness engineering: leveraging Codex in an agent-first world" describes a
  repository that grew to "roughly a million lines in five months" with Codex writing the code.
- An April paper from Fudan and Peking University, "Agentic Harness Engineering", has one agent edit
  another coding agent's harness and check each edit against its prediction. After ten rounds,
  Terminal-Bench 2 pass@1 went from **69.7%** to **77.0%**, beating the human-designed Codex-CLI
  harness at **71.9%**. The frozen harness used **12%** fewer tokens on SWE-bench Verified, and "the
  gains came from tools, middleware and long-term memory, not from the system prompt".

The suggested first move is a Claude Code Stop hook that runs the tests and exits with code 2 on
failure, which blocks the stop and returns the error to the model: "Now 'done' means the tests pass,
not that the model feels finished." The ceiling: "you're still the trigger".

### Level 4, loop engineering: stop being the one who prompts

The level's name and definition come from Addy Osmani's June 7 essay: "Loop engineering is
replacing yourself as the person who prompts the agent", and it "sits one floor above the harness".
The post relays Steinberger ("You shouldn't be prompting coding agents anymore") and Cherny ("I
don't prompt Claude anymore"). Osmani's anatomy is relayed as five parts plus a state store:
scheduled automations, worktrees, skills, plugins and connectors, sub-agents that split proposer
from checker, and a state file or board. Claude Code's `/loop` runs a task on an interval, or at the
model's own pace if no interval is given. A loop on a timer "can spend money all night", so four
brakes are required:

- a done check outside the model (the Stop hook);
- a budget of max runs, tokens, or dollars;
- a dry-round rule: "stop after two rounds that find nothing new";
- state written after every step, so a crash resumes.

"The loop removes the typing, not the thinking." The ceiling: a loop is "still one track".

### Level 5, graph engineering: draw the shape of the job

A node is one bounded job with clear input and output; an edge exists only where one node's output
feeds another's input. Most step-by-step agents are "graphs full of fake edges". Deleting them gives
a diamond: split the job, fan out agents in clean contexts, verify with a gate that "tries to kill
every finding", and merge only the survivors. Claude Code's dynamic workflows, "a research preview
since June", let Claude write the plan as a JavaScript script and run it with "tens to hundreds" of
subagents in one session, with routing in code. Two rules: wait for all results only where a node
needs them together (dedupe, ranking), and tier models, with a cheap model on fan-out nodes and the
strongest on verdicts and the merge.

## Why it matters

- [[Agent Workflow Maturity]]: another level ladder, this one ordered by what the model is given,
  with a self-placement test.
- [[Coding Agent Harness]] and [[Context Engineering]]: compact definitions, a window budget, and a
  Stop-hook gate as the first harness move.
- [[Loop Engineering]]: four loop brakes, including a two-round dry rule that matches the vault's
  earlier loop-until-dry example.
- [[Graph Engineering]]: the diamond pattern and the fake-edge test for Claude Code workflows.
- Proposed for [[Harness Optimization]] and [[Agentic Testing]].

## Tensions / open questions

- Secondary and promotional. The OpenAI and Fudan/Peking claims are relayed with no links, paper
  details, or baselines beyond those quoted, and neither is captured in this vault.
- "The levels don't move" is asserted, not shown. [[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]]
  reports the opposite experience: "with every new model, my workflow changes".
- The five-level stack is the same sequence as [[AI Builder Club - The 5 Layers of AI Engineering]],
  whose vault summary reads it as "a diagnostic rather than a strict history or maturity ladder"; this post
  presents them as floors to climb ("Which level are you on?"). Its loop anatomy relays the same Osmani essay as
  [[AI Builder Club - Addy Osmani's Loop Engineering - The 5 Components]], so these are not
  independent confirmations.
- The level 5 description of dynamic workflows comes from the post, not Anthropic documentation.
- The closing line asks readers to follow "@Rel1vs337", which does not match the @L1vsun byline.
- The capture came through a newsletter link; the URL was stripped of tracking parameters.

## Affected pages

- [[Agent Workflow Maturity]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Loop Engineering]]
- [[Graph Engineering]]
- [[Harness Optimization]]
- [[Agentic Testing]]

## Raw capture

- [[knowledge-base/raw/sources/Prompt → Context → Harness → Loop → Graph The 5 Levels of AI Engineering]]

## Citations

- Canonical URL: https://x.com/L1vsun/status/2116519560631205914
- Byline: @L1vsun (X article). The closing call to follow "@Rel1vs337" does not match the byline.
- Published: 2026-10-31. Captured: 2026-11-25 via a theaivalley.com newsletter link (tracking
  parameters removed).

## Related pages

- [[Agent Workflow Maturity]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Loop Engineering]]
- [[Graph Engineering]]
- [[Harness Optimization]]
- [[Agentic Testing]]
- [[AI Builder Club - The 5 Layers of AI Engineering]]
- [[AI Builder Club - Addy Osmani's Loop Engineering - The 5 Components]]
- [[@0xCodez - Graph Engineering with Claude - 14-Step Roadmap from 0 to Graph Architect]]
- [[Addy Osmani]]
- [[Andrej Karpathy]]
- [[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]]
