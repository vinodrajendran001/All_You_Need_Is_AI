---
type: concept
created: 2026-09-11
updated: 2026-09-11
tags:
  - concept
  - self-supervised-learning
  - architecture
  - theory
source_ids:
  - src-2026-09-07-rai-lejepa
status: active
---

# Joint-Embedding Predictive Architecture

## Definition

A self-supervised learning family in which a model predicts the *representation* of one view of an input
from another view, rather than reconstructing pixels or contrasting against negatives. The training
criterion has two clauses: a differentiable **predictive loss**, and the requirement that the learned
representation be **"not degenerate."**

The second clause is the whole subject. It is the only part of the criterion that is not a formula, and
the literature's anti-collapse machinery — stop-gradients, momentum encoders, predictors, register tokens
— exists to satisfy it without ever writing it down as a loss. The useful framing from
[[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]] is that SSL is "an optimization
problem with constraints, and the constraints are where the entire inductive bias of the method lives."

## Why it matters

**Dimensional collapse is the failure that matters because it is silent.** Complete collapse — a constant
encoder — is loud. Dimensional collapse is the encoder quietly using a low-rank subspace: nothing in the
training run reports it, and it is a spectrum rather than a binary. A method can be slowly failing for an
entire run without any visible symptom.

The three existing families are distinguished by *where* the anti-collapse constraint lives, and two of
the three put it somewhere inconvenient. **Contrastive** methods push energy up explicitly — InfoNCE
splits cleanly into a predictive numerator and a repulsive denominator — at **O(B²K)** cost.
**Architectural** methods have **g ≡ 0**: the constraint has been moved into gradient surgery, where it
"cannot be inspected, weighted, or ported." **Regularisation-term** methods make an explicit
distributional claim, and are the only family where the constraint is a first-class object.

Even within that third family, moment-matching is provably insufficient. VICReg fails a specific test:
because `Cov(P) = Cov(Q) ⟹ g(P) = g(Q)`, any criterion constraining finitely many moments cannot fully
specify a distribution. That is true by construction, not a tuning failure.

## Current synthesis

**LeJEPA (Balestriero and LeCun) makes the informal clause a derived objective**, via six requirements:
the constraint must be a real loss term; fully specified; linear in both batch size and embedding
dimension; controlled by one knob; bounded in gradient; and **optimal for downstream tasks not yet
seen**. The last requirement is what converts the problem into distribution matching — `g = D(p_z ‖ Q)` —
and splits it into two independent questions.

**Which target distribution Q?** The linear-probe argument gives isotropy: holding the covariance trace
fixed, ridge-regression worst-case bias is governed by the *smallest* eigenvalue and the variance term
`(σ²/N)·Σ 1/λ_k` diverges as any eigenvalue approaches zero, so both point at maximising λ_min under a
fixed sum. But a linear probe only sees `ZᵀZ`, so isotropy is all it can ask for — "exactly the result
VICReg already had." A **radius-based k-NN probe** goes further: its neighbourhood bias is proportional to
`∇log p`, which integrates to **Fisher information** `J(p) = ∫‖∇log p‖² p dz`, and the classical bound
`J(p) ≥ tr(Σ⁻¹)` holds **with equality if and only if p is Gaussian**. Combining the two gives
**Q = N(0, σ²I_K)**, cross-checked by maximum entropy under a covariance constraint. The intuition Rai
offers: **"You are building a searchlight before you know where you will need to look."**

**Which divergence D?** Reframe distribution matching as a **hypothesis test** and use the test statistic
as the loss — "training the encoder until a statistician could no longer distinguish its embeddings from
Gaussian samples." Uniquely among loss choices this supplies a *scale*, since the statistic can be
compared against a critical value. Direct multivariate testing is hopeless (256 samples in 1024
dimensions); the escape is **Cramér–Wold (1936)**: matching every one-dimensional projection implies
matching the distributions. **SIGReg** samples M random unit directions, runs a cheap univariate
Epps–Pulley characteristic-function test on each, and **averages** — noting explicitly that the maximum
is the statistically correct test but gives a sparse gradient.

