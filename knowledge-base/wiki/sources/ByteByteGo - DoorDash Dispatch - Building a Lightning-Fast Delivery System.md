---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-24-bytebytego-doordash-dispatch
source_title: "DoorDash Dispatch: Building a Lightning-Fast Delivery System"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/doordash-dispatch-building-a-lightning
tags:
  - source/summary
  - system-design
  - distributed-systems
  - optimization
  - ml-serving
source_ids:
  - src-2026-11-24-bytebytego-doordash-dispatch
status: active
---

# DoorDash Dispatch: Building a Lightning-Fast Delivery System

## Summary

A ByteByteGo relay of one DoorDash engineering post about rebuilding the dispatch engine that
assigns orders to Dashers, DoorDash's delivery drivers. The article likens dispatch to the
vehicle-routing problem over space and time, with inputs that keep changing, so a good assignment is
useless if it arrives late. The old monolith combined state, business rules and routing
calculations, and its key algorithms had roughly quadratic complexity. Under peak demand it had to
cut its search or fall back to simpler rules. Adding servers alone would not fix this, because
nearby orders are coupled and a central coordinator can become the new bottleneck if it is
overloaded. The redesign separates a coordinator tier from a stateless compute tier, sends workers
only local, self-contained payloads, and decomposes the problem geographically, with a global
reconciliation layer for boundary effects. Rollout went through shadow testing, then production
switchback experiments. DoorDash reports **10×** processing scale, **>99.96%** of runs under **20
seconds** and **>99.99%** availability during Super Bowl spikes. None of these comes with a
quantified baseline (the latency figure is compared only with "minutes under heavy load" in the old
system) or a decision-quality metric.

## Key claims

### Why the old engine hit a wall

- Dispatch must weigh more than distance. A Dasher two minutes away is a poor choice if the food needs
  another 15 minutes, and two orders heading the same way could be batched into one trip. New orders
  arrive, Dashers move and prep estimates change "even as the system is calculating".
- The monolith ran candidate generation, route checks and optimization in sequence. Its important
  algorithms "had roughly quadratic complexity", so doubling the input could mean about four times the
  work.
- During peaks, demand could reach "nearly four times the system's dispatch processing capacity". The
  engine then had to limit what it considered or fall back to simpler rules, and its delays degraded
  the decisions themselves: a Dasher might move away from a pickup, or ready food might wait.

### Why more servers alone fail

Horizontal scaling works for independent requests. Dispatch assignments are not independent: two
orders that could share a trip may land on separate workers, and two workers may pick the same
Dasher. Something must also prepare the work, send data, gather results and combine them. If that
component overloads, the bottleneck has only moved. DoorDash therefore had two problems: an
architecture that distributes computation, and a way to divide the optimization problem while keeping
the useful relationships between orders, routes and Dashers.

### The redesign

- **Two independently scalable tiers.** A coordinator tier maintains logistics state, applies business
  rules and organizes the work. A compute tier of workers generates and evaluates routing
  possibilities, runs optimization and executes ML models.
- **Localized payload sharding.** Rather than sending every worker the whole logistics state, the
  coordinator sends each one the local context it needs, over gRPC, on each dispatch tick. Payloads are
  self-contained, so workers stay stateless; the coordinator keeps responsibility for changing state.
- **Hierarchical decomposition.** Rapid pre-clustering creates initial groups, and centroid-based
  refinement adjusts them into localized geographic clusters and delivery trajectories. Each partition
  is a unit of work for one compute node.
- **Global reconciliation and scoring.** Partition boundaries are artificial, and orders near them may
  still be related, so a reconciliation layer combines results across partitions before final
  assignment. The article says this "preserves much of the optimization quality of the original
  problem", without a measurement.

### Rollout

Shadow testing duplicated production work to the new engine, which recorded what it would have done
while the old engine kept control. The team compared proposed matches, delivery-time behaviour and
resilience, which the article calls behavioural regression analysis. Because shadow decisions are
never executed, the team then ran **production switchback experiments**, in which the systems take
turns controlling real activity, with limited exposure and fallback, before expanding the rollout.

### Reported results

- "Ten times the dispatch processing scale, enabled by distributing computation."
- "More than **99.96%** of runs completed in under **20 seconds**", against execution "stretching to
  minutes under heavy load" in the old system.
- "More than **99.99%** availability during Super Bowl traffic spikes, despite a **10%**
  week-over-week increase in peak volume."
- DoorDash connects the broader search to improved Dasher acceptance rates, fulfillment efficiency and
  Dasher earnings, and reports "millions of dollars in annualized fulfillment savings". None of these
  is quantified further.

### ML inside dispatch

The extra capacity made heavier ML practical. **L1** serves models locally inside compute workers with
ONNX Runtime, avoiding a network round trip for frequent evaluations. **L2** serves heavier, less
frequent policy evaluations from isolated remote clusters, away from the coordinator's state
management. The platform also enabled a multi-agent reinforcement-learning system that adapts the
optimizer's objective weights, for example between delivery speed and batching efficiency. No design
or result is given for it.

## Why it matters

[[ML Systems at Scale]] states a rule from LLM routing: scaling patterns are nouns, and workload
signals choose the policy. Here the same rule holds with a different scarce resource. The coupling is
between nearby orders and Dashers, not cached prefixes, and the fix is to partition by geography and
reconcile at the boundaries. The L1/L2 split also restates that page's theme of keeping heavy work off
the synchronous path. For [[DoorDash]] it adds a non-LLM optimization system to the vault's
evaluation, search and tool-gateway accounts. For [[ByteByteGo]] it is another relay of one named
company's post, with a staged rollout but no reported comparison.

## Tensions / open questions

- **Secondhand and single-source.** The article carries ByteByteGo's disclaimer that it "is based on
  publicly shared details", and its one reference, DoorDash's engineering post, is not in the vault.
  Every figure is DoorDash's description of its own system.
- **No baselines or quality metrics.** "Ten times" is not tied to a stated old capacity. The
  decomposition's quality cost is described but not measured. The shadow and switchback results that
  justified the rollout are not reported.
- **Unquantified benefits.** Acceptance rates, efficiency, earnings and "millions of dollars" carry no
  numbers. The RL system is a single paragraph with no method or outcome.
- The latency figure is for dispatch runs, not end-to-end delivery times, and 20 seconds is a run-time
  bound, not a decision-quality bound.
- The capture opens with a sponsored CI-tooling block (WarpBuild), which is not part of the article and
  is excluded here.

## Affected pages

- [[ML Systems at Scale]]
- [[DoorDash]]
- [[ByteByteGo]]

## Raw capture

- [[knowledge-base/raw/sources/DoorDash Dispatch Building a Lightning-Fast Delivery System]]

## Citations

- Canonical URL: <https://blog.bytebytego.com/p/doordash-dispatch-building-a-lightning> (email
  tracking parameters removed).
- Byline ByteByteGo; published and captured 2026-11-24.
- Its only reference is DoorDash's engineering post "How DoorDash built a next-generation real-time
  dispatch platform", which this vault has not captured.

## Related pages

- [[ML Systems at Scale]]
- [[DoorDash]]
- [[ByteByteGo]]
- [[Reinforcement Learning]]
- [[ByteByteGo - How DoorDash Built a Toolbox for AI Agents]]
- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[DoorDash - LLM-as-a-Judge for Search Evaluation]]
- [[Vinod - KV-Cache-Aware LLM Routing on Kubernetes]]
