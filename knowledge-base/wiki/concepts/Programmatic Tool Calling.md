---
type: concept
created: 2026-08-26
updated: 2026-08-26
tags:
  - concept
  - ai-agents
  - tool-use
  - agent-harness
  - code-execution
source_ids:
  - src-2026-08-26-alex-zhang-speculative-programmatic-tool-calling
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

## Open questions

- Where is the boundary? Some tools genuinely want a constrained schema — irreversible actions, anything with an approval gate. Does PTC mean *all* tools become functions, or that a code tool sits alongside a small set of governed JSON tools?
- How should approval work when the unit of action is a program? Approving a program is approving everything it might do; approving each call inside it forfeits the composition benefit.
- Does PTC shift the model-capability bar? Writing correct multi-step programs is harder than filling a schema, which may make it a frontier-model-only pattern and worsen the tiering asymmetry described in [[Reasoning Trace Privacy]].
- Language choice is unsettled — current implementations span Python, bash, and Bun, with no evidence about which suits which harness.

## Related pages

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
