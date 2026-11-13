---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-10-goodfire-neurons-interpretable-basis
source_title: "Neurons as an Interpretable Basis"
source_author: Curt Tigges, Matthew Kowal, Thomas McGrath, Owen Lewis, Nick Cammarata
source_url: https://www.goodfire.com/research/neurons-as-an-interpretable-basis
tags:
  - source/summary
  - interpretability
  - mechanistic-interpretability
  - mixture-of-experts
  - evaluation
source_ids:
  - src-2026-11-10-goodfire-neurons-interpretable-basis
status: active
---

# Neurons as an Interpretable Basis

## Summary

This is Goodfire's technical companion to [[Nick Cammarata - Neural Networks Are Already Clean]]. It
is also the first post in a series on "native interpretability", which means studying a network
through its own units rather than through a replacement model. Curt Tigges, Matthew Kowal, Thomas
McGrath, Owen Lewis and Nick Cammarata study the MLP neurons of **Qwen3.6-35B-A3B**, a
mixture-of-experts model, and argue that neurons have three properties that make them usable units:

- **They are functionally sparse.** Ablating the weakest **92.2%** of routed neuron activations on
  each forward pass costs "a 2.9% increase in language model loss".
- **Most neuron poles have few modes.** A pole usually has one computational mode, or one mode that
  does nearly all of the causal work.
- **Agent-written descriptions can be tested.** They are good enough to detect, classify, simulate
  and deliberately drive the neuron's firings.

The work is large and carefully controlled, but it is first-party and built mainly on one model,
and LLMs build and judge most of the measurements. Reasoning benchmarks fall under sparsity until
the model is fine-tuned, and the trained comparison is against the untrained base, not against an
equally trained model.

## Key claims

### The unit and the model

- A neuron is the post-SiLU hidden unit of a SwiGLU MLP. Its activation is the SwiGLU output times
  the expert's router weight.
- Gated neurons are bipolar, so the unit of analysis is a neuron-*pole*. The signs of gate and up
  define four regimes:
  - Q1 (gate+, up+) and Q3 (gate−, up−) give positive activations.
  - Q2 and Q4 give negative activations.
- The model has **5.26 million** neurons (rounded elsewhere to "5 million") in 40 layers. Each layer
  has 256 experts of 512 neurons; the router picks 8 per token, plus one shared expert that is
  always active. The shared experts hold **20,480** neurons (about **0.4%**) and are left unablated
  in every experiment.

### Sparsity: the causal role sits in the activation tails

- **Layer top-320.** Each token keeps the 320 of **4,096** routed neurons with the largest
  |activation| × router weight, and the other **92.2%** are ablated. Loss rises from **1.886** to
  **1.940** (Δ **+0.054**).
- **Expert top-K.** Keeping the top 64 per expert (87.5% ablated) gives Δ **+0.066**; the top 32
  gives **+0.146**.
- **Controls collapse.** A random 64 per expert gives Δ **+2.328**, and the bottom 448 gives
  **+2.701**.
- The retained activations fall almost entirely in the **p97/3** band, meaning at or above a
  neuron's 97th percentile or at or below its 3rd.
- **Benchmarks.** Classic benchmarks stay near parity. Thinking benchmarks under a 4,096-token cap
  drop for untrained top-320: SuperGPQA **−13.0** and GPQA-Diamond **−11.1**.
- **Why reasoning drops.** Claude Opus 5.5 agents classified the rollouts. The sparsified model
  usually still mentions the correct answer, often as its last candidate, and then self-checks
  endlessly.
- **Recovery by fine-tuning.** Training under the mask used **100M** tokens in two stages:
  - **91M** tokens of SFT distillation over 1,000 steps, which recovered about **72%** of the
    SuperGPQA drop;
  - **9M** tokens of RL over 100 steps, which supplied **34KB** of reward information.

  After this, "SuperGPQA reached 45.4 against clean's 44.8". For scale, the authors note Qwen's
  **34T** pretraining tokens and say ShearedLLaMa and Minitron needed billions of tokens to recover.
  The same training did not repair random-64 or bottom-448, and the most-changed neurons kept their
  meanings.

### The double-negative (Q3) regime and reasoning length

- Q3 activations are about one-third of all neuron activations. Ablating them does less damage than
  ablating the gate-up regimes, with one exception.
- **The exception.** On 24 GSM8K problems, removing Q3 cut reasoning from **1,550** tokens on
  average to **176**.
- **Patching tests.** Patching *real* Q3 trajectories back in kept reasoning long in most runs:
  - time-reversed: **13/17**;
  - taken from another problem and reversed: **10/15**;
  - restored at a scattered 25% of positions: **9/17**;
  - restored as a contiguous 25% block: only **1/17**.
- The authors suggest Q3 works through "aggregate properties" of its activity. They leave the
  mechanism for future work.

### Even sparser circuits, transcoders and random baselines

- **RelP attribution.** A few thousand neurons, **0.2-0.8%** of active routed units, recover 90% of
  the logit margin. Random sets of the same size recover at most **0.02**.
