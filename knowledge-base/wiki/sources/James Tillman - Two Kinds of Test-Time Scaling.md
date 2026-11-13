---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-09-tillman-two-kinds-test-time-scaling
source_title: Two Kinds of Test-Time Scaling
source_author: James Tillman
source_url: https://www.forethought.org/research/two-kinds-of-test-time-scaling
tags:
  - source/summary
  - test-time-scaling
  - evaluation
  - forecasting
source_ids:
  - src-2026-11-09-tillman-two-kinds-test-time-scaling
status: active
---

# Two Kinds of Test-Time Scaling

## Summary

James Tillman (Forethought) separates two kinds of test-time scaling. In the first, extra
per-task compute helps only up to the most a model used per task in training. In the second,
which he calls **compute extrapolation**, performance keeps rising at test time beyond anything
the model saw in training. He argues that compute extrapolation speeds up the most impressive AI
capabilities, makes dangerous-capability evaluations much harder, and moves races in compute
spending from training to inference. He dates its arrival in frontier LLMs to around the end of
2025, through "LLM compaction" and other context management. He supports this with clear evidence
from one academic paper and calls the rest circumstantial, because labs do not publish how
training compute is spread across tasks. The essay is an argument and forecast, not a new
experiment.

## Key claims

### A definition that resists training outliers

- Learned test-time scaling methods include **chain-of-thought length** for an RLVR-trained LLM,
  **number of loops** in a looped Transformer, and **number of agents** in a swarm. Each has a
  per-task maximum during training. The question is whether that maximum also caps useful
  test-time compute.
- To keep a single expensive training task from erasing the effect, the reference point **N** is
  the per-task compute below which **99%** of total training compute was spent. Tillman says 98%
  or 99.9% would work about as well. A method shows compute extrapolation if spending **10x N** or
  **1000x N** per task still improves performance.
- Two measurements describe it. The **ceiling** is the multiple of N at which gains stop. Tillman
  believes there will often be no absolute ceiling, or that it might be "extremely
  (1,000-1,000,000) high". The **slope** p compares performance past N with the curve fitted
  below N. Both probably vary by domain and are easier to push in domains where incremental
  progress is easy to recognize, such as math or cyber.
- It overlaps with, but is distinct from, horizon-length generalization in Cotra's bioanchors
  report. Extra loops in a looped Transformer could extrapolate without lengthening task
  horizons.
- The 10^17, 10^21, and 10^24 FLOPs figures in the essay are illustrations, not measurements.

### Three consequences, plus a generalization signal

- **The top of the capability range moves faster.** Without extrapolation, spending 10^24 FLOPs
  on one consequential task requires spending that much on many training tasks. The analogy is
  AlphaGo Zero: about **0.4s** of thought per move in training, **5s** in one evaluation, and
  about **a minute** in a tournament. Tillman reads this as a ceiling of **at least 100x**. His own
  estimate is that training to the same level without extrapolation would have cost **10x-50x**
  more.
- **Dangerous-capability evaluations become impossible or very expensive by default.** An
  evaluator can no longer stop at the training-time per-task maximum. Citing the UK AISI, he
  expects evaluations that can only rule out a dangerous capability *below a given spending
  budget*, affordable in only a few high-importance domains. Scaling curves on smaller tasks could
  substitute, but he says that is not how such evaluations are currently run.
- **Spending races move to test time.** If being first matters, it can be rational to spend
  "millions of dollars on some task" with an earlier model, even if a later model could do it for
  **10%** or **0.1%** of the cost. He expects growing inference spending on AI moonshots and
  growing losses on failed bets.
- **Extrapolation is evidence of better learning.** A model that generalizes beyond its training
  compute range probably also generalizes better within it.

### When it started

- Tillman thinks RLVR as first implemented at the end of 2024 likely showed no significant
  extrapolation; o1 and R1 are his examples of the capped state. He says progress in "LLM
  compaction" probably began producing significant extrapolation around the end of 2025, and that
  this probably helps explain the jump in compute use by OpenAI and Anthropic researchers.
- **The Markovian Thinker** (Aghajohari et al., 2025) gives the cleanest evidence. Standard
  RLVR lets the model generate up to **24k** chain-of-thought tokens without interruption.
  "Delethink" generates **8k** tokens, deletes all but the last **4k**, and continues. That cycle
  is allowed up to **5** times in training and **30** or more at inference. Delethink keeps
  improving on AIME25 well past the training maximum; the standard method does not. Tillman
  says the model can "think past 4x" its training compute and that the paper shows no clear
  ceiling, so it gives only a lower bound. The figure description puts Delethink at about **0.35**
  at **128K** tokens and standard long chain-of-thought RL leveling off at about **0.30**. Delethink
  also uses fewer total FLOPs per training step.
