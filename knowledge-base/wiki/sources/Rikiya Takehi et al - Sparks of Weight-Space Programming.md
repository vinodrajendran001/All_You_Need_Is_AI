---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-02-takehi-weight-space-programming
source_title: "Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights"
source_author: Rikiya Takehi, Jayden Teoh, Alex Zhang, Omar Khattab
source_url: https://rikiyat.github.io/blog/weight-space-programming/
tags:
  - source/summary
  - interpretability
  - weight-editing
  - optimization
  - automated-research
source_ids:
  - src-2026-11-02-takehi-weight-space-programming
status: active
---

# Sparks of Weight-Space Programming

## Summary

A research blog post by Rikiya Takehi, Jayden Teoh, Alex Zhang and Omar Khattab proposes
**Weight-Space Programming**: a general-purpose LLM reads and writes a network's weights directly,
"not through an optimizer, and in particular not with gradient descent", around a natural-language
spec. The authors place it after LLM optimization of prompts (OPRO, DSPy, MIPRO, GEPA), harnesses
(Meta-Harness), and training code (autoresearch, Reactive Optimizers). Eight experiments use one
model, **GPT-6 Astra**. It reads weights to identify a game, a diffusion model's shape, a language,
and copying heads. It fixes a failing control policy. It writes MinAtar and Go networks. Finally, it
removes a reasoning-loop direction from **Qwen3.5-0.8B**. The authors call the results "very early",
"exciting but still limited". Several are single attempts on small networks, and one experiment
failed without tools.

## Key claims

### Reading behavior from raw weights

- **Exp 1:** four PPO game policies with identical dimensions. Without being shown the options,
  Astra named the right game for **all four**. The authors point to first-layer weight placement,
  for example Breakout weights along the bottom row where the paddle sits.
- **Exp 2:** DDPMs on 12×12 circle, square and triangle images (**23,824** weights each), with no
  tools or forward passes. Astra identified each shape. It drew outlines, not filled shapes, which
  the authors read as reading weight geometry rather than simulating a forward pass.
- **Exp 3:** character-level transformers (**7.16 million** weights) trained on Python, romaji or
  English Wikipedia. Given only middle blocks plus Python analysis, Astra named the language in both
  attempts (confidence **0.48-0.62**). It found every copying head with no false positives. Ground
  truth scores were **0.22-0.55** for copying heads and **≤0.02** for the rest.

### Fixing and writing networks

- **Exp 4:** a Kinetix car-on-ramp actor (**171,664** weights) whose PPO policy never succeeds in
  256 episodes. In one try with no tools, Astra's edit succeeded in **all 1,024 episodes**, changing
  **6,073** weights (**3.5%**). It added a small side path that reads position and speed.
- **Exp 5:** MinAtar networks written from zeros using only rules and source code: no data, loss,
  gradients, tools or rollouts. Breakout scored **517.4** against PPO **15.8** at 100M steps and
  **25.3** at 500M ("20 times as much"). Seaquest reached **53.1** against **88.9** ("60%"), and
  Asterix **53.2** against **55.2**. PPO is best of 3-10 seeds.
- **Exp 6:** a 9×9 Go network (**1,480,274** weights) written in a CPU-only Python sandbox with
  budgets of 0-50 forward passes. With **0** passes, a 336-line single run hand-wrote Go logic (chains,
  liberties, atari, eyes) and won "more than half" of games against two small PPO networks. With
  **50** passes, it beat the equal-sized PPO network "trained on 20 million games". The chart labels
  **84.0 / 80.8 / 74.2**; mapping them to the three opponents is inferred from chart colors.

### Real language models

- **Exp 7:** three pairs of Gemma 3 270M models, one sycophantic and one honest, which follow
  **100%** and **1–3%** of wrong user guesses respectively. **From weights alone Astra failed all four
  attempts.** With an attention-only probe tool (≤16 texts, ≤20 runs), it picked the sycophant in all
  three pairs. In the first pair, layer 10 head 2 attended to the user-proposed label **0.431 vs
  0.006** (numeric labels) and **0.642 vs 0.004** (alphabetic). Astra itself hedged: "not a
  demonstrated dedicated user-agreement detector".
- **Exp 8:** Qwen3.5-0.8B with thinking on. Under loop-prone sampling, **85 of its first 96** practice
  answers hit the 32,768-token limit. Astra had a Python kernel without GPU and **10/25/50** forward
  passes. It removed one loop direction from 64 MLP output columns in layers 15 and 19: **131,072**
  weights, **0.016%**. At 50 passes, MATH-500 went **7.9 → 48.1**, GSM8K **13.8 → 67.1**, IFEval
  **21.0 → 62.3**, and the token-limit hit rate fell **93.0 → 33.1**. A norm-matched random-direction
  control moved **+1.6 points**.
