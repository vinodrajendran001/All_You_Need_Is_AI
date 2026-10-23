---
title: "Understanding Databricks: Time Travel in Delta Lake"
source: "https://mbvyn.medium.com/understanding-databricks-time-travel-in-delta-lake-42e45b34de83"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-08-08
created: 2026-10-23
description: "Query the past, undo mistakes, and know exactly how far back you can go. Updated July 2026."
tags:
  - "clippings"
---
## Query the past, undo mistakes, and know exactly how far back you can go. Updated July 2026.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5kEQPa-RNKd6zmyEay-jmw.png)

Sooner or later it happens to everyone. A DELETE without a WHERE clause. A MERGE that matched the wrong rows. A 3 am job that overwrote a production table with garbage. And then the cold feeling: **is the data gone?**

On a Delta table, the answer is usually no — because Delta never really forgets. Every write creates a new version of the table, and time travel lets you query any of those versions, compare them, and restore the one you want back. It has saved me more than once, and knowing how it works — including its limits — is one of the highest-value skills in this whole series.

In this article, I will show you how time travel actually works, how to query the past, how to undo a bad write with RESTORE, and — critically — the retention rules that decide how far back you can go. That last part matters more than ever, because Databricks Runtime 18 changed the retention behavior in 2026, and most older tutorials are now wrong about it.

This article is part of the **Understanding Databricks** series and builds on [Delta Lake in Practice](https://medium.com/@mbvyn/understanding-databricks-delta-lake-in-practice-create-append-and-merge-18b58f8f50c9), where we first touched on table history.

### Key takeaways

- Every write to a Delta table creates a new **version**. Time travel queries the table as it existed at any past version or timestamp:  
	*SELECT \* FROM t VERSION AS OF 41*.
- **DESCRIBE HISTORY** shows every version — who did what, when, and how many rows it touched.
- **RESTORE** rolls the table back to a past version by creating a **new** version — history is never rewritten.
- **Time travel** is bounded by retention: **7 days of files** (*delta.deletedFileRetentionDuration*) and **30 days of history** (*delta.logRetentionDuration*) by default.
- **VACUUM** enforces the file limit.
- **2026 change:** on Databricks Runtime 18, time travel past the file retention window is hard-blocked, and *VACUUM … RETAIN n HOURS* is ignored — retention is controlled by table properties now.
- Time travel is not a backup. For real backups, use DEEP CLONE or external copies.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AE6oh4Em3GhivfyxnCDPPg.png)

## How Time Travel Works

Time travel falls out of Delta’s design almost for free, and once you see why, the feature stops being magic.

Remember from earlier articles: a Delta table is a folder of Parquet files plus a transaction log (*\_delta\_log*). Every operation — INSERT, UPDATE, DELETE, MERGE, OPTIMIZE — writes a new commit to that log, recording exactly which data files were **added** and which were **removed**. Each commit is a numbered **version**, starting from 0.

Here is the key insight: when Delta “deletes” data, it does not physically erase the old Parquet files. It just records in the log that those files are no longer part of the current version. The files sit in storage, unreferenced but intact.

So time travel is simply this: pick a past version, replay the log up to that point to work out which files were “live” then, and read those files. You get a complete snapshot of the table exactly as it existed — same rows, same schema, same everything.

That also explains time travel’s one hard limit, which we will get to: it only works while the old files still exist. And the thing that removes old files is VACUUM.

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

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*uyb3tGraXre1IQg5G4YCdA.png)

## Querying the Past

There are two ways to point at a past state: by version number or by timestamp.

### By version:

```c
SELECT * 
FROM main.sales.customers 
VERSION AS OF 41;
```

### By timestamp

Delta resolves it to the latest version committed at or before that moment:

```c
SELECT * 
FROM main.sales.customers 
TIMESTAMP AS OF '2026–07–20T00:00:00Z';

SELECT * 
FROM main.sales.customers 
TIMESTAMP AS OF current_timestamp() - INTERVAL 12 HOURS;
```

