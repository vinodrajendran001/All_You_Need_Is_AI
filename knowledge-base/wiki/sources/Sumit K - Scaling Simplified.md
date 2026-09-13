---
type: source-summary
created: 2026-09-13
updated: 2026-09-13
source_id: src-2026-09-13-sumit-scaling-distributed-systems
source_title: "Scaling Simplified: How Distributed Systems Handle Millions"
source_author: Sumit K
source_url: https://medium.com/google-cloud/scaling-simplified-how-distributed-systems-handle-millions-2854aa1024c6
tags:
  - source/summary
  - distributed-systems
  - scalability
  - system-design
source_ids:
  - src-2026-09-13-sumit-scaling-distributed-systems
status: active
---

# Sumit K - Scaling Simplified

## Summary

An introductory taxonomy of vertical, horizontal, and diagonal scaling plus load balancing, caching, sharding, and asynchronous work. It is useful as a checklist and as a reminder that performance and scalability are different properties, but the title's "millions" is not supported by measurements or case studies.

## Key claims

- Vertical scaling adds resources to one machine; the example moves from **16 GB to 64 GB RAM**. It is simple but bounded by hardware and retains a single failure domain.
- Horizontal scaling adds nodes and therefore requires load balancing, state coordination, synchronization, and broader monitoring.
- "Diagonal" scaling means scaling one node up to a threshold and then adding nodes.
- Caching can occur in clients, applications, database-query layers, and CDNs.
- Sharding partitions a dataset across physical database nodes; event-driven processing removes slow work from synchronous request paths.
- Performance and scalability differ: the example is a service that performs well for **100 users** and fails at **10,000**.
- Scaling introduces consistency, replication, failure coordination, network-hop, propagation, infrastructure-cost, and operational-cost tradeoffs.
- Microservices permit independent scaling but exchange deployment coupling for network, consistency, and observability complexity.

## Why it matters

The source supplies general distributed-systems vocabulary that underlies ML serving too. Its strongest sentence is negative: not every component needs equal scale. Capacity should follow measured bottlenecks rather than architectural fashion.

## Tensions / open questions

- "Virtually unlimited" horizontal scale is an overstatement.
- Categorical claims about load balancing, sharding, CDNs, and microservices are workload-dependent.
- No capacity model, real architecture, cost curve, or benchmark supports the "millions" framing.
- The source is introductory and does not resolve consistency or hotspot mechanics.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[ML Systems at Scale]]
- [[Software Performance Engineering]]

## Citations

- Sumit K, "Scaling Simplified: How Distributed Systems Handle Millions", 2025-01-05.

## Raw capture

- [[2026-09-13 Sumit K - Scaling Simplified]]

## Related pages

- [[LLM Application Resilience]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Serving Engines]]
