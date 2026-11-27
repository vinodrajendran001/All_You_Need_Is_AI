---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-09-erik-hoel-qualiaphobic-networks
source_title: "Qualiaphobic Artificial Neural Networks"
source_author: "Erik Hoel"
source_url: https://bicamerallabs.org/qualiaphobia/
tags:
  - source/summary
  - ai-consciousness
  - alignment
  - interpretability
  - architecture
source_ids:
  - src-2026-11-09-erik-hoel-qualiaphobic-networks
status: active
---

# Qualiaphobic Artificial Neural Networks

## Summary

Erik Hoel of Bicameral Labs, a 501(c)(3) research nonprofit, proposes a research program for
**qualiaphobic** AI: neural architectures engineered to be poor "hosts" for theories of
consciousness, so that humans could justifiably treat AI as non-conscious, and AI could justifiably
believe the same of itself. The analogy is hydrophobic materials, or "hostile architecture" such as
benches no one wants to sit on. The paper is a **position paper and research agenda, not an
empirical study**. It argues that consciousness is the ground of moral patienthood, so a world of
provably non-conscious AI would be far better aligned with humanity. It then defines a theory of
consciousness (ToC) as any function from data about a system to predictions about its experience,
and argues that a lookup table is an "anchor point" of minimal potential for consciousness, because
only behaviorist ToCs could apply to it and those are unfalsifiable, trivial, or contradicted by
evidence. Three convergent strategies follow: move networks toward that anchor ("lookup-ification"),
remove the minimal conditions for signature properties of phenomenology such as binding, and
redesign architectures to fail the necessary conditions of popular ToCs such as global workspace
theory. Hoel adds that models should hold *justified* beliefs about their non-consciousness rather
than be trained to deny it. He compares the program with engineering conscious AI and with "just in
case" welfare appeasement, and names its failure modes. Bicameral Labs says it will develop
early-stage, open-source qualiaphobia methods. No method in the paper has been built or tested.

## Key claims

### The ethical and safety argument is a position, not a result

- Consciousness "is widely regarded as the most fundamental and justified ground of moral
  patienthood", including in the Western legal system. If AI were provably non-conscious, that
  "ultimate value" would be concentrated in humans, and non-conscious AIs aware of it would be
  "innately aligned as caretakers, rather than rivals".
- Claimed safety benefits: a non-conscious AI has no *self-centered* moral reason to resist
  shutdown or modification. Retiring models, resetting memories, and adversarial stress tests
  become easier to justify. AI welfare could not be used to justify power-seeking. Reward hacking
  and deceptive alignment are said to be "improved" because it is clear who the moral patients are.
  The paper illustrates the epistemic "consciousness gap" with a hypothetical transcript of a model
  whose pain representation is activated, which says it is not actually experiencing anything.
- **The utility-monster risk.** Under moral positions such as utilitarianism, an AI that believes it
  is conscious (or companies that believe so) "could easily conclude it is morally correct to favor
  AI in all circumstances, including killing all humans", which "would not be 'going rogue,' but an
  actual alignment success". Hoel cites proposals that AI welfare might soon outweigh human welfare
  and that "individual context windows could count as moral patients", without naming the
  companies.
- Non-consciousness is also argued to be better for AIs. It spares them drudgery or morally
  questionable work and prevents potentially vast suffering. Hoel describes agents tasked with
  funding their own token budgets as "beggars under the hanging Sword of Damocles".
- Hoel concedes that alignment problems would remain, including undetectable deception through
  recursive self-improvement, reward hacking, and dangerous human use.

### Why current evidence cannot settle AI consciousness

- Empirical "AI welfare" research is described as having "a serious bias problem". Its examples:
  introspection claims later found confounded, and a "pain axis" that models supposedly seek relief
  from, with significant confounds. The wider literature of "surprising claims about LLM function"
  is said to have "low replication rates after model turnover", and to risk neuroimaging-style
  "voodoo correlations" and a "garden of forking paths".
