---
type: concept
created: 2026-05-08
updated: 2026-09-04
tags:
  - concept
  - navigation
  - maintenance
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-09-02-meta-organizational-second-brain
status: active
---

# Index and Log

## Definition

`index.md` is the content-oriented catalog of the wiki, while `log.md` is the append-only operational timeline of what changed and when.

## Why it matters

Together they give both the human and the LLM lightweight navigation and memory without requiring dedicated retrieval infrastructure at small scale.

## Current synthesis

- The index is the first file to read when routing a question through the wiki.
- The log preserves chronology, which helps reconstruct recent ingests, queries, and maintenance passes.
- Keeping both files current makes the wiki legible even as it grows.
- This vault uses them as explicit control surfaces rather than passive notes.

## Deterministic routing, and the log as a regression suite

[[Meta - An Organizational Second Brain]] independently arrives at both halves of this page and pushes each one
further.

**Routing indexes are deterministic, not similarity-based.** In that deployment, the path from a question's shape
to the relevant files is a lookup structure, explicitly not an embedding neighbourhood. This is the design choice
that makes mechanical checking possible at all: a declared route can be tested for dangling references, and a
nearest-neighbour result cannot. It is the same reason this vault's `index.md` is a written catalog rather than a
generated one, but the argument here is sharper — determinism is not a stylistic preference, it is the
precondition for the linter.

**The change record can be more than chronology.** This vault's `log.md` preserves what happened. In Meta's loop
every fix is **folded back into a regression suite**, so the record of past failures is executable: it prevents
the loop from silently trading an old capability for a new one. That is the capability this page's log does not
have — it can tell you when a claim was added, but nothing replays whether the claim still holds.

Alongside it sits a validation practice worth naming: **targeted replay is blind.** The agent does not know it is
being tested, and the judge does not know what changed. Both halves matter, and both are absent from a purely
chronological log.

## Open questions

- At what scale should index maintenance become partially automated with Dataview or custom tooling?
- What level of detail in log entries best balances traceability with readability?

## Related pages

- [[index|Knowledge Base Index]]
- [[log|Knowledge Base Log]]
- [[Ingest Query Lint Loop]]
- [[Persistent Wiki]]
- [[Schema-Driven Knowledge Base]]
- [[Obsidian]]
- [[Andrej Karpathy - LLM Wiki]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[LLM-as-a-Judge]]
