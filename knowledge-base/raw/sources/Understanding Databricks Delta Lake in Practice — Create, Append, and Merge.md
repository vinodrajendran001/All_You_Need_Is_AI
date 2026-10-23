---
title: "Understanding Databricks: Delta Lake in Practice — Create, Append, and Merge"
source: "https://mbvyn.medium.com/understanding-databricks-delta-lake-in-practice-create-append-and-merge-18b58f8f50c9"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-07-11
created: 2026-10-23
description: "A hands-on guide to working with Delta tables, with copy-pasteable code."
tags:
  - "clippings"
---
## A hands-on guide to working with Delta tables, with copy-pasteable code.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Q8PK-XS0g7N3mpzfjTOI1w.png)

In the last article, we learned what Delta Lake is — a table format built on top of Parquet that adds a transaction log and turns a folder of files into a real, reliable table. That was the theory. Now we get our hands dirty.

This is a practical, code-first guide. By the end, you will know how to create Delta tables, load data into them the right way, update and delete rows, handle the dreaded upsert with MERGE, and evolve your schema without breaking anything. Every example is copy-pasteable in both SQL and PySpark and works on current Databricks (Delta Lake 4.x, Runtime 18).

If you learn best by doing, open a notebook and follow along. This is the article where Delta stops being an idea and becomes a tool you actually use.

This article is part of the **Understanding Databricks** series. Follow up to read more.

## Key takeaways

- On Databricks, every table is a Delta table by default — \`USING DELTA\` is optional. Tables live in a three-level namespace: \`catalog.schema.table\`.
- Use **append** to add rows, **overwrite** to replace all data, and **replaceWhere** to atomically replace a slice (like one day) without touching the rest.
- **MERGE** is the upsert workhorse: update matching rows, insert new ones, and delete in a single statement. Always deduplicate your source first.
- **Schema enforcement** rejects bad-shaped data on write; **schema evolution** (\`mergeSchema\`) lets you add columns on purpose. Enable it per write, not session-wide.
- On managed tables, **predictive optimization** runs OPTIMIZE and VACUUM for you. Use **liquid clustering** instead of partitioning for new tables.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PfCYARZ5xHIoj_Nwq1--_Q.png)

## Creating Delta Tables

On Databricks, creating a Delta table is refreshingly simple because Delta is the default. Unless you say otherwise, every table you create is a Delta table — so \`USING DELTA\` is optional (though I keep it in open-source Spark or when I want to be explicit).

Tables live in Unity Catalog’s three-level namespace: \`catalog.schema.table\`. Here is the basic SQL:

```c
CREATE TABLE IF NOT EXISTS main.sales.orders (
order_id BIGINT,
customer_id BIGINT,
amount DECIMAL(10,2),
status STRING,
order_date DATE
);
```

In PySpark, you write a DataFrame straight to a table:

```c
df.write.saveAsTable("main.sales.orders")
# equivalent, explicit form:
df.write.format("delta").saveAsTable("main.sales.orders")
```

You can also create a table directly from existing data with CTAS (create table as select):

```c
CREATE OR REPLACE TABLE main.sales.orders AS
SELECT * FROM read_files('/Volumes/main/sales/landing/orders.csv',
format => 'csv', header => true);
```

**Managed vs external — know the difference.** A managed table lets Unity Catalog handle storage; an external table points at a location you manage with a \`LOCATION\` clause. The difference bites you at DROP time: dropping a **managed** table deletes its data files (after a recovery window); dropping an **external** table only removes the metadata and leaves the files sitting in storage. Databricks recommends managed tables as the default — they are cheaper, faster, and get automatic optimization. Use external tables only when you have a specific reason to control the storage location yourself.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*s187Jnm6AwoOSVLHHF3OZg.png)

## Appending and Overwriting Data

Once a table exists, you load data into it. There are two basic modes, and mixing them up is one of the most common — and most painful — mistakes in data engineering.

**Append** adds new rows, leaving existing data untouched. This is your everyday incremental load:

```c
df.write.mode("append").saveAsTable("main.sales.orders")
```
```c
INSERT INTO main.sales.orders SELECT * FROM staging_orders;
```

**Overwrite** replaces *all* the data in the table. Use it for full refreshes:

```c
df.write.mode("overwrite").saveAsTable("main.sales.orders")
```
```c
INSERT OVERWRITE main.sales.orders SELECT * FROM staging_orders;
```

Be careful here. With \`saveAsTable\`, an accidental \`overwrite\` silently wipes your table and replaces it. I have seen a one-word mistake erase a production table. When in doubt, append.

There is a smarter middle option: **replaceWhere** atomically replaces just a slice of the table — say, reloading a single day — without touching the rest:

```c
(
replace_df.write.mode("overwrite")
.option("replaceWhere", "order_date >= '2026–06–01' AND order_date < '2026–07–01'")
.saveAsTable("main.sales.orders")
)
```

This is perfect for idempotent daily loads: reprocess a day, and only that day’s rows get replaced. Clean and safe.

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

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KYKlzfAnyZE2zvLUUXOx-A.png)

## MERGE: One Statement to Rule Them All

MERGE is the operation that plain Parquet cannot do, and the reason Delta exists for so many teams. It is the **upsert** — in a single statement, you update rows that match, insert rows that are new, and optionally delete rows that are gone. This is how you keep a table in sync with a changing source.

Here is a realistic customer sync in SQL, using all three clause families:

```c
MERGE INTO customers AS target
USING customer_updates AS source
ON target.customer_id = source.customer_id
WHEN MATCHED AND source.op = 'DELETE' THEN DELETE
WHEN MATCHED THEN UPDATE SET
target.name = source.name,
target.email = source.email,
target.updated_at = source.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, name, email, updated_at)
VALUES (source.customer_id, source.name, source.email, source.updated_at)
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

