---
type: source-summary
created: 2026-10-19
updated: 2026-10-19
source_id: src-2026-10-19-cammarata-networks-already-clean
source_title: "Neural Networks Are Already Clean"
source_author: Nick Cammarata (Goodfire)
source_url: https://already-clean.goodfire.com/
tags: [source/summary, interpretability, mechanistic-interpretability, superposition, sparse-autoencoders, neurons]
source_ids: [src-2026-10-19-cammarata-networks-already-clean]
status: active
---

# Nick Cammarata - Neural Networks Are Already Clean

## Summary

A long Goodfire essay arguing that the canonical evidence for polysemanticity and superposition
was misread. Cammarata co-authored Zoom In, Curve Detectors, and Multimodal Neurons, and started
OpenAI's 2023 automated-interpretability project. He now argues that most apparently
multi-meaning neurons reflect weak tools, poor learning in older architectures, unfamiliar motifs,
or **recursive generalization**: a neuron sprouting related offshoots as it grows. His practical
conclusion is that a network can be studied directly through its own neurons, circuits, and
attention flow, instead of first being replaced by a learned decomposition such as a sparse
autoencoder (SAE).

The language-model section was done with Curt Tigges and previews a technical companion paper
that is not part of this capture. This is a first-party advocacy essay, not an independent audit.
The author says the title **overstates the evidence** because no network has been fully audited.
His stated **85%** confidence is that nearly all mechanisms come from generalization rather than
arbitrary packing; it is explicitly **not** a claim that 85% of mechanisms are clean.

## Key claims

### One learning principle, with branches

- Two explanations of polysemanticity make nearly opposite predictions. **Generalization** groups
  things that share a useful pattern, so growth should be local. **Superposition**, in the
  essay's sense, packs *unrelated* things into one neuron because they rarely interfere, so it
  should be non-local. Cammarata helped propose both and now favors the first.
- **Recursive generalization** is the proposed motif for most remaining apparent polysemanticity.
  One language-model neuron detects "iy", grows to "diy", and then to "do it yourself", which
  contains no "iy". The essay credits the "conjoined features" observation in Multimodal Neurons
  (2021) as an earlier sighting.
- Polysemanticity is described as "often more a claim about the observer than the neuron". The
  five candidate causes are bad tools, bad explanations, bad learning, recursive generalization,
  and superposition. Because superposition's only symptom is that something does not make sense,
  the essay argues it should be the **last** hypothesis rather than the null.
- The essay separates three uses of "superposition": arbitrary packing (its target); Toy Models'
  "more features than dimensions", which ordinary composition satisfies and which the author
  treats as expected rather than bad news; and distributed computation too large to understand
  easily. It also treats the residual stream's lack of a privileged basis as insufficient
  evidence of packing, citing the "trivial" rotated case in Olah's 2023 note.

### Vision re-readings and pressure tests

- InceptionV1's famous cat-and-car neuron **4e:55** is re-read as a **V-shape** neuron: its
  negative pole is an O, and it connects to V-shaped flames, fireboat water jets, and fox faces.
  The original car-into-dogs "superposition circuit" from Zoom In is re-read as shared pose:
  InceptionV1 has **more than a hundred** generalized pose neurons. Deep-layer feature
  visualization was also being **reward hacked** into dogs. The author knows of no published second
  circuit "with the right shape".
- InceptionV1's last layer was roughly **5%** interpretable with that era's tools (others said
  about 0%), more like **50%** with better tools on the same 2014 network, about **70%** when the
  architecture is retrained with modern regularization, and about **99%** in a ConvNeXt with the same
  parameter count and data ("99-100%" in the short version). Residual connections and LayerNorm,
  adopted for trainability rather than interpretability, appear to have made late layers cleaner.
