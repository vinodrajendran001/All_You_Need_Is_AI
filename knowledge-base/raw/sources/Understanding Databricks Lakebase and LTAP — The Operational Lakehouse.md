---
title: "Understanding Databricks: Lakebase and LTAP — The Operational Lakehouse"
source: "https://mbvyn.medium.com/understanding-databricks-lakebase-and-ltap-the-operational-lakehouse-8667ffc7f8c8"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-08-30
created: 2026-10-23
description: "Serverless Postgres inside Databricks, the LTAP architecture, and what “one copy of data” really means. Updated August 2026."
tags:
  - "clippings"
---
## Serverless Postgres inside Databricks, the LTAP architecture, and what “one copy of data” really means. Updated August 2026.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ln4s3adugMinMmurEb160Q.png)

I’ve built more CDC pipelines than I care to admit. Postgres on one side, a lakehouse on the other, and in between: Debezium, Kafka topics, sync jobs, watermark columns, and a monitoring dashboard that exists mostly to tell me the sync broke over the weekend. If you’ve done data engineering for more than a year, you have your own version of this story.

That gap between the database your application writes to and the platform your analytics run on is arguably the oldest tax in our profession. Databricks now claims it’s closing it: Lakebase puts a real Postgres inside the platform, and LTAP, announced at this year’s Data+AI Summit, promises transactions and analytics on a single copy of data with no CDC pipeline at all.

Big claim. So let’s unpack what Lakebase actually is, how the LTAP architecture works under the hood, what’s genuinely GA versus preview (the honest version, with dates), and whether you should start planning the funeral for your sync jobs.

This article is part of the Understanding Databricks series. It pairs with [Genie Explained](https://medium.com/@mbvyn/understanding-databricks-genie-explained-genie-one-agents-and-the-ontology-710792b66c5a?sharedUserId=mbvyn): Genie is the AI that consumes your data; Lakebase is where operational data now lives.

> **Key takeaways**
> 
> **Lakebase** is a serverless Postgres built into Databricks: real Postgres 17/18, scale-to-zero, copy-on-write branching, point-in-time restore, all governed by Unity Catalog. GA on AWS and Azure; still Beta on GCP.
> 
> **LTAP** (Lake Transactional/Analytical Processing) is the architecture behind it: the storage layer transcodes Postgres row data into open columnar formats, so transactions and analytics share one logical copy with no CDC pipeline.
> 
> Component reality check: synced tables are GA, LTAP Direct Writes are Beta, Lakebase Change Data Feed is Public Preview, and Lakehouse//RT querying Lakebase is Beta. The full single-copy vision is still being assembled.
> 
> Lakebase Search (Beta) adds vector and BM25 full-text search as Postgres extensions, which quietly makes Lakebase a serving layer for AI agents.
> 
> Pricing favors experiments: scale-to-zero means idle databases cost almost nothing, and always-on compute carries a 50% promotional discount through January 2027.
> 
> For data engineers this is a role expansion: the operational database just moved into your platform, under your governance model.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*VycsTjl7IBmbrVI4T8hejQ.png)

## What Lakebase Is

Lakebase is a fully managed Postgres database that lives inside your Databricks workspace. Not “Postgres-compatible”, not “a SQL layer that speaks the wire protocol” — actual Postgres, currently versions 16 through 18 with 17 as the default. Your existing drivers, ORMs, and tools connect to it like to any other Postgres.

The technology came from Databricks’ acquisition of Neon in 2025, and it inherits Neon’s defining trick: compute and storage are fully separated. Stateless Postgres compute nodes talk to a durable storage layer built on cloud object storage. That one architectural decision produces most of the headline features:

- **Scale-to-zero.** No traffic means compute shuts down and you pay almost nothing. A request wakes it in a few hundred milliseconds officially; in practice, budget up to a couple of seconds end-to-end for a cold start
- **Branching.** A database branch is a copy-on-write metadata operation, not a copy. You can branch production, run a destructive migration test, and throw the branch away in seconds
- **Point-in-time restore.** Rewind a database to any moment in the retention window, again as a metadata operation
- **Independent scaling.** Storage grows without touching compute; compute scales without moving data

