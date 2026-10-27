---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-08-08-vynnytskyi-delta-time-travel
source_title: "Understanding Databricks: Time Travel in Delta Lake"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-time-travel-in-delta-lake-42e45b34de83
tags:
  - source/summary
  - storage-formats
  - data-engineering
  - series/understanding-databricks
source_ids:
  - src-2026-08-08-vynnytskyi-delta-time-travel
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake

## Summary

Part nine: **"Every write creates a new version of the table."** Time travel reads the Parquet files
that were live at an earlier version or timestamp, `DESCRIBE HISTORY` exposes the audit trail, and
`RESTORE` creates a *new* version matching an old one rather than rewriting history.

The warning the article is built around: **"Time travel is a seatbelt, not insurance."** It is not a
backup, because it shares the table's storage and retention lifecycle.

## Key claims

- A Delta table is Parquet data files plus a **`_delta_log`**; each write records added and removed
  files in a numbered commit. **Logical deletion removes files from current table state without
  immediately deleting the physical files** — which is what makes time travel possible at all.
- **`DESCRIBE HISTORY`** reports versions, timestamps, users, operations, parameters, and metrics.
- **`RESTORE`** creates a new commit whose contents match an earlier version; it does not erase history.
- **`VACUUM`** deletes unreferenced files after retention, reclaiming storage but **limiting historical
  queryability**.
- The sharpest distinction in the article: **"History visibility and queryability are two different
  windows."** File retention and log retention are separate settings, so a history entry can remain
  visible after its data files are gone.
- **Change Data Feed (CDF)** returns changed rows between versions with change type and commit metadata
  — not a full snapshot — and **must be enabled before the relevant changes**, whereas time travel works
  retroactively within retention.
- **Shallow clone** copies metadata and references the source's files, so it breaks once those files are
  vacuumed. **Deep clone** copies data independently and can serve as a point-in-time backup.
- **[Product defaults, time-sensitive]** `delta.deletedFileRetentionDuration` defaults to **7 days**;
  `delta.logRetentionDuration` to **30 days**. On Runtime **18**, time travel beyond file retention is
  hard-blocked and `VACUUM ... RETAIN n HOURS` is ignored except `RETAIN 0 HOURS`.

## Why it matters

This gives [[Open Table Formats]] the recovery semantics that distinguish an ACID table from a
versioned directory, and it names a trap worth recording: a visible `DESCRIBE HISTORY` entry can
**look** recoverable while being unqueryable, because two independent retention windows govern metadata
and data.

The clone distinction is the practical takeaway. Shallow clones are cheap test fixtures with a hidden
dependency on the source's retention; **only a deep clone is an independent artifact**. Any recovery
plan built on time travel is really a plan built on a VACUUM retention setting.

## Tensions / open questions

- The author is explicit that **aggressive `VACUUM` can permanently remove versions needed for
  recovery**, and that treating time travel as backup is a mistake.
- Shallow clones can fail after source files are vacuumed — a failure mode that appears only later.
- Retention defaults, Runtime 18's hard block, and `VACUUM` option handling are product-specific and
  likely to change; the durable part is the two-window model, not the day counts.
- Setting retention deliberately for audit and compliance needs is the author's recommendation, not a
  measured policy; longer retention trades storage cost against recoverability and the article does not
  quantify that trade.

## Affected pages

- [[Open Table Formats]]
- [[Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Table Layout Optimization]]

## Raw capture

- [[Understanding Databricks Time Travel in Delta Lake]]

## Citations

- Raw capture: [[Understanding Databricks Time Travel in Delta Lake]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-time-travel-in-delta-lake-42e45b34de83>
- Published 2026-08-08; captured 2026-10-23.

## Related pages

- [[Slowly Changing Dimensions]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Optimizing Delta Tables]]
