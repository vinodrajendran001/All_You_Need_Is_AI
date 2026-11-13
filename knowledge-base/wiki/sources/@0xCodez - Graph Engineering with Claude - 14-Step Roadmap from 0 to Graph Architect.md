---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-07-20-0xcodez-graph-engineering-roadmap
source_title: "Graph Engineering with Claude: 14-Step roadmap from 0 to graph architect (Full Course)"
source_author: "@0xCodez"
source_url: "https://x.com/0xCodez/status/2079165300625330317"
tags:
  - source/summary
  - graph-engineering
  - multi-agent
  - claude-code
source_ids:
  - src-2026-07-20-0xcodez-graph-engineering-roadmap
status: active
---

# Graph Engineering with Claude - 14-Step Roadmap from 0 to Graph Architect

## Summary

An X long-form course by [[@0xCodez]] teaches agent design as graph design using Claude Code's
**dynamic workflows**, in which "Claude writes a plain JavaScript orchestration script, then spawns a
coordinated fleet of subagents to execute it". The 14 steps define nodes as jobs and edges as data
dependencies, then cover node schemas, plain-code edges, `parallel()` fan-out and barrier fan-in, the
diamond topology, routers, verifier patterns, failure containment, convergent cycles, model tiering,
`pipeline()` versus barriers, and letting Claude draw the graph. The durable contribution is a
compact design discipline: draw an edge only where one step reads another's output, put model
judgment in nodes and plumbing in code, and make every cycle converge. It is a practitioner tutorial
with no measurements; its headline claim that coordination "costs zero model tokens" overstates what
the mechanism shows, and one success story is unsourced.

## Key claims

### Nodes are jobs, edges are data dependencies

The test for every "and then" is: "**does the next step read the last step's output?**" If not, "there
is no edge, and the wait is wasted." A linear agent is "a degenerate graph" — a single unbranching
chain whose ordering often reflects "the order you happened to type things in". Cutting arrows that
carry no data turns the chain into independent nodes feeding one node that needs them all.

### Node contracts and code edges

Each node gets a contract: an `agent()` call with a JSON schema forces validated structured output,
and "validation happens at the tool-call layer, so Claude retries on mismatch instead of handing you
free text". Edges that only reshape data are written in plain JavaScript (`flatMap` and a `Set`) —
"deterministic, instant, zero tokens. Save agents for judgment, not for plumbing."

### Fan-out, fan-in, and the diamond

`parallel()` spawns one subagent per thunk and is a **barrier**: it waits for every thunk. A thunk that
throws "resolves to null instead of rejecting the whole batch", so results are always
`.filter(Boolean)`-ed. "Concurrency is capped around your core count and the excess queues", which
the author says lets a workflow scale to "dozens or hundreds of subagents" without filling the main
context, because each subagent carries its own and only final answers return. A fan-in barrier is
justified only when a stage "genuinely needs every prior result together", such as cross-source
dedupe; `parallel → transform → parallel` with no cross-item dependency is a smell. Fan-out plus
fan-in makes the **diamond**, the "workhorse topology".

### Routers: the agent classifies, the code routes

A router node branches on a node's validated output with an ordinary `if` or `switch`. "The router's
decision can be Claude-powered (a subagent classifies), but the routing is code Claude wrote", so the
same classification takes the same path every time: "No emergent 'Claude decided to skip the audit'
surprises - because the skip would have to be written into the graph, and it isn't."

### Verifiers, containment, and isolation

Three verifier patterns sit on edges: **adversarial** (N skeptics try to refute each finding; keep it
if a majority survive), **perspective-diverse** (distinct lenses such as correctness, security, and
reproducibility), and a **judge panel** (N attempts scored by parallel judges, synthesizing from the
winner). Failures should be contained to a node, and fan-ins should tolerate missing inputs. Git
worktree isolation is "the seatbelt for the one topology that needs it" — use it "only when nodes
actually write in parallel", not as a default.

