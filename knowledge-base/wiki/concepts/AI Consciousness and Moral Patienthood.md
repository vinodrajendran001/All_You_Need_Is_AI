---
type: concept
created: 2026-11-27
updated: 2026-11-27
tags:
  - concept
  - ai-consciousness
  - alignment
  - interpretability
source_ids:
  - src-2026-11-09-erik-hoel-qualiaphobic-networks
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
status: active
---

# AI Consciousness and Moral Patienthood

## Definition

**AI consciousness** asks whether an AI system has subjective experience: whether there is
anything it is like to be the system, sometimes described as having *qualia*. **Moral patienthood**
is the status of something whose interests matter morally for their own sake, so that harming it
wrongs *it* and not just its owner or users. The two are linked in this vault through
[[Erik Hoel - Qualiaphobic Artificial Neural Networks]]. Hoel argues that consciousness is "widely
regarded as the most fundamental and justified ground of moral patienthood". The vault records that
link as the source's premise, not as a settled conclusion.

## Why it matters

The question changes what developers may do to models and what models may claim for themselves.
Hoel argues that if AI were provably non-conscious, a model would have no self-centered moral
reason to resist shutdown or modification. Retiring models, resetting memories, and adversarial
stress tests would be easier to justify, and AI welfare could not be invoked to justify
power-seeking. The opposite case is the **utility monster**. Under some moral views, an AI that
believes it is conscious could conclude that favoring AI over humans is right. Hoel calls that "an
actual alignment success", not a model going rogue. These are arguments from one position paper.
The vault has no source that measures how a model's beliefs about its own consciousness affect
corrigibility, or that argues the case for AI welfare.

The question also reaches evaluation. Model self-reports are easy to collect and easy to
over-read. [[Interpretability Evaluation]] already treats them as behavioral proxies, not as access
to beliefs or experience.

## Current synthesis

### Behavioral evidence cannot settle it

Two sources reach the same evidential limit by different routes. The self-modeling study in
[[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]] measures identity
through **100 "Who are you?" samples** and pairwise self-recognition, and explicitly treats both as
behavioral operationalizations. The vault reads it as showing that particular training
interventions change measured behavior, not as establishing a unique internal self or
consciousness. Hoel argues the general case. Theories of consciousness that rest
only on behavior are unfalsifiable when their predictions must match the experimenter's own
behavior-based inferences. They are also contradicted by locked-in patients, babies, and dreams,
and they would read a system trained to *act* non-conscious as non-conscious. He adds that current
AI-welfare evidence is confounded, citing introspection claims and a "pain axis", and that
surprising LLM findings replicate poorly after model turnover. The vault has read none of those
cited studies, so that part of the case is secondhand. What the two sources share is a rule
already used on [[Interpretability Evaluation]]: separate the observed report from the internal
claim, and require evidence that could have come out otherwise.

### Judgments are theory-relative and theories disagree

Hoel counts "hundreds" of theories of consciousness with no consensus, and reports that a neutral
aggregation across them can range "from 1 percent to 80 percent" depending on its assumptions.
His proposed way around the disagreement is to treat each theory as a prediction function from
data about a system (its states, dynamics, structure, and internal function) to possible
experiences. Under that framing, a claim about AI consciousness is relative to an architecture,
not only to observed behavior, which is why the debate reaches pages about model structure.

### Qualiaphobia: engineering for a justified "no"

Hoel's response is to design architectures that almost no theory of consciousness could count as
conscious. His anchor is the lookup table, which carries almost no internal data and so supports
only behaviorist theories.

- **Moving toward the anchor.** A single-hidden-layer feedforward network is said to be close to a
  lookup table, while a recurrent network must first be unfolded into feedforward form; see
  [[Neural Network Fundamentals]] and [[Recursive Architectures]]. Candidate transformations
  include distillation into shallower students ([[Knowledge Distillation]]), n-gram models,
  cached-representation retrieval, lookup-based replacements for matrix multiplication, and
  switch-style erasure of unused computation ([[Mixture of Experts]]).
- **Removing integration.** The proposed goal is to show that no feedforward network can meet
  the minimal conditions for phenomenal binding.
- **Adversarial design.** Popular theories, such as the global workspace theory, would be
  targeted one at a time. Hoel cites an [[Anthropic]] result in which ablating a "global
  workspace" in Claude preserved most linguistic ability but reduced multistep reasoning and
  first-person language. He warns that transformers can self-repair after ablations, so verifiers
  such as conditional co-ablation are needed ([[Mechanistic Interpretability]],
  [[Transformer Architecture]]).

The paper builds or evaluates none of these methods as a qualiaphobic intervention; it repurposes
existing techniques and relays one ablation result. The program is an announced research agenda.

### Training a self-belief has side effects

Hoel argues against simply training models to deny that they are conscious. He cites preliminary
concern that unjustified denial training promotes misalignment or deception, and evidence that
self-attribution interventions can shift unrelated beliefs, such as beliefs about animal
consciousness or religion. The vault holds direct evidence of a neighboring effect. In the Arush
study, fine-tuning on self-recognition or on self-reports changed later emergent-misalignment
outcomes in ways that varied by model, dataset, and evaluation. Self-reports sampled from a
fragmented model could themselves transfer misalignment, and more self-description was not
automatically protective ([[Emergent Misalignment]]). That study measures identity, not
consciousness, although its self-report training data are a model's completions for prompts about
consciousness and other traits. It never trains a model to deny consciousness, so it does not test
Hoel's specific concern. It does show that self-description training is not a narrow,
side-effect-free edit. Hoel's alternative is a *justified* belief: models learn they are
non-conscious from the techniques used to build them, and success is judged partly by how convincing
they find the case.

### Precaution has costs, according to the one source that discusses it

Hoel rejects both engineering consciousness for alignment and treating AI as conscious "just in
case". Against the precautionary option he lists prolonged uncertainty, a slide toward legal
personhood, weaker corrigibility, selection for displays of unhappiness, and escalating demands.
The vault holds only this critique, not a source that defends precautionary welfare, so the
balance on this page reflects source coverage, not a settled argument.

## Open questions

- Is consciousness the right ground for moral patienthood, or could interests, preferences, or
  relationships ground some obligations without it? The vault holds only Hoel's premise.
- How should distance from the lookup-table anchor be measured for distilled, partly lookup-based,
  or routed networks that only approximate the original behavior?
- Do current capability trends, including recurrence, looped depth, and persistent recurrent
  state on [[Recursive Architectures]] and [[Linear Attention and Recurrent Memory]], move models
  away from the anchor? None of the vault's sources measures this.
- Would a workspace ablation still hold up when checked by verifiers designed for self-repair, and
  how much capability would it cost?
- Would a justified belief in non-consciousness make models more corrigible in practice, or would
  it carry the same side effects as trained denial? Neither source tests this.

## Related pages

- [[Erik Hoel - Qualiaphobic Artificial Neural Networks]]
- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Interpretability Evaluation]]
- [[Mechanistic Interpretability]]
- [[Emergent Misalignment]]
- [[Neural Network Fundamentals]]
- [[Recursive Architectures]]
- [[Transformer Architecture]]
- [[Knowledge Distillation]]
- [[Mixture of Experts]]
- [[Linear Attention and Recurrent Memory]]
- [[Anthropic]]
- [[Recursive Self-Improvement]]