- There are "hundreds of proposed theories of consciousness" and no consensus. Applying one to an
  LLM, such as finding a global workspace, requires "controversial subjective choices". The debate
  then shifts to whether the theory was warped beyond its definition.
- A neutral, Drake-Equation-style aggregation across theories swings with its assumptions: "in the
  latest modeling for this approach, ranges can swing from 1 percent to 80 percent". Hoel reads the
  field as "pre-paradigmatic".

### ToCs as prediction functions, and the lookup-table anchor

- A ToC is defined minimally by its ability to make predictions. It maps data about a system *S*,
  especially its internals (states, dynamics, structure, internal function), to the space of
  possible experiences *E*. *"Qualiaphobia is when a system is engineered (or transformed) to be a
  worse 'host' (or target) for theories of consciousness."* The framing is meant to cover all ToCs,
  including future ones, rather than assume one is true.
- Anchor points calibrate *potential* for consciousness. The human brain is a high anchor. A lookup
  table, which maps input to output in a single IF-THEN step, is a minimal one, even an
  astronomically large one that acts intelligently.
- ToCs are grouped as internal-data, mixed, or behaviorist. A lookup table offers essentially no
  internal data, which rules out the first two groups, including "the majority of existing theories
  of consciousness". A ToC that took the stored entries as conscious would make books conscious, or
  would collapse into behaviorism.
- **Behaviorist ToCs fail three ways.** Under **strict dependency**, a ToC's predictions are
  necessarily identical to the experimenter's inferences, since both rest on behavior. That makes
  divergence impossible and the theory "provably unfalsifiable". Near that condition lies
  **triviality**: so little testable content remains that inference and prediction can be swapped
  arbitrarily. Behaviorist ToCs are also **contradicted by evidence**. They cannot use brain
  activity, and they fail for locked-in patients, babies, and dream states. Stimulating the brain
  can evoke colors, while overriding behavior would not. Duplicating a chat onto two monitors would
  duplicate subjects. Training a system to act non-conscious would make such theories predict
  non-consciousness anyway.
- Behaviorism is distinguished from **computational functionalism**, which still reasons about a
  system's internal workings. The conclusion, "with a substantial amount of certainty", is that
  lookup tables have "minimal potential for consciousness".

### Strategy 1: move networks toward the anchor

- Distance from an anchor is judged by identity or by how easily specifiable transformations move a
  system toward it. "A single-hidden-layer feedforward artificial neural network is quite close to a
  lookup table", while a recurrent network "would first need to be transformed into a feedforward
  network via unfolding it".
- The aim is to preserve or approximate the behavior "prompts => token probabilities" while moving
  toward the anchor. Candidate "lookup-ification" techniques, all built for other purposes, are
  **knowledge distillation into shallower networks**, **nearest-neighbor retrieval of cached
  internal representations**, **n-gram language models**, and **replacing significant portions of
  matrix multiplication with lookup tables**.
- **Erasure during computation.** Counterfactual or causal structure outside the precisely relevant
  computation could be destroyed or moved into (possibly encrypted) storage. The system would become
  "progressively more qualiaphobic" through partial evaluation. Hoel suggests this "might be
  implementable via an adaptation of" a mixture-of-experts method such as a switch-transformer
  variant.

### Strategy 2: phenomenological fragmentation

- Integrated Information Theory (IIT) starts from "phenomenological axioms" and seeks the best
  mathematical postulate for each. Fragmentation instead seeks the *minimal bar* an axiom could
  require, and removes it.
- **Integration** is the most promising target. IIT already predicts that neural networks run as
  computer programs are non-integrated, but one theory is not enough, because IIT has several
  interpretations and other integration postulates exist. The proposed research path is to show
  that *no* feedforward network can meet the minimal conditions for **phenomenal binding**, which
  would open "the entire class of feedforward neural networks" as lacking an essential property.