- **Across a generation.** Over ten generated sequences, a median of **519 of 163,840** active
  neurons suffices when only the current token is ablated. Median KL is **0.019** nats when the
  whole text is ablated and **0.016** when only the current token is.
- **Transcoders.** Following Shabalin & Piotrowski (2026), "Many Transcoder Features Are Neurons in
  Disguise", the authors decompose transcoder features that do not align with a neuron. Using
  orthogonal matching pursuit, many turn out to be coalitions of co-firing neurons. Coalitions mostly
  mean what their neurons share: **60%** at 2 neurons and **64%** at 33-64.
- **Random directions.** Neurons behave differently from random directions in three ways:
  - **8** neurons recover as much expert or layer function as **128-256** random directions;
  - neurons are wired to specific readers, while random directions activate readers diffusely;
  - a neuron's meaning narrows as it fires more strongly, while a random direction stays mixed at
    every strength.

### Modes: few per pole, usually one dominant

- **Data and sample.** The authors ran **10B** tokens through the model and harvested examples for
  every neuron. A stratified **2,734** neurons (**5,468** poles) got 30,000 extra examples each.
- **Method.** Firings are clustered by their input attributions into subcircuits, a median of **19**
  per pole. Two Claude Opus 5.5 passes then group the subcircuits into semantic modes.
- **Counts.**
  - **2,556** poles (**47%**) have one mode, **2,673** have two or more, and **239** have no
    readable mode.
  - **69%** of poles are dominated by one mode, meaning it does at least 90% of the KL damage.
- **Among multi-mode poles:**
  - the median damage outside the main mode is **14%**, and **27%** have half or more outside it;
  - the most frequent mode takes a median **73%** of firings, and the second takes **16%**.
- **Reproducibility.** Three reruns on 219 poles agreed on one-mode versus multi-mode **96%** of the
  time (median adjusted Rand index **0.95**). Splitting the fitting documents in half recovered
  **68%** of subcircuits, against **1%** under a shuffled null.
- **How readers disambiguate.** Neuron L18_E219_N55 has two unrelated modes, oral surgery and marine
  environments, yet writes one output direction. Its downstream readers receive it through their
  up-projection while context "primers" drive their gate, so a reader fires only for its mode. The
  evidence is two circuit case studies.

### Descriptions tested four ways

The Neuron Scientist is an agent harness running Claude Fable 5.0 or 5.1, Opus 5.5, or GPT-6 Sol.
It gets 200 firing documents and iterates hypothesis, experiment and description against a metric
on training texts. All tests below are on held-out documents.

