---
type: entity
created: 2026-08-30
updated: 2026-08-30
entity_kind: person
tags:
  - entity
  - person
  - developer-tooling
  - agents
  - context-engineering
source_ids:
  - src-2026-08-30-addy-osmani-audit-agent-files
status: active
---

# Addy Osmani

## What it is

An engineering leader at Google working on Chrome and web developer experience, and a prolific writer
on developer productivity. His recent writing focuses on how software engineers should actually work
with coding agents.

## Why it matters here

[[Addy Osmani - Audit your Agent files]] is the vault's principal source of *counter-evidence* on
context files. Where most agent material assumes richer instructions help, Osmani assembles studies
that put a number on the null hypothesis:

- A June study of 100 repositories found **lint leakage in 62%, context bloat in 42%, skill leakage in
  35%**.
- Anthropic removed **more than 80%** of Claude Code's system prompt with **no measurable eval loss**.
- Across **288 runs on 17 tasks**, the presence of `AGENTS.md` / `CLAUDE.md` made **no clear difference
  to correctness**.
- Agents answering behavioural questions from prose summaries scored **4/45**; agents reading source
  code scored **27/45**.

His framing — agent configuration **has a half-life** — is the argument [[Context Engineering]] and
[[Agent Skill]] now have to answer.

## Notes

- He names a real usability trap: `/doctor` (in-session) audits the active configuration, while
  `claude doctor` (CLI) only runs install diagnostics. The names are near-identical; the jobs are not.
- He flags his own weakest citation, noting that the personalization study used an **LLM-based
  developer simulator** rather than real developers.
- The practical rule his evidence supports: instructions must justify themselves against an eval, and
  the default action for an unjustified rule is deletion.

## Related pages

- [[Context Engineering]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
- [[Agent Memory]]
- [[AI-Native Software Development Lifecycle]]
- [[Harness Optimization]]
- [[Addy Osmani - Audit your Agent files]]
