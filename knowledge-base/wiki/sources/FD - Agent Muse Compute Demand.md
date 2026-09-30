---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-27-fd-agent-muse-compute-demand
source_title: "Agent (Muse) Compute Demand"
source_author: FD
source_url: https://robonomics.substack.com/p/agent-muse-compute-demand
tags: [source/summary, ai-agents, cost, inference, hardware]
source_ids: [src-2026-09-27-fd-agent-muse-compute-demand]
status: active
---

# FD - Agent Muse Compute Demand

## Summary

FD builds a bottom-up scenario estimate of the infrastructure needed to serve a hypothetical 100
million daily active users of Meta's Muse agent. The analysis separates *logical* per-user VM
allocation from *physical* resource demand by applying activity rates, peak-to-average ratios,
capacity headroom, CPU oversubscription, and observed memory residency. It concludes at roughly 1-2 GW
of average total power, of which the entire VM sandbox layer is only about 0.1 GW. The dominant term
is inference, because each user drives many reasoning-equivalent model calls.

## Key claims

- Observed Muse sandbox allocation per user: **2 vCPUs, ~8 GB of RAM, ~100 GB of persistent logical
  storage**. The author treats these as advertised logical allocations, not physical reservations.
- Concurrency chain: **100M DAU** x **two active hours per day** / 24 = **~8M average simultaneous
  active VMs**; a **2.5x peak-to-average ratio** gives **~20M peak**; **~20% headroom** gives
  **~25M provisioned live VMs**, or roughly **25% of DAU live simultaneously**.
- The oversubscription ratio is anchored on DeepSeek's DSec paper: **~30,000 physical CPU cores**,
  **250 TB of DRAM**, **~160 nodes**, peak concurrency above **380,000 sandboxes**, stable at about
  **800 microVMs per node** on roughly **188 physical cores per node** - about **0.23 physical cores
  per live VM**.
- Muse is assumed less efficient: sensitivity range **0.3-0.75 physical cores per live VM**, base case
  **0.5** (two live VMs per physical core). At 25M live VMs that is **12.5M physical CPU cores**, or
  **~50K CPUs** at 256 cores each (**~65K** at 192 cores), estimated at **~$800M** at current public
  prices.
- Memory: the environment exposes **~8 GB** but one observed instance used about **~3 GB**; at
  25M x 3 GB that is **75 PB**, with a base range of **~75-100 PB physical DRAM**, estimated at **~$2B**.
- The entire sandbox/VM layer is estimated at **~0.1 GW** at 100M DAU.
- Inference dominates: a Microsoft study's median is **~0.31 Wh per normal query**; a long reasoning
  query with roughly **15x the token count** uses about **13x the energy**, or around **4 Wh**, with a
  Muse-like range of **5-10 Wh per heavy reasoning-equivalent event**. At **50 reasoning-equivalent
  events per DAU per day** and 5 Wh each: **25 GWh/day**, or **~1.0 GW average power**.
- Base case total: **~1-2 GW average power**, with **3-4 GW** called entirely plausible under higher
  reasoning-call demand.

## Why it matters

The vault has plenty of per-token efficiency evidence and little that connects it to fleet-level
demand. This source supplies the missing chain of ratios, and its central finding is structural: the
sandbox that makes an agent *feel* expensive is roughly a tenth of the bill, while the model calls
behind it carry the rest. It also names the scaling asymmetry that matters for agent economics -
demand tracks reasoning-equivalent events per user, not user count, so an agent that deliberates more
per task raises compute demand without acquiring a single new user.

## Tensions and caveats

Nearly every major input is assumed rather than measured: active hours, peak ratio, headroom, CPU
oversubscription, memory residency, events per user, energy per event, and hardware prices. The
**~3 GB** memory observation comes from a single instance and cannot establish fleet working-set
behavior. DeepSeek's DSec is used as an efficiency reference even though Muse's sandbox workload and
implementation may differ materially. The **~$800M** and **~$2B** figures omit networking, storage,
orchestration, redundancy, facilities, cooling, depreciation, and operations. The **100M DAU**
scenario is hypothetical and the post does not establish Meta's actual deployment scale; the **3-4 GW**
number is a sensitivity conclusion, not a forecast.

## Raw capture

- [[2026-09-27 FD - Agent Muse Compute Demand]]

## Affected pages

- [[Multi-Tenant Agent Architecture]]
- [[Tool Roster Economics]]
- [[AI Agents in Production]]
- [[Inference Efficiency Frontier]]
- [[Meta]]
- [[DeepSeek]]

## Related pages

- [[Agentic Loop]]
- [[LLM Inference]]
- [[Serving Benchmarks and Goodput]]
- [[Test-Time Scaling]]
