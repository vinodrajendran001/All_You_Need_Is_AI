---
type: concept
created: 2026-10-23
updated: 2026-10-27
tags:
  - concept
  - agents
  - data-platform
  - evaluation
source_ids:
  - src-2026-08-23-vynnytskyi-genie-explained
  - src-2026-06-21-vynnytskyi-modern-data-platform
  - src-2026-05-21-bytebytego-batch
  - src-2026-10-19-bytebytego-uber-genie
status: active
---

# Text-to-SQL Agents

## Definition

A system that takes a natural-language question, generates SQL against governed tables, executes it, and
returns an answer or chart. The vault's main source is
[[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]].

> **Naming note.** This vault holds two unrelated systems called "Genie". **Databricks Genie** is the
> text-to-SQL interface described here. **Uber Genie**, in
> [[ByteByteGo - How Uber Built a Genie to Answer Questions Correctly]], is a Slack retrieval assistant
> over documentation. They share only a name.

## Why it matters

Text-to-SQL is the clearest commercial case where **accuracy comes from context and scope rather than
from model capability**. The vault's source states it twice, in two forms:
**"Scoping is where the accuracy comes from"** and
**"AI doesn't have an intelligence problem; it has a context problem."**

That is the same mechanism [[Context Engineering]] and [[Retrieval-Augmented Generation]] describe from
other directions: restricting and curating what the system can see improves output more reliably than
improving the model.

## Current synthesis

### Scope is the primary accuracy lever

An agent is configured over **selected tables** with instructions and example queries, not pointed at a
whole catalog. Narrowing the surface removes ambiguity before the model sees it — fewer candidate
joins, fewer same-named columns, fewer plausible-but-wrong interpretations.

This is why the layering in [[Medallion Architecture]] matters operationally. Pointing a text-to-SQL
agent at Bronze asks the model to resolve, at query time and without evidence, the inconsistencies the
Silver layer exists to remove once. The source is explicit that the interface **does not make raw data
reliable**.

### Curation signals recruited as a ranking function

The most interesting design detail is the **ontology**: a continuously learned knowledge graph holding
business terms, metric definitions, calculations, and relationships between data assets and teams —
ranked by authority signals of **usage, freshness, authorship, and catalog certification**.

This treats **organizational metadata as retrieval evidence**. Which table is actually used, how
recently it was refreshed, who owns it, and whether anyone certified it are cheap, already-existing
signals that encode the judgment a newcomer would otherwise have to ask a colleague for. It is a close
relative of the curation mechanisms in [[Institutional Knowledge Agents]], and a structural answer to
the ambiguity that defeats naive text-to-SQL.

### Governance as the capability boundary

Catalog permissions govern what the agent can see, so the agent inherits an existing, audited
authorization boundary rather than introducing a new one — a notably better position than bolting
guardrails onto an unconstrained query interface. See [[Agent Security and Governance]] and
[[Lakehouse Architecture]].

### Guardrails sit before execution, not after

[[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]] supplies the vault's only **production**
text-to-SQL deployment, and it is the counterweight to the vendor material above. Grab's Analytics Data
Warehouse team automated an investigation workflow over **15,000+ tables** — roughly half the queries in
its data lake, serving about **1,000 monthly internal users**. The team's observation is the one that
justifies the whole category: the questions varied constantly, but the **investigation playbook stayed
the same** — search the catalog, trace lineage, validate with SQL, check pipeline logs. Consistency of
process, not of question, is what made the work automatable.

Its guardrails are structured as layers that run **before** any query executes. A Classifier extracts
table and column references and rejects PII requests and out-of-scope questions up front. Every
generated query is then validated for PII column access, destructive operations such as `DELETE` or
`DROP`, **missing partition filters** — which would otherwise scan an entire table rather than the
relevant slice — and schema validity. The Data Agent validates schemas specifically to avoid
unnecessary scans.

This is worth separating from the failure mode below. Grab's layers prevent **dangerous and expensive**
queries; none of them establish that a permitted query returns the **right number**. Guardrails and
correctness evaluation are different problems, and the vault still holds a source for only the first.
Grab's reported gains — routine inquiries mostly handled by the system, resolution time down an **order
of magnitude** — are first-party and unablated.

### The failure mode

**A text-to-SQL agent can answer confidently from poor data.** The output is a fluent sentence and a
number, and nothing in the interface distinguishes a correct aggregation from a wrong join. This is the
case for [[Embedded Evaluation]] and [[LLM-as-a-Judge]]-style harnesses rather than spot-checking, and
**no source in the vault supplies an evaluation harness** for detecting it — Grab's pre-execution
validation is the closest thing, and it checks safety and cost rather than correctness.

## Open questions

- **The only accuracy figure the vault holds is vendor-reported and unmethodologized**: 84.5%
  first-attempt accuracy versus 52.4% for "the strongest general-purpose coding agent", with no task
  distribution, no baseline description, and no independent replication. The author himself advises
  skepticism. It must not be cited as a measured capability. See [[Benchmark Optimization]] for why
  self-reported comparisons on self-chosen tasks are weak evidence.
- "First-attempt accuracy" is not defined in the vault. Accuracy against what ground truth, over which
  question distribution, judged by whom?
- What is the right evaluation design for a system whose errors are **plausible SQL producing wrong
  numbers**? Execution success is not correctness.
- Does the ontology's authority ranking entrench incumbency — heavily used tables become more
  recommended, and correct-but-new tables stay invisible?
- How much curation work does the accuracy depend on, and who does it? The curation cost is the hidden
  denominator in every text-to-SQL claim.

## Related pages

- [[Context Engineering]]
- [[Retrieval-Augmented Generation]]
- [[Institutional Knowledge Agents]]
- [[Medallion Architecture]]
- [[Lakehouse Architecture]]
- [[Agent Security and Governance]]
- [[Embedded Evaluation]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
- [[Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Genie Explained]]
- [[ByteByteGo - How Uber Built a Genie to Answer Questions Correctly]]
- [[ByteByteGo - System Design and AI at Scale (May 2026 Batch)]]
- [[Uber]]
