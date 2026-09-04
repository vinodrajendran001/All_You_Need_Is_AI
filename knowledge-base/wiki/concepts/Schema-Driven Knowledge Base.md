---
type: concept
created: 2026-05-08
updated: 2026-09-04
tags:
  - concept
  - schema
  - workflow
source_ids:
  - src-2026-05-08-karpathy-llm-wiki
  - src-2026-09-02-meta-organizational-second-brain
status: active
---

# Schema-Driven Knowledge Base

## Definition

A schema-driven knowledge base uses an instruction file to define the directory structure, note types, naming conventions, workflows, and maintenance rules that the LLM must follow.

## Why it matters

Without a schema, the model behaves like a generic assistant. With a schema, it behaves like a disciplined maintainer that updates the right pages, preserves consistency, and keeps the wiki navigable.

## Current synthesis

- The schema is the operational contract between human and LLM.
- It encodes how ingests happen, how durable answers get filed, and how the wiki gets linted.
- In this workspace, the root `CLAUDE.md` file is the schema and `knowledge-base/` is the maintained surface it governs.
- The schema should evolve as the vault grows, especially when new page types or workflows prove useful.

## An industrial instance, and three rules this schema does not have

[[Meta - An Organizational Second Brain]] is the first source in this vault describing a **schema-driven
knowledge base built by someone else, in production, for a different purpose** — a compliance-domain expert agent
over 200+ files. The convergence is close enough to be useful as a comparison: declared frontmatter, typed page
kinds, an explicit routing layer, and a maintenance pass that checks the graph rather than reading it.

Three of its rules are stronger than anything in this vault's schema.

**Declared bidirectional dependencies.** Every file names both `depends_on` and `referenced_by`. The redundancy
is deliberate: it converts "did this edit break something?" from a search into a lookup. This vault's schema
declares `source_ids` but leaves page-to-page dependency implicit in wikilinks, which is why its link checking is
a whole-vault scan rather than a local query.

**A hard separation between procedures and facts.** *Recipes* are imperative and contain no domain facts;
*knowledge files* are declarative positions and contain no procedures. The payoff is attribution — a wrong answer
is a recipe bug or a knowledge gap, and you can tell which. This vault's schema mixes the two: `CLAUDE.md` holds
workflows, and concept pages hold claims, but nothing forbids a concept page from encoding procedure.

**A deterministic linter with pass/fail semantics.** Its checks are dangling cross-references, file-size budgets,
identifier collisions, and dependency cycles — *"not probabilistic. It passes or fails."* This vault's lint pass
has grown ten mechanical checks along the same lines, but as an ad-hoc script rather than a schema-declared
contract, which is why each pass re-derives its own exclusions.

The stated design principle is the same one this schema exists to serve, and worth recording in its author's
words: **"Keep the complexity in text files, not in model weights or opaque embeddings. Every improvement is a
text edit a domain expert can review in 30 seconds."**

## Open questions

- Which metadata fields will become most useful once the number of sources grows?
- When should the schema introduce stronger constraints for tags, aliases, or citation formats?

## Related pages

- [[Persistent Wiki]]
- [[Ingest Query Lint Loop]]
- [[Index and Log]]
- [[Obsidian]]
- [[AI Knowledge Base Overview]]
- [[Andrej Karpathy - LLM Wiki]]
- [[index|Knowledge Base Index]]
- [[Institutional Knowledge Agents]]
- [[Meta - An Organizational Second Brain]]
- [[Meta]]
- [[Retrieval-Augmented Generation]]
- [[Agent Memory]]