Read it top to bottom: if a customer exists and is marked deleted, remove them; if they exist, update their details; if they are new, insert them; and if a customer is in the target but no longer in the source, delete them. One statement, full synchronization.

The same thing in PySpark:

```c
from delta.tables import DeltaTable

(
DeltaTable.forName(spark, "customers").alias("target")
.merge(source=updates_df.alias("source"),
condition="target.customer_id = source.customer_id")
.whenMatchedDelete(condition="source.op = 'DELETE'")
.whenMatchedUpdate(set={"name": "source.name", "email": "source.email",
"updated_at": "source.updated_at"})
.whenNotMatchedInsert(values={"customer_id": "source.customer_id",
"name": "source.name", "email": "source.email",
"updated_at": "source.updated_at"})
.whenNotMatchedBySourceDelete()
.execute()
)
```

**The one gotcha that will bite you.** If two rows in your source match the same target row, MERGE throws an error — it does not know which one wins. This happens constantly with change feeds that contain several updates for the same key. The fix is to deduplicate the source first, keeping only the latest row per key:

```c
from pyspark.sql import Window
from pyspark.sql.functions import col, row_number

w = Window.partitionBy("customer_id").orderBy(col("updated_at").desc())

updates_df = (updates_df
.withColumn("rn", row_number().over(w))
.filter("rn = 1")
.drop("rn"))
```

Make deduplication a reflex. Every MERGE from a change feed should start with it.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0oVJbT8jlY6XsNoWnLGiXw.png)

## Updating and Deleting Rows

Sometimes you do not need a full merge — you just need to change or remove some rows. Delta makes this feel like a normal database, which is exactly the point.

```c
UPDATE main.sales.orders SET status = 'shipped' WHERE order_id = 42;
DELETE FROM main.sales.orders WHERE order_date < '2025–01–01';
```

In PySpark:

```c
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "main.sales.orders")
dt.update(condition="status = 'pending'", set={"status": "'cancelled'"})
dt.delete("order_date < '2025–01–01'")
```

Here is what makes this fast on modern Delta. With **deletion vectors** enabled, an UPDATE or DELETE does not rewrite entire Parquet files to change a few rows. Instead, Delta marks the affected rows in a compact bitmap and applies it at read time — a “merge-on-read” approach. The heavy rewriting is deferred and later cleaned up by OPTIMIZE. This is why deletes and updates that used to be slow are now quick. One thing to remember: the data is not physically removed from storage until you run VACUUM.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-HOfF3mHD-g16SRqgtJaWA.png)

## Schema Enforcement and Evolution

This is where Delta protects you from yourself. **Schema enforcement** means Delta checks every write against the table’s schema and rejects anything that does not fit. If your incoming data has an unexpected extra column, or a type that cannot be safely cast, or a column name that only differs by case, the write fails — all or nothing, no partial mess. This is a feature, not an annoyance. It is what stops one bad file from quietly corrupting your table.

