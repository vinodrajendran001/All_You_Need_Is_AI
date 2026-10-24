---
type: entity
created: 2026-10-23
updated: 2026-10-23
entity_kind: person
tags:
  - entity
  - data-engineering
  - lakehouse
source_ids:
  - src-2026-05-23-vynnytskyi-databricks-snowflake-bigquery
  - src-2026-06-01-vynnytskyi-databricks-core-components
  - src-2026-06-14-vynnytskyi-databricks-cloud-choice
  - src-2026-06-21-vynnytskyi-modern-data-platform
  - src-2026-06-29-vynnytskyi-medallion-architecture
  - src-2026-07-04-vynnytskyi-data-formats
  - src-2026-07-11-vynnytskyi-delta-lake-practice
  - src-2026-08-01-vynnytskyi-scd-types
  - src-2026-08-08-vynnytskyi-delta-time-travel
  - src-2026-08-15-vynnytskyi-optimizing-delta-tables
  - src-2026-08-23-vynnytskyi-genie-explained
  - src-2026-08-30-vynnytskyi-lakebase-ltap
  - src-2026-10-18-vynnytskyi-databricks-project-structure
status: active
---

# Mykola-Bohdan Vynnytskyi

## What it is

Author of the thirteen-part **"Understanding Databricks"** series published on Medium between May and
October 2026 — the vault's single largest body of data-platform material and the source of ten of its
lakehouse-related pages.

## Why it matters here

The series is the vault's **bridge between AI systems and the data platforms underneath them**. Most
agent material in this vault treats data as given; this series describes how the data gets to be the way
it is, which turns out to explain several agent behaviours — why [[Text-to-SQL Agents]] are scoped to
curated layers, why catalog permissions can serve as an agent capability boundary, and why notebook-
heavy codebases are opaque to coding agents.

It also supplies concepts that transfer well beyond their platform:

- **File formats versus table formats** — the distinction that makes [[Open Table Formats]] coherent.
- **"Compaction fixes file size. Clustering fixes file contents."** — two independent axes in
  [[Table Layout Optimization]].
- **"History visibility and queryability are two different windows."**
- **"You can always ignore history, but you cannot recover what you never kept."** — the retention
  asymmetry in [[Slowly Changing Dimensions]].
- **"The names describe the quality of the data, not the technology behind it."** — the correction at
  the centre of [[Medallion Architecture]].

## Notes

### Evidence discipline — a mixed but improving picture

The series' strongest property for this vault is that **the author consistently separates his own
opinion from the vendor's claims**, and flags both. He tells readers to take the Genie benchmark "with
a grain of salt", calls the convergence architecture early and unproven, names the renaming churn a
"self-inflicted wound", and repeatedly marks guidance as 2026-specific.

Its weakest property is that **it contains almost no measurements of its own**. Compression ratios,
clustering speedups, file-size targets, cost multipliers, and throughput figures are reproduced from
vendor guidance. The exceptions are small and clearly scoped — a deployment producing
`0 created, 0 changed, 0 deleted, 2 unchanged`, a 22-file first commit, two materialized views of 22K
and 128 rows taking three seconds each — and are demonstrations rather than benchmarks.

The vault therefore treats this series as **authoritative on mechanism and unverified on magnitude**.

### Opinions worth labelling as opinions

Loose types in Bronze; analysts never querying Bronze; liquid clustering replacing partitioning for all
new tables; serverless as the default; Type 2 dimensions "when in doubt"; `%run` chains categorically
discouraged; the official project template as the settled 2026 answer. Each is reasonable and none is
established by evidence presented in the series.

## Related pages

- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Lakehouse Architecture]]
- [[Open Table Formats]]
- [[Columnar Storage Formats]]
- [[Medallion Architecture]]
- [[Slowly Changing Dimensions]]
- [[Table Layout Optimization]]
- [[Operational Analytical Convergence]]
- [[Text-to-SQL Agents]]
- [[Declarative Data Pipeline Deployment]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Honest Comparison with Snowflake and BigQuery]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Core Components]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Azure vs AWS vs GCP]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - What a Modern Data Platform Looks Like in 2026]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Medallion Architecture Explained Simply]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Data Formats Explained]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - SCD Type 1 and Type 2 in Delta Lake]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Optimizing Delta Tables]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Lakebase and LTAP]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - How to Structure a Databricks Project from Scratch]]
