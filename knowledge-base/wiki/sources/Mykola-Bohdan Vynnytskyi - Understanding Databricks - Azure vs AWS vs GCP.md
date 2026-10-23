---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-06-14-vynnytskyi-databricks-cloud-choice
source_title: "Understanding Databricks: Azure vs AWS vs GCP — Which Cloud to Choose in 2026"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-azure-vs-aws-vs-gcp-which-cloud-to-choose-in-2026-2101d04c5d0c
tags:
  - source/summary
  - data-platforms
  - cloud
  - series/understanding-databricks
source_ids:
  - src-2026-06-14-vynnytskyi-databricks-cloud-choice
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Azure vs AWS vs GCP

## Summary

Part three. The argument is that Databricks' **core technology is broadly consistent across clouds**,
while integration, billing, feature availability, and compliance are not — so the cloud choice should
follow the organization's existing footprint rather than the data platform.

Summary line: **"Azure = deepest integration. AWS = most mature, features first. GCP = newest, unique
architecture, some trade-offs."** And the decision rule: **"Start with the cloud where most of your data
already lives."**

## Key claims

- **First-party integration** means a service co-developed with the cloud provider, with unified
  identity, billing, and support. Azure Databricks is first-party; AWS and GCP deployments bill
  separately from Databricks.
- **Azure:** deepest Microsoft integration, unified billing and support, Fabric and Power BI
  integration, **confidential computing** (hardware-backed protection of data in use, via AMD SEV-SNP
  VMs), and Serverless Workspaces. Tradeoff is higher Jobs Compute pricing.
- **AWS:** most mature deployment, features typically arrive first, Graviton price-performance, GovCloud
  compliance, and fleet instance types.
- **GCP:** suited to existing Google/BigQuery/Gemini estates with federation and sustained-use
  discounts, but carries **GKE infrastructure overhead** and feature and compliance gaps.
- **Private networking** (VNet/VPC, peering, PrivateLink, Private Service Connect) is recommended;
  public production endpoints are characterized as a security risk.
- **[Product-specific, time-sensitive]** Azure Serverless Workspaces GA **March 2026**, startup "in
  seconds instead of 20 minutes". AWS Databricks available since **2014**, GCP since **2021**. GCP GKE
  overhead ~**$200/month per workspace**. Azure Jobs Compute **$0.30/DBU** versus **$0.15** on AWS/GCP,
  with Azure serverless workloads asserted **20-30% higher**. Infrastructure asserted as **50-70%** of
  total Databricks spend. Azure three-year DBCU commitments **up to 37% off**. AWS Graviton **up to 3x
  better price-performance** with Photon ETL. Standard tier sunset on AWS/GCP **October 2025**; Azure
  blocked new Standard workspaces from **April 2026** with upgrades by **October 2026**. AWS GovCloud
  FedRAMP High **February 2025**; Azure DoD IL5 and FedRAMP High; GCP standard FedRAMP only.
- **[Time-sensitive gap list]** As of mid-2026, GCP lacked Lakebase, AI Runtime, managed foundation-model
  fine-tuning, some serverless regions, and government-certified deployment.
- Multi-cloud portability is attributed to Unity Catalog plus open table formats.

## Why it matters

This is the clearest statement in the vault that **"the same platform" is not the same platform across
clouds**. For [[Lakehouse Architecture]], it establishes that portability claims rest on two specific
things — a governance catalog and [[Open Table Formats]] — and that everything above those layers
(identity, networking, compliance certifications, feature availability, unit price) varies.

The **50-70% infrastructure share** claim, if even roughly right, is the practically important one: it
means DBU rate comparisons address a minority of the bill.

## Tensions / open questions

- Essentially every comparative number is **asserted without an author-run benchmark**: the 20-30%
  serverless premium, 3x Graviton price-performance, 50-70% infrastructure share, $200 GKE overhead, and
  the "seconds instead of 20 minutes" startup claim.
- The author's own caveats are appropriate: **"DBU rates vary frequently"**, feature availability must
  be checked against current documentation, and the GCP gap list is explicitly qualified to mid-2026.
- Compliance certification status changes and is jurisdiction-specific; the dates given are snapshots.
- The recommendation structure is criteria-based opinion (Azure for Microsoft-centric enterprises, AWS
  for maturity, GCP for Google-centric estates), not a measured evaluation.

## Affected pages

- [[Lakehouse Architecture]]
- [[Databricks]]

## Raw capture

- [[Understanding Databricks Azure vs AWS vs GCP — Which Cloud to Choose in 2026]]

## Citations

- Raw capture: [[Understanding Databricks Azure vs AWS vs GCP — Which Cloud to Choose in 2026]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-azure-vs-aws-vs-gcp-which-cloud-to-choose-in-2026-2101d04c5d0c>
- Published 2026-06-14; captured 2026-10-23.

## Related pages

- [[Mykola-Bohdan Vynnytskyi]]
- [[Open Table Formats]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Honest Comparison with Snowflake and BigQuery]]
- [[Google Cloud]]
- [[GPU Fleet Reliability]]
- [[ML Systems at Scale]]
