---
type: entity
created: 2026-11-06
updated: 2026-11-06
entity_kind: organization
tags: [entity, organization, design-tools, post-training, agents]
source_ids:
  - src-2026-10-30-figma-fluent-editing-model
status: active
---

# Figma

## What it is

Figma is a collaborative design tool. Designers use it "from exploring a new idea to building out
an entire product". It now ships a Figma agent that edits work on the canvas. In this vault it
appears twice: as an MCP server that exposes design context to outside coding agents, and as the
publisher of a first-party account of post-training its own design-editing model.

## Why it matters here

Both appearances respond to the same problem: Figma's native design representation is hard for a
general model to read or write efficiently. The two responses differ.

- **Expose a curated interface.** In [[Model Context Protocol]] and [[AI Agents in Production]],
  Figma's MCP server turns raw design JSON into a more token-efficient representation. It
  recommends a scan-then-zoom tool sequence, so external agents do not drown in the file.
- **Train the model on the native format.**
  [[Josh Clemm - How We're Training a Figma-Fluent Editing Model]] says frontier models "couldn't
  understand Figma syntax", and that system prompting around this would have been "incredibly
  token-consumptive". Figma therefore fine-tuned a model whose
  inputs and outputs are designs in Figma's own file format, so edits can be applied straight back
  to the canvas.

The first route serves agents Figma does not control; the second serves Figma's own agent. The
vault has no source comparing them on the same task.

## The editing model

The post describes a [[Model Factory]] in miniature. Synthetic edit requests are paired with
starting designs. Larger teacher models attempt the edits, and deterministic validators plus visual
model judges keep valid, request-fulfilling candidates. SFT came first, on an earlier **Llama 3.3
70B** trained on **more than 250,000 examples**. RL followed, because imitation "at the cost of loss
of generalization" was also "less sample efficient". The latest unreleased model is "post-trained
on Qwen 3.8 27B". It scores **77.8%** against "Sol 6.1" at **76.9%** on Figma's internal editing
eval, which the post calls "just one input among many".

The agent routes work by task. Third-party models take image generation, vectors and new
explorations; the first-party model takes precise edits and iterations. This is a concrete
[[Model Routing]] split by task type rather than by difficulty. Between beta and general
availability, Figma reports typical tasks about **20% faster**; it also reports user ratings **33%
higher**, without a stated baseline. The new agent beats or matches the previous one **62%** of the
time with expert designers, and users undo its work **60% less often**. Figma attributes these gains
to "models, tools, and harness" together, so they are not evidence for the model alone.

## Caveats

- Both accounts are first-party or vendor-adjacent descriptions, not independent evaluations.
- The editing eval, its size and its judge calibration are internal and unpublished.
- Editing an existing design is a narrower task than
  [[Generative User Interface|generating an interface]]. Results for one should not be assumed for
  the other.

## Related pages

- [[Josh Clemm - How We're Training a Figma-Fluent Editing Model]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Model Context Protocol]]
- [[AI Agents in Production]]
- [[Model Factory]]
- [[Model Routing]]
- [[Generative User Interface]]
- [[Qwen]]
