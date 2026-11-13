---
type: concept
created: 2026-08-26
updated: 2026-11-13
tags:
  - concept
  - ai-agents
  - tool-use
  - agent-harness
  - code-execution
source_ids:
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
  - src-2026-08-24-openai-builders-guide-gpt-5-6
  - src-2026-10-29-factory-droid-frontier-harness
  - src-2026-11-01-philipp-schmid-code-mode
status: active
---

# Programmatic Tool Calling

## Definition

**Programmatic tool calling (PTC)** makes executable code the agent's action space. Instead of emitting a JSON object naming one tool and its arguments, the model writes a program — typically Python in a REPL — and the available tools are ordinary functions callable from inside it. The strong form of the position, argued by [[Alex L. Zhang - Speculative Programmatic Tool Calling]], is that **code in a REPL is the only tool a system needs, and every other tool should be a function in that code.**

## Why it matters

The action space is not an implementation detail; it decides what the agent can express in one turn and what the runtime can optimize.

JSON tool calling is a request-response protocol: one call, one result, back to the model. Anything compositional — loop over these chunks, run these three in parallel, filter then aggregate — costs one full model turn per step, with the entire intermediate result passing back through context. PTC collapses that into a single generation. Control flow, data reduction, and fan-out all happen in the interpreter, and only the answer returns.

This has three consequences that the vault's earlier tool-use material does not capture:

- **Context economy.** A program that processes a large intermediate result can return a summary of it. Under JSON tool calling that result must traverse the context window to be acted on. This is the same pressure [[Context Engineering]] describes, addressed at the protocol layer.
- **Composition without orchestration.** Fan-out over sub-agents is a list comprehension rather than a graph the harness author had to build in advance. Compare [[Graph Engineering]] and [[Loop Engineering]], which solve the same problem by structuring the harness instead of the action.
- **An optimization surface.** Because the action is a program with a parseable structure, the runtime can reason about it — see [[Speculative Tool Execution]], where a harness starts running calls it finds in code the model is still writing. JSON tool calling offers almost nothing to optimize: by the time the call is fully specified, generation is nearly over.

## What it costs

PTC trades a constrained action space for an unconstrained one, and the constraint was doing security work.

A JSON tool call is a bounded request against a known schema; a program is arbitrary code the model wrote. Sandboxing becomes load-bearing rather than defensive-in-depth, and the blast radius of a successful prompt injection widens from "call one tool with bad arguments" to "execute anything the interpreter can reach." [[Agent Security and Governance]] applies directly, and the capability-budget framing there is arguably more necessary here than anywhere else.

Purity also becomes a first-class concern. Once a runtime wants to analyse, reorder, or pre-run parts of a program, it needs to know which functions have side effects — a question JSON tool calling never had to ask because it never ran anything twice or early.

## Relationship to the vault's existing tool material

