---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-07-rai-lejepa
source_title: "LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics"
source_author: Siddhant Rai
source_url: https://vizuara.substack.com/p/lejepa-provable-and-scalable-self
tags:
  - source/summary
  - topic/self-supervised-learning
  - topic/architecture
  - topic/theory
source_ids:
  - src-2026-09-07-rai-lejepa
status: active
---

# Siddhant Rai - LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics

## Summary

A long derivation-first tutorial on Balestriero and LeCun's LeJEPA, written as an argument that
self-supervised learning is **"an optimization problem with constraints, and the constraints are where
the entire inductive bias of the method lives."**

The framing is a crack in the JEPA criterion itself. It has two clauses: a differentiable predictive loss,
and the English phrase **"not degenerate."** As Rai puts it, "that crack between a clause you can compute
and a clause you can only gesture at is... the entire subject of this article." Every anti-collapse
heuristic in the SSL literature — stop-gradients, momentum encoders, predictors, register tokens — exists
to fill that gap without ever writing it down as a loss.

LeJEPA writes it down. The construction proceeds in two independent halves — **which distribution should
embeddings match** (answer: an isotropic Gaussian) and **how should you measure the mismatch** (answer: a
statistical hypothesis test) — and the separability of those two questions is itself treated as evidence:
"That separability is usually a sign the framing is correct."

The empirical payoff is a single hyperparameter, a loss that is **~8 lines of code with no predictor and
no second network**, and **training loss that correlates with downstream accuracy** — enabling model
selection without labels.

## Key claims

### The problem

**Dimensional collapse is the dangerous failure because it is silent.** Complete collapse — a constant
encoder — is loud and obvious. Dimensional collapse is the encoder using a low-rank subspace: **"nothing
in your training run will tell you it is happening,"** and it is a spectrum rather than a binary.

**Existing methods fall into three families, distinguished by where the constraint lives.** Contrastive
methods push energy up explicitly — InfoNCE "splits cleanly" into a predictive numerator and a repulsive
denominator — at **O(B²K)** cost. Architectural methods have **g ≡ 0**: the constraint has been moved into
gradient surgery, where it "cannot be inspected, weighted, or ported." Regularisation-term methods make a
global distributional claim.

**VICReg fails a specific, provable test.** Because `Cov(P) = Cov(Q) ⟹ g(P) = g(Q)`, any criterion
constraining finitely many moments cannot fully specify a distribution. This is not a tuning problem; it
is true by construction.

### Six requirements for a real anti-collapse term

The constraint must (1) exist as an actual loss term; (2) be fully specified, which rules out
moment-matching; (3) scale linearly in both batch size B and embedding dimension K — contrastive is
O(B²K), whitening O(BK²); (4) have one knob; (5) have bounded gradients; and (6) be **optimal for
downstream tasks not yet seen.**

**Requirement six is what converts the problem into a distribution-matching problem**, since it forces g
to be `D(p_z ‖ Q)` for some target Q.

### Which Q?

**The linear-probe argument gives isotropy.** Holding `tr(Cov(Z)) = κ` fixed, ridge-regression bias per
coordinate is `−s_k β*_k` with `s_k = λ/(Nλ_k + λ)`; worst-case over the unknown `‖β*‖` is governed by the
*smallest* eigenvalue, so minimising worst-case bias means maximising `λ_min` under a fixed trace — which
gives isotropy. The variance term `tr(Var(β̂)) = (σ²/N)·Σ 1/λ_k` gives the same answer and **diverges as
any eigenvalue approaches zero**.

**But a linear probe cannot ask for more than isotropy** — it only sees `ZᵀZ`, so "that is exactly the
result VICReg already had."

**A radius-based k-NN probe gives the Gaussian, and it is unique.** The neighbourhood average is biased in
proportion to `∇log p`; integrating gives **Fisher information** `J(p) = ∫‖∇log p‖² p dz`. The classical
bound `J(p) ≥ tr(Σ⁻¹)` holds **with equality if and only if p = N(0, Σ)** — so among all distributions
with a given covariance, the Gaussian uniquely minimises the k-NN probe's bias.

**Combining the two gives Q = N(0, σ²I_K)**, and the same answer falls out of maximum entropy under a
covariance constraint. Rai's metaphor for what isotropy is doing: **"You are building a searchlight before
you know where you will need to look."**

### Which D?

**Reframe distribution matching as a hypothesis test and use the test statistic as the loss** — "training
the encoder until a statistician could no longer distinguish its embeddings from Gaussian samples."
Uniquely among loss choices, this gives a **scale**: the value can be compared against a critical value.

**Direct multivariate testing is hopeless** — 256 samples in 1024 dimensions.

**Cramér–Wold (1936) is the escape**: matching every one-dimensional projection implies matching the
distributions.

**SIGReg samples M random unit directions, runs a cheap univariate Epps–Pulley characteristic-function
test on each, and averages.** Rai flags the deliberate compromise: **the maximum over directions is the
statistically correct test, but averaging is used because the max gives a sparse gradient.**

**The implementation details carry the scalability claims.** `global_step` seeds the direction generator
so every device draws the *same* directions with **no communication**, and directions are resampled every
step. After the projection `x @ A`, **K never appears again**. A 17-point grid on [−5, 5] is used, where
`exp(-0.5*t**2)` serves as both the Gaussian characteristic function and the window. **One all-reduce of
an (M, T) array "is the entire distributed story."**

