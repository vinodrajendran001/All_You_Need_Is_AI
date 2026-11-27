---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-13-william-hu-always-on-agents
source_title: Building always-on agents
source_author: William Hu
source_url: https://claude.com/resources/articles/building-always-on-agents
tags:
  - source/summary
  - ai-agents
  - agent-architecture
  - agent-memory
  - permissions
source_ids:
  - src-2026-11-13-william-hu-always-on-agents
status: active
---

# Building Always-On Agents

## Summary

William Hu's guide on Anthropic's claude.com resources site argues that an "always-on" agent is a
description of the user experience, not of the runtime. The agent mostly sleeps. It wakes for a
brief **run**, works inside a **session** (the transcript of messages and tool calls), saves what
it learned, and goes back to sleep. Such agents are "stateful and proactive", but they run "on the
same core loop" as other agents; what differs is the surrounding architecture. Hu builds that
architecture from five primitives, each with its own durable store or service: an **event inbox**,
**timers**, **memory**, **permissions**, and an **outbox**. The value of the post is the
mechanism-level design rules for each primitive: one worker per inbox, timers that only enqueue
events, memory that holds only what cannot be looked up again, deferred tool calls that end a run
instead of blocking it, and an outbox tuned by evals. It is a first-party design guide with no
measured results for the architecture itself.

## Key claims

### Why now: better judgment and cheaper long tasks

Hu attributes the "resurgence" of always-on agents to models that are better at understanding
intent and "knowing when to check in", and to cheaper intelligence. His one number: "on one
long-horizon coding benchmark, Opus 5.5 cost **78%** less per solved task than Opus 5, compared
with **40%** less on typical workloads". The benchmark is not named in the post, which links an
Anthropic documentation page instead.

### Event inbox: every trigger becomes a row

Having each source call the agent directly fails in two ways: simultaneous events start competing
runs, and a crash can lose an event. Instead, a handler (usually an HTTP endpoint) writes each
event to a durable list (usually a database table), and a worker reads it. The inbox tracks status
and drops duplicates using the source's unique identifiers. Hu recommends **one inbox per user** to
start. Events that continue earlier work, such as a user reply, resume an existing session; others
start a new one. The rules:

- The handler acknowledges quickly; deeper checks "such as checking for prompt injection, should be
  done during the run".
- "The inbox should be the source of truth": a woken worker pulls the latest events first, so a
  replacement worker can retry after a crash.
- Only **one active worker** per inbox. A mid-run event can be pushed to the next run, folded into
  the current one, or used to interrupt and restart.
- The worker batches pending events, so several user messages in a row get one reply.

### Timers: follow-ups and schedules only enqueue events

A **follow-up** is a deadline the agent sets for itself; a **schedule** is a recurring task, such
as a daily newsletter. Timers live in their own durable store, separate from the inbox, which
"should only hold events that are ready to be worked on". A timer never starts a run. A scheduler
polls at a fixed interval, marks due follow-ups done or advances schedules to the next occurrence,
then adds an event to the inbox and wakes the worker. Teams can build that service or "use a
durable execution engine".

### Memory: hold only what cannot be looked up again

Memory gets its own store. Claude Code's auto memory and the Messages API's memory tool implement
it as a directory of files; for an always-on agent those directories should map to a database or
object store, "This way memories outlive the worker". The rule of thumb: "memory should only hold
what the agent can't look up again"; anything in another system, such as an issue tracker, is
saved as a pointer. Hu lists four memory types:

- **User instructions**, in their own file, loaded every run.
- **User notes**: one file at first, then many small files behind an index that loads every run.
- **Past messages**, so the agent does not repeat itself.
- **Task progress**, one file per ongoing task, also behind a loaded index.

The example layout loads `instructions.md`, `index.md`, and `reported.md` each run and reads
`notes/` and `progress/` on demand. Memory is written during the run. Optionally, **dreaming**
"reviews past sessions to curate memories", replacing outdated entries and finding "patterns that
only show up across many runs"; the post defers details to Anthropic's agent-memory post.

### Context: fixed overhead on every run

