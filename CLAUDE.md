# Workspace Knowledge Base Schema

This workspace contains a persistent Obsidian-friendly knowledge base rooted at `knowledge-base/`.
Treat it as an LLM-maintained wiki for AI, LLMs, agents, and adjacent topics.

## Non-negotiable rules

- Keep all knowledge-base artifacts inside `knowledge-base/` and this root `CLAUDE.md`.
- Treat files in `knowledge-base/raw/sources/` as immutable after capture unless a user explicitly asks to correct metadata or replace a bad capture.
- On every ingest, update the raw source capture if needed, the source summary page, all materially affected concept/entity/overview/synthesis pages, `knowledge-base/wiki/index.md`, and `knowledge-base/wiki/log.md`.
- Use Obsidian wikilinks for vault-internal references.
- Prefer updating existing pages over creating near-duplicate notes.
- Preserve contradictions and uncertainty; do not erase older claims without recording what changed.
- Keep source-backed facts tied to a source page or raw capture.
- Do not modify unrelated workspace content unless the task explicitly requires it.

## Directory map

- `knowledge-base/raw/inbox/` - drop zone for newly collected sources before formal ingest
- `knowledge-base/raw/sources/` - immutable captured source notes
- `knowledge-base/raw/assets/` - locally stored attachments referenced by raw sources
- `knowledge-base/wiki/index.md` - content-oriented catalog; read this first during queries
- `knowledge-base/wiki/log.md` - append-only chronological record of ingests, queries, and lint passes
- `knowledge-base/wiki/overviews/` - high-level orientation pages
- `knowledge-base/wiki/sources/` - one wiki page per ingested source
- `knowledge-base/wiki/concepts/` - durable concept pages maintained across sources
- `knowledge-base/wiki/entities/` - people, orgs, tools, models, datasets, and other named things
- `knowledge-base/wiki/syntheses/` - multi-source theses, comparisons, and durable analyses
- `knowledge-base/wiki/queries/` - filed answers worth keeping beyond chat
- `knowledge-base/wiki/lint/` - wiki health-check reports
- `knowledge-base/templates/` - templates for all recurring page types

## Naming conventions

- Raw source captures: `YYYY-MM-DD Author - Title.md`
- Source summary pages: `Author - Title.md` when disambiguation helps, otherwise `Title.md`
- Concept pages: singular noun phrase, e.g. `Persistent Wiki.md`
- Entity pages: canonical proper noun, e.g. `Andrej Karpathy.md`
- Query outputs: `YYYY-MM-DD Short Question.md`
- Lint reports: `YYYY-MM-DD Lint Pass.md`

## Frontmatter schema

Use these common fields wherever they make sense:

```yaml
type:
created:
updated:
tags: []
source_ids: []
status: active
```

Type-specific expectations:

- `raw-source`: `source_id`, `title`, `author`, `url`, `captured`
- `source-summary`: `source_id`, `source_title`, `source_author`, `source_url`
- `entity`: `entity_kind`
- `query`: `question`
- `lint-report`: `scope`

## Workflows

### Ingest

1. Save the source under `knowledge-base/raw/sources/` if it is not already captured.
2. Read the raw source and the relevant pages surfaced by `knowledge-base/wiki/index.md`.
3. Create or update the source summary page in `knowledge-base/wiki/sources/`.
4. Update every affected concept, entity, overview, or synthesis page.
5. Update `knowledge-base/wiki/index.md`.
6. Append a new entry to `knowledge-base/wiki/log.md` using the exact heading format `## [YYYY-MM-DD] ingest | Title`.

### Query

1. Read `knowledge-base/wiki/index.md` first.
2. Follow links into the most relevant wiki pages before consulting raw sources.
3. Answer with citations to the source summary pages and raw captures when needed.
4. If the answer is durable, file it under `knowledge-base/wiki/queries/` or `knowledge-base/wiki/syntheses/`.
5. Update the index and append a log entry.

### Lint

1. Look for orphan pages, stale claims, contradictions, missing cross-links, thin summaries, and gaps worth researching.
2. Record findings in `knowledge-base/wiki/lint/`.
3. Fix what can be fixed immediately.
4. Update the index if new pages were created and append a log entry.

## Page expectations

- Source pages summarize a source, extract durable claims, list affected pages, and point back to the raw capture.
- Concept pages synthesize across sources; they should not simply restate one source.
- Entity pages explain why the named thing matters to this vault.
- Overview pages orient the reader quickly and link outward to the most important pages.
- Every substantive wiki page should end with a `## Related pages` section.

## Current focus

The current domain is AI, especially LLMs, agents, tooling, and learning workflows. Existing notes elsewhere in the workspace are background material, but this knowledge base should stay self-consistent and maintain its own index, log, and page graph.
