---
type: source-summary
created: 2026-10-09
updated: 2026-10-09
source_id: src-2026-10-09-dickson-agent-stack-optimization
source_title: How AI agents are learning to optimize their own stack
source_author: Ben Dickson
source_url: https://alphasignal.ai/news/how-ai-agents-are-learning-to-rewrite-their-own-stack
publisher: Alpha Signal
tags: [source/summary, ai-agents, self-improvement, harness, skills, evaluation]
source_ids:
  - src-2026-10-09-dickson-agent-stack-optimization
status: active
---

# Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack

## Summary

Dickson maps self-improving agents by **what gets changed**: skills, runtime scaffolding, model
weights together with the harness, training environments, or multi-agent coordination. These are
overlapping intervention surfaces, not mandatory stages of a maturity ladder. The practical
recommendation is to start with the narrowest surface that contains the observed bottleneck.

This Alpha Signal newsletter extends the vault's earlier SkillOpt and Self-Harness/HarnessX
briefings. The new contributions are WikiSkill's persistent experience layer, explicit
model-harness co-evolution, environment-side adaptation, and orchestration as an optimization
target. Research results remain secondary reporting.

## Key claims

| Editable surface | Described mechanism |
| --- | --- |
| Skills | SkillOpt proposes bounded document edits and accepts them against held-out validation; WikiSkill organizes successes, failures, and rejected fixes in a wiki between execution traces and executable skills |
| Harness and improvement code | Self-Harness mines recurring failures and validates targeted runtime changes; Darwin Godel Machine keeps an archive of descendants; Hyperagents puts a task agent and its modifying meta-agent in one editable program |
| Model-harness pair | HarnessX evolves scaffolding and reuses trajectories as model-training data, so strategies discovered by the harness can be internalized by the model |
| Training environment | EnvHarness modifies starting conditions, observations, or available actions through programmable wrappers while leaving underlying environment logic and the verifier unchanged |
| Orchestration | Raven's host decomposes work, assigns specialists, coordinates dependencies, and can evolve model/domain-specific harnesses from benchmark feedback |

WikiSkill's wiki is not the deployed skill itself. It retains evidence used to propose future
skills and aims to avoid rediscovering failures or retrying rejected fixes. Hyperagents likewise
adds a separate distinction: editing the process that proposes improvements is broader than
editing a task-performing agent.

### Reported results and their boundaries

The clipping reports Self-Harness across **three model families** on **Terminal-Bench-2.0,
SWE-bench Verified, and AppWorld**, with relative gains reaching **132%**. The matching public
article's accessible takeaways resolve that maximum to **Qwen3.5-35B-A3B on AppWorld,
22.5% to 52.2% overall**. That is a **29.7-percentage-point absolute increase**, not 132 points.
They report gains on both splits in all nine model-benchmark runs and identify
**GLM-5 on AppWorld, 44.4% to 85.0%**, as the largest absolute increase.

For EnvHarness, the clipping reports **up to nine points on held-out tasks across five benchmarks**
and **about 9.8% fewer interaction steps**. It does not give the per-benchmark rows, denominators,
aggregation method, or total training/search cost. Fewer interaction steps are not a measured
9.8% reduction in wall-clock time or total compute.

No numerical WikiSkill or Raven comparison is supplied in the clipping. This ingest does not
reproduce any of the cited experiments.

## Why it matters

The map refines [[Harness Optimization]] rather than replacing its editable-scope ladder.
Procedural errors can warrant a skill edit; stale training experience can warrant an environment
change; coordination failure can warrant graph work. More editable code is not automatically the
right intervention.

[[Persistent Wiki]] gains another role: a durable evidence store upstream of deployable procedures,
not only a knowledge store upstream of answers. [[Recursive Self-Improvement]] also needs to track
which artifact persists after a run instead of classifying every HarnessX result as frozen-model
workflow improvement.

## Tensions / open questions

- The earlier newsletter described HarnessX through harness-module search, while this account
  explicitly includes model training. Preserve both scopes; the product name does not establish
  which experimental variant changed weights.
- The older 33-60% Self-Harness figures and this wider-suite 132% maximum are not a like-for-like
  trend. Model, benchmark, split, baseline, and relative-versus-absolute units must travel with each.
- The clipping says co-evolution applies only to open-weight models. The technical requirement
  is access to train and version the underlying model; an inference-only API cannot provide it.
  "Open weight" is an enabling access arrangement, not the definition of co-evolution.
- Regression gates are design controls, not proof against reward hacking or an ablation showing
  that the gate alone caused the gain. Repeated validation can still overfit.
- Holding a verifier fixed does not prove an environment wrapper preserved task meaning or
  prevented answer leakage. Those are additional checks the proposed loop needs.

## Affected pages

- [[Agent Skill]]
- [[Persistent Wiki]]
- [[Harness Optimization]]
- [[Coding Agent Harness]]
- [[Recursive Self-Improvement]]
- [[RL Environment Design]]
- [[Graph Engineering]]
- [[Alpha Signal]]

## Raw capture

- [[2026-10-09 Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]]

## Citations

- Original user-supplied Alpha Signal newsletter clipping, previously in the inbox; its original
  capture timestamp is unknown. Formally archived on October 9 with its body bytes preserved.
- Public version: <https://alphasignal.ai/news/how-ai-agents-are-learning-to-rewrite-their-own-stack>,
  titled "How AI Agents Are Learning to Rewrite Their Own Stack." The matching opening/skill
  sections, Ben Dickson byline, canonical URL, and accessible result qualifications were checked
  on October 9 and recorded separately in the raw capture's provenance section.
- The complete newsletter text comes from the user's clipping. The public page's sign-in
  boundary was not bypassed, and subscriber tracking redirects were not used as canonical URLs.

## Related pages

- [[Alpha Signal - How your agents can write and optimize their own skills]]
- [[Alpha Signal - Why self-improving harnesses are the next frontier]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Benchmark Optimization]]
- [[Agent Security and Governance]]
