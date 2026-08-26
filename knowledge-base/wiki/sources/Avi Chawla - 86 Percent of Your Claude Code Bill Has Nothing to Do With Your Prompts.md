---
type: source-summary
created: 2026-08-07
updated: 2026-08-26
source_id: src-2026-08-07-avi-chawla-claude-code-cost
source_title: 86% of Your Claude Code Bill Has Nothing to Do With Your Prompts
source_author: Avi Chawla
source_url: https://blog.dailydoseofds.com/p/8904b4e2-4510-4221-8e5d-18f44a3a1d59
tags:
  - source/summary
  - coding-agents
  - cost
  - observability
source_ids:
  - src-2026-08-07-avi-chawla-claude-code-cost
status: active
---

# Avi Chawla - 86% of Your Claude Code Bill Has Nothing to Do With Your Prompts

## Summary

Avi Chawla argues that coding-agent cost is dominated by repeatedly transmitted context rather than developers' visible prompts. In a vendor-associated analysis of a 45-person team, only 14% of input tokens were attributed to user prompts; the remainder included system instructions, skills, `CLAUDE.md`, MCP schemas, tool results, and prior assistant context. Prompt caching discounts repeated prefixes but does not eliminate their volume.

The article proposes category-level cost observability followed by configuration changes: remove unused MCP servers, load skills selectively, compact sooner, shorten sessions, lower reasoning effort, route routine work to cheaper models, and keep global instructions limited to invariants.

## Key claims

- Tool outputs compound because file reads, searches, and command results are replayed on later turns.
- Always-connected MCP tools impose schema cost even when never called.
- Long-lived instruction and memory files can become recurring overhead unrelated to the current task.
- Model tier and reasoning effort multiply the cost of every context decision.
- Session totals are insufficient for optimization; teams need attribution by context category and configuration source.
- Cost should be optimized without hiding quality impact, using measured policies rather than blanket restrictions.

## Why it matters

The source connects [[Context Engineering]], [[Coding Agent Harness]], [[Model Context Protocol]], and [[Model Routing]] through a single economic mechanism: every turn reprocesses a selected context. It strengthens the case for measuring full cost per successful task rather than only prompt size or request count.

## Tensions / open questions

- The article promotes Comet/Opik's Cost Intelligence product, and several headline figures are company-reported rather than independently reproduced.
- Token volume, cached-token price, wall-clock latency, and business value are different metrics and should not be collapsed.
- Aggressive compaction or instruction removal can reduce cost while silently harming task success.
- Claims about model equivalence and reasoning-effort savings are workload- and version-dependent.
- Hashing content reduces stored exposure but does not remove all metadata and deployment trust questions.

## Affected pages

- [[Context Engineering]]
- [[Coding Agent Harness]]
- [[Model Context Protocol]]
- [[Model Routing]]
- [[AI Agents in Production]]

## Citations

- Raw capture: [[2026-08-07 Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]]
- Canonical URL: https://blog.dailydoseofds.com/p/8904b4e2-4510-4221-8e5d-18f44a3a1d59

## Raw capture

- [[2026-08-07 Avi Chawla - 86 Percent of Your Claude Code Bill Has Nothing to Do With Your Prompts]]

## Related pages

- [[Agent Security and Governance]]
- [[Multi-Turn Evaluation]]
- [[Agent Memory]]

