---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-08-30-vynnytskyi-lakebase-ltap
source_title: "Understanding Databricks: Lakebase and LTAP — The Operational Lakehouse"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-lakebase-and-ltap-the-operational-lakehouse-8667ffc7f8c8
tags:
  - source/summary
  - lakehouse
  - databases
  - series/understanding-databricks
source_ids:
  - src-2026-08-30-vynnytskyi-lakebase-ltap
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Lakebase and LTAP

## Summary

Part twelve introduces **Lakebase** (managed, serverless Postgres inside the platform) and **LTAP**
(Lake Transactional/Analytical Processing), the architecture for serving operational and analytical
workloads from one logical copy of data.

The architectural claim worth keeping is the contrast with HTAP: **"LTAP keeps two purpose-built engines
and instead unifies the storage."** And the qualification the author insists on: **"Single copy means
single logical copy"** — the elimination of a maintained CDC pipeline, not a single physical
representation.

## Key claims

- **OLTP** handles many small row-oriented reads and writes for application transactions; **OLAP**
  handles large columnar scans and aggregations. The two have genuinely different storage preferences,
  which is why one engine serving both (the HTAP ambition) has historically disappointed.
- **LTAP transcodes Postgres row data into open columnar formats** such as Parquet under Delta or
  Iceberg, while retaining row-oriented indexes for operational access. The two engines remain separate;
  the **storage layer** is what converges.
- "One copy" means **one logical copy and no maintained CDC synchronization pipeline** — the author
  explicitly acknowledges multiple physical representations.
- **Compute/storage separation** enables scale-to-zero, copy-on-write **branching**, point-in-time
  restore, and independent scaling. Branching supports testing destructive migrations cheaply.
- **Lakebase Search** adds approximate-nearest-neighbor vector search and **BM25** full-text search
  through Postgres extensions — making the operational database a plausible home for agent state and
  retrieval.
- **Synced tables** serve lakehouse data to Postgres-backed applications; **Unity Catalog registration**
  extends catalog permissions, lineage, and audit to the operational database.
- Standard Postgres drivers, tools, and ORMs apply.
- **[Vendor claims]** approximately **25,000 transactions per second** written onto open table formats;
  approximately **12 million database launches per day** on the platform. Neither has supplied
  methodology, workload description, or configuration.
- **[Self-reported, time-sensitive]** Postgres **16–18** with **17** default; GA on AWS (February) and
  Azure (March), **Beta on GCP** as of August 2026; Change Data Feed Public Preview; LTAP Direct Writes
  Beta; Lakehouse//RT querying Beta/select customers; synced tables and UC registration GA; technology
  acquired from **Neon in 2025**; snapshot storage billable since June; Always-On baseline capacity
  described as **25% lower** after **24 hours** continuous use with a **50% promotional discount through
  2027-01-31**; HA SLA and SOC 2 Type 2 stated as available. Cold-start wake-up is quoted officially as
  "a few hundred milliseconds", but the author advises budgeting **"a couple of seconds end-to-end"**.

## Why it matters

[[Operational Analytical Convergence]] enters the vault with a specific and credible mechanism. The
usual version of this idea — one engine for everything — has repeatedly failed because the access
patterns are genuinely incompatible. LTAP's move is narrower and more defensible: **keep both engines,
converge the storage, and delete the pipeline between them.** The thing being eliminated is the CDC
plumbing, which is where freshness lag and operational failure actually live.

For agents, Lakebase Search is the detail with downstream consequences. Vector plus full-text search
inside the transactional database means [[Agent Memory]] can be transactional, governed by the same
permissions, and queried without a separate vector service — which touches
[[Approximate Nearest-Neighbor Search]] and the operational-simplicity argument that usually decides
such choices.

## Tensions / open questions

- **Full LTAP single-copy functionality is not shipped**; Direct Writes and Lakehouse//RT remain Beta or
  limited. The author's own summary: **"The full single-copy experience is still assembling, piece by
  piece."**
- The **25,000 TPS** and **12 million launches/day** figures are vendor claims without methodology and
  should not be treated as benchmarks.
- Scale-to-zero cold starts may take seconds in practice despite the official sub-second figure — a real
  constraint for latency-sensitive serving.
- Snapshot and branch retention are billable and need management.
- GCP was not GA in the article's timeframe.
- The author advises **against migrating mature production databases**, recommending new applications,
  internal tools, or serving layers first — an opinion, but a conservative one consistent with the
  preview statuses.

## Affected pages

- [[Operational Analytical Convergence]]
- [[Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Lakehouse Architecture]]

## Raw capture

- [[Understanding Databricks Lakebase and LTAP — The Operational Lakehouse]]

## Citations

- Raw capture: [[Understanding Databricks Lakebase and LTAP — The Operational Lakehouse]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-lakebase-and-ltap-the-operational-lakehouse-8667ffc7f8c8>
- Published 2026-08-30; captured 2026-10-23.

## Related pages

- [[Open Table Formats]]
- [[Approximate Nearest-Neighbor Search]]
- [[Agent Memory]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - What a Modern Data Platform Looks Like in 2026]]
