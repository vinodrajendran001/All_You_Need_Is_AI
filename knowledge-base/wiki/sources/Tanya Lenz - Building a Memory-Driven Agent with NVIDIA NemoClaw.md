---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-05-lenz-nemoclaw-memory-agent
source_title: "Building a Memory-Driven Agent with NVIDIA NemoClaw"
source_author: Tanya Lenz
source_url: https://developer.nvidia.com/blog/building-a-memory-driven-agent-with-nvidia-nemoclaw/
tags: [source/summary, agent-memory, governance, evaluation]
source_ids: [src-2026-09-05-lenz-nemoclaw-memory-agent]
status: active
---

# Tanya Lenz - Building a Memory-Driven Agent with NVIDIA NemoClaw

## Summary

NVIDIA's memory-driven Chief of Staff separates source evidence, derived knowledge, and authorized
action. Structured Markdown stores a human-readable self model with provenance; SQLite stores
obligations, rankings, corrections, and audit events. Scheduled maintenance and bounded retrieval
turn that state into task-specific context, while OpenShell keeps filesystem, process, network, and
credential access behind a separate policy boundary.

## Key claims

- On 186 author-reported questions, the self model raised overall accuracy from **82.8% to 90.9%**.
- Hard questions improved **67.7% to 87.1%** (`n=31`), entity disambiguation **66.7% to 86.7%**
  (`n=15`), and multisource synthesis **87.7% to 94.5%** (`n=73`).
- Citation coverage rose **92.5% to 97.8%**.
- The intervention was not uniformly beneficial: corpus faithfulness fell **100% to 92.3%**
  (`n=13`) and single-hop lookup fell **86.7% to 83.3%** (`n=30`).
- Corrections follow an inspectable path: judgment, user correction, audit event, preference update.

## Why it matters

The design makes memory a governed artifact rather than accumulated conversation. It also preserves
the distinction between contextual knowledge and authority: knowing a preferred communication channel
does not grant permission or credentials to use it.

## Tensions and caveats

- NVIDIA reports the benchmark; there is no independent replication or significance analysis.
- Several subsets are tiny (`n=5`, `n=6`, and `n=13`), making large percentage-point changes unstable.
- The walkthrough uses invented workplace data and prerecorded offline decisions, sends no real
  messages, and changes no source systems.

## Raw capture

- [[2026-09-05 Tanya Lenz - Building a Memory-Driven Agent with NVIDIA NemoClaw]]

## Affected pages

- [[Agent Memory]]
- [[Agent Security and Governance]]
- [[NVIDIA]]

## Related pages

- [[Context Engineering]]
- [[Institutional Knowledge Agents]]
- [[Continual Learning for Agents]]

