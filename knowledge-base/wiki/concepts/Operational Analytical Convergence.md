---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - lakehouse
  - databases
  - architecture
source_ids:
  - src-2026-08-30-vynnytskyi-lakebase-ltap
  - src-2026-06-21-vynnytskyi-modern-data-platform
status: active
---

# Operational Analytical Convergence

## Definition

The attempt to serve **transactional (OLTP)** and **analytical (OLAP)** workloads from one logical copy
of data, rather than maintaining an operational database, an analytical store, and a change-data-capture
pipeline synchronizing them.

Two distinct strategies appear in this vault:

- **HTAP** — make **one engine** serve both workloads.
- **LTAP** — keep two purpose-built engines and converge the **storage layer** beneath them. From
  [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Lakebase and LTAP]]:
  **"LTAP keeps two purpose-built engines and instead unifies the storage."**

## Why it matters

The access patterns are genuinely incompatible: OLTP wants many small row-oriented reads and writes;
OLAP wants large columnar scans and aggregations (see [[Columnar Storage Formats]]). The single-engine
version of this idea has disappointed repeatedly because it asks one storage layout to be good at both.

The storage-convergence version is narrower and more defensible, because **the thing being eliminated is
the pipeline, not the specialization**. CDC plumbing between an operational database and a lakehouse is
where freshness lag, schema drift, and most operational failures actually live. Deleting it is a real
reduction in moving parts even if both engines remain.

## Current synthesis

### What "one copy" actually means

The vault records the qualification the source insists on: **"Single copy means single logical copy."**
Row data is transcoded into open columnar formats under [[Open Table Formats]] tables while
row-oriented indexes are retained for operational access — so **multiple physical representations still
exist**. The claim is the elimination of a *maintained synchronization pipeline*, not of duplication.

Treating "one copy" as a storage-footprint claim misreads it. This is the kind of phrase that should be
unpacked before being repeated.

### Architectural properties that come along

- **Compute/storage separation** enabling scale-to-zero, independent scaling, point-in-time restore, and
  **copy-on-write branching** — which makes testing a destructive migration cheap.
- **Catalog registration of the operational database**, extending the permissions, lineage, and audit
  model of [[Lakehouse Architecture]] to transactional data instead of leaving it as a separate
  governance boundary.
- **Vector and full-text search inside the transactional database** (approximate nearest neighbour plus
  BM25, via extensions). This is the detail with the most downstream consequence for this vault: it
  makes [[Agent Memory]] potentially transactional, permission-governed, and queryable without a
  separate vector service — touching [[Approximate Nearest-Neighbor Search]] and the
  operational-simplicity argument that usually decides such choices.
- Standard database drivers, tools, and ORMs continue to apply, which is what makes adoption incremental.

## Open questions

- **The architecture is only partly shipped.** The vault's source says so directly: **"The full
  single-copy experience is still assembling, piece by piece"**, with direct writes and real-time
  querying still in beta or limited availability. This belongs in the vault as a design with an
  argument, not as a proven system.
- Throughput and scale figures in the source — approximately **25,000 transactions per second** onto
  open table formats, approximately **12 million database launches per day** — are **vendor claims with
  no methodology, workload description, or configuration**, and should not be cited as benchmarks.
- **Scale-to-zero has a latency cost.** The official wake-up figure is "a few hundred milliseconds" while
  the author advises budgeting "a couple of seconds end-to-end" — a meaningful gap for latency-sensitive
  serving, and an example of why vendor latency figures need an independent read.
- Snapshot and branch storage is billable, so the cheap-branching property has an unquantified
  ongoing cost.
- The recommendation to start with new applications or serving layers rather than migrating mature
  production databases is conservative opinion — but consistent with the preview statuses.

## Related pages

- [[Lakehouse Architecture]]
- [[Open Table Formats]]
- [[Columnar Storage Formats]]
- [[Agent Memory]]
- [[Approximate Nearest-Neighbor Search]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Lakebase and LTAP]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - What a Modern Data Platform Looks Like in 2026]]
