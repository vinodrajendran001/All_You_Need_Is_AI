---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-19-naam-million-agents-superintelligence
source_title: Can a Million AI Agents Create Superintelligence
source_author: Ramez Naam
source_url: https://www.rameznaam.com/p/can-a-million-ai-agents-create-superintelligence
tags:
  - source/summary
  - multi-agent
  - scaling
  - recursive-self-improvement
source_ids:
  - src-2026-10-19-naam-million-agents-superintelligence
status: active
---

# Ramez Naam - Can a Million AI Agents Create Superintelligence

## Summary

A survey-and-synthesis essay arguing that adding agents buys **speed** far more than it buys
**collective intelligence** — the ability to solve harder problems or reach a new skill level. Naam
assembles roughly a dozen multi-agent scaling results and finds them consistently logarithmic or
**sub-logarithmic**, then argues that runaway recursive self-improvement requires conceptual
breakthroughs rather than more parallel copies of current models.

The essay's own summary of its epistemic position: **"We're all operating on far too little real world
data."**

## Key claims

### The distinction the essay rests on

- **"More agents are useful for speed: they can solve many problems faster. They're less useful for
  boosting AI intelligence."**
- Three mechanisms are offered for why: **coordination** cost, **homogeneity** producing shared blind
  spots, and the **sequential structure** of hard problems — *"A million independent searches can run at
  once. A sequential investigation can't."* and *"A thousand copies don't automatically supply the
  insight one copy is missing."*
- Scaling shapes are classified as linear, power-law diminishing, logarithmic, and sub-logarithmic.
  **[Illustrative]** at power-law exponent **0.5** doubling output needs **4x** input; at **0.2**,
  **32x**; at **0.1**, **1,024x**.

### Evidence assembled — nearly all third-party

- OpenAI reportedly used **124x as many tokens per researcher** but ran only **1.6x as many experiments
  per researcher**; Naam's earlier work put the measured software feedback loop **five to ten times
  below** self-sustaining strength.
- **Toby Ord's analyses:** on Terminal-Bench four agents were **~1.9x faster** at **~2.1x** token cost;
  on BrowseComp **~2.6x faster** at **~1.6x** cost. With five agents, Opus 5.5 reached **~2.7x** solo
  speed versus **~2.2x** for Opus 5, using total agent runtime as a cost proxy.
- **Lean formal math:** the local speed exponent **λ** fell from about **0.75 to 0.33** as teams went
  from 10→30 and then 30→100 agents.
- **SEC-Bench Pro:** peak scores about **71.2** (1 agent), **74.3** (4), **76.4** (16) — a total gain of
  **~5.2 points**, split **3.1** then **2.1** across the two fourfold increases.
- **Anthropic Opus 5.5 formal math:** 49 weighted theorem statements, 24 hours per team. Going from ten
  to one hundred agents added **27 score points**; going further added only **two**. The hundred-agent
  team self-organized a hierarchy with **12 sub-leads** and could spend **10x** the aggregate runtime.
- **Navier-Stokes:** OpenAI ran approximately **10,000 agents** concurrently over an **88-hour run**.
  Noam Brown said he would attribute **"not even 10%"** of the result to multi-agent scaling.
- **Diversity study:** substantial gains up to **8 agents**, then average performance barely moved.
- **Molecular exploration:** scaling from **1 to 128 agents** showed logarithmic diminishing returns.

### The extrapolation and the proposed test

- Modelling assumptions he is arguing against: Chan et al. (2026) assume doubling effective research
  labor raises the software-improvement rate **~2.6x**; Eth and Davidson use a doubling-for-doubling
  paper model; Davidson and Houlden use a parallel-research exponent of **0.6** (10x labor → ~4x pace),
  dropping to **0.3** when experimental compute is the bottleneck.
- Anthropic's employment report showed research agents logging about **9 agent-hours per human
  work-hour by mid-July**, **19** by late August, and a company-wide ratio near **6**. Assuming equal
  value per hour, that is **~10x** human-only labor in July and **~20x** in August, or **5x** and
  **10x** total labor growth relative to April.
