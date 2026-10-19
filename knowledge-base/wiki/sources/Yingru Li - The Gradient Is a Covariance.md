---
type: source-summary
created: 2026-10-19
updated: 2026-10-19
source_id: src-2026-10-15-li-gradient-is-covariance
source_title: "The Gradient Is a Covariance"
source_author: Yingru Li
source_url: https://richardli.xyz/post/gradient-is-covariance/
tags: [source/summary, reinforcement-learning, policy-gradient, post-training, fisher-information, distillation]
source_ids: [src-2026-10-15-li-gradient-is-covariance]
status: active
---

# Yingru Li - The Gradient Is a Covariance

## Summary

Part 1 of Yingru Li's three-part series "Why Post-Training Is Sparse." It is a derivation, not an
experiment. On the model's own samples, the score (the gradient of a response's log-probability)
has zero mean. As a result, the expected policy gradient for each parameter equals the
**covariance** between the learning signal and that parameter's score. The diagonal
**Fisher** is the score's **variance**. Together these bound the expected gradient for any
reward.

The post then decomposes the Fisher. At one position it measures how differently a parameter
moves the logits of likely candidate tokens. Along a response, it sums over positions. All of
the results carry over to **off-policy** samples once the score is centered under a known
sampler.

The sparsity measurements that motivate the series are cited from other papers. The post's own
contribution is an account of which coordinates **can** move, and why that set can be estimated
before any reward is seen.

## Key claims

- **Small is not sparse.** Cited work finds RL fine-tuning changes only **5–30%** of a model's
  parameters across **seven algorithms and ten models** (Mukherjee et al., 2025). On-policy
  distillation and SFT on near-policy data reportedly behave the same way (Zhang, Mukherjee &
  Peng, 2026). Two common explanations are that RL only reweights answers the model can already
  produce, and that a scalar advantage with `B` values carries at most `log2 B` bits per
  episode. Li argues these explain why the update is small or carries little information, not
  which coordinates move: "a hundred million parameters each moving a little would satisfy
  both."
- **The identities.** On-policy, the score has zero mean, `E[score_i] = 0`. Hence the
  expected update `G_i = E[A · score_i] = Cov(A, score_i)` and the diagonal Fisher
  `F_i = E[score_i^2] = Var(score_i)`. By Cauchy–Schwarz, `|G_i| <= std(A) · sqrt(F_i)`.
  Both statements hold per prompt, so `G_i = E_x[Cov(r, score_i | x)]`.
- **Baselines are noise control.** A baseline `b(x)` that depends only on the prompt leaves `G_i`
  unchanged, because `Cov(A - b, score_i) = Cov(A, score_i)`. It changes only `std(A)` and the
  noise of the estimate. The author's own **Optimal Token Baseline** (ICML 2026) is presented as
  the per-token choice that minimizes that noise; this is a self-citation not evaluated here.
- **Necessary, not sufficient.** "The Fisher says where learning can happen; the reward decides
  where it does." After "She drank a cup of," the output rows for *tea* and *coffee* have a
  large Fisher, yet if the reward is indifferent between them their gradient is zero. A cited
  measurement taken before RL training finds the top **1%** of coordinates by Fisher hold
  **47.40%** of the top 1% by gradient magnitude, against **1%** at random.
- **One position.** The token Fisher of parameter `i` is the variance, under the model's
  next-token distribution, of how strongly that parameter moves each candidate's logit. The
  softmax removes the common component, which shifts every logit together and changes no
  probability, so only differences between likely candidates count. A parameter therefore has a
  small token Fisher when the model is confident, or when its likely candidates react alike.
- **Along a response.** Cross terms between positions average to zero, so the response Fisher
  is the expected sum of token Fishers. Length sets the overall scale for every parameter
  alike; the token Fishers decide which coordinates are large.
- **Off-policy needs centering.** When tokens come from an inference engine or a stale model,
  subtracting the sampler's average sensitivity at every prefix restores the zero mean, and the
  derivation goes through with the sampler `μ` in place of the model. This requires `μ`'s **full
  next-token distribution at every prefix**. Stale models and inference engines that return full
  log-probabilities provide it. Human demonstrations do not, "which is why SFT cannot be
  centered." Off-policy, `G_i` is the expected update of the centered estimator, which is the
  gradient of a covariance loss rather than of on-policy expected reward. The public reference
  for score centering is Marek & Ryabinin (2026).
