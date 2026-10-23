---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-06-01-vynnytskyi-databricks-core-components
source_title: "Understanding Databricks: Core Components You Need to Know"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-core-components-you-need-to-know-fbede947e94e
tags:
  - source/summary
  - data-platforms
  - lakehouse
  - series/understanding-databricks
source_ids:
  - src-2026-06-01-vynnytskyi-databricks-core-components
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Core Components

## Summary

Part two of the series: an orientation map of Databricks' principal services — notebooks, Workflows /
Lakeflow Jobs, SQL Warehouses, Lakeflow, Unity Catalog, Mosaic AI, compute tiers, Apps, Marketplace, and
deployment bundles.

The durable idea is a **separation of duties** that generalizes past this vendor: notebooks are
development environments, declarative pipelines or orchestrated jobs are production, a governance
catalog is the shared namespace, and analytics and ML read the same governed data rather than copies.

## Key claims

- **Notebook:** interactive document combining executable code, results, visualizations, and
  documentation. **"Notebooks are where you spend most of your time"** — but the author's position is
  that production work belongs in Workflows or Lakeflow, not in scheduled notebooks.
- **Workflow / DAG:** production orchestration graph where tasks execute by dependency. DAG = directed
  acyclic graph.
- **Lakeflow:** declarative data-engineering suite (formerly Delta Live Tables) where users declare the
  desired datasets and quality rules rather than the execution steps. The author's strongest claim:
  **"Lakeflow is the most underused component in Databricks."**
- **Expectation:** a declarative data-quality rule that can warn, drop violating rows, or fail a
  pipeline.
- **Unity Catalog:** governance and discovery layer with a **catalog → schema → object** namespace
  covering tables, views, volumes, functions, models, and connections. **"Unity Catalog is the thread
  that holds it all together."** It must be adopted early to avoid costly retrofitting.
- **ABAC:** attribute-based access control, where policies use user or resource attributes rather than
  only individually assigned grants.
- **Lakehouse Federation:** querying external databases without copying their data in — avoiding data
  movement at the cost of dependence on the external system's connectivity and query behavior.
- **Photon:** a C++ vectorized query engine accelerating compatible SQL and data-processing workloads.
- **DBU:** the Databricks Unit metering compute consumption.
- **Declarative Automation Bundles:** YAML infrastructure-as-code for deploying jobs, pipelines,
  endpoints, and apps.
- **[Product-specific, time-sensitive]** Jobs Compute ~**$0.15/DBU** versus All-Purpose **$0.55/DBU**,
  described as roughly **3.7x cheaper**; SQL Serverless ~**$0.70/DBU** on AWS. Workflows support up to
  **1,000 tasks per job** and **2,000 concurrent task runs per workspace**. Lakeflow real-time mode
  claims latency **as low as 5 ms**. Unity Catalog ABAC GA **April 2026**; Unity Catalog open-sourced
  **June 2024 under Apache 2.0**; Lakeflow Designer default-on **May 2026** in Public Preview.
- **[Vendor claims]** Mosaic AI serving infrastructure at **250,000+ queries per second**; Vector Search
  over **1 billion vectors** at **7x lower cost**; MLflow **over 30 million monthly downloads**.

## Why it matters

For [[Lakehouse Architecture]], this is the component inventory that the rest of the series assumes. Two
patterns are transferable beyond Databricks.

First, **the dev/prod compute split is a cost control, not just a hygiene rule** — interactive compute
is priced for interactivity, and running production on it is the single most common avoidable expense in
the article's framing.

Second, **declarative pipelines with inline data-quality expectations** put validation in the pipeline
definition rather than in a separate test suite, which is the data-engineering analogue of the
evidence-before-merge discipline this vault tracks under [[Agentic Testing]].

## Tensions / open questions

- Performance, adoption, throughput, and cost claims are **vendor-reported and unverified**: the 250K
  QPS, 1-billion-vector, 7x-cost, and 5 ms figures carry no methodology.
- The author concedes Databricks renames products frequently, that several named features are in
  Preview or newly GA, and that pricing, defaults, availability, and throughput figures are
  time-sensitive.
- Much of the guidance is explicit opinion — "Lakeflow is the most underused component", Unity Catalog
  "every single time", "use Serverless", "serious teams" — rather than neutral documentation.
- The capture has minor truncation at the final sentence.

## Affected pages

- [[Lakehouse Architecture]]
- [[Declarative Data Pipeline Deployment]]
- [[Databricks]]

## Raw capture

- [[Understanding Databricks Core Components You Need to Know]]

## Citations

- Raw capture: [[Understanding Databricks Core Components You Need to Know]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-core-components-you-need-to-know-fbede947e94e>
- Published 2026-06-01; captured 2026-10-23.

## Related pages

- [[Mykola-Bohdan Vynnytskyi]]
- [[Open Table Formats]]
- [[Medallion Architecture]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - How to Structure a Databricks Project from Scratch]]
- [[Approximate Nearest-Neighbor Search]]
- [[Model Factory]]
