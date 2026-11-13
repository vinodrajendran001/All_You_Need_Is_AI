---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-06-doubleai-llms-redesign-themselves
source_title: "Can LLMs redesign themselves as they train?"
source_author: Unattributed in capture
source_url: https://www.doubleai.com/research/can-llms-redesign-themselves-as-they-train
tags:
  - source/summary
  - automated-research
  - architecture
  - self-improvement
  - interpretability
source_ids:
  - src-2026-11-06-doubleai-llms-redesign-themselves
status: active
---

# Can LLMs Redesign Themselves as They Train?

## Summary

A research blog post from DoubleAI (no individual byline in the capture) proposes putting a coding
agent inside a network's training run. Ordinarily only the weights change during training. Here the
agent reads the network's internals and changes "the data, the objective, the update rule or the
architecture itself". The authors call this **mechanistic intervention**: it uses interpretability-style
tools, but on a network that is still learning.

The main edit is a **code layer**, a small program inserted behind a gate initialized at zero so
that the network is unchanged at the moment of insertion. Four early experiments are reported:

- three code layers lower validation loss on nanochat;
- a lookup layer inserted midway recalls more than the same layer present from the start;
- ten code layers raise CLRS-Text algorithm accuracy from **55%** to **84%**;
- two closed-loop cases: DeepSeek-V4.1-Flash raises its own contest score from **64%** to **71%**,
  and Qwen3-8B from **59%** to **66%**.

The results are first-party and report no seeds or error bars, and the agent model is unnamed. The
two "self" improvements change how answers are sampled and accepted, not the model's weights or
architecture.

## Key claims

### Mechanistic intervention and code layers

- **Why code.** Gradient descent "settles for whatever lowers the loss fastest", often through
  shortcuts. Programs "apply the same rule to every input, seen or unseen, so they generalise by
  construction". The authors appeal to minimum description length.
- **How a layer enters.** It is added behind a learnable scalar gate `g` initialized to zero. "At
  the moment of insertion the network is exactly identical to what it was." If the layer helps, the
  gradient opens the gate "within about 100 steps".
- **Lineage.** The post places itself after agents that run research end to end, tune training code
  overnight (karpathy/autoresearch), rewrite update rules (Bai et al., 2026), and edit weights
  directly (Takehi et al., 2026).

### The phantom gradient

- **Definition.** The phantom gradient at layer ℓ is ∂L/∂h_ℓ: the loss gradient with respect to the
  residual stream rather than the weights, a `[B, T, D]` "demand map". The name comes from the
  gradient that imaginary per-token, zero-initialized weights would receive.
- **The agent's role.** It is described as "the first mechanistic intervention tool discovered by
  the agent". The agents also found that it "misleads" unless centred, by subtracting the mean over
  documents that share the same correct next token.
- **When to intervene.** Demand that persists in a layer across checkpoints marks what gradient
  descent is not satisfying, and triggers an insertion there.
- **One recipe, from the CLRS-Text runs:**
  1. Grade every task and input size, and target the cells whose error stays high and flat.
  2. Backpropagate each wrong token's loss on its own.
  3. Cluster the wrong tokens on [phantom gradient, hidden state] with spherical k-means. The
     clusters are stable when the clustering is repeated on half the tokens.
  4. Fit candidate code layers to point along the centred phantom gradient.
  5. Score candidates on held-out documents against a plain linear-map baseline.
- **Limits and controls.**
  - The phantom gradient "does not predict reliably" how a candidate will perform once trained, so
    ordinary training makes the final call.
  - Each candidate races a *twin*: the same run with the layer switched off.
  - It also races *shams*, which keep the layer's shape and parameters but scramble its
    information.
  - If a sham does almost as well, the gain came from capacity alone and the candidate is dropped.
  - Each layer must first pass a causality check: scrambling later tokens must not change anything
    the layer computes up to that position.

### The four training experiments

- **nanochat.** A twelve-layer transformer of about **286M** parameters, with context extended to
  16K tokens and code mixed into the data. The agent inserted three code layers, and validation loss
  dropped after each. The gap "persists to the end of training, at step 5,000". The prose gives no
  loss values. One layer "computes gradients of hidden representations within a single forward
  pass" and uses them to self-correct.
