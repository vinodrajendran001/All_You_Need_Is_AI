---
title: "Understanding Databricks: Optimizing Delta Tables"
source: "https://mbvyn.medium.com/understanding-databricks-optimizing-delta-tables-6065b1388676"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-08-15
created: 2026-10-23
description: "Why tables get slow and the modern way to keep them fast. Updated July 2026."
tags:
  - "clippings"
---
## Why tables get slow and the modern way to keep them fast. Updated July 2026.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GZPmQZ7xsQdCj6cChC54xw.png)

A table that was fast in January is crawling by July. The queries did not change. The data grew, sure, but not that much. So what happened?

Nine times out of ten, I can tell you without looking: **small files.**

Thousands of them, created one batch at a time by streaming writes and frequent jobs, each adding a little overhead until your queries spend more time opening files than reading data. It is the most common performance problem in every lakehouse — and the most fixable.

This article closes out our Delta Lake block with the maintenance side of the story: how tables degrade, how OPTIMIZE and liquid clustering fix them, what VACUUM actually does, and — the big 2026 shift — how much of this Databricks now handles for you automatically. By the end, you will have a simple health-check workflow you can run on any slow table.

This article is part of the ***Understanding Databricks*** series and builds on [Delta Lake in Practice](https://medium.com/@mbvyn/understanding-databricks-delta-lake-in-practice-create-append-and-merge-18b58f8f50c9?sharedUserId=mbvyn) and [Time Travel](https://medium.com/@mbvyn/understanding-databricks-time-travel-in-delta-lake-42e45b34de83?sharedUserId=mbvyn).

## Key takeaways

- The number one cause of slow Delta tables is the **small files problem** — every file adds listing, opening, and metadata overhead. Healthy files are roughly 128 MB to 1 GB.
- **OPTIMIZE** compacts small files into big ones. It is idempotent and safe to run anytime.
- **Liquid clustering** (*CLUSTER BY*) is the modern data layout — it replaced both partitioning and ZORDER for new tables. *CLUSTER BY AUTO* even picks the keys for you.
- **VACUUM** removes old unreferenced files. On Runtime 18, *RETAIN n HOURS* is ignored — control retention with table properties.
- On Unity Catalog managed tables, **predictive optimization** runs OPTIMIZE, VACUUM, and statistics automatically. Manual maintenance is now mainly an external-tables concern.
- Diagnose any table in one query: *DESCRIBE DETAIL* → divide size by file count → if the average file is tiny, you found your problem.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*80MFWwJpVJQm0HTYRdewiA.png)

## Why Delta Tables Get Slow

Every file in your table has a fixed cost. The engine has to list it, open it, read its footer, and evaluate its statistics — before reading a single row of actual data. With a hundred files, that overhead is invisible. With a hundred thousand, it dominates the query.

And small files accumulate naturally. Streaming writes land a few rows at a time. Hourly jobs append small batches. MERGE operations rewrite fragments. Nobody does anything wrong, and yet six months later the table is a swamp of 5 MB files.

What should files look like instead? Databricks autotunes the target by table size: roughly **256 MB** files for tables under 2.5 TB, scaling up to **1 GB** for the largest tables. You do not need to memorize the numbers — just internalize the shape of the problem: fewer, bigger files are faster than many small ones. Nearly everything in this article is a tool for getting from the second state to the first.

