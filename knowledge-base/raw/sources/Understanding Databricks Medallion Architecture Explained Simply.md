---
title: "Understanding Databricks: Medallion Architecture Explained Simply"
source: "https://mbvyn.medium.com/understanding-databricks-medallion-architecture-explained-simply-67085e47c40b"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-06-29
created: 2026-10-23
description: "More"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*BcrUGywp8Sybturk-JuXhQ.png)

If you have spent any time around Databricks, you have heard the words Bronze, Silver, and Gold. People throw them around like everyone already knows what they mean. And when you are new, it can feel like there is some secret rulebook everyone has read except you.

Here is the good news: the Medallion Architecture is one of the simplest, most useful ideas in all of data engineering. Once it clicks, you will start seeing it everywhere — and you will wonder how you ever built pipelines without it.

In this article, I will explain the Medallion Architecture in plain language. What the three layers actually do, how data flows through them, how it maps to Databricks tools in 2026, and — just as important — when you should not use it. We will follow a real example the whole way through so it stays concrete.

This article is part of the **Understanding Databricks** series. Follow to read more!

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*dK3TmTGtCsWeEZI52ySfyw.png)

## What the Medallion Architecture Actually Is

The Medallion Architecture is a way of organizing your data into three layers, where each layer is cleaner and more useful than the one before it. Data flows in one direction — Bronze to Silver to Gold — getting better at every step.

The names come from medals, and that is the whole mental model. Bronze is raw and unrefined. Silver is cleaned up and trustworthy. Gold is polished and ready to drive decisions. The names describe the **quality** of the data, not the technology behind it.

You might also hear it called a “multi-hop architecture,” because data hops from one layer to the next. Same thing.

Here is the part most tutorials skip: Databricks itself describes Medallion as “a recommended best practice but not a requirement.” That line matters. Medallion is a guideline that solves a real problem — turning messy source data into something you can trust — but it is not a law. We will come back to that near the end, because knowing when to break the pattern is as important as knowing the pattern.

Let me walk you through each layer using one running example: an online store processing customer orders.

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

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*bYajJKVeg9ud6teieEPEig.png)

## Bronze: Land It Raw, Touch Nothing

The Bronze layer is where raw data lands, exactly as it arrives from the source. No cleaning, no validation, no business logic. You take what the source gives you and you store it.

This feels wrong to a lot of beginners. Why would I store messy data? Because Bronze has one job: be a faithful, complete record of what actually came in. If something breaks downstream, you can always reprocess from Bronze. If an auditor asks what the source sent on a specific day, Bronze has the answer. It is your safety net and your single source of truth.

A few best practices that took me a while to learn:

- **Store fields loosely.** Keep columns as strings or use the VARIANT type rather than enforcing strict types. This protects you when the source suddenly changes its schema — and it always does, usually on a Friday
- **Append, never overwrite.** Bronze grows over time. You add new data, you do not modify old data
- **Capture metadata.** Record where each row came from (the source file name and path), when it was loaded, and which process loaded it. You will thank yourself during debugging
- **Do not let analysts query Bronze directly.** Bronze is for building Silver, not for reporting. Raw data with no guarantees is a trap for anyone trying to make decisions

In our online store example, Bronze holds the raw order records dumped straight from the app database, plus the raw payment events streaming in from the payment provider. Messy, unvalidated, complete. On Databricks, you typically land this with **Auto Loader** (which incrementally picks up new files from cloud storage) or **Lakeflow Connect** (managed connectors for databases and SaaS apps).

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*h-s2Qkvx31eMNuyHoZytmA.png)

## Silver: Clean It, Conform It, Trust It

The Silver layer is where the real work happens. You take the raw data from Bronze and turn it into something clean, consistent, and trustworthy.

This is where you:

- Enforce schemas and fix data types (that string of cents becomes a proper dollar amount)
- Handle nulls and missing values
- Deduplicate records (the same customer should not appear three times)
- Resolve late-arriving and out-of-order data
- Join related data together (orders enriched with their payment status)
- Apply data quality checks and drop or flag bad records

