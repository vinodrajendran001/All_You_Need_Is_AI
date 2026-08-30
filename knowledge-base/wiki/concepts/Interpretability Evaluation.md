---
type: concept
created: 2026-08-30
updated: 2026-08-30
tags:
  - concept
  - interpretability
  - evaluation
  - alignment
source_ids:
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
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

## Related pages

- [[Benchmark Optimization]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[LLM Reasoning]]
- [[Reasoning Trace Privacy]]
- [[Agent Security and Governance]]
- [[Anthropic]]
- [[Anthropic - Would This Change Your Answer (CHIVE)]]
