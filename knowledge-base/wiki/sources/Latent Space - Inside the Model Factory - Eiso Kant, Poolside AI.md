---
type: source-summary
created: 2026-08-03
updated: 2026-10-19
source_id: src-2026-07-23-latent-space-eiso-kant-poolside-model-factory
source_title: "Inside the Model Factory - Eiso Kant, Poolside AI"
source_author: Latent Space
source_url: https://www.latent.space/p/poolside
tags: [source/summary, training, research, poolside]
source_ids: [src-2026-07-23-latent-space-eiso-kant-poolside-model-factory]
status: active
---

# Latent Space - Inside the Model Factory - Eiso Kant, Poolside AI

## Summary

A Latent Space podcast interview in which swyx and Vibhu talk with Poolside co-founder Eiso Kant on
the launch of Laguna S. Kant frames Poolside's advantage as a **model factory**. It treats model
building as an industrial process, "ultimately 90% engineering," optimized for "the speed of an idea
from a researcher to an experimental result that we can trust." Reproducible data and code,
streamed data mixtures, and reliable runs make each model "an artifact of someone's process." It is
a case study in research throughput, not a claim that automation replaces research judgment. Nearly
every figure is a launch-day self-report.

## Key claims

### The factory

- Kant reports "less than 70 researchers, another 35 engineers" running "far more than 10,000, maybe
  10 to 20,000 experiments a month." He adds that he has not checked the latest count.
- Laguna XS 2 took "five weeks from the beginning of training to launch," and Laguna S eight weeks.
  Earlier six-month gaps between trainings mixed so many changes that the result was "a bit of a
  soup." Laguna S had zero on-call events; only the first six hours of a run usually need fixes for
  configuration mistakes.
- Data streams into training instead of being packaged and copied to clusters. A service called
  **Blender** expresses mixtures as configuration, so a job can start while data still materializes.
- An immutable data layer plus experiments as code allow tracing "down to the single token at which
  cursor it went in on which version of the code." Kant says, "I can still reproduce runs from two
  years ago." He says it took about a year and a half to see that this rigor, not speed alone, was
  the point.

### Agents inside the factory

- Agents on researchers' screens are "writing the code. They're launching the jobs. They're
  evaluating the results ... making the changes." Humans are "still in the driver's seat ... coming
  up with the ideas ... helping with the debugging." Agents are most prominent in the pre-training,
  post-training, and synthetic data pipelines, and now increasingly in architecture work. Kant calls
  this "twinklings of what RSI is gonna look like."
- Changes with experimental results from the previous day can enter the next run. The interview
  does not say who decides that promotion.

### Laguna S

- Laguna S is a **118B-total, 8B-active** MoE, scaled up from XS, with a three-to-one ratio of
  sliding-window to global attention. It was trained in FP8 on what Kant calls a "10K H200 cluster."
  The embedded launch post adds a context window of up to 1M tokens and thinking and no-thinking
  modes.
- Applied-research head Peng Ming attributes much of the gain to behavior rather than intelligence:
  "more verification, less taking things for granted, not declaring victory early, and being way
  more persistent." Kant says the gains are "entirely post-training."
- Kant says it solved Erdős 397 independently and outperforms models "two or three times their
  size." He calls it "probably" state of the art in its weight class, while naming Fable and 5.6 as
  the best models overall. Latent Space's framing has it beating Thinking Machines' roughly
  1T-parameter release, and swyx says this holds on some of that release's benchmarks.

### Training, harnesses, and openness

- Kant expects RL to move earlier into pre-training and says next-token prediction alone is "not
  enough." He calls distillation and environments the industry's "drugs" and doubts the path to AGI
  is "just more environments." He describes mid-training as "a really dumb way to do a curriculum."
- RL wall-clock time is his biggest bottleneck. Finite task sets cap RL batch size, so he hopes
  prefill/decode-style hardware splits reach RL training.
- Poolside does not distill its released models from a larger internal model. The models are "dual
  purpose": they are both research progress checks and products.
- Poolside's own harness has about six tools. Kant calls MCP and tool calls "stupid" and prefers
  containers in which models write code, while Poolside still supports tools.
- He would rather live with "100 foundation model companies than ... five, even if I was one of the
  five." He calls weights "a binary" and research the more meaningful release. He opposes
  restricting open models at current capability levels but expects that to change at some point.

## Why it matters

The interview is the evidence base for [[Model Factory]]: streamed, versioned, rerunnable inputs as
the precondition for trustworthy experiment volume. It also gives a concrete account of agents
executing experiments while humans keep the ideas, relevant to [[Automated AI Research]] and
[[Recursive Self-Improvement]]. Its skepticism about ever-larger environment sets is a counterweight
on [[RL Environment Design]], and its code-over-tools stance parallels [[Programmatic Tool Calling]].

## Tensions / open questions

- Throughput, reliability, cadence, and capability figures are unaudited self-reports. "Experiment"
  is never defined, and the count is an estimate.
- The behavior-over-intelligence explanation is one researcher's impression, not an ablation.
- The capability claims depend on benchmark and weight-class framing; third-party evaluation is
  described as planned.
- Agents' share of the work is unquantified. Who promotes changes into runs is not stated, so the
  interview does not show humans gating promotion.
- "The training run is not the expensive part" comes with no cost figures in the capture.

## Affected pages

- [[Model Factory]]

## Raw capture

- [[2026-07-27 Latent.Space - Inside the Model Factory — Eiso Kant, Poolside AI|Inside the Model Factory — Eiso Kant, Poolside AI]]

## Citations

- Canonical URL: https://www.latent.space/p/poolside
- Published July 23, 2026; captured July 27, 2026. The transcript dates the recording to around
  July 15.
- Speakers: Eiso Kant (Poolside) with hosts swyx and Vibhu. The Laguna technical reports and the
  launch post are referenced but not captured here.

## Related pages

- [[Model Factory]]
- [[Automated AI Research]]
- [[LLM Training Pipeline]]
- [[Recursive Self-Improvement]]
- [[RL Environment Design]]
- [[Programmatic Tool Calling]]
- [[Coding Agent Harness]]
- [[Prefill-Decode Disaggregation]]
- [[Open Model Ecosystems]]
- [[Knowledge Distillation]]
