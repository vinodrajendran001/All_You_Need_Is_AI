---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-05-23-vynnytskyi-databricks-snowflake-bigquery
source_title: "Understanding Databricks: Honest Comparison with Snowflake and BigQuery"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-honest-comparison-with-snowflake-and-bigquery-f53c5621a2c5
tags:
  - source/summary
  - data-platforms
  - lakehouse
  - series/understanding-databricks
source_ids:
  - src-2026-05-23-vynnytskyi-databricks-snowflake-bigquery
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Honest Comparison with Snowflake and BigQuery

## Summary

Part one of the **Understanding Databricks** series. It compares Databricks, Snowflake, and BigQuery on
architecture, billing model, workload fit, openness, and AI capability, reaching a deliberately
unglamorous conclusion: **"There is no single winner."**

The durable content is the **billing-model taxonomy**, which explains why cost comparisons between these
platforms are so often meaningless. The comparative performance claims are not.

## Key claims

- **Three architectures:** Databricks keeps data in **customer-controlled cloud storage in open
  formats** (Delta, Iceberg) with Spark/Photon compute; Snowflake is a managed warehouse with separated
  storage and compute and minimal administration; BigQuery is **fully serverless**, with Google managing
  both compute and storage.
- **Three incompatible billing units:** Databricks meters **DBUs** of compute consumption; Snowflake
  meters **credits** that vary by warehouse size and edition; BigQuery on demand bills **bytes scanned**,
  which makes partitioning and clustering a direct cost lever rather than a performance one.
- **[Product-specific pricing, time-sensitive]** Databricks Jobs Compute ~**$0.15/DBU**, All-Purpose
  ~**$0.55**, SQL Serverless ~**$0.70**. Snowflake credits roughly **$2** Standard, **$3** Enterprise,
  **$4** Business Critical, with warehouse sizes running 1 credit/hour at X-Small up to **512
  credits/hour** at 6X-Large, and storage about **$23 per compressed TB/month**. BigQuery **$6.25 per
  TB scanned**, capacity rates **$0.04 / $0.06 / $0.10** per slot-hour, free tier **10 GB** storage and
  **1 TiB** queries monthly.
- **[Illustrative]** The on-demand-to-capacity crossover is placed at roughly **15-25 TB of monthly
  scanning**, and a `SELECT *` on a large unpartitioned BigQuery table is said to cost **over $60**.
- Workload fit as asserted: Databricks for ETL, streaming, ML, AI agents, and open formats; Snowflake
  for SQL-first teams, data sharing, BI concurrency, and multi-cloud consistency; BigQuery for
  Google-centric, sporadic, serverless analytics.
- Drawbacks as asserted: Databricks has a learning curve, dual billing, and compute-management
  complexity; Snowflake has higher claimed ETL cost and weaker real-time streaming; BigQuery has cost
  unpredictability, GCP dependence, limited transaction support, and less tuning control.

## Why it matters

This is the vault's entry point into [[Lakehouse Architecture]] as a commercial category rather than an
abstract design. The billing-unit comparison is the part that survives version churn: **DBUs, credits,
and bytes scanned are not convertible**, so any "platform X is N times cheaper" claim is really a claim
about one workload shape under one contract.

It also sets up the open-format argument the rest of the series depends on — that storing data in
[[Open Table Formats]] under customer-controlled object storage is what makes multi-engine access and
vendor exit possible at all.

## Tensions / open questions

- The article's own best line is also its indictment of its own numbers: **"Vendor benchmarks are
  marketing. Your own benchmarks are true."** The author then repeats several vendor comparisons anyway.
- **Photon "2.7x faster than Snowflake on cold starts"** and **Snowflake ETL "3 to 5 times more"
  expensive** are asserted with **no workload, no methodology, and no author-run benchmark**.
- Snowflake compression "**3 to 5x**", "**53 regional deployments**", "**over 9,100 accounts**" using AI
  features, Databricks AI revenue "**over $1.4 billion**", MLflow "**over 30 million monthly
  downloads**", growth rates (**29%** Snowflake FY2026 vs **65%** Databricks) and market caps (**$90B**,
  **~$52B**) are all vendor- or third-party-reported with no citation.
- Gartner 2025 and Forrester Q2 2025 rankings are named without reference details.
- The author concedes prices vary by edition, workload, cloud, contract, and infrastructure, that many
  organizations run multiple platforms, and that readers should test their own workloads.
- All pricing and market figures are time-sensitive and were current to **May 2026**.

## Affected pages

- [[Lakehouse Architecture]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Databricks]]

## Raw capture

- [[Understanding Databricks Honest Comparison with Snowflake and BigQuery]]

## Citations

- Raw capture: [[Understanding Databricks Honest Comparison with Snowflake and BigQuery]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-honest-comparison-with-snowflake-and-bigquery-f53c5621a2c5>
- Published 2026-05-23; captured 2026-10-23. Final "What Is Next" sentence is truncated in the capture.

## Related pages

- [[Open Table Formats]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Core Components]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Azure vs AWS vs GCP]]
- [[Benchmark Optimization]]
- [[ML Systems at Scale]]
