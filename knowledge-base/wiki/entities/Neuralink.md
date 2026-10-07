---
type: entity
entity_kind: organization
created: 2026-10-07
updated: 2026-10-07
tags: [entity, organization, brain-computer-interface, representation-learning]
source_ids:
  - src-2026-10-01-neuralink-unlabeled-brain-pretraining
status: active
---

# Neuralink

## What it is

Neuralink develops brain-computer interfaces. In this vault it is a source of first-party engineering
evidence about learning useful neural representations from unlabeled recordings and adapting them
to a person's control task.

## Why it matters here

[[Neuralink - Pretraining on 50,000 Hours of Unlabeled Brain Data]] extends the representation-learning
branch beyond text and vision. Its spike embeddings, Perceiver input stage, and Mamba temporal model
serve a causal low-latency decoder rather than a language-generation loop. The self-supervised task
predicts masked neural channels with auto-Poisson regression, not text tokens or JEPA embeddings.

The deployment test is practical: less labeled calibration, useful control, and stability as
recordings change. In the reported cursor task, six participants set personal records and one reaches
11.32 BPS. That unit combines speed and accuracy on the task; it is not a measurement of thought
bandwidth.

## Keep the corpus and deployment scopes separate

More than 50,000 hours is the pooled available corpus, while **every reported live encoder is
participant-specific**. Pooled multi-participant models have not improved online performance in
the account. One P9-to-P2 transfer experiment with 99% of weights frozen is promising but does not
erase that negative result.

The robotic-arm result is simulated. One-shot/zero-shot calibration and a universal motor interface
remain research goals. These boundaries make the report useful as an engineering case rather than
evidence of a universal neural decoder or broad clinical readiness.

## Related pages

- [[Neuralink - Pretraining on 50,000 Hours of Unlabeled Brain Data]]
- [[Linear Attention and Recurrent Memory]]
- [[Joint-Embedding Predictive Architecture]]
- [[Video Pre-training for Robot Policies]]
- [[Neural Network Fundamentals]]
