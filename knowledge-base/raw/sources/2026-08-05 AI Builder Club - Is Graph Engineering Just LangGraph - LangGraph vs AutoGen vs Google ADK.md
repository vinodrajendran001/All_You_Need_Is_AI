---
type: raw-source
source_id: src-2026-08-05-aibuilderclub-is-graph-engineering-just-langgraph
title: Is Graph Engineering Just LangGraph? LangGraph vs AutoGen vs Google ADK
author: AI Builder Club
url: https://www.aibuilderclub.com/blog/is-graph-engineering-just-langgraph
published: '2026-07-20'
captured: '2026-08-05'
status: immutable
tags:
- source/raw
- ai-agents
- ai-builder-club
---

> Preserve the source body below this line as the canonical capture.

# Is Graph Engineering Just LangGraph? LangGraph vs AutoGen vs Google ADK

**Graph engineering is a pattern, not a product: you wire specialized agents into a graph of nodes, edges, and shared state. LangGraph, Microsoft AutoGen, and Google ADK are three frameworks that implement that pattern - and they all shipped before the buzzword did.** So the honest answer to "is graph engineering just LangGraph?" is no, twice over: LangGraph is one implementation among several, and the idea underneath is older than the term now trending on your timeline.

When "graph engineering" caught fire on X in mid-July 2026, the sharpest replies weren't hype - they were reminders. **@NathanFlurry** posted that it was "funny that these 'graph engineering' posts don't mention a2a," and separately that "linkedin was on this in 2025, ibm is moving faster." **@santtiagom\_** put it even more bluntly: "los graphs no son una idea nueva" - graphs are not a new idea. Both are right. If you're trying to figure out what to actually *use*, the framework you pick matters more than the label. So let's compare the real tools.

---

## The Pattern vs the Tool

First, keep two things separate.

**The pattern** is [graph engineering](/blog/graph-engineering-guide-2026): decompose a job into specialized **nodes** (a researcher, a writer, a reviewer - each an agent or a step), connect them with **edges** (the routing between nodes, including conditional branches, fan-out/fan-in, and loops), and pass **shared state** along those edges. **@rohit4verse** reached for the org-chart metaphor: agents graduating from while-loops to org charts, with specialized nodes running in parallel and state flowing between them. A single [agent loop](/blog/loop-engineering-guide-2026) is just the smallest possible graph: one node with an edge back to itself.

**The tool** is whatever library gives you nodes, edges, and state without you re-inventing them. That's where LangGraph, AutoGen, and ADK come in. The pattern is what you're thinking about; the tool is what you're typing. Confusing the two is how you end up believing a design idea belongs to one vendor.

Here's the test for whether you actually need graph engineering at all - and it's the skeptics' real point, which is correct: if your work is one well-scoped task with a clear verifier, a loop is enough, and reaching for a graph framework just adds complexity you'll pay for. Graphs earn their keep when the work splits into distinct specialties or per-step tools that a single loop can't cleanly hold - a call we work through signal by signal in [when to use a graph vs a loop](/blog/agent-graph-vs-loop-when-to-use). Assuming you've decided a graph fits, here are your options.

---

## What Is LangGraph, and Why Does Everyone Reach for It First?

