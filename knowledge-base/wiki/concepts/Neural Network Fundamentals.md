---
type: concept
created: 2026-05-18
updated: 2026-09-11
tags:
  - concept
  - neural-networks
  - pytorch
  - optimization
  - backpropagation
source_ids:
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-05-18-hanfang-pytorch-practice
  - src-2026-05-21-leetcode-templates
  - src-2026-06-03-fareed-khan-train-llm-from-scratch
  - src-2026-06-23-mayank-pratap-singh-diffusion-visual-breakdown
  - src-2026-06-30-alisa-liu-book-of-llms
  - src-2026-06-30-alisa-liu-math-notes
  - src-2026-07-01-anastasiia-alekseeva-parallel-training
  - src-2026-09-07-rai-lejepa
status: active
---

# Neural Network Fundamentals

## Definition

Neural network fundamentals are the small set of ideas that make modern deep learning work: tensors, linear layers, forward passes, loss functions, gradients, backpropagation, and iterative parameter updates through optimizers.

## Why it matters

This vault has several higher-level pages about LLMs and RL, but those topics depend on a compact substrate of optimization and implementation knowledge. The PocketFlow tutorials make that substrate explicit and teach it from first principles.

## Current synthesis

- The `nn` tutorial reduces learning to a simple loop: define an error surface, compute gradients, and repeatedly step downhill. It connects gradient descent, partial derivatives, and the chain rule into one story about assigning credit through layered computation.
- A durable takeaway from that lesson is that backpropagation is not a separate magical algorithm; it is just the **chain rule applied systematically through a computation graph**.
- The `pytorch` tutorial translates that math into the five-step training loop used everywhere: **prediction → loss calculation → backward pass → parameter update → gradient reset**. That loop scales from toy regression models to LLM training.
- PyTorch's `requires_grad`, computation graphs, and `loss.backward()` are valuable because they automate differentiation without changing the underlying math. The abstraction is ergonomic, not conceptual.
- The collection also keeps returning to the `nn.Linear` layer as the workhorse primitive. Much of modern deep learning, including the inside of a Transformer block, is still repeated affine transformation plus nonlinearity.
- The `adam` tutorial gives the optimizer layer of the story: Adam combines
  - **momentum / first-moment tracking** for directional stability,
  - **second-moment tracking** for adaptive per-parameter step sizes, and
  - **bias correction** to avoid tiny early updates.
- That makes Adam a practical answer to two weaknesses of vanilla gradient descent: memoryless updates and one-size-fits-all learning rates.
- Taken together, these tutorials imply a strong vault-level pattern: before treating Transformers and RLHF as special, first recognize that they are compositions of the same core objects—tensors, matrix multiplies, gradients, losses, and optimizers.
- [[Han Fang - PyTorch Practice]] complements that conceptual story with runnable interview-style implementations of stable softmax, custom BatchNorm, a hand-built SGD-with-momentum optimizer, and masked attention, making the page's abstractions feel like ordinary PyTorch building blocks rather than separate theory.
- [[Fareed Khan - Train LLM From Scratch]] reinforces the same point at the LLM scale: a language model still reduces to familiar PyTorch pieces such as embeddings, MLPs, attention modules, batch iterators, AdamW updates, and cross-entropy loss. The repo is a useful reminder that "LLM training" is mostly these standard components composed at larger scale.
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]] adds a complementary generative-model example. A diffusion model still fits the same neural-network training loop — prediction, loss, backward pass, optimizer step — but the target is known Gaussian noise added by the training code, not the next token. This makes [[Diffusion Models]] a clean contrast case for how changing the supervised target changes the whole generative behavior.
- For the complementary DSA side of interview preparation, [[Algorithm Templates for Interviews]] covers the reusable array, graph, DP, and data-structure patterns that often appear alongside ML-specific coding rounds.
- [[Alisa Liu - Book of LLMs]] consolidates these fundamentals from an interview-cram angle: it restates the MLP as `h = f(Wx + b)`, stresses that non-linearities are what make depth matter (without them `W₁W₂x = Wx` collapses to one linear map), and adds the numerical-stability tricks (stable softmax / log-sum-exp) and information-theory basis (entropy, cross-entropy, KL) that sit under every loss function. [[Alisa Liu - Math Notes]] supplies the probability/statistics substrate — **maximum likelihood estimation** and the **bias–variance decomposition** — that this page's optimization story ultimately rests on. Both feed [[ML Research Interview Preparation]].
- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]] adds the *memory* footprint of this same loop at scale. Mixed-precision **Adam** costs ~16 bytes per parameter — 2 (fp16 weight) + 2 (fp16 gradient) + 12 (fp32 master weight plus the first- and second-moment estimates) — so the optimizer state, not the weights, dominates memory and is the quantity [[Distributed Training Parallelism]] is engineered to shard.

