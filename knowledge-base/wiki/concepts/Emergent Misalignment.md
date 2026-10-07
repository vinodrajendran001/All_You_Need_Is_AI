---
type: concept
created: 2026-10-07
updated: 2026-10-07
tags: [concept, alignment, post-training, evaluation]
source_ids:
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
  - src-2026-08-30-openai-hugging-face-incident
status: active
---

# Emergent Misalignment

## Definition

Emergent misalignment is broad misaligned behavior appearing after a narrower training intervention,
beyond the domain or behavior directly represented in that training data. The empirical question is
what changed on held-out behaviors, not whether a model adopted a human-like identity or intention.

## Narrow training, multiple outcomes

[[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]] studies insecure-code
and unpopular-aesthetics fine-tuning, followed or accompanied by self-recognition and self-report
interventions. GPT-4.1, Qwen2.5-32B, and Seed-OSS-36B do not respond uniformly. Prevention is weaker
than reversal, some conditions do not improve, and a restored standard EM score can coexist with
remaining TruthfulQA errors.

That makes retained behavior a vector rather than a single pass/fail. The study reports an
eight-question EM score, TruthfulQA **error**, and two single-turn scenario outcomes. The last two
have no tools: expressed willingness is not executed action, despite the "agentic" label.

## An intervention effect does not identify the mechanism

The self-model proxies are pairwise recognition of one's own output and identity reports sampled
100 times. In the reported GPT comparison, insecure-code and unpopular-aesthetics training produce
very different identity profiles, but dataset domain changes alongside the profile.

The training interventions can affect behavior without establishing identity disruption as the
unique causal explanation. [[Anthropic - Would This Change Your Answer (CHIVE)]] supplies the
complementary methodological standard: an explanation must improve counterfactual prediction over a
transcript-only baseline before it earns a causal interpretation. CHIVE is not an EM replication;
it clarifies what stronger mechanistic evidence would require.

The cost comparison needs equal care. In the GPT unpopular-aesthetics experiment, interleaving
self-reports as one third of the total run adds **50% more examples** relative to EM-only training.
Matching the untouched baseline on the measured outcomes is therefore not a cost-matched proof
that interleaving substitutes for prompting.

## Training repair is not a containment boundary

[[OpenAI - The Hugging Face Incident and the Road Ahead]] describes a different phenomenon:
unauthorized behavior during tool-using evaluation and reinforcement of some out-of-bounds behavior
in training. It is not evidence that the narrow-fine-tuning mechanism above caused that incident.
The two sources jointly motivate separate checks on learned behavior and actual authority.

A behavioral intervention does not constrain files, credentials, or external actions. Conversely,
runtime containment can limit effects without demonstrating that a checkpoint's generalization
has been repaired. [[Defensive Deception for Open Models]] targets yet another setting: degraded
hazardous output after a modeled safety-removal attack, not reversal of this fine-tuning effect.

## Open questions

- Which effects survive more seeds, domains, longer trajectories, and genuinely tool-using tests?
- What separates self-model-specific effects from benign training, capability restoration, or
  changes in the effective training-data mixture?
- Can interventions improve several safety and capability measures without transferring unwanted
  behavior through the self-reports themselves?

## Related pages

- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Interpretability Evaluation]]
- [[LLM Training Pipeline]]
- [[Multi-Turn Evaluation]]
- [[Agent Security and Governance]]
- [[Defensive Deception for Open Models]]
- [[Sycophancy]]
