---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-harness-six-components
title: The 6 Components of a Production Agent Harness
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/harness-six-components
published: '2026-06-11'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# The 6 Components of a Production Agent Harness

**Same model, same API, same price - one team's agent acts like a seasoned employee, the other's like an intern with amnesia.** The difference has a location, and it isn't the weights. LangChain's equation names it: **Agent = Model + Harness**, so Harness = everything that isn't the model. The labs set your model ceiling. The harness is entirely yours.

"Everything that isn't the model" is too vague to build from, so here's the working decomposition - six components, what each does, and the characteristic failure that appears when it's missing. The last column is the useful one: agents fail in patterns, and the pattern points at the gap.

| # | Component | Question it answers | Missing → failure looks like |
| --- | --- | --- | --- |
| 1 | Context management | What does the model see? | Inconsistent quality, forgotten constraints |
| 2 | Tool system | What can it touch? | Hallucinated facts, wrong tool, no tool |
| 3 | Orchestration | What happens next? | Half-finished pieces, no coherent whole |
| 4 | State & memory | What persists? | Every session starts from zero |
| 5 | Evaluation & observability | Was it right? | Confident garbage, undebuggable runs |
| 6 | Constraints & recovery | What if it breaks? | One bad step kills the run |

![The six harness components surrounding the model: context, tools, orchestration, state and memory, evaluation, constraints and recovery](/images/blog/harness-components-diagram.png "The six harness components surrounding the model: context, tools, orchestration, state and memory, evaluation, constraints and recovery")

---

## 1. Context Management: What the Model Sees

The most counterintuitive truth in agent work: most "dumb model" complaints are *information environment* complaints. Same intelligence, curated inputs, transformed output.

Three sub-jobs. **Boundary definition** - role, goal, success criteria. "Write an article" and "write a technical explainer for builders who know APIs but not transformers, optimizing for clarity over completeness" are different tasks; only one of them is the task you meant. **Selection and exclusion** - the senior-engineer move of handing over three relevant docs instead of forwarding the whole wiki. Relevance in, noise out, because [noise costs attention](/blog/context-engineering-guide) even when ignored. **Structure** - fixed rules, current task, run state, external evidence in stable layers, so the model never loses the constraint in the pile.

This component is deep enough to be its own discipline - the [context engineering guide](/blog/context-engineering-guide) covers rot, poisoning, and the four management strategies.

## 2. Tool System: What It Can Touch

Without tools a model only predicts text. [Tools](/blog/function-calling-how-llms-use-tools) are where prediction becomes action - and where three design questions hide:

**Which tools?** Scope to the job. A writing agent and a security-audit agent should have *disjoint* toolsets; the universal-toolbelt design is how you get the 46-tool collapse, where selection accuracy degrades just from menu length. **When to call?** Both failure directions are real: the agent that searches the web to answer "what's 2+2," and the agent that confidently invents your API's auth flow instead of reading the docs sitting in its toolset. Calibrating tool-reach is harness work - prompts, examples, and tool descriptions that draw the line. **What happens to results?** Ten raw search results dumped into context is [pollution](/blog/context-engineering-guide); the harness distills - extract the claims, keep the citations, drop the boilerplate - before the model reasons over it.

## 3. Orchestration: What Happens Next

The gap between "can do every step" and "does the whole job" is orchestration. An unorchestrated agent freestyles: does some things, in some order, stops at some point. The output is jagged - brilliant fragments, missing connective tissue, no verification pass.