- Those same inputs give wildly different predictions: Davidson-Houlden implies **~2-4x** April's
  research pace by August, Chan's exponent **~25x**, plain logarithmic scaling **~2x**, and the
  observed sub-logarithmic shapes only **~1.1-1.8x**. The spread is the argument.
- **[Proposal]** Measure three quantities on real AI research — **G** (verified task-performance gain
  per multiplication of agents), **λ** (speed-cost scaling), and **N** (the team size where gains
  saturate) — reported separately for **1→10, 10→100, and 100→1,000 agents**.
- **[Forecast]** Allowing a **six-month** research-to-publication lag, Naam expects no sustained
  acceleration in the Epoch Capabilities Index through the first half of 2027, with signals from the
  late-May agent-hour ratio arriving around November.

## Why it matters

[[Recursive Self-Improvement]] and [[Automated AI Research]] in this vault contain both takeoff
arguments and scattered multi-agent results. This source is the first to put the two together and make
the **scaling exponent itself** the crux: fast-takeoff models assume parallel research scales near
linearly, and the measured curves do not.

The speed-versus-capability split is also directly useful to [[Agent Delegation]] and
[[Test-Time Scaling]]. It predicts that parallel agents should help most where work decomposes and help
least where the bottleneck is a missing idea — which matches the Lean and SEC-Bench curves, where
early multiplications paid and later ones did not.

The proposed G/λ/N protocol is the most actionable part: it specifies **reporting gains per
multiplication rather than per total**, which is exactly what makes diminishing returns visible.

## Tensions / open questions

- The author calls his own data **"scant"** and repeatedly says real-world data should recalibrate the
  conclusion.
- **No measurement here approaches a million agents.** The largest cited team is roughly 10,000, and
  million- and billion-agent conclusions are extrapolations.
- The SEC-Bench figures compare **best reported scores across different budgets**, not equal-compute
  experiments. Runtime is only a cost proxy. The Navier-Stokes result **lacked a single-agent control**.
- Benchmark scores are a task-specific proxy, not a measure of intelligence; the essay does not show
  benchmark scaling curves transfer to real research.
- The formal-math results do not distinguish **sequential bottleneck** from **missing insight**.
- The Anthropic extrapolation assumes equal value per agent-hour and treats extra runtime as parallel
  labor — both strong assumptions.
- The Astra-versus-internal-model estimate (**~300x compute**) is explicitly flagged as an unknown
  extrapolation.
- Counterpossibilities the author concedes: better coordination, more diverse training, recombination
  such as the Fork-and-Flush branching method, or genuinely new learning methods could change the curves.
- The essay does **not** falsify runaway RSI; it argues the scaling assumptions in those models exceed
  current evidence.

## Affected pages

- [[Recursive Self-Improvement]]
- [[Automated AI Research]]
- [[Test-Time Scaling]]
- [[Ramez Naam]]

## Raw capture

- [[Can a Million AI Agents Create Superintelligence]]

## Citations

- Raw capture: [[Can a Million AI Agents Create Superintelligence]]
- Canonical URL: <https://www.rameznaam.com/p/can-a-million-ai-agents-create-superintelligence>
- Published 2026-10-19; captured 2026-10-22. Also crossposted on Noah Smith's blog.
- Cites, but this ingest did not read: Toby Ord's swarm-scaling analyses; OpenAI GPT-5.6 cybersecurity
  and Navier-Stokes materials; the Anthropic Opus 5.5 system card; Chan et al. (2026); Eth and Davidson
  (2025); Davidson and Houlden (2025); the Artificial Hivemind study; X-MAS; Aitchison et al.;
  Greenblatt's ARC experiment; Argus; Microsoft/Berkeley ARC-AGI-3; and the Fork-and-Flush study.

## Related pages

- [[Agent Delegation]]
- [[Benchmark Optimization]]
- [[Epoch AI]]
- [[Self-Replicating Agents]]
- [[Multi-Tenant Agent Architecture]]
- [[LLM Reasoning]]
- [[The Decoherence Trap]]
