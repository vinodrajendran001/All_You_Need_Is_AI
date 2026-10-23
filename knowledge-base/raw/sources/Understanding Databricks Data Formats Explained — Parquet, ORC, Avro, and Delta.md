---
title: "Understanding Databricks: Data Formats Explained — Parquet, ORC, Avro, and Delta"
source: "https://mbvyn.medium.com/understanding-databricks-data-formats-explained-parquet-orc-avro-and-delta-b8b561f6b4ec"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-07-04
created: 2026-10-23
description: "A plain-language guide to the formats behind every Lakehouse. Updated June 2026."
tags:
  - "clippings"
---
## A plain-language guide to the formats behind every Lakehouse. Updated June 2026.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yCOjriqawzpLOSpD6yGBBw.png)

Welcome to Part II of the series. We spent Part I on the big picture — what Databricks is, how it compares, how a modern platform is built. Now we go hands-on, and we start at the very bottom of the stack: the data formats themselves.

This is one of those topics that seems boring until it quietly wrecks your platform. I have seen teams store terabytes as CSV and then wonder why every query takes twenty minutes. I have seen people pick ORC because a blog told them to, with no idea why. And I have seen the single most common confusion in all of data engineering — thinking Parquet and Delta are competitors, when one is literally built on top of the other.

In this article, I will clear all of that up. We will go through Parquet, ORC, Avro, and Delta Lake in plain language — what each one is, how it stores data, and when to actually use it. By the end, you will know exactly which format to reach for and why.

One idea to hold on to before we start, because it is the backbone of everything: **Parquet, ORC, and Avro are file formats.** Delta Lake, Iceberg, and Hudi are table formats. A file format is how bytes are arranged inside one file. A table format is a layer of metadata and transactions that sits atop many files, turning a folder into a real, reliable table. Keep that distinction in your head, and the whole landscape suddenly makes sense.

### Key takeaways

- **Parquet** is a columnar file format — the standard for analytics. Fast reads, great compression, universal support.
- **ORC** is a columnar format from the Hadoop/Hive world. Fine in legacy Hive stacks, but Parquet won the broader ecosystem.
- **Avro** is a row-based format built for streaming and event-by-event ingestion (Kafka, Pub/Sub), with strong schema evolution.
- **Delta Lake** is not a file format — it is a table format built on top of Parquet, adding ACID transactions, time travel, and UPDATE/DELETE/MERGE.
- **Rule of thumb on Databricks:** ingest with Avro or raw files, then keep everything as Delta. Columnar speed plus full SQL operations.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*4PG5GiYcwNmgPv9mCzRpdA.png)

## Row vs Columnar: The Idea Behind Everything

Before we touch any specific format, you need one mental model. Every format is either row-oriented or columnar, and that single choice decides what it is good at.

**Row-oriented** storage keeps all the fields of one record together. Record one, then record two, then record three. If you want to read or write one whole record, it is one cheap operation. This is how databases have always worked, and it is great for transactions and for writing data one event at a time.

**Columnar** storage flips it. Instead of keeping records together, it keeps each column together — all the IDs in one place, all the names in another, all the amounts in another.

