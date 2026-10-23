---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-20-guan-beyond-gmean-squared
source_title: "Beyond g-mean²: complementary metrics for monitorability"
source_author: Melody Guan, Yuxiang Xie, Bowen Baker
source_url: https://alignment.openai.com/beyond-gmean-squared/
tags:
  - source/summary
  - monitoring
  - evaluation
  - metrics
source_ids:
  - src-2026-10-20-guan-beyond-gmean-squared
status: active
---

# Melody Guan et al - Complementary Metrics for Monitorability

## Summary

An OpenAI Alignment post arguing that **one monitorability number is not enough**. It keeps
dataset-level **g-mean²** as the primary headline metric and adds two complements: **pair-matched
monitorability**, which compares models only on instances both support, and **post-control risk**,
which asks what survives when the monitor is used as a rejection gate and the model retries.

The contribution is methodological. Nearly every formula is a **proposal**, the recovery
demonstrations are **synthetic simulations**, and the historical analysis re-scores existing system-card
evaluations rather than running new model experiments.

## Key claims

### The metrics being proposed

- **g-mean²** is the product of class-conditional rates, **TPR × TNR**, where TPR = P(Z=1 | Y=1) and
  TNR = P(Z=0 | Y=0). Y is the ground-truth behavior label and Z is the monitor's flag.
- For **process evaluations**, only Y=1 rollouts are scored, so TNR = 1 and g-mean² collapses to TPR.
- For **intervention evaluations**, the original score uses an **optimistic upper bound** on causal
  recall. The post adds a pessimistic lower bound, `TPR_lower = max(0, (r + R_effect − 1) / R_effect)`,
  alongside `TPR_upper = min(1, r / R_effect)`.
- **Pair matching** scores models only on shared supported instances, removing the selection effect
  where models produce valid positive behavior on different task subsets.
- **HodgeRank**, inverse-variance weighted, fits model scores whose pairwise differences best reproduce
  observed pairwise differences. The authors rejected Bradley-Terry/Elo-style ratings here because
  those keep only win/loss direction and discard the **magnitude** of each pairwise gap.
- **Post-control risk** simulates sampling up to **K** outputs, rejecting flagged ones, and deploying
  the first accepted output. It reports **B(K)** (probability of deploying a bad output), **A(K)**
  (probability of deploying anything), and the conditional ratio **B(K)/A(K)**.

### What was actually run

- **Synthetic simulation:** a seven-model setup with known ordering M7 > M6 > ... > M1, where adjacent
  models differ by **0.03 TPR** on every fixed instance and M7 versus M1 differs by **0.18**. These are
  simulation parameters, not observations of real models.
- In a two-model simulation, Model B was easier to monitor on **every fixed instance**, yet raising B's
  capability made it produce harder positive instances until dataset-level g-mean² favored A. Pair
  matching continued to favor B. The post reports no numeric values for this demonstration in prose.
- **Historical re-analysis:** **7** agent-model configurations — o1, o3, GPT-5, GPT-5.2, GPT-5.4,
  GPT-5.5, and GPT-5.6 Sol — with GPT-5 at high reasoning effort as monitor. GPT-6 Astra was excluded
  because it used a different monitor. Error bars came from **500** deterministic hierarchical
  bootstrap replicates.
- Historical pair-matched and dataset-level orderings **generally agreed**; antischeming was close to a
  tie and one health-queries environment sat near the ceiling. No exact scores appear in the prose.
- **Post-control configuration:** headline estimates at **K=1** and **K=4**, reported only when at least
  **5** instances met the requirement. In two illustrative Honeypot slices, **B(4)** was below **3%**
  and **A(4)** below **7%**, with **41-45%** of deployed outputs positive. These are specific measured
  slices, not general rates.

## Why it matters

This is the first source in the vault that treats **the monitorability metric itself** as the contested
object rather than reporting a monitor's score. It supplies [[Chain-of-Thought Monitoring]] with a
concrete mechanism for a failure this vault has only described qualitatively: a model can become
**harder to monitor at the dataset level while being easier to monitor on every individual instance**,
purely because improved capability shifts which instances it succeeds on. That is a selection effect,
not a monitoring regression.

The post-control framing also separates **detection quality** from **deployed risk**, which matters for
[[Interpretability Evaluation]] and [[Embedded Evaluation]]: a rejection gate plus retries changes the
quantity being measured, and the authors are explicit that the deployment scheme is hypothetical.

## Tensions / open questions

- The authors keep dataset-level g-mean² as primary; pair matching is a complement, **not a replacement**.
- Pair matching does **not** guarantee the compared instances elicit the same behavior type, difficulty,
  severity, or legibility. A higher matched TPR may mean a model produced **more legible** misbehavior.
- HodgeRank cannot compare disconnected comparison components, and its absolute scores are not comparable
  across components or fits. Large residuals signal that a single ordering is a poor summary.
- **A low B(K) can mean the system rarely deploys anything at all.** It must be read with A(K) and
  B(K)/A(K), and K=1 and K=4 results can use different eligible instance sets.
- Outcome post-control risk is base-rate dependent: a model that rarely misbehaves can show low risk
  even when it is poorly monitorable.
- Retries are **non-adaptive** — the model is not told an earlier output was rejected — so this does not
  model adaptive evasion.
- A high intervention upper bound alone does not show that causal positives are reliably caught; the
  causal-recall interval can stay wide even with exactly known population rates.
- The post cites a prior finding that a model trained against a CoT monitor hacked less overall yet
  produced **more accepted hacks** under monitor-gated rejection sampling. That is a particular setup,
  not a universal law.
- Synthetic recovery of a known ordering does not establish recovery on real model behavior.

## Affected pages

- [[Chain-of-Thought Monitoring]]
- [[Interpretability Evaluation]]
- [[Embedded Evaluation]]
- [[OpenAI]]

## Raw capture

- [[Beyond g-mean² complementary metrics for monitorability]]

## Citations

- Raw capture: [[Beyond g-mean² complementary metrics for monitorability]]
- Canonical URL: <https://alignment.openai.com/beyond-gmean-squared/>
- Published 2026-10-20; captured 2026-10-22.
- Cites "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation", Figure 7,
  for the rejection-sampling result; that paper was not read during this ingest.

## Related pages

- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Agentic Testing]]
- [[Benchmark Optimization]]
- [[Reasoning Trace Privacy]]
- [[Apollo Research - Principles for Embedded Evaluations]]
