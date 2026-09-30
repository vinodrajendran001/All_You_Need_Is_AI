---
type: entity
created: 2026-09-04
updated: 2026-09-30
entity_kind: organization
tags:
  - entity
  - organization
  - ai-lab
  - ai-agents
  - knowledge-management
  - cost
  - inference
source_ids:
  - src-2026-09-02-meta-organizational-second-brain
  - src-2026-09-27-fd-agent-muse-compute-demand
status: active
---

# Meta

## What it is

Technology company operating at very large scale, publisher of the Llama open-weight model family, and — in this
vault's only directly ingested Meta source — an operator of internal domain-expert agents.

## Why it matters here

Meta enters this vault not through a model release but through an **internal deployment report**:
[[Meta - An Organizational Second Brain]] describes a compliance-domain expert agent built on 200+ structured
knowledge files, improved by compiling expert feedback into text under regression tests rather than by retraining.
It anchors [[Institutional Knowledge Agents]].

The reason it matters more than a typical engineering-blog post is the position it stakes out: **"Keep the
complexity in text files, not in model weights or opaque embeddings. Every improvement is a text edit a domain
expert can review in 30 seconds."** That is an argument about governance as much as capability, and it comes from
an organisation with the resources to fine-tune instead.

It also gives this vault a mirror. The described architecture — declared frontmatter dependencies, deterministic
routing indexes, an append-only improvement record, a deterministic linter — converges independently on the shape
described in [[Schema-Driven Knowledge Base]], [[Persistent Wiki]], [[Index and Log]], and
[[Ingest Query Lint Loop]]. The divergences are the useful part: Meta's loop adds blind regression replay and an
**independent adversarial reviewer** that sees only diffs and not the rationale.

## Notes

- The source positions itself as a production instance of ideas already circulating, explicitly citing
  **Karpathy's LLM Wiki** proposal (see [[Andrej Karpathy]]) and **Google's Open Knowledge Format** as prior art.
- Reported results after three two-week sprints — "useful almost all the time," days reduced to minutes, "zero
  regressions" — are **entirely qualitative, with no denominators, baselines, or task counts.** Read as a design
  report, not as evidence of effectiveness.
- The one quantitative figure, roughly **80% fewer tokens per turn** from progressive disclosure, is unattributed
  across several simultaneous changes.
- Meta appears elsewhere in this vault only indirectly, through Llama in the open-weight model discussions.

## Serving its agent at consumer scale would be an inference bill, not a sandbox bill

Meta enters this vault a second time through an outside analysis of its **Muse** agent, and the
provenance shift is the first thing to record: [[FD - Agent Muse Compute Demand]] is a **bottom-up
scenario estimate built on assumptions**, not a measurement of Meta's infrastructure. Its **100M DAU**
premise is hypothetical and the post does not establish Meta's actual deployment scale. What it treats
as *observed* is narrow - the sandbox exposes **2 vCPUs, ~8 GB of RAM, and ~100 GB of persistent
logical storage** per user, and **one** observed instance used about **~3 GB**.

Everything else is a chain of ratios. 100M DAU x **two active hours per day** / 24 = **~8M average
simultaneous VMs**, x **2.5** peak-to-average = **~20M peak**, plus **~20% headroom** = **~25M
provisioned live VMs**. With an assumed **0.5 physical cores per live VM** - deliberately worse than
the **~0.23** implied by DeepSeek's DSec paper - that is **12.5M physical cores** (**~50K CPUs** at
256 cores each, **~$800M**), and the **~3 GB** residency figure extrapolates to **75 PB** of DRAM
(**~75-100 PB**, **~$2B**), both excluding networking, storage, orchestration, redundancy, facilities,
cooling, depreciation, and operations. The conclusion that matters is a ratio, not a total: the entire
sandbox/VM layer is estimated at **~0.1 GW** against **~1-2 GW** of total average power, because
inference dominates at **50 reasoning-equivalent events per DAU per day** x **5 Wh** = **25 GWh/day**,
or **~1.0 GW**. The frequently quoted **3-4 GW** is a sensitivity conclusion under higher reasoning
demand, not a forecast.

The two Meta entries in this vault sit in productive tension. [[Meta - An Organizational Second Brain]]
is first-party and qualitative: a design report arguing that an agent's complexity belongs in text a
domain expert can review in 30 seconds, with no denominators behind its results. The Muse estimate is
third-party and quantitative but entirely modelled: it has no access to Meta's fleet and prices a
deployment scale it cannot confirm. Neither checks the other, and they describe different Meta agents.
What they share is a direction of travel - both locate the expensive part of an agent in how much it
deliberates and how much text it must read to do so, rather than in the model weights or the
environment around them.

## Related pages

- [[Meta - An Organizational Second Brain]]
- [[Institutional Knowledge Agents]]
- [[Schema-Driven Knowledge Base]]
- [[Persistent Wiki]]
- [[Retrieval-Augmented Generation]]
- [[Agent Memory]]
- [[Continual Learning for Agents]]
- [[LLM-as-a-Judge]]
- [[Andrej Karpathy]]
- [[AI Knowledge Base Overview]]
- [[FD - Agent Muse Compute Demand]]
- [[Multi-Tenant Agent Architecture]]
- [[Tool Roster Economics]]
- [[AI Agents in Production]]
- [[Inference Efficiency Frontier]]
- [[DeepSeek]]
