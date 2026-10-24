---
type: concept
created: 2026-10-23
updated: 2026-10-23
tags:
  - concept
  - data-modeling
  - data-engineering
source_ids:
  - src-2026-08-01-vynnytskyi-scd-types
  - src-2026-06-29-vynnytskyi-medallion-architecture
status: active
---

# Slowly Changing Dimensions

## Definition

A **dimension** describes a business entity — customer, product, store. **Slowly changing dimension**
(SCD) handling is the set of patterns for what happens when a descriptive attribute changes.
The trade, from
[[Mykola-Bohdan Vynnytskyi - Understanding Databricks - SCD Type 1 and Type 2 in Delta Lake]]:
**"keep only current values, or preserve history."**

| Type | Behaviour |
|---|---|
| **0** | Keep the original value permanently |
| **1** | Overwrite; only current state survives |
| **2** | Insert a new row per version with start date, end date, current flag |
| **3** | Keep one previous value in an extra column |
| **4** | Current values in the main table, history in a separate one |

## Why it matters

The reason a 1990s warehousing pattern belongs in an AI-focused vault is that **history retention
determines what questions can be asked later**. "What tier was this customer on when that order was
placed" is answerable from a Type 2 dimension and unanswerable from a Type 1 one — the Type 1 update
silently destroyed the evidence.

That makes SCD a **data-retention policy disguised as a modelling choice**, and the asymmetry is the
whole argument: **"You can always ignore history, but you cannot recover what you never kept."**

The same asymmetry runs through this vault's own practice. Immutable raw captures and the rule that
older claims are never erased without recording what changed are a Type 2 discipline applied to
knowledge: see [[Schema-Driven Knowledge Base]]. A wiki that overwrites claims in place is a Type 1
dimension, and loses the ability to answer when and why a position changed.

## Current synthesis

### Keys are what make history joinable

In Type 2, the **business key repeats across versions** while a **surrogate key** uniquely identifies
each version. Fact rows join to the surrogate key, which is how a historical measurement stays attached
to the attribute values that were true at the time rather than to today's values. Without the surrogate
key, Type 2 storage exists but delivers no historical correctness.

### A single MERGE cannot do it

Worth recording because it explains why declarative APIs exist here: **one ordinary `MERGE` cannot both
close a matched row and insert its replacement for the same key**, since matching is per-row. The
demonstrated workaround unions two copies of each change — one carrying the real key to match and close
the old row, one with a `NULL` merge key to force the insert — producing **"One MERGE, both effects."**

This sits on top of the general `MERGE` precondition in [[Open Table Formats]]: sources must be
deduplicated and ordered first, because multiple changes for one key can error or apply out of order.

### Declarative change data capture

Platform CDC APIs handle Type 1 and Type 2 declaratively, including sequencing, deletes, and
late-arriving data: a sequencing clause establishes logical event order, and a delete-mapping clause
decides whether a delete event becomes a physical delete or a closed history row. The generated history
columns and API naming are product-specific; **`MERGE` is the portable fallback.**

## Open questions

- **Type 1 history loss is irreversible.** The source's default recommendation of Type 2 "when in doubt"
  is an opinion, and it costs storage and query complexity that the vault has **no measurement for**.
- Manual Type 2 logic is error-prone without deduplication and sequencing; a failure to close the old
  row leaves **two current rows for one business key** — a corruption that reads as valid data.
- Calling Type 2 "the backbone of proper data warehousing" is a value judgment.
- Where does the analogy to knowledge versioning stop being useful? A wiki has no surrogate keys and no
  fact tables, so the mapping is about **retention discipline**, not implementation.

## Related pages

- [[Open Table Formats]]
- [[Medallion Architecture]]
- [[Table Layout Optimization]]
- [[Schema-Driven Knowledge Base]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - SCD Type 1 and Type 2 in Delta Lake]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Medallion Architecture Explained Simply]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
