---
type: concept
created: 2026-05-08
updated: 2026-09-04
tags:
  - concept
  - workflow
  - maintenance
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-09-02-meta-organizational-second-brain
status: active
---

# Ingest Query Lint Loop

## Definition

The core operating loop of the knowledge base is threefold: ingest new sources, answer questions against the maintained wiki, and periodically lint the wiki for coherence and gaps.

## Why it matters

This loop turns the knowledge base into a living system rather than a pile of notes. It gives the LLM recurring responsibilities and makes knowledge maintenance explicit.

## Current synthesis

- **Ingest** converts a new source into a raw capture, a source page, and a set of updates across concept and entity pages.
- **Query** reads the index first, follows the current wiki graph, and can file durable outputs back into the vault.
- **Lint** checks for broken links, stale claims, missing pages, weak summaries, and research gaps.
- The loop compounds value because every pass improves future passes.

## Maintenance as compilation

[[Meta - An Organizational Second Brain]] describes the same loop from an industrial deployment and frames it
differently: **maintenance is a compilation problem.** Expert feedback is the source language, the knowledge base
is the target, and the pipeline has four staged steps — diagnose, compile, validate, expert review — each with a
specific defence.

**Diagnosis needs the right question, and the obvious one fails.** Classifying failures by conversational form
did not work. The test that did: **"Could the agent have reached the correct conclusion from its source
materials?"** If yes and it erred, the procedure is wrong. If no, knowledge is missing. If the experts disagree
with each other, the underlying position is ambiguous and the fix is a decision, not an edit. That third branch
is the one this vault's lint pass has no vocabulary for — it records contradictions but cannot distinguish a
contradiction between sources from an unmade decision.

**Compilation is reviewed adversarially.** A second agent sees only the diffs, with no knowledge of the rationale
that motivated them, and argues against the change. Withholding the story is the point: a reviewer who knows why
a change was made will reconstruct its justification.

**Validation is two-layered**: a deterministic linter that passes or fails (dangling cross-references, file-size
budgets, identifier collisions, dependency cycles), then blind regression replay where the agent does not know it
is under test and the judge does not know what changed.

Read against this vault's loop, the gaps are specific. Ingest and lint exist here; **compile** is implicit,
**adversarial review** is absent, and **regression replay** has no analogue at all — this vault's lint checks
structure but never re-asks a question it previously answered. The reported outcome ("zero regressions" over
three sprints) also carries its own caveat: it is measured by a suite the same loop wrote, so a failure the
diagnosis step never characterised would not be in it.

## Open questions

- How often should lint passes happen in practice for this vault?
- Which user prompts should automatically result in a filed query note or synthesis page?

## Related pages

- [[Schema-Driven Knowledge Base]]
- [[Index and Log]]
- [[Persistent Wiki]]
- [[Andrej Karpathy]]
- [[Obsidian]]
- [[Andrej Karpathy - LLM Wiki]]
- [[AI Knowledge Base Overview]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[LLM-as-a-Judge]]
- [[Recursive Self-Improvement]]