Since GA, the operational maturity has been filling in fast. There’s a zone-redundant high-availability SLA (July 15), SOC 2 Type 2 certification (July 14), AI-assisted troubleshooting in Beta that combines database telemetry with Genie, and as of August 14, the full management surface (projects, branches, endpoints, roles, synced tables) is GA through the REST API, CLI, and SDKs. That last one matters more than it sounds: it means Lakebase is now scriptable enough for real CI/CD, not just clicking around the UI.

And one more piece worth knowing about: Lakebase Search (Beta, since the Summit) adds two Postgres extensions, one for approximate nearest-neighbor vector search and one for BM25 full-text search. Put together with scale-to-zero, that turns Lakebase into a natural serving layer for AI agents: state, transactions, and retrieval in one place, next to the data platform the agents already query.

> **Take Your Databricks Prep to the Next Level**
> 
> If you are serious about mastering Databricks and preparing for certification, check out my practice exams on Udemy:
> 
> [Databricks Data Engineer Professional: 300+ Practice Questions](https://www.udemy.com/course/databricks-data-engineer-professional-300-practice-question/?referralCode=04CA66473BF290882536) — Exam-grade questions covering Delta Lake, Structured Streaming, and production data engineering scenarios
> 
> [Databricks Data Engineer Associate: 5 Practice Tests (2026)](https://www.udemy.com/course/databricks-data-engineer-associate-5-practice-tests-2026/?referralCode=E930A2DCEDFBDCFA0374) — Five full-length practice tests aligned to the latest exam blueprint with detailed explanations
> 
> [Databricks GenAI Engineer Associate: 5 Practice Tests (2026)](https://www.udemy.com/course/databricks-genai-engineer-associate-5-practice-tests-2026/?referralCode=48CC75361435DC8F7F48) — Five practice tests covering Mosaic AI, RAG, model serving, and GenAI workflows on Databricks
> 
> These tests are designed to challenge you in the same way the real exam will.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*1V5b5_USf4FtkGdK8-9wAA.png)

## The Problem LTAP Wants to Kill

Before the architecture, the problem. Every company past a certain size runs two data worlds. The OLTP world: Postgres or MySQL behind the application, optimized for many small reads and writes, rows stored together so a single order can be fetched in a millisecond. And the OLAP world: a warehouse or lakehouse, columnar storage, optimized for scanning millions of rows to answer “revenue by region.”

Neither can do the other’s job well, so we copy data between them. That copying is the CDC pipeline I complained about in the intro, and it costs you three things. Money, because you’re storing everything at least twice and paying compute to move it. Freshness, because your analytics see the world as it was minutes or hours ago. And engineering time, because sync pipelines are the classic 2am pager: schema drift on the source, a full-refresh that never finishes, a connector version bump that changes semantics.

The industry has tried to merge the two worlds before under the name HTAP (hybrid transactional/analytical processing), with mixed results. Databricks’ pitch is that HTAP failed because it tried to make one engine do both jobs. LTAP keeps two purpose-built engines and instead unifies the **storage**.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*6cv2ZlJjvwWJeb3kGmDH0g.png)

## LTAP: How One Copy Actually Works

Here’s the mechanism, and it’s genuinely elegant. In Lakebase, Postgres compute doesn’t own its storage; a separate storage layer does. As data materializes to cloud object storage, that layer transcodes it from Postgres’ row-oriented format into open columnar formats (Parquet under Delta and Iceberg tables), preserving row versions and transaction semantics. Indexes stay row-oriented for fast transactional reads.

So the same logical data is transactional when Postgres touches it and analytical when Spark or a SQL warehouse touches it. No Debezium, no Kafka in the middle, no sync job to babysit. Databricks reports the write path holds up at roughly 25,000 transactions per second onto open table formats, and the platform is running around 12 million database launches a day, so this is not a lab demo.

A dose of honesty, though, because vendor architecture diagrams deserve one. “Single copy” means single **logical** copy: physically there’s still a row representation (for indexes and hot data) and a columnar one. What disappears isn’t bytes on disk — it’s the pipeline you maintain between them, which was always the expensive part. The Register made exactly this point in a wonderfully titled piece, “Databricks unifies OLTP and OLAP, depending on what counts as a copy.” Fair. I’d still take “one logical copy, zero pipelines” over my Debezium dashboards any day.

The current component statuses, precisely:

- **Synced tables** (lakehouse ↔ Postgres serving) — GA, with LTAP Direct Writes in Beta as a faster load path that writes straight to storage
- **Lakebase Change Data Feed** (streaming changes out of Postgres) — Public Preview
- **Lakehouse//RT querying Lakebase** — Beta, for select customers
- **Registering Lakebase in Unity Catalog** — GA

Read that list carefully and you’ll see the real story: the foundation is shipped, and the fully-automatic single-copy experience is still assembling, piece by piece, mostly in preview. Plan accordingly.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*mhcecNvJTPctbN7AZpp_fQ.png)