Mature orchestration makes five things explicit: **step decomposition** (the task as a sequence, not a vibe), **decision points** (where the path branches and on what), **intermediate artifacts** (each step's output is the next step's input - so it gets named and stored), **termination conditions** (what "done" means, mechanically), and **escalation rules** (which failures invite a retry and which summon a human). The structure can be code (a LangGraph graph), convention (Claude Code's explore-plan-code-commit), or a [task list with dependencies](/blog/claude-code-todowrite-vs-task) - what matters is that the agent walks a track rather than wandering a field.

## 4. State and Memory: What Persists

A stateless agent is Groundhog Day with API costs - re-explaining the project every morning, re-discovering Tuesday's conclusion on Thursday. Statefulness splits into three tiers, and conflating them is the classic mistake:

- **Run state** - where am I in *this* task? Done, doing, blocked. (The [Task system's](/blog/claude-code-todowrite-vs-task) territory.)
- **Session memory** - what happened in *this* conversation that later steps need?
- **Long-term memory** - what survives across sessions? Preferences, conventions, decisions. ([Three memory types, write/maintain/retrieve lifecycle](/blog/agent-memory-systems-guide) - its own discipline.)

Tier-mixing produces both failure flavors: agents that forget the project context (under-persistence) and agents whose memory is a junk drawer of expired facts steering current work (over-persistence, no hygiene).

## 5. Evaluation and Observability: Was It Right?

The harness layer most often skipped, and the one that separates demos from production. Two halves:

**Evaluation** - because models grade their own homework generously. Anthropic measured this directly: self-evaluation skews optimistic, especially on fuzzy criteria like design quality. Their fix - a separate evaluator agent with fresh context that *actually operates the output* (clicks the UI, runs the tests) rather than admiring the code - is the [generator/evaluator pattern](/blog/harness-engineering-agent-production-guide), and the production results that followed are that article's whole story. The principle is older than AI: **production and acceptance must be different parties.** When you run agents in a loop, this evaluator *is* the [verifier that decides "good enough"](/blog/loop-engineering-guide-2026) - and it, not the model, is the bottleneck.

**Observability** - a 15-step run with 8 tool calls that produced a wrong answer is undebuggable without structured traces: which step drifted, what the tool returned, where reasoning forked wrong. Log every step's inputs, outputs, and decision; make runs replayable; alert on no-progress loops. Boring. Indispensable. The first thing you'll wish you had.

## 6. Constraints and Recovery: What If It Breaks

Demos run the happy path; production runs the other ones. Real runs hit expired tokens, malformed files, rate limits, and instructions the model creatively reinterprets. Three sub-layers hold the line:

- **Constraints** - what's off-limits regardless of model opinion: [permission boundaries](/blog/agent-modes-plan-default-auto), [deterministic hooks](/blog/claude-code-hooks-complete-guide) on dangerous patterns, [sandbox walls](/blog/agent-sandbox-os-level-security) underneath everything. Hard rails, not suggestions.
- **Validation** - pre-handoff checks: does the output answer the ask, match the format, pass the tests? Catches "confidently wrong" at the cheapest possible moment.
- **Recovery** - the difference between a stumble and a dead run: classify the error, retry transients with backoff, reroute hard failures to an alternate path, drop back to the last good state when the branch is poisoned. (One nuance from the [context guide](/blog/context-engineering-guide): keep the *evidence* of failure in context while recovering - models that see their own error stop repeating it.)

---

## Using This as a Gap Check

The six aren't a maturity ladder you climb in order - they're load-bearing walls, and your agent's weirdest behavior points at the weak one. Run the diagnostic backwards from symptoms: quality varies run-to-run with identical inputs → context. Makes things up despite having the right tool → tool calibration. Great pieces, incoherent whole → orchestration. Asks you things it knew yesterday → state. You discover failures only when users do → evaluation. One flaky API call kills forty minutes of work → recovery.

Most builders, honestly scored, are strong on tools, passable on context, and near-zero on evaluation and recovery - which is exactly why most agents demo beautifully and deploy badly. The labs keep shipping better engines. The six walls are the house, and [the teams getting production results](/blog/harness-engineering-agent-production-guide) are the ones who built all six. And if you're unsure where these six walls end and the agent's *loop* begins - the goal, the verifier, the stop condition - [the loop vs harness comparison](/blog/loop-engineering-vs-harness-engineering) draws that boundary precisely.

Open source · free

AI Builder Club Skills

The six components, packaged. /setup-codebase-harness from our open-source plugin wires them into your repo in one command.

[View on GitHub →](https://github.com/AI-Builder-Club/skills)

This guide is written from hands-on testing, then cross-checked against primary sources - official documentation and first-party announcements. Field results and opinions are labeled as such. See our [editorial standards](/about).
