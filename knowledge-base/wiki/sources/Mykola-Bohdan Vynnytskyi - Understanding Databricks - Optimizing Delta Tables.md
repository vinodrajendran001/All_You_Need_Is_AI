---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-08-15-vynnytskyi-optimizing-delta-tables
source_title: "Understanding Databricks: Optimizing Delta Tables"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-optimizing-delta-tables-6065b1388676
tags:
  - source/summary
  - performance
  - data-engineering
  - series/understanding-databricks
source_ids:
  - src-2026-08-15-vynnytskyi-optimizing-delta-tables
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Optimizing Delta Tables

## Summary

Part ten attributes most Delta-table slowdowns to one cause: **"Nine times out of ten, I can tell you
without looking: small files."** Streaming, frequent appends, and rewrites accumulate many small files,
and the per-file overhead of listing, opening, and inspecting them dominates.

The two-axis framing is the keeper: **"Compaction fixes file size. Clustering fixes file contents."**
And the separation of duties: **"OPTIMIZE makes reads fast; VACUUM reclaims space."**

## Key claims

- **Small-file problem:** query overhead from listing, opening, inspecting, and evaluating many files
  before reading data.
- **`OPTIMIZE`** bin-packs small files into larger ones. It **does not delete old files** — `VACUUM`
  does that, after retention.
- **Liquid clustering** co-locates rows by clustering key in a flexible layout that can be changed
  without fixed directory partitions. The author presents it as superseding **Z-ORDER** (the two cannot
  coexist) and as preferable to **partitioning** for new tables.
- **Partitioning** organizes data into directory partitions; it creates too many tiny partitions when
  over-applied and is difficult to change afterwards. The author calls over-partitioning the most common
  self-inflicted performance problem.
- **Data skipping** avoids files whose min/max statistics show they cannot contain matching rows — which
  is why clustering keys should follow **actual filters and joins**, not intuition.
- **Deletion vectors** mark deleted rows via bitmaps without rewriting whole Parquet files. Consequently
  **`DELETE` does not necessarily mean physical erasure**: true erasure requires `DELETE`, then
  `REORG TABLE ... APPLY (PURGE)`, then retention expiry, then `VACUUM`.
- **Predictive optimization** can run OPTIMIZE, VACUUM, and statistics collection automatically — but
  **only on Unity Catalog managed tables**; external tables remain the customer's responsibility.
- Health check: `DESCRIBE DETAIL`, divide `sizeInBytes` by `numFiles` for average file size, then
  inspect `DESCRIBE HISTORY` and statistics.
- **[Product guidance, time-sensitive]** Healthy file size roughly **128 MB to 1 GB**; Databricks targets
  about **256 MB** for tables under **2.5 TB**, scaling to **1 GB** for the largest. Up to **four**
  liquid clustering keys, fewer preferred. Do not partition tables under **1 TB**; partitions should
  generally hold at least **1 GB**; partitioning may still suit **100 TB+** tables or hard operational
  boundaries. Statistics collected by default on the first **32 columns**. `CLUSTER BY AUTO` GA for
  managed tables with predictive optimization; Runtime **18.1** supports one-statement migration from
  partitioning to liquid clustering; Runtime **18** ignores `VACUUM ... RETAIN n HOURS`.

## Why it matters

[[Table Layout Optimization]] enters the vault with a clean separation that generalizes beyond this
platform: **file size** and **file contents** are independent problems with independent remedies, and
confusing them produces the common failure of compacting a table that is actually suffering from poor
row locality.

The deletion-vector erasure sequence is also worth recording for [[Agent Security and Governance]] and
any compliance-adjacent work: in a format where deletes are metadata, **a successful `DELETE` statement
is not a deletion guarantee**, and the physical erasure path has four steps and a waiting period.

## Tensions / open questions

- File-size targets, the 1 TB partitioning threshold, the 32-column statistics default, and the runtime
  version behaviors are **vendor guidance, not measurements**, and the article supplies no benchmark
  showing the resulting speedups.
- Liquid clustering **enables deletion vectors and row tracking and raises the table protocol**, which
  can exclude older clients — a migration cost that is easy to miss.
- Long text columns may add statistics cost without useful skipping.
- "Daily" external-table maintenance is offered as a starting proposal, not a derived schedule.
- The advice to stop manual tuning on managed tables with predictive optimization is opinion and depends
  on the automation behaving well on the table in question.

## Affected pages

- [[Table Layout Optimization]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Columnar Storage Formats]]
- [[Open Table Formats]]

## Raw capture

- [[Understanding Databricks Optimizing Delta Tables]]

## Citations

- Raw capture: [[Understanding Databricks Optimizing Delta Tables]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-optimizing-delta-tables-6065b1388676>
- Published 2026-08-15; captured 2026-10-23.

## Related pages

- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
- [[Software Performance Engineering]]