**Boundedness is visible in the code, not just in a theorem.** The empirical characteristic function has
magnitude at most one, so **"no single input can dominate this statistic"** (Theorem 4) — whereas a
kurtosis penalty would let an embedding at 10⁶ contribute 10²⁴.

**Cost is `O(N·M·(K+T))` and small in practice**: ~**0.47 ms** forward-backward on a V100 at N=M=512, and
only ~**0.67 ms at M=8192**.

### Results

**Architecture-independence is the strongest empirical claim.** **50 timm architectures under 20M
parameters from 8 families all land between 91.5% and 95% top-1** on ImageNet-10 with a single λ, and λ is
stable across two orders of magnitude. It remains competitive at **batch size 128**.

**Every heuristic is removable.** Predictor, teacher–student asymmetry and register tokens can all be
dropped — significant because prior work found that removing predictors yields chance-level encoders.

**Training loss predicts downstream accuracy without labels.** Spearman correlation between training loss
and linear-probe accuracy is **~85%**, rising to **~99%** under the rescaling
`C(α) = ρ_s(train_loss/λ^α, test_accuracy)` at **α ≈ 0.4**.

**It beats far larger pretrained models in the small-data regime.** On **Galaxy10 (11,000 samples, 10
classes)**, a LeJEPA ResNet-34 scores **78.17 frozen against DINOv3's 71.38 and DINOv2's 67.62**, and
**83.28 finetuned against 81.60 and 78.34**. Rai's summary: **"A 21M-parameter model trained from scratch
on eleven thousand images beats a model pretrained on 1.7 billion."** Flowers102, with **1,020 training
samples**, reaches 82.19 with a ResNeXt-26.

**At scale it is competitive rather than dominant**: **77.1% on ImageNet-1k with ViT-L (0.3B)** and
**78.5% with ConvNeXtV2-Huge (0.6B)**; transfer across eight datasets averages **79.48 against I-JEPA's
78.50** with half the parameters and **100 epochs against 300**. A 1.8B ViT-gigantic trains stably.
Emergent PCA object–background separation and unsupervised video object tracking are reported.

## Why it matters

The durable idea here is not LeJEPA specifically. It is the **method**: when a criterion contains an
informal clause, make the clause a distribution-matching objective, derive the target distribution from
what the downstream probe needs, and pick the divergence by choosing a hypothesis test. Both halves are
derived rather than tuned, and the tutorial's own gloss is the best statement of what that buys — the
heuristics **"were never wrong, they were unnamed."**

The **label-free model selection** result is the most immediately usable finding and deserves emphasis
precisely because it is stated carefully. Rai's phrasing is that the loss **"does not predict
performance, it measures it."** For a field where SSL pretraining quality is normally only knowable after
a labelled evaluation, an ~85% (rescaled ~99%) Spearman correlation changes the development loop.

The **bounded-gradient-visible-in-the-code** point is a small but transferable piece of engineering
judgement: a statistic built from a bounded function cannot be dominated by an outlier, and you can see
that from the implementation rather than trusting a theorem. That argument transfers to any loss built on
characteristic functions.

The final open question is the one with the widest reach: **LLM embeddings are famously anisotropic (the
cone effect)**, and that anisotropy may encode real token-frequency structure — **"Or the cone is
dimensional collapse we have been rationalizing for years because we had no principled reason to
object."** LeJEPA supplies, for the first time, the principled reason to object.

## Tensions / open questions

- **The decisive experiment has not been run.** There is no matched-compute comparison against DINOv2 or
  DINOv3. The Galaxy10 result compares a from-scratch model against transferred features, which is a
  different question from "is LeJEPA a better pretraining objective at equal compute."
- **"One hyperparameter" is narrower than it sounds.** It excludes learning rate, weight decay, batch
  size, augmentation policy, and architecture. What is removed is the *anti-collapse* knob, not tuning.
- Vision only. Language is the obvious next move, and it is exactly where the isotropy assumption is most
  contested.
- **Isotropy is correct only if you are genuinely not betting on the downstream task.** Rai names a
  task-informed anisotropic Q as the most actionable gap — the derivation assumes ignorance, and most
  practitioners are not fully ignorant.
- SIGReg averages over directions rather than maximising, which is admitted as a departure from the
  statistically correct test. What the averaged statistic misses is not characterised.
- Open: whether SIGReg's isotropy removes the need for the Hadamard rotation used in quantisation schemes
  like TurboQuant — a connection to [[Model Quantization and Efficiency]] that is raised and left
  unresolved.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Joint-Embedding Predictive Architecture]]
- [[World Models]]
- [[Neural Network Fundamentals]]
- [[Model Quantization and Efficiency]]
- [[Siddhant Rai]]
- [[Vizuara]]

## Related pages

- [[Embedding Model Selection]]
- [[Diffusion Models]]
- [[Flow Matching]]
- [[Vision-Language Grounding]]
- [[Video Transformers]]
- [[Interpretability Evaluation]]

## Citations

- Raw capture: [[2026-09-07 Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]]
- Source: <https://vizuara.substack.com/p/lejepa-provable-and-scalable-self>
- Paper: Balestriero and LeCun, *LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics*
