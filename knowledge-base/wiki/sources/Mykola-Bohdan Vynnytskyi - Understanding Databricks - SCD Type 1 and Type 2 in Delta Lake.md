---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-08-01-vynnytskyi-scd-types
source_title: "Understanding Databricks: SCD Type 1 and Type 2 in Delta Lake"
source_author: Mykola-Bohdan Vynnytskyi
source_url: https://mbvyn.medium.com/understanding-databricks-scd-type-1-and-type-2-in-delta-lake-6ada4855c5d5
tags:
  - source/summary
  - data-modeling
  - data-engineering
  - series/understanding-databricks
source_ids:
  - src-2026-08-01-vynnytskyi-scd-types
status: active
---

# Mykola-Bohdan Vynnytskyi - Understanding Databricks - SCD Type 1 and Type 2 in Delta Lake

## Summary

Part eight covers slowly changing dimensions: **"The core trade-off: keep only current values, or
preserve history."** Type 1 overwrites; Type 2 closes the previous row and inserts a new version with
validity metadata.

The asymmetry argument is the one that matters: **"You can always ignore history, but you cannot recover
what you never kept."**

## Key claims

- **Dimension:** a table describing a business entity — customer, product, store.
- **SCD Type 0** keeps the original value permanently. **Type 1** overwrites, retaining only current
  state. **Type 2** adds a row per version with start date, end date, and current flag. **Type 3**
  stores one previous value in an extra column. **Type 4** keeps current values in the main table and
  history in a separate one.
- In Type 2, the **business key repeats across versions** while a **surrogate key** uniquely identifies
  each version, letting fact rows join to the precise historical version rather than the current one.
- **A single ordinary `MERGE` cannot both close a matched row and insert its replacement for the same
  key.** The demonstrated workaround unions two copies of each change — one with the real key to match
  and close the old row, one with a `NULL` merge key to force the insert — giving **"One MERGE, both
  effects."**
- Source changes must be **deduplicated and ordered** before a manual MERGE; multiple changes for one
  key can error or apply out of order.
- **AUTO CDC** replaces the older APPLY CHANGES API and handles Type 1 and Type 2 declaratively,
  including sequencing, deletes, and late-arriving data. `SEQUENCE BY` establishes logical event order;
  `APPLY AS DELETE WHEN` maps delete events to either deletes or closed history depending on SCD mode.
- **[Product-specific]** Code targets Delta Lake 4.x / Runtime 18. AUTO CDC generates `__START_AT` and
  `__END_AT` history columns. `STORED AS SCD TYPE 1` is optional because Type 1 is the default. APPLY
  CHANGES still works but AUTO CDC is the recommended API for new code.

## Why it matters

[[Slowly Changing Dimensions]] is a durable modeling concept that long predates this platform, and the
reason to keep it in an AI-focused vault is that **history retention determines what questions can be
asked later**. An agent or analyst asking "what did this customer's tier look like when that order was
placed" can only be answered from a Type 2 dimension; a Type 1 dimension has silently destroyed the
answer.

The MERGE limitation is also a genuinely instructive piece of engineering: the two-copy union trick
exists because `MERGE` matching is per-row, and understanding *why* the workaround is necessary is what
separates using a declarative API from debugging it when sequencing goes wrong.

## Tensions / open questions

- **Type 1 history loss is irreversible**, which is why the author's default recommendation is Type 2
  "when in doubt" — an opinion, and one that costs storage and query complexity the article does not
  quantify.
- Manual Type 2 logic is **error-prone without source deduplication and sequencing**, and a failure to
  close the old row leaves **two current rows for one business key**.
- Calling Type 2 "the backbone of proper data warehousing" is a value judgment.
- AUTO CDC behavior, generated column names, defaults, and API recommendations are product-specific and
  subject to change; the portable fallback is `MERGE`.

## Affected pages

- [[Slowly Changing Dimensions]]
- [[All_You_Need_Is_AI/knowledge-base/wiki/entities/Databricks]]
- [[Mykola-Bohdan Vynnytskyi]]

## Raw capture

- [[Understanding Databricks SCD Type 1 and Type 2 in Delta Lake]]

## Citations

- Raw capture: [[Understanding Databricks SCD Type 1 and Type 2 in Delta Lake]]
- Canonical URL: <https://mbvyn.medium.com/understanding-databricks-scd-type-1-and-type-2-in-delta-lake-6ada4855c5d5>
- Published 2026-08-01; captured 2026-10-23.

## Related pages

- [[Medallion Architecture]]
- [[Open Table Formats]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Delta Lake in Practice]]
- [[Mykola-Bohdan Vynnytskyi - Understanding Databricks - Time Travel in Delta Lake]]
