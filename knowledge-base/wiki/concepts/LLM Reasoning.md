---
type: concept
created: 2026-07-03
updated: 2026-10-30
tags:
  - concept
  - reasoning
  - llm
  - evaluation
  - post-training
source_ids:
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-08-25-bytebytego-stealing-reasoning-traces
  - src-2026-07-20-raschka-reasoning-effort
  - src-2026-09-10-fu-progressive-point-matching
  - src-2026-10-12-bytebytego-energy-based-reasoning
  - src-2026-10-15-li-gradient-is-covariance
  - src-2026-10-28-sick-on-policy-self-training
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

- The tutorial argues that **internal search and exploration** and **external verification, retrieval, and tools** can improve performance with fixed inference weights. This connects [[Test-Time Scaling]] and [[Latent-Space Reasoning]] with [[Retrieval-Augmented Generation]] and [[LLM-as-a-Judge]]. It does not imply that post-training only reveals existing skills: SFT and RL change weights, and the source leaves the boundary between teaching and elicitation unresolved.

### Reasoning traces are not thoughts

- Reasoning traces are token sequences like any other; they **do not have to be faithful**. Biased context can flip an answer while the CoT rationalizes post-hoc — "reasoning models don't always say what they think." Longer traces are not always better (a model can get lost in a wrong path, or self-correct a right answer into a wrong one). This is why [[Reasoning Compression]] treats trace length as a controllable budget and why mechanistic interpretability is proposed as a better lens than reading the trace.

### Reasoning is brittle

- Four fragility axes, each backed by multiple studies: **input perturbations** (rename/renumber → 10–65% drop, GSM-Symbolic); **cultural/context** (an irrelevant cultural rule = −24.5 pp on NormAd); **prompt sensitivity** (fidelity-preserving prompt polish raises plain input-output prompting from 3.0 → 31.3); and **faithfulness**. A key methodological consequence: single-run evaluation hides instability, so repeated runs and error bars are mandatory (ReasonBench).
- **High-stakes failure** is concrete: against the Ledley (1959) diagnostic loop, models manage clinical facts but fail at hypothesis generation, probability estimation, and — most dangerously — action selection (a triage test undertriaged 52% of emergencies). This pushes evaluation toward interactive **simulators** rather than static QA.

### Making models reason better

- Two levers, developed on their own pages: **inference-time** compute ([[Test-Time Scaling]]) and **post-training** ([[LLM Training Pipeline]], [[Reinforcement Learning]]). The post-training story runs SFT (compose skills from a data mix; quality > quantity) → preference learning ([[Direct Preference Optimization]]) → verifiable-reward RL ([[Reward Design for RL|RLVR]]) with [[Group Relative Policy Optimization|GRPO]], and increasingly **distillation merged with RL** ([[Multi-Teacher On-Policy Distillation]]).
- The tutorial's "SFT reproduces, RL discovers" contrast motivates an open question, not a law: does RL create new reasoning or amplify latent capability? Reported logic-to-math transfer and reasoning in base models do not prove that SFT cannot generalize or that RL always does. The October 9 lint scopes the earlier slogan accordingly.

### Frontiers

Open pillars, each with 2025–2026 evidence they are unsolved: retrieval-vs-memory; verification (calibrated uncertainty, process rewards without human labels, verifier robustness, formal bridges); test-time scaling (sufficiency detection, early exit, test-time RL); **multi-agent systems** (the "illusion of MAS advantage" — does it help under *token-matched* controls?); **continual learning** (catastrophic forgetting, model collapse, "peak data," reward hacking — overlaps [[Nested Learning]]); and systems (parallel/speculative decoding, batched-inference determinism).

## The displayed summary is a different artifact from the trace

[[ByteByteGo - How to Steal an AI Model's Private Thoughts]] documents something this page should hold onto independently of its security framing: the "thinking" block shown alongside an answer is **generated separately** from the full reasoning trace, and the two can diverge substantially.

On an AIME 2025 problem the summary described methodical work through the geometry using the law of cosines. The recovered trace opened by stating the answer from memory and then worked backward toward a justification, with several wrong guesses along the way. The researchers did not measure how often this happens, and note that a smaller model summarising a larger one will compress the original — but one clean counterexample is enough to break the inference.

Two consequences. **Displayed reasoning is not evidence of process**, so it cannot be used to audit how an answer was reached — the same caution [[Latent-Space Reasoning]] raises from the other direction. And recovered traces were frequently telegraphic and ungrammatical rather than fluent English, which matters because trace-based safety monitoring assumes traces are legible. See [[Reasoning Trace Privacy]].

## Delimiters do not determine the computation behind a trace

[[Sebastian Raschka - Controlling Reasoning Effort in LLMs]] corrects a misreading that this page
should record explicitly: **`<think>` tags confer no reasoning ability by themselves**. They
delimit a trace so it can be displayed, budgeted, or stripped. Models acquire them from a *format*
reward added alongside the accuracy reward (`R_total = R_accuracy + R_format`) — the accuracy term
teaches reasoning, the format term teaches where to put it.

Qwen3's hard switch **prefills** an empty `<think></think>` block to close the designated trace
phase; that is not evidence of an inability to reason internally. Separately, the Kimi K2.5
report's Toggle evaluation on **K2 Thinking** reports **25-30% fewer generated tokens with
little change in benchmark performance**. Training can reorganize computation, so this does
not identify nonessential tokens in the original trace or establish the new trace's faithfulness.
The October 16 lint removes that earlier causal inference. See [[Reasoning Effort Control]].

## A longer training budget can teach a policy to waste it

[[Preston Fu - Progressive Point Matching]] reports a result that inverts a standard assumption: in training Progressive Point
Matching, **a 4K context length was comparable to or better than 8K.**

The explanation offered is behavioural rather than mechanical. The 8K policy **collapses its output length
and guesses early**, while the 4K policy is pushed to optimise partial progress within the budget it has.
Extra room does not automatically buy longer reasoning; under a sparse or poorly-shaped reward it can
instead teach the policy that early guessing is the better bet.

This connects the length-collapse dynamics recorded under [[Reasoning Compression]] to the credit
assignment problem: guessing early is rational when late-trajectory signal is worthless, so output-length
collapse is a symptom of the reward structure rather than of the model. The caveat is that the source
offers no ablation isolating output-length collapse — it is a plausible story attached to a real
measurement.

The same note treats controlling test-time budget in deployed agents as unsolved, citing Claude Code's
`/effort ultracode` mode as insufficient for scaling it. See [[Test-Time Scaling]] and
[[Long-Horizon Credit Assignment]].

## A constrained specialist tests a task, not the limits of every language-model system

[[ByteByteGo - How to Build Models Without Language]] reports Logical Intelligence's Kona
solving **96.2%** of a Sudoku demonstration's puzzles versus **2%** across the LLM panel
and **6.9%** for its best member. This is a vendor demonstration reported secondhand;
the generic energy-based explanation is not Kona's disclosed implementation.

The durable addition is a three-part reasoning pipeline: learn a compatibility score,
search candidate states, and check encoded constraints independently. It does not establish
the article's broader claims that LLMs cannot revise, extrapolate, or verify. Search, tools,
and formal checkers can also surround an autoregressive model.

Nor can the GPU-time/API-charge or mean/maximum-runtime comparisons establish general
price and speed ratios. [[Energy-Based Model]] expands the mechanism map while keeping
formal validity, accurate problem specification, and practical safety separate.

## How much RL changes a model is a different question from what it changes

[[Yingru Li - The Gradient Is a Covariance]] separates two claims that the create-versus-amplify
debate tends to merge. One common explanation of RL's effect, that it "only reweights answers the
model can already produce," accounts for why post-training updates are **small**. A bound on bits
per episode accounts for why they carry little information. Neither explains why they are
**sparse**. Li's example is that a hundred million parameters each moving slightly would satisfy
both.

Li's account of *which* coordinates can move rests on the Fisher. The expected policy gradient for
a parameter is the covariance between reward and that parameter's score on the model's own
samples. That is capped by the score's variance, so only parameters that change the model's
choices among already-likely candidates can receive much expected gradient. The cited
measurements are secondhand: RL changes **5–30%** of parameters across seven algorithms and ten
models, and on-policy distillation and near-policy SFT reportedly behave alike.

This informs the open question below without answering it. On the vault's reading, movement
concentrated where the model already spreads probability fits the amplification side. Li does not
draw that conclusion, and a necessary condition on *where* gradient can flow says nothing about
whether the resulting behavior is new. Li also leaves to later parts of the series
what policy gradient can and cannot reach.

## Self-training gains depend on the reasoning protocol and do not establish new knowledge

[[Leon Sick et al - On-Policy Self-Training]] supplies a bounded amplification result.
For Gemma 4 E2B, MMLU rises **37.5 to 47.7 without thinking**, but **69.9 to 71.1 with
thinking**. The former scores answer-option log-likelihoods; the latter parses generated
answers. Those are separate baselines and evaluation protocols, not interchangeable evidence
for one reasoning gain.

The student learns on its own rollouts while an EMA teacher sees additional generated
answer/rationale context; that teacher is also the final evaluated checkpoint. Fresh-context
and paraphrase checks test consistency, not factual truth. The authors describe amplification
of pretrained knowledge and acknowledge that consistent errors survive.

The result therefore informs rather than settles the create-versus-amplify question.
Hand-picked topics and small-model experiments bound its scope, and the all-three-domain
mixture loses **4.9 MATH-500 points** despite an improved out-of-domain average. Better
aggregate scores cannot substitute for capability-specific retention checks.

## Open questions

- Does RL create reasoning or amplify pre-existing capability — and how should that answer reshape reward design and data curation?
- If traces are unfaithful, what should supervise and evaluate reasoning instead of the trace itself?
- Can robustness (to perturbation, culture, prompt, language) be trained in, or is it an evaluation-protocol artifact we keep mismeasuring?

## Related pages

- [[Leon Sick et al - On-Policy Self-Training]]
- [[Knowledge Distillation]]
- [[Continual Learning for Agents]]
- [[Yingru Li - The Gradient Is a Covariance]]
- [[ByteByteGo - How to Build Models Without Language]]
- [[Energy-Based Model]]
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
- [[ByteByteGo - How to Steal an AI Model's Private Thoughts]]
- [[Reasoning Trace Privacy]]
- [[Reasoning Effort Control]]
- [[Sebastian Raschka - Controlling Reasoning Effort in LLMs]]
- [[Preston Fu - Progressive Point Matching]]
- [[Long-Horizon Credit Assignment]]
- [[Preston Fu]]
