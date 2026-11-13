---
type: entity
created: 2026-10-19
updated: 2026-11-13
entity_kind: organization
tags:
  - entity
  - organization
  - interpretability
source_ids:
  - src-2026-10-19-cammarata-networks-already-clean
  - src-2026-11-10-goodfire-neurons-interpretable-basis
status: active
---

# Goodfire

## What it is

An interpretability research organization. It publishes Nick Cammarata's essay
[[Nick Cammarata - Neural Networks Are Already Clean]] at its own domain, along with interactive
model microscopes. It also runs a research programme that includes the Block-Sparse Featurizer
vision work cited in that essay (Fel et al., 2026). Its technical paper [[Curt Tigges et al - Neurons as an Interpretable Basis]] opens a series on
"native interpretability": studying a network through its own units rather than through a
replacement model.

## Why it matters here

Goodfire is the vault's first source arguing that native neurons, rather than learned replacement
models, should be the starting unit of [[Mechanistic Interpretability]]. Its essay pairs a
historical re-reading of vision models with preliminary audits of language-model neurons in
Qwen3-32B and Kimi K3. The vault does not treat this as settled. It is a counterweight to the
superposition-first framing and to the null result for activation readers recorded in
[[Interpretability Evaluation]].

The organization's methods lean on agents: they write neuron explanations, generate positive and
near-miss controls, group neurons and experts, and review attribution graphs at scale. That makes
Goodfire a concrete case for [[Automated AI Research]] applied to interpretability, and it means
agent-assisted labeling is part of what its numbers measure.

The companion paper turns the essay's claims into measurements on **Qwen3.6-35B-A3B**, an open
[[Mixture of Experts]] model. It reports that routed neurons are functionally sparse, that most
neuron poles have one dominant mode, and that agent-written descriptions pass held-out detection,
classification, simulation and synthesis tests. Its agent harness, the Neuron Scientist, runs on
frontier models and iterates hypotheses and experiments for each neuron. Goodfire released a public
neuron atlas for **2,734** stratified neurons and low-effort labels for all 10 million neuron-poles.
This makes the organization a supplier of open interpretability data on a [[Qwen]] model, not only
of arguments.

## Notes

- The essay is first-party advocacy; its cleanliness figures are threshold-dependent and
  preliminary. The author says the title overstates the evidence and states roughly 85%
  confidence in a change of kind, not an 85% share of clean mechanisms.
- Named contributors in the capture include Nick Cammarata and Curt Tigges, who did the
  language-model work with him. The acknowledgments thank further colleagues, including
  Thomas Fel, who is lead author of the Block-Sparse Featurizer work.
- The essay announced a technical companion paper on language-model neurons. As of 2026-11-10 it is
  captured as [[Curt Tigges et al - Neurons as an Interpretable Basis]], by Curt Tigges, Matthew Kowal, Thomas McGrath, Owen Lewis and Nick Cammarata.
  Before that, the vault held only the essay's summaries of those experiments. The paper measures a
  different model and metric from the essay's Qwen3-32B audits: **69%** of poles are dominated by
  one mode, against the essay's roughly 90% with one main job. So it does not directly confirm the
  essay's figure.
- The paper is also first-party. LLMs build and judge most of its measurements, and its fine-tuned
  sparse model is compared with the untrained base rather than with an equally trained full model.
- The essay recommends the continuous submanifolds found by the block-sparse featurizer work as a
  natural view of the residual stream, which has no privileged basis. So the organization does not
  reject learned decompositions outright; it argues they should come after studying the native
  mechanisms, not replace them.

## Related pages

- [[Nick Cammarata - Neural Networks Are Already Clean]]
- [[Curt Tigges et al - Neurons as an Interpretable Basis]]
- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Automated AI Research]]
- [[Mixture of Experts]]
- [[Transformer Architecture]]
- [[Qwen]]
- [[Anthropic]]
- [[OpenAI]]
