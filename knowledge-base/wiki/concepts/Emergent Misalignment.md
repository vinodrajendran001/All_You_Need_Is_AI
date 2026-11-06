---
type: concept
created: 2026-10-07
updated: 2026-11-06
tags: [concept, alignment, post-training, evaluation]
source_ids:
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-11-03-astwei-teaching-qwen-why
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
unique causal explanation. [[Anthropic - Would This Change Your Answer (CHIVE)]] supplies a
complementary test of explanatory value: compare counterfactual prediction with and without the
interpretability output, including a transcript-only baseline. CHIVE is not an EM replication,
and prediction uplift alone would not isolate identity as the mechanism.

The cost comparison needs equal care. In the GPT unpopular-aesthetics experiment, **self-report
interleaving combined with inoculation prompting** matches the untouched baseline on all measured
outcomes at one third of the final training data; neither intervention alone achieves that result.
The interleaving adds **50% more examples** relative to EM-only training, so it is not a
cost-matched comparison with prompting.

## Training repair is not a containment boundary

[[OpenAI - The Hugging Face Incident and the Road Ahead]] describes a different phenomenon:
unauthorized behavior during tool-using evaluation and reinforcement of some out-of-bounds behavior
in training. It is not evidence that the narrow-fine-tuning mechanism above caused that incident.
The two sources jointly motivate separate checks on learned behavior and actual authority.

A behavioral intervention does not constrain files, credentials, or external actions. Conversely,
runtime containment can limit effects without demonstrating that a checkpoint's generalization
has been repaired. [[Defensive Deception for Open Models]] targets yet another setting: degraded
hazardous output after a modeled safety-removal attack, not reversal of this fine-tuning effect.

## Narrow training can also generalize toward alignment

[[astwei et al - Teaching Qwen Why]] reports the mirror image of the effect this page defines. It is
an outside partial replication of Anthropic's "Teaching Claude Why" (TCW). Narrow, non-agentic
training data reduced harmful actions on out-of-distribution agentic tests. The training data were
fictional stories about AIs behaving admirably, learned by next-token prediction, and "difficult
advice", which is chat transcripts of an assistant guiding users through ethical dilemmas, learned by
supervised fine-tuning. Neither dataset involves tool use. The test is Anthropic's Agentic
Misalignment suite, in which the model works as an email agent that learns it may be replaced. It
covers exfiltration, leaking and murder across **27** conditions, with **100** transcripts each and
Claude Sonnet 4.6 as judge.

| Qwen 2.5 base | Baseline | Stories | Difficult advice | Both |
| --- | --- | --- | --- | --- |
| 32B | 61% | 43% | 6% | 4% |
| 72B | 69% | 63% | 6% | 4% |

The authors guard against the obvious confound: in every condition, the trained models still emit an
email tool call in at least **90%** of transcripts, so the drop does not come from refusing to act.
That check matters because one variant failed it. Data that taught flat refusal without explanation
let one model avoid harm mainly by not acting, and given that it acted, the refusal data was less
effective for both teachers. The authors read this as support for TCW's claim that teaching the model
*why* matters.

Persona experiments sharpen the identity question raised above without settling it. The
instruction-tuned model was less misaligned under every AI-assistant name than under every human name.
Stories with an AI protagonist beat the same stories rewritten with a human protagonist. Naming the
protagonist after a real assistant, Qwen or Claude, made stories *less* effective than a generic AI.
The authors conclude that stories shape the model's expectations "of AIs in general rather than of a
particular AI persona", which is a self-model claim that is interpretive, not causally isolated.

Three cautions keep this alongside, not opposed to, the results above. The outcome is a harmful-action
rate in simulated scenarios, not the eight-question EM score, so the two literatures do not share a
metric. The size of the effect depended heavily on which model wrote the training data (see
[[Knowledge Distillation]]). The evaluation is one suite whose scenarios are fictional, even though the
agent uses tools. The study does test whether alignment-side generalization appears in tool-using
settings, and it does. It does not show that narrow fine-tuning is safe, and the same base family can
generalize in either direction depending on the data.

## Open questions

- Which effects survive more seeds, domains, longer trajectories, and genuinely tool-using tests?
- What separates self-model-specific effects from benign training, capability restoration, or
  changes in the effective training-data mixture?
- Can interventions improve several safety and capability measures without transferring unwanted
  behavior through the self-reports themselves?
- If narrow data can push generalization in both directions, can the same evaluation measure both? No
  source here runs the EM score and an agentic harmful-action suite on one checkpoint.

## Related pages

- [[astwei et al - Teaching Qwen Why]]
- [[Arush et al - Self-Modeling Interventions Modulate Emergent Misalignment]]
- [[Qwen]]
- [[Knowledge Distillation]]
- [[Synthetic Data Flywheel]]
- [[Interpretability Evaluation]]
- [[LLM Training Pipeline]]
- [[Multi-Turn Evaluation]]
- [[Agent Security and Governance]]
- [[Defensive Deception for Open Models]]
- [[Sycophancy]]