Why does this matter so much? Imagine a table with 50 columns and a billion rows, and you run \`SELECT SUM(amount)\`. A columnar format reads just the \`amount\` column — about one-fiftieth of the data — and ignores the rest. A row format has to read every single row, all 50 columns, just to get to the one it needs. That is the entire reason analytics engines are columnar.

Columnar wins for three reasons:

- **You read only the columns you need** — no wasted I/O
- **Compression is dramatically better** — values in a column are similar, so they compress hard
- **Vectorized execution** — engines process a column as a tight array, which modern CPUs love

So here is the model to remember: **analytics and reporting want columnar. Transactions and streaming want row-oriented.** Everything below follows from this.

(One nuance for the curious: Parquet and ORC are technically hybrid. They split data into horizontal chunks of rows first, then store columns within each chunk. You get columnar scan speed while keeping a chunk as a unit of parallel work.)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Wu4xoMFKhmlzcEG-v6aAuA.png)

## CSV and JSON: Where Everyone Starts

Every data engineer’s journey begins with CSV and JSON, and for good reason. They are simple, human-readable, and every tool on earth can read them. For small data, quick inspection, or moving data between systems, they are perfectly fine.

The problem is what happens when you scale.

**CSV** has no schema and no types. Everything is a string until something guesses otherwise, usually wrong. It is row-oriented text, so there is no reading just the columns you need — you parse the whole file every time. There is no compression built in, no way to skip irrelevant data, and every tool has its own subtle dialect for quoting and escaping. At a few megabytes, none of this matters. At a few terabytes, it is a disaster.

**JSON** is better at structure — it handles nested data naturally, which is why APIs love it. But it is verbose (every record repeats all its keys as text), slow to parse at volume, and has no enforced schema, so the shape can change on you without warning.

When are they still the right call? Small datasets, human inspection, config files, API payloads, and simple interchange between systems. If you are dealing with logs or event data as text, look at **JSON Lines** (also called NDJSON) — one JSON object per line, which is much friendlier to process record by record.

The rule: CSV and JSON are great for getting data **in**. They are the wrong place to keep it for analytics. The moment data lands, you convert it to something better.

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

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*unKTWLWeclzqls6wzfulaQ.png)

## Parquet: The Columnar Format That Won

If you remember one file format, make it Parquet. It is the columnar format that became the standard for analytics everywhere — the [default write format in Apache Spark](https://parquet.apache.org/docs/), readable by Trino, DuckDB, BigQuery, Snowflake, Athena, and virtually everything else. It is also the foundation that Delta Lake, Iceberg, and Hudi are all built on. Parquet is the bedrock of the modern data lake.

Here is how it works inside. A Parquet file is split into **row groups** (horizontal slices of rows). Within each row group, data is stored **column by column** — these are called column chunks — and each chunk is broken into pages. At the end of the file sits a **footer** containing the schema and, crucially, statistics for each column chunk: the minimum value, the maximum value, and null counts.

Those statistics are the magic. When you run a query with a filter — say \`WHERE amount > 1000\` — the engine reads the footer first, checks the min/max of each row group, and skips any row group that cannot possibly match. This is called ***predicate pushdown,*** and combined with ***column pruning*** (reading only the columns you need), it is why Parquet queries fly. On top of that, Parquet uses smart encoding (dictionary, run-length, bit-packing) and compression (Snappy, ZSTD) to shrink files dramatically.

The one thing Parquet is not good at: updating data. A Parquet file is effectively immutable. Change a few rows, and you are rewriting large chunks of the file. It is also not built for streaming writes or row-by-row inserts. For analytics reads, though, nothing beats it.

Quick tip from my own workflow: when I need to peek inside a Parquet file — check the schema, inspect a few rows, verify what a pipeline actually wrote — I do not spin up a Spark cluster for that. I built a small tool for exactly this, [**parquetreader.app**](https://parquetreader.app/), that lets you open and explore Parquet files right in your browser. If you work with Parquet daily, it will save you a lot of time.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_1xE_miBrp_t-3sRuvllZw.png)

## ORC: Parquet’s Hadoop Cousin

ORC — Optimized Row Columnar — is the other big columnar format. It came out of the Hadoop and Hive world, and technically it is excellent. In many ways it was ahead of Parquet on features.

Structurally it is similar to Parquet but with different names. Instead of row groups, ORC has **stripes**. It has a built-in row index (every 10,000 rows by default) with column statistics, and it supported **bloom filters** for fast equality lookups early on. It also underpinned Hive’s ACID support, using delta files and a compactor to merge changes — an early version of ideas we now see in Delta and Iceberg.

So why did Parquet win the broader ecosystem? Not because ORC is worse — it often compresses beautifully and its indexing is strong. It is because ORC stayed tightly tied to Hive and Hadoop, while Parquet became Spark’s default, got adopted by every cloud warehouse, and became the substrate for the lakehouse table formats. Ecosystem momentum decided it.

Where should you use ORC today? Honestly, mostly in legacy Hive and Hadoop environments where it is already in place, especially if Hive ACID is involved. For anything new on Databricks or a modern lakehouse, reach for Parquet (or Delta on top of it). Choosing ORC for a greenfield project “because it compresses well” is a classic mistake — the ecosystem fit matters more than a few percent of file size.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PkmDBG-XiI9JarcHoJYQRw.png)

## Avro: Built for Streaming

Avro is the odd one out here, and that is exactly why it is useful. While Parquet and ORC are columnar and built for reading, **Avro is row-based and built for writing** — specifically, for writing data one record at a time.

That makes Avro the natural fit for streaming. When you ingest from Apache Kafka, Google Pub/Sub, or any event stream, you are dealing with records arriving one after another. A row-based format writes each complete record in one cheap operation, which is exactly what you want for event-by-event ingestion.

Avro has two more standout traits. First, the **schema travels with the data**. In an Avro data file, the schema is stored right in the header as JSON, so any program can read the file later and know exactly what it contains. (In the Kafka world, the schema usually lives once in a Schema Registry, and each message just carries a small schema ID — same idea, less repetition.)

Second, Avro has **excellent schema evolution**. You can add a field with a default, remove a field, and old and new readers still work together. In streaming systems this is huge, because producers and consumers get updated at different times. Confluent formalizes this with compatibility modes — backward, forward, and full — so you can evolve schemas without breaking anyone.

The trade-off: because Avro is row-based, it is slow for analytical queries. There is no column pruning, no reading just one column across a billion rows. So the standard pattern in a lakehouse is exactly what you would expect: **ingest as Avro, then convert to Parquet or Delta for analytics.** Row format for the write, columnar format for the read. Best of both.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*oF80vdIzPz1OQUHDJ8czzg.png)

## Delta Lake: Parquet With a Brain

Now for the one everyone confuses. [Delta Lake](https://docs.databricks.com/aws/en/delta/) is not a file format — it is a **table format**, and it is built directly on top of Parquet. Your data still lives in ordinary Parquet files. What Delta adds is a **transaction log**.

That log — a folder called \`\_delta\_log\` sitting next to your data — is the whole trick. Every change to the table is recorded as a sequential commit in the log. The log is the single source of truth: a Parquet file only counts as part of the table if the log says so. This one idea unlocks everything Delta is known for:

- **ACID transactions** — writes either fully succeed or fully fail, even with many writers at once (using optimistic concurrency)
- **Time travel** — every write is a version, so you can query the table as it looked yesterday with \`VERSION AS OF\` or \`TIMESTAMP AS OF\` (bounded by your VACUUM retention, 7 days by default)
- **Schema enforcement and evolution** — bad-shaped data gets rejected on write, and you can evolve the schema deliberately when you mean to
- **DELETE, UPDATE, and MERGE** — the operations plain Parquet cannot do. MERGE gives you full upserts in one statement, perfect for slowly changing dimensions
- **Deletion vectors** — instead of rewriting a whole Parquet file to delete a few rows, Delta marks them in a compact bitmap and applies it at read time. Much faster deletes and updates. This is GA now

On Databricks, Delta is the default — unless you say otherwise, every table you create is a Delta table. And it keeps evolving: Delta Lake 4.0 (2025) added the Variant type for semi-structured data, and 4.1 (2026) introduced catalog-managed tables, moving the source of truth into the catalog itself.

Two things to remember operationally: Delta tables need occasional maintenance — \`OPTIMIZE\` to compact small files and \`VACUUM\` to clean up old ones. And for laying out data, use **liquid clustering** (now GA) instead of old-style partitioning. That is the “Parquet with a brain” story: same files underneath, but now with reliability, history, and full SQL operations on top.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*5w_2KVK7jOXgFPCxC4AEyg.png)

## The 2026 Landscape: Delta, Iceberg, and Hudi

There are three table formats you will hear about: **Delta Lake** (from Databricks), [Apache Iceberg](https://iceberg.apache.org/) (born at Netflix, now the engine-neutral standard), and **Apache Hudi** (from Uber, strong at streaming upserts). For years, people talked about a “format war.” In 2026, that war is basically over — and the winner is interoperability.

Here is what changed. Databricks acquired Tabular, the company founded by Iceberg’s creators, back in 2024, with the explicit goal of making Delta and Iceberg work together. Out of that came [***UniForm***](https://www.databricks.com/blog/delta-lake-universal-format-uniform-iceberg-compatibility-now-ga) — you write your data once as Delta, and Delta automatically generates Iceberg metadata over the very same Parquet files. No copies, no duplication. Any Iceberg-compatible engine can then read your Delta tables.

And in 2026, Databricks went further: managed Iceberg tables in Unity Catalog reached general availability, and Unity Catalog can now act as an Iceberg REST catalog that external engines — Snowflake, Trino, Flink, DuckDB — connect to directly. The Iceberg v3 spec landed too, bringing deletion vectors, row lineage, and the Variant type, converging with what Delta already had.

The takeaway is bigger than any one format. The industry is settling on a single principle: **one copy of your data, in open formats, readable by many engines.** You should not be copying data between platforms just because they speak different table formats anymore. Choose open, and your data stays reachable — by any engine, and increasingly by any AI agent too.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Je-YE-zzIcUv_6GAhu-HDw.png)

## Which Format Should You Use?

Here is the practical decision guide I would give anyone starting out.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*bSSfDUztVzUA5rkfmROcKg.png)

For most people building on Databricks, the answer collapses to something simple: **ingest with Avro or land raw files, then keep everything as Delta.** Delta is Parquet underneath, so you get columnar speed, plus ACID, time travel, and full SQL operations on top. You rarely need to think harder than that.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yNPIMeQtYr2VQY1TG9NhiA.png)

## Common Mistakes to Avoid

- **Storing big data as CSV or JSON.** No schema, no compression, no pushdown, full-file scans every query. Convert to Parquet or Delta the moment data lands
- **Confusing Parquet with Delta.** They are not competitors at the same layer. Delta **is** Parquet files plus a transaction log. Saying “Parquet or Delta” is like saying “bricks or a house”
- **Using bare Parquet when you need updates.** Plain Parquet is effectively immutable. If you need UPDATE, DELETE, MERGE, or time travel, you need a table format like Delta
- **Choosing ORC for a new project without a reason.** Outside a Hive/Hadoop shop, Parquet has broader support and is the lakehouse standard. Do not pick it just for compression
- **Locking into a proprietary format.** In 2026, open formats mean one copy of data readable by every engine. Giving that up for short-term convenience is a trap
- **Skipping Delta maintenance.** No OPTIMIZE and VACUUM means a pile of small files and ever-growing storage. Let predictive optimization handle it, or schedule it yourself
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*O2ymFijIZvITIxoRRp5ffg.png)

## Frequently Asked Questions

**What is the difference between Parquet and Delta Lake?**  
Parquet is a file format — it defines how data is stored inside a single file, in columns. Delta Lake is a table format that sits on top of Parquet files and adds a transaction log. In other words, a Delta table is made of ordinary Parquet files plus metadata that gives you ACID transactions, time travel, and UPDATE/DELETE/MERGE. They are not competitors; Delta is built on Parquet.

**Is Parquet better than CSV?**  
For analytics at scale, yes, by a wide margin. Parquet is columnar, compressed, typed, and lets query engines read only the columns they need and skip data that cannot match a filter. CSV is uncompressed row-based text with no schema, so every query parses the whole file. Use CSV for small data and interchange; use Parquet for analytics.

**When should I use Avro instead of Parquet?**  
Use Avro when you are writing data one record at a time, especially for streaming from Kafka or Pub/Sub. Avro is row-based, so writing a full record is cheap, and it has excellent schema evolution. Use Parquet when you are reading data for analytics. The common pattern is to ingest as Avro, then convert to Parquet or Delta for querying.

**Is Delta Lake a file format?**  
No. Delta Lake is a table format or storage layer. The actual data files are standard Parquet. What Delta adds is the \`\_delta\_log\` transaction log, which turns a folder of Parquet files into a reliable table with ACID guarantees.

**Should I use Delta Lake or Apache Iceberg?**  
On Databricks, Delta is the default and the most tightly integrated. But in 2026 the two are converging: Delta UniForm lets you write once as Delta and read it as Iceberg from any engine, and Unity Catalog now supports managed Iceberg tables natively. Choose based on your platform, and lean on open formats so your data stays readable by any engine.

**Can Parquet files be updated?**  
Not easily. A plain Parquet file is effectively immutable — changing a few rows means rewriting large parts of the file. If you need UPDATE, DELETE, MERGE, or time travel, use a table format like Delta Lake, which handles these operations on top of Parquet.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AXqE4UR1YU1Z_1jFpihNdg.png)

## What Is Next

Now that you understand the formats, we are ready to get our hands dirty. In the next article, we go deep on **Delta Lake in practice** — creating tables, appending and merging data, schema enforcement and evolution, and the operations that make Delta the heart of every Databricks platform. This is where the real building begins.

Make sure to bookmark this series so you do not miss any upcoming articles.

*Want more? Visit* [*mbvyn.com*](https://mbvyn.com/) *for mentorship, consulting, and all my content in one place. And if you work with Parquet files, try* [*parquetreader.app*](https://parquetreader.app/) *— my free tool for exploring them in the browser.*