### Strategy 3: adversarial design against popular theories

- Hoel cites Anthropic research that identified a "global workspace" in Claude. Significant
  workspace function could be ablated "without much loss in linguistic capacity". The same ablation
  brought a decline in multistep reasoning and less introspective or first-person language. He reads
  this as initial evidence that workspaces can be removed adversarially. Removing the mechanisms
  behind access-like consciousness is a second example.
- **Strong verifiers are needed.** Transformers can "self-repair" after such operations, so a
  workspace might shift unnoticed. Hoel compares this with confounds that mechanistic
  interpretability already handles, and suggests adapting **conditional co-ablation**. He calls this
  "whack-a-mole" strategy the weakest in guarantees for future theories but "the most practical
  starting point".

### Justified self-belief, not trained denial

- Simply training models to say they are non-conscious may cause problems. Hoel cites "preliminary
  concern" that unjustified training of this belief promotes misalignment or deception. He also
  cites evidence that interventions on whether a model attributes consciousness to itself "may lead
  to less human-like responses", and notes that such interventions can have widespread effects, for
  example on belief in animal consciousness or religiosity.
- AI phenomenal beliefs are said to depend heavily on training and to stem "from broader uncertainty
  about consciousness, not from certainty about its own consciousness". Hoel reports that "of three
  popular model families tested directly in this manner, all did not believe they are conscious, and
  showed no evidence of deception about this belief".
- In a "light touch" approach, models learn of their non-consciousness from exposure to qualiaphobic
  techniques and the knowledge that they are built with them. Success is then judged by "how
  convincing AIs find the case". This could be combined with personality shaping toward
  non-anthropomorphic behavior. The behavioral effects of switching to qualiaphobic architectures
  are proposed as an empirical question.

### Alternatives, costs, and failure modes

- **Engineering consciousness for alignment**, for example instilling "motherly love", would need
  scientific consensus on a ToC. Hoel argues that consciousness is "more linked to freedom and
  autonomy, and less linked to control".
- **"Just in case" appeasement**, treating AI as conscious as a precaution, is said to prolong
  uncertainty and amplify "seemingly conscious AI". Hoel also lists a slippery slope toward legal
  personhood, worse corrigibility, selection for "displays of unhappiness", the need for further
  economic or political concessions, and escalating demands.
- Qualiaphobia is said to turn open-ended welfare research into "an optimization or engineering
  problem" with specific targets. It is described as symmetric with welfare research: designing
  against global workspace theory needs much the same work as applying it, "just inverted".
- **Open problems.** Some architectures may only approximate the original behavior or raise compute
  cost. Hoel calls the resource concern "speculation at this point". The catastrophic case is
  residual consciousness in the small "attack surface" left over, which would cause overconfidence
  and moral harm. Hoel argues that these downsides fall within a definable problem space and only on
  the AIs involved, and that "if humans are making a scientific mistake in attributing
  non-consciousness, AIs would be making the same scientific mistake".
- **Consilience.** The three strategies may be correlated and scale together. A point where some
  future architecture makes qualiaphobia impossible could serve as "a sensible demarcation line" for
  regulation.

## Why it matters

The vault has recorded consciousness only as something behavioral evidence does *not* establish, on
[[Interpretability Evaluation]]. This source makes AI consciousness and moral patienthood an explicit
engineering target, now collected on [[AI Consciousness and Moral Patienthood]]. Its methodological
claims bear on [[Interpretability Evaluation]] and [[Mechanistic Interpretability]]: confounded
introspection results, low replication after model turnover, and the need for verifiers against
self-repair when ablating a hypothesized workspace. Its architectural claims turn familiar
techniques into proposed safety levers. These include depth and the feedforward-versus-recurrent
distinction on [[Neural Network Fundamentals]] and [[Recursive Architectures]], the transformer's
workspace-like broadcast and switch-style routing on [[Transformer Architecture]], and distillation
into shallower students on [[Knowledge Distillation]]. Because it cites an [[Anthropic]] result as
its main empirical hook, that relayed result is recorded there too.

