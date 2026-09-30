---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-27-romero-policy-gradient-llms
source_title: "Policy Gradient for LLMs, Explained Visually"
source_author: Tyler Romero
source_url: https://www.tylerromero.com/posts/2026-09-policy-gradient/
tags: [source/summary, reinforcement-learning, post-training, mathematics, education]
source_ids: [src-2026-09-27-romero-policy-gradient-llms]
status: active
---

# Tyler Romero - Policy Gradient for LLMs, Explained Visually

## Summary

Tyler Romero derives REINFORCE for language models from first principles and shows where each later
refinement enters. Starting from the sequence probability and the log-derivative trick, he obtains the
policy-gradient identity, decomposes it into per-token log-probability gradients, then proves the
zero-mean score identity that licenses baseline subtraction. GRPO's group-centered advantage then
appears not as a trick but as the cheapest legal baseline. The piece is a pedagogical derivation, not
new empirical work.

## Key claims

- A completion is `p_theta(y|x) = prod_t p_theta(y_t | x, y_<t)`, and the objective is the expected
  reward `J(theta) = E[R(x,y)]` over prompts and sampled completions.
- Direct enumeration is hopeless: with a vocabulary of about **150,000 tokens**, a **100-token
  completion has more than 10^500 possibilities**.
- The log-derivative trick gives `grad J = E[R(y) grad log p_theta(y)]`, whose Monte Carlo estimator
  is REINFORCE: `(1/N) sum_i R(y_i) grad log p_theta(y_i)` with `y_i ~ p_theta`.
- The sequence score decomposes into a sum of per-token terms, and the softmax logit gradient is
  `1 - p_v` for the sampled token and `-p_u` otherwise - so reinforcing a completion pushes up the
  sampled token and pushes down every alternative in proportion to its probability.
- With verifier rewards of `R=1` for correct and `R=0` for incorrect, policy gradient is "literally
  SFT on the correct completions": incorrect completions contribute nothing and are never directly
  pushed down.
- The score has zero mean on-policy, `E_p[s_yt] = 0`. Therefore for any baseline `b` that does not
  depend on the sampled token, `E_p[(R-b) s_yt] = E_p[R s_yt]`: subtracting a baseline changes the
  variance but not the expected gradient.
- GRPO's baseline is the group mean, `A_i = R_i - (1/G) sum_j R_j`. With four rollouts at a group mean
  reward of **0.5**, advantages are **+0.5** and **-0.5**; groups where every completion succeeds or
  every one fails contribute no gradient at all.
- Named methods: **REINFORCE**, **PPO**, **GRPO**, **DAPO**.

## Why it matters

The vault carries a lot of applied RL evidence - reward hacking, group-relative baselines, credit
assignment over long horizons - largely as practice. This source supplies the identity those practices
rest on, and in doing so explains two structural consequences precisely: why a binary verifier reward
yields a gradient supported only on the correct completions, and why homogeneous rollout groups
contribute no gradient.

## Tensions and caveats

The numerical examples are explicitly illustrative, not measurements. Baseline unbiasedness holds
only under on-policy sampling, and Romero warns that inference engines such as vLLM or SGLang may use
different numerical precision or stale weights, so the practical estimator is often off-policy and the
identity is approximate. The "literally SFT" equivalence is a statement about the gradient at binary
reward, not a claim that RL and SFT share training dynamics. The derivation covers terminal sequence
rewards and does not address token-level credit assignment, KL regularization, clipping, importance
ratios, or PPO's value estimation.

## Raw capture

- [[2026-09-27 Tyler Romero - Policy Gradient for LLMs, Explained Visually]]

## Affected pages

- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Reward Design for RL]]
- [[Long-Horizon Credit Assignment]]

## Related pages

- [[LLM Training Pipeline]]
- [[Agentic Reinforcement Learning]]
- [[Neural Network Fundamentals]]
- [[LLM Reasoning]]
