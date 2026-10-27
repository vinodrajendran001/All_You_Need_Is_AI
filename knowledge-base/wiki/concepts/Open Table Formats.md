---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - storage-formats
  - lakehouse
  - data-engineering
source_ids:
  - src-2026-07-04-vynnytskyi-data-formats
  - src-2026-07-11-vynnytskyi-delta-lake-practice
  - src-2026-08-08-vynnytskyi-delta-time-travel
  - src-2026-08-15-vynnytskyi-optimizing-delta-tables
status: active
---

# Open Table Formats

## Definition

An **open table format** is a **metadata and transaction layer** that governs many ordinary data files
as one logical table. The distinction that makes the category coherent, from
[[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Data Formats Explained]]:

> **"Parquet, ORC, and Avro are file formats. Delta Lake, Iceberg, and Hudi are table formats."**

A file format defines how bytes are arranged inside one file. A table format adds a transaction log,
giving ACID commits, schema enforcement, versioning, and row-level mutation over files that remain
readable as plain Parquet.

## Why it matters

This is the mechanism behind multi-engine interoperability, and it explains why "open" is a meaningful
claim rather than marketing. Because the table layer is **metadata over ordinary files**, a second
engine can read the same bytes given compatible metadata — which is exactly what format-translation
features exploit when they write one format while exposing another's metadata over the same Parquet.

Plain Parquet is effectively **immutable**: routine `UPDATE`, `DELETE`, and `MERGE` are not practical
without a table format on top. Everything a lakehouse claims over a data lake — see
[[Lakehouse Architecture]] — is supplied by this layer.

## Current synthesis

### What the transaction log buys

Each write records added and removed files in a numbered commit against a transaction log, using
optimistic concurrency. Three consequences follow:

- **Logical deletion is not physical deletion.** Files are removed from current table state while
  remaining on disk, which is what makes time travel possible at all.
- **Time travel** queries an earlier version by version number or timestamp, bounded by file retention.
- **Deletion vectors** record deleted rows compactly and apply them at read time, avoiding immediate
  full-file rewrites.

### Two retention windows, not one

The sharpest operational distinction the vault holds here:
**"History visibility and queryability are two different windows."** File retention and log retention
are independent settings, so a history entry can remain **visible** after its data files have been
vacuumed and is no longer **queryable**. Any recovery plan built on time travel is in fact a plan built
on a retention setting.

### Operational semantics that make ACID usable

From [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice]]:

- **Append** for incremental loads; **overwrite** only for full refreshes; **`MERGE`** for
  synchronization. Overwrite can silently destroy a production table through a one-word mistake.
- **`replaceWhere`** atomically replaces only rows matching a predicate — the safe middle path for
  **idempotent reprocessing of a bounded slice**, which is the routine operation in any layered
  pipeline. Doing it with overwrite is destructive; doing it with delete-then-insert is non-atomic.
- **Source data must be deduplicated to one latest row per key before `MERGE`.** MERGE fails when
  multiple source rows match the same target row — the limitation that also forces the two-copy union
  workaround in [[Slowly Changing Dimensions]].
- **Schema enforcement** rejects incompatible writes; **schema evolution** changes the schema
  deliberately. Per-write evolution is preferred over session-wide automatic evolution, which lets drift
  arrive silently.
- **Type widening** broadens a column type without rewriting data.

### Deletion is a four-step operation

Because deletes are metadata, **a successful `DELETE` statement is not an erasure guarantee**. Physical
erasure requires `DELETE`, then a purge reorganization, then retention expiry, then `VACUUM` — a detail
that matters for any compliance or right-to-erasure obligation, and for
[[Agent Security and Governance]] wherever an agent is trusted to delete.

### Clone semantics

A **shallow clone** copies metadata and references the source's files, so it breaks once those files are
vacuumed — a failure that surfaces only later. A **deep clone** copies data independently and is the
only form that functions as a point-in-time backup.

## Open questions

- The vault's sources for this concept contain **no measured numbers**: no compression ratios, no scan
  speedups, no verified interoperability overhead. Claims like "no duplication" under format translation
  are product architecture statements about metadata, not measurements.
- Format version and capability details are explicitly time-sensitive; the **durable material is the
  file/table split, the transaction log, and the two-window retention model**, not version numbers.
- Ecosystem dominance of one file format is attributed by the source to **momentum rather than technical
  superiority** — a claim the vault cannot verify.
- How much of the openness survives in practice when the optimization, governance, and automation layers
  above the format remain proprietary?

## Related pages

- [[Columnar Storage Formats]]
- [[Lakehouse Architecture]]
- [[Table Layout Optimization]]
- [[Slowly Changing Dimensions]]
- [[Medallion Architecture]]
- [[Agent Security and Governance]]
- [[Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Data Formats Explained]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Optimizing Delta Tables]]
