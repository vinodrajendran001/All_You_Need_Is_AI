---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-19-bytebytego-uber-genie
source_title: How Uber Built a Genie to Answer Questions Correctly
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-uber-built-a-genie-to-answer-051
tags:
  - source/summary
  - rag
  - internal-tools
  - system-design
source_ids:
  - src-2026-10-19-bytebytego-uber-genie
status: active
---

# ByteByteGo - How Uber Built a Genie to Answer Questions Correctly

## Summary

A system-design walkthrough of **Uber's Genie**, an internal Slack assistant that answers engineering
support questions by retrieval rather than fine-tuning. The architectural argument is that internal
documentation changes constantly, so retrieving passages at question time is cheaper and fresher than
retraining a model on them.

The design detail worth keeping is that Genie presents each retrieved passage as a **separate
sub-context carrying its source URL**, instructs the model to answer only from those contexts, and
cites the URLs — then explicitly refuses to treat citation as proof of correctness.

**Naming note:** this Genie is unrelated to the Databricks Genie discussed in
[[Databricks AI Research - MemCurrent Persistent Memory for Production Agents]].

## Key claims

### Pipeline

- **Knowledge preparation:** an ETL pipeline extracts content from Engwiki, internal Stack Overflow, and
  other documents, transforms it into chunks and embeddings, and loads it for retrieval, using Apache
  Spark and Spark DataFrames.
- **Indexing and serving:** LangChain chunks documents; an OpenAI embedding model represents meaning;
  **Sia** stores and searches vectors; **Terrablob** stores index data; serving machines called
  **leaves** download and synchronize index snapshots.
- **Answering:** a Slack question goes to Knowledge Service, is embedded, matched against the vector
  index, and combined with retrieved passages, source information, the question, and answer
  instructions before generation.
- **Corpus restriction:** Genie's sources are limited to information broadly available to developers —
  a permissions control implemented by corpus scoping rather than per-user filtering.
- **Fallback:** users can ask follow-ups, mark an issue resolved, or escalate to human support; Genie
  **mutes itself** once a human takes over.
- **Feedback loop:** Slack feedback categories flow through Kafka to Hive and into dashboards.
- **Evaluation loop:** recorded contexts, answers, metadata, and feedback are scored by an **LLM judge**
  for qualities such as relevance and hallucination. Notably, the **documents themselves** also receive
  scores, explanations, and improvement suggestions through the Michelangelo interface.
- A UUID passed from the Slack client through Knowledge Service to the Michelangelo Gateway supports
  audit and cost tracking.

### Reported numbers — all self-reported by Uber

- Internal support channels received approximately **45K questions each month**.
- Genie launched in **September 2023**; within a year it was used in **154 Slack channels** and had
  answered **more than 70K questions**.
- Overall helpfulness / full-resolution rate: **48.9%**. No baseline or comparison is stated.
- Engineering-time savings: **around 13,000 hours**. The explanation of how this was derived is
  **truncated in the capture** mid-sentence.

## Why it matters

[[Institutional Knowledge Agents]] in this vault has collected several internal-assistant designs. Genie
contributes two mechanisms the others lack.

First, **the evaluation loop scores the documentation, not only the answers.** An LLM judge that emits
improvement suggestions for source documents turns a question-answering system into a
documentation-quality instrument — the assistant's failures become a map of where internal docs are
wrong or missing.

Second, the **48.9% helpfulness rate** is a rare published number for this class of system, and the
article is careful that "helpful" is not "fully resolved" and that "Not Relevant" often means the
request (for example code review) was outside the assistant's role at all. That is a more honest
framing than the usual deflection-rate headline.

For [[Retrieval-Augmented Generation]], the sub-context-with-URL prompt structure is a concrete
implementation of grounding that the vault has mostly described abstractly.

## Tensions / open questions

- **The capture is truncated.** The conclusion breaks mid-sentence at the cost-tracking discussion, so
  the derivation of the 13,000-hour savings figure is not recoverable.
- All usage, helpfulness, and savings figures are **self-reported by Uber** and relayed by a third-party
  explainer; ByteByteGo's own disclaimer says the article is based on publicly shared details and may
  contain inaccuracies.
- No precision/recall, hallucination rate, latency, cost-per-answer, or controlled comparison against
  human support is given.
- The article is explicit that **citations do not guarantee correctness**: retrieved passages may be
  irrelevant, source documents may themselves be wrong, and the model may misrepresent them —
  **"A source link doesn't guarantee that every statement is correct."**
- There is no evidence that the LLM judge's scores correlate with human judgment, which weakens both the
  answer evaluation and the document scoring.
- Nothing establishes that the design generalizes beyond Uber's curated internal corpus and support
  workflow.

## Affected pages

- [[Institutional Knowledge Agents]]
- [[Retrieval-Augmented Generation]]
- [[ByteByteGo]]
- [[Uber]]

## Raw capture

- [[How Uber Built a Genie to Answer Questions Correctly]]

## Citations

- Raw capture: [[How Uber Built a Genie to Answer Questions Correctly]]
- Canonical URL: <https://blog.bytebytego.com/p/how-uber-built-a-genie-to-answer-051>
- Published 2026-10-19; captured 2026-10-22. **Capture is truncated near the conclusion.**
- Relays Uber engineering material that was not read directly during this ingest.

## Related pages

- [[LLM-as-a-Judge]]
- [[Approximate Nearest-Neighbor Search]]
- [[Embedding Model Selection]]
- [[Agent Observability]]
- [[AI Agents in Production]]
- [[Direct Corpus Interaction]]
- [[Retrieval Poisoning]]
