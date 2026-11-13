---
type: concept
created: 2026-10-07
updated: 2026-11-13
tags: [concept, alignment, post-training, evaluation]
source_ids:
  - src-2026-10-06-arush-self-modeling-emergent-misalignment
  - src-2026-08-28-anthropic-chive-counterfactual-explanations
  - src-2026-08-30-openai-hugging-face-incident
  - src-2026-11-03-astwei-teaching-qwen-why
  - src-2026-11-06-nous-arete-27b
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
That check matters because one variant failed it. In a follow-up on Qwen3-14B-Instruct, GPT-5.6
Terra's difficult advice rewritten to refuse without explanation left the model acting in fewer than
half of the evaluation transcripts, so it often avoided harm by not acting. Given that the model
acted, the refusal versions were less effective for both teachers. The authors conclude that refusal
is not what makes difficult advice work, consistent with TCW's claim that teaching the model *why*
matters.

Persona experiments sharpen the identity question raised above without settling it. The
instruction-tuned model was less misaligned under every AI-assistant name than under every human name.
Stories with an AI protagonist beat the same stories rewritten with a human protagonist. Naming the
protagonist after a real assistant, Qwen or Claude, made stories *less* effective than a generic AI.
The authors suggest, while saying they "are not certain of this explanation", that stories shape the
model's expectations "of AIs in general rather than of a particular AI persona", which is a self-model
claim that is interpretive, not causally isolated.

Three cautions keep this alongside, not opposed to, the results above. The outcome is a harmful-action
rate in simulated scenarios, not the eight-question EM score, so the two literatures do not share a
metric. The size of the effect depended heavily on which model wrote the training data (see
[[Knowledge Distillation]]). The evaluation is one suite whose scenarios are fictional, even though the
agent uses tools. Within those limits, the study shows that alignment-side generalization
from non-agentic data reaches a tool-using setting. It does not show that narrow fine-tuning is safe:
the same base family can generalize in either direction depending on the data.

## A narrow values fine-tune measured only near its target

[[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]]
is a narrow intervention of the kind this page is about, although it is not a study of the effect.
Nous fine-tuned Qwen3.8-27B on teacher answers to about twenty thousand prompts in seven
political-values categories. It measured the result on an 803-prompt evaluation in the same
categories, after removing training prompts that overlapped the evaluation, and on two capability
benchmarks. The targeted behavior moved: answers adopting the Chinese state's account fell from
**22%** to **0.9%**, and the capability scores were roughly unchanged.

The release does not measure what this page asks about. It reports no behavior outside the target
topics, such as refusals, safety responses, or political topics beyond the seven categories. Its
finding of "no capability regression anywhere we looked" is bounded by where it looked. The contrast
with astwei above is in what was measured. That study trained on non-agentic data and tested
out-of-distribution agentic behavior. Arete tested within its training domain plus general
capability. The release neither shows nor rules out broader behavioral change.

## Open questions

- Which effects survive more seeds, domains, longer trajectories, and genuinely tool-using tests?
- What separates self-model-specific effects from benign training, capability restoration, or
  changes in the effective training-data mixture?
- Can interventions improve several safety and capability measures without transferring unwanted
  behavior through the self-reports themselves?
- If narrow data can push generalization in both directions, can the same evaluation measure both? No
  source here runs the EM score and an agentic harmful-action suite on one checkpoint.
- Does a narrow values fine-tune such as Arete's shift behavior outside its topic set, for example
  refusals or safety responses? Its release measures only the target domain and general capability.

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
- [[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]]
