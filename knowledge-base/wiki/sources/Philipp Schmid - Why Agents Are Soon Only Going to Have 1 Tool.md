---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-01-philipp-schmid-code-mode
source_title: "Why Agents Are Soon Only Going to Have 1 Tool"
source_author: "Philipp Schmid"
source_url: "https://www.philschmid.de/code-mode"
tags:
  - source/summary
  - tool-use
  - agent-harness
  - code-execution
source_ids:
  - src-2026-11-01-philipp-schmid-code-mode
status: active
---

# Why Agents Are Soon Only Going to Have 1 Tool

## Summary

[[Philipp Schmid]] argues that agents are converging on **Code Mode**, which he also calls
Programmatic Tool Calling: the harness exposes one `exec(code)` tool, the model writes a short
TypeScript or Python script, and the script "chains, combines, and awaits actions inside an isolated
sandbox" before returning only a final result. The essay places this at the end of a short history of
tool calling, explains the host-side bridge that makes it work, argues for a JavaScript or Python
runtime over `bash`, and shows a pseudo-implementation on the Gemini Interactions API. It is an
opinion and design essay grounded in "my own experience"; it reports no measurements of its own, and
its one quantitative claim is a secondhand account of Factory's results that does not match the
vault's capture of Factory's post.

## Key claims

### One action per turn is the limit that tool search did not remove

Schmid's evolution narrative runs: first a handful of tools, because models "couldn't reliably choose
or filter across a large catalog"; then dozens of tools or MCP servers, which hit context-window
limits; then tool search and progressive disclosure to load tools on demand. Even with dynamic loading,
standard tool calling still allowed "*one* action per turn" (or "at best a flat batch of independent
calls"), followed by a round trip through the model. Code Mode targets that round trip, not the
catalog size.

His four use cases are research and filtering in one step, multi-file edits with inline verification
and branching on pass or fail, browser and computer-use sequences scripted in a loop, and parallel
fan-out, such as **20** lookups awaited with `Promise.all` and fed into a second API without passing
through the context window between steps.

### Why now: code-trained models and declared return types

Three shifts are named: frontier models "are trained heavily on code"; providers "have started
post-training models for Code Mode"; and MCP servers "increasingly ship" an `outputSchema` alongside
`inputSchema`, a field the essay links in the MCP **draft** specification. Knowing the return type up
front lets the model chain Tool A into Tool B "*before* seeing runtime output". No evidence is given for
the post-training claim.

### The mechanism: compiled declarations, a bridge, and explicit output helpers

"Instead of passing 80 separate JSON Schema tool objects", the agent compiles schemas into compact
type declarations (`declare namespace tools { ... }`) and the script calls
`await tools.<server>.<tool>(args)`. Large catalogs need not be fully exposed: tool search still
applies, or the sandbox can hold an `ALL_TOOLS` map of descriptions and signatures. Output helpers
`text()`, `image()`, and `audio()` define what returns: "only what is passed here enters the model
context window". `store()` and `load()` keep state outside the context across turns.

In the illustrative issue-tracker cleanup, the sandbox "executes all **55** underlying API calls",
filters in memory, and returns one line: "Archived **42** unassigned issues across **12** projects."
The example is constructed, not measured.

### Why a language runtime rather than bash

Schmid grants that a tool proxy can be built in `bash`, then lists five advantages of JavaScript or
Python: typed calls with native objects, `Promise.all`, and `try`/`catch` instead of string escaping;
**no CLI exploration tax**, because models given custom CLIs "tend to over-explore before acting",
running `--help` across subcommands; **multimodal context**, since a shell returns stdout and cannot
`cat screenshot.png` into the model; a **credential and policy proxy**, because every `tools.*` call
crosses a bridge where the host "can inject OAuth tokens outside the sandbox, validate schemas, or
pause for user confirmation on destructive calls"; and key-value **state** outside the prompt history.

### A runnable sketch on the Gemini Interactions API

The pseudo-example gives `gemini-4-argon` a single execution tool, runs its script with
`vm.runInNewContext` with the warning to "use QuickJS or isolated-vm for untrusted code", and sends
only a one-line summary back through `previous_interaction_id`. The task scans `.ts` files with more
than **50** additions in PR **#42**; intermediate file objects and scanner payloads never enter the
context window.

### Adoption claims and the closing hedge

Schmid writes that Pi, Factory Droid, and OpenAI Codex "now ship with or default to Code Mode", and
that "Factory switched Droid 1.0 to Code Mode, improving their Terminal-Bench 4 accuracy by **+3.5**
points and cutting model spend by **15%**." Pydantic AI, LangChain, and Cloudflare's Agents SDK are
said to support similar tools. He then answers his title's question with "Not necessarily": many
tools, CLIs, and Agent Skills "were optimized for `bash` and human-readable text", so adopting Code
Mode may force you to "audit what your agent actually needs".

## Why it matters

The essay is the clearest single-author statement in the vault that [[Programmatic Tool Calling]] is
becoming the default model surface rather than an optional optimization. It reframes
[[Tool Use and Function Calling]] as a contract question — one script per turn instead of one call —
and gives [[Model Context Protocol]] a concrete reason to declare output types. Its "no CLI
exploration tax" argument is a qualitative counterpoint in [[Tool Roster Economics]], where a
discoverable CLI behind one tool has been proposed as the way to keep the roster small. The
credential and policy bridge, and the harness-default claim, extend [[Coding Agent Harness]].

## Tensions / open questions

- **The Factory numbers are conflated.** In
  [[Factory Research - Droid 1.0 - Building a Frontier Harness]], **3.5** points is Droid's margin
  over Codex on GPT-6.1 Sol in a harness comparison (three trials, at 12% lower cost), and **15%** is
  Script mode's cost saving on Claude Opus 5.5 with an unstated measurement method. Schmid attributes
  both to "Factory switched Droid 1.0 to Code Mode"; neither figure isolates that switch as described.
- No measurements of his own: the "big jump" in chaining reliability, the over-exploration of CLIs,
  and the post-training claim are experience-based assertions.
- The bash comparison is one-sided. The vault's [[Tool Roster Economics]] records arguments for a
  CLI behind one tool; whether typed declarations cost fewer turns than `--help` exploration is
  unmeasured on either side.
- The approval point is a capability of the bridge, not a demonstrated policy: which calls count as
  destructive, and who decides, is left to the host.
- The sample code uses `vm.runInNewContext`, which the essay itself says is unsafe for untrusted
  code; sandbox isolation is out of scope.
- `outputSchema` is cited from the draft MCP specification, so its stability is not established.
- Schmid is at Google DeepMind (per [[Philipp Schmid]]) and the worked example uses the Gemini
  Interactions API; the claims about other harnesses rest on links, not described tests.

## Affected pages

- [[Programmatic Tool Calling]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Tool Roster Economics]]
- [[Coding Agent Harness]]
- [[Philipp Schmid]]

## Raw capture

- [[knowledge-base/raw/sources/Why Agents Are Soon Only Going to Have 1 Tool]]

## Citations

- Canonical URL: <https://www.philschmid.de/code-mode>
- By Philipp Schmid on philschmid.de, published November 1, 2026; captured November 10, 2026 (the
  captured link carried Substack email tracking parameters, removed here).

## Related pages

- [[Programmatic Tool Calling]]
- [[Tool Use and Function Calling]]
- [[Model Context Protocol]]
- [[Tool Roster Economics]]
- [[Coding Agent Harness]]
- [[Philipp Schmid]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Computer Use Agents]]
- [[Agent Skill]]
