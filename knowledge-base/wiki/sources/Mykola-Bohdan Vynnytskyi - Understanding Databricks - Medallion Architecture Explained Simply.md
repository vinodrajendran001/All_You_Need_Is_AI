---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-06-29-vynnytskyi-medallion-architecture
source_title: "Understanding Databricks: Medallion Architecture Explained Simply"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-medallion-architecture-explained-simply-67085e47c40b
tags:
  - source/summary
  - data-modeling
  - lakehouse
  - series/understanding-databricks
source_ids:
  - src-2026-06-29-vynnytskyi-medallion-architecture
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Medallion Architecture Explained Simply

## Summary

Part five explains the **Bronze / Silver / Gold** progression and immediately defuses the most common
misreading of it: **"The names describe the quality of the data, not the technology behind it."**
Medallion is a recommended practice, not a requirement, and applying it mechanically produces redundant,
context-free layers.

## Key claims

- **Bronze:** raw, append-oriented landing layer preserving source records and ingestion metadata, so it
  can serve as a **replay, audit, and recovery boundary**. **"Bronze is raw and untouched"** — it should
  contain no business logic, and the author argues analysts should not query it.
- **Silver:** cleaned, validated, typed, deduplicated, conformed data that **retains row-level detail**.
  The design rule given is that **"Silver should still have at least one clean, validated row per
  original record."** Silver should be built from Bronze, not directly from ingestion.
- **Gold:** business-oriented, often aggregated and denormalized data for analytics, dashboards, ML, and
  decisions. It should be organized **by business domain**, not multiplied per dashboard.
- **Data-quality expectation:** a declarative rule determining whether invalid rows are retained,
  dropped, or fail the pipeline.
- **Dimensional modeling:** fact tables for events and measures, dimension tables for descriptive
  entities; the star schema is the common form.
- **AUTO CDC** applies change data capture and supports **SCD Type 1** (update in place, no history) and
  **SCD Type 2** (retain versions with effective dates or a current-row flag).
- **Liquid clustering** is recommended in place of traditional partitioning and ZORDER for new tables.
- **Lakeflow mapping:** Bronze as streaming tables, Silver as streaming tables or materialized views,
  Gold as materialized views.
- **[Illustrative]** "A 100 GB source can balloon to 300 GB across three layers" — the storage cost of
  the pattern, stated as an example rather than a measurement.
- **[Product-specific]** Liquid clustering recommended for all new tables and most tables under a
  terabyte; predictive optimization automatically runs OPTIMIZE and VACUUM and is on by default for
  newer accounts; LTAP announced June 2026 as supporting real-time querying on a single copy.

## Why it matters

[[Medallion Architecture]] enters the vault here, and the framing worth keeping is **not** the three
names but the **three distinct responsibilities**: an immutable recovery boundary, a trusted detailed
layer, and a consumption layer shaped by business meaning.

That maps unexpectedly well onto this vault's own [[Schema-Driven Knowledge Base]] practice — raw
captures are immutable Bronze, source summaries are validated row-level Silver, and concept and
synthesis pages are domain-shaped Gold. The parallel is structural, not borrowed from the source.

It also explains why [[Text-to-SQL Agents]] are usually pointed at Gold: a natural-language interface
over Bronze inherits every source inconsistency the Silver layer exists to remove.

## Tensions / open questions

- The author is explicit that Medallion is **"a recommended best practice but not a requirement"**, that
  three layers can be over-engineering, and that **two layers — Raw and Curated — may be sufficient**
  for small, clean, or latency-sensitive data.
- The storage, latency, and processing cost of three layers is real; the 100 GB → 300 GB figure is an
  illustration, and the vault holds no measured multiplier.
- LTAP may reduce physical copies and freshness lag, but the author says it **does not eliminate the
  logical progression** from raw to clean to business-ready.
- Several specific recommendations — Bronze should use loose types, analysts should never query Bronze,
  liquid clustering should replace partitioning — are **opinion**, and the clustering and predictive
  optimization guidance is product-dependent and dated to 2026.

## Affected pages

- [[Medallion Architecture]]
- [[Slowly Changing Dimensions]]
- [[Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]

## Raw capture

- [[Understanding Databricks Medallion Architecture Explained Simply]]

## Citations

- Raw capture: [[Understanding Databricks Medallion Architecture Explained Simply]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-medallion-architecture-explained-simply-67085e47c40b>
- Published 2026-06-29; captured 2026-10-23.

## Related pages

- [[Lakehouse Architecture]]
- [[Open Table Formats]]
- [[Table Layout Optimization]]
- [[Text-to-SQL Agents]]
- [[Schema-Driven Knowledge Base]]