- **Supporting and contrary papers.** "Reasoning Cache" trains on up to **16k** generated tokens
  and keeps improving up to half a million. A summarization-based context-management paper shows
  similar gains in an agentic setting. As contrary evidence, E3 gets extrapolation without
  chunking, but only "2.5x extrapolation" and with other training changes; it also finds several
  open-weight LLMs do not benefit from more tokens than they were trained on. Tillman concludes
  that chunking is not strictly required but that the more Markovian loop is a good prior for
  generalization.
- **Frontier-lab evidence is weaker.** For Anthropic he points to around Opus 4.6 (February 2026).
  On MirrorCode, Opus 4.1 and 4.5 hallucinated time limits. Opus 4.6 was still improving its
  reimplementation of *pkl* at the end of a **billion-token** budget, with about **2 million**
  generated tokens and tens of compactions. He calls this weak evidence. Toby Ord's analysis of UK
  AISI data, "with large error bars", has Opus 4.5 needing **370x** more chain-of-thought tokens for
  the gain a human gets from thinking **10x** longer, against **46x** for Opus 4.6.
- **OpenAI's evidence is ambiguous.** GPT-5.1-Codex-Max (November 2025) was advertised as the
  "first model natively trained to operate across multiple context windows through a process
  called compaction", but METR reports that compaction does not increase its time horizon.

### Multi-agent scaling may extend the ceiling

- OpenAI's agents cooperated on the order of **1,000** (the HF swarm, by accident) and **10,000**
  (the Navier-Stokes swarm, on purpose), though Noam Brown attributes little of that result's
  efficacy to swarm size. Tillman guesses that training used at most **10-100** agents, which would
  imply an extrapolation horizon of **at least 10-1,000**. He calls this weak evidence.
- Networks whose members keep a bounded number of connections may be self-similar across scales,
  unlike one linear chain of thought. Time also caps single-agent extrapolation in practice,
  because an agent that thinks for months becomes unwieldy to use.

## Why it matters

[[Test-Time Scaling]] gains a distinction it lacked: whether a method merely uses its training
budget, or keeps paying off beyond it. That changes how the page's width and team results should
be read. [[Recursive Self-Improvement]] and [[Automated AI Research]] gain a mechanism by which the
largest AI R&D tasks could be attempted with test-time spending rather than new training. For
[[METR]], it records a METR time-horizon finding that cuts against its own thesis. The math-and-cyber
point about recognizable progress also bears on [[AI for Mathematical Discovery]]. The
evaluation consequence connects to [[Embedded Evaluation]], compaction to [[Context Engineering]],
and the swarm argument to [[Multi-Agent Coordination]].

## Tensions / open questions

- **The central dating claim is inferential.** Tillman says direct evidence is impossible from
  outside, because Anthropic and OpenAI do not publish per-task training-compute distributions.
  The frontier-model evidence is in his words weak or ambiguous, and METR's finding on
  GPT-5.1-Codex-Max cuts against it.
- **The strongest result is one small academic setup.** The Markovian Thinker result is on
  competition math, and the figure description includes an R1-Distill 1.5B baseline. Whether it
  transfers to frontier agentic work is not shown.
- **The AlphaGo Zero numbers are partly his own estimate.** The 10x-50x training-cost figure is
  Tillman's estimate, not a reported measurement.
- **The multi-agent argument rests on a guess.** The 10-100 training-agent maximum is his
  assumption, and Noam Brown's view that swarm size contributed little weakens the 10,000-agent
  example.
- **Footnotes are missing.** The prose references seven footnotes, but their text is not in the
  capture. The two chart descriptions are image text; only their prose restatements are used here.
- The essay names policy questions rather than answers: should labs publish their most
  compute-intensive training tasks, which domains allow recognizable incremental progress, and what
  the first sign would be that extrapolation reaches algorithmic taste and machine learning research.

## Affected pages

- [[Test-Time Scaling]]
- [[Recursive Self-Improvement]]
- [[METR]]
- [[AI for Mathematical Discovery]]
- [[Embedded Evaluation]]
- [[Context Engineering]]
- [[Multi-Agent Coordination]]

## Raw capture

- [[knowledge-base/raw/sources/Two Kinds of Test-Time Scaling]]

## Citations

- Canonical URL: <https://www.forethought.org/research/two-kinds-of-test-time-scaling>
  (the capture's URL carried a `utm_source=tldrai` parameter, removed here).
- By James Tillman, published by Forethought on November 9, 2026; captured November 11, 2026.

## Related pages

- [[Test-Time Scaling]]
- [[Recursive Self-Improvement]]
- [[Automated AI Research]]
- [[METR]]
- [[AI for Mathematical Discovery]]
- [[Embedded Evaluation]]
- [[Context Engineering]]
- [[Multi-Agent Coordination]]
- [[LLM Reasoning]]
- [[Reinforcement Learning]]
- [[Alex Wang - What Objective Is Reasoning Solving]]
- [[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]]
- [[General Reasoning - How to Train a Swarm]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