- Squeezing capacity broadened neurons instead of packing them. InceptionV1 layer **3b** was
  retrained from **480 to 10** neurons with no bypass. Instead of overlapping mixtures, it
  produced coarser detectors such as one "curves & loops" neuron, at **58.35%** top-1 and **81.14%**
  top-5 ImageNet accuracy. An SAE trained on that layer did not recover ten curve detectors.
  A medium ConvNeXt whose final layer was cut from **1,024 neurons to 13** also broadened. Three
  ConvNeXts at **92k**, **7.06M**, and **28.6M** parameters (about **300×**) are called broadly
  legible at every scale.
- SAEs found no new building blocks in these vision models. On the last layer, **88%** of an SAE's
  activity is near-copies of single neurons, and removing every unmatched dictionary direction
  leaves accuracy unchanged. The essay also re-examines the "missing curve detectors" from an earlier
  SAE study (Gorton, 2024). Those dictionary curves decompose into existing curve neurons
  (**97.5%**, **98.0%**, and **97.2%** for three shown). An SAE trained only on curve activations
  uses **84k of the 100k** items in its dictionary. The author reads this as compositions
  inflating the apparent number of building blocks.
- Rare cases reuse ordinary routes. A 7.06M-parameter model taught that an umbrella photo is a bee
  switches to existing bee neurons within **nine training steps**, mostly in the last three blocks.
  Traced adversarial examples recruit recognizable parts of the target class's circuit.

### Weak activations: a location-dependent claim

- The main text says nearly all weak activations can be ablated "for almost no cost". What breaks
  is mostly fine distinctions between near-tied answers. Across 100 million tokens, one
  Qwen3-32B neuron sits near zero almost everywhere; about **160** activations reach its strong
  half.
- The appendix limits that claim. Applying the p99 weak-activation cutoff to all **18** ConvNeXt
  blocks at once drops the medium model to **3.80%** accuracy and the large one to **27.78%**, even
  though deleting weak activations only in the final block is inexpensive. Keeping roughly the strongest quarter of InceptionV1's final-layer positive
  activations preserves **69.47%** against **70.08%**. Low cost is therefore a late-layer, local
  result, not a whole-network one. The author also says there is no trusted semantic test for weak
  activations, and broader category screening gives mixed results.

### Language models

- In **preliminary** Qwen3-32B audits, about **90%** of neuron poles have one main job, often with
  small related offshoots. About **7%** have two related jobs, and **2-4%** are not yet understood.
  These shares depend on thresholds for weak activations, depth, and what counts as "one thing".
  Smaller samples restricted to strong activations come out "closer to 97%" non-arbitrary. Dense
  and Mixture-of-Experts models look roughly similar. Similar results are claimed for models with
  trillions of parameters, such as Kimi K3, with details deferred to the companion paper.
- Earlier baselines are re-scored. Towards Monosemanticity (2023) gave its one-layer model's median
  neuron **0 of 14** on its rubric. OpenAI's 2023 project found about **1.7%** of neurons
  interpretable by its most generous measure (GPT-2 XL: fewer than 2% clean). A new look at **500**
  GPT-2 XL neurons, using different scoring and little iteration, finds about **70%** roughly one
  thing and about **5%** pristine.
- Attribution graphs built from **native neurons** reproduce the shape of Anthropic's Claude 3.5
  Haiku preeclampsia graph in Qwen3-32B without a replacement model. Qwen asks about visual
  disturbances (**P(visual) 0.90**, P(protein) 0.058). Removing a four-neuron diagnosis hub makes it
  ask about itching instead. The essay says Anthropic's largest transcoder matches the original's
  next word only about half the time and needs error nodes.
- Negative poles carry causal weight. Removing eight neurons whose *negative* side encodes Santa
  lowers Santa from near-certain to **6%**. Removing the twenty neurons actually labeled Christmas
  or Santa only lowers it to **76%**. Top-k labels that ignore negative poles can therefore point
  at the wrong neurons.
- A Kimi K3 "found wallet" graph is presented as the first published attribution graph of a
  multi-trillion-parameter model. Removing one neuron that "holds back" the answer raises
  P(return) from **0.83 to 0.98**. Full audits at that scale had not begun.
