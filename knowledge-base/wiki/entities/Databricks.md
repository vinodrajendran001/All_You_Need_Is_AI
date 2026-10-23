---
type: entity
created: 2026-10-23
updated: 2026-10-23
entity_kind: organization
tags:
  - entity
  - data-platform
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
  - src-2026-10-21-databricks-memcurrent
status: active
---

# Databricks

## What it is

A data and AI platform organized around the **lakehouse** idea: data in customer-controlled object
storage in open formats, with warehouse-grade transactions, governance, and compute layered on top. Its
components recur throughout this vault — Delta Lake as a table format, Unity Catalog as the governance
namespace, Lakeflow for declarative pipelines, Mosaic AI for model and agent serving, and Genie as a
natural-language query interface.

## Why it matters here

Databricks enters this vault through two very different doors, and the contrast is the reason this page
is worth keeping.

**As a platform**, it is the setting for the thirteen-part series by [[Mykola-Bohdan Vynnytskyi]], which
supplies most of the vault's coverage of [[Lakehouse Architecture]], [[Open Table Formats]],
[[Medallion Architecture]], [[Table Layout Optimization]], [[Slowly Changing Dimensions]],
[[Operational Analytical Convergence]], and [[Declarative Data Pipeline Deployment]]. That material
matters because it describes **the substrate AI agents increasingly act on**: when an agent can query
and write enterprise data, catalog permissions become the boundary on what the agent can do.

**As a research publisher**, it contributes
[[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]], one of the more
carefully ablated memory systems in the vault — notable for reporting that **derived memory does most of
the work** (66.1% alone versus 35.8% for episodic alone, both together 68.4%, from a 22.3% no-memory
floor) rather than claiming every component helps.

## Notes

### Vendor-claim density is unusually high

Nearly every quantitative claim about this platform in the vault is **self-reported or vendor-reported
without methodology**. Figures the vault holds but does not treat as evidence include:

- **84.5% versus 52.4%** first-attempt accuracy for Genie against "the strongest general-purpose coding
  agent" — no task distribution, no baseline description, no independent replication.
- **~25,000 transactions/second** onto open table formats and **~12 million database launches/day**.
- **sub-100 ms** real-time lakehouse latency; **5 ms** declarative-pipeline real-time mode;
  **250,000+ queries/second** serving infrastructure; **7x lower cost** vector search.
- Revenue run-rate and valuation figures, which are self-reported or third-party reported.

The MemCurrent numbers are **first-party but methodologically disclosed** — benchmarks named, harnesses
named, repeats stated, ablations run — which is a materially different evidentiary standard from the
marketing figures above. The vault should keep that distinction visible rather than averaging them.

### Frequent renaming

Product names change often enough that the vault's own sources flag it as a cost: Databricks One →
Genie → Genie One, Genie Spaces → Genie Agents, Delta Live Tables → Lakeflow, Databricks Asset Bundles
→ Declarative Automation Bundles. Older documentation and older vault pages age quickly as a result, so
concept pages here are written around **mechanisms** rather than product names.

### Preview status is load-bearing

Much of what is described — the convergence architecture's direct writes, real-time querying, the
ontology, autonomous operations — sits in preview or limited availability. The vault records these as
**designs with arguments, not shipped and verified systems**.

## Related pages

- [[Lakehouse Architecture]]
- [[Open Table Formats]]
- [[Medallion Architecture]]
- [[Table Layout Optimization]]
- [[Slowly Changing Dimensions]]
- [[Columnar Storage Formats]]
- [[Operational Analytical Convergence]]
- [[Text-to-SQL Agents]]
- [[Declarative Data Pipeline Deployment]]
- [[Agent Memory]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Honest Comparison with Snowflake and BigQuery]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Core Components]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Lakebase and LTAP]]
