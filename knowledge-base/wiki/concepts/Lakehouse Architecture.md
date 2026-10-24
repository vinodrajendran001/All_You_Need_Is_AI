---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - data-platform
  - lakehouse
  - architecture
source_ids:
  - src-2026-05-23-vynnytskyi-databricks-snowflake-bigquery
  - src-2026-06-01-vynnytskyi-databricks-core-components
  - src-2026-06-14-vynnytskyi-databricks-cloud-choice
  - src-2026-06-21-vynnytskyi-modern-data-platform
  - src-2026-08-30-vynnytskyi-lakebase-ltap
status: active
---

# Lakehouse Architecture

## Definition

A **lakehouse** stores data in customer-controlled cloud object storage using open formats, and layers
warehouse-grade reliability — transactions, schema enforcement, governance — on top of it through a
metadata layer rather than through a proprietary storage engine.

The defining structural property is **separation of storage and compute**: data sits in object storage
(S3, ADLS, GCS) while compute is provisioned independently, scaled per workload, and can be scaled to
zero. Multiple engines can read the same bytes.

## Why it matters

For this vault, the lakehouse matters less as a data-engineering trend than as **the substrate AI agents
act on**. [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - What a Modern Data Platform Looks Like in 2026]]
argues the platform is increasingly designed for agents rather than only for human analysts, and the
consequence is concrete: when an agent can query and write enterprise data, the governance layer stops
being paperwork and becomes **the mechanism that bounds what the agent can do**.

That connects directly to [[Agent Security and Governance]]. An agent whose reach is defined by catalog
permissions inherits an audited, pre-existing authorization boundary instead of requiring a new one —
which is the design [[Text-to-SQL Agents]] depends on.

## Current synthesis

### Five layers

The vault's sources describe a modern platform as **storage, compute, governance, orchestration, and
intelligence**. The lakehouse supplies the first two and anchors the third; it is, in the source's own
framing, **"the foundation, not the whole platform."**

- **Open storage** — data in customer-controlled object storage, in interoperable formats such as Delta
  or Iceberg. The stated motive is reduced vendor lock-in; see [[Open Table Formats]].
- **Elastic / serverless compute** — provider-managed, scaling with demand, scaling to zero when idle.
  The trade is reduced administration in exchange for **consumption-based pricing**, which moves cost
  from a provisioning decision to a query-by-query one.
- **Governance** — access control, lineage, discovery, classification, and auditing, answering who may
  use data, where it came from, and whether it is trustworthy.
- **Orchestration** — scheduling, dependencies, monitoring, error handling; see
  [[Declarative Data Pipeline Deployment]].
- **Intelligence** — model training, serving, agents, and vector search over the governed data.

### Why the separation is the load-bearing idea

Warehouses historically coupled storage and compute inside one proprietary engine, which made the data
reachable only through that engine. Putting data in open formats on object storage **decouples the
question "where does the data live" from "what reads it"**, which is what allows a SQL engine, a Spark
job, an ML trainer, and an agent to operate on one copy. Federation extends the same idea outward —
querying external databases without copying them — at the cost of depending on the remote system's
connectivity and query behaviour.

### Governance as the namespace

Across the Databricks series, governance is organized as a **catalog → schema → object** namespace
covering tables, views, volumes, functions, models, and connections — notably including **models and
agents as governed objects**, not just tables. Attribute-based access control (policies keyed on user or
resource attributes rather than individually assigned grants) is what makes this tractable at scale.

The recurring practical warning is that governance **must be installed early**; retrofitting it across
an established estate is expensive.

### The convergence direction

[[Operational Analytical Convergence]] is the live frontier: the attempt to serve transactional and
analytical workloads from one logical copy, eliminating the change-data-capture pipeline between an
operational database and the lakehouse. The vault records this as **architecturally coherent but only
partly shipped**.

## Open questions

- Separation of storage and compute is well established; **the business claims around it are not**. The
  vault's sources carry vendor revenue, valuation, latency, and throughput figures that are
  self-reported or third-party reported, with no methodology — they should not be cited as measurements.
- Consumption pricing makes cost a function of query behaviour, which is hard to forecast. None of the
  vault's sources supply a measured cost comparison against provisioned alternatives.
- "Open format" reduces but does not eliminate lock-in: the engine-specific optimization, governance,
  and automation layers above the format remain proprietary.
- If agents become primary consumers of the platform, what evaluation exists for whether governance
  boundaries actually hold under agentic access patterns? The vault has governance *design* here but no
  governance *testing*.

## Related pages

- [[Open Table Formats]]
- [[Medallion Architecture]]
- [[Columnar Storage Formats]]
- [[Operational Analytical Convergence]]
- [[Text-to-SQL Agents]]
- [[Declarative Data Pipeline Deployment]]
- [[Table Layout Optimization]]
- [[Agent Security and Governance]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - What a Modern Data Platform Looks Like in 2026]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Core Components]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Honest Comparison with Snowflake and BigQuery]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Azure vs AWS vs GCP]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Lakebase and LTAP]]
- [[ML Systems at Scale]]
- [[AI Knowledge Base Overview]]
