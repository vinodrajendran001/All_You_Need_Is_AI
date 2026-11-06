---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-10-30-figma-fluent-editing-model
source_title: "How We're Training a Figma-Fluent Editing Model"
source_author: Josh Clemm
source_url: https://www.figma.com/blog/training-a-figma-fluent-editing-model/
tags:
  - source/summary
  - post-training
  - design-tools
  - evaluation
  - agents
source_ids:
  - src-2026-10-30-figma-fluent-editing-model
status: active
---

# How We're Training a Figma-Fluent Editing Model

## Summary

Josh Clemm describes how [[Figma]] post-trains a first-party model for one narrow job inside the
Figma agent: **editing designs that already exist on the canvas**. That work is frequent, iterative,
"often non-verifiable", and latency-sensitive. The first recipe was supervised fine-tuning (SFT) on
synthetic edit examples in Figma's native file format. Larger teacher models produced candidates,
and deterministic validators plus visual model judges filtered them. Because of SFT's limits on
generalization and sample efficiency, Figma is adding reinforcement learning. Evaluation breaks
quality into separate dimensions, combines structural checks with visual judges, and uses expert
designers for calibration. In production the agent routes between this model and third-party
models. Figma reports faster tasks, higher ratings and fewer undos. It attributes these gains to the
whole agent, not to the model alone.

## Key claims

### Why a specialized model

- The target is everyday edits: adjust spacing, change a color, rework a layout after feedback.
  "Speed matters", because a slow edit interrupts the workflow it is meant to help.
- When the work began, frontier models "couldn't understand Figma syntax". Prompting them into it
  would have been "incredibly token-consumptive", so Figma invested in fine-tuning instead.

### The SFT data pipeline

- Each example pairs a starting design, a generated synthetic edit request, and a successful change.
  Designs are represented in **Figma's native file format**, so outputs can be applied back to the
  canvas. Synthetic prompts also cover design-system themes and components.
- **Larger teacher models** attempt the edits. **Deterministic validators** and **visual model
  judges** check candidates for valid output and request fulfillment. The pipeline can "self-heal"
  by revising an edit using evaluator feedback.
- An earlier **Llama 3.3 70B** model trained on **more than 250,000 examples** was "competitive on
  editing tasks with top models at the time". No numbers are given.
- The pipeline diagram also shows LLM-judge training informed by designer annotations.

### From imitation to RL

- Figma has moved to more capable base models: "the newer Qwen models, Muse Spark Open, Inkling, and
  others".
- SFT alone hit limits. Imitation produces designs close to training data "at the cost of loss of
  generalization", and it is "less sample efficient".
- RL work focuses on design RL environments, example diversity, reward-model shaping, and expanded
  expert-written criteria so that rewards reflect what designers care about.

### Decomposed evaluation

- Internal evals score Figma fluency, instruction following and useful changes, plus **speed and
  cost**.
- Quality is split into separate dimensions. A design can have good alignment and poor contrast. An
  edit can look polished and miss the request. A button can look right and use the wrong component.
  Structural checks and visual judges are combined, and expert designers calibrate and review the
  results.
- On the internal Figma editing eval, "Figma design edits v3" scores **77.8%** and "Sol 6.1" scores
  **76.9%**. The caption calls it the latest unreleased model, "post-trained on Qwen 3.8 27B". The
  post calls the eval "just one input among many".

### Production routing and reported outcomes

- The agent, rolled out to all users "earlier this month", runs this model alongside third-party
  models. Image generation, vectors and brand-new explorations go to "the best third-party model
  available". Precise edits and iterations go to the first-party model.
- Between beta and general availability: typical tasks about **20% faster**. The new agent beats or
  matches the previous production agent **62%** of the time with expert designers. User ratings are
  **33% higher**, and undo happens **60% less often**. The share of work on the first-party model
  "more than doubled", and average cost per message fell.

## Why it matters

- [[Model Factory]]: a concrete product-team instance of teacher-generated data, verifier-filtered
  samples, SFT, then RL with expert criteria, gated by an internal eval that includes cost and speed.
- [[Generative User Interface]]: editing an existing design in its native format is a different
  problem from generating an interface from scratch. Unrelated content must be preserved, and
  output must re-apply to the canvas.
- [[Figma]]: the publisher's own account of why it owns one model in a mixed-vendor agent.
- [[Model Routing]] and [[LLM-as-a-Judge]]: task-type routing between first- and third-party models,
  and visual judges calibrated by designers.

## Tensions / open questions

- **First-party and partly promotional**: the post ends with a hiring pitch. No eval set size, rubric,
  inter-rater agreement or confidence intervals are given.
- **The headline chart compares one model with one rival** at a 0.9-point margin (derived) on
  Figma's own eval. "Several top models" are mentioned, but only two values appear in the capture.
- **Outcome metrics are not attributable to the model.** Figma itself says the gains come from
  "models, tools, and harness". The baseline is the previous production agent, not an ablation.
- **"Non-verifiable" is handled by proxy.** Validators check structure and visual judges check
  appearance, but how well the judges agree with designers is not shown.
- The base model for the shipped model versus the unreleased v3 is not stated, and the Llama 3.3 70B
  result has no numbers.

## Affected pages

- [[Figma]]
- [[Model Factory]]
- [[Generative User Interface]]
- [[Model Routing]]
- [[Synthetic Data Flywheel]]

## Raw capture

- [[knowledge-base/raw/sources/How We're Training a Figma-Fluent Editing Model]]

## Citations

- Canonical URL: https://www.figma.com/blog/training-a-figma-fluent-editing-model/
- Byline: Josh Clemm
- Published: 2026-10-30; captured: 2026-11-02
- Publisher: Figma blog

## Related pages

- [[Figma]]
- [[Model Factory]]
- [[Generative User Interface]]
- [[Model Routing]]
- [[Synthetic Data Flywheel]]
- [[LLM-as-a-Judge]]
- [[Knowledge Distillation]]
- [[AI Agents in Production]]
- [[Qwen]]
- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]]