**The implementation is what makes the scalability claim credible.** `global_step` seeds the direction
generator so every device draws the same directions with **no communication**; directions resample every
step; after the projection the embedding dimension **never appears again**; a 17-point grid on [−5, 5]
uses `exp(-0.5*t**2)` as both the Gaussian characteristic function and the window; one all-reduce of an
(M, T) array "is the entire distributed story." **Boundedness is visible in the code**: the empirical
characteristic function has magnitude at most one, so no single input can dominate the statistic —
whereas a kurtosis penalty would let an embedding at 10⁶ contribute 10²⁴. Cost is `O(N·M·(K+T))`,
measured at ~**0.47 ms** forward-backward on a V100 at N=M=512 and only ~0.67 ms at M=8192. The full loss
is about 8 lines, with **no predictor and no second network**.

**The empirical claims worth carrying.** **50 timm architectures under 20M parameters from 8 families all
land between 91.5% and 95% top-1** on ImageNet-10 with one λ, stable across two orders of magnitude, and
competitive at batch size 128. Predictor, teacher–student asymmetry, and register tokens are all
removable — significant because prior work found removing predictors yields chance-level encoders. **The
training loss correlates with downstream linear-probe accuracy at ~85% Spearman, rising to ~99%** under
the rescaling `C(α) = ρ_s(train_loss/λ^α, test_accuracy)` at α ≈ 0.4, enabling **label-free model
selection** — the loss "does not predict performance, it measures it."

**Small-data results are the strongest.** On **Galaxy10 (11,000 samples)** a LeJEPA ResNet-34 scores
**78.17 frozen against DINOv3's 71.38 and DINOv2's 67.62**, and 83.28 finetuned against 81.60 and 78.34:
a 21M-parameter model trained from scratch on eleven thousand images beating a model pretrained on 1.7
billion. Flowers102, with 1,020 training samples, reaches 82.19 with a ResNeXt-26. At scale it is
competitive rather than dominant — **77.1% on ImageNet-1k with ViT-L (0.3B)**, 78.5% with
ConvNeXtV2-Huge, and an eight-dataset transfer average of **79.48 against I-JEPA's 78.50** with half the
parameters and 100 epochs against 300.

**The transferable lesson is the method, not the model.** When a criterion contains an informal clause,
make it a distribution-matching objective, derive the target from what the downstream probe needs, and
pick the divergence by choosing a hypothesis test. As Rai puts it, the heuristics **"were never wrong,
they were unnamed."**

## Open questions

- **The decisive experiment has not been run**: there is no matched-compute comparison against DINOv2 or
  DINOv3. Galaxy10 compares from-scratch training against transferred features, which is a different
  question.
- "One hyperparameter" means one *anti-collapse* knob. Learning rate, weight decay, batch size,
  augmentation and architecture are all still tuned.
- Vision only. Language is the obvious next move and the hardest case, because **LLM embeddings are
  famously anisotropic (the cone effect)** — and that anisotropy may encode real token-frequency
  structure, "or the cone is dimensional collapse we have been rationalizing for years because we had no
  principled reason to object." LeJEPA supplies the principled reason to object without settling which
  reading is right.
- Isotropy is correct **only if you are genuinely not betting** on the downstream task. A task-informed
  anisotropic Q is named as the most actionable gap, and nobody has built one.
- SIGReg averages over directions instead of maximising, admitted as a departure from the correct test.
  What the averaged statistic misses is uncharacterised.
- Open whether SIGReg's induced isotropy removes the need for the Hadamard rotation used in quantisation
  schemes like TurboQuant — see [[Model Quantization and Efficiency]].

## Related pages

- [[World Models]]
- [[Neural Network Fundamentals]]
- [[Embedding Model Selection]]
- [[Model Quantization and Efficiency]]
- [[Diffusion Models]]
- [[Flow Matching]]
- [[Vision-Language Grounding]]
- [[Video Transformers]]
- [[Interpretability Evaluation]]
- [[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]]