- **Stated assumptions.** The response space is finite (finite vocabulary, bounded length).
  Probabilities are positive, "which softmax sampling at temperature 1 without top-k or top-p
  guarantees." The reward and prompt distribution do not depend on the parameters. The full
  Fisher equals the expected negative Hessian of log-probability and must be estimated on
  responses the model samples. Applying the same formula to data labels gives the **empirical
  Fisher**, a different quantity.
- **Previewed, not captured.** Part 2 is said to show an output-layer Fisher that is "an exact
  coin flip," a low-dimensional Fisher in hidden layers, and a mean shift that can push gradient
  where the Fisher cannot see when the score is not centered. These are previews, not evidence
  on this page.

## Why it matters

The vault's policy-gradient material, mainly [[Tyler Romero - Policy Gradient for LLMs, Explained Visually]],
already had the zero-mean score and the baseline identity. Li turns them into a **per-parameter**
account with three consequences:

- A coordinate whose score barely varies on the model's own samples cannot receive much expected
  gradient, whatever the reward.
- A prompt whose reward is constant over the model's samples contributes no expected gradient.
- A prompt-level baseline shapes variance, not direction.

The off-policy section turns the inference-engine mismatch recorded on [[Reinforcement Learning]]
from a warning into a stated condition: knowing the sampler's full distribution.

It also separates two questions often merged in post-training debates. How *much* RL changes a
model is a different question from *which* parameters it changes. That distinction bears on the
creation-versus-elicitation debate on [[LLM Reasoning]] and on low-rank adaptation in
[[Parameter-Efficient Fine-Tuning]].

## Tensions / open questions

- **The empirical motivation is secondhand.** The 5–30% range, the near-policy SFT and
  distillation claim, and the **47.40%** overlap come from cited papers not ingested here. One
  of them is a 2026 arXiv preprint, and the capture lists no models or settings for the overlap
  statistic.
- **A bound on the gradient is not a bound on the update.** The bound covers the expected
  gradient. Optimizers such as Adam rescale each coordinate's step by its own gradient history,
  so mapping the Fisher bound onto which parameters actually change requires the optimizer.
  Part 1 does not address that step; this gap is the vault's observation.
- **Production sampling falls outside the on-policy proof.** Top-k and top-p truncation violates
  its positive-probability assumption. On Li's construction, such samplers are covered only by
  treating the truncated distribution as the sampler and centering. That changes the objective to
  the covariance loss and requires recording the sampler's full distribution.
- **Expected versus per-sample contrast.** The expectation-level identity qualifies the
  per-sample reading on [[Reward Design for RL]], where under a 0/1 reward failures contribute no
  terms. In expectation, the update is the covariance with or without a prompt-level baseline.
  See that page for the reconciliation.
- **Not about adapters.** Sparse in coordinates is a different property from low rank. The post
  does not test LoRA or masked fine-tuning.

## Affected pages

- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Reward Design for RL]]
- [[LLM Reasoning]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Multi-Teacher On-Policy Distillation]]
- [[Knowledge Distillation]]
- [[Neural Network Fundamentals]]

## Raw capture

- [[The Gradient Is a Covariance]]

## Citations

- Canonical URL: <https://richardli.xyz/post/gradient-is-covariance/>
- Published 2026-10-15; captured 2026-10-19, per the clipping's metadata. The clipping's
  interactive SVG figures are not reproduced here; its formulas and prose are.
- Series pages linked but not captured: Part 2,
  <https://richardli.xyz/post/sparsity-score-centering/>, and Part 3,
  <https://richardli.xyz/post/what-policy-gradient-can-reach/>.
- Works cited by the post and not ingested in this vault:
  - Mukherjee et al., *Reinforcement Learning Finetunes Small Subnetworks in Large Language Models*, NeurIPS 2025 (arXiv 2505.11711).
  - Zhang, Mukherjee & Peng, *Understanding LLM Parameter Update Sparsity through the Lens of Fisher*, arXiv 2609.36262 (2026).
  - Marek & Ryabinin, *Score Centering Stabilizes Off-policy Reinforcement Learning*, arXiv 2609.20807 (2026).
  - Li, Xu et al., *The Optimal Token Baseline*, ICML 2026 (arXiv 2602.07078).
  - Li, *Information Bandwidth in Reinforcement Learning*, blog, 2025.

## Related pages

- [[Tyler Romero - Policy Gradient for LLMs, Explained Visually]]
- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Reward Design for RL]]
- [[LLM Reasoning]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Multi-Teacher On-Policy Distillation]]
- [[Knowledge Distillation]]
- [[Neural Network Fundamentals]]
- [[Inference Serving Engines]]
- [[LLM Training Pipeline]]
