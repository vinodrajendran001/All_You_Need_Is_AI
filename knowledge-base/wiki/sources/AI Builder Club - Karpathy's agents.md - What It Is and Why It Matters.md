---
type: source-summary
created: 2026-08-05
updated: 2026-08-26
source_id: src-2026-08-05-aibuilderclub-karpathy-agents-md-framework
source_title: 'Karpathy''s agents.md: What It Is and Why It Matters'
source_author: AI Builder Club
source_url: https://www.aibuilderclub.com/blog/karpathy-agents-md-framework
tags:
  - source/summary
  - ai-agents
  - ai-builder-club
source_ids:
  - src-2026-08-05-aibuilderclub-karpathy-agents-md-framework
status: active
---

# AI Builder Club - Karpathy's agents.md: What It Is and Why It Matters

## Summary

This article is explicitly speculative: it says Karpathy had not published an `agents.md`, then reconstructs what such guidance might contain from his public themes and existing community conventions. It distinguishes project instruction files used by coding assistants from guidance for autonomous systems, emphasizing permission boundaries, auditable or reversible actions, loud failure, human checkpoints, and persistent memory. It also describes `AGENTS.md` as a cross-tool instruction convention alongside tool-specific files.

## Key claims

- Instructions for using a coding assistant differ from rules for an autonomous agent because the latter has broader action and trust boundaries.
- Permissions should be enumerated before implementation: readable resources, writable resources, forbidden areas, and actions requiring approval.
- Irreversible actions require checkpoints; reversible actions still need logs sufficient for reconstruction.
- Agents should stop and surface out-of-scope failures rather than improvise silently.
- A durable, inspectable memory file can provide more accountable continuity than ephemeral model context.
- Shared Markdown instruction files can reduce duplicated configuration across coding-agent tools.

## Why it matters

The piece identifies instruction files as part of the agent harness rather than mere prompt notes. Its proposed rules highlight that autonomy must be constrained in executable code and operational policy, not only described to the model.

## Tensions / open questions

- The central “Karpathy agents.md” artifact did not exist according to the source; the proposed contents are the author’s reconstruction, not Karpathy’s published framework.
- Claims about standards stewardship, native tool support, repository stars, and provenance should be independently verified.
- A memory file cannot be the sole source of truth if it can be poisoned, become stale, or conflict with runtime policy.
- Auditability does not make an unsafe or unauthorized action acceptable.

## Affected pages

- [[Andrej Karpathy]]
- [[Coding Agent Harness]]
- [[Agent Memory]]
- [[AI Agents in Production]]
- [[Agent Skill]]

## Citations

- Raw capture: [[2026-08-05 AI Builder Club - Karpathy's agents.md - What It Is and Why It Matters]]
- Canonical URL: https://www.aibuilderclub.com/blog/karpathy-agents-md-framework

## Raw capture

- [[2026-08-05 AI Builder Club - Karpathy's agents.md - What It Is and Why It Matters]]

## Related pages

- [[Context Engineering]]
- [[Tool Use and Function Calling]]
- [[Multi-Turn Evaluation]]

