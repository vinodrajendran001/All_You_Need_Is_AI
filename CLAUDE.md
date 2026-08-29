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
- `knowledge-base/wiki/posts/` - LinkedIn post drafts derived from the vault, plus the post archive
- `knowledge-base/wiki/lint/` - wiki health-check reports
- `knowledge-base/templates/` - templates for all recurring page types

## Naming conventions

- Raw source captures: `YYYY-MM-DD Author - Title.md`
- Source summary pages: `Author - Title.md` when disambiguation helps, otherwise `Title.md`
- Concept pages: singular noun phrase, e.g. `Persistent Wiki.md`
- Entity pages: canonical proper noun, e.g. `Andrej Karpathy.md`
- Query outputs: `YYYY-MM-DD Short Question.md`
- Post drafts: `YYYY-MM-DD Post Slug.md`, dated by the day the post is drafted
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
- `linkedin-post`: `pages_used`, `topics`, `covers_from`, `covers_through`; `status` runs `draft` -> `ready` -> `published`
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
4. If the answer is durable, newly generated query pages may be filed under `knowledge-base/wiki/queries/`, which is local-only and ignored by Git.
5. Do not add local-only query pages, their titles, or their contents to tracked index, log, overview, concept, entity, or synthesis pages unless the user explicitly asks to publish them.
6. Existing tracked query pages may remain indexed and maintained normally.

### Post

Weekly LinkedIn post drafted from the most recent ingests. Output is a paste-ready draft; nothing is published
automatically. The vault changes often, so every run recomputes its own window and its own anti-repeat state —
never assume a fixed cadence or a hardcoded date.

1. **Orient.** Read `knowledge-base/wiki/posts/Post Archive.md` first: the posts table, the topics covered, and
   the spine pages still in cooldown.
2. **Compute the window.** `covers_from` is the `covers_through` date of the newest post in `wiki/posts/`; if there
   are no posts yet, use 7 days before today. `covers_through` is today. Because the start is anchored to the last
   post rather than to a calendar week, skipped weeks are still covered on the next run.
3. **Collect what changed.** Take every `## [YYYY-MM-DD] ingest | Title` heading in `wiki/log.md` inside the window,
   then cross-check with `git log --since=<covers_from> --name-only -- knowledge-base/wiki` for pages that changed
   without a log entry. The log entries are the primary signal because they already record why each source mattered.
4. **Shortlist 3-5 angles and score each 1-5** on **surprise** (does it overturn something a competent reader
   believes — weigh this highest), **concreteness** (is there a number, benchmark, or named mechanism to anchor it),
   **reach** (does it land for practitioners and for interested non-specialists), and **freshness** (not already in
   the archive's topics, spine page not in cooldown). Prefer angles the vault *derived* across sources over facts a
   single source stated; "Company X released model Y" is not a post.
5. **Draft** from `knowledge-base/templates/linkedin-post.md` into `knowledge-base/wiki/posts/`, following the
   anatomy and voice rules in that template. Record the shortlist and scores under `## Why this topic`.
6. **Fact-check before marking `ready`.** Trace every factual sentence to a page in `pages_used`, match every number
   to the vault verbatim, match every attribution to the source summary's `source_author`, and hedge in the post body
   anything the vault records as uncertain, self-reported, unablated, or contradicted. Cut unverifiable claims rather
   than softening them, and record what was cut.
7. **File.** Update the archive's posts table, topics covered, and cooldown list, then append a log entry using the
   heading format `## [YYYY-MM-DD] post | Title`.

Posts are derived output, not evidence: they declare no `source_id`s, they are never cited by concept, entity, or
synthesis pages, and they do not participate in source-ID parity or traceability checks. Attribution lives in
`pages_used` and the draft's `## Attribution` section. Draw only on tracked pages — `wiki/queries/` is local-only
and must not reach a public post.

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
- Post pages are derived public-facing output; they cite the vault but the vault never cites them.
- Every substantive wiki page should end with a `## Related pages` section.

## Current focus

The current domain is AI, especially LLMs, agents, tooling, and learning workflows. Existing notes elsewhere in the workspace are background material, but this knowledge base should stay self-consistent and maintain its own index, log, and page graph.