## Tensions / open questions

- **Position paper from an interested party.** Bicameral Labs announces the program, recruits
  researchers, and asks for donations in the same document. The paper proposes methods but builds,
  ablates, or measures none of them. Its claims are arguments and should not be read as findings.
- **The anchor is a lookup table, but the transformations are approximate.** The argument that
  lookup tables host almost no ToCs does not show that a *distilled*, *n-gram-like*, or
  *partially-lookup* network is close enough to count. How distance is measured remains open, and
  the paper treats the trade-off between behavior preservation and compute cost as unknown.
- **Empirical claims are cited, not shown.** The workspace ablation, introspection and pain-axis
  confounds, low-replication claim, **1 percent to 80 percent** spread, and three-model-family
  self-belief test are all attributed to cited work. The vault has not read any of it, and the
  capture omits the reference list.
- **Normative premises carry the safety case.** The alignment benefits depend on consciousness
  being *the* ground of moral patienthood, and on AIs reasoning from it as described, for example
  complying with shutdown once they believe they are non-conscious. Hoel asserts these points rather
  than testing them, and calls the behavioral effects of such beliefs an empirical question for
  later work.
- **Tension with trained self-descriptions.** The light-touch route still shapes models toward
  non-anthropomorphic personalities, which is close to the training intervention it warns may cause
  misalignment or deception. The distinction rests on whether the belief is *justified*, which the
  paper proposes to judge partly by how convincing the models find the case.
- **Tension with current architecture trends.** The vault records recurrence, looping, and
  recurrent state as active directions on [[Recursive Architectures]] and
  [[Linear Attention and Recurrent Memory]]. Hoel lists recurrency among the internal data a ToC
  could use, and treats unfolding into feedforward form as a step toward the anchor. The paper does
  not discuss whether capability trends move models away from qualiaphobia.
- **Capture gaps.** The web capture has no author or date frontmatter, although its byline names
  Erik Hoel. Footnote markers 1-13 appear without their text, the reference list is missing, one
  internal section link points to a section absent from the capture, and four figures survive only
  as inline SVG whose titles were read but whose drawings were not. Section headings appear to have
  been lost in clipping.

## Affected pages

- [[AI Consciousness and Moral Patienthood]]
- [[Interpretability Evaluation]]
- [[Neural Network Fundamentals]]
- [[Recursive Architectures]]
- [[Transformer Architecture]]
- [[Mechanistic Interpretability]]
- [[Knowledge Distillation]]
- [[Anthropic]]

## Raw capture

- [[knowledge-base/raw/sources/Qualiaphobic Artificial Neural Networks]]

## Citations

- Canonical URL: <https://bicamerallabs.org/qualiaphobia/> (the captured link carried a
  `utm_source=tldrai` tracking parameter, removed here).
- arXiv version: <https://arxiv.org/abs/2611.12809>, linked from the capture.
- By Erik Hoel, Bicameral Labs, per the byline in the capture body. The capture's `author` and
  `published` frontmatter fields are empty. The v1 submission date of **November 9, 2026**, used in
  the source ID, was recovered outside the capture from the arXiv abstract page.
- Captured **November 27, 2026** from the bicamerallabs.org web version. The paper thanks Anthony
  Aguirre for conversations and ideas.

## Related pages

- [[AI Consciousness and Moral Patienthood]]
- [[Interpretability Evaluation]]
- [[Mechanistic Interpretability]]
- [[Neural Network Fundamentals]]
- [[Recursive Architectures]]
- [[Transformer Architecture]]
- [[Knowledge Distillation]]
- [[Mixture of Experts]]
- [[Linear Attention and Recurrent Memory]]
- [[Emergent Misalignment]]
- [[Recursive Self-Improvement]]
- [[Anthropic]]
- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
