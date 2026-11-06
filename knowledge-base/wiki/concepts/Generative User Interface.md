---
type: concept
created: 2026-10-16
updated: 2026-11-06
tags: [concept, software-architecture, extensibility, state]
source_ids:
  - src-2026-08-20-jeremy-morrell-extensible-software
  - src-2026-10-09-rabi-guha-intelligent-ui
  - src-2026-10-30-figma-fluent-editing-model
status: active
---

# Generative User Interface

## Definition

A generative user interface is an interactive presentation whose structure or behavior is
produced by a model and interpreted by an application runtime. It may use a constrained
component language rather than unrestricted HTML. Generation, validation, execution, rendering,
and state ownership are separate architectural decisions.

## Why it matters

Streaming a useful interface requires more than syntactically valid final code. Partial
revisions must remain interpretable, user actions need stable state, and generated logic must
not inherit all the host application's privileges. These are runtime contracts, not properties
that a prompt can guarantee.

## Current synthesis

### A trusted host can interpret generated artifacts

[[Jeremy Morrell - Extensible Software in the Age of LLMs]] proposes a trusted application
shell that owns identity, storage, routing, and privileged capabilities while generated
extensions run behind narrow interfaces. It emphasizes durable, inspectable artifacts.

[[@rabi_guha - How ChatGPT Intelligent UI Works]] supplies a narrower observational example:
Markdown/JSX-like DIL is compiled into JavaScript plus data tables; an isolated worker
reconciles a UI tree and sends operations to a host-owned component renderer. Event handlers
cross as identifiers, and local interaction can update state without another model call.
This is third-party web reverse engineering, not OpenAI's specification or a security audit.

The shared design principle is to constrain what the generated artifact may express and
invoke while retaining host authority. It does not imply the two systems use the same
implementation or offer the same guarantees.

### Streaming continuity is not durable application state

The Intelligent UI account describes keyed state surviving recompilation and a last-working
program retained when a revision fails. Those mechanisms can preserve a slider's value during
streaming without establishing cross-session persistence, deterministic replay, schema
migration, or recoverable storage.

Morrell's durable-extension proposal therefore asks a further question: what artifact and
state survive the conversation, who can inspect them, and how are later versions upgraded?
The vault distinguishes both from [[Harness State Authority]], where authoritative state
must survive execution boundaries independently of generated descriptions.

### A catalog is only one execution path

The account observes roughly 70 native registered components and 39 in captured responses.
These are a dated registry and sample, not a stable public API. AppBlock separately runs
generated HTML/CSS/JavaScript in an iframe, and some native properties accept raw CSS.
Catalog validation cannot be generalized into a prohibition on arbitrary styling or into
an assurance covering every runtime path.

Likewise, compilation checks, a worker, an iframe, restricted globals, and a watchdog serve
different purposes. Their presence does not demonstrate containment or accessibility.
Fallback behavior also needs an explicit diagnostic policy rather than silently presenting
stale output as the requested new interface.

### Editing an existing design is a different contract from generating one

The two accounts above generate a new interface and let a host interpret it.
[[Josh Clemm - How We're Training a Figma-Fluent Editing Model]] starts from an interface that
already exists. [[Figma]]'s agent edits work on the canvas: spacing, a color, a layout rework
after feedback. The model reads and writes designs in **Figma's native file format**, so its
output is applied straight back to the canvas instead of being compiled into a separate runtime.
The worked example's success criterion is that the inserted component is "present, legible, and
contained" and that "unrelated content is preserved".

That shifts what has to be validated. Here the native format plays the part a constrained
component language plays above. Figma pairs deterministic validators of structure with visual
model judges, and scores separately for alignment, contrast, request fulfillment and use of the
correct design-system component. Expert designers calibrate those judges. Generation from
scratch is not routed to this model: image generation, vectors and new explorations go to
third-party models, and the first-party model handles precise edits. The account is first-party,
and it reports no accessibility, versioning or state-persistence guarantees of the kind raised
above.

## Open questions

- Which state must survive a revision, a failed worker, and a new session?
- How are capability grants and data access constrained on each execution path?
- How are accessibility, replay, versioning, and user-visible compilation failures assessed?
- When a model edits an existing artifact rather than generating one, which unchanged elements
  must a validator prove were preserved, and can visual judges detect structural regressions?

## Related pages

- [[@rabi_guha - How ChatGPT Intelligent UI Works]]
- [[Jeremy Morrell - Extensible Software in the Age of LLMs]]
- [[LLM-Native Extensible Software]]
- [[Josh Clemm - How We're Training a Figma-Fluent Editing Model]]
- [[Figma]]
- [[Harness State Authority]]
- [[Agent Security and Governance]]
- [[OpenAI]]