The golden rule of Silver: ***build it by reading from Bronze, never directly from ingestion.*** If you point your cleaning logic straight at the incoming raw feed, a single schema change or corrupt file can take down your whole pipeline. Read from Bronze instead, where the data has already safely landed.

One more principle: Silver should still have ***at least one clean, validated row per original record.*** You are cleaning data here, not summarizing it. Aggregations belong in Gold. Think of Silver as “the truth, organized.”

In our example, Silver joins each order to its latest payment status, deduplicates customers by email, converts amounts from cents to dollars, and normalizes currencies. Every order is now a clean, single, trustworthy row. This is the layer your data scientists will actually love, because they can build on it without fear.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*WoxM9eUU5itsIsOnTKKzZQ.png)

## Gold: Business-Ready by Design

The Gold layer is the finished product. This is data shaped around business questions, aggregated and optimized for the people and systems that consume it — dashboards, reports, ML models, executives.

Gold has three defining traits:

- **Aggregated** for analytics and reporting (daily revenue, customer lifetime value, average order value)
- **Aligned with business logic** (an “active customer” means whatever your business decides it means)
- **Optimized for fast queries** because this is what gets hit constantly

Gold is usually where you apply dimensional modeling — fact tables and dimension tables, the classic star schema. And you typically have fewer Gold tables than Silver, often organized by business domain: a finance Gold, a marketing Gold, a product Gold. Each one is denormalized and tuned for the questions that the team asks.

In our online store, Gold might contain a \`fct\_orders\` fact table (one row per order line, with keys, totals, and order state), a \`dim\_customers\` dimension (one row per customer with lifetime value and order history), and aggregate tables for daily revenue and customer metrics. An analyst opens a dashboard, and it just works — fast, clean, business-ready.

One tip: resist the urge to materialize huge historical volumes into Gold. Keep the long history in Silver and let Gold stay lean and fast.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*w6_VR37qIdd1uygwjZCwfw.png)

## How Medallion Maps to Databricks in 2026

The pattern is technology-agnostic, but Databricks gives you tools built specifically for it. Here is how it comes together in 2026.

**Lakeflow** (the data engineering suite — its pipeline framework was formerly called Delta Live Tables) is the natural home for Medallion. You declare your layers as datasets, and Lakeflow handles the flow between them:

- **Bronze** as streaming tables — append-only, ingesting raw data continuously
- **Silver** as streaming tables for row-level cleaning, or materialized views when you need joins and enrichment
- **Gold** as materialized views — pre-computed aggregations that refresh automatically

Here is what a Bronze-to-Silver step looks like in Lakeflow SQL:

```c
CREATE OR REFRESH STREAMING TABLE silver_orders (
 CONSTRAINT valid_amount EXPECT (amount > 0) ON VIOLATION DROP ROW,
 CONSTRAINT valid_customer EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW
)
AS SELECT
 order_id,
 customer_id,
 CAST(amount_cents AS DOUBLE) / 100 AS amount,
 CAST(order_ts AS TIMESTAMP) AS order_time