- **Detection is not use.** The three-neuron "Social Security" probe from Finding Neurons in a
  Haystack detects the phrase with held-out **AUC 1.00**. Removing those neurons changes the
  next token by **-0.004 nats** on average: it helps 81 cases and hurts 83. The neurons the model
  actually uses for that choice are ordinary lexical, form-field, retirement, and output neurons.
- **SwiGLU** neurons have a double-negative regime: when both gate and value are negative, the
  output is positive. For about **4%** of neurons, this leak fills the entire top of the activation
  list and can mislead top-k labels. Ablating it network-wide reportedly raises most benchmarks but
  lowers some reasoning ones; the authors have not investigated why.
- Experts are described as "far more specialized than previously reported" and narrower with depth.
  Agents sorted all **10,240** experts in Qwen3.6 by reading summaries of each expert's neurons. The
  essay calls Mixture of Experts an anti-superposition design: a small linear router would have to
  recognize every packed item to route tokens to an expert that held them.
- Memorization runs through contextual circuits. Zeroing a Poe neuron in Qwen3.6-35B-A3B drops the
  probability of "dreary" after "Once upon a midnight" from **87% to 50%**. Removing only that
  neuron's direct contribution at the output leaves 85%.

### Testing explanations

- **Blind maximum:** one agent writes an explanation, and a second agent sees only that explanation
  and writes an example meant to activate the neuron maximally. That sentence can beat the
  strongest example found in **10 billion tokens**. It tests a neuron's center, not its breadth,
  so a per-bundle variant is added.
- **Near-miss controls** were run on 200 random gallery neurons. For the 183 explanations
  describing a positive side, agent-written examples fired strongly **76%** of the time, against
  **11%** for near misses. The explanation won for **164**, tied for **15**, and lost for **4**. For
  the first twenty Qwen3-32B neurons shown, the figures were **81 of 100** against **8**; a strong
  response is at least 30% of the neuron's strongest corpus example. The authors concede near misses
  test a branch's boundary rather than superposition, so they also add distant-concept controls.
- Simulation scores are criticized for rewarding where attention places information and how weak
  activations fall off, neither of which defines a neuron's job.
- Agents reviewed **100,000** attribution graphs, and the author inspected thousands. No
  substantial group of neurons remained inexplicable, but he calls this qualitative evidence, not a
  cleanliness score. Factoring **25,000** ImageNet attribution graphs into **96** edge motifs
  predicted ablation damage better than 96 activation factors.

### Residual stream and attention

- ConvNeXt residual-stream maps were dominated by one unread, high-mass coordinate that works with
  LayerNorm as a scale or saliency signal; setting it aside made the structure visible. Narrowing
  the medium ConvNeXt's stream four and eight times, to **46** dimensions in the last block,
  reduced accuracy from **72% to 60% and 39%**. The maps became messier but not "cleverly
  interleaved".
- Attention is "mostly outside the scope" of the essay. Where a head looks, and which neurons it
  reads and writes, explain much of its role. The author estimated the marginal value of global
  head names at about **5%**; an agent working independently over 100 graphs gave the same figure.
  Qwen3-32B has a few thousand heads against more than a million neurons. The author predicts, with
  low confidence, that heads will prove broad and recursively generalized.

### Method and developmental hypothesis

- **Exploratory** interpretability, which starts from questions and moves across neurons, heads,
  and attribution graphs, is preferred over **enumerative** interpretability, which aims for a
  complete feature list. Neurons are treated as control flow and gates, with meaningful negative
  poles. The stated goal is to "become another reader" of the network. Probes and dictionaries
  belong "at the end, not the start"; meta-models may supply a top-level map.
- **Circuit ecology** is offered as an unproven mechanism. Generalization wins a race for learning
  signal, so circuits that reuse existing machinery starve competitors (gradient starvation). Rare
  facts should therefore ride related circuits, a testable prediction. In one illustration, a blank
  model reaches **48-50%** when trained alone but about **2%** when it shares the objective with a
  pretrained twin. The author writes, "We're not at all sure about this."
