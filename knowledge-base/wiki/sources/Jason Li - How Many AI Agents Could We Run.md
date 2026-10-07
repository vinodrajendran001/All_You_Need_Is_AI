---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-10-02-epoch-agent-population
source_title: "How many AI agents could we run?"
source_author: Jason Li
source_url: https://epoch.ai/publications/estimating-the-agent-population
tags: [source/summary, inference, ai-agents, hardware, cost]
source_ids: [src-2026-10-02-epoch-agent-population]
status: active
---

# Jason Li - How Many AI Agents Could We Run

## Summary

Epoch AI estimates how many concurrent agent sessions hardware associated with 2025-2027 HBM
shipments could eventually support. It combines a hardware-supply model, assumed closed-model
economics, public open-model serving measurements, and agent-session traces. These are conditional
capacity scenarios, not forecasts of deployment, demand, provider margins, or economically equivalent
human workers.

## Key claims

The closed-model headline assumes **$30 per active agent-hour**, **$5 per GB300 GPU-hour**, an
API-revenue/reference-serving-cost ratio of **5-10x**, and **1-4x** throughput uplift per GB for
HBM4/4E relative to HBM3E. Hardware is eventually deployed and fully allocated in the capacity
calculation; shipment year is not deployment year.

| Hardware shipment horizon | Central 2x uplift | Wider uplift/economics range |
| --- | --- | --- |
| Through 2026 | 20-40 million concurrent sessions | 16-56 million |
| Through 2027 | 50-101 million concurrent sessions | 33-171 million |

The through-2027 table gives **50.3-100.6 million** centrally and **32.8-170.7 million** in the
wide range. These are nested shipment horizons, not additive annual populations.

- The memory normalization is **288 GB per GB300 GPU**, not per superchip. Annual HBM supply is
  modeled at **2.21, 3.75, and 5.81 billion GB** for 2025, 2026, and 2027, with assumed generation
  shares. The central effective totals are **24.03 million GB300 equivalents through 2026** and
  **60.36 million through 2027**.
- For DeepSeek V4 Pro, the selected AgentX measurements/interpolation give **31.4 sessions per GPU
  at a P90 50-output-token/s/user target**, versus **14.4 at 100**. Applied to the same central
  through-2027 hardware, the 50-TPS case supports about **1.9 billion sessions**. It is an
  alternative allocation, not additional simultaneous capacity or equivalent frontier capability.
- A streaming-speed target excludes first-token and end-to-end delay. Selected Kimi K3 GB300
  deployments have P90 first-token delays of **39.8, 12.4, and 4.6 seconds** at 50/100/200-TPS
  targets. Different deployments are being selected; this is not an isolated causal effect of TPS.
- AgentX treats a root and its subagents as one tree. TraceLab accounting may not include the whole
  tree. The adjusted agent-hour excludes identified human waits, caps other gaps at five minutes,
  and retains tool waits; it is not simply elapsed session time.
- TraceLab uses **3,390 session/model groups from 3,382 sessions**, not unique users. Under frozen
  prices and a retained-cache scenario, full-model pooled rates are **$18.19 GPT-5.5**, **$15.50
  GPT-5.6 Sol**, **$24.34 Opus 4.8**, and **$50.16 Fable 5** per adjusted agent-hour. These are
  reconstructed rates, not actual invoices, and high-context subsets overlap their full rows.
- At **20% effective use**, defined as **40% allocation x 50% utilization**, the modeled
  through-2027 capacity implies **$2.6-5.3 trillion/year in API-equivalent spending**. This is not
  provider break-even revenue or a prediction of realized sales.

## Why it matters

The unit "agent" conceals a service-level target, tree boundary, activity denominator, model
capability, and utilization assumption. Those definitions can change capacity more than the hardware
headline. This complements [[FD - Agent Muse Compute Demand]]: one works backward from supply,
the other forward from assumed consumer activity, in units that cannot be directly added.

## Tensions / open questions

Future HBM shares, deployment lag, generation uplifts, prices, margins, and workload mix are
uncertain. The roughly $1 trillion end-2027 annualized-revenue illustration is an extrapolation,
not a calendar-year forecast. Likewise, **168/40 = 4.2** compares available hours, not quality,
productivity, or displaced jobs. Some equations lost variable names in the clipping; the preserved
tables and prose support the stated assumptions, but the capture is not a complete equation source.

## Affected pages

- [[Epoch AI]]
- [[Serving Benchmarks and Goodput]]
- [[AI Accelerator Architecture]]
- [[Inference Efficiency Frontier]]
- [[AI Agents in Production]]
- [[ML Systems at Scale]]

## Raw capture

- [[How many AI agents could we run]]

## Citations

- Canonical URL: <https://epoch.ai/publications/estimating-the-agent-population>
- Published October 2 and captured October 6, 2026.

## Related pages

- [[FD - Agent Muse Compute Demand]]
- [[Jason Li - Latency Scaling Differences for GPT and Claude Models]]
- [[Reasoning Effort Control]]
- [[Agent Delegation]]
