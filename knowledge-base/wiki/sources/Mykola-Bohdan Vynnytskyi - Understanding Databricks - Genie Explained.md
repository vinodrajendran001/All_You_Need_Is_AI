---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-08-23-vynnytskyi-genie-explained
source_title: "Understanding Databricks: Genie Explained — Genie One, Agents, and the Ontology"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-genie-explained-genie-one-agents-and-the-ontology-710792b66c5a
tags:
  - source/summary
  - agents
  - text-to-sql
  - series/understanding-databricks
source_ids:
  - src-2026-08-23-vynnytskyi-genie-explained
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained

## Summary

Part eleven untangles a year of renaming — Databricks One became Genie, then Genie One, then Genie
Spaces became Genie Agents — and separates the pieces: **Genie** (natural-language interface that
generates and runs SQL over governed data), **Genie One** (the business-user application), **Genie
Agents** (scoped assistants configured over selected tables), the **Ontology** (a continuously learned
knowledge graph of business meaning), **Genie Code**, and **Genie ZeroOps**.

The claim the vault should keep is about where accuracy comes from: **"Scoping is where the accuracy
comes from"**, and **"AI doesn't have an intelligence problem; it has a context problem."**

> **Naming note.** This is **Databricks Genie**, a text-to-SQL interface over governed tables. It is not
> **Uber Genie**, the Slack retrieval assistant covered in
> [[ByteByteGo - How Uber Built a Genie to Answer Questions Correctly]]. The two systems share only a
> name.

## Key claims

- A **Genie Agent** is configured over **selected tables** with instructions and example queries, rather
  than pointed at a whole catalog. Narrowing the surface is presented as the primary accuracy lever.
- The **Ontology** captures business terms, metric definitions, calculations, and relationships among
  data assets and teams, and ranks authority using **usage, freshness, authorship, and Unity Catalog
  certification** — treating curation signals as retrieval evidence.
- **Unity Catalog permissions govern what Genie can see**, making the governance layer the safety
  boundary for the agent rather than a separate guardrail.
- Genie Agents can reach unstructured data and external tools via **MCP**, per the article.
- **Genie Code** is the engineering-facing assistant for dashboards and notebooks; **Genie ZeroOps** is
  an autonomous data-platform operations concept.
- Answer quality depends on **curated Silver/Gold data, documentation, instructions, examples, and
  scope** — Genie does not make Bronze data reliable.
- **[Vendor claim]** A Databricks benchmark reports **84.5% first-attempt accuracy** versus **52.4%** for
  "the strongest general-purpose coding agent". **No methodology, task distribution, or independent
  replication is supplied.**
- **[Self-reported, time-sensitive]** Renames: Genie **2026-04-27**, Genie One **2026-06-09**, GA for
  Genie One and Ontology **2026-06-16**, Genie Agents **2026-07-08**. Ontology is **Public Preview since
  May 2026** and connects to **50+** applications (external connections Beta). Scheduled tasks and
  Inspect are Public Preview; mobile and a dedicated Teams app are Public Preview; Genie Code is GA with
  Beta BI import; ZeroOps is private preview. Pricing: **150 free DBUs per identified user per month**
  (~**$10.50** at stated US rates), with Genie One and Agents free **through 2027-01-31**.

## Why it matters

This is the clearest product-side statement of [[Text-to-SQL Agents]] as a **context and governance
problem rather than a model problem**. The mechanism is the same one this vault keeps finding in
[[Context Engineering]] and [[Retrieval-Augmented Generation]]: restricting and curating what the system
can see improves output more reliably than improving the model.

The Ontology's authority signals are the notable design detail. Usage, freshness, authorship, and
certification are **organizational metadata recruited as a ranking function** — a structural answer to
the ambiguity that defeats naive text-to-SQL, and a close cousin of the curation signals in
[[Institutional Knowledge Agents]].

Binding agent capability to Unity Catalog permissions also matters for
[[Agent Security and Governance]]: the agent inherits an existing, audited authorization boundary
instead of introducing a new one.

## Tensions / open questions

- The **84.5% vs 52.4%** comparison is **vendor-reported with no published methodology**; the author
  himself advises skepticism. It should not be cited as a measured capability.
- Most components sit at different preview stages, so the described system is partly aspirational.
- Pricing and the free period are explicitly temporary.
- **Genie can answer confidently from poor data** — a confident wrong answer over Bronze tables is the
  central failure mode, and the article offers no evaluation harness for detecting it.
- The repeated renaming makes older documentation unreliable, which is itself a cost.
- Calling the rename sequence a "self-inflicted wound" and predicting Genie becomes the default
  consumption interface are opinion.

## Affected pages

- [[Text-to-SQL Agents]]
- [[Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]

## Raw capture

- [[Understanding Databricks Genie Explained — Genie One, Agents, and the Ontology]]

## Citations

- Raw capture: [[Understanding Databricks Genie Explained — Genie One, Agents, and the Ontology]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-genie-explained-genie-one-agents-and-the-ontology-710792b66c5a>
- Published 2026-08-23; captured 2026-10-23.

## Related pages

- [[Context Engineering]]
- [[Retrieval-Augmented Generation]]
- [[Institutional Knowledge Agents]]
- [[Agent Security and Governance]]
- [[Medallion Architecture]]
- [[ByteByteGo - How Uber Built a Genie to Answer Questions Correctly]]
