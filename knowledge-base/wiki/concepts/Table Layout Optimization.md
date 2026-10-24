---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - performance
  - data-engineering
  - storage-formats
source_ids:
  - src-2026-08-15-vynnytskyi-optimizing-delta-tables
  - src-2026-07-11-vynnytskyi-delta-lake-practice
  - src-2026-08-08-vynnytskyi-delta-time-travel
status: active
---

# Table Layout Optimization

## Definition

The practice of controlling **how many files a table has and how rows are distributed across them**, so
that query engines can skip work. Two independent axes, from
[[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Optimizing Delta Tables]]:

> **"Compaction fixes file size. Clustering fixes file contents."**

And a matching division of maintenance duties: **"OPTIMIZE makes reads fast; VACUUM reclaims space."**

## Why it matters

Confusing the two axes produces the most common wasted effort in this area — compacting a table that is
actually suffering from poor row locality, or re-clustering a table whose real problem is ten thousand
tiny files.

The **small-file problem** dominates real slowdowns: streaming, frequent appends, and rewrites
accumulate many small files, and the per-file overhead of listing, opening, and inspecting them exceeds
the cost of reading the data. The source's blunt version: **"Nine times out of ten, I can tell you
without looking: small files."**

Clustering is the other half. The statistics that drive predicate pushdown (see
[[Columnar Storage Formats]]) only skip files when values are physically co-located, so **clustering
keys should follow actual filters and joins**, not intuition about what seems important.

## Current synthesis

### The health check is two numbers

Divide table size by file count for an average file size, then inspect commit history and statistics.
A table whose average file is a few megabytes has a layout problem regardless of what its query plan
says.

### Clustering versus partitioning

**Partitioning** organizes data into directory partitions. It is hard to change afterwards, and
**over-partitioning is the most common self-inflicted performance problem**: too many tiny partitions
reintroduce the small-file problem at directory granularity.

**Liquid clustering** co-locates rows by clustering key in a flexible layout that can be changed later
without fixed directories. The vault's source presents it as superseding Z-ORDER (the two cannot
coexist) and as preferable to partitioning for new tables — with a migration cost worth flagging:
enabling it **raises the table protocol version** and turns on deletion vectors and row tracking, which
can exclude older clients.

### Deletion is layout work too

Deletion vectors mark deleted rows via bitmaps without rewriting whole files, so delete operations get
fast while **storage reclamation is deferred**. The erasure path is therefore four steps —
`DELETE`, purge reorganization, retention expiry, `VACUUM` — a point carried in detail by
[[Open Table Formats]] and relevant to any compliance obligation.

### Maintenance can be automated, but not everywhere

Predictive optimization can run compaction, vacuuming, and statistics collection automatically, but in
the vault's source **only for catalog-managed tables**. External tables remain the owner's
responsibility, and the source's "daily maintenance" suggestion is a starting proposal rather than a
derived schedule.

### Layout and recovery are coupled

Aggressive vacuuming improves storage cost and conflicts directly with the time-travel window described
in [[Open Table Formats]]: the retention setting that reclaims space is the same setting that bounds how
far back the table can be queried or restored.

## Open questions

- **Every target figure in the vault is vendor guidance, not measurement**: healthy file sizes of roughly
  128 MB–1 GB, a ~256 MB target below 2.5 TB scaling to 1 GB, "don't partition below 1 TB", partitions
  of at least 1 GB, statistics on the first 32 columns, at most four clustering keys. No benchmark
  accompanies any of them.
- No source in the vault measures the speedup from compaction or clustering, so the **size of the
  benefit is unknown** even though the mechanism is clear.
- When does automated optimization misjudge a table, and what signal reveals it? The advice to stop
  manual tuning assumes the automation behaves well.
- Long text columns can consume statistics budget without yielding skipping — how should column order be
  chosen when query patterns are not yet known?

## Related pages

- [[Open Table Formats]]
- [[Columnar Storage Formats]]
- [[Lakehouse Architecture]]
- [[Medallion Architecture]]
- [[Software Performance Engineering]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Optimizing Delta Tables]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