LangGraph, from the LangChain team, is the framework most people mean when they say "graph." Its [own docs](https://docs.langchain.com/oss/python/langgraph/overview) describe it as "a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents."

The word doing the work there is **low-level**. LangGraph deliberately avoids hiding the graph from you. You define the state, you define the nodes, and you define the edges between them - including **conditional edges** that route execution down different paths at runtime. Building with it feels like assembling a state machine by hand, which is exactly the appeal for people who got burned by higher-level abstractions that made the easy 80% trivial and the hard 20% impossible.

Two capabilities are the reason it dominates the conversation:

- **Checkpointing and persistence.** LangGraph agents, per the docs, "persist through failures and can run for extended periods, resuming from where they left off." State is saved at each step, so a crash three hours into a run doesn't mean starting over. For anything long-running, this is the feature you didn't know you needed until you lost a run without it.
- **Human-in-the-loop.** The runtime supports "human oversight by inspecting and modifying agent state at any point." You can pause the graph, let a person edit the state, and resume - which is how you keep an auditable agent from doing something irreversible.

LangGraph is Python-first (there's also a JavaScript/TypeScript library), and while it's built by the LangChain team, the docs are explicit that you don't need to use LangChain to use LangGraph. If your mental model is "I want to define an explicit graph and own the control flow, with durable state underneath," this is the default answer - which is precisely why people mistake the pattern for this one tool.

---

## What Is Microsoft AutoGen's GraphFlow?

Microsoft's AutoGen approaches the same pattern from the multi-agent-conversation side. Its [GraphFlow feature](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/graph-flow.html) is documented as "a team that follows a `DiGraph` to control the execution flow between agents," and it "supports sequential, parallel, conditional, and looping behaviors." One caveat up front: the docs flag GraphFlow as an experimental feature whose API, behavior, and capabilities are subject to change in future releases, so treat it as a moving target rather than a settled one.

The mental shift from LangGraph is subtle but real. AutoGen started with conversational agents - agents that talk to each other to get work done. GraphFlow adds a **directed graph** on top of that so you're no longer relying on a manager agent to decide who speaks next; you define the flow explicitly. The docs walk through exactly the patterns graph engineering is about:

- **Sequential** (writer → reviewer),
- **Parallel fan-out/fan-in** (writer → two editors → final reviewer),
- **Conditional branching with loops** (a generator and reviewer cycling until a summarizer takes over).

That's the full graph vocabulary - nodes, branches, joins, and loops - expressed as a team of conversational agents. AutoGen is Python.

One honest caveat worth knowing before you build a company on it: Microsoft has been consolidating AutoGen's orchestration patterns, GraphFlow included, into a newer **Microsoft Agent Framework** under a unified "Workflow" abstraction. The GraphFlow docs are live and usable today, but if you adopt it, track where Microsoft is steering the ecosystem so you're not surprised by a migration later. Pick it if you're already thinking in terms of agents that converse and you want directed-graph control over the turn-taking.

---

## What Is Google ADK, and Where Does A2A Fit?

Google's **Agent Development Kit (ADK)** is the third serious implementation, and its pitch, straight from the [docs](https://adk.dev/), is "Build production agents, not prototypes." It's the most explicitly enterprise-and-scale of the three.

ADK ships the graph pattern as **workflow agents**: sequential, parallel, and loop. On top of that it provides **routing** to direct tasks to different agents based on conditions, which gives you **fan-out** (distribute work) and **fan-in** (consolidate results). In 2026 its Go SDK reached a **2.0 GA** milestone that the docs highlight for its graph workflows and collaborative agents - note that this "2.0" is the ADK Go SDK's version, not a framework-wide relabel. ADK is unusually broad on languages: **Python, TypeScript/JS, Go, Java, and Kotlin**.

The part that makes ADK distinct is **A2A**. The [Agent2Agent (A2A) protocol](https://a2a-protocol.org/latest/) is an open standard that lets agents built by different vendors, on different frameworks, discover each other, delegate tasks, and share results without exposing their internal memory, tools, or proprietary logic. ADK integrates it directly, with quickstarts for both exposing and consuming agent capabilities.

This is the piece the buzzword conversation kept skipping, and it's the whole substance of @NathanFlurry's jab. A2A isn't a Google-only thing anymore: Google **donated it to the Linux Foundation in June 2025**, where it's now governed by a technical steering committee that includes AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, and ServiceNow. If an edge in a graph is a handoff between two nodes inside one program, A2A is that same handoff standardized *across* systems and vendors. That's the strongest evidence that "graph engineering" describes something real - and that it isn't new.

---

## LangGraph vs AutoGen vs Google ADK: The Comparison

| Framework | Graph model | Best for | Language / ecosystem |
| --- | --- | --- | --- |
| **LangGraph** (LangChain) | You explicitly define state, nodes, and conditional edges; a low-level runtime with checkpointing, resumable state, and human-in-the-loop | Durable, long-running stateful agents where you want fine-grained control of the graph | Python-first, plus JS/TS; usable with or without LangChain |
| **AutoGen - GraphFlow** (Microsoft) | A team that follows a directed graph (`DiGraph`) to control flow between conversational agents; sequential, parallel, conditional, looping | Multi-agent teams that "converse" but need explicit, directed control over who runs when | Python; patterns being consolidated into Microsoft Agent Framework |
| **Google ADK** | Workflow agents (sequential / parallel / loop) with routing and fan-out/fan-in, plus A2A for cross-system delegation | Production, enterprise-scale, multi-language teams; standardized agent-to-agent delegation | Python, TypeScript/JS, Go, Java, Kotlin; open A2A protocol |

Read the table as three answers to the same question. All three give you nodes, edges, and shared state. They differ in *what they optimize*: LangGraph optimizes control and durability, GraphFlow optimizes conversational multi-agent teams, ADK optimizes production scale and cross-vendor interoperability. None of them owns the pattern. Each is a different opinion about how to express it.

---

## Do You Even Need a Framework?

Here's the question the framework marketing won't ask for you: what if you skip all three?

A graph is nodes, edges, and shared state. You can build that in plain code without importing anything. A dictionary that holds the state, a handful of functions that each read and write it (your nodes), and an `if/else` router that decides which function runs next (your edges) - that *is* a graph. For a three-step pipeline, hand-rolling it is often clearer than learning a framework's abstractions, and you can see exactly what happens. We work through this hand-rolled approach in [dynamic workflows with Claude Code](/blog/claude-code-dynamic-workflows), where a script orchestrates subagents directly.

So what do the frameworks actually sell you? Not the graph - you can write that yourself. They sell the boring, load-bearing infrastructure around it:

- **State management and checkpointing** - so a failure at node 7 of 10 doesn't wipe the run (LangGraph's headline feature).
- **Resumability and persistence** - long runs that survive restarts and pick up where they left off.
- **Observability** - seeing what each node received, produced, and decided, instead of `print`-debugging a tangle of functions.
- **Cross-vendor delegation** - handing work to an agent you don't own, over a standard like A2A, instead of gluing APIs together by hand.

That's the real buy/build line. Hand-roll the graph while it's small and you understand every edge. Adopt a framework when checkpointing, observability, or cross-system handoffs start costing you more to fake than to import. The mistake isn't picking the wrong framework - it's reaching for any framework before a plain-code graph has stopped being enough. This is the same discipline as [loop engineering](/blog/loop-engineering-guide-2026): use the least machinery that ships the result.

---

## How to Pick: A Short Checklist

Run your project through this before you install anything:

1. **Is this even a graph?** One task, one clear verifier → stay with a [loop](/blog/agent-graph-vs-loop-when-to-use). Distinct specialties, parallel branches, or per-step tools → yes, it's a graph.
2. **Can I hand-roll it?** If it's a few nodes and you understand every edge, write it in plain code first. Ship, then reassess.
3. **Do I need durability?** If losing a long run hurts, you need checkpointing → **LangGraph**.
4. **Am I orchestrating conversational agents?** If your agents talk to each other and you want directed-graph turn control → **AutoGen GraphFlow**.
5. **Do I need scale, many languages, or cross-vendor handoffs?** Production targets, non-Python stacks, or agents delegating across systems → **Google ADK + A2A**.
6. **Did I pick the pattern before the product?** If you chose a framework first and are now reverse-engineering the design to fit it, start over.

The label "graph engineering" will fade or stick - that's not your problem to solve. The pattern under it, and the three real frameworks that implement it, are what you build on.

---

## Related Content

- **[Graph Engineering: The 2026 Guide](/blog/graph-engineering-guide-2026)** - The pillar: what nodes, edges, and shared state actually mean, and where graph sits in the AI engineering stack.
- **[Agent Graph vs Loop: When to Use Which](/blog/agent-graph-vs-loop-when-to-use)** - The decision that comes *before* choosing a framework. Don't wire a graph you don't need.
- **[Graph Engineering vs Loop Engineering](/blog/graph-engineering-vs-loop-engineering)** - How the two disciplines relate, and why a loop is a single-node graph.
- **[Loop Engineering Guide](/blog/loop-engineering-guide-2026)** - The layer below graph engineering: designing the loop one agent runs, and writing the verifier that decides "done."
- **[Dynamic Workflows with Claude Code](/blog/claude-code-dynamic-workflows)** - Hand-roll a graph in a script and orchestrate subagents without a framework.

---

## Start Here

Graph engineering is the layer *above* loop engineering - so the honest move is to master the loop before you wire the graph. A graph of weak loops is just a more expensive way to produce slop. Nail the single agent's discover → plan → execute → verify cycle first, and the nodes you later wire together will each be worth wiring.

The [**Loop Engineering course**](/courses/loop-engineering) takes you from "you are the for loop" to an agent that runs on its own and clears a bar *you* defined - the exact building block each node in a graph has to be.

LangGraph, AutoGen, and ADK will keep shipping releases and shuffling their abstractions, so if you'd rather not track five docs sites alone, the AI Builder Club runs framework teardowns and side-by-side picks as they land - come compare notes and ship something real.

Jason's criticism in our August 2 workshop was blunt: LangGraph makes you specify every step, even though the node is now an agent rather than a function. [Watch the session](/courses/live-ai-workshops?utm_source=blog&utm_medium=article&utm_campaign=is-graph-engineering-just-langgraph).

[Join AI Builder Club](https://www.aibuilderclub.com)

No. Graph engineering is a design pattern - wiring specialized agents into a graph of nodes (agents or steps), edges (routing, branches, fan-out/fan-in, loops), and shared state that flows between them. LangGraph is one framework that implements that pattern. Microsoft AutoGen's GraphFlow and Google ADK implement it too, and the underlying idea predates all of them, as the A2A protocol's roots in enterprise multi-agent work show.

LangGraph (LangChain) is a low-level orchestration framework and runtime where you explicitly define state, nodes, and edges - it leans toward giving you fine-grained control and built-in persistence for long-running, stateful agents. AutoGen's GraphFlow is a team abstraction that follows a directed graph (DiGraph) to control execution flow between conversational agents, supporting sequential, parallel, conditional, and looping behaviors. LangGraph feels like building a state machine; GraphFlow feels like scripting a conversation between agents along a graph.

ADK (Agent Development Kit) is Google's open-source framework for building production agents. It ships workflow agents - sequential, parallel, and loop - plus routing and fan-out/fan-in, and integrates the A2A protocol for agent-to-agent delegation. Its Go SDK hit a 2.0 GA in 2026, highlighting graph workflows and collaborative agents. ADK is available in Python, TypeScript/JS, Go, Java, and Kotlin.

A2A (Agent2Agent) is an open protocol that lets agents built by different vendors and on different frameworks discover each other, delegate tasks, and share results without exposing their internal memory, tools, or logic. Google donated it to the Linux Foundation in June 2025, where it is governed by a technical steering committee including AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, and ServiceNow. It is the cross-system version of an edge in a graph.

No. A graph is just nodes, edges, and shared state, and you can hand-roll that in plain code - a dictionary of state passed between functions with an if/else router is a graph. Frameworks earn their place when you want state management and checkpointing, resumability after failures, observability into each node, and cross-vendor delegation. Reach for one when hand-rolled control flow starts costing you more than it saves.

If you want maximum control and durable, long-running stateful agents, LangGraph. If you are already building conversational multi-agent teams and want directed-graph control over who runs when, AutoGen's GraphFlow. If you are on Google Cloud, want multiple language SDKs, or need standardized agent-to-agent delegation via A2A, Google ADK. But pick the pattern first and the framework second - and only adopt one once a plain-code graph stops being enough.

This guide explains an emerging term, not a benchmark. 'Graph engineering' surfaced on X on July 18-19, 2026 (Peter Steinberger, @svpino, @rohit4verse, @sairahul1, plus skeptics @RhysSullivan, @DavidKPiano, @PawelHuryn, @NathanFlurry); the framework specifics are drawn from the official docs of LangGraph, Microsoft AutoGen (GraphFlow), and Google ADK, and the A2A protocol project, all verified July 2026 and linked below. Treat framework capabilities as of that date. See our [editorial standards](/about).
