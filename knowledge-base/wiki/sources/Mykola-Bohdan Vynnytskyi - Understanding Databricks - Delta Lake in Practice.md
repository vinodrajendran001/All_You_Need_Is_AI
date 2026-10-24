---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-07-11-vynnytskyi-delta-lake-practice
source_title: "Understanding Databricks: Delta Lake in Practice — Create, Append, and Merge"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-delta-lake-in-practice-create-append-and-merge-18b58f8f50c9
tags:
  - source/summary
  - storage-formats
  - data-engineering
  - series/understanding-databricks
source_ids:
  - src-2026-07-11-vynnytskyi-delta-lake-practice
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice

## Summary

Part seven is the code-first companion to the formats article: managed versus external tables, append
versus overwrite, atomic `replaceWhere`, `MERGE`, schema enforcement and evolution, time travel, and
maintenance.

The operational core is three write modes for three situations — **append for incremental loads,
overwrite only for full refreshes, `MERGE` for synchronization** — plus one non-negotiable precondition:
**"Always deduplicate your source first."**

## Key claims

- **Managed table:** the catalog controls storage; dropping the table removes the data after the
  recovery period. **External table:** metadata points at user-managed storage; dropping removes
  metadata but leaves files.
- **Append** adds rows without modifying existing ones. **Overwrite** replaces all table data — the
  author warns it can silently wipe a production table through a one-word mistake.
- **`replaceWhere`** atomically replaces only rows matching a predicate, which is the safer middle path
  for **idempotent reprocessing of a bounded slice**.
- **`MERGE`** is the upsert workhorse, supporting matched updates and deletes plus unmatched inserts.
  The durable pattern:

  ```sql
  MERGE INTO target
  USING source
  ON target.id = source.id
  WHEN MATCHED THEN UPDATE SET ...
  WHEN NOT MATCHED THEN INSERT ...
  ```

  Source data must first be reduced to **one latest row per key**, typically with `row_number()`.
  **MERGE fails if multiple source rows match the same target row.**
- **Schema enforcement** rejects incompatible writes; **schema evolution** deliberately changes the
  schema via `mergeSchema` or `WITH SCHEMA EVOLUTION`. The author prefers **per-write** evolution over
  session-wide automatic evolution, to limit unintended schema drift.
- **Type widening** safely broadens a column type, such as INT to BIGINT, without rewriting data.
- **Deletion vectors** record row deletions as metadata applied at read; physical files remain until
  cleanup, so delete performance improves but storage reclamation is deferred.
- **Time travel** reads a prior version with `VERSION AS OF` or `TIMESTAMP AS OF`, **bounded by VACUUM
  retention — 7 days by default**.
- **`OPTIMIZE`** compacts small files; **`VACUUM`** removes obsolete files after retention.
- **[Product-specific]** Code targets Delta Lake 4.x / Runtime 18; every table on Databricks is a Delta
  table by default; predictive optimization runs OPTIMIZE, VACUUM, and clustering automatically but
  **only on managed tables**; liquid clustering is recommended instead of partitioning for new tables;
  type widening is "now generally available".

## Why it matters

This supplies [[Open Table Formats]] with the operational semantics that make ACID on object storage
actually usable, and it names the failure modes that distinguish a table format from a directory of
Parquet: **non-idempotent reprocessing**, **duplicate source keys breaking MERGE**, and **schema drift
arriving silently through automatic evolution**.

The `replaceWhere` pattern is the one most worth generalizing. Reprocessing a date slice is the routine
operation in any medallion pipeline, and doing it with overwrite is destructive while doing it with
delete-then-insert is non-atomic.

## Tensions / open questions

- Characterizations of managed tables as **"cheaper, faster"** and of deletion-vector performance gains
  are **asserted without measurement**.
- Predictive optimization coverage is limited to managed tables, so external-table users retain manual
  maintenance duty — a cost the article does not quantify.
- Time travel is bounded by VACUUM retention, so the recovery window is a configuration decision rather
  than a guarantee.
- Product defaults, runtime versions, and maintenance behavior are explicitly time-sensitive.
- The recommendations (prefer managed tables, default to append, per-write schema evolution, liquid
  clustering, deduplicate every change feed) are opinion, though the MERGE deduplication rule follows
  from the documented matching semantics.

## Affected pages

- [[Open Table Formats]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Table Layout Optimization]]

## Raw capture

- [[Understanding Databricks Delta Lake in Practice — Create, Append, and Merge]]

## Citations

- Raw capture: [[Understanding Databricks Delta Lake in Practice — Create, Append, and Merge]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-delta-lake-in-practice-create-append-and-merge-18b58f8f50c9>
- Published 2026-07-11; captured 2026-10-23.

## Related pages

- [[Slowly Changing Dimensions]]
- [[Medallion Architecture]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Data Formats Explained]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