| Test | What is checked | Result |
| --- | --- | --- |
| Detection | Opus 5.5 picks the firing snippet from a pair (496 poles, chance 0.50) | **0.858** in the weakest band to **0.955** in the strongest. Across all bands: **0.914** against all distractors, **0.885** against same-expert distractors, **0.946** against random text (the abstract's "95%"). |
| Classification | Which mode explains a firing, macro-F1 across all bands | From inputs **0.968**; from readers **0.853**; from text alone (Jev) **0.707**; chance **0.290**. Text F1 falls from **0.856** at router rank 1 to **0.652** outside the recorded top 8. |
| Simulation | Jev predicts levels 0-9 per token from a description that Claude Sonnet 5.5 converts to JSON (486 poles) | An ideal 10-level reader recovers **96%** of the ablation damage. The simulator recovers **73%** of that ceiling (72.7%): **56%** at p99.9-99.99, **64%** at p99.99+, **76%** for the top 1,000 firings. |
| Input synthesis | An Opus 5.5 controller directs writer agents from the description | **120 of 128** poles exceeded their 10B-token corpus maximum, 22 of them only after final editing. Final best: median **1.06×**, range **0.46-1.55×**. |

- **Why simulation is hard.** Text features explain only about **14%** of the variance in firing
  size, against **59%** for the neuron's gate inputs. Giving the simulator a summary of input
  activity and attention at each token raises the restored share by about 10%.
- Jev is described as a "non-autoregressive decision model"; it is used here as a judge and
  simulator, not trained for the task.
- **Leakage checks.** About **2.6%** of firings repeat a context; removing them changes headline
  results by at most **0.002**. Short snippets give AUROC **0.927**, rising to **0.978** with 250
  preceding tokens.

### A counterexample examined in another model

- The authors examine "the most popular counterexample" to the essay: a Colorado neuron in
  **Qwen3-32B** (L55/N11703) that also fires on Tornado, a Python web framework. About **98.8%** of
  its causal effect comes from Colorado, mountain or place text.
- **The Tornado link is causally real.** Asked where Tornado was developed, Qwen3-32B gives
  Colorado **30%** and the correct California **0.7%**. Suppressing the neuron moves these to **1%**
  and **4.7%**.
- **Tornado is not one of many hidden jobs.** Over 100M tokens the neuron fired strongly **3,812**
  times, **98.5%** of them on places.
- **Possible origin.** The authors suspect Qwen3-32B was initialized by copying Qwen3-14B layers,
  because many neurons align semantically 24 layers apart.

### Releases

- A public neuron atlas with Neuron Scientist pages for the 2,734 stratified neurons.
- Low-effort labels for all 10 million neuron-poles. The starting labels came from an internal
  fine-tuned Qwen3-8B.

## Why it matters

- [[Mechanistic Interpretability]]: the essay's "native neurons first" position now has measured
  sparsity, mode counts, random-direction baselines and description tests behind it, all on a
  production-scale open MoE model.
- [[Interpretability Evaluation]]: each description test reports chance, a ceiling or a matched
  control, and the authors label their own near-ceiling reference. None of the tests is CHIVE's
  transcript-only comparison, so the vault's central open experiment remains open.
- [[Transformer Architecture]]: SwiGLU's gate × up product is shown doing work. A reader's gate
  acts as a context switch on an upstream neuron, and the double-negative regime affects reasoning
  length.
- [[Goodfire]], [[Qwen]], [[Mixture of Experts]] and [[Automated AI Research]]: the post shows
  routed-neuron sparsity measured with router weights, and agent labor at the scale of a population
  study.

## Tensions / open questions

- **First-party, mostly one model.** Almost everything is measured on Qwen3.6-35B-A3B, plus a
  Qwen3-32B case study. The authors list generalization across models and behaviors as open.
- **LLMs throughout the measurement.** Agents write the descriptions, Opus 5.5 builds the modes and
  judges detection, Jev classifies and simulates, and Sonnet 5.5 formats descriptions. The authors
  say mode counts "are not *definitive*" because they depend on the granularity of the descriptions.
- **Parity is against the untrained base.** The "Full model RL v1" control ran the same recipe with
  no mask and also gained: SuperGPQA **+5.1** and GPQA-Diamond **+9.1**. Top-320 RL v1 gained
  **+0.2** and **+2.0**. Against an equally trained full model, the sparse model trails.
- **A figure mismatch.** The prose gives 45.4 against 44.8 (**+0.6**), but the table's Top-320 RL v1
  column shows **+0.2** on SuperGPQA. The +0.6 appears in the reference Top-64 RL v1 column.
- **Reasoning results depend on the token cap.** The thinking panel counts capped traces as wrong
  at 4,096 tokens. In the second panel "the base model finished no AIME item at the 16k cap" (base
  **0.0**), so the ablated models' AIME gains (**+11.7**) partly reflect finishing at all.
- **What the tests can and cannot show.** Input-based classification scores modes on the features
  they were clustered from; the authors call it "a near-ceiling reference rather than an independent
  test". Input synthesis gives the controller activation feedback, so it is not description-only.
  The abstract's "fire more strongly than anything observed" holds for 120 of 128 poles, not all.
- **Two unrelated 73% figures.** The simulator recovers 73% of the ceiling, and, separately, the
  bands from p99.9 up account for 73% of neuron damage.
- **Not yet explained.** Weak and Q3 activations, the disambiguation mechanism's prevalence beyond
  its case studies, and neurons whose main readers are attention layers, which were "initially quite
  difficult to interpret". The roughly **5%** of Colorado and Tornado circuit firings that look
  unrelated was revised down from **10-16%**. The authors think it is "probably higher than the true
  amount" and treat it as highly uncertain.
- **Not the same metric as the essay.** The essay's preliminary Qwen3-32B figure (about **90%** of
  poles with one main job) and this post's **69%** damage-dominated poles come from different models
  and measures. They should not be read as one estimate revised.
- **Unmeasured scaling claim.** The conclusion says scaling agent-driven investigation "reliably
  improves our explanations". The capture gives no compute-versus-quality curve for this.

## Affected pages

- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Goodfire]]
- [[Transformer Architecture]]
- [[Qwen]]
- [[Mixture of Experts]]
- [[Automated AI Research]]

## Raw capture

- [[knowledge-base/raw/sources/Neurons as an Interpretable Basis]]

## Citations

- Canonical URL: https://www.goodfire.com/research/neurons-as-an-interpretable-basis
- Byline: Curt Tigges, Matthew Kowal, Thomas McGrath, Owen Lewis, Nick Cammarata
- Published: 2026-11-10; captured: 2026-11-12
- Publisher: Goodfire research site. Companion to "Neural Networks Are Already Clean"
  (already-clean.goodfire.com).
- The capture contains very large inline interactive SVG figures. This summary uses the prose,
  tables and figure captions and their accessible text, not the SVG geometry.

## Related pages

- [[Nick Cammarata - Neural Networks Are Already Clean]]
- [[Goodfire]]
- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Transformer Architecture]]
- [[Mixture of Experts]]
- [[Qwen]]
- [[Automated AI Research]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[DoubleAI - Can LLMs Redesign Themselves as They Train]]
- [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]]
- [[Typed Probabilistic Decision Models]]