Every run pays the system prompt, tool definitions, and memory files, so Hu recommends keeping that
overhead lean and using prompt caching. Existing sessions also bring back their transcripts. When
a session grows too long, it can be compacted or replaced by a new one: "Both approaches lose
detail, so anything that needs to persist should be saved to memory along the way."

### Permissions: where the risk is

"Permissions are where always-on agents carry the most risk", because a run holds the user's access
and operates unattended. Three components:

- A **credential proxy** outside the agent's environment injects real credentials into outgoing
  requests; the agent never holds them.
- Claude Code's **auto mode** uses classifiers to block actions they identify as dangerous; "User
  review, however, is still necessary for the most important decisions".
- A **deferred tool call** (a Claude Code hook) ends the run and saves the session mid-call. The
  request is shown to the user, for example as an interactive card built with MCP Apps. The answer
  returns as an inbox event that resumes the session. Meanwhile the worker can take other events.

### Outbox: start quiet

A run ends by sending a message, deciding to send nothing, or deferring a call. A "send" tool is
enough for most agents. A formal outbox table plus a dispatcher is needed only to pace messages or
recover from errors. Hu recommends evals for message volume, because too many messages are noise
and too few miss things: "start quiet and then earn more of the user's attention over time".

## Why it matters

- [[Agentic Loop]]: the clearest vendor description in the vault of the sleep, run, and session
  cycle around a standard loop, including how a user reply re-enters as an event.
- [[Harness State Authority]]: names the inbox as the source of truth while giving timers, memory,
  and the outbox their own stores.
- [[Agent Memory]] and [[Continual Learning for Agents]]: four memory types, a pointer rule, and
  in-run writes with optional dreaming.
- [[Context Engineering]]: per-run overhead, caching, and the admission that compaction loses
  detail.
- [[AI Agents in Production]] and [[Agent Security and Governance]]: idempotent intake, a
  credential proxy, deferred approvals, and message-volume evals.
- [[Generative User Interface]]: approvals rendered as MCP Apps cards rather than chat text.
- [[Loop Engineering]]: timers are the trigger mechanism behind scheduled and self-scheduled loops.
- [[Anthropic]]: a first-party architecture guide for proactive agents built on its products.

## Tensions / open questions

- First-party guidance from Anthropic, written partly to help customers build on Claude products.
  No architecture in the post is measured; the only number is a model-cost comparison.
- The **78%** and **40%** figures name neither the benchmark nor the typical workloads, and the
  post gives no baseline beyond Opus 5.
- Hu says the inbox is the source of truth, yet timers, memory, and the outbox each keep separate
  durable state. How the stores stay consistent when a run crashes between writes is not covered.
- Prompt-injection checks are deferred "during the run" but are not specified.
- Dreaming is mentioned as an option without evidence that it improves an always-on agent.
- Message-volume evals are recommended but no eval design or result is given.

## Affected pages

- [[Agentic Loop]]
- [[Agent Memory]]
- [[Context Engineering]]
- [[Loop Engineering]]
- [[Harness State Authority]]
- [[Continual Learning for Agents]]
- [[AI Agents in Production]]
- [[Generative User Interface]]
- [[Anthropic]]
- [[Agent Security and Governance]]

## Raw capture

- [[knowledge-base/raw/sources/Building always-on agents]]

## Citations

- Canonical URL: https://claude.com/resources/articles/building-always-on-agents
- Byline: William Hu; the acknowledgements thank Rodrigo Olivares and Michael Segner.
- Publisher: Anthropic (claude.com resources).
- Published: 2026-11-13. Captured: 2026-11-24 (newsletter-tracked URL; tracking parameters removed).

## Related pages

- [[Agentic Loop]]
- [[Agent Memory]]
- [[Context Engineering]]
- [[Loop Engineering]]
- [[Harness State Authority]]
- [[Continual Learning for Agents]]
- [[AI Agents in Production]]
- [[Generative User Interface]]
- [[Agent Security and Governance]]
- [[Model Context Protocol]]
- [[Anthropic]]
- [[Instinct]]
- [[Bas Nijholt - I Used to Orchestrate Agents, Now I Orchestrate Orchestrators]]
- [[Frank Rousseau - Agentic Coding on an Open-Source Project]]
