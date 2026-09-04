---
type: concept
created: 2026-05-08
updated: 2026-09-04
tags:
  - concept
  - wiki
  - llm
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-09-02-meta-organizational-second-brain
status: active
---

# Persistent Wiki

## Definition

A persistent wiki is an interlinked markdown layer that the LLM updates over time so that synthesis, cross-references, and contradictions accumulate instead of being recomputed from raw sources for every question.

## Why it matters

It changes the value of the system from "good retrieval at query time" to "continuously improving compiled knowledge." The wiki becomes the durable working memory of the vault.

## Current synthesis

- The wiki sits between raw sources and downstream questions.
- Each ingest should strengthen or revise existing pages instead of producing isolated summaries.
- Good query answers can become durable pages, which means exploration compounds too.
- Maintenance cost stays low because the LLM can update many related files in one pass.

## What belongs in the wiki, and what stays in retrieval

This page has assumed the wiki is the right home for synthesis without saying what should *not* live there.
[[Meta - An Organizational Second Brain]] supplies a criterion from a production deployment: **split wiki from
retrieval by information density and expected usage frequency.** Dense material that is needed often becomes a
curated file the agent reads directly; sparse or rarely needed material stays in a retrieval corpus. That is a
resource-allocation rule rather than an architectural preference, and it makes the boundary decidable per topic
instead of per system.

The same source gives the wiki-as-context approach its first reported magnitude. Routing an agent through gateway
files and indexes rather than loading a fixed context — **progressive disclosure** — cut tokens per turn by
roughly **80%**. A curated wiki is not only better organised than a corpus; at that ratio it is materially
cheaper to consult.

It also shifts who the wiki is for. In that deployment the primary reader is an agent, and the file structure is
shaped by what an agent needs to traverse: gateway files that orient before descending, taxonomy files that fix
vocabulary, position files that each answer one question. This vault's pages are still shaped for a human reader
who happens to be assisted by a model. Whether those two audiences want the same page granularity is now an open
question with evidence on one side.

The convergence is worth noting for what it is: an independent team, a different domain, no shared code, and the
same shape. See [[Institutional Knowledge Agents]].

## Open questions

- When should a new idea extend an existing concept page versus creating a fresh one?
- What review cadence keeps the wiki coherent as the number of sources grows?

## Related pages

- [[Andrej Karpathy - LLM Wiki]]
- [[AI Knowledge Base Overview]]
- [[Schema-Driven Knowledge Base]]
- [[Ingest Query Lint Loop]]
- [[Index and Log]]
- [[Obsidian]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[Retrieval-Augmented Generation]]
- [[Context Engineering]]