But sometimes you *want* to change the schema — you are adding a real new column. That is **schema evolution**, and you opt into it explicitly:

```c
# add new columns from the source on append
df.write.option("mergeSchema", "true").mode("append").saveAsTable("main.sales.orders")
```
```c
INSERT INTO main.sales.orders WITH SCHEMA EVOLUTION
SELECT * FROM source_with_new_column;
```

For MERGE, add \`WITH SCHEMA EVOLUTION\` between \`MERGE\` and \`INTO\`, or call \`.withSchemaEvolution()\` in Python.

**An important recommendation:** enable schema evolution per write, using the option shown above — not with a session-wide config. There is a Spark setting (\`spark.databricks.delta.schema.autoMerge.enabled\`) that turns it on for everything, but Databricks recommends against it because it can silently change schemas across unrelated jobs. Be deliberate. Evolve the schema where you mean to, not everywhere at once.

There is also **type widening** (now generally available) — you can safely widen a column’s type, say from INT to BIGINT or DECIMAL, without rewriting the data. Enable it with a table property:

```c
ALTER TABLE main.sales.orders SET TBLPROPERTIES ('delta.enableTypeWidening' = 'true');
```
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*XLqKglw2csXu_91iaitUZw.png)

## Reading Data and Time Travel

Reading a Delta table is just SQL, nothing special:

```c
SELECT * FROM main.sales.orders WHERE status = 'shipped';
```

But Delta has a superpower that plain tables do not: **time travel**. Because every write creates a new version, you can query the table as it looked in the past. This is priceless for debugging (“what did this table contain before last night’s job?”) and for auditing.

```c
SELECT * FROM main.sales.orders VERSION AS OF 12;
SELECT * FROM main.sales.orders TIMESTAMP AS OF '2026–06–01T00:00:00Z';
DESCRIBE HISTORY main.sales.orders;
```

\`DESCRIBE HISTORY\` shows you every version, who wrote it, and what operation it was. One caveat: time travel only reaches back as far as your VACUUM retention (7 days by default), because VACUUM is what removes the old files. We will go deep on time travel in a later article — for now, just know it is there and it will save you one day.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*NQ5-rw0stlv9_n2S7LwCXg.png)

## Keeping Your Tables Healthy

Delta tables need a little upkeep because streaming and frequent writes create many small files, which slow down reads. Two commands handle it:

```c
OPTIMIZE main.sales.orders; - compacts small files into bigger ones
VACUUM main.sales.orders; - removes old files past the 7-day retention
```

For laying out data so queries skip what they do not need, the modern answer is **liquid clustering**, not partitioning. Old advice said to partition your tables by date. In 2026, Databricks recommends liquid clustering for all new tables — it adapts to your query patterns and avoids the painful mistakes bad partitioning causes:

```c
CREATE TABLE main.sales.orders (order_id BIGINT, order_date DATE)
CLUSTER BY (order_date);
```

Here is the best part: on Unity Catalog-managed tables, **predictive optimization** runs OPTIMIZE, VACUUM, and clustering for you automatically. It is generally available and enabled by default for newer accounts. So for most managed tables, you do not run these commands by hand at all — Databricks handles maintenance in the background. You mainly need them for external tables, which are not covered by predictive optimization.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*90NMwkx8j6BHbWZo-3vTRA.png)

## Putting It All Together: An Orders Table

Let me tie every piece into one realistic flow. Imagine a daily orders pipeline.

**Create the table**, clustered by order date:

```c
CREATE TABLE IF NOT EXISTS main.sales.orders (
order_id BIGINT, customer_id BIGINT, amount DECIMAL(10,2),
status STRING, order_date DATE
) CLUSTER BY (order_date);
```

**Append** today’s new orders as they arrive:

```c
new_orders.write.mode("append").saveAsTable("main.sales.orders")
```

**Merge** in status updates from the source system, deduplicating first. New orders arrive through the append step above, so this MERGE only needs to update existing ones:

```c
from pyspark.sql import Window
from pyspark.sql.functions import col, row_number
from delta.tables import DeltaTable

# keep only the latest update per order
w = Window.partitionBy("order_id").orderBy(col("updated_at").desc())