- **Sliding-window attention ("Evolution is mandatory").**
  - Setup: a **124M**-parameter model trained on 8K-token documents, with attention limited to the
    last **500** tokens.
  - The agent added a parameter-free exact-match lookup into every attention head.
  - Recall of a variable defined **600-4,000** tokens earlier was **72%** when the layer was
    inserted halfway (step 1,200) and **55%** when it was present from the start, despite
    "near-identical loss curves".
  - The authors "believe" this is shortcut learning: present from the start, the network leans on
    the layer instead of building its own circuits.
- **CLRS-Text (jaggedness).**
  - Setup: thirty classical algorithms, and a twelve-layer, **86M**-parameter transformer.
  - Plain training plateaus at **55%** after 20 thousand steps, and twice as many steps plateaus
    similarly.
  - With **ten** code layers inserted along the way, the run reaches **84%**.
  - At input sizes between those seen in training, accuracy rises from "only a third" to **79%**.
  - The agent, "powered by a frontier model, already knows how to solve the tasks". It used linear
    probes to find which layer holds the input values that a code layer should read.

### Closing the loop on a model's own states

- **DeepSeek-V4.1-Flash on itself.**
  - Setup: a **763B** mixture-of-experts model acting as the agent on itself, answering without
    thinking mode. The test sets were AIME 2026 and HMMT February 2026 from MathArena, hidden
    throughout.
  - Accuracy rose from **64%** to **71%**.
  - The "code layer" is a linear probe on the residual stream at seven deep blocks, read when a
    solution ends. If the probe predicts a wrong answer, the solution is discarded and resampled, up
    to three times.
  - DeepSeek built the probe from its own graded solutions to **243** problems from the 2024 and
    2025 contests, choosing the blocks, the probe's form and the threshold itself. A single linear
    readout did as well as a small neural network. It predicted a gain of about eight points, and the hidden contests gave seven.
  - The probe rejects "four in five" wrong answers and "one right answer in fifteen". Restarting the
    longest solutions instead gains "less than two points".
  - Probed midway through a solution, the hidden states "mostly encode how hard the problem is".
    That probe could not tell a failing attempt from a successful one at the same problem.
- **Qwen3-8B.**
  - Setup: thinking on. A frontier agent had already built probes on Qwen's hidden state: a stop
    probe, a doom probe and three local probes.
  - Qwen then wrote its own Python policy for when to stop, restart and accept, with no gradient
    training.
  - The policy came from a search over about **15,000** policies, each scored on about **800** older
    problems. The ingredient that "turned out to matter most" was having Qwen write analysis code over
    its graded attempts before writing each policy.
  - Accuracy rose from **59%** to **66%**.
  - Pooled over **63** problems, the policy gains **7.0** points over baseline and **3.3** over a
    length-only rule. It uses **2.8×** the thinking tokens of a single attempt, against **1.8×** for
    the length-only rule.

### Looking ahead

The authors sketch five directions:

- **Alignment through code.** Weights are opaque, but "Code, on the other hand, is readable by
  humans", so computation moved into code "becomes far easier to align".
- **Mechanistic intervention.** The authors concede "The tools we have are still noisy": the phantom
  gradient "is better at showing *where* a network needs help than *what* it needs".
- **Performance engineering.** Code layers need fast GPU kernels too. The post links this to
  DoubleAI's own Maxwell kernel posts.
- **Going beyond transformers.** A fixed architecture is the paradigm the authors say their
  results "challenge".
- **Recursive self-improvement** through self-referential meta-learning (Kirsch and Schmidhuber,
  2022). A model improving both how it trains and its tools "is on a direct path to recursive
  self-improvement".

The TL;DR says "We are on the cusp of models that train and re-architect themselves".

## Why it matters

- [[Mechanistic Interpretability]]: the post turns interpretability tools (linear probes, gradients
  with respect to activations, clustering of failures) into tools for editing a network during
  training. It claims this gives interpretability "an objective test. An intervention either
  improves the metric or it doesn't".
