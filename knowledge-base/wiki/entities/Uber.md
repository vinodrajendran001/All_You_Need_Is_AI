---
type: entity
created: 2026-10-23
updated: 2026-10-27
entity_kind: organization
tags:
  - entity
  - ai-agents
  - rag
source_ids:
  - src-2026-10-19-bytebytego-uber-genie
  - src-2026-10-25-rastogi-agentcore-enterprise
status: active
---

# Uber

## What it is

A ride-hailing and delivery company whose internal engineering-support assistant, **Genie**, is covered
in this vault through [[ByteByteGo - How Uber Built a Genie to Answer Questions Correctly]].

> **Naming note.** Uber Genie is a Slack retrieval assistant over internal documentation. It is
> unrelated to **Databricks Genie**, the text-to-SQL interface described in [[Text-to-SQL Agents]].

## Why it matters here

Uber appears in this vault as a **production case study in retrieval over fine-tuning**, and the
reasoning is worth keeping: internal documentation changes constantly, so retrieving passages at
question time is cheaper and fresher than retraining a model on them. This is the practical argument
behind [[Retrieval-Augmented Generation]] stated in operational rather than academic terms.

Three design choices generalize beyond Uber:

**Each retrieved passage is a separate sub-context carrying its source URL.** The model is instructed to
answer only from those contexts and to cite the URLs — and the source explicitly refuses to treat
citation as proof of correctness. That refusal is the part most systems skip.

**Permissions are enforced by corpus scoping, not per-user filtering.** Genie's sources are limited to
information already broadly available to developers, which sidesteps the per-query authorization problem
by making the whole corpus safe for the whole audience. It is a blunt but auditable boundary — contrast
the per-user approaches in [[Multi-Tenant Agent Architecture]].

**The evaluation loop scores the documents, not only the answers.** An LLM judge rates recorded
contexts and answers for qualities such as relevance and hallucination, and **the underlying documents
also receive scores, explanations, and improvement suggestions**. That closes a loop most retrieval
systems leave open: bad answers become documentation defects with an owner, rather than model
complaints. See [[Institutional Knowledge Agents]] and [[LLM-as-a-Judge]].

A smaller detail worth noting: **Genie mutes itself once a human takes over**, which is a clean
handover rule for assistants operating in shared channels.

Uber also appears secondhand as an agent-platform reference.
[[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]] cites its MCP
Gateway, which hosts over 800 MCP servers and more than 5,000 tools, and its short-lived, single-hop JSON
Web Tokens (JWTs) that carry the full actor chain; see [[Tool Roster Economics]] and
[[Agent Security and Governance]].

## Notes

### The numbers are self-reported, and one is unrecoverable

- Internal support channels received approximately **45K questions per month**; Genie launched in
  **September 2023** and within a year was used in **154 Slack channels**, answering more than
  **70K questions**.
- Overall helpfulness / full-resolution rate: **48.9%**, with **no baseline or comparison stated** —
  so whether that is good is unknown. Roughly half of answered questions were not fully resolved.
- An engineering-time saving of **around 13,000 hours** is claimed, but **the derivation is truncated in
  the vault's capture**, so the vault cannot reconstruct how the figure was produced and should not cite
  it as evidence.

## Related pages

- [[Retrieval-Augmented Generation]]
- [[Institutional Knowledge Agents]]
- [[LLM-as-a-Judge]]
- [[Agent Observability]]
- [[Multi-Tenant Agent Architecture]]
- [[Approximate Nearest-Neighbor Search]]
- [[Embedding Model Selection]]
- [[Text-to-SQL Agents]]
- [[ByteByteGo]]
- [[ByteByteGo - How Uber Built a Genie to Answer Questions Correctly]]
- [[Sarthak Rastogi - How to Build an Enterprise AI Agent System with AgentCore (Part 1)]]
- [[Tool Roster Economics]]
- [[Agent Security and Governance]]
