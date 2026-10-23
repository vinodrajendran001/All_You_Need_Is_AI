---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-21-mcateer-claude-mods
source_title: "Claude Mods: Flipping the Harness Inside Out"
source_author: Dan McAteer
source_url: https://www.latent.space/p/claude-mods
tags: [source/summary, coding-agents, extensibility, governance]
source_ids:
  - src-2026-10-21-mcateer-claude-mods
status: active
---

# Dan McAteer - Claude Mods and the Attention Interface

## Summary

A practitioner account of programmable, human-facing agent-harness middleware. McAteer calls
the layer choosing what to show, when to interrupt, and what decision to request the
**Attention Interface**. Claude Mods are described as JavaScript/TypeScript functions running
inside Claude Code and responding to prompts, tools, and rendering events. The architectural
idea is useful; the evidence for effectiveness consists of personal examples, not an
evaluation of productivity or safety.

## Key claims

- Mods can observe, change rendering, or handle events instead of default behavior. The
  author reports six built-ins: agents-md, diff, plugin-authoring, sec-default, telemetry,
  and you-should-know, with the last off by default.
- **You Should Know** is described as an observing side agent. In one anecdote, it warned
  that a file being edited already contained uncommitted work, as did about **45 other
  files**; discarding the demonstration edits risked losing earlier changes.
- The author's **Next Steps Supervisor**, distributed through ModSmith, runs after turns
  that edit files, run commands, or make **8 or more tool calls**. Since October 15,
  **99 of 111** of his turns met that rule. This measures trigger frequency, not false
  positives or helpful interventions; the author reports starting to skim the output.
- Each check forks and rereads conversation state. The mod README is quoted estimating
  **5-6k input-equivalent tokens per check on a 50k-token session**, with more cost after
  cache expiry. This is an estimate, not measured incremental billing.
- Mods are reported **unsandboxed**, able to read/write files, inspect prompts, and spend
  usage under the user's permissions. Built-in mods reportedly continue under `--safe-mode`;
  the name is not evidence of an all-extension isolation mode.

Three products illustrate different control surfaces: ChatGPT's Intelligent UI lets the
model choose an answer-specific interface; Cursor's PR Routing & Approval lets a team set
review policy; Claude Mods let the user and agent author the interface behavior itself.
This is McAteer's comparison, not proof that competing products lack every similar feature.

The Cursor account includes a concrete authority rule: a pull request modifying approval
policy is assessed using the **base-branch policy**, not its proposed relaxation. Risk
scores, reviewer findings, and thresholds help route attention but do not replace full review.

## Why it matters

[[Coding Agent Harness]] optimization must count human attention and supervisor cost as well
as task execution. [[LLM-Native Extensible Software]] needs a distinction between malleable
code and isolated code: these mods do not instantiate the narrow-capability architecture
merely because an agent can generate them. [[Agent Security and Governance]] keeps attention
suggestions separate from authority and approval policy.

## Tensions / open questions

- The author built ModSmith and reports his own use; no control group, time saving, or
  correctness rate is established.
- One supervisor labeled a task "Solved" while listing **two gaps and three shortcuts**.
  A second opinion or completion label is not a verified deliverable.
- The proposed harness that mines transcripts and suggests its own modifications is a
  future direction, not a demonstrated autonomous improvement loop.
- Cost and interruption frequency need to be weighed against issues actually caught.
  High visibility can create habituation rather than better oversight.
- Product behavior and permission claims are captured descriptions; linked documentation
  and plugin implementation were not independently audited or executed in this ingest.

## Affected pages

- [[Coding Agent Harness]]
- [[LLM-Native Extensible Software]]
- [[Agent Security and Governance]]
- [[Anthropic]]

## Raw capture

- [[Claude Mods Flipping the Harness Inside Out]]

## Citations

- Dan McAteer: <https://www.latent.space/p/claude-mods>.
- Published October 21; captured October 23, 2026. Tracking query removed from the summary URL.
- Linked ModSmith implementation: <https://github.com/DannyMac180/skills/tree/main/modsmith>.
- Linked product documentation: <https://code.claude.com/docs/en/plugins/mods/overview>
  and <https://cursor.com/docs/approval-agents>; not separately ingested.

## Related pages

- [[Coding Agent Harness]]
- [[LLM-Native Extensible Software]]
- [[Agent Security and Governance]]
- [[Anthropic]]
- [[Generative User Interface]]
- [[Harness State Authority]]
- [[Agent Plugin Architecture]]