There is also a compact *@* syntax that works anywhere a table name does — handy in tools that do not like extra clauses:

```c
SELECT * 
FROM main.sales.customers@v41;
```

In PySpark, the same two options:

```c
df = spark.read.option("versionAsOf", 41).table("main.sales.customers")
df = spark.read.option("timestampAsOf", "2026–07–20") \
     .table("main.sales.customers")
```

One pattern I use constantly: **diffing two versions**. Read both into DataFrames and subtract:

```c
before = spark.read.option("versionAsOf", 41).table("main.sales.customers")
after = spark.read.option("versionAsOf", 42).table("main.sales.customers")
before.exceptAll(after).show() # rows that disappeared in version 42
```

That one snippet answers “what exactly did that job change?” in seconds. It is the fastest debugging tool I know on Databricks.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*RwECXnIeb4Ua1qPzH08P-g.png)

## DESCRIBE HISTORY: The Story of Your Table

Before you can travel to a version, you need to know which version to travel to. That is what [DESCRIBE HISTORY](https://docs.databricks.com/aws/en/delta/history) is for — it shows the full audit trail of the table:

```c
DESCRIBE HISTORY main.sales.customers;
```

Every row is one version, with the columns that matter:

- **version** and **timestamp** — the version number and when it was committed
- **userName** — who ran the operation. Yes, it names names
- **operation** — WRITE, DELETE, UPDATE, MERGE, RESTORE, OPTIMIZE
- **operationParameters** — the details, like the predicate of a DELETE
- **operationMetrics** — how many rows and files were affected (*numDeletedRows*, *numOutputRows*, and so on)

Because the output is a table, you can filter it. Looking for the DELETE that ruined your morning?

```c
SELECT version, timestamp, userName, operationParameters
FROM (DESCRIBE HISTORY main.sales.customers)
WHERE operation = 'DELETE';
```

In Python, *DeltaTable.forName(spark, “main.sales.customers”).history()* gives you the same thing as a DataFrame. Beyond debugging, this is a genuine audit log — who changed what and when, for free, on every Delta table.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*vnzgfrTdJMe2mZdjBPVrlw.png)

## RESTORE: The Undo Button

Querying the past is nice. Putting the table **back** is what saves your day.

```c
RESTORE TABLE main.sales.customers TO VERSION AS OF 41;
RESTORE TABLE main.sales.customers TO TIMESTAMP AS OF '2026–07–20 00:00:00';
```

Or in Python:

```c
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "main.sales.customers")
dt.restoreToVersion(41)
```

Here is the elegant part: [**RESTORE**](https://docs.databricks.com/aws/en/sql/language-manual/delta-restore) **does not rewrite history.** It creates a **new** version whose content equals the past version you chose — a metadata operation that re-adds the old files and removes the current ones. If your table was at version 42 when you restored to 41, you are now at version 43, and **DESCRIBE HISTORY** shows all of it, including the **RESTORE** itself. Nothing is hidden, nothing is lost, and if the restore itself was a mistake, you can restore forward again.

The one requirement: the files of the target version must still exist. Which brings us to the fine print.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*XzhcNyHhVx8xoDpg49Vf5g.png)

## Retention: How Far Back Can You Actually Go?

This is the section that separates people who **think** they understand time travel from people who actually do. Two independent clocks limit your reach into the past:

- [**delta.deletedFileRetentionDuration**](https://docs.databricks.com/aws/en/tables/operations/vacuum) — default ***7 days***. How long unreferenced Parquet files are kept before VACUUM is allowed to delete them. This is the **real** time travel limit, because no files means no snapshot
- **delta.logRetentionDuration** — default **30 days**. How long history entries are kept in the transaction log

Notice the mismatch: with defaults, ***DESCRIBE HISTORY*** can show you versions from three weeks ago that you **cannot actually query**, because their files were vacuumed after seven days. History visibility and queryability are two different windows. This is the classic trap.

**And here is what changed in 2026.** Databricks Runtime 18 made the rules stricter, and this is where older tutorials will mislead you:

- Time travel past the file retention window is now **hard-blocked** — even if the log still references the version, the query fails. Previously you could sometimes get lucky if the files happened to survive
- ***VACUUM t RETAIN 100 HOURS*** no longer does what you think. The RETAIN argument is now ignored (except ***RETAIN 0 HOURS***). Retention is controlled by the table property, not the command
- The log retention must now be **at least as long** as the file retention — you cannot set them inconsistently

So if you need more than a week of queryable history — for audit, compliance, or just peace of mind — set it explicitly on the table:

```c
ALTER TABLE main.sales.customers SET TBLPROPERTIES (
 'delta.deletedFileRetentionDuration' = 'interval 30 days',
 'delta.logRetentionDuration' = 'interval 30 days'
);
```

The trade-off is honest and simple: longer retention means old files sit in storage longer, and storage costs money. Decide the window your business actually needs, set it deliberately, and remember that predictive optimization runs VACUUM automatically on managed tables — the defaults are being enforced whether you run VACUUM by hand or not.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Vycp6p43TkFZHOI83q9Fvw.png)

## Time Travel vs Change Data Feed

A quick clarification, because these two features get confused. Time travel gives you **full snapshots** — the whole table as it was at a moment. Sometimes you want something different: only the **rows that changed** between versions. That is the **Change Data Feed (CDF).**

```c
ALTER TABLE main.sales.customers 
SET TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

SELECT * 
FROM table_changes('main.sales.customers', 41, 42);
```

CDF returns each changed row with ***\_change\_type*** (insert, delete, update\_preimage, update\_postimage), ***\_commit\_version***, and ***\_commit\_timestamp***. It is the tool for propagating incremental changes downstream — feeding a Silver table only what changed in Bronze, for example.

The rule of thumb: **”what did the table look like?” is time travel.**

**“Which rows changed?” is CDF.** One caveat — CDF must be enabled **before** the changes you care about happen. Time travel works retroactively (within retention); CDF does not.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*iEJZ6jceroc-hQA6U4kB3Q.png)

## Clones: Snapshots You Can Keep

Time travel plus one more feature gives you something powerful: point-in-time copies of a table.

```c
-- a cheap, instant test copy (no data copied - references source files)
CREATE TABLE main.dev.customers_test SHALLOW CLONE main.sales.customers;

-- a full, independent copy of the table as it was at version 41
CREATE TABLE main.backup.customers_v41 
DEEP CLONE main.sales.customers VERSION AS OF 41;
```

**SHALLOW CLONE** copies only metadata and points at the source’s files — instant and nearly free, perfect for testing changes against production data without touching it. Just know that it depends on the source’s files: if the source gets vacuumed, the shallow clone can break.

**DEEP CLONE** physically copies the data, giving you an independent table. Combined with ***VERSION AS OF***, this is how you make a real point-in-time backup — one that survives VACUUM, survives retention, and survives someone dropping the source table.

Which leads to the most important sentence in this article: **time travel is not a backup.** The history lives inside the same table, in the same storage. Retention eats it after days, and a dropped table takes its history with it. For anything you truly cannot lose, take a DEEP CLONE or an external copy. Time travel is a seatbelt, not insurance.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tq5vQ3hvDGuRYsvPYsMDLg.png)

## End to End: Recovering From an Accidental DELETE

Here is the full recovery flow, the one worth bookmarking. Someone just deleted all EU customers by mistake.

**Step 1 — find out what happened:**

```c
DESCRIBE HISTORY main.sales.customers;
-- version 42: operation = DELETE, operationParameters shows predicate region = 'EU'
-- version 41: the last good state
```

**Step 2 — confirm the good version still has the data:**

```c
SELECT count(*) 
FROM main.sales.customers VERSION AS OF 41 WHERE region = 'EU';
-- 18,204 rows. They are still there.
```

**Step 3 — restore:**

```c
RESTORE TABLE main.sales.customers TO VERSION AS OF 41;
```

