---
title: "Understanding Databricks: Genie Explained — Genie One, Agents, and the Ontology"
source: "https://mbvyn.medium.com/understanding-databricks-genie-explained-genie-one-agents-and-the-ontology-710792b66c5a"
author:
  - "[[Mykola-Bohdan Vynnytskyi]]"
published: 2026-08-23
created: 2026-10-23
description: "What actually shipped, what the names mean, and why it’s free until February 2027. Updated August 2026."
tags:
  - "clippings"
---
## What actually shipped, what the names mean, and why it’s free until February 2027. Updated August 2026.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*NF9Av7vUKjU3le2Sp2rJNw.png)

If you’ve tried to follow what’s happening with Databricks Genie this year, I don’t blame you for being confused. Databricks One became Genie. Genie Spaces became Genie Agents. Something called Genie One appeared, which is not the same as Databricks One, except it sort of is. And half the articles online still use last year’s names.

I spent a good chunk of a weekend untangling this, and it turned out to be worth the time. Genie is the biggest bet Databricks made at this year’s Data+AI Summit. It’s the closest thing yet to “ask your data a question, get a correct answer.” And the part almost nobody has noticed: **it’s completely free to use until January 31, 2027.**

So let’s decode the whole family as it exists today. What each piece does, what’s GA versus preview, how the Ontology works under the hood, and what any of this has to do with you as a data engineer. Current names, verified statuses, no hype.

This article is part of the Understanding Databricks series. It builds on [What a Modern Data Platform Looks Like](https://medium.com/@mbvyn/understanding-databricks-what-a-modern-data-platform-looks-like-in-2026-649a95cf1293?sharedUserId=mbvyn), where we first covered the “context problem” that Genie was built to solve.

> **Key takeaways**
> 
> Genie is Databricks’ natural-language interface to data: ask questions in plain English, get governed answers. It was renamed from “Databricks One” in April 2026.
> 
> Genie One (GA) is the agentic coworker app for business users on web, mobile, Slack, and Teams. Genie Agents (GA) are the configurable agents formerly called Genie Spaces.
> 
> The Genie Ontology (Public Preview) is the engine underneath: a self-learning knowledge graph of your tables, queries, dashboards, and 50+ connected apps that gives Genie business context.
> 
> For engineers there’s Genie Code (GA) for dashboards and notebooks, and Genie ZeroOps (private preview) for autonomous pipeline operations.
> 
> Pricing: a consumption model (150 free DBUs per user per month) launched in July 2026 and was immediately paused. **Genie One and Genie Agents are free through January 31, 2027.**
> 
> For data engineers, Genie changes the job: your data quality, documentation, and governance are now the difference between an AI that answers correctly and one that guesses.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-B3N7NfElzMKVudk_prv9A.png)

## What Genie Is (and Why the Names Keep Changing)

Genie is Databricks’ conversational interface to data. You ask a question in natural language (“what was our revenue by region last quarter?”), it writes the SQL, runs it against your governed tables, and returns the answer with charts. That core idea has existed for a while. What changed in 2026 is scale, ambition, and unfortunately also the naming.

The timeline, so you can decode any article you read:

- **April 27, 2026 —** Databricks One, the no-code experience for business users, was renamed Genie. One brand for the whole conversational layer
- **June 9, 2026** — the business-user experience got its own name: Genie One
- **June 16, 2026** — at the Data+AI Summit, Genie One went GA alongside the Genie Ontology and a wave of new capabilities
- **July 8, 2026** — Genie Spaces were renamed Genie Agents

So today the family looks like this: Genie is the umbrella. Genie One is the app people use. Genie Agents are the configurable agents underneath. The Ontology is the brain that gives them context. Genie Code and Genie ZeroOps are the engineer-facing side.

I’ll be honest, I think three renames in four months was a self-inflicted wound, and it’s the main reason this article needs to exist. But here we are. Let’s take the pieces one at a time.

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

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tznkOmM90R0glCmWp_ipqw.png)

## Genie One: An AI Coworker for Every Team

**Genie One** is the flagship, generally available since June 16, 2026. Databricks positions it not as a chat-with-your-data toy but as an agentic coworker, and for once the marketing distinction is real: a chat interface answers questions, while this thing also creates documents, runs scheduled tasks, follows up on multi-step requests, and calls external tools through MCP.

In practice, that means a business user gets a full-screen conversational workspace where they can explore data, ask follow-ups, and get charts without touching SQL. It lives everywhere the team already works: web is GA, iOS and Android apps are in Public Preview, and Slack and Teams integrations launched in June (the dedicated Teams app is also in Public Preview).

==There’s an agent mode, where instead of answering one question at a time, Genie builds a research plan, runs several queries in parallel, and assembles an answer with its reasoning visible.==

Scheduled tasks (Public Preview) let you set up recurring prompts with results delivered by email, basically a self-writing Monday-morning report.

And a feature called Inspect (Public Preview) makes Genie iteratively verify its own SQL before answering, which sounds minor but matters a lot for accuracy.