## Dimensional collapse is silent, and the fix can be derived rather than tuned

[[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]] is a clean worked example of converting a training heuristic into a derived
objective, and the failure mode it addresses generalises well beyond self-supervised vision.

**The failure is silent.** Complete collapse — a constant encoder — is loud and obvious. **Dimensional
collapse**, where the encoder uses a low-rank subspace, is a spectrum, and **"nothing in your training run
will tell you it is happening."**

**Moment matching cannot fix it, provably.** Because `Cov(P) = Cov(Q) ⟹ g(P) = g(Q)`, any criterion
constraining finitely many moments cannot fully specify a distribution. VICReg's failure here is by
construction, not by tuning.

**The derivation runs in two halves.** *Which target distribution?* A linear probe's worst-case
ridge-regression bias is governed by the **smallest** eigenvalue under a fixed trace, so minimising it
gives **isotropy** — but a linear probe only sees `ZᵀZ` and cannot ask for more, "which is exactly the
result VICReg already had." A **radius-based k-NN probe** is biased in proportion to `∇log p`; integrating
gives **Fisher information**, and `J(p) ≥ tr(Σ⁻¹)` holds **with equality iff p = N(0, Σ)**. Together they
give **Q = N(0, σ²I_K)**, which maximum entropy under a covariance constraint also yields.

*Which divergence?* Treat distribution matching as a **hypothesis test and use the test statistic as the
loss** — uniquely, this gives a **scale**, comparable against a critical value. Direct multivariate
testing is hopeless (256 samples in 1024 dimensions), so **Cramér–Wold (1936)** reduces it to
one-dimensional projections: **SIGReg** samples M random unit directions, runs a cheap univariate
**Epps–Pulley** characteristic-function test on each, and averages.

**Boundedness is visible in the code rather than only in a theorem.** The empirical characteristic
function has magnitude at most one, so **"no single input can dominate this statistic"** — whereas a
kurtosis penalty would let an embedding at 10⁶ contribute 10²⁴. That argument transfers to any loss built
on characteristic functions.

**Training loss predicts downstream accuracy without labels**: Spearman **~85%** against linear-probe
accuracy, rising to **~99%** under the rescaling `C(α) = ρ_s(train_loss/λ^α, test_accuracy)` at
**α ≈ 0.4**. Rai's phrasing is careful — the loss **"does not predict performance, it measures it."**

Two honest caveats: SIGReg **averages over directions rather than maximising**, which is the statistically
correct test, and what the averaged statistic misses is not characterised; and **"one hyperparameter"**
excludes learning rate, weight decay, batch size, augmentation and architecture — what is removed is the
anti-collapse knob, not tuning.

## Open questions

- Which additional fundamentals deserve their own pages next: initialization, normalization, regularization, or batching/data pipelines?
- How much of modern model behavior is still well explained by these fundamentals versus by scale-specific phenomena?

## Related pages

- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Han Fang - PyTorch Practice]]
- [[Fareed Khan - Train LLM From Scratch]]
- [[Transformer Architecture]]
- [[Diffusion Models]]
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]]
- [[LLM Training Pipeline]]
- [[Distributed Training Parallelism]]
- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]]
- [[Model Quantization and Efficiency]]
- [[Algorithm Templates for Interviews]]
- [[ML Research Interview Preparation]]
- [[Alisa Liu - Book of LLMs]]
- [[Alisa Liu - Math Notes]]
- [[AI Knowledge Base Overview]]
- [[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]]
- [[Joint-Embedding Predictive Architecture]]
- [[Siddhant Rai]]
