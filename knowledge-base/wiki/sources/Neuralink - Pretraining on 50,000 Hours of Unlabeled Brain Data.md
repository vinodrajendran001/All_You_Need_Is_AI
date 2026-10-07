---
type: source-summary
created: 2026-10-07
updated: 2026-10-07
source_id: src-2026-10-01-neuralink-unlabeled-brain-pretraining
source_title: "Pretraining on 50,000 Hours of Unlabeled Brain Data"
source_author: Neuralink
source_url: https://neuralink.com/updates/pretraining-on-50000-hours/
tags: [source/summary, representation-learning, recurrent-models, brain-computer-interface]
source_ids: [src-2026-10-01-neuralink-unlabeled-brain-pretraining]
status: active
---

# Neuralink - Pretraining on 50,000 Hours of Unlabeled Brain Data

## Summary

Neuralink reports self-supervised neural-signal pretraining followed by lightweight labeled
calibration for cursor control. More than **50,000 hours** describes the pooled available corpus;
**all live results in the article use participant-specific encoders pretrained on that participant's
recordings**. This is a first-party engineering report, not evidence of a deployed universal brain
model or broad clinical efficacy.

## Key claims

- The first participant supplied **9,000+ hours and 22.4 billion spikes**. Unlabeled daily-use
  recordings provide much more training signal than short supervised calibration sessions.
- Channel-specific spike embeddings feed a variable-activity Perceiver input stage and a **Mamba**
  temporal model. Spatially masked **auto-Poisson regression** observes half the channels and
  predicts the other half. Deployment is fully causal and designed for low latency.
- Six participants set personal cursor-control records, and three exceeded the previous
  **10.39 BPS** reference. One reached **11.32 BPS**, which Neuralink calls a BCI record.
  BPS here is task-specific information transfer combining cursor speed and accuracy, not
  neural bandwidth or arbitrary thought decoding.
- Some participants reduced calibration from **10 minutes daily to 10 minutes weekly**.
  The older overall average of **55 minutes weekly** is a different statistic.
- In the shown comparison, **30 seconds of labeled embeddings** performs comparably to
  **3.5 minutes of labeled raw spikes**, including next-month generalization. This is not a
  universal data-efficiency ratio across participants and tasks.
- Some decoders remained strong for more than three weeks. One **20-month-old calibration**
  remained usable, which does not establish record-level performance maintained for 20 months.
- The robotic-arm example runs in **simulation**, not a demonstrated physical robot deployment.
- Pooled multi-participant models have **not improved online performance**. One transfer experiment
  from participant P9 to P2, with **99% of weights frozen**, outperformed P2's previous decoder;
  it does not establish universal cross-participant transfer.

## Why it matters

The report extends the vault's representation-learning and recurrent-state material beyond language.
Its deployment question is whether unlabeled pretraining reduces labeled calibration and remains
useful as recordings change, not whether a model generates fluent output.

## Tensions / open questions

One-shot/zero-shot calibration and a universal motor interface remain goals. Cursor teleportation is
preliminary, with an initial result above 10 BPS rather than pixel-perfect control. The report does
not isolate every architecture/training component in matched ablations, and its available pooled
corpus must not be described as the training set of every reported encoder.

## Affected pages

- [[Neuralink]]
- [[Linear Attention and Recurrent Memory]]

## Raw capture

- [[Pretraining on 50,000 Hours of Unlabeled Brain Data]]

## Citations

- Canonical URL: <https://neuralink.com/updates/pretraining-on-50000-hours/>
- Published October 1 and captured October 6, 2026.

## Related pages

- [[Joint-Embedding Predictive Architecture]]
- [[Video Pre-training for Robot Policies]]
- [[Neural Network Fundamentals]]