## Where You Can Run It Today

Cloud availability is uneven, and it matters for planning. Lakebase is GA on AWS (since February) and Azure (since March). On GCP, it’s still Beta as of August 2026. Regions keep expanding (Tokyo went live June 30).

Postgres version support is current: 16, 17, and 18, with 17 as the default and minor versions patched automatically on compute restart. If you’ve worked with managed Postgres elsewhere, this will feel familiar, which is the point. The unusual part is governance: a Lakebase database registers in Unity Catalog, so the same permission model, lineage, and audit trail you use for Delta tables now covers your operational database too. That single fact is half the argument for running Postgres here instead of RDS next door.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-OyYvckblWaigAv7xLyjeQ.png)

## Pricing: Built for Experiments

The economics are friendlier than you’d expect, for a reason: Databricks wants you to try it.

Scale-to-zero means a dev or low-traffic database costs close to nothing while idle; you pay for compute only when it’s awake, plus storage (snapshot storage became billable in June, so watch retention settings on branches you forget about). For production databases that need to stay hot, there’s Always-On pricing: disable scale-to-zero, and after 24 hours of continuous use your baseline capacity bills 25% lower than standard autoscaling rates, with a **50% promotional discount stacked on top through January 31, 2027**.

Same playbook as Genie’s free window from [the previous article](https://medium.com/@mbvyn/understanding-databricks-genie-explained-genie-one-agents-and-the-ontology-710792b66c5a?sharedUserId=mbvyn): adoption now, revenue later. And the same practical conclusion: the cheap-experiment window is open, and it closes in early 2027.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zgtg0SqvfVLDmi_aPcXHbA.png)

## What This Means for Data Engineers

For years, the operational database was somebody else’s problem. Backend engineers owned Postgres; we owned everything downstream of the CDC pipeline. Lakebase moves the boundary: the database is now inside the platform you run, governed by the catalog you manage.

I’d frame the opportunity in three layers. First, the boring-but-valuable one: reverse ETL gets simpler. Serving a Gold table to an application today means exporting to some external store; a synced table into Postgres does the job without leaving the platform, and it’s GA now. Second, the architectural one: new internal apps and agents can just be built on Lakebase, next to the analytics, skipping the two-worlds problem entirely instead of solving it. Third, the career one: understanding both OLTP and OLAP semantics stops being a specialization and starts being the job description. The wall between “app data” and “analytics data” is exactly what’s being demolished.

If you want a low-risk start, do what I’d do: take one internal dashboard-ish app that today reads from an exported table, create a Lakebase instance with a synced table, and point the app at Postgres. You’ll touch branching, sync behavior, and the permission model in one small project, while the promo pricing makes the bill a rounding error.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AJJKJp0n4BNV9yBVyL3nPg.png)