- [[Interpretability Evaluation]]: the DeepSeek probe is checked against a trivial length-only
  baseline and a prediction made before the hidden test. The post also admits its main diagnostic
  does not predict how a candidate will perform once trained.
- [[Neural Network Fundamentals]]: the post uses gradients with respect to activations, inserts
  layers with an identity-preserving zero gate, and reports that the timing of an insertion changes
  what the network learns.
- [[Transformer Architecture]]: the architecture becomes a variable during training rather than a
  fixed blueprint. Parameter-free lookups and exact programs are added beside attention and MLPs.
- [[Automated AI Research]], [[Recursive Self-Improvement]], [[LLM Training Pipeline]],
  [[Test-Time Scaling]], [[Qwen]] and [[DeepSeek]]: the post adds an agent inside the training loop,
  models acting on their own activations, and probe-gated resampling as a test-time method.

## Tensions / open questions

- **Unattributed and first-party.** The capture names no author. It is DoubleAI describing its own
  method, in a blog rather than a peer-reviewed paper, and it calls the results "early signs".
- **Missing statistics.** No seeds, error bars or repeat runs are reported. nanochat's loss gains
  appear only in a figure. The SWA timing result is a single 72% versus 55% comparison.
- **Unnamed agent, unreported cost.** The agent is "powered by a frontier model" but never named,
  and agent compute is not reported. For CLRS-Text the agent "already knows how to solve the tasks",
  so the gains partly import known algorithms as exact code.
- **The "self-improvement" changes sampling, not the model.** DeepSeek's code layer is a learned
  verifier gating up to three resamples. It is closer to verifier-based best-of-n sampling than to a
  change of weights or architecture, and the extra sampling cost is not reported.
- **Qwen's gain depends on another agent's tools.** Qwen's probes were built by a frontier agent.
  Qwen wrote only the policy, selected from about 15,000 candidates on about 800 problems. The test
  set stayed hidden, but if each of the 63 pooled problems is scored once, a 7.0-point gain is about
  four or five problems (vault arithmetic; the post does not say how many runs were pooled). The
  policy also used **2.8×** the thinking tokens of a single attempt.
- **Is the phantom gradient new?** It is the ordinary gradient of the loss with respect to
  activations. What is new here is how it is used (centring, per-token backpropagation,
  clustering), not the quantity. The post does not compare it with existing gradient-attribution
  methods. Its footnote separates the name from Geng et al.'s (2021) "phantom gradients".
- **Aspirational framing.** "On the cusp", "a direct path to recursive self-improvement" and
  "alignment through code" are aims. None is tested in the experiments.
- **Chart values omitted.** A Qwen results chart survives only as alt text. This summary uses only
  values that also appear in the prose.

## Affected pages

- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]
- [[Automated AI Research]]
- [[Recursive Self-Improvement]]
- [[LLM Training Pipeline]]
- [[Test-Time Scaling]]
- [[Qwen]]
- [[DeepSeek]]

## Raw capture

- [[knowledge-base/raw/sources/Can LLMs redesign themselves as they train]]

## Citations

- Canonical URL: https://www.doubleai.com/research/can-llms-redesign-themselves-as-they-train
- Byline: none in the capture; `source_author` is recorded as "Unattributed in capture".
- Publisher: DoubleAI (doubleai.com research blog, "Blog", 23 min read)
- Published: 2026-11-06; captured: 2026-11-10

## Related pages

- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]]
- [[Curt Tigges et al - Neurons as an Interpretable Basis]]
- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Automated AI Research]]
- [[Recursive Self-Improvement]]
- [[LLM Training Pipeline]]
- [[Test-Time Scaling]]
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]
- [[Qwen]]
- [[DeepSeek]]
- [[Andrej Karpathy]]
- [[Zvi Mowshowitz - AI R&D Is Accelerating Towards Potential RSI in 2027]]
- [[Ethan Mollick - Fable 5.2 and Jagged AGI]]
- [[James Tillman - Two Kinds of Test-Time Scaling]]