### Cycles must converge

For discovery of unknown size, **loop-until-dry** spawns finders until K consecutive rounds find
nothing new (the example stops after **2** empty rounds). The decisive detail is to dedupe "against
everything seen, not just against confirmed results"; otherwise rejected findings reappear and the
loop "pays to rediscover the same dead ends forever". Fresh findings are verified through three
lenses before they count.

### Model tiering and topology

"Every subagent Claude spawns inherits your session model unless the script overrides it", so "a big
run bills entirely at your session tier". The advice is to "Check /model before a large run" and send
repetitive fan-out nodes to a cheaper model while keeping the merge node strong. On latency, a
`parallel()` barrier waits for the slowest node, while `pipeline()` streams each item through all
stages; "**Default to pipeline()**."

### Let Claude draw the graph

Saying "workflow" makes Claude write one; `/deep-research` is described as a shipped graph (scope →
parallel search → fetch → adversarial verify → synthesize); "ultracode" plans a workflow for every
substantial task; pressing `s` saves a good run's script to `.claude/workflows/`. Six example graphs
include a per-route security sweep, a file-by-file module port, diff review routed by size, a scheduled
ecosystem scan, and discovery of unknown size.

## Why it matters

[[Graph Engineering]] previously described Claude Code graphs as model-chosen delegation. This
roadmap describes a different mechanism: the graph is code Claude writes and then follows, which moves
routing from conversation to script. It sharpens [[Agent Planning]] by treating a plan as an
executable dependency graph and gives [[Loop Engineering]] a convergence rule for open-ended cycles.
Its tiering advice is proposed for [[Model Routing]].

## Tensions / open questions

- **"Zero tokens" is overstated.** Code edges spend no tokens to execute, but Claude spends tokens to
  write the script and every node is a model call; the course reports no token or cost totals.
- **Model-chosen vs code-chosen routing.**
  [[AI Builder Club - Graph Engineering with Claude Code - Anthropic's Agent Graph]] treats the main
  agent's delegation decisions as edges and notes that Claude Code's routing "is not equivalent to a
  declared graph runtime with durable checkpointing". This course shows routing as written code, which
  answers the determinism half; checkpointing and resume after a crash remain undescribed.
- The Bun runtime port "with adversarial code review baked into the loop" is given without a link or
  numbers; "**9/10** notice" that half of a chain's steps need not wait is rhetorical.
- No measurement of speedup, accuracy, or cost for any example graph; concurrency limits are stated
  loosely ("around your core count").
- Feature names (dynamic workflows, ultracode, `/deep-research`, `.claude/workflows/`) are taken from
  the post, not from Anthropic documentation in the capture.
- The post is promotional (it advertises the author's Substack), and its body contains no date; the
  publication date comes from the capture's frontmatter. It says "edges are free", which holds for
  execution only.

## Affected pages

- [[Graph Engineering]]
- [[Agent Planning]]
- [[Loop Engineering]]
- [[@0xCodez]]
- [[Model Routing]]

## Raw capture

- [[knowledge-base/raw/sources/Graph Engineering with Claude 14-Step roadmap from 0 to graph architect (Full Course)]]

## Citations

- Canonical URL: <https://x.com/0xCodez/status/2079165300625330317>
- By @0xCodez on X, published July 20, 2026; captured November 11, 2026 via a newsletter link (tracking
  parameters removed). The capture's filename drops the title's colon.

## Related pages

- [[@0xCodez]]
- [[@0xCodez - Build a Self-Improving Agent System with Fable 5 in 14 Steps]]
- [[AI Builder Club - Graph Engineering with Claude Code - Anthropic's Agent Graph]]
- [[Graph Engineering]]
- [[Agent Planning]]
- [[Loop Engineering]]
- [[Model Routing]]
- [[Agent Delegation]]
- [[LLM-as-a-Judge]]
- [[Agentic Loop]]
- [[Coding Agent Harness]]
