---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-09-29-raschka-text-classification-jev
source_title: "Language Models for Text Classification: From Bag-of-Words to Jev"
source_author: Sebastian Raschka
source_url: https://magazine.sebastianraschka.com/p/classifier-history-and-jev
tags: [source/summary, decision-models, evaluation, training, inference]
source_ids: [src-2026-09-29-raschka-text-classification-jev]
status: active
---

# Sebastian Raschka - Language Models for Text Classification - From Bag-of-Words to Jev

## Summary

Raschka places typed decision models in the history of text classification, independently tests Jev
on IMDb, and explains calibration objectives without claiming to know Jev's proprietary method.
He states that he is unaffiliated with TypeSafe and received no free access. "PhD" in the clipping's
author array is a credential, not a second author.

## Key claims

The historical tutorial compares bag-of-words logistic regression (**89.9%**), a scratch LSTM
(**85.66%**), a CNN (**90.07%**), cited ULMFiT (**95.4%**), ModernBERT (about **95%**), and GPT-2
124M (about **92%**). These use different setups; the figures are not architecture ceilings.

His **jev-1.13.0** evaluation uses **25,000 IMDb test reviews**:

| Interface | Accuracy | Correct reviews | Elapsed time | Input tokens | Reported cost |
| --- | --- | --- | --- | --- | --- |
| Choice | 96.47% | 24,117 | 22m24s | 15,456,663 | $0.6492 |
| Noul | 96.20% | 24,050 | 23m03s | 15,106,663 | $0.6345 |

- Runs are nondeterministic and IMDb training contamination is unknown. The small Choice/Noul gap
  is not shown to be statistically meaningful.
- ModernBERT achieved comparable accuracy on a DGX Spark with **23 minutes of fine-tuning plus
  seven minutes of evaluation**. Training time and inference time must not be merged into an
  inference-latency comparison.
- Follow-up IMDb trials gave **CLM 82.90%** and **Laya 92.33%**; both also failed his Tetris
  demonstration. Those observations test transfer to his tasks, not the validity of every
  task-specific benchmark published by their authors.
- Choice probabilities describe mutually exclusive options. Its separate `confidence` field
  summarizes distribution concentration, **not the winning option's probability**. Noul questions
  have independent probabilities and need not sum to one.
- A scalar scoring head over text, task, and candidate can support a variable label set. Matching
  that interface does not establish generalization to arbitrary new tasks.
- Jev's architecture, training mixture, and Reinforcement Learning for Calibrated Decisions
  (RLCD) remain undisclosed. A ModernBERT-like design is Raschka's hypothesis. The statement that
  training data is **100% synthetic** is attributed to the vendor.

## Calibration is an objective, not a disclosed Jev recipe

Raschka discusses the separate published method **Reinforcement Learning with Calibration Rewards
(RLCR)**, using `R = c - (q-c)^2`, where `c` indicates correctness and `q` is reported confidence.
An incorrect answer at 0.9 receives **-0.81**, at 0.2 **-0.04**, and a correct answer at 0.9 **0.99**.

The cited RLCR paper reports HotpotQA expected calibration error **0.37 to 0.03**, with accuracy
**62.1% versus 63.0%**. Across six other datasets, mean calibration error falls **0.46 to 0.21**
while accuracy rises **53.9% to 56.2%**. These are **RLCR results, not Jev results**, and no
official connection to RLCD is established.

Cross-entropy and Brier loss are both proper scoring rules with the same ideal probability optimum.
A setup-specific benefit from adding Brier loss does not show that cross-entropy cannot calibrate
or that reinforcement learning is necessary. Temperature scaling preserves the argmax; probability
calibration and the policy threshold that acts on it are different decisions.

## Why it matters

This source adds independent task evidence where the vault previously held vendor claims and
competitor comparisons. It also supplies the mathematical correction needed to evaluate explanations
that portray calibrated decision models as requiring an entirely new learning principle.

## Tensions / open questions

IMDb accuracy does not establish calibration, contamination-free generalization, agent reliability,
or broad Jev superiority. A September 29 update describes OpenAI's Decisions API as a **limited
preview**, not demonstrated general availability. The vendor recipe remains unknown despite plausible
reconstructions and the availability of open alternatives.

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[TypeSafe AI]]
- [[Sebastian Raschka]]
- [[Siddhant Rai]]
- [[Model Routing]]
- [[Agent Delegation]]
- [[Inference Efficiency Frontier]]
- [[Reward Design for RL]]
- [[Transformer Architecture]]

## Raw capture

- [[Language Models for Text Classification From Bag-of-Words to Jev]]

## Citations

- Canonical URL: <https://magazine.sebastianraschka.com/p/classifier-history-and-jev>
- Published September 29 and captured September 30, 2026.

## Related pages

- [[Siddhant Rai - Jev - Models Built for Decisions Rather Than Text]]
- [[Jacky Kwok et al - Contrastive Language Models]]
- [[Nandakishor M - Non-Autoregressive Decision Models and Laya]]
- [[LLM-as-a-Judge]]
