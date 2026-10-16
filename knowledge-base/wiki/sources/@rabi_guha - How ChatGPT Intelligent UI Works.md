---
type: source-summary
created: 2026-10-16
updated: 2026-10-16
source_id: src-2026-10-09-rabi-guha-intelligent-ui
source_title: "We reverse engineered ChatGPT Intelligent UI. Here's how it actually works"
source_author: "@rabi_guha"
source_url: https://x.com/rabi_guha/status/2108238432355123572
tags: [source/summary, generative-ui, software-architecture, state, sandboxing]
source_ids: [src-2026-10-09-rabi-guha-intelligent-ui]
status: active
---

# @rabi_guha - How ChatGPT Intelligent UI Works

## Summary

A third-party reverse-engineering account of ChatGPT Intelligent UI, based on the authors'
own accounts, web traffic, and publicly served client JavaScript in October 2026.
Its useful model is a split between generated interface source, server compilation, an
isolated client runtime, and host-owned rendering. It is not an OpenAI specification,
an independent sandbox audit, or direct evidence for every mobile implementation.

## Key claims

1. **Generated source:** DIL combines Markdown, JSX-like components, and JavaScript for state
   and logic. The format supports useful partial constructs during token streaming.
2. **Compilation:** the server turns source into JavaScript plus JSON text/data tables,
   stored under `model_dil_v2`. Reported transformations include keyed state, expression-level
   error isolation, incomplete-construct repair, and catalog property validation.
3. **Runtime:** a hidden sandboxed iframe starts a worker that evaluates the compiled program,
   maintains keyed hook state, reconciles trees, and emits operations rather than drawing UI.
   The account describes restricted globals and a watchdog that restarts an unresponsive worker.
4. **Rendering:** the host interprets operations using its known component catalog. Event
   handlers cross the boundary as identifiers; a slider update can run locally without a
   fresh model call.
5. **Streaming:** patches update source, compiled code, constants, and data. Stable keys let
   state survive successive recompilations. The runtime reportedly retains the last working
   program if a new revision fails.

The author reports **about 70 registered native components**, of which **39 appeared in the
captured responses**. These are an inspected registry and an observation sample, not a promised
stable public API. Two observed validation diagnostics remove an unknown icon property and
a string literal of the wrong type on a box.

Static text is separated from executable structure so growing prose can update data tables.
The server is described as recompiling the accumulated response rather than compiling only
new source; the exact few-hundred-millisecond cadence and chunk trigger are observational
inferences, not independently established server internals.

**AppBlock is a separate path:** generated HTML/CSS/JavaScript runs in an iframe when the native
catalog is insufficient. Some native component properties also accept raw CSS values.
The catalog restriction therefore must not be generalized to every output path.

## Why it matters

[[Generative User Interface]] is a compilation and state-management problem, not just a
prompt that asks for HTML. The connection to [[LLM-Native Extensible Software]] is the trusted
host controlling capabilities and interpretation while generated artifacts remain constrained.
Keeping interaction state stable across streamed revisions is narrower than maintaining a
durable, versioned extension across sessions.

## Tensions / open questions

- Browser-visible behavior supports an architectural hypothesis, not exhaustive knowledge of
  server implementation, release coverage, or all clients.
- The methodology inspects web traffic and public web JavaScript. Claims about native mobile
  parity are not separately demonstrated by that method.
- Restricted globals, a worker, an iframe, validation, and a watchdog are different controls.
  Their description is not proof that generated code cannot escape, leak data, or exhaust resources.
- The raw example illustrates compiler error isolation; it is not a recommendation to silently
  suppress failures in arbitrary applications. Diagnostics and last-working-state fallback
  need an explicit user-visible failure policy.
- Stable hook keys preserve particular interaction state, not every property of replay,
  persistence, schema migration, authorization, or accessibility.

## Affected pages

- [[Generative User Interface]]
- [[LLM-Native Extensible Software]]
- [[Agent Security and Governance]]
- [[OpenAI]]

## Raw capture

- [[We reverse engineered ChatGPT Intelligent UI. Here's how it actually works]]

## Citations

- Original post: <https://x.com/rabi_guha/status/2108238432355123572>
- Published October 9; captured October 12, 2026.
- Linked fuller account, not separately ingested:
  <https://www.openui.com/blog/how-chatgpt-intelligent-ui-works>.

## Related pages

- [[Generative User Interface]]
- [[LLM-Native Extensible Software]]
- [[Harness State Authority]]
- [[Agent Security and Governance]]
- [[OpenAI]]
