---
type: source-summary
created: 2026-08-30
updated: 2026-08-30
source_id: src-2026-08-30-addy-osmani-audit-agent-files
source_title: "Audit your Agent files"
source_author: "Addy Osmani"
source_url: "https://addyo.substack.com/p/audit-your-agent-files"
tags:
  - source/summary
  - topic/agents
  - topic/context-engineering
  - topic/developer-tooling
source_ids:
  - src-2026-08-30-addy-osmani-audit-agent-files
status: active
---

# Addy Osmani - Audit your Agent files

## Summary

An argument that agent configuration — `AGENTS.md`, `CLAUDE.md`, skills, memory files, MCP servers —
**has a half-life**. Rules written for a model that needed them survive into a model that does not,
and the accumulated instructions quietly consume context and constrain behaviour without anyone
re-testing whether they still earn their place. Osmani's prescription is a periodic audit, and his
evidence is a set of studies that are unusually unflattering to the practice.

## Key claims

**Agent files rot measurably.** A June study of 100 repositories found **lint leakage in 62%**
(project-specific lint rules baked into agent instructions), **context bloat in 42%**, and **skill
leakage in 35%**.

**Removing instructions often costs nothing.** Anthropic removed **more than 80% of Claude Code's
system prompt with no measurable loss on evals**.

**The headline negative result: context files may not improve correctness at all.** A study of **288
runs across 17 tasks** found that the presence of `AGENTS.md` / `CLAUDE.md` made **no clear
difference to correctness**. It did change *how* agents worked — they wrote more targeted tests — but
the outcome measure did not move.

**Personalization is not obviously worth it.** Personalized skills performed roughly on par with
borrowed ones, and a **generic skill built from many developers' practice was more useful** than a
personalized one. Osmani flags the caveat himself: the study used an LLM-based developer simulator
rather than real developers.

**Prose summaries are a poor substitute for the code.** Agents answering behavioural questions from
prose summaries got **4 of 45** right; agents reading the source code got **27 of 45**. Documentation
that describes behaviour is not a shortcut around the behaviour.

**Practical audit mechanics.**

- `/doctor` (in-session) audits the active configuration; `claude doctor` (CLI) only runs install
  diagnostics. The similar names are a trap — the two commands do different jobs.
- `/memory` covers memory files and should be reviewed as a separate pass.
- Skill *listings* are budgeted at roughly **1% of the context window** by default; only the body of
  an invoked skill loads. So a long skill body is cheap until called, but a proliferation of skill
  names is not free.

## Why it matters

The vault's [[Context Engineering]] and [[Agent Skill]] pages are largely built from sources that
assume richer context files help. This is the first source here that puts a number on the null
hypothesis, and it is a large study by the standards of this literature. Combined with Anthropic's
80% prompt reduction, the working assumption should invert: **instructions must justify themselves
against an eval, and the default action for an unjustified rule is deletion.**

The 4/45 vs 27/45 result also constrains how documentation should be written for agents: summaries
of behaviour are near-useless compared with pointers to the code that implements it.

## Tensions / open questions

- The 288-run study measures correctness. Agents with context files wrote more targeted tests, which
  is a real behavioural change with plausible long-run value that a per-task correctness metric
  cannot see. "No clear difference" may be a measurement limit rather than a null effect.
- The personalization study used an LLM-based developer simulator; whether simulated preferences
  track real ones is unestablished.
- If a generic skill beats a personalized one, that could mean personalization is worthless, or that
  the personalization signal available to the study was too thin. The source cannot distinguish these.
- Osmani prescribes auditing but offers no eval harness for deciding which specific rule to cut — the
  studies show aggregate bloat, not per-rule attribution.

## Affected pages

- [[Context Engineering]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
- [[Addy Osmani]]

## Related pages

- [[Agent Memory]]
- [[AI Agents in Production]]
- [[Model Context Protocol]]
- [[AI-Native Software Development Lifecycle]]
- [[Harness Optimization]]

## Citations

- Raw capture: [[2026-08-30 Addy Osmani - Audit your Agent files]]
- Original: <https://addyo.substack.com/p/audit-your-agent-files> (published 2026-08-27)