For your business colleagues, this is the promise of “self-service analytics” that BI tools have been making for twenty years. Except this time the interface is a sentence, not a dashboard builder.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-e8qni1U8nMGdnBeUGaU8Q.png)

## Genie Agents: Scoped, Configurable, Shareable

Underneath Genie One sit **Genie Agents**, the renamed Genie Spaces. An agent is a scoped assistant you configure over a specific set of data: you pick the tables, add instructions and example queries, and share it with a team.

Scoping is where the accuracy comes from. A general-purpose assistant over your entire catalog has to guess which “revenue” column of the eleven in your lakehouse is the right one. An agent scoped to the finance schema with curated instructions doesn’t guess. It knows.

The 2026 upgrades made agents notably more capable. They reason over unstructured data now, not just tables. They call external tools via MCP, and a managed MCP server (Beta) lets other agents ask your Genie Agents questions, which effectively turns your data into a service for the whole agent ecosystem. They can also be shared externally, beyond your workspace.

If Genie One is the coworker, agents are its specialist skills. And you, the data engineer, are the one who builds and curates them.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*2PFYs1Lcf0e_4dN46YhgHw.png)

## The Genie Ontology: The Context Layer

Now for the piece that makes the rest work. The **Genie Ontology** (Public Preview since May 2026, despite what some coverage implies — it’s not GA yet) is a continuously learned knowledge graph of what your data *means*.

