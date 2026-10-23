---
title: "Understanding Databricks: Core Components You Need to Know"
source: "https://mbvyn.medium.com/understanding-databricks-core-components-you-need-to-know-fbede947e94e"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-06-01
created: 2026-10-23
description: "More"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*68BmgeId0cOT_4qZmw_Siw.png)

When I first opened Databricks, I remember staring at the left sidebar thinking — what is all of this? Notebooks, clusters, warehouses, workflows, pipelines, catalogs, AI tools. And every one of them seems to have three sub-features with their own names.

It took me a while to figure out which pieces actually matter day to day and which ones I could learn later. Let me share what I figured out.

In this article, I will walk you through the core components of Databricks — what each one does, when you use it, and how they all fit together. We will focus on the six you will interact with most as a data engineer, then cover the rest so you know they exist when you need them.

This article is part of the **Understanding Databricks** series. If you are new here, please subscribe and check more!

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*CX6TZY4IS-fMogB880wBNA.png)

## Notebooks: Where the Work Happens

Notebooks are where you spend most of your time in Databricks. They are interactive documents where you write code, run it, see results, and document your work — all in one place.

You can write in Python, SQL, Scala, or R, and you can mix languages in the same notebook using magic commands like \`%python\` and \`%sql\`.

Need to run a quick shell command? \`%sh\`.

Check the filesystem? \`%fs\`.

It is flexible in a way that feels natural once you get used to it.

If you have used Jupyter before, Databricks notebooks will feel familiar — but with a few things that make a real difference:

- **Real-time collaboration.** Multiple people can edit the same notebook at the same time and see each other’s cursors. Sounds simple, but when you are debugging something together at 11 pm, it is a lifesaver
- **Built-in Git integration.** Full version control through Git folders. Push, pull, branch, merge — all from the workspace. No more emailing notebook files around
- **Genie Code.** This is the AI assistant built into every notebook. In agent mode, you give it a prompt, and it generates code, runs it, fixes errors, and produces visualizations on its own. It has been available for most workspaces for a while now, and as of May 2026, it is also enabled by default for compliance-profile workspaces — HIPAA, PCI-DSS, FedRAMP — which previously could not use it
- **Visualizations and widgets.** Built-in charts, interactive parameters, data profiling, and the ability to create dashboards directly from notebook results. No need to export to another tool just to make a chart

Notebooks run on compute — either all-purpose clusters for interactive work or serverless compute for faster startup with no idle costs.

**When to use notebooks:** Exploration, prototyping, ad-hoc analysis, interactive development. They are your workshop. But when something needs to run reliably in production, that is where the next component comes in.

> Take Your Databricks Prep to the Next Level
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

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AyXG7oLZ58rIo9QUWDdu9w.png)

## Workflows: From Notebook to Production

Notebooks are great for development. But when you need something to run every night at 2 am, handle errors gracefully, and notify your team if anything breaks — you need Workflows.

A quick note on naming — Databricks has been rebranding things, so you might see Workflows called “Lakeflow Jobs” in newer documentation. Same thing, new name. Databricks loves renaming things. You get used to it.

Workflows let you build multi-task DAGs — directed acyclic graphs. Each task can be a notebook, a Python script, a SQL query, a Lakeflow pipeline, a dbt model, or a JAR file. Tasks connect through dependencies, so task B only runs after task A succeeds. Here is what makes them powerful:

- **Flexible triggers.** Schedule with cron, trigger when a new file lands in cloud storage, trigger when a Delta table updates, or run continuously. The file arrival trigger is one of my favorites — no polling, no custom code, it just works
- **Real control flow.** Conditional branching (if/else) and loops (for each) are built right into the DAG. You can build real logic, not just linear chains of tasks
- **Smart error handling.** If one task fails, re-run just that task without restarting the whole job. Set retry policies per task. Get notifications via email, Slack, or webhooks
- **Scale.** Up to 1,000 tasks per job and 2,000 concurrent task runs per workspace. That is enough for even the most complex pipelines
- **Monitoring.** Built-in system tables track all runs across your account. The Unified Runs List consolidates job and pipeline runs with real-time filtering by status, time, and error codes

Here is something that will save you money immediately: jobs run on Jobs Compute at about $0.15 per DBU — roughly **3.7 times cheaper** than all-purpose compute at $0.55 per DBU. If you are running production pipelines on all-purpose clusters, you are overpaying. Switch to jobs compute.

**When to use Workflows:** Anything that runs in production. Scheduled ETL, orchestrated multi-step processing, anything that needs to be reliable and monitored. And now, let’s talk about where your SQL analysts will spend their time.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Pq4NsUpxCWJHwafXPvlLCA.png)

## SQL Warehouses: Analytics for the Whole Team

Not everyone on your team writes Python. Not everyone knows what Spark is. And that is completely fine — SQL Warehouses exist exactly for this.

SQL Warehouses are dedicated SQL engines optimized for analytical queries and BI dashboards. Your analysts write SQL, get fast results, build dashboards — all without touching a single line of Spark code. And they query the same data that your engineers work with, governed by the same Unity Catalog. No copies, no sync issues.

There are three types, but let me save you time — **use Serverless:**

- **SQL Classic** — the original option. Being phased out, avoid for new projects
- **SQL Pro** — better performance, self-managed. Use only if you need specific compute configurations
- **SQL Serverless** — fully managed, elastic, auto-scales with demand, Photon always enabled. Infrastructure costs are included in the DBU rate (~$0.70/DBU on AWS). No separate VM charges. This is the default for new workspaces, and for good reason

What else comes with SQL Warehouses:

- **AI/BI Dashboards.** Legacy dashboards were retired in early 2026. The new dashboards support cross-filtering, drill-through, pivot hierarchies, mobile layouts, and embedding. You can even build them with natural language through Genie Code — describe what you want, and it creates the dashboard
- **Genie.** Think of it as a conversation with your data. Analysts ask questions in plain English, Genie generates SQL, verifies it, and produces results. Agent mode handles multi-step analysis with parallel queries. It is surprisingly good
- **Query Federation.** Through Lakehouse Federation, you can query external databases — MySQL, PostgreSQL, Snowflake, BigQuery, Redshift, Teradata, Oracle, and more — directly from your SQL Warehouse without moving data. Join your Delta tables with your Postgres production database in one query

**When to use SQL Warehouses:** BI dashboards, ad-hoc SQL queries, serving analytics to business users, and querying across external systems. Now, for the component I am most excited about.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*uhegrn_J74t7TvKm3TQgiA.png)

## Lakeflow: My Favorite Thing in Databricks

I genuinely believe Lakeflow is the most underused component in Databricks. Most teams I talk to are still writing raw Spark jobs with custom orchestration when Lakeflow would do it better with a fraction of the code.

It used to be called Delta Live Tables (DLT). In 2025, it was rebranded as part of the Lakeflow suite. The core idea has not changed — instead of writing complex imperative code for your data pipelines, you declare what your data should look like, and Lakeflow figures out how to get there.

You write in SQL or Python. Here is a real example:

```c
CREATE OR REFRESH STREAMING TABLE raw_orders
AS SELECT * FROM cloud_files('/data/orders/', 'json');
CREATE OR REFRESH MATERIALIZED VIEW clean_orders (
 CONSTRAINT valid_amount EXPECT (amount > 0) ON VIOLATION DROP ROW
)
AS SELECT order_id, customer_id, amount, order_date
FROM LIVE.raw_orders
WHERE status != 'cancelled';
```

Two statements. The first ingests JSON files from cloud storage as a streaming table. The second creates a clean view with a data quality rule — any row where \`amount\` is zero or negative gets dropped automatically. Lakeflow handles ingestion, execution order, dependencies, error recovery, and quality tracking.

**What makes it special:**

- **Expectations.** Data quality rules are built into the pipeline. \`EXPECT\` logs violations, \`EXPECT OR DROP\` removes bad rows, \`EXPECT OR FAIL\` stops the pipeline. As of 2026, expectations are first-class metadata in Unity Catalog — visible in Catalog Explorer, queryable via system tables, shareable across pipelines
- **Flexible execution.** Triggered mode processes available data and stops. Continuous mode runs always. The new real-time mode delivers end-to-end latency as low as 5 milliseconds for use cases like fraud detection
- **Lakeflow Connect.** Managed connectors for ingesting from external sources — Salesforce, HubSpot, MySQL, PostgreSQL, Kafka, Google Analytics, and many more. CDC connectors handle change data capture automatically. No custom ingestion code
- **Lakeflow Designer.** A visual drag-and-drop pipeline editor, enabled by default for all workspaces as of May 2026 (Public Preview). No-code interface with AI-powered operator search — great for teams that prefer visual tools or for prototyping before writing code

**When to use Lakeflow:** Any data pipeline — batch or streaming. Bronze/Silver/Gold medallion transformations. Data quality enforcement. Ingestion from external sources. If you are writing raw Spark ETL jobs, seriously consider switching.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*r3c0WouYKxC4tSlJcg4crw.png)

## Unity Catalog: The Foundation of Everything

Let me tell you why I keep bringing up Unity Catalog in every article. I once worked with a team that built its entire platform without governance. Six months in, they had 200 tables, and nobody knew who could access what, where the data came from, or which tables were still accurate. Setting up governance after the fact took them longer than building the original platform.

That is why Unity Catalog exists. It is the governance layer for everything in Databricks — data, ML models, AI agents, and the connections between them.

The structure is clean: **catalog → schema → object**. Objects can be tables, views, volumes (for files), functions, models, or connections to external systems. You grant permissions at any level — from an entire catalog down to a single column.

Here is what makes it essential:

- ==**Attribute-based access control (ABAC).**== ==GA as of April 2026. Instead of managing hundreds of individual grants, define dynamic policies based on user attributes. A clinician sees only their patients’ records. A regional manager sees only their region’s data. The rules scale without manual maintenance==
- **Automatic data classification.** AI-powered classification detects and tags sensitive data — PII, financial records, health information. You do not have to manually audit every column in every table to find email addresses and phone numbers
- **Column-level lineage.** See exactly where data came from and where it goes — from source tables through transformations to dashboards. When a dashboard shows wrong numbers, lineage tells you which upstream table changed
- **Data discovery.** The Catalog Explorer lets anyone search for tables, read documentation, and understand what is available. AI-generated comments describe tables and columns automatically. Your new team member can find the data they need without asking five people
- **Lakehouse Federation.** Query external databases — MySQL, PostgreSQL, Snowflake, BigQuery, Redshift, Teradata, Oracle — without copying data. Security policies apply even to federated queries
- **Open source.** Unity Catalog was open-sourced in June 2024 under Apache 2.0. It supports the Iceberg REST Catalog API, so Trino, Flink, DuckDB, and other engines can connect to it

Unity Catalog is included with Premium and Enterprise tiers — no separate charge.

**When to use it:** From the first day of your project. Every single time. There are no exceptions.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*VgfMAXXsAjXCAeliT1MESw.png)

## Mosaic AI: Intelligence Built Into the Platform

Even if you are not building ML models today, read this section. Because the gap between “data engineer” and “AI engineer” is closing fast, and understanding Mosaic AI now will save you a steep learning curve later.

Mosaic AI is Databricks’ AI and machine learning platform. Here is what it includes and why each piece matters:

- **Model Serving** lets you deploy models as REST API endpoints. Three options: Foundation Model APIs host models like Claude, GPT, and Gemini on Databricks infrastructure (pay-per-token). External Models route to providers through a unified interface. Custom Models serve your own trained models. The infrastructure handles 250,000+ queries per second — you do not manage scaling.
- **Agent Framework and Agent Bricks** are how you build AI agents. Agent Bricks is the fast path — describe what you want the agent to do, connect your enterprise data, and it builds the agent for you. For more control, the Agent Framework SDK supports multi-agent systems, MCP servers, and custom logic. Think of a customer support agent that can look up orders, check refund policies, and generate responses — all governed by Unity Catalog.
- **MLflow 3.0** is the open-source ML lifecycle tool, redesigned for GenAI. Experiment tracking, model registry, prompt versioning, agent observability, and cross-platform monitoring. With over 30 million monthly downloads, it is the de facto standard for ML experiment management.
- **Vector Search** indexes your knowledge bases for semantic search — the backbone of RAG applications. Storage-optimized endpoints can handle over 1 billion vectors at 7x lower cost than previous versions. If you are building anything that needs to search through documents, this is how you do it.
- **AI Gateway** is the centralized control point for all AI services. Rate limiting, PII detection and redaction, safety guardrails, usage logging, and automatic provider fallback. This is how you govern AI usage without becoming a bottleneck.
- **AI Functions in SQL** bring intelligence directly to SQL queries. \`ai\_parse\_document\` extracts data from PDFs, images, Word, and PowerPoint files — GA since April 2026. Your analysts can parse invoices and contracts in SQL without writing Python.

**When to use Mosaic AI:** Model training and serving, building AI agents, RAG applications, AI governance, and parsing documents at scale. And increasingly — as part of your regular data engineering work.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*p2di_334plJaAfqIeug5PA.png)

## Beyond the Core: Four More Components Worth Knowing

These components are important, and you will encounter them as your platform grows. Here is what each one does:

- **Compute** is the engine behind everything. Three types: all-purpose clusters for interactive work ($0.55/DBU on AWS Premium), jobs clusters for production ($0.15/DBU), and serverless compute that handles everything automatically with no idle costs. The Photon engine — a C++ vectorized query engine — runs by default and delivers up to 5x better price-performance on compatible workloads. Simple rule: use jobs compute or serverless for production, all-purpose only for interactive development.
- **Databricks Apps** lets you build and deploy data applications directly on the platform. Python frameworks like Streamlit, Dash, and Gradio, or Node.js with React, Angular, or Svelte. Apps run on serverless compute, integrate with Unity Catalog, and authenticate through SSO. Perfect for building internal tools — a data quality monitor, a pipeline status dashboard, a self-service data request form.
- **Databricks Marketplace** is an open exchange for data, AI models, notebooks, and solution accelerators. Providers publish, consumers access directly in their workspace through Delta Sharing. As of 2026, the Marketplace also supports MCP servers — tools that AI agents can use to interact with external systems. Always check the Marketplace before building something from scratch.
- **CLI and Bundles** are how you treat Databricks as code. The CLI manages your workspace from the terminal. Declarative Automation Bundles (DABs) let you define your entire project in YAML — jobs, pipelines, endpoints, apps — and deploy with \`databricks bundle deploy\`. Integrates with GitHub Actions, Azure DevOps, and GitLab CI. This is infrastructure-as-code for Databricks, and it is how serious teams manage deployments.
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*A9ZZKrvpy6SkFdYT3pOJ9A.png)

## How Everything Fits Together

When I was learning Databricks, the moment it all clicked was when I stopped thinking about individual components and started seeing how they connect. Here is the mental model that helped me:

**Notebooks** are your workshop. You explore data, test ideas, and build prototypes.

When something is ready for production, you wrap it in a **Workflow** — scheduled, orchestrated, monitored. Or better yet, you rewrite it as a **Lakeflow** pipeline — declarative, with built-in quality rules and automatic dependency management.

Your data lands in **Delta Lake** tables. **Unity Catalog** sits on top of everything — controlling who can access what, tracking where data came from, and helping people find what they need.

**SQL analysts** query that same governed data through **SQL Warehouses** — with dashboards, Genie, and federated queries to external systems. No separate data copies.

**Data scientists** use **Mosaic AI** to train models, build agents, and deploy AI-powered applications — all connected to the same data, the same governance, the same platform.

And everything gets versioned and deployed through **Bundles** and the **CLI** — infrastructure-as-code, just like your application codebase.

That is the picture. Each component has one clear job, and Unity Catalog is the thread that holds it all together

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yNPIMeQtYr2VQY1TG9NhiA.png)

## Common Mistakes to Avoid

- **Running production on all-purpose clusters.** Nearly 4x more expensive than Jobs Compute. Switch to job clusters or serverless for anything scheduled — this one change can cut your compute bill dramatically
- **Writing raw Spark when Lakeflow would do.** If you are manually orchestrating Spark jobs with custom error handling and quality checks, Lakeflow does all of that declaratively with less code and better monitoring
- **Postponing Unity Catalog.** The cost of adding governance later is always higher than setting it up now. I have seen this play out multiple times. Set it up on day one
- **Ignoring serverless compute.** Serverless notebooks, jobs, and SQL warehouses eliminate idle costs and infrastructure management. Use them wherever available — the startup time alone is worth it
- **Building before checking the ecosystem.** Before writing a custom ingestion connector, check Lakeflow Connect. Before building an internal tool, check Databricks Apps. Before sourcing data, check the Marketplace. The platform is bigger than most people realize
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*AXqE4UR1YU1Z_1jFpihNdg.png)

## What Is Next

In the next article, we will look at **Databricks on Azure vs AWS vs GCP** — the real differences between cloud providers, which features are available where, and how to choose the right cloud for your Databricks deployment.

Make sure to subscribe to this series so you do not miss any upcoming articles.