---
type: concept
created: 2026-05-08
updated: 2026-10-09
tags:
  - concept
  - wiki
  - llm
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-09-02-meta-organizational-second-brain
  - src-2026-10-09-dickson-agent-stack-optimization
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

## A wiki can feed future procedures as well as future answers

[[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]] describes WikiSkill
as an intermediate store between raw execution traces and executable skills. Successes, failures,
and rejected fixes become structured experience for later skill optimization instead of
remaining scattered across runs.

That is a different output path from this vault's source-to-answer loop: **trace to evidence
wiki to proposed skill to evaluation**. The shared principle is retaining provenance and failed
attempts so that compression does not leave only an apparently successful procedure.

The proposal does not establish that every stored explanation is right, or that merely keeping
a wiki improves performance. The clipping reports no isolated WikiSkill gain. A practical
extension would retain model/task versions, the observations behind an edit, and its acceptance
or rejection evidence; these are maintenance implications, not a measured result or a claim that
this vault already executes that optimization loop.

## Open questions

- When should a new idea extend an existing concept page versus creating a fresh one?
- What review cadence keeps the wiki coherent as the number of sources grows?

## Related pages

- [[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]]
- [[Agent Skill]]
- [[Harness Optimization]]
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