**Step 4 — verify:**

```c
SELECT count(*) 
FROM main.sales.customers 
WHERE region = 'EU'; -- 18,204 

DESCRIBE HISTORY main.sales.customers LIMIT 1; -- operation = RESTORE
```

Four commands, maybe two minutes, and the incident is over — with a full audit trail of both the mistake and the fix. The first time you do this in a real incident, this article pays for itself.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*CmjZEuECC3TpNjqxyiN4Nw.png)

## Common Mistakes to Avoid

- **Assuming history is infinite.** By default, you can **query** about 7 days back and **see** 30 days of history. Past that, versions are gone. Plan retention deliberately
- **Confusing the two retention settings.** ***logRetentionDuration*** controls what DESCRIBE HISTORY shows; ***deletedFileRetentionDuration*** controls what you can actually query. History listing a version does not mean you can read it
- **Running VACUUM and then needing the versions it removed.** VACUUM permanently deletes unreferenced files past retention. Before vacuuming aggressively, ask whether anyone needs those versions
- Relying on ***VACUUM … RETAIN n HOURS*** on Runtime 18. It is ignored now. Set ***delta.deletedFileRetentionDuration*** on the table instead
- **Using time travel as a backup strategy.** Same table, same storage, time-limited. Use DEEP CLONE or external backups for anything critical
- **Forgetting shallow clones depend on the source.** VACUUM the source table, and your shallow clone may start throwing file-not-found errors
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*DaKF1fMonQGS0b1pkOAoVQ.png)

## Frequently Asked Questions

### What is time travel in Delta Lake?

Time travel is Delta Lake’s ability to query a table as it existed at a past version or timestamp. Every write creates a new table version recorded in the transaction log, and old data files are kept (until retention expires), so you can read a complete snapshot of any retained version with ***VERSION AS OF*** or ***TIMESTAMP AS OF***.

### How do I query a previous version of a Delta table?

**In SQL**: ***SELECT \* FROM my\_table VERSION AS OF 41*** or ***TIMESTAMP AS OF ‘2026–07–20’***.

**In PySpark**: ***spark.read.option(“versionAsOf”, 41).table(“my\_table”)***. Use ***DESCRIBE HISTORY my\_table*** first to find the version you want.

### How do I undo a DELETE in Databricks?

Use RESTORE. Find the last good version with ***DESCRIBE HISTORY***, confirm it with a time-travel query, then run ***RESTORE TABLE my\_table TO VERSION AS OF n***. The restore creates a new version with the old content — history is preserved, including a record of the restore itself.

### How far back does Delta time travel go?

By default, about 7 days — that is the ***delta.deletedFileRetentionDuration***, after which VACUUM may remove the old files. History metadata is kept 30 days by default, but a version is only queryable while its files exist. On Databricks Runtime 18, queries past the file retention window are hard-blocked. You can extend both windows with table properties.

### Does RESTORE delete the table’s history?

No. RESTORE creates a new version whose content matches the target version. All previous versions, including the bad write and the restore operation itself, remain visible in DESCRIBE HISTORY. You can even restore forward again if the restore was a mistake.

### Is Delta time travel a backup?

No. The version history lives in the same table and storage as the data, is limited by retention, and disappears if the table is dropped. For real backups, create a DEEP CLONE (optionally of a specific version) or copy data to separate storage.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*nzaaBoIn2NB8iFu4i8w72w.png)

## What Is Next

You now have the safety net under everything else you do with Delta — the ability to see the past and put it back. In the next article, we close out the Delta Lake fundamentals with **optimizing Delta tables** — OPTIMIZE, liquid clustering, VACUUM strategy, and the settings that keep your tables fast as they grow.

Make sure to bookmark this series so you do not miss any upcoming articles.

*Want more? Visit* [*mbvyn.com*](https://mbvyn.com/) *for mentorship, consulting, and all my content in one place. And if you work with Parquet files, try* [*parquetreader.app*](https://parquetreader.app/) *— my free tool for exploring them on the desktop.*