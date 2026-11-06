---
type: entity
entity_kind: organization
created: 2026-11-06
updated: 2026-11-06
tags:
  - entity
  - organization
  - coding-agents
  - agent-harness
source_ids:
  - src-2026-10-29-factory-droid-frontier-harness
status: active
---

# Factory AI

## What it is

Factory is the company behind **Droid**, a coding-agent harness sold as a desktop app for macOS and
Windows, a terminal UI, and a TypeScript SDK (`@factory/droid-sdk`) that runs the same harness as the
CLI. Its research posts carry the byline "Factory Research". The company describes itself as
"model-independent by design": Droid supports many frontier models, open- and closed-weight, and an
auto model router, Factory Router, can pick "the most efficient mix" for the user. Factory says it
has worked with "hundreds of thousands of developers" at large enterprises; that figure is
self-reported.

The vault names it "Factory AI" to separate the company from the generic word. Its captured post
lives on factory.com, its citation line gives factory.ai, and its SDK repository sits under the
`Factory-AI` GitHub organization.

## Why it matters here

[[Factory Research - Droid 1.0 - Building a Frontier Harness]] is the vault's first account from a
harness vendor that tunes one harness across many model families and publishes a head-to-head against
the model labs' own harnesses with pinned versions and a written methodology. Three things matter
beyond the product claims:

- **Programmatic tool calling as a default.** Droid's Script tool runs many tool calls inside one
  model request and is on by default for ten frontier models. See [[Programmatic Tool Calling]].
- **A human-merged improvement loop.** The internal Agent Factory turns benchmark failures and user
  friction into proposed changes with stated hypotheses, measures each on every affected model, and
  leaves the merge decision to engineers. See [[Harness Optimization]] and [[Loop Engineering]].
- **Model-specific effects inside a model-independent harness.** Its line-numbering result helped
  two models (Sol and Opus) and raised cost on two others, which is direct evidence that a harness
  change does not transfer automatically across models. See [[Coding Agent Harness]].

All of these are first-party claims. The Terminal-Bench 4 comparison was run by Factory, with cost
and time counted only on tasks both harnesses passed in all three trials, and with some trials
imputed or substituted; see [[Benchmark Optimization]].

## Related pages

- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[Coding Agent Harness]]
- [[Programmatic Tool Calling]]
- [[Harness Optimization]]
- [[Loop Engineering]]
- [[Benchmark Optimization]]
- [[Model Routing]]
- [[Replit]]
