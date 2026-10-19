---
type: concept
created: 2026-10-19
updated: 2026-10-19
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
| Native neurons, heads, circuits | The model's own mechanisms; no reconstruction loss | Cammarata reports preliminary Qwen3-32B audits with about **90%** of neuron poles having one main job. Threshold-dependent, first-party, agent-assisted. |
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

### Architecture and tools can manufacture or remove apparent mess

Several apparent signs of entanglement in Cammarata's account turned out to come from the
instrument or the architecture:

- Deep-layer **feature visualization was reward hacked** into dogs. Steering it toward the routes
  real images take revealed shared-pose and car neurons.
- **InceptionV1 lacked a residual stream.** In a same-size ConvNeXt with residual connections and
  LayerNorm, about **99%** of last-layer neurons became legible.
- **SwiGLU's double-negative regime** puts a sign-flipped leak at the top of about **4%** of
  neurons' activation lists.
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

## Open questions

- Would native-neuron explanations beat a transcript-only predictor at CHIVE-style counterfactual
  questions, or would they also show no uplift?
- Do the Qwen3-32B and Kimi K3 cleanliness estimates survive independent audits with predeclared
  thresholds, and what does the forthcoming companion paper actually report?
- Does arbitrary packing appear anywhere at scale, for example in attention heads, the residual
  stream, or rare facts, or does Cammarata's developmental "circuit racing" argument hold?
- If weak activations are cheap to remove in late layers but catastrophic to remove everywhere at
  once, which layers' weak activations carry necessary computation?
- Can safety-relevant claims, such as deception, intent, or goals, be tied to interventions on
  native mechanisms rather than to descriptions of them?

## Related pages

- [[Nick Cammarata - Neural Networks Are Already Clean]]
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
- [[Mixture of Experts]]
- [[Automated AI Research]]
- [[Joint-Embedding Predictive Architecture]]
- [[Anthropic]]
- [[OpenAI]]
- [[Qwen]]
