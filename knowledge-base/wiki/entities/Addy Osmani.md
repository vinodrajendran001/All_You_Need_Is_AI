---
type: entity
created: 2026-08-30
updated: 2026-10-23
entity_kind: person
tags:
  - entity
  - person
  - developer-tooling
  - ai-agents
  - context-engineering
source_ids:
  - src-2026-08-30-addy-osmani-audit-agent-files
  - src-2026-10-15-osmani-claude-code-review
status: active
---

# Addy Osmani

## What it is

An engineering leader at Google working on Chrome and web developer experience, and a prolific writer
on developer productivity. His recent writing focuses on how software engineers should actually work
with coding agents.

## Why it matters here

The vault now holds two Osmani sources with **different evidential standing**, and the distinction is
worth keeping: the first assembles studies, the second reports another organisation's process.

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

## As a reporter of someone else's process, not an assembler of evidence

[[Addy Osmani - How the Claude Code Team Does Code Review]] is Osmani writing in a second mode. The
agent-files piece gathers studies and argues against a prevailing assumption; this one describes how
Anthropic restructured review once agents wrote most of the diff, and **every figure in it is
Anthropic's own, self-reported, with no controlled comparison**. Read it as reportage of one
organisation's operating model rather than as evidence for its effectiveness.

The content most worth carrying from it is the loop-termination machinery, because it is the part
least dependent on Anthropic's tooling. Review is **capped after three rounds**, later passes can be
**diff-only**, repeated findings are suppressed, and agents are asked to name bug *classes* rather
than isolated lines. The motivating failure was a single CLI pull request that ran **more than fifty
rounds** of review and fixes, and the diagnosis is the sharpest number in the piece: about **59%** of
repeatedly flagged code **predated the reviewer's first pass**, so the loop was partly re-litigating
surrounding code rather than the change. After that work, Anthropic reports the one-round pass rate
moving **65% → 78%**, five-or-more rounds **8.9% → 1.5%**, and mean reviews-to-pass **2.08 → 1.32** —
before versus after the convergence changes, with population and time window unstated.

**This sits awkwardly beside his own null result, and the tension should not be smoothed away.** The
agent-files evidence says instruction files did not move correctness across 288 runs; here a
repository-specific **`REVIEW.md`** — failure modes, evidence requirements, paths to skip, limits on
stylistic findings — is treated as load-bearing, kept deliberately separate from `CLAUDE.md`. Nothing
in the second source ablates that file, so it is a described practice, not a refutation of the first
source's measurement. What changed is the scope of the claim Osmani is transmitting: from *does a
context file help a model get the answer right* to *does a committed policy file keep a review loop
converging*. Those are different questions and the vault holds evidence for neither answering the
other.

## Open questions

- Does `REVIEW.md` earn its place against an eval, by Osmani's own standard from the agent-files
  piece? Neither source tests a repository with and without one.
- The convergence figures are Anthropic's, reported through Osmani, with no population, time window,
  or independent replication. Would the three-round cap help a team without merge queues, feature
  flags, risk classifiers, and daily eval sets behind it?
- Neither source speaks to review **recall** — what agent reviewers miss — only to volume, noise, and
  convergence.

## Related pages

- [[Addy Osmani - How the Claude Code Team Does Code Review]]
- [[Anthropic]]
- [[Agentic Testing]]
- [[AI-Native Software Development Lifecycle]]
- [[Context Engineering]]
- [[Agent Skill]]
- [[Coding Agent Harness]]
- [[Agent Memory]]
- [[Harness Optimization]]
- [[Addy Osmani - Audit your Agent files]]
