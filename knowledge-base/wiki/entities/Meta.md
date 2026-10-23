---
type: entity
created: 2026-09-04
updated: 2026-10-23
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
  - src-2026-10-19-rath-thin-orchestrator
status: active
---

# Meta

## What it is

Technology company operating at very large scale, publisher of the Llama open-weight model family, and — in the
vault's directly ingested Meta sources — an operator of internal domain-expert and data-onboarding agents.

## Why it matters here

Meta enters this vault not through a model release but through **internal deployment reports**:
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
- Meta appears elsewhere in this vault through Llama in the open-weight model discussions, and — since the
  October 2026 ingest — through a second first-party engineering report, the thin orchestrator described below.

## Serving its agent at consumer scale would be an inference bill, not a sandbox bill

Meta enters this vault a second time through an outside analysis of its **Muse** agent, and the
provenance shift is the first thing to record: [[FD - Agent Muse Compute Demand]] is a **bottom-up
scenario estimate built on assumptions**, not a measurement of Meta's infrastructure. Its **100M DAU**
premise is hypothetical and the post does not establish Meta's actual deployment scale. What the post
cites as *observed* is narrow, and is a **third-party write-up of the VM configuration, not a Meta
specification** - **2 vCPUs, ~8 GB of RAM, and ~100 GB of persistent logical storage** per user, with
**one** observed instance using about **~3 GB**.

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

## A second first-party report: complexity in files, control flow in code

[[Plawan Rath et al - The Thin Orchestrator]] is Meta Engineering's account of rebuilding a
data-onboarding agent after a single agent holding all the domain knowledge — schemas, code-generation
rules, routing logic, validation requirements, patterns for **more than 10 data sources** — worked in
demos and hallucinated in production. The replacement is a **roughly 1,300-line** router coordinating
**20+ workflows** across **14 specialist agents**, which performs no domain work itself, and
**25+ domain knowledge files** of typically a few thousand tokens each, loaded at runtime by the
specialists rather than embedded in the router.

Read beside [[Meta - An Organizational Second Brain]], the two first-party Meta reports converge on one
house position from different problems. The second brain keeps complexity in **200+ text files a
domain expert can review in 30 seconds**, declining to fine-tune. The thin orchestrator keeps domain
knowledge in files loaded at runtime and keeps sequencing, input gathering, reliability checks, and
error handling in ordinary deterministic code — **"Deterministic decisions stay deterministic."** In
both, the thing an engineer edits to change behaviour is a reviewable file, and in both the model is
deliberately given less to hold. The onboarding system's own numbers: a single-agent alternative at
**70-80%** success **with manual prompt engineering per task** and **10-20%** without; process
duration across successive versions moving from **three to four days** manual to **about a day** on an
earlier config-driven system to **under an hour**; and **"about two-thirds"** of changes landing
without significant human edits.

**The evidentiary weakness is also shared, and it is the same weakness.** Both are company
self-reports from a team describing its own system. Neither runs a controlled comparison, both omit
denominators — the second brain's "zero regressions" and the orchestrator's "two-thirds" are equally
undefined — and the orchestrator reports **no ablation** separating deterministic routing, context
isolation, workflow templates, and runtime knowledge loading, so its central attribution (reliability
came from the router reasoning less) is an argument rather than a measurement. Its recommendations and
its expectation that scaling means adding templates and knowledge files are **proposals**, and its
continuous-improvement loop is **future work gated by human review**. The third-party result the
article cites in support — orchestrated multiagent systems at **65.3%** accuracy versus **16.6%** for
single agents on **80-task batches** — concerns a different workload and does not test Meta's system.

What this adds to the entity's profile is a pattern worth tracking rather than a validated claim:
across two unrelated internal agent deployments, Meta's published answer to unreliability has been to
**remove material from the model and put it in versioned, human-legible artifacts**, then make the
surrounding control flow deterministic.

## Open questions

- Both first-party Meta reports argue for text-and-code over model capability, and neither ablates the
  claim. Is this a tested engineering position or a house style the published write-ups reflect?
- The second brain's text files are compiled from **expert feedback under human review**; the
  orchestrator's knowledge files are loaded at runtime with no stated review, versioning, or regression
  process. Does the governance travel with the pattern, or only with the knowledge-management use case?
- Nothing connects Meta's internal agent architectures to the consumer-scale Muse deployment the
  third-party estimate prices. Whether the thin-orchestrator shape is used anywhere near that scale is
  unknown.

## Related pages

- [[Plawan Rath et al - The Thin Orchestrator]]
- [[Agent Frameworks]]
- [[Agent Delegation]]
- [[Model Routing]]
- [[Context Engineering]]
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
