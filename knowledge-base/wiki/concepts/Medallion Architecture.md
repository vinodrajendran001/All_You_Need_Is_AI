---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - data-modeling
  - lakehouse
  - data-quality
source_ids:
  - src-2026-06-29-vynnytskyi-medallion-architecture
status: active
---

# Medallion Architecture

## Definition

A layered data-refinement pattern — **Bronze → Silver → Gold** — in which data becomes progressively
more trustworthy and more business-shaped at each stage. The canonical correction from
[[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Medallion Architecture Explained Simply]]:
**"The names describe the quality of the data, not the technology behind it."**

## Why it matters

The three names are the least interesting part. What transfers is the **three distinct
responsibilities**, each of which fails differently if collapsed into another:

1. **Bronze is a recovery boundary.** Raw, append-oriented, preserving source records and ingestion
   metadata so that any downstream mistake can be replayed and audited. It holds no business logic.
2. **Silver is the trusted detailed layer.** Cleaned, validated, typed, deduplicated, conformed — and
   critically it **retains row-level detail**: "at least one clean, validated row per original record."
3. **Gold is shaped by business meaning.** Aggregated, denormalized, organized **by domain** rather than
   one table per dashboard.

Collapsing Bronze into Silver destroys replayability. Aggregating in Silver destroys the ability to ask
new questions. Multiplying Gold per dashboard produces the sprawl the pattern was meant to prevent.

## Current synthesis

### The same shape appears in this vault's own workflow

The parallel is structural rather than borrowed: `knowledge-base/raw/sources/` is an immutable Bronze
layer; source summaries are the validated, one-per-source Silver layer; concept, entity, and synthesis
pages are the domain-shaped Gold layer. The [[Schema-Driven Knowledge Base]] discipline of never
rewriting raw captures is exactly the Bronze recovery-boundary rule, and the rule that every claim trace
back to a `source_id` is the row-level-detail rule.

This is a useful cross-check: a knowledge pipeline that mutates its raw layer loses the same property a
data pipeline does.

### Why consumption layers point at Gold

[[Text-to-SQL Agents]] are normally scoped to Gold tables, and the reason is mechanical rather than
stylistic. A natural-language interface over Bronze inherits every source inconsistency, duplicate, and
untyped column that Silver exists to remove — so the model is asked to resolve, at query time and
without evidence, ambiguity the pipeline was built to resolve once. Curation is the accuracy lever.

### Mechanisms the sources attach to the layers

- **Expectations** — declarative data-quality rules that retain, drop, or fail on invalid rows, making
  quality a pipeline artifact rather than a downstream discovery.
- **Dimensional modeling** — fact tables for events and measures, dimension tables for descriptive
  entities, commonly a star schema. History retention in dimensions is governed by
  [[Slowly Changing Dimensions]].
- **Change data capture** applied declaratively, supporting Type 1 and Type 2 dimension handling.
- **Streaming tables and materialized views** as the respective implementation defaults for the layers
  — product-specific guidance, dated 2026.

## Open questions

- The author is explicit that Medallion is **"a recommended best practice but not a requirement"**, that
  three layers can be over-engineering, and that **two layers — Raw and Curated — may suffice** for
  small, clean, or latency-sensitive data. The vault should not treat three layers as a default.
- **The cost is real and unmeasured.** The only figure available is illustrative — "a 100 GB source can
  balloon to 300 GB across three layers" — and there is no measured multiplier, latency cost, or
  processing cost in the vault.
- Convergence architectures may reduce physical copies and freshness lag, but the source argues they do
  **not** eliminate the logical progression from raw to clean to business-ready. Whether that holds in
  practice is untested here.
- Several attached recommendations — loose types in Bronze, analysts never querying Bronze, clustering
  instead of partitioning — are **opinion** and product-dependent.

## Related pages

- [[Lakehouse Architecture]]
- [[Slowly Changing Dimensions]]
- [[Open Table Formats]]
- [[Table Layout Optimization]]
- [[Text-to-SQL Agents]]
- [[Declarative Data Pipeline Deployment]]
- [[Schema-Driven Knowledge Base]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Medallion Architecture Explained Simply]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - What a Modern Data Platform Looks Like in 2026]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - How to Structure a Databricks Project from Scratch]]