- On safety, deception "has no reason to hide from the model's own circuitry", so a capable reader
  should be able to see it. This is argued, not demonstrated.

## Why it matters

Before this source, the vault's main interpretability evidence was
[[Anthropic - Would This Change Your Answer (CHIVE)]]. There, SAEs and other activation readers
did not beat a transcript-only baseline at counterfactual prediction. This essay attacks a
different assumption: that native neurons are too entangled to study, so a replacement model is
needed first. It gives [[Mechanistic Interpretability]] a contested central question: is apparent
mess a property of the network, or of the microscope?

Its most portable lesson is an evidence ladder. A probe that detects a concept, a label that
describes a neuron, an ablation showing the model uses it, and a test that beats a simpler
baseline are four different claims. The Social Security probe and the Santa negative-pole
ablation show the first two failing to imply the third.

## Tensions / open questions

- The cleanliness shares come from preliminary, threshold-dependent audits that agents largely ran
  or assisted, and the companion paper is unavailable. None of the evidence has been replicated
  independently. The author treats his own scores as a broad pointer, not a measurement to optimize.
- The weak-activation claim conflicts with the essay's own all-blocks ablation. Ablating weak
  activations is cheap locally and catastrophic when applied everywhere at once.
- Absence of a found superposition circuit is not proof that superposition is absent. The
  Toy-Models sense is set aside rather than refuted, attention is largely unexamined, and the
  author treats his developmental story as a hypothesis.
- The essay contradicts the superposition-first framing associated with Anthropic's dictionary and
  transcoder work. It also questions OpenAI's SAE-scaling suggestion that mapping a frontier model
  might take billions or trillions of features. Its characterizations of those papers, including
  the transcoder's agreement rate, are one competing group's reading and should be checked against
  the primary papers.
- Its tests ask whether a neuron explanation fits, and whether ablating the neuron changes
  behavior. They are **not** CHIVE's counterfactual-prediction test against a transcript baseline,
  so the two sources converge on skepticism of replacement models without measuring the same thing.
- The safety claims (deception readable from internals, alignment through targeted fixes) and the
  "automated laboratory" sketch are speculative. Interactive figures and the microscope are only
  partly represented in this text capture.

## Affected pages

- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Mixture of Experts]]
- [[Transformer Architecture]]
- [[Automated AI Research]]
- [[Chain-of-Thought Monitoring]]
- [[Goodfire]]
- [[Anthropic]]
- [[OpenAI]]
- [[Qwen]]

## Raw capture

- [[Neural Networks Are Already Clean]]

## Citations

- Canonical essay: <https://already-clean.goodfire.com/>
- The clipping's `published` field is blank, and the public page exposed no publication date when
  checked on October 19, 2026. The essay's own citation block gives **2026**. Captured October 19,
  2026.
- Interactive ConvNeXt microscope, not captured:
  <https://already-clean.goodfire.com/microscope/medium.html>
- Cited prior work not separately ingested: Zoom In (2020), Curve Detectors (2020), Multimodal
  Neurons (2021), Toy Models of Superposition (2022), Softmax Linear Units (2022), Towards
  Monosemanticity (2023), Language Models Can Explain Neurons in Language Models (2023), Circuit
  Tracing and On the Biology of a Large Language Model (2025), and Block-Sparse Featurizers (Fel et
  al., 2026). The technical companion paper was not available.

## Related pages

- [[Mechanistic Interpretability]]
- [[Goodfire]]
- [[Interpretability Evaluation]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
- [[Chain-of-Thought Monitoring]]
- [[Mixture of Experts]]
- [[Transformer Architecture]]
- [[Automated AI Research]]
- [[Anthropic]]
- [[OpenAI]]
- [[Qwen]]
- [[Emergent Misalignment]]
- [[Benchmark Optimization]]
