---
type: source-summary
created: 2026-10-30
updated: 2026-10-30
source_id: src-2026-10-28-sick-on-policy-self-training
source_title: "On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models"
source_author: Leon Sick, Lukas Hoyer, Yannick Strümpler, Christian Reisswig, Timo Ropinski, and Federico Tombari
source_url: https://arxiv.org/html/2610.32770v1
tags:
  - source/summary
  - distillation
  - synthetic-data
  - self-improvement
source_ids:
  - src-2026-10-28-sick-on-policy-self-training
status: active
---

# On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models

## Summary

On-Policy Self-Training (OPST) combines model-generated curricula, consistency filters, and
privileged-information self-distillation. The text experiments start from hand-chosen coarse
topics rather than curated questions/answers or a stronger external teacher. A teacher sees
generated context that the student does not, and supervises the student's own answer
trajectories. The authors frame the result as amplification of existing knowledge, not creation
of independently verified new knowledge.

## Key claims

### The loop separates generation, filtering, and teaching

The generator is an exponential-moving-average (EMA) teacher or the frozen initial model, not
the student itself. It produces a question and candidate answer/rationale. Fresh-context
regeneration and question paraphrasing test answer consistency; a consensus gate removes
questions that all student rollouts already answer in agreement with the candidate.

The student receives only the question. The privileged teacher receives the additional
generated context and evaluates student-generated prefixes, yielding dense token-distribution
supervision rather than one terminal reward. The EMA teacher tracks the student and is the
**final evaluated checkpoint**. Curricula are regenerated across rounds with duplicate
removal. Neither consistency filter is a truth oracle.

### Results depend on the evaluation protocol

| Reported Gemma 4 E2B setting | Base | OPST | Meaning |
| --- | ---: | ---: | --- |
| MMLU, without thinking | 37.5 | 47.7 | +10.2 points; answer-option log-likelihood scoring |
| MMLU, with thinking | 69.9 | 71.1 | +1.2 points; parsed generated answers |
| GPQA, with thinking | 27.8 | 34.3 | Separate thinking evaluation |
| GSM8K, with thinking | 72.7 | 80.9 | Separate thinking evaluation |
| HellaSwag, with thinking | 63.1 | 65.6 | Separate thinking evaluation |

The paper reports three-seed E2B uncertainty, including **47.7 +/- 0.8** for no-thinking
MMLU. These protocols must not be mixed into one improvement claim. The Qwen3-4B-Base extension
reports an average **66.7 to 72.7 (+6.0)** without instruction tuning; it is a separate model
experiment, not a Qwen-family result.

### The ablations constrain the explanation

- No verification scores **42.7**; verification gives **45.4**; adding the consensus gate gives
  **47.7**. Retention and filtering affect which generated examples become useful training.
- No privileged information gives **40.6**, context from a different problem on the same
  topic **40.2**, answer-only context **44.6**, rationale-only **45.8**, and full context
  **47.7**. The mechanism needs sample-specific information, not merely topic-relevant context.
- The EMA teacher scores **47.7** versus the student's **45.9**. Changing teacher update rate
  matters; the final checkpoint identity is part of the method.
- More rounds do not keep compounding: **37.5** at baseline, **43.1** after three rounds,
  **47.7** after seven, and **46.2** after twelve or twenty.
- With both filters disabled, injecting 75% wrong answers lowers OPST from **42.7 to 40.8**
  and SFT from **38.8 to 33.1**. This is relative robustness in one ablation, not immunity
  to incorrect generated targets.

### Retention and visual inputs qualify the headline

The all-three-domain mixture improves the out-of-domain average by **0.8 points** but loses
**4.9 points on MATH-500**; the MMLU/HellaSwag mixture loses **8.5** there. Retention is mixed.

Visual OPST additionally consumes **unlabeled OpenImages V4 images**. Generated captions and
bounding-box spatial relations supply privileged context. Gemma 4 E2B rises from **49.1 to
56.0** on VQAv2 with captions plus spatial information, but E4B's spatial-only variant beats
the combined variant. Label-free is not external-input-free or universally best when combined.

## Why it matters

[[Knowledge Distillation]] can exploit an information asymmetry within one model lineage,
without requiring a more capable external teacher. [[Synthetic Data Flywheel]] gains a concrete
student-conditioned curriculum loop, while [[Recursive Self-Improvement]] gains a bounded
weight-update example with fixed human-designed rules. [[Continual Learning for Agents]] and
[[LLM Reasoning]] must retain the forgetting results and the authors' amplification interpretation.

## Tensions / open questions

- Coarse topics are hand selected, pretrained knowledge remains essential, and most experiments
  concern small models. Consistent misconceptions can survive every consistency check.
- A stopping rule without labeled validation remains open; the seven-round peak rules out
  reading the reported iterations as indefinite improvement.
- The captured generalized-divergence equation appears inconsistent between its mixture
  coefficients, KL weights, and stated limits. This summary records the qualitative dense
  self-distillation mechanism rather than silently repairing an executable formula; the
  original PDF equation needs checking before mathematical reuse.
- Raw author and publication metadata are empty. The author list is recovered from the paper
  body; the source ID uses the **October 28 capture date**, not an inferred publication date.

## Affected pages

- [[Knowledge Distillation]]
- [[Synthetic Data Flywheel]]
- [[Recursive Self-Improvement]]
- [[Continual Learning for Agents]]
- [[LLM Reasoning]]
- [[Qwen]]

## Raw capture

- [[knowledge-base/raw/sources/On-Policy Self-Training Data-Free Self-Improvement in Large Language Models]]

## Citations

- Captured paper: <https://arxiv.org/html/2610.32770v1>
- Authors: Leon Sick, Lukas Hoyer, Yannick Strümpler, Christian Reisswig, Timo Ropinski, and
  Federico Tombari. Publication date is not established by the capture metadata.

## Related pages

- [[Knowledge Distillation]]
- [[Synthetic Data Flywheel]]
- [[Recursive Self-Improvement]]
- [[Continual Learning for Agents]]
- [[LLM Reasoning]]
- [[Qwen]]
- [[Ali Behrouz and Vahab Mirrokni - The Sleep Framework]]
- [[RL Environment Design]]
