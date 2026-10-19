---
type: entity
created: 2026-10-19
updated: 2026-10-19
entity_kind: organization
tags:
  - entity
  - organization
  - interpretability
source_ids:
  - src-2026-10-19-cammarata-networks-already-clean
status: active
---

# Goodfire

## What it is

An interpretability research organization. It publishes Nick Cammarata's essay
[[Nick Cammarata - Neural Networks Are Already Clean]] at its own domain, along with interactive
model microscopes. It also runs a research programme that includes the Block-Sparse Featurizer
vision work cited in that essay (Fel et al., 2026).

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

## Notes

- The essay is first-party advocacy; its cleanliness figures are threshold-dependent and
  preliminary. The author says the title overstates the evidence and states roughly 85%
  confidence in a change of kind, not an 85% share of clean mechanisms.
- Named contributors in the capture include Nick Cammarata and Curt Tigges, who did the
  language-model work with him. The acknowledgments thank further colleagues, including
  Thomas Fel, who is lead author of the Block-Sparse Featurizer work.
- The technical companion paper on language-model neurons is announced but not captured, so the
  vault holds the essay's summaries of those experiments, not their full methods.
- The essay recommends the continuous submanifolds found by the block-sparse featurizer work as a
  natural view of the residual stream, which has no privileged basis. So the organization does not
  reject learned decompositions outright; it argues they should come after studying the native
  mechanisms, not replace them.

## Related pages

- [[Nick Cammarata - Neural Networks Are Already Clean]]
- [[Mechanistic Interpretability]]
- [[Interpretability Evaluation]]
- [[Automated AI Research]]
- [[Qwen]]
- [[Anthropic]]
- [[OpenAI]]
