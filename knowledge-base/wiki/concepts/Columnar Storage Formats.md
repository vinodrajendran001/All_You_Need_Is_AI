---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - storage-formats
  - performance
source_ids:
  - src-2026-07-04-vynnytskyi-data-formats
  - src-2026-08-15-vynnytskyi-optimizing-delta-tables
status: active
---

# Columnar Storage Formats

## Definition

**Row-oriented storage** keeps all fields of a record together, suiting complete-record writes and event
ingestion. **Columnar storage** stores values column by column, suiting analytical scans because engines
read only the columns a query needs and compress similar values together.

The working rule from
[[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Data Formats Explained]]:
**"Row format for the write, columnar format for the read."**

## Why it matters

Columnar layout is why analytical cost scales with **columns touched and statistics quality** rather
than with table size. Two mechanisms do the work:

- **Column pruning** — read only the required columns. Illustratively, selecting one column from a
  50-column table reads "about one-fiftieth" of the data.
- **Predicate pushdown** — use filter predicates together with per-file min/max statistics to skip files
  that cannot contain matching rows.

Both are the reason bytes-scanned pricing is tractable at all, and both are **defeated by poor data
layout**: statistics only skip data when values are physically co-located by the columns people actually
filter on. That is the bridge to [[Table Layout Optimization]].

## Current synthesis

### The three formats the vault holds

| Format | Orientation | Internal structure | Fits |
|---|---|---|---|
| **Parquet** | Columnar | Row groups → column chunks → pages, with footer statistics | Analytical scans |
| **ORC** | Columnar | Stripes, indexes, statistics, bloom filters; row index every 10,000 rows by default | Analytical scans, Hive/Hadoop lineage |
| **Avro** | Row-based | Record-at-a-time, schema embedded or registry-managed, schema evolution | Streaming ingestion |

Parquet and ORC are technically **hybrid** — row chunks containing columnar data — which is what lets
them support both file-level skipping and column-level reads. The source attributes Parquet's ecosystem
lead to **momentum rather than technical superiority**, and explicitly declines to call ORC inferior.

Compression is named (Snappy, ZSTD) but **no ratios are supplied**.

### Statistics have a cost and a limit

Statistics are typically collected on a leading subset of columns (32 by default in the vault's source),
so a filter on a column outside that set gets no skipping. Long text columns can add statistics cost
without useful skipping. This makes **column ordering a performance decision**, which is an easy thing
to overlook when designing a table.

### Where the format boundary actually sits

A columnar file format gives efficient reads. It does **not** give transactions, versioning, or
row-level mutation — those come from the layer above, described in [[Open Table Formats]]. Keeping the
two separate is what prevents the common confusion of treating Parquet and Delta as alternatives rather
than as layers.

CSV and JSON remain appropriate for small datasets, interchange, APIs, and human inspection; the source
does not treat columnar as universally correct.

## Open questions

- The vault holds **no measured compression ratios or scan speedups** for these formats. Phrases such as
  "queries fly" and "nothing beats Parquet" in the source are opinion.
- At what table size and query mix does the statistics-collection cost exceed the skipping benefit? The
  32-column default is vendor guidance with no measurement behind it.
- How much of the row-versus-columnar trade is altered by convergence architectures that transcode row
  data into columnar form continuously — see [[Operational Analytical Convergence]]?

## Related pages

- [[Open Table Formats]]
- [[Table Layout Optimization]]
- [[Lakehouse Architecture]]
- [[Operational Analytical Convergence]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Data Formats Explained]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Optimizing Delta Tables]]
- [[Software Performance Engineering]]
