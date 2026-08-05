---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-five-layers-ai-engineering
title: The 5 Layers of AI Engineering
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/five-layers-ai-engineering
published: '2026-07-20'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# The 5 Layers of AI Engineering

**AI engineering isn't one skill - it's a stack of five, and each layer engineers the system one level further out from the model: prompt, context, harness, loop, graph.** You don't pick one. You climb them, and you climb only when the model gets good enough to handle the layer below on its own.

The clearest version of this ladder showed up on X in mid-July 2026. [@sairahul1](https://x.com/sairahul1) put it plainly: "The best AI engineers don't just write prompts anymore. They engineer the entire system around the model. You can think of an AI application as five layers." It landed because it named something builders had been feeling for two years - that every few months the leverage moves *outward*, away from the words you type and toward the machinery around them.

**This is the taxonomy page.** If you want the *history* - the story of how the field actually moved from one layer to the next, and why each shift hit a ceiling that forced the following one - that lives in [From Prompts to Loops: The 4 Shifts](/blog/prompt-context-harness-evolution). What you get here instead is the clean five-layer table, a nesting diagram, and the part most people skip: a symptom-based diagnostic for figuring out which layer is your real bottleneck *today*. So the first three layers below are deliberately short - they're deeply covered elsewhere, and linked - and the weight of this page sits on layers four and five and the diagnostic.

---

## The Five Layers at a Glance

Every layer wraps the one beneath it. The model sits at the center and never changes; what changes is how much system you've built around it, and therefore what skill is scarce.

| Layer | What you engineer | Your role | The scarce skill |
| --- | --- | --- | --- |
| **Prompt** | The single request to the model | Operator | Language design - saying it so the model does it |
| **Context** | Everything the model sees at call time | Librarian | Information architecture - what to include, cut, summarize |
| **Harness** | One full run - tools, state, checks, recovery | Systems designer | Control design - keeping a long run on the rails |
| **Loop** | The run repeating without you | Loop engineer | Verifier + stop-condition design - defining "done" and "good" |
| **Graph** | Many specialized agents wired together | Orchestrator | Decomposition + routing - which node does what, and when |

Read it top to bottom and you have the shape of the last three years. Read it as a diagnostic - "which row is my problem in?" - and it earns its keep every day. The rest of this page teaches you to read it the second way.

---

## Layers 1-3, in Brief (the owned depth lives elsewhere)

The first three layers are the most mature and the most written-about, so this page states what each one *owns* and sends you to the deep-dive. The full narrative of how the field climbed through them - with the receipts - is the job of the [4 Shifts guide](/blog/prompt-context-harness-evolution).

**Layer 1: Prompt - say it better.** The single request: a role, a few examples, a step-by-step decomposition, an output-format contract, all of it shaping the probability space the answer gets drawn from. Its ceiling is quick and hard - a phrasing-perfect prompt still can't supply a fact that isn't in the window, which is exactly what pushes the leverage up to the next layer. Full story: [The 4 Shifts, Shift 1](/blog/prompt-context-harness-evolution).

**Layer 2: Context - feed it better.** Everything the model sees at call time: retrieval, ranking, progressive disclosure, and the constant editorial call of what to quote versus summarize versus cut. Context *contains* the prompt - the prompt is just one curated object in the window, which is why the layers nest instead of compete. Its ceiling is that great inputs still leave nobody watching the work happen, so a model with every fact can still come apart across a long run. Full story: [The 4 Shifts, Shift 2](/blog/prompt-context-harness-evolution).

**Layer 3: Harness - control the run.** Everything around the weights for one full execution: what the model can touch, how steps sequence, what persists, who checks the output, what happens on failure. LangChain's shorthand is the cleanest in circulation: **Agent = Model + Harness.** Its ceiling is subtle but decisive - a perfect harness still controls exactly *one run*, and you are still the trigger for every one of them. We break the harness into its six load-bearing parts - context, tools, orchestration, state, evaluation, recovery - in [Harness: The 6 Components](/blog/harness-six-components).

That trigger problem - you, personally, kicking off every run - is where the owned depth of this page begins.

---

## Layer 4: Loop Engineering - Remove Yourself From the Run

Once the harness controls a run, the next move is to make that run *repeat without you*. That's the loop: **discover → plan → execute → verify → repeat until a condition holds.** You stop issuing instructions and instead define a goal with a testable stop condition, a verifier that decides "good enough," and a trigger - cron, webhook, another agent - that fires it. Then you walk away, and the work keeps happening on a schedule you no longer have to attend.

Here's the part that trips people up: the loop and the harness are easy to blur. **The loop defines *what* the agent does and *when*; the harness defines *where* it runs, what it can touch, and how it recovers.** The loop is the choreography, the harness is the stage - and you need both.

The scarce skill at this layer isn't the prompt - a machine writes that now. It's the **verifier.** In a loop the generator runs cheaply, over and over, so the thing that decides whether all that motion produces value is the check at the end, not the model in the middle. A loop with a weak verifier doesn't fail loudly. It succeeds at producing garbage, confidently, all night, at token prices - and this is the first layer where the failure mode is measured in dollars, not just quality. That single fact is the entire argument of the flagship [Loop Engineering guide](/blog/loop-engineering-guide-2026): stop perfecting prompts, start writing verifiers.

Loops also come in shapes - open vs closed, self-verifying vs human-gated, single vs nested - and choosing the right one for the task is its own skill. We catalog them in [The Types of Agentic Loops](/blog/types-of-agentic-loops).

The ceiling of a single loop is where the taxonomy points you upward: one agent, however well-looped, is still *one specialty on repeat*. Point it at work that splits into genuinely different jobs - research, then write, then critique, each wanting a different model and different tools - and one loop starts doing all of them mediocrely. That's the pressure that pushes you to the last layer.

---

## Layer 5: Graph Engineering - Wire the Agents Together

When one loop isn't enough, you wire **multiple** specialized agents into a graph. Three parts carry it:

- **Nodes** - the specialist agents or steps (a researcher, a writer, a critic), each with its own model, tools, and job.
- **Edges** - the routing between nodes: conditional branches, fan-out to run several in parallel, fan-in to join their results, and loops back for a retry.
- **Shared state** - the object that flows along the edges, so what one node learns is available to the next.

The shift even has a stock metaphor now: agents graduating from a while-loop to an org chart, with specialized nodes running in parallel and state passing between them - the org-chart framing [@rohit4verse](https://x.com/rohit4verse) helped popularize. The cleanest way to hold the relationship in your head is that a loop is just a graph with one node looping on itself; a graph is what you get when you add more nodes and route between them.

So when do you actually climb here? The short version: **only when one loop genuinely can't hold the work** - [when the task splits into distinct specialties that a single loop can't serve well](/blog/agent-graph-vs-loop-when-to-use), which is a call worth making deliberately rather than by reflex. The longer version, with the full signal table, is a page of its own.

And be suspicious of anyone selling this layer as brand-new, because it has real prior art - the frameworks shipped before the buzzword trended:

- [**LangGraph**](https://docs.langchain.com/oss/python/langgraph/overview) builds agent workflows as graphs of states, nodes, and edges (and per its own docs, you don't need to use LangChain to use it).
- **Microsoft AutoGen** offers graph-based multi-agent orchestration; its GraphFlow feature describes a DiGraph with sequential, parallel, conditional, and looping execution - though the docs flag it as **experimental and subject to change.**
- [**Google's ADK**](https://adk.dev/) provides graph-based workflows with sequential, loop, and parallel patterns, plus A2A agent-to-agent delegation. (Its Go SDK hit a 2.0 GA in 2026; that's the SDK version, not a framework "2.0.")

[@NathanFlurry](https://x.com/NathanFlurry) makes the prior-art case pointedly - one post needling that "graph engineering" write-ups don't even mention A2A, and separately arguing that LinkedIn was already on this in 2025 and IBM is moving faster still. Whether or not you buy his timeline, the underlying point holds: the pattern predates its trending name. The full teardown - what's genuinely new versus a rebrand, and when a graph actually beats a loop - lives in the [Graph Engineering guide](/blog/graph-engineering-guide-2026).

---

## How Do the Layers Actually Nest?

Each layer wraps the last, with the model at the dead center and nothing but system built outward from it:

code

```
  ┌───────────────────────────────────────────────────────────┐
  │  GRAPH        many agents wired as nodes + edges + state    │
  │  ┌─────────────────────────────────────────────────────┐   │
  │  │  LOOP       the run repeats until a condition holds  │   │
  │  │  ┌───────────────────────────────────────────────┐  │   │
  │  │  │  HARNESS    one full run: tools · state · check│  │   │
  │  │  │  ┌─────────────────────────────────────────┐  │  │   │
  │  │  │  │  CONTEXT   what the model sees at call   │  │  │   │
  │  │  │  │  ┌───────────────────────────────────┐  │  │  │   │
  │  │  │  │  │  PROMPT    the single request     │  │  │  │   │
  │  │  │  │  │  ┌─────────────────────────────┐  │  │  │  │   │
  │  │  │  │  │  │        M O D E L            │  │  │  │  │   │
  │  │  │  │  │  └─────────────────────────────┘  │  │  │  │   │
  │  │  │  │  └───────────────────────────────────┘  │  │  │   │
  │  │  │  └─────────────────────────────────────────┘  │  │   │
  │  │  └───────────────────────────────────────────────┘  │   │
  │  └─────────────────────────────────────────────────────┘   │
  │   outward = more system, less model                         │
  └───────────────────────────────────────────────────────────┘
```

Two things to read off the diagram. First, **nothing gets obsolete.** A weak prompt still poisons the best graph ever built, because the prompt is still in there at the core. Climbing the stack adds layers; it never lets you skip one. Second, **the scarce skill migrates outward.** In 2023 it was phrasing. In 2026 it's decomposition and verification. The model - the one thing you don't engineer - sits still while everything you *do* engineer accretes around it.

---

## Which Layer Is Your Bottleneck Right Now?

This is the diagnostic the taxonomy exists for. The buzz always crowds around the top of the stack - "graph engineering is the new loop engineering!" - and tempts people to jump straight to the outermost layer. The honest move is the opposite: **work the lowest layer that's still your bottleneck.** Start from the symptom you can actually observe, not the layer that's trending.

| What you're seeing | The failing layer | The fix (not a whole-system rebuild) |
| --- | --- | --- |
| The model solved the wrong problem - it misread the ask | **Prompt** | Tighten the request: role, constraints, an output-format contract. |
| The answer reads well but is wrong, generic, or out of date | **Context** | Get the right facts into the window - retrieval, ranking, what to cut. |
| It starts right, then drifts, or claims "done" on work that doesn't run | **Harness** | Add checks, state, and recovery so one run stays on the rails. |
| It works, but only when *you* personally kick it off | **Loop** | Give it a trigger, a verifier, and a stop condition, then step away. |
| One agent is doing three different jobs, all of them mediocre | **Graph** | Split into specialist nodes with routing - only if a single loop truly can't hold it. |

The trap this table is built to prevent: reaching for a multi-agent graph while your prompts are vague and your context is thin. You add nodes and edges to a system whose real problem is two layers down, and now you have five agents confidently compounding the same bad input - more moving parts, the same root cause, five times the token bill. Find the *lowest* row that's failing, fix it there, and climb only when the layer below is genuinely solid.

The skeptics are worth listening to at exactly this point, because they're not attacking the *idea* of the stack - they're attacking the reflex to skip to the top. [@PawelHuryn](https://x.com/PawelHuryn) said it bluntly: "I call BS on graph engineering. Loop engineering was already confusing." His constructive version - give the agent the objective, why it matters, and how success is measured - is really an argument for nailing the harness and loop layers before you reach for nodes and edges. [@DavidKPiano](https://x.com/DavidKPiano), who built XState and knows state machines cold, put it flatly: "Keep this in mind before reading a slop article about 'agent graph engineering.'" Their shared point isn't "graphs are fake." It's that most builders don't need the top layer yet, and the people selling it hardest tend to skip the boring layers where your actual bottleneck lives.

So take the ladder as @sairahul1 framed it - "engineer the entire system around the model" - but climb it one rung at a time. The layer you should be working on is almost never the one trending on X. It's the lowest one that's still broken.

---

## The Five-Layer Checklist

Before you add a layer, run this from the bottom up:

1. **Name your symptom** - misunderstood, wrong, drifting, not-running, or needs-many-specialties. That names your layer.
2. **Confirm the layer below is solid.** Never engineer layer N while layer N−1 is your real bottleneck.
3. **Prompt / context:** is the ask clear and are the right facts in the window? If not, stop here.
4. **Harness:** does one full run stay on the rails - tools, state, checks, recovery? Fix this before you automate it.
5. **Loop:** is "done" defined in measurable terms, with a verifier and a stop condition? A loop without a verifier is a slop machine.
6. **Graph:** does the task genuinely split into distinct specialties that want different models, parallel execution, or auditable routing? If a single loop still holds it, don't wire a graph.
7. **Use the least system that ships the result.** Autonomy is not the goal. A shipped result is.

---

## Related Content

- **[From Prompts to Loops: The 4 Shifts](/blog/prompt-context-harness-evolution)** - The history behind this taxonomy: how the field moved through layers 1-4 and why each hit a ceiling that forced the next.
- **[Harness: The 6 Components](/blog/harness-six-components)** - Layer 3 broken into context, tools, orchestration, state, evaluation, recovery.
- **[Loop Engineering: Stop Writing Prompts, Start Writing Verifiers](/blog/loop-engineering-guide-2026)** - The flagship treatment of layer 4: open vs closed loops and why the verifier is the bottleneck.
- **[When to Use an Agent Graph vs a Loop](/blog/agent-graph-vs-loop-when-to-use)** - The full signal table for the layer-5 decision this page only points at.
- **[Graph Engineering Guide (2026)](/blog/graph-engineering-guide-2026)** - Layer 5 in full: nodes, edges, shared state, the frameworks, and when a graph actually beats a loop.

---

## Start Here

The five layers aren't a menu - they're a ladder, and the honest advice is to master each rung before you climb. Almost everyone reading about graph engineering this week has a loop that isn't solid yet, and a loop that isn't solid is a graph waiting to multiply its own mistakes.

So nail the loop before you wire the graph. The [**Loop Engineering course**](/courses/loop-engineering) takes you from "you are the for loop" to a loop that wakes on schedule, pulls the top task off your backlog, ships a PR behind quality gates, and reports back - with a copy-paste practice on your own repo every lesson. That's the fourth layer done properly, which is the one that unlocks the fifth.

Run the diagnostic, find the one layer you're actually stuck on - prompt, context, harness, loop, or graph - and bring it to people building the same thing. That's what the [Join AI Builder Club](https://www.aibuilderclub.com) is for: come get it unstuck, and ship something real.

Prompt, context, harness, loop, and graph. Each layer engineers the system one level further out from the model: the prompt shapes a single request, context controls what the model sees, the harness controls one run, the loop makes the run repeat without you, and the graph wires multiple agents together. You climb the stack as models get good enough to handle the layer below on their own.

This guide synthesizes the 'five layers' framing that surfaced on X in mid-July 2026 (notably @sairahul1's 'five layers' post, plus @svpino, @rohit4verse, and Peter Steinberger's seed question) and the documented capabilities of shipping agent frameworks (LangGraph, Microsoft AutoGen, Google ADK). It's a mental model for organizing the layers we already cover in depth at AI Builder Club - not a firsthand benchmark. Where the sibling '4 Shifts' guide tells the history of how the field moved between layers, this page is the taxonomy and the diagnostic. Framework specifics are current as of July 2026. See our [editorial standards](/about).