FROM STREAM(LIVE.bronze_orders);
```

Those \`EXPECT\` rules are **Expectations** — Lakeflow’s built-in data quality enforcement. You define a rule, and you choose what happens when data violates it: warn and keep the row, drop the row, or fail the pipeline entirely. This is how you stop bad data from flowing Bronze to Silver to Gold.

For slowly changing dimensions and change data capture, Lakeflow gives you **AUTO CDC** (which replaced the older APPLY CHANGES API). It handles SCD Type 1 and Type 2 automatically — no more hand-writing merge logic.

And for organizing all of this in **Unity Catalog**, the common pattern is a schema per layer — something like \`shop.bronze\`, \`shop.silver\`, \`shop.gold\`. Databricks leaves the exact structure to you; just be consistent.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*uRttIr73uR74GDAN-aX3lw.png)

## Best Practices That Actually Matter in 2026

A few things have changed in how you optimize Medallion tables, and the old advice is now outdated.

- **Use liquid clustering, not partitioning.  
	**This is the big one. For years, everyone partitioned their tables by date. In 2026, Databricks recommends **liquid clustering for all new tables**, including streaming tables and materialized views. It replaces both partitioning and ZORDER, adapts as your query patterns change, and avoids the painful mistakes that bad partitioning causes. For most tables under a terabyte, you do not need partitioning at all
- **Let predictive optimization handle maintenance.**  
	Predictive optimization automatically runs OPTIMIZE and VACUUM on your managed tables, so you are not scheduling cleanup jobs by hand. It is on by default for newer accounts, with older accounts being rolled in through 2026
- **Stream where it makes sense, batch where it does not.  
	**Most Bronze-to-Silver reads work best as streaming. Reserve a batch for small dimension tables that do not change often
- **Keep Bronze append-only and let it grow.** Storage is cheap; lost raw history is expensive
- **Be consistent with naming.**  
	Bronze, Silver, Gold is a convention, not a rule — but pick one scheme and stick to it across every project so your team always knows where they are
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*V_LNiIeOGICQcy0yVKRBZA.png)

## Is Medallion Always the Right Choice?

Medallion is excellent, but it is not free, and it is not always the answer.

Every hop copies data. A 100 GB source can balloon to 300 GB across three layers, and each hop adds latency and cost. If your data is already clean, or your dataset is tiny, or you need near-instant freshness, three full layers can be overkill. Some teams do just fine with two layers — Raw and Curated — and skip the ceremony.

There is also a growing conversation in the industry about the limits of Medallion. Critics point out that it can become a generic, context-free assembly line that produces redundant copies and pushes cleanup downstream instead of fixing data at the source. Those are fair points worth knowing.

And then there is what Databricks announced at the Data+AI Summit in June 2026: **LTAP** (Lake Transactional/Analytical Processing), an architecture that unifies transactional and analytical data on a single copy, with real-time querying directly on the lakehouse. This attacks exactly the weakness critics raise — the physical copies and the staleness between layers.

But here is the nuance, and it matters: LTAP changes ***where data physically lives and how fast you can serve it.*** It does not abolish the **logic** of Medallion.

You still go from raw to clean, to business-ready — that progression of quality is a data-organization principle, not a storage detail. Real-time architectures reduce the copies and the lag. They do not remove the need to turn messy data into trustworthy data.

So learn Medallion deeply. It is the mental model underneath almost everything, even as the physical implementation evolves.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*KA-y2kjqMcq5k2lYQDDdkA.png)

## Common Mistakes to Avoid

- **Putting business logic in Bronze.** This is the number one mistake. Bronze is raw and untouched. The moment you start “fixing” data in Bronze, you lose your safety net
- **Querying Bronze for reports.** Bronze has no guarantees. If analysts build dashboards on it, they are building on sand. Point them at Silver or Gold
- **Writing to Silver straight from ingestion.** Always build Silver from Bronze. Skipping that step means one bad file can break your whole pipeline
- **Over-engineering small data.** Not every dataset needs three layers. If your data is small and clean, two layers — or even one — may be plenty. Do not add ceremony for its own sake
- **Letting Gold tables multiply.** One Gold table per dashboard leads to dozens of near-duplicate tables that slowly drift apart. Design Gold around business domains, not individual reports
- **Still partitioning everything by date.** Old habit, outdated advice. Use liquid clustering for new tables instead
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AXqE4UR1YU1Z_1jFpihNdg.png)

## What Is Next

This wraps up **Part I** of the series — the foundations. You now understand what Databricks is, how it compares to other platforms, its core components, how the clouds differ, what a modern data platform looks like, and how to organize data with the Medallion Architecture.

In the next article, we open **Part II: Delta Lake and Data Formats.** We will start at the foundation of every Lakehouse — the data formats themselves. Parquet, ORC, Avro, and how Delta Lake builds on top of Parquet to make your data reliable. This is where the hands-on work really begins.

Make sure to bookmark this series so you do not miss any upcoming articles.

Want more? Visit [mbvyn.com](https://mbvyn.com/) for mentorship, consulting, and all my content in one place.