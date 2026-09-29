---
title: "Agent (Muse) Compute Demand"
source: "https://robonomics.substack.com/p/agent-muse-compute-demand?utm_source=tldrai"
author:
  - "[[FD]]"
published: 2026-09-27
created: 2026-09-29
description: "An attempt to estimate the infrastructure required to serve 100M DAU"
tags:
  - "clippings"
---
There are obviously a lot of moving assumptions: how long agents stay active, how aggressively CPUs and memory can be oversubscribed, how many model calls an agent generates, and how efficiently those models are served.

Rough conclusion is:

- **~1–2 GW of average total power** to serve 100M DAU in the base case, of which only **~0.1 GW comes from the CPU/VM layer**. Depending on the # of reasoning-equivalent model calls one Muse DAU generates per day, **3-4GW** is entirely plausible.
- The sandbox layer = **sub $1B** **of CPU content** and **~$2B of DRAM content, which is smaller than many expected.**

Welcome all feedbacks/ pushbacks.

---

Two very different pieces of infrastructure behind Muse.

1\. Muse VM / sandbox infrastructure

**2 vCPUs, ~8 GB of RAM and ~100 GB of persistent logical storage per user**. [Observed Muse VM configuration](https://www.starkinsider.com/2026/09/meta-muse-specs-what-it-runs-on.html)

2\. Muse Spark inference

Model inference goes out through Meta's external inference infrastructure. [Meta’s description of Muse architecture](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

---

## 1/ Sandbox infrastructure

## A. CPU

The first mistake is assuming that **100M DAU means 100M VMs are actively consuming compute at the same time**.

Suppose the average Muse DAU has an agent actively working for two hours per day.

100M users \* 2 hours / 24 hours = ~8M average simultaneous active VMs

Meta obviously cannot provision only for the daily average. Usage will be concentrated during waking hours and bursty.

Assume a 2.5x peak-to-average ratio:

8M \* 2.5 = ~20M peak active VMs

Then add roughly 20% capacity headroom: **~25M provisioned live VMs.** So the base assumption is effectively that Meta needs enough infrastructure to support roughly **25% of DAU being live simultaneously**.

![](https://substackcdn.com/image/fetch/$s_!Rk_q!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F958cc7c7-8b76-4da9-80d1-7052b0deb327_1672x456.png)

The next important distinction is between **virtual CPU allocation** and **physical CPU demand**. Agent sandboxes are particularly well suited to CPU oversubscription. They spend a lot of time waiting. During those periods, the VM may still be alive, but it is barely using CPU.

DeepSeek’s recently published DSec infrastructure provides a useful benchmark. Its production agent sandbox platform runs approximately **30,000 physical CPU cores and 250TB of DRAM across ~160 nodes**, with peak concurrency above **380,000 sandboxes**. [DeepSeek DSec paper](https://arxiv.org/abs/2609.22978). DSec also demonstrates stable operation at around: **800 microVMs per node.** With roughly 188 physical cores per node: 188 physical cores / 800 microVMs = ~0.23 physical cores per live VM.

DeepSeek is obviously the King of efficiency. The number for Muse might be at 0.3-0.75 physical cores per live VM, or assume **0.5 physical cores per live VM as the base case.** That is equivalent to roughly **two simultaneously live Muse VMs per physical CPU core**.

Using the base assumptions: **25M live VMs \* 0.5 physical cores per VM = 12.5M physical CPU cores.**

On a 256-core CPU: 12.5M cores / 256 cores per CPU = ~50K CPUs; Or on a 192-core CPU that would be 65K CPUs.

**At the current public pricing, that is ~$800M.**

![](https://substackcdn.com/image/fetch/$s_!h3Sq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F707b35ef-5681-4371-9c6e-fa61b918df5a_1684x676.png)

## B. DRAM

CPU can be aggressively oversubscribed because a VM that is waiting may consume almost no CPU. Memory is harder to oversubscribe because a live VM still needs to retain its working state.

Muse exposes roughly **8GB of RAM** to the user environment, but one observed instance was actually using only around **3GB** at the time of measurement.

25M live VMs \* 3GB = 75PB of physical DRAM, call it ~75-100PB of physical DRAM feels like a reasonable base range.

**At the current public pricing, that is ~$2B.**

## C. Sandbox power

**~0.1 GW for the entire Muse sandbox / VM layer at 100M DAU.**

---

## 2/ Inference

Muse’s personal computer executes tools and stores state locally, but the actual model runs on separate inference infrastructure. [Meta’s Muse architecture](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)

## Energy per inference event

Microsoft’s 2026 study estimates that optimized frontier-scale inference consumes a median of approximately: **0.31Wh per normal query**

But a long reasoning query with roughly 15x the token count consumes approximately 13x as much energy, or around: **4Wh per long reasoning query**

The study specifically highlights reasoning and agentic workloads as significantly more energy intensive. [Microsoft Research on AI inference energy](https://www.microsoft.com/en-us/research/publication/energy-use-of-ai-inference-efficiency-pathways-and-test-time-scaling/?utm_source=chatgpt.com)

For a Muse-like workload, let’s assume **5-10Wh per heavy reasoning-equivalent inference event** as a rough sensitivity range.

## Sensitivity analysis on # reasoning-equivalent events per DAU per day

Assume 50 reasoning-equivalent events per DAU per day

Suppose each active Muse user generates the equivalent of 50 heavy inference events per day.

At 5Wh each:

100M users \* 50 events/day \* 5Wh = 25GWh/day

25GWh/day / 24 hours = ~1.0GW average power

So inference alone could require: **~1-2GW of average power**

![](https://substackcdn.com/image/fetch/$s_!QYgl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3883608c-7bda-4731-800d-bf10da4d2d75_1696x558.png)

So a **3-4GW Muse** is entirely plausible. Maybe that’s why Meta is rumored to be adding 7-10GW of compute next year.

---

## Bottom line

The popular framing around Muse is that giving every user **2 vCPUs and 8GB of RAM** creates an enormous CPU requirement. But the naive calculation materially exaggerates the CPU requirement because it treats logical VM allocation as dedicated physical infrastructure.

The more interesting conclusion is: **Consumer agents may be a meaningful new demand driver for CPUs and conventional DRAM, but inference remains the real compute bottleneck.** And as agents do more work, run longer trajectories and increasingly spawn other agents, **inference demand can scale much faster than the number of users itself.**