> ***Take Your Databricks Prep to the Next Level***
> 
> *If you are serious about mastering Databricks and preparing for certification, check out my practice exams on Udemy:*
> 
> [*Databricks Data Engineer Professional: 300+ Practice Questions*](https://www.udemy.com/course/databricks-data-engineer-professional-300-practice-question/?referralCode=04CA66473BF290882536) *— Exam-grade questions covering Delta Lake, Structured Streaming, and production data engineering scenarios*
> 
> [*Databricks Data Engineer Associate: 5 Practice Tests (2026)*](https://www.udemy.com/course/databricks-data-engineer-associate-5-practice-tests-2026/?referralCode=E930A2DCEDFBDCFA0374) *— Five full-length practice tests aligned to the latest exam blueprint with detailed explanations*
> 
> [*Databricks GenAI Engineer Associate: 5 Practice Tests (2026)*](https://www.udemy.com/course/databricks-genai-engineer-associate-5-practice-tests-2026/?referralCode=48CC75361435DC8F7F48) *— Five practice tests covering Mosaic AI, RAG, model serving, and GenAI workflows on Databricks*
> 
> *These tests are designed to challenge you in the same way the real exam will.*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ivwMsp0wQMeqPZntgFJBhA.png)

## OPTIMIZE: Compacting Small Files

[OPTIMIZE](https://docs.databricks.com/aws/en/delta/optimize) is the direct fix: it bin-packs small files into larger ones.

```c
OPTIMIZE main.sales.orders;
OPTIMIZE main.sales.orders WHERE order_date >= '2026–07–01'; - just a slice
OPTIMIZE main.sales.orders FULL; - rewrite everything
```

Three things to know about it:

- **It is idempotent.** Running it twice does nothing extra. There is no “too often” — it only compacts what needs compacting
- **The *WHERE* clause** limits work to a slice, but only on partition or clustering columns — useful for daily maintenance of just the fresh data
- **It does not free storage by itself.** The old small files stay behind for time travel until VACUUM removes them past retention. OPTIMIZE makes reads fast; VACUUM reclaims space. Two different jobs

There is also a preventive layer: **optimized writes** and **auto compaction** (*delta.autoOptimize.optimizeWrite* and *delta.autoOptimize.autoCompact*) shape files as they are written, so fewer small files exist in the first place. On modern Databricks, these are largely enabled where they matter — MERGE targets, SQL warehouse writes — and the *auto* compaction mode tunes target sizes dynamically. Know they exist; you rarely need to touch them.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*VR7I-3YnuhCcOlODAY3B_g.png)

## Liquid Clustering: The Modern Layout

Compaction fixes file size. Clustering fixes file contents — which rows live together, so queries can skip the files that cannot match. And in 2026, the answer to “how should I lay out my table?” is one thing: [**liquid clustering**](https://docs.databricks.com/aws/en/delta/clustering).

```c
-- at creation
CREATE TABLE main.sales.events (
 event_id BIGINT, event_date DATE, user_id STRING
) CLUSTER BY (event_date, user_id);
 
-- on an existing table (affects future writes; 
-- run OPTIMIZE FULL to re-layout old data)
ALTER TABLE main.sales.events CLUSTER BY (event_date, user_id);
OPTIMIZE main.sales.events FULL;
```

Databricks explicitly recommends liquid clustering for all new tables, replacing both partitioning and ZORDER. Why it won: it adapts. Partitioning locked you into a physical directory layout that was painful to change and catastrophic to get wrong. Liquid clustering co-locates related rows flexibly, redefines keys with a single ALTER, and never creates the tiny-partition explosion that ruined so many tables.

Choosing keys is simple: **cluster on the columns you actually filter and join by**, up to four, and fewer is usually better. Not the highest-cardinality columns — the most queried ones.

Better yet, you can delegate the choice entirely:

```c
CREATE OR REPLACE TABLE main.sales.events CLUSTER BY AUTO;
```

***CLUSTER BY AUTO*** (GA, on Unity Catalog managed tables with predictive optimization) watches your actual query patterns — which predicates, which joins — and selects and adjusts clustering keys itself, only re-clustering when the predicted benefit outweighs the cost. This is the “stop thinking about layout” option, and for most managed tables it is the right default.

And if you have an old partitioned table? Runtime 18.1 made the migration one statement:

```c
ALTER TABLE main.sales.legacy_events 
REPLACE PARTITIONED BY WITH CLUSTER BY (event_date);
OPTIMIZE main.sales.legacy_events;
```

One protocol note: enabling liquid clustering also enables deletion vectors and row tracking, which bumps the table protocol — very old clients will not be able to read the table.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_wu3pMZ1L6muFJCnFRbzYA.png)

## ZORDER and Partitioning: The Old Ways

You will still meet both of these in the wild, so let me give you the honest 2026 position on each.

**ZORDER** was the previous co-location technique: ***OPTIMIZE t ZORDER BY (col)***. It worked, but it was not idempotent, degraded with more columns, and had to be re-run manually forever. Liquid clustering supersedes it, and the two **cannot coexist** on one table. If you inherit a ZORDER table, the migration is exactly what you would guess: ***ALTER TABLE t CLUSTER BY (\<the former zorder columns>)***, then ***OPTIMIZE t FULL***. Do not use ZORDER on new tables.

**Partitioning** deserves more nuance, because it was ***the*** standard for a decade. The current guidance is blunt: **do not partition tables under 1 TB**, and every partition should hold at least 1 GB. Most tables people partition by date should never have been partitioned at all — unpartitioned Delta tables even get ingestion-time clustering automatically, which provides similar date-locality for free. Over-partitioning is the single most common self-inflicted performance wound I see, and until recently it was miserable to undo.

Where partitioning still earns its place is not performance but **operational boundaries** — genuinely huge tables (100 TB+), or hard isolation lines where you must drop or manage whole slices independently, such as per-jurisdiction data. If that is not your situation, cluster instead.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*8vqZkXqlWTbnR7W-q7UR4A.png)

## VACUUM: Reclaiming Storage

Everything that rewrites files — OPTIMIZE, MERGE, overwrites — leaves the old files behind for time travel. [VACUUM](https://docs.databricks.com/aws/en/tables/operations/vacuum) is what finally deletes the unreferenced ones once they age past retention:

```c
VACUUM main.sales.orders; -- removes unreferenced files older than retention (7 days default)
VACUUM main.sales.orders DRY RUN; -- preview what would be deleted
VACUUM main. sales.orders LITE; -- faster: uses the transaction log instead of listing storage
```

Skip it and nothing breaks — storage just grows forever, and you pay for every stale gigabyte. As we covered in the \[time travel article\](12-time-travel.md), retention is the balance point: keep files long enough for the history you need, not so long that storage bloats.

A reminder of the **Runtime 18 change**, because it kills a decade of old snippets: ***VACUUM t RETAIN 168 HOURS*** no longer does anything — the RETAIN argument is ignored. Retention is controlled by the table property now:

```c
ALTER TABLE main.sales.orders
SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 14 days');
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*b1K5XQfbT5tNRJkV0i_yKA.png)

## Predictive Optimization: Maintenance on Autopilot

Here is the 2026 plot twist to this whole article: for a growing share of tables, **you do not run any of these commands yourself.**

[Predictive optimization](https://docs.databricks.com/aws/en/optimizations/predictive-optimization) is GA and enabled by default for newer accounts (with the rollout to older accounts completing through 2026). On Unity Catalog managed tables, it automatically runs OPTIMIZE, VACUUM, and statistics collection — and, paired with ***CLUSTER BY AUTO***, even chooses and maintains clustering keys. It watches how each table is actually used and schedules maintenance where it pays off, skipping it where it would not.

This reframes what “table maintenance” means:

- **Unity Catalog managed tables** → maintenance is automated. Your job is to confirm predictive optimization is on and then stop hand-tuning. Manual OPTIMIZE schedules on these tables are usually wasted or redundant work
- **External tables** → still entirely on you. Predictive optimization does not touch them. If you use external tables, schedule OPTIMIZE and VACUUM yourself, forever

This is also one more quiet argument for managed tables, adding to the list from earlier articles. The platform can only maintain what it manages.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*F9yoiQlUqItfb0wGCdZGPQ.png)

## Data Skipping and Statistics

One more lever, subtler but worth knowing. Delta collects min/max statistics per file — the same statistics that power the file-skipping we met back in the \[data formats article\](07-data-formats.md). By default, stats are collected on the **first 32 columns** of the table.

Two practical consequences:

- **Column order matters.** If the column you always filter by sits at position 40, it has no stats and no skipping. Keep filter columns early in the schema — or better, set the stats columns explicitly:
```c
ALTER TABLE main.sales.orders
SET TBLPROPERTIES ('delta.dataSkippingStatsColumns' = 'order_date,customer_id,status');
```
- **Long text columns are dead weight in stats.** A ***description*** column full of paragraphs adds stats-collection cost and skips nothing. Exclude such columns from the stats list.

If you change these settings on an existing table, recompute with ***ANALYZE TABLE t COMPUTE DELTA STATISTICS***. On managed tables, the query-optimizer statistics themselves are yet another thing predictive optimization keeps fresh for you.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*GY-gf4h-eFhrstAbingKPg.png)

## Deletion Vectors and Physical Deletes

We met deletion vectors in \[Delta Lake in Practice\](08-delta-lake-in-practice.md): instead of rewriting a whole Parquet file to delete three rows, Delta marks them in a bitmap and readers apply it on the fly. Fast deletes, deferred rewriting.

The flip side: the “deleted” rows are still physically present in the files. Usually that is fine. But for compliance — a GDPR erasure request, say — “marked deleted” is not “gone.” When the bytes must actually disappear, you purge:

```c
REORG TABLE main.sales.customers APPLY (PURGE);
```

This rewrites just the files that carry deletion vectors, materializing the deletes. Then the old files still need to age past retention and be VACUUMed before the data is physically gone from storage. So the full erasure chain is: **DELETE → REORG APPLY (PURGE) → retention passes → VACUUM.** If you handle personal data, write that sequence down — the gap between logical and physical deletion is exactly the kind of detail an auditor asks about.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*6xvjR7jMUefx5Ip8BOjD_A.png)

## The Five-Minute Table Health Check

Let me tie it all together into the workflow I actually use when someone says “this table is slow.”

### Step 1 — measure the files:

```c
DESCRIBE DETAIL main.sales.orders;
-- look at: numFiles, sizeInBytes, clusteringColumns, partitionColumns
```

Divide ***sizeInBytes*** by ***numFiles***. If the average file is well under ~128 MB and there are thousands of files, you have found the problem. While you are there, note whether the table has clustering keys, legacy partitions, or neither.

### Step 2 — check the maintenance story:

```c
DESCRIBE HISTORY main.sales.orders;
-- when did OPTIMIZE or VACUUM last run? What does the write pattern look like?
```

A table with hourly tiny appends and no OPTIMIZE in its history tells you everything.

### Step 3 — fix in order:

1. **Managed table?** Confirm predictive optimization is enabled. If it is, the small-files problem will heal itself — and your manual tuning is probably interference
2. **No layout, or legacy partitions?** ***ALTER TABLE … CLUSTER BY (…)*** (or ***CLUSTER BY AUTO***, or ***REPLACE PARTITIONED BY WITH CLUSTER BY*** for partitioned tables), then ***OPTIMIZE … FULL*** once
3. **External table?** Schedule OPTIMIZE and VACUUM — daily is a fine start
4. **Still slow?** Check that your real filter columns are covered by statistics, and set ***dataSkippingStatsColumns*** if not

That sequence resolves the overwhelming majority of “slow Delta table” complaints I have ever seen.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Q6Lpo1i-b05TgDBNEB2WbA.png)

## Common Mistakes to Avoid

- **Partitioning small tables.** Under 1 TB, do not partition — cluster. Over-partitioning creates exactly the small-files problem you were trying to avoid
- **Using ZORDER on new tables.** It is the previous generation. Liquid clustering replaces it, and they cannot be mixed
- **Choosing clustering keys by cardinality instead of usage.** Cluster on what you filter and join by. A unique ID nobody filters on is a useless key
- **Hand-scheduling OPTIMIZE on managed tables.** Predictive optimization already does it, with better timing than your cron job. Check before you duplicate work
- **Never vacuum external tables.** Nobody else will. Storage grows silently until the bill arrives
- **Expecting *VACUUM … RETAIN* to work on Runtime 18.** It is ignored now — set ***delta.deletedFileRetentionDuration*** instead
- **Assuming DELETE means the data is physically gone.** With deletion vectors, it is not. For compliance erasure: REORG APPLY (PURGE), then VACUUM after retention
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PMVGEmOxR5R3Vimoxi7Fsg.png)

## Frequently Asked Questions

### Why is my Delta table slow?

Most often because of the small files problem: many small files created by streaming or frequent writes, each adding listing and metadata overhead. Run ***DESCRIBE DETAIL*** and divide ***sizeInBytes*** by ***numFiles*** — if the average file is far below ~128 MB, compact with OPTIMIZE and add liquid clustering.

### What does OPTIMIZE do in Databricks?

OPTIMIZE compacts small files into larger ones (bin-packing), and on liquid clustering tables it also clusters the data by your keys. It is idempotent — safe to run repeatedly — and it does not delete old files; VACUUM does that separately.

### Should I use liquid clustering or partitioning?

Liquid clustering, for almost every table. Databricks recommends it for all new tables instead of partitioning and ZORDER. Do not partition tables under 1 TB. Partitioning remains sensible mainly for very large tables or hard operational boundaries, like per-jurisdiction data isolation.

### What is CLUSTER BY AUTO?

Automatic liquid clustering: Databricks analyzes your actual query patterns and chooses (and updates) the clustering keys itself. It is GA and requires a Unity Catalog managed table with predictive optimization enabled. For most managed tables, it is the easiest correct choice.

### Do I still need to run OPTIMIZE and VACUUM manually?

On Unity Catalog managed tables, usually not — predictive optimization runs OPTIMIZE, VACUUM, and statistics automatically and is on by default for newer accounts. On external tables, yes: predictive optimization does not cover them, so schedule maintenance yourself.

### How do I migrate a ZORDER or partitioned table to liquid clustering?

For ZORDER: ***ALTER TABLE t CLUSTER BY (your former ZORDER columns)***, then ***OPTIMIZE t FULL***. For partitioned tables on Runtime 18.1+: ***ALTER TABLE t REPLACE PARTITIONED BY WITH CLUSTER BY (cols)*** — or ***WITH CLUSTER BY AUTO*** — then run OPTIMIZE to re-layout existing data.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nzaaBoIn2NB8iFu4i8w72w.png)

## What Is Next

With this article, you have the complete Delta Lake toolkit: formats, tables, upserts, history, schemas, ingestion, time travel, and now performance. That closes **Part II** of the series.

Next we open **Part III: Data Engineering on Databricks** — and it starts where every real project starts: **structuring a Databricks project from scratch**. Repositories, notebooks vs modules, configuration, environments — the unglamorous decisions that decide whether your platform is maintainable two years from now.

Make sure to bookmark this series so you do not miss any upcoming articles.

*Want more? Visit* [*mbvyn.com*](https://mbvyn.com/) *for mentorship, consulting, and all my content in one place. And if you work with Parquet files, try* [*parquetreader.app*](https://parquetreader.app/) *— my free tool for exploring them on the desktop.*