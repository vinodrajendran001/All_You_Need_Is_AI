---
type: concept
created: 2026-07-03
updated: 2026-08-26
tags:
  - concept
  - reasoning
  - llm
  - evaluation
  - post-training
source_ids:
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
status: active
---

# LLM Reasoning

## Definition

LLM reasoning is the ability of a language model to draw new, consistent conclusions from known facts — going beyond recall or surface pattern-matching — and the body of techniques for eliciting, improving, and evaluating that ability. This page is the **hub** that ties together the vault's reasoning material: how models reason, how well they reason, how we make them reason better, and how brittle it all is.

## Why it matters

General-purpose reasoning has become the substrate under chat, search, browsing, coding, medicine, and science. But "reasoning" in an LLM is not what the metaphor suggests, and the gap between benchmark accuracy and dependable reasoning is where most of the open problems live. Organizing the vault's scattered reasoning pages ([[Reasoning Compression]], [[Test-Time Scaling]], [[Latent-Space Reasoning]], [[Recursive Architectures]], [[Monte Carlo Tree Search]]) under one map makes those problems legible.

## Current synthesis

[[Akhil Arora et al - Current Advances in LLM Reasoning]] is the anchor: a full field survey organized as *how well can models reason → how do we make them reason better → what are the frontiers*.

### What reasoning is

- Three classical types: **deduction** (apply a rule → certainty), **abduction** (guess the best cause → plausibility), **induction** (learn the rule → probability). LLMs are **primarily inductive** — they emulate reasoning by pattern completion at inference time, and "thinking models" bake those patterns into the weights.
- Chain-of-Thought emulates *deductive* chains. *Abductive* reasoning (generate candidate causes, then score them against evidence) needs divergent-then-convergent search that a single linear pass can't do — the reason [[Monte Carlo Tree Search|tree/search methods]] and multi-agent orchestration exist.

### The frozen-θ thesis

- A trained model already contains latent CoT paths, self-verification, backtracking, subgoal decomposition, and tool schemas. Gains come from two directions, both of which post-training *unlocks* rather than teaches: **internal search & exploration** (self-consistency, Tree-of-Thoughts, MCTS, beam search, Fleet of Agents) and **external verification, retrieval & tools** (RAG, tool calls, process/generative reward models, code execution). "Better reasoning — same θ." This is the through-line connecting [[Test-Time Scaling]] and [[Latent-Space Reasoning]] (surface a latent path) with [[Retrieval-Augmented Generation]] and [[LLM-as-a-Judge]] (anchor to ground truth).

### Reasoning traces are not thoughts

- Reasoning traces are token sequences like any other; they **do not have to be faithful**. Biased context can flip an answer while the CoT rationalizes post-hoc — "reasoning models don't always say what they think." Longer traces are not always better (a model can get lost in a wrong path, or self-correct a right answer into a wrong one). This is why [[Reasoning Compression]] treats trace length as a controllable budget and why mechanistic interpretability is proposed as a better lens than reading the trace.

### Reasoning is brittle

- Four fragility axes, each backed by multiple studies: **input perturbations** (rename/renumber → 10–65% drop, GSM-Symbolic); **cultural/context** (an irrelevant cultural rule = −24.5 pp on NormAd); **prompt sensitivity** (fidelity-preserving prompt polish raises plain input-output prompting from 3.0 → 31.3); and **faithfulness**. A key methodological consequence: single-run evaluation hides instability, so repeated runs and error bars are mandatory (ReasonBench).
- **High-stakes failure** is concrete: against the Ledley (1959) diagnostic loop, models manage clinical facts but fail at hypothesis generation, probability estimation, and — most dangerously — action selection (a triage test undertriaged 52% of emergencies). This pushes evaluation toward interactive **simulators** rather than static QA.

### Making models reason better

- Two levers, developed on their own pages: **inference-time** compute ([[Test-Time Scaling]]) and **post-training** ([[LLM Training Pipeline]], [[Reinforcement Learning]]). The post-training story runs SFT (compose skills from a data mix; quality > quantity) → preference learning ([[Direct Preference Optimization]]) → verifiable-reward RL ([[Reward Design for RL|RLVR]]) with [[Group Relative Policy Optimization|GRPO]], and increasingly **distillation merged with RL** ([[Multi-Teacher On-Policy Distillation]]).
- A load-bearing open debate frames all of it: **SFT reproduces, RL discovers** — but does RL *create* new reasoning or merely *amplify* latent pre-training capability? (Base models show "aha moments" without RL.)

### Frontiers

Open pillars, each with 2025–2026 evidence they are unsolved: retrieval-vs-memory; verification (calibrated uncertainty, process rewards without human labels, verifier robustness, formal bridges); test-time scaling (sufficiency detection, early exit, test-time RL); **multi-agent systems** (the "illusion of MAS advantage" — does it help under *token-matched* controls?); **continual learning** (catastrophic forgetting, model collapse, "peak data," reward hacking — overlaps [[Nested Learning]]); and systems (parallel/speculative decoding, batched-inference determinism).

## Open questions

- Does RL create reasoning or amplify pre-existing capability — and how should that answer reshape reward design and data curation?
- If traces are unfaithful, what should supervise and evaluate reasoning instead of the trace itself?
- Can robustness (to perturbation, culture, prompt, language) be trained in, or is it an evaluation-protocol artifact we keep mismeasuring?

## Related pages

- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Reasoning Compression]]
- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[Monte Carlo Tree Search]]
- [[Reinforcement Learning]]
- [[LLM Training Pipeline]]
- [[Group Relative Policy Optimization]]
- [[Reward Design for RL]]
- [[LLM-as-a-Judge]]
- [[Retrieval-Augmented Generation]]
- [[Agentic Reinforcement Learning]]
- [[Nested Learning]]
- [[LLM Inference]]
- [[AI Knowledge Base Overview]]