updates = order_updates.withColumn("rn", row_number().over(w)).filter("rn = 1").drop("rn")
(
DeltaTable.forName(spark, "main.sales.orders").alias("t")
.merge(updates.alias("s"), "t.order_id = s.order_id")
.whenMatchedUpdate(set={"status": "s.status", "amount": "s.amount"})
.execute()
)
```

**Handle a schema change** when the source adds a discount column:

```c
orders_with_discount.write.option("mergeSchema", "true") \
.mode("append").saveAsTable("main.sales.orders")
```

**Check history and time-travel** to compare before and after:

```c
DESCRIBE HISTORY main.sales.orders;
SELECT * FROM main.sales.orders VERSION AS OF 3;
```

And maintenance? On a managed table, predictive optimization already handled it. That is the whole lifecycle — create, load, sync, evolve, inspect — in a handful of commands.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KA-y2kjqMcq5k2lYQDDdkA.png)

## Common Mistakes to Avoid

- **Overwriting when you meant to append.** With \`saveAsTable\`, one wrong mode wipes the table. Double-check every \`overwrite\`, and default to \`append\` when unsure
- **Merging without deduplicating the source.** Multiple source rows matching one target row throws an error. Always deduplicate to the latest row per key before a MERGE
- **Turning on schema evolution session-wide.** The \`autoMerge\` config silently changes schemas across jobs. Use the per-write \`mergeSchema\` option instead, so evolution is deliberate
- **Forgetting maintenance on external tables.** Predictive optimization covers managed tables, not external ones. If you use external tables, schedule OPTIMIZE and VACUUM yourself
- **Confusing managed and external tables.** Dropping a managed table deletes the data; dropping an external table leaves the files behind. Know which one you created before you DROP
- **Still partitioning by date out of habit.** For new tables, use liquid clustering instead — it adapts and avoids the small-partition problems partitioning creates
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*OkyW5S9v3bh9aldtrhBDNQ.png)

## Frequently Asked Questions

### How do I do an upsert in Delta Lake?

Use MERGE. It updates rows that match your join condition, inserts rows that do not, and can delete rows in the same statement. In SQL it is \`MERGE INTO target USING source ON condition WHEN MATCHED THEN UPDATE … WHEN NOT MATCHED THEN INSERT …\`. Always deduplicate your source to one row per key first, or MERGE will error on duplicate matches.

### What is the difference between append and overwrite?

Append adds new rows and leaves existing data alone — use it for incremental loads. Overwrite replaces all the data in the table — use it for full refreshes. To replace just part of a table (like a single day) atomically, use the \`replaceWhere\` option instead of a full overwrite.

### Do I have to run OPTIMIZE and VACUUM myself?

On Unity Catalog-managed tables, usually no. Predictive optimization runs OPTIMIZE, VACUUM, and clustering automatically, and it is on by default for newer accounts. You mainly run these commands manually on external tables, which predictive optimization does not cover.

### How do I add a new column to a Delta table?

Enable schema evolution on the write with \`.option(“mergeSchema”, “true”)\` in PySpark, or \`WITH SCHEMA EVOLUTION\` in SQL. Do it per write rather than turning on the session-wide auto-merge config, so you only change the schema when you intend to.

### Should I use a managed or external table?

Prefer managed tables. They are the Databricks default and recommendation — cheaper, faster, and automatically maintained by predictive optimization. Use external tables only when you have a specific reason to control the storage location yourself.

### Why does my MERGE fail with “multiple source rows matched”?

Because two or more rows in your source match the same target row, and Delta cannot tell which should win. Deduplicate the source first, keeping the latest row per key with a window function (\`row\_number()\` ordered by your timestamp, filtered to \`rn = 1\`).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KF4E05SztqpVtPH3iVgfQQ.png)

## What Is Next

You can now create, load, update, and synchronize Delta tables — the core of daily data engineering work. In the next article, we go deeper into one of Delta’s most powerful patterns: **Slowly Changing Dimensions (SCD Type 1 and Type 2)** — how to track history in your tables, and how Delta’s MERGE and AUTO CDC make it straightforward.

Make sure to bookmark this series so you do not miss any upcoming articles.

*Want more? Visit* [*mbvyn.com*](https://mbvyn.com/) *for mentorship, consulting, and all my content in one place. And if you work with Parquet files, try* [*parquetreader.app*](https://parquetreader.app/) *— my free tool for exploring them in the desktop.*