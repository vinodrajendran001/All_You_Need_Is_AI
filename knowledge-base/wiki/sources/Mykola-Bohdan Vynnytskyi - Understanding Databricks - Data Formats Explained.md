---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-07-04-vynnytskyi-data-formats
source_title: "Understanding Databricks: Data Formats Explained — Parquet, ORC, Avro, and Delta"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-data-formats-explained-parquet-orc-avro-and-delta-b8b561f6b4ec
tags:
  - source/summary
  - storage-formats
  - lakehouse
  - series/understanding-databricks
source_ids:
  - src-2026-07-04-vynnytskyi-data-formats
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Data Formats Explained

## Summary

Part six draws the distinction the rest of the series depends on: **"Parquet, ORC, and Avro are file
formats. Delta Lake, Iceberg, and Hudi are table formats."** A file format defines how bytes are
arranged inside one file; a table format is a metadata and transaction layer governing many files as one
logical table.

The practical rule: **"Row format for the write, columnar format for the read."**

## Key claims

### File formats

- **Row-oriented storage** keeps all fields of a record together, suiting complete-record writes and
  event ingestion. **Columnar storage** stores values by column, suiting analytical scans because
  engines read only needed columns and compress similar values well.
- **Parquet:** columnar, organized into row groups, column chunks, pages, and footer statistics.
- **ORC:** columnar, associated with Hive/Hadoop, using stripes, indexes, statistics, and bloom filters,
  with a row index **every 10,000 rows by default**.
- **Avro:** row-based, written record at a time, with embedded or registry-managed schemas and schema
  evolution — good for streaming ingestion, poor for analytical scans.
- **Predicate pushdown** uses filter predicates plus file statistics to skip data that cannot match;
  **column pruning** reads only required columns. **[Illustrative]** on a table of "50 columns and a
  billion rows", selecting one column reads "about one-fiftieth".
- The author notes Parquet and ORC are technically **hybrid** — row chunks containing columnar data —
  and attributes Parquet's lead to **ecosystem momentum rather than technical superiority**.
- Compression is named as Snappy and ZSTD. **No measured compression or performance ratios are given.**

### Table formats

- **Delta Lake** is a table format built on Parquet with a **`_delta_log`** transaction log, providing
  **ACID** commits through optimistic concurrency.
- **Time travel** queries prior versions by version or timestamp, retained **7 days by default**.
- **Deletion vectors** record row deletions compactly and apply them at read time, avoiding immediate
  full-file rewrites.
- **UniForm** writes Delta while exposing Iceberg-compatible metadata over the same Parquet files —
  **"no copies, no duplication"**, a product architecture claim.
- Plain Parquet is effectively **immutable**: routine UPDATE, DELETE, and MERGE are not practical
  without a table format on top.
- **[Version-specific]** Delta Lake **4.0 (2025)** added Variant; **4.1 (2026)** introduced
  catalog-managed tables; deletion vectors are GA; **Iceberg v3** added deletion vectors, row lineage,
  and Variant.

## Why it matters

The file-format / table-format split is the single most reusable idea in the series, and it is what
makes [[Open Table Formats]] a coherent concept rather than a vendor label. It also explains the
mechanism behind multi-engine interoperability: because the table format is **metadata over ordinary
Parquet files**, a second engine can read the same bytes given compatible metadata — which is exactly
what UniForm exploits.

For [[Columnar Storage Formats]], the durable mechanics are predicate pushdown and column pruning, which
are the reason analytical cost scales with **columns and statistics quality**, not table size — the same
logic that makes bytes-scanned billing tractable.

## Tensions / open questions

- **No measured numbers at all.** Compression ratios, scan speedups, and ecosystem dominance are
  asserted; phrases such as "queries fly" and "nothing beats Parquet" are opinion.
- The author is careful that ORC is not technically inferior and that CSV and JSON remain appropriate
  for small datasets, interchange, APIs, and inspection.
- UniForm's "no duplication" is a product architecture claim about metadata, not an independently
  verified storage measurement.
- Version and capability details for Delta, Iceberg, and UniForm are explicitly time-sensitive.
- The capture's final FAQ text is slightly truncated.

## Affected pages

- [[Columnar Storage Formats]]
- [[Open Table Formats]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]

## Raw capture

- [[Understanding Databricks Data Formats Explained — Parquet, ORC, Avro, and Delta]]

## Citations

- Raw capture: [[Understanding Databricks Data Formats Explained — Parquet, ORC, Avro, and Delta]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-data-formats-explained-parquet-orc-avro-and-delta-b8b561f6b4ec>
- Published 2026-07-04; captured 2026-10-23.

## Related pages

- [[Lakehouse Architecture]]
- [[Table Layout Optimization]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
