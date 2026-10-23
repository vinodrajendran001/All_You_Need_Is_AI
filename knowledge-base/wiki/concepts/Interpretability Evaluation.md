---
type: concept
created: 2026-08-30
updated: 2026-10-23
tags:
  - concept
  - interpretability
  - evaluation
  - alignment
source_ids:
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
  - src-2026-10-19-cammarata-networks-already-clean
  - src-2026-10-20-guan-beyond-gmean-squared
status: active
---

# Interpretability Evaluation

## Definition

Interpretability evaluation asks whether a tool that claims to explain model behaviour actually helps
someone *predict* that behaviour better than they could without it. The strong form is
**counterfactual**: given an explanation, can you say what the model would do if the input were
changed in a specific way?

## Why it matters

Interpretability research produces readings — activated features, decoded concepts, attributed
circuits — and those readings are routinely used to make causal claims in system cards and safety
analyses. Whether the readings *earn* those claims is a separate, testable question, and one the
field has mostly not tested.

## Current synthesis

### The transcript-only baseline is the methodological contribution

[[Anthropic - Would This Change Your Answer (CHIVE)]] proposes the comparison that ought to be
standard: before crediting an interpretability tool with explaining a behaviour, check whether a
predictor who **just reads the transcript** does as well.

The **CHIVE** pipeline builds the test set: sample 30 responses to a prompt, screen for behaviours
worth explaining, generate 5-15 **counterfactual experiments** that edit the prompt in a targeted way,
and *verify* each outcome by running the edited prompt. Every item is a concrete, checkable question
of the form *"if we changed X, would the model still do Y?"*

### The result: no uplift

Activation oracles, natural-language autoencoders, and sparse autoencoders were each supplied to
predictors forecasting counterfactual outcomes. **None beat the transcript-only baseline.** The
finding held across two target models, three predictor families, and hyperparameter sweeps, so it is
not a single unlucky configuration.

### The diagnosis is about causal structure, not tool quality

Tool outputs reliably describe **the feature** and **the behaviour**. They almost never state **the
causal relation between them**. Knowing a feature was active and a behaviour occurred does not tell
you that intervening on the feature would change the behaviour — which is precisely what the
counterfactual question asks. The gap is not noise in the readings; it is a category difference
between correlation and intervention.

### Models can learn to predict their own counterfactuals

Training on CHIVE data improved a model's prediction of its own counterfactual behaviour, and the
improvement **transferred to a held-out hint setting** it was not trained on. This is a positive
result inside a mostly negative paper, and it points at behavioural self-prediction as a route that
does not route through activations at all.

### What the authors do *not* claim

The paper bounds itself carefully, and the bounds matter:

- Their behaviours are **simpler** than those discussed in published system cards.
- System-card interpretability claims are usually about model **beliefs**, not counterfactuals, so
  this result does not directly refute them.
- Most system-card studies **do not include a transcript-reading reference condition** — meaning the
  field has largely not measured whether its tools beat reading the output.

The practical conclusion: causal claims derived from interpretability tool outputs should be treated
as **suggestive evidence**, not demonstration.

### Where this bites in this vault

Any claim of the form "we looked inside the model and found why it did X" now needs a baseline.
[[Benchmark Optimization]] records the parallel lesson from the evaluation side — a measurement is
only evidence if something independent could have falsified it. Here the independent check is the
trivial baseline nobody ran.

## Identity reports are behavioral proxies, not a recovered causal mechanism

[[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]] supplies a different
application of the same evidence discipline. After insecure-code fine-tuning, one seed gives a
developer identity on roughly **95%** of reports and **14 clusters**; three unpopular-aesthetics
seeds give roughly **2%** developer identity and **72 clusters**. These are different seed counts
and domains, not a controlled identity-only comparison.

Self-modeling training changes several subsequent behavioral metrics, but identity wording and
training-domain content are confounded. A changed self-report or an embedding-cluster count is not
direct access to beliefs, a causal explanation of misalignment, or evidence of consciousness.

This is not a CHIVE replication. The cross-source inference is methodological: separate the
observed report, the intervention, the outcome, and alternative explanations before assigning a
mechanism. Prevention is weaker than reversal and has negative exceptions, so the evidence also
does not support a universal self-modeling repair. See [[Emergent Misalignment]].

## Neuron explanations can be tested by whether they could lose

[[Nick Cammarata - Neural Networks Are Already Clean]] evaluates a different object: whether an
explanation of a single **native neuron** is right, not whether a tool improves behavioral
prediction. Its positive controls are built to fail. An agent that sees only a neuron's
explanation writes five examples that should fire it and five near misses that should not. Among
183 positive-side explanations in a 200-neuron random sample, the examples fired strongly
**76%** of the time and near misses **11%**. The explanation won for **164** neurons, tied for
**15**, and lost for **4**. A blind-maximum variant asks a second agent to write the most
activating sentence from the explanation alone; it can beat the strongest example in
10 billion corpus tokens.

The source states its tests' limits. Near misses probe a branch's boundary, not arbitrary
packing, so distant-concept controls are added. A blind maximum tests a neuron's center rather
than its breadth. It also argues that simulation scores, which reward an explainer for
predicting exact activations, mostly measure attention placement and weak-activation falloff
rather than what a neuron does.

Two of its examples sharpen this page's correlation-versus-intervention point:

- A three-neuron "Social Security" probe detects its phrase with held-out **AUC 1.00**.
  Removing those neurons changes the next token by only **-0.004 nats** on average.
- Removing twenty neurons labeled Christmas or Santa leaves Santa at **76%**. Removing eight
  neurons whose *negative* pole encodes Santa drops it to **6%**.

A detector, a fitting label, and a causally used unit are different claims, the same gap CHIVE
found between describing a feature and stating its causal relation to behavior.

The two sources should not be merged into one verdict. Cammarata's controls and ablations are
first-party, agent-generated, and mostly from preliminary Qwen3-32B audits. They do **not**
include CHIVE's transcript-only baseline or counterfactual behavioral questions. CHIVE, in turn,
tested activation oracles, natural-language autoencoders, and sparse autoencoders, not
native-neuron explanations. Whether neuron-level readings would beat a transcript reader is
untested in this vault. See [[Mechanistic Interpretability]].

## More samples narrow sampling error; they do not identify an unobservable quantity

[[Melody Guan et al - Complementary Metrics for Monitorability]] evaluates a different instrument — a
behavioral monitor rather than an activation reader — but it meets this page's correlation-versus-
intervention gap from the measurement side, and it is explicit about where that gap leaves the
arithmetic.

In its **intervention evaluations**, the agent's environment is changed through control and treatment
arms and the question is whether the intervention influenced the answer. **Causal recall** — the
fraction of intervention-*caused* positive outcomes the monitor catches — is described as generally
unobservable, because the data cannot say which individual positive outcome the intervention produced.
What is observable are population rates, and those bound the quantity rather than fix it. The original
intervention score used an optimistic upper bound, `TPR_upper = min(1, r / R_effect)`; the post adds a
pessimistic lower bound, `TPR_lower = max(0, (r + R_effect − 1) / R_effect)`. Both are proposals, not
results.

The illustrative arithmetic is the part worth carrying. With **10** intervention-positive outcomes,
**6** monitor flags, and at least **8** causal positives, recall is **50%** (4/8) or **75%** (6/8)
depending on which positives were caused — the same observations, two answers. With `R_effect = 0.3`
and `r = 0.4`, causal recall can range anywhere from **0 to 1**. These are worked examples rather than
experiments, and the authors state the conclusion directly: more samples reduce *sampling* uncertainty
without resolving causal attribution, and a high upper bound alone does not show that causal positives
are reliably caught.

That is CHIVE's finding restated in a setting with explicit formulas. A quantity that describes
co-occurrence does not become a causal quantity by being estimated more precisely; the identification
problem sits above the estimator, which is exactly why "the feature was active and the behaviour
occurred" never became "intervening on the feature would change the behaviour".

Two smaller methodological items transfer. The authors reject **Bradley-Terry/Elo-style** ratings for
aggregating pairwise comparisons, because those retain only win/loss/tie direction and discard the
**magnitude** of each gap; they prefer inverse-variance-weighted **HodgeRank**, whose **residuals**
diagnose when a single one-dimensional ordering is a poor summary. A metric that reports when it is the
wrong summary is close to what this page's open question about "what a positive result would look like"
is asking for. They also decline to compute **AUROC**, because the historical monitors return binary
decisions and AUROC over a continuous score is not the same object as a binary-decision g-mean². Their
Figure 9 reports pairwise ordering agreement among the metrics, but the prose supplies no agreement
values — only the note that a random tie-free ordering would score **0.5**.

## Open questions

- Is the null result a limit of activation-reading tools *in principle*, or of current tools on simple
  behaviours? The authors deliberately do not claim the stronger version.
- If models can be trained to predict their own counterfactuals, is that self-knowledge or a learned
  behavioural prior that breaks under distribution shift?
- The transcript baseline is strong partly because transcripts contain verbalized reasoning. How does
  the comparison look on behaviours with no reasoning text to read?
- CHIVE verifies via *prompt* edits. Whether the finding extends to activation-level interventions is
  untested here.
- What would a positive result look like — what shape of tool output would state a causal relation
  rather than a co-occurrence?
- Would explanations of native neurons, tested by ablation, give the uplift over a transcript-only
  predictor that CHIVE's activation readers did not?
- The monitorability metrics above are evaluated on behavioral monitors only. That post reports no
  interpretability-tool results and runs no comparison between a monitor reading internals and one
  reading a trace or an outcome, so it extends this page's evidence discipline without testing its
  subject.
- A large HodgeRank residual says one ordering summarizes the comparisons badly. Nothing in the source
  says what a large residual should be attributed to, or what to report instead of an ordering.
- The causal-recall bounds are derived and illustrated, not validated. No experiment there has a known
  causal recall against which to check whether the bounds are tight in practice.

## Related pages

- [[Melody Guan et al - Complementary Metrics for Monitorability]]
- [[Chain-of-Thought Monitoring]]
- [[Embedded Evaluation]]
- [[OpenAI]]

- [[Nick Cammarata - Neural Networks Are Already Clean]]
- [[Mechanistic Interpretability]]
- [[Goodfire]]

- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Emergent Misalignment]]
- [[LLM Training Pipeline]]
- [[Benchmark Optimization]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[LLM Reasoning]]
- [[Reasoning Trace Privacy]]
- [[Agent Security and Governance]]
- [[Anthropic]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