[[Tool Use and Function Calling]] describes the JSON-era contract: schemas, argument validation, and the round-trip. [[Model Context Protocol]] standardizes how tools are *published* and is orthogonal — MCP servers can be exposed as functions inside a PTC namespace just as easily as as JSON tools. Vendor guidance in [[OpenAI - The Builder's Guide to GPT-5.6]] treats programmatic tool calling as a selectable mode, which is the commercial signal that this is no longer a research preference.

## A production default, with a measured replay and a long tail

[[Factory Research - Droid 1.0 - Building a Frontier Harness]] is the vault's first account of PTC
shipped as the **default** action mode of a multi-model coding harness. [[Factory AI]]'s Script tool
runs model-written JavaScript in a sandbox with no file, network, or system access of its own; the
harness's tools are callable from inside it, printed output is capped, full results are logged where
the model can search them later, and independent calls run concurrently. It answers this page's
language question for one product (JavaScript, not Python) and sits beside, rather than replacing,
direct tool calls.

The evidence comes in three grades, and they should not be merged:

- **Measured replay.** One common session — fixing a failing unit test on GPT-6.1 Sol — replayed both
  ways made the same **15** tool calls in **10** model calls directly and **5** with Script. Model
  time fell from **42.3 s** to **28.0 s** and the task from **56.8 s** to **41.6 s**. Tool durations
  were measured; the direct run's call placement was reconstructed.
- **Reported aggregate.** Script mode cuts Droid's cost by **15%** on Claude Opus 5.5, with the
  savings concentrated in the **12.5%** of Scripts that make six or more tool calls. The method behind
  the 15% is not stated. Most Scripts are small, so the benefit is a long-tail effect rather than a
  per-call one.
- **Modeled examples.** For a CI sweep over **5,384** jobs, the Script made **550** calls in **2**
  requests where direct calling would take an estimated **59 to 187**, and under **0.1%** of tool
  results reached the model's context. The direct-call side is an estimate.

Two findings bear on this page's open questions. First, on the capability bar: Factory says frontier
models "already get the most out of" PTC because stronger models plan further ahead and write more
complex Scripts, and Script is on by default for ten named models while Factory's automation tracks
more than **20**. That is consistent with PTC being a frontier-model pattern, though the post
reports nothing for models left off the list. Second, **getting models to use the mode is itself a
tuning problem**: on four models, reaching the goal that models choose Script when both modes are
available took changes to the prompt, to the descriptions of tools called inside Script, and to
Script's result format, and no single change worked on every model. The design rules that mattered —
whole files and typed results inside programs, raw blocks for literal text, short edit results, a
**5**-minute wait before returning partial output, and a dedicated tool instead of polling — are
harness engineering around the action space, not properties of code-as-action itself.

The security cost this page describes is not discussed. The sandbox's lack of direct file or network
access does not bound what the tools called inside it can do, and the post says nothing about how a
program is approved before it runs. The reliability claim — loops in code cannot "be lazy and drop a
case" — also only holds if the model wrote the loop correctly.

## One tool on the model surface: Code Mode

[[Philipp Schmid - Why Agents Are Soon Only Going to Have 1 Tool]] restates this page's strong form as
a convergence claim: harnesses are collapsing their catalog into a single `exec(code)` tool, which he
calls **Code Mode (or Programmatic Tool Calling)**. His framing adds a history this page lacked. Tool
search and progressive disclosure solved catalog size, but left standard calling at "*one* action per
turn"; Code Mode targets the round trip that remains. He names three enablers — models "trained
heavily on code", providers "post-training models for Code Mode", and MCP servers that ship an
`outputSchema`, so a script can chain Tool A into Tool B before seeing runtime output — none of which
the essay measures.

The essay makes the host side concrete. Tool schemas are compiled into compact TypeScript declarations
rather than "80 separate JSON Schema tool objects"; a large catalog can stay behind tool search or an
`ALL_TOOLS` map inside the sandbox; and explicit helpers decide what returns: `text()`, `image()`, and
`audio()`, with "only what is passed here" entering the context, and `store()` / `load()` for state
outside it. That turns Factory's capped printed output into a declared return channel, and adds
multimodal results, which a shell cannot return.

It also gives a partial answer to the approval question below. Every `await tools.*` call crosses a
bridge where the host "can inject OAuth tokens outside the sandbox, validate schemas, or pause for user
confirmation on destructive calls". Approval can therefore attach to individual calls inside a running
program without approving the whole program up front — though a paused script holds partial side
effects, and the essay does not say how destructive calls are identified. On language, Schmid prefers
JavaScript or Python to `bash`: typed calls with `Promise.all` and `try`/`catch`, and no "CLI
exploration tax" of `--help` probing. That is an experience-based argument, not a comparison.

The essay's evidence for adoption needs a correction. It says "Factory switched Droid 1.0 to Code Mode,
improving their Terminal-Bench 4 accuracy by +3.5 points and cutting model spend by 15%." In
[[Factory Research - Droid 1.0 - Building a Frontier Harness]], **3.5** points is Droid's margin over
Codex on GPT-6.1 Sol in a whole-harness comparison, and **15%** is Script mode's reported cost saving
on Claude Opus 5.5, graded above as a reported aggregate. Neither isolates a switch to code-as-action,
so the vault keeps Factory's own figures and grading. Schmid
closes with "Not necessarily" to his title: tools, CLIs, and Agent Skills built for `bash` and
human-readable text may need rework before they fit a typed code surface.

## Open questions

- Where is the boundary? Some tools genuinely want a constrained schema — irreversible actions, anything with an approval gate. Does PTC mean *all* tools become functions, or that a code tool sits alongside a small set of governed JSON tools?
- How should approval work when the unit of action is a program? Approving a program is approving everything it might do; approving each call inside it forfeits the composition benefit.
- Does PTC shift the model-capability bar? Writing correct multi-step programs is harder than filling a schema, which may make it a frontier-model-only pattern and worsen the tiering asymmetry described in [[Reasoning Trace Privacy]].
- Language choice is unsettled — current implementations span Python, bash, and Bun, with no evidence about which suits which harness. Schmid's case for JavaScript or Python over `bash` is qualitative.
- If most Scripts are small and the savings sit in the **12.5%** that make six or more calls, should a harness
  steer models toward Script only when a step is predicted to fan out, rather than by default?

## Related pages

- [[Philipp Schmid - Why Agents Are Soon Only Going to Have 1 Tool]]
- [[Philipp Schmid]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[Factory AI]]
- [[Tool Roster Economics]]
- [[Alex L. Zhang - Speculative Programmatic Tool Calling]]
- [[Speculative Tool Execution]]
- [[Tool Use and Function Calling]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
- [[Context Engineering]]
- [[Model Context Protocol]]
- [[Loop Engineering]]
- [[Graph Engineering]]
- [[Agent Planning]]