The problem it solves is one you already know if you’ve ever onboarded a new analyst. An LLM can write SQL. What it can’t do, out of the box, is know that in *your* company “active customer” means someone with a purchase in the last 90 days, that \`rev\_adj\` is the column Finance actually uses, and that the numbers in the CFO’s certified dashboard outrank the ones in an intern’s scratch query. That knowledge lives in people’s heads, in Slack threads, in wiki pages nobody updates. The Ontology goes and gets it.

It automatically extracts “knowledge snippets” from your tables, queries, dashboards, and pipelines, and from 50+ connected apps: Google Drive, Jira, Slack, Confluence, SharePoint, Gmail, Teams, and more (external source connections are in Beta). It captures metric definitions, business terms, calculations, and the relationships between concepts, tables, and teams. When sources disagree, it resolves authority with a PageRank-like approach that weighs who wrote it, how often it’s used, whether the asset is certified in Unity Catalog, and how fresh it is.

Databricks’ own benchmark claims Genie with the Ontology answered 84.5 percent of real employee questions correctly on the first attempt, versus 52.4 percent for the strongest general-purpose coding agent. It’s a vendor benchmark, so treat the exact number with healthy skepticism. But the direction is credible, because it matches the thesis from [What a Modern Data Platform Looks Like](https://medium.com/@mbvyn/understanding-databricks-what-a-modern-data-platform-looks-like-in-2026-649a95cf1293?sharedUserId=mbvyn): AI doesn’t have an intelligence problem; it has a context problem. The Ontology is Databricks’ answer to exactly that.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rn4G_RMfKH-Kp3n2uO05ZQ.png)

## Genie for Engineers: Code and ZeroOps

Genie isn’t only for business users. Two members of the family point straight at us.

**Genie Code** (GA) is the AI development assistant woven through the platform. It authors AI/BI dashboards from natural language (GA since May), works inside notebooks (GA since July), can import Tableau and Power BI workbooks and rebuild them as native dashboards (Beta). Since late July, it’s available even in HIPAA-compliant workspaces. If you write Databricks code daily, this is the piece you’ll touch first.

**Genie ZeroOps** (announced at the Summit, currently in private preview, so you can’t self-serve it yet) is the more radical idea: a background agent that watches your jobs, pipelines, tables, and ML systems, detects problems, diagnoses root causes, and proposes or applies fixes. Agentic data engineering, in other words. The pipeline that pages an AI instead of paging you. It’s early, and I wouldn’t plan production processes around it yet. Still, the direction is unmistakable: the maintenance-automation story we saw with predictive optimization in [the table optimization article](https://medium.com/@mbvyn/understanding-databricks-optimizing-delta-tables-6065b1388676?sharedUserId=mbvyn) is expanding from tables to entire pipelines.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tMAD0qPekQrKTGaB2XozZA.png)

## Pricing: Free Until February 2027

This is the part surprisingly few people know about, and it’s the best reason to act now.

At the Summit, Databricks announced consumption-based pricing for Genie, with no per-seat licenses. Every identified human user gets **150 free DBUs of AI usage per month** (roughly $10.50 worth at US rates), resetting monthly, with overage billed per DBU. Pay-as-you-go duly started on July 6, 2026.

And then, nine days later, Databricks paused billing entirely. As of July 15, reconfirmed on August 3: **Genie One and Genie Agents usage is free through January 31, 2027**, and the charges from that first week were credited back. The free-allowance model still exists on paper and will presumably switch on in February 2027. One note for planning: service principals (that is, automated agents) get no free allowance and will be billed from the first request when it does.

The logic isn’t hard to guess. Databricks wants adoption now and revenue later, betting that agent-driven usage grows the pie. For you, the takeaway is simpler: the next six months are a free trial of the flagship AI product on the platform you already use. If you’ve been waiting for a reason to evaluate Genie with your real data, this is it.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zgtg0SqvfVLDmi_aPcXHbA.png)

## What This Means for Data Engineers

You might be tempted to file Genie under “business user stuff.” I’d push back on that.

When a human analyst gets a confusing query result, they investigate.

When Genie gets confusing data, it answers anyway, and the quality of that answer is determined almost entirely by the platform *you* built. Every practice from this series suddenly has a second customer, and that customer reads everything. Table and column comments stop being nice-to-have documentation; they’re context the Ontology ingests and reasons over.

Unity Catalog certification now literally changes answer authority, because certified assets outrank uncertified ones in conflict resolution. Clean Silver and Gold layers with clear naming become the difference between 84 percent accuracy and a confident hallucination. And since Genie respects Unity Catalog permissions, your ACLs decide what an agent can see on whose behalf.

My honest advice: pick one well-modeled domain, your cleanest Gold schema, create a scoped Genie Agent over it, write good instructions, and hand it to a friendly business team while it’s free. You’ll learn more about the real state of your data quality in two weeks of Genie questions than from any audit. And you’ll be six months ahead of your market when this becomes the default way companies consume data.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_cJANPBpfQ67myJ7OgxzEA.png)

## Common Mistakes to Avoid

- **Confusing the names in 2026 content.** Databricks One → Genie (April). Genie Spaces → Genie Agents (July). Genie One is the business app, not the old Databricks One. Check the date on anything you read
- **Assuming everything is GA.** Genie One, Agents, and Code are GA. The Ontology is Public Preview. ZeroOps is private preview. Mobile apps are in Public Preview. Plan accordingly
- **Pointing Genie at raw or messy data.** An agent over your Bronze layer will confidently answer with garbage. Scope agents to curated Silver and Gold tables
- **Skipping instructions and examples.** A scoped agent with good instructions and sample queries dramatically outperforms a bare one. Curation is the job
- **Ignoring the free window.** Free until January 31, 2027, then consumption pricing with 150 DBUs free per user per month. Evaluate now; budget for February
- **Treating documentation as optional.** Comments, certified assets, and clear metric definitions now directly feed answer quality. Undocumented data is invisible context
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MJipmHfSIjYMYmgU6kERlQ.png)

## Frequently Asked Questions

### What is Databricks Genie?

Genie is Databricks’ natural-language interface to data: an AI layer where users ask questions in plain English and get governed, verifiable answers from lakehouse data. The family includes Genie One (the app for business users), Genie Agents (scoped configurable agents), the Genie Ontology (the knowledge graph providing business context), and Genie Code (the developer assistant).

### What is the difference between Genie One and Genie Agents?

Genie One is the agentic coworker application (chat, mobile, Slack, and Teams) that business users interact with.

Genie Agents, formerly Genie Spaces, are the scoped assistants underneath: each agent is configured over specific tables with instructions and examples, then shared with a team. Genie One went GA in June 2026; Agents were renamed from Spaces in July 2026.

### Is Databricks Genie free?

Right now, yes. Databricks paused Genie billing on July 15, 2026, and Genie One and Genie Agents are free through January 31, 2027. After that, the consumption model applies: every identified user gets 150 free DBUs of AI usage per month, with overage billed per DBU and no free allowance for service principals.

### What is the Genie Ontology?

A continuously-learned knowledge graph (Public Preview) that extracts business meaning, such as metric definitions, terms, and relationships, from your tables, queries, dashboards, pipelines, and 50+ connected apps like Slack, Jira, and Google Drive. It resolves conflicting definitions using authority signals such as Unity Catalog certification, usage frequency, and freshness, and it’s what grounds Genie’s answers in your business context.

### How accurate is Genie?

Databricks’ internal benchmark reports 84.5 percent first-attempt accuracy on real employee questions with the Ontology, versus 52.4 percent for the strongest general-purpose coding agent. It’s a vendor benchmark, so treat the exact figure cautiously. What’s not in question is that accuracy depends heavily on your data quality, documentation, and how well agents are scoped and instructed.

### What do data engineers need to do for Genie?

Feed it context: comment your tables and columns, certify trusted assets in Unity Catalog, keep Silver and Gold layers clean and clearly named, and scope agents to curated schemas with good instructions. Genie inherits Unity Catalog permissions, so your governance model is also its safety boundary.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Iv-Im_ydwNpdig8n_iCacQ.png)

## What Is Next

Genie is one half of the biggest story on the platform right now: the AI that consumes your data. In the next article, we cover the other half: Lakebase and LTAP, the operational database Databricks built into the lakehouse, and the architecture that promises to end the wall between transactional and analytical data. If Genie changes who asks the questions, Lakebase changes where the data lives.

Make sure to bookmark this series so you don’t miss any upcoming articles.

*Want more? Visit* [*mbvyn.com*](https://mbvyn.com/) *for mentorship, consulting, and all my content in one place.*

*And if you work with Parquet files, try* [*parquetreader.app*](https://parquetreader.app/) *— my free tool for exploring them on the desktop.*