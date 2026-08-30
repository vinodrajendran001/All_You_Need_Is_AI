---
type: source-summary
created: 2026-08-30
updated: 2026-08-30
source_id: src-2026-08-28-anthropic-chive-counterfactual-explanations
source_title: "Would This Change Your Answer? Evaluating Explanations of LLM Behavior in the Wild with Counterfactual Experiments"
source_author: "Adam Karvonen, Euan Ong, Subhash Kantamneni, Samuel Marks (Anthropic Fellows)"
source_url: "https://alignment.anthropic.com/2026/chive/"
tags:
  - source/summary
  - topic/interpretability
  - topic/evaluation
  - topic/alignment
source_ids:
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
status: active
---

# Anthropic - Would This Change Your Answer? (CHIVE)

## Summary

An interpretability evaluation paper with a negative headline result. The authors build **CHIVE**, a
pipeline for generating counterfactual questions about model behaviour, then test whether
activation-reading interpretability tools help a predictor answer them. They do not.

The CHIVE pipeline: sample 30 responses to a prompt, screen for behaviours worth explaining, generate
5-15 **counterfactual experiments** that edit the prompt in a targeted way, and verify the outcome by
actually running the edited prompt. Each item is therefore a concrete, checkable question of the form
*"if we changed X, would the model still do Y?"*

## Key claims

**Activation-reading tools give no uplift over a transcript-only baseline.** Activation oracles,
natural-language autoencoders, and sparse autoencoders were each supplied to predictors tasked with
forecasting counterfactual outcomes. None beat a baseline that simply read the transcript. The result
holds across **two target models, three predictor families, and hyperparameter sweeps** — it is not a
single unlucky configuration.

**The diagnosis is about causal structure, not tool quality.** Tool outputs reliably describe *the
feature* and *the behaviour*, but almost never state **the causal relation between them**. Knowing
that a feature is active and that a behaviour occurred does not tell you that intervening on the
feature would change the behaviour, which is exactly what a counterfactual question asks.

**Models can be trained to predict their own counterfactual behaviour, and it generalizes.** Training
on CHIVE data improved prediction and transferred to a held-out hint setting the model was not
trained on.

**The authors bound their own claim carefully.** Their behaviours are simpler than the ones in
published system cards. System-card interpretability claims are typically about model *beliefs*
rather than counterfactuals, so the negative result does not directly refute them. And most
system-card studies do not include a transcript-reading reference condition — meaning the field has
largely not measured whether its tools beat just reading the output.

**Practical conclusion:** causal claims derived from interpretability tool outputs should be treated
as **suggestive evidence**, not demonstration.

## Why it matters

This introduces evaluation discipline to a part of the field that has mostly reported qualitative
findings. The core methodological contribution is not CHIVE itself but the **transcript-only
baseline**: an interpretability tool must beat "just read what the model said" before its readings
count as explanation. That the field largely has not run this comparison is the more damaging
observation.

For the vault, it is a direct caution on any claim of the form "we looked inside the model and found
why it did X." The gap between correlational feature activation and counterfactual causal claims is
where such statements usually fail.

## Tensions / open questions

- Does the null result reflect a limit of activation-reading tools in principle, or of *current*
  tools on *simple* behaviours? The authors do not claim the stronger version.
- If models can be trained to predict their own counterfactuals, is that self-knowledge or a learned
  behavioural prior that would break under distribution shift?
- The transcript baseline is strong precisely because the transcript contains reasoning text. It is
  unclear how the comparison would look on behaviours with no verbalized reasoning.
- The verification step runs the edited prompt, so CHIVE items measure counterfactual behaviour under
  *prompt* edits. Whether the finding extends to activation-level interventions is untested here.

## Affected pages

- [[Interpretability Evaluation]]
- [[Benchmark Optimization]]
- [[Anthropic]]

## Related pages

- [[LLM Reasoning]]
- [[LLM-as-a-Judge]]
- [[Multi-Turn Evaluation]]
- [[Reasoning Trace Privacy]]
- [[Agent Security and Governance]]

## Citations

- Raw capture: [[2026-08-28 Anthropic - Would This Change Your Answer - CHIVE]]
- Original: <https://alignment.anthropic.com/2026/chive/>
