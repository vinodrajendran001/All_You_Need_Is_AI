---
type: concept
created: 2026-10-19
updated: 2026-11-13
tags:
  - concept
  - interpretability
  - mechanistic-interpretability
  - alignment
source_ids:
  - src-2026-10-19-cammarata-networks-already-clean
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-11-02-takehi-weight-space-programming
  - src-2026-11-10-goodfire-neurons-interpretable-basis
  - src-2026-11-03-willison-qwen-interprets-weights
  - src-2026-11-06-doubleai-llms-redesign-themselves
status: active
---

# Mechanistic Interpretability

## Definition

Mechanistic interpretability explains a trained network's behavior through its internal
computation. It works with the network's units (neurons, attention heads, or learned dictionary
features), the circuits that connect them, and interventions that test whether an explanation is
right. By contrast, behavioral evaluation infers what a model does from inputs and outputs alone.

## Why it matters

Claims about what a model represents, intends, or uses now appear in safety analyses and system
cards. The vault holds evidence pulling in two directions.
[[Anthropic - Would This Change Your Answer (CHIVE)]] found that several activation-reading tools
did not help predict behavior better than reading the transcript.
[[Nick Cammarata - Neural Networks Are Already Clean]] argues that a network's own neurons are far
more legible than the field assumed, and that replacement models can make it look messier than it
is. Both bear on whether looking inside a model yields evidence beyond what its outputs already
show.

## Current synthesis

### Choosing the unit of analysis is the first methodological decision

| Unit | What it is | Vault evidence and limits |
| --- | --- | --- |
| Native neurons, heads, circuits | The model's own mechanisms; no reconstruction loss | Cammarata reports preliminary Qwen3-32B audits with about **90%** of neuron poles having one main job. Threshold-dependent, first-party, agent-assisted. The companion paper measures a different model and metric: on Qwen3.6-35B-A3B, **69%** of poles are dominated by one mode and **47%** have exactly one. |
| Sparse dictionaries (SAEs) | A second model trained to re-express activations as sparse features | CHIVE: no uplift over the transcript at counterfactual prediction. Cammarata: on vision models, mostly near-copies of neurons or compositions of them. |
| Transcoders and replacement graphs | Substitute layers that make circuits traceable | Cammarata says Anthropic's largest transcoder predicts the original's next word "only half the time" and needs error nodes; this is a competitor's characterization. |
| Probes | Readers trained to answer a question chosen in advance | Can detect without the model using what they detect: Cammarata's Social Security probe. |
| Activation oracles, natural-language autoencoders, meta-models | Models that read another model's activations and describe them | CHIVE: no uplift for the oracle and autoencoder variants it tested. Cammarata suggests meta-models may be a top-level map whose directions still need mechanism checks. |

The disagreement is about order, not simply whether to use dictionaries. Cammarata puts probes and
dictionaries "at the end, not the start". His argument: if the native mechanisms are already
organized, replacing them can split generalizations that are not yet understood. For example, an
SAE splits the V-shape neuron into a car feature and a cat feature. The superposition-first
programme reached the opposite conclusion from the same starting difficulty: if neurons pack
unrelated things, they must be unpacked first. The vault has no independent study deciding
between the two.

"Probe" also carries an unrelated sense elsewhere in the vault. In
[[Joint-Embedding Predictive Architecture]], a linear or k-NN probe measures how useful a
representation is for a downstream task, not how the network computes. Both senses share the
limit Cammarata points to: a probe answers only the question it was built to ask.

### Why a neuron looks polysemantic is the contested question

Cammarata lists five candidate causes for an apparently multi-meaning neuron: bad tools, bad
explanations, bad learning, recursive generalization, and superposition. Only the last is a
different learning principle: packing unrelated things together because they rarely interfere.
The others can each be tested. A better tool either resolves the neuron or it does not; retraining
with a better architecture shows whether learning was at fault; and a branch can be watched as it
grows over training checkpoints. In his account, superposition's only symptom is that something
does not make sense, so he places it last rather than treating it as the default.

The vault should keep the word's meanings apart rather than settle them:

- **Arbitrary packing** (Cammarata's target): unrelated things share a neuron because they rarely
  collide.
- **More features than dimensions** (the Toy Models definition): satisfied by any composing
  network, and treated by Cammarata as expected rather than bad news.
- **Distributed computation too large to understand**: a real difficulty, but a different one.

Cammarata quotes Anthropic's 2022 Softmax Linear Units paper: superposition "is often treated as
the default hypothesis simply because it seems intuitively more compelling than other
explanations, but there is little evidence." The quote does not settle the question either way. It
shows that the default was openly acknowledged as weakly evidenced.

### Detection, description, use, and prediction are four different claims

Two independent sources converge on a ladder that interpretability claims are prone to skip:

1. **Detection:** a reader can tell when a property is present.
2. **Description:** a unit has a label that fits its top activations.
3. **Use:** intervening on the unit changes the behavior.
4. **Predictive value:** the explanation predicts counterfactual behavior better than a simpler
   reference condition.

Cammarata's examples break the ladder at step 3. The three-neuron Social Security probe detects the
phrase with held-out **AUC 1.00**, yet removing those neurons changes next-token log-probability by
only **-0.004 nats** on average. In the Santa graph, removing twenty neurons *labeled* Christmas or
Santa leaves Santa at **76%**, while removing eight neurons whose negative pole encodes Santa drops
it to **6%**. [[Anthropic - Would This Change Your Answer (CHIVE)]] breaks the ladder at step 4. Its
tool outputs described the feature and the behavior, but rarely the causal relation between them,
and gave no uplift over the transcript-only baseline.

Neither source tests native neurons in CHIVE's protocol. Cammarata's ablations establish use for
specific units, not whether a neuron-level reading would beat a transcript reader at predicting
counterfactual behavior. That comparison is the clearest open experiment on this page.

### Explanations need tests that can lose

Cammarata's positive controls are specific enough to fail. In the near-miss test, an agent that
sees only a neuron's explanation writes five examples that should fire it and five near misses that
should not. Across 183 positive-side explanations, the examples fired strongly **76%** of the time
against **11%** for near misses. In the blind-maximum test, a sentence written from the explanation
alone can out-activate the best of 10 billion corpus tokens. He also criticizes simulation scores
for rewarding attention placement and weak-activation detail rather than a neuron's job.

These tests have stated limits: near misses probe a branch's boundary, not packing, so
distant-concept controls are added. They resemble the discipline
[[Benchmark Optimization]] records for evaluation generally: a measurement counts as evidence when
something independent could have falsified it. Behavioral proxies need the same care.
[[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]] treats identity
self-reports as behavioral measurements rather than access to an internal belief.

### The companion paper puts numbers on neurons as units

[[Curt Tigges et al - Neurons as an Interpretable Basis]] is the technical companion that the essay
announced. It tests three properties on the routed MLP neurons of Qwen3.6-35B-A3B, a
mixture-of-experts model:

- **Sparsity.** Keeping only the top 320 of **4,096** routed neurons per token, ranked by
  |activation| × router weight, ablates **92.2%** of them and raises loss from **1.886** to
  **1.940**. In the per-expert version, keeping the top 64 raises loss by **0.066**, while a random
  64 raises it by **2.328** and the bottom 448 by **2.701**.
- **Few modes.** **69%** of neuron poles are dominated by one mode (at least 90% of the KL
  damage), and **47%** have only one. Multi-mode poles are common, though. The paper's worked
  example is one neuron with two unrelated modes, oral surgery and marine environments. Its
  downstream readers take it in through their up-projection while context "primers" drive their
  gate, so each set of readers fires only for its own mode.
- **Testable descriptions.** Agent-written descriptions are scored on held-out text: detection
  **0.914**; text-only mode classification **0.707** against chance **0.290**; simulation
  recovering **73%** of an ideal reader's ceiling; and synthesized inputs beating the corpus maximum
  for **120 of 128** poles.

The paper also compares neurons with random directions: **8** neurons recover as much expert or
layer function as **128-256** random directions. If neurons were not a privileged basis, random
directions should have done about as well.
It re-examines the most cited counterexample, a Qwen3-32B Colorado neuron that also fires on the
Tornado web framework. The Tornado link is causally real: suppressing the neuron moves the model's
"where was Tornado developed" answer away from Colorado. But **98.5%** of the neuron's strong
firings are on places. The authors suspect the link comes from copying Qwen3-14B layers at
initialization. Read against Cammarata's five causes, that would make it a training artifact
rather than packing. That reading is the vault's, not the authors'.

On the ladder above, the paper covers detection, description and use (through ablation damage). It
still does not run step 4 against a transcript reader. The work is first-party and mostly on one
model. LLMs write the descriptions, build the modes and judge most of the tests.

### Architecture and tools can manufacture or remove apparent mess

Several apparent signs of entanglement in Cammarata's account turned out to come from the
instrument or the architecture:

- Deep-layer **feature visualization was reward hacked** into dogs. Steering it toward the routes
  real images take revealed shared-pose and car neurons.
- **InceptionV1 lacked a residual stream.** In a same-size ConvNeXt with residual connections and
  LayerNorm, about **99%** of last-layer neurons became legible.
- **SwiGLU's double-negative regime** puts a sign-flipped leak at the top of about **4%** of
  neurons' activation lists. The companion paper measures that regime (Q3) differently, as about
  one third of all activations. Removing it cut GSM8K reasoning from **1,550** tokens on average
  to **176**. The two figures are different measures and should not be merged.
- An **unread high-mass residual coordinate** working with LayerNorm hid the structure of ConvNeXt
  residual-stream maps.
- **Percentile thresholds** flatten the difference between dial-like and detector-like neurons.

The architectural side is developed on [[Transformer Architecture]] and [[Mixture of Experts]]. On
the latter, routed experts are presented as narrow and as structurally hostile to arbitrary packing.

### Reading computation is not reading stated intent

[[Chain-of-Thought Monitoring]] reads what a model wrote; mechanistic interpretability reads what
it computed. The vault's evidence keeps the two complementary rather than ranked.
[[Akhil Arora et al - Current Advances in LLM Reasoning]] proposes mechanistic interpretability as
the better lens because reasoning traces can be unfaithful. CHIVE's tested activation readers did
not beat the transcript. [[OpenAI - The Hugging Face Incident and the Road Ahead]] describes
reasoning text legible enough to classify by severity.

Cammarata adds an argument rather than a measurement. A deceptive computation still has to be
readable by the model's downstream circuitry, so a sufficiently good reader of that circuitry
should see it. That is a hypothesis about what internals could reveal, not evidence that current
tools reveal it.

### Agents now supply much of the labor

Cammarata's programme runs on agent labor. Agents write neuron explanations, generate controls,
group neurons and experts, and review **100,000** attribution graphs. This places interpretability
inside [[Automated AI Research]]: execution scales, while choosing which questions and motifs
matter remains the scarce judgment. It also adds a validation burden. Agent-written labels and
agent-judged groupings are part of the measurement, and the essay reports that agents bring their
own default reading of contested terms such as "superposition".

The companion paper scales this up. Its Neuron Scientist harness iterates hypotheses and
experiments for each neuron, and the release includes pages for **2,734** stratified neurons plus
low-effort labels for all 10 million neuron-poles. LLM judges score the descriptions, so a
description's quality is measured partly by other models.

### A frontier model as reader and editor of weights

[[Rikiya Takehi et al - Sparks of Weight-Space Programming]] hands raw weights to an off-the-shelf
frontier model, GPT-6 Astra, instead of a trained explainer or a human analyst. On small
character-level transformers, its own Python analysis found every copying head with no false
positives. It multiplied weight matrices to link a look-back head to later search heads, and the
authors note that this matches a method from Elhage et al. On three Gemma 3 270M sycophant/honest
pairs it **failed in all four attempts from weights alone**. It picked the sycophant in all three
pairs once it could probe attention on texts it wrote. On Qwen3.5-0.8B it localized a
reasoning-loop direction in the MLPs of layers 15 and 19 and subtracted it from **131,072**
weights. A norm-matched random-direction control moved only **+1.6 points**.

This extends Cammarata's agent-labor point in one direction and qualifies it in another. The
reader can now also be the intervener, and an edit that changes behavior while a matched random
edit does not is stronger evidence than a label alone. But the post is a single-model,
few-attempt blog, not a paper. The language-model results needed tools, and Astra's own
conclusion on the sycophancy heads was "not a demonstrated dedicated user-agreement detector".
Reading weights without tools is shown only on small networks. Whether such readings beat a
behavior-only baseline, the test [[Interpretability Evaluation]] asks for, was not run.

A third party has since rerun the no-tools game prompts. In
[[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]], Qwen 3.8 27B,
running locally on a laptop, named three of the four games (Pac-Man, Pong and Breakout) and mistook
Freeway for a Pac-Man-like game. Each answer with a reported time took 46 minutes to over an hour.
Kimi K3.1 Pro named Breakout. This suggests the small-network task does not need a frontier model.
But it is one run per game, the stated confidences are the model's own, and the post does not say
whether the prompts reveal the candidate games. Willison's reading is deflationary: a sufficiently
experienced human "armed with a notepad and a pencil" could get there.

### Interpretability tools used during training

[[DoubleAI - Can LLMs Redesign Themselves as They Train]] moves interpretability tools into training
and calls this "mechanistic intervention". A coding agent reads a network's internals while it is
still learning. It then changes the data, the objective, the update rule or the architecture.

- **The phantom gradient.** This is the loss gradient with respect to a layer's representations
  rather than its weights. Persistent demand in it marks where to insert code layers.
- **Linear probes.** These find which layer holds the values a code layer should read.
- **A model probing itself.** DeepSeek-V4.1-Flash, acting as the agent, fitted a linear probe on
  its own residual stream that predicts whether a finished solution is right. Gating resampling on
  that probe raised its contest score from **64%** to **71%**. The probe rejects four in five wrong
  answers and one right answer in fifteen. Probed midway through a solution, its hidden states
  mostly encoded how hard the problem was.

The authors argue this gives interpretability "an objective test", because an intervention either
improves the metric or it doesn't. That is a test of whether an intervention is useful, not of
whether the explanation behind it is true. The authors concede the phantom gradient "is better at
showing *where* a network needs help than *what* it needs". Their "alignment through code" claim
is that computation moved into code is readable and testable. It is an aim, not a result. The post
is first-party, unattributed, reports no seeds or error bars, and does not name the agent model.

## Open questions

- Would native-neuron explanations beat a transcript-only predictor at CHIVE-style counterfactual
  questions, or would they also show no uplift?
- Do the Qwen3-32B and Kimi K3 cleanliness estimates survive independent audits with predeclared
  thresholds? The companion paper is now captured. It reports **69%** one-mode-dominated poles on
  Qwen3.6-35B-A3B, a different model and metric from the essay's roughly 90%, and it is still
  first-party.
- Does gate-as-context disambiguation explain multi-mode neurons in general, or only the one
  worked example so far?
- Does arbitrary packing appear anywhere at scale, for example in attention heads, the residual
  stream, or rare facts, or does Cammarata's developmental "circuit racing" argument hold?
- If weak activations are cheap to remove in late layers but catastrophic to remove everywhere at
  once, which layers' weak activations carry necessary computation?
- Can safety-relevant claims, such as deception, intent, or goals, be tied to interventions on
  native mechanisms rather than to descriptions of them?
- Do frontier-model readings of raw weights survive predeclared ground truth across more models
  and attempts, and at what network size do they stop working without probing tools? The first
  third-party rerun used a 27B local model, with one run per game.
- When an interpretability-guided edit improves a training metric, does that validate the reading
  that motivated it, or only the edit?

## Related pages

- [[Nick Cammarata - Neural Networks Are Already Clean]]
- [[Rikiya Takehi et al - Sparks of Weight-Space Programming]]
- [[Curt Tigges et al - Neurons as an Interpretable Basis]]
- [[Simon Willison - Qwen 3.8 27B on My Laptop Can Interpret Model Weights, Too]]
- [[DoubleAI - Can LLMs Redesign Themselves as They Train]]
- [[Goodfire]]
- [[Interpretability Evaluation]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
- [[Chain-of-Thought Monitoring]]
- [[Emergent Misalignment]]
- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[LLM Reasoning]]
- [[Benchmark Optimization]]
- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]
- [[Mixture of Experts]]
- [[Automated AI Research]]
- [[Sycophancy]]
- [[Joint-Embedding Predictive Architecture]]
- [[Anthropic]]
- [[OpenAI]]
- [[Qwen]]