## Common Mistakes to Avoid

- **Treating LTAP as fully shipped.** The architecture is real, but Change Data Feed is in Public Preview, Direct Writes are Beta, and Lakehouse//RT access is select-customer Beta. Build production only on the GA pieces
- **Planning a GCP rollout.** Lakebase is still Beta. AWS and Azure are the GA clouds as of August 2026
- **Migrating your main application database first.** Start with new apps, internal tools, or serving layers. Lakebase is young; your 10-year-old order database has scars and edge cases
- **Ignoring branch and snapshot hygiene.** Branches are cheap to create and easy to forget; snapshot storage bills since June. Set retention and clean up
- **Comparing it to RDS on price alone.** The value is governance, branching, synced tables, and zero-pipeline analytics. Spreadsheet it on total cost, including the CDC infrastructure you’d retire
- **Missing the promo window.** 50% off always-on compute ends in January 2027. Evaluate while it’s cheap; budget for full price after
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MJipmHfSIjYMYmgU6kERlQ.png)

## Frequently Asked Questions

### What is Databricks Lakebase?

Lakebase is a fully managed, serverless Postgres database built into Databricks, based on technology from the Neon acquisition. It separates compute from storage, which enables scale-to-zero, copy-on-write branching, and point-in-time restore, and it registers in Unity Catalog so operational data shares governance with the lakehouse. It’s GA on AWS and Azure, Beta on GCP.

### What is LTAP and how is it different from HTAP?

LTAP (Lake Transactional/Analytical Processing) is Databricks’ architecture for running transactions and analytics on one logical copy of data in open formats. HTAP systems tried to make a single engine serve both workloads; LTAP keeps two purpose-built engines (Postgres for OLTP, the lakehouse for OLAP) and unifies the storage layer instead: Postgres row data is transcoded into open columnar formats as it lands in cloud storage, removing the need for CDC pipelines.

### Is LTAP generally available?

Partially. Synced tables and Unity Catalog registration are GA. LTAP Direct Writes are Beta, Lakebase Change Data Feed is Public Preview, and Lakehouse//RT querying of Lakebase is a select-customer Beta. The full single-copy experience is still rolling out.

### How much does Lakebase cost?

You pay for compute while the database is awake plus storage (including snapshot storage). Scale-to-zero makes idle databases nearly free, and always-on compute carries a 50% promotional discount through January 2027. There’s no per-seat licensing.

### Can Lakebase replace my existing Postgres (RDS, Cloud SQL)?

Technically, yes, for many workloads: it’s real Postgres 16–18 with standard drivers, an HA SLA, and SOC 2 Type 2. Practically, start with new applications, internal tools, and serving layers rather than migrating a battle-hardened production database on day one. The strongest reasons to choose it are governance through Unity Catalog and pipeline-free analytics, not raw Postgres hosting.

### What is Lakebase Search?

A Beta capability that adds two Postgres extensions: approximate nearest-neighbor vector search and BM25 full-text search. It lets AI agents and applications do retrieval directly against Lakebase, which, combined with transactions and scale-to-zero, makes it a compelling backend for agent state and RAG-style serving.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*sl0nG_8IMAKyadcnQwDNpQ.png)

With Genie and Lakebase covered, we’ve mapped the platform's two newest wings. Next we go back to the ground and start building: Part III opens with how to structure a Databricks project from scratch (repositories, notebooks versus modules, configs, and environments). The unglamorous decisions that decide whether your platform is maintainable in year two.

Bookmark this series so you don’t miss any upcoming articles.

*Want more? Visit* [*mbvyn.com*](https://mbvyn.com/) *for mentorship, consulting, and all my content in one place.*

*And if you work with Parquet files, try* [*parquetreader.app*](https://parquetreader.app/) *— my free tool for exploring them on the desktop*

***Reviewed by Coconut and Whiskey. Coconut demands ACID guarantees on every meal. Whiskey is eventually consistent.***