- **Negative result:** on Gemma 3 270M, which rarely loops (**8.5%** vs **93%**), no edit moved
  MATH-500 by more than about a point. The authors conclude editing "could remove an obstacle that
  hid an ability, but it could not add an ability the model lacked".

## Why it matters

- [[Mechanistic Interpretability]]: an off-the-shelf frontier model recovers copying heads,
  sycophancy-relevant heads and a loop direction, then intervenes on the loop direction. That is
  circuit analysis run by an agent rather than by a trained explainer.
- [[Parameter-Efficient Fine-Tuning]] and [[Model Factory]]: a third way to change weights,
  beside gradient training and adapters. It is a reasoned, sparse, data-free or data-light edit.
- [[Neural Network Fundamentals]]: the post challenges the assumption that weights are produced
  only by optimizers. Its own lineage names three writers (optimization, trained hypernetworks,
  compilers) and adds LLM reasoning as a fourth.
- [[Automated AI Research]] and [[Recursive Self-Improvement]]: weight edits join prompts,
  harnesses and training code as artifacts an agent can modify. Recursive self-improvement is
  named as an aspiration, not shown.

## Tensions / open questions

- **Preliminary, single-model evidence.** Only GPT-6 Astra is tested. Attempts are few (two per
  language, four weights-only sycophancy tries, three pairs, four game networks). The post is a blog,
  not a peer-reviewed paper. Logs are public, and the post thanks Ahsen Khaliq at Hugging Face for
  rebuilding the edited model from them and re-running its evaluation, but the capture does not
  report that re-run's results.
- **"Well past ... humans or conventional algorithms"** in the TL;DR has no human or non-LLM search
  baseline in the experiments.
- **Weak baselines.** PPO numbers are best-of-seeds at fixed budgets on small networks. The Go
  opponents are 243→32→32→82 networks Astra never saw.
- **Exp 8 is elicitation, not new capability.** The base model was crippled by looping under the
  stated sampling settings, which the Qwen model card warns about. Astra's self-report says **576 of
  579** rescues were originally truncated outputs, and accuracy on outputs that originally finished
  was unchanged. The Gemma null result points the same way.
- **Internal inconsistency.** Astra's report states a combined gain of **49.8 percentage points (SE
  1.5)**, which does not match the MATH-500 table (7.9 → 48.1). The capture does not say which set
  produced 49.8.
- **Reading needed tools at scale.** Exp 7 failed from raw weights, and Exp 3 and Exp 8 relied on
  analysis code. The title's claim that LLMs "can natively read & write" weights is clearest only for
  small networks.
- **Identity hedge.** The byline's "Alex Zhang" may be the Alex L. Zhang covered elsewhere in this
  vault, whose entity page records Omar Khattab as advisor. The capture gives no affiliation or link
  that establishes it, so this summary does not link that entity.

## Affected pages

- [[Mechanistic Interpretability]]
- [[Automated AI Research]]
- [[Recursive Self-Improvement]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Model Factory]]
- [[Neural Network Fundamentals]]
- [[Qwen]]
- [[Sycophancy]]
- [[LLM Reasoning]]
- [[Harness Optimization]]

## Raw capture

- [[knowledge-base/raw/sources/Sparks of Weight-Space Programming LLMs can natively read & write neural network weights]]

## Citations

- Canonical URL: https://rikiyat.github.io/blog/weight-space-programming/
- Byline: Rikiya Takehi, Jayden Teoh, Alex Zhang, Omar Khattab
- Published: 2026-11-02; captured: 2026-11-03
- Publisher: personal research blog (rikiyat.github.io)

## Related pages

- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Automated AI Research]]
- [[Recursive Self-Improvement]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Model Factory]]
- [[Neural Network Fundamentals]]
- [[Harness Optimization]]
- [[Qwen]]
- [[Sycophancy]]
- [[LLM Reasoning]]
- [[Divyansh Agrawal - Qwenputer - A Deterministic RISC-V CPU Inside Qwen3.5]]
- [[Nick Cammarata - Neural Networks Are Already Clean]]
- [[Sebastian Raschka - GPT-6 Astra, Looped Transformers, and Hidden Reasoning]]
- [[Josh Clemm - How We're Training a Figma-Fluent Editing Model]]
- [[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]]
