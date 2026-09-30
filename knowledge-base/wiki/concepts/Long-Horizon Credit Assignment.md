---
type: concept
created: 2026-09-11
updated: 2026-09-30
tags:
  - concept
  - reinforcement-learning
  - reasoning
source_ids:
  - src-2026-09-10-fu-progressive-point-matching
  - src-2026-09-12-zhang-recurrent-looped-transformer
  - src-2026-09-27-romero-policy-gradient-llms
status: active
---

# Long-Horizon Credit Assignment

## Definition

The problem of attributing reward to individual steps of a long reasoning or agentic trajectory when the
only reliable signal arrives at the end. The failure is quantitative, not qualitative: sparse outcome
rewards **produce policy gradients whose signal-to-noise ratio degrades exponentially in the task
horizon**. Beyond some horizon, outcome-only RL does not train slowly — it stops training.

Every partial-credit method is an attempt to manufacture signal before the end of the trajectory, and the
question that separates them is whether the manufactured signal is **biased**: whether the policy that
maximises the dense reward is still the policy that maximises the true outcome reward.

## Why it matters

The threshold behaviour is the reason this deserves its own treatment rather than a section under reward
design. On a near-impossible math dataset reported in
[[Preston Fu - Progressive Point Matching]], **GRPO could not fill even a single training batch after 24
hours** — no successful rollouts, therefore no gradient, therefore no learning at any budget. That is a
different regime from "converges slowly," and it is the regime that agentic tasks with dozens of tool
calls increasingly occupy.

The standard fixes all buy signal by introducing asymptotic bias. Learned value functions, process
rewards, and self-distillation converge to a policy that is not optimal for the outcome. The concrete
failure of process rewards is instructive: they **"can incentivize saying logically correct statements
that are unrelated to eventual task success"** — a reward for looking like good reasoning rather than for
reaching the goal, which is reward hacking with a respectable face.

## Current synthesis

**Progressive Point Matching is the clearest worked example of an unbiased dense reward.** Its
construction has three moves, and the third is the load-bearing one.

*Monotone state space.* Reasoning is modelled as a path through a Markovian state space whose states are
**sets** of **reasoning points** — intermediate results extracted from a reference trajectory. Because a
state is the set of points visited so far, it never shrinks: **progress can never be undone**. This makes
"progress" well-defined as a reward signal at every step.

*The naive version is biased, and the cause is specific.* A trajectory that succeeds using a *different*
strategy visits few of the reference points and therefore scores low. The naive progress reward penalises
correct answers for being unlike the reference — exactly the bias it was meant to avoid.

*Shortcutting removes it.* A point counts as reached if all the points that depend on it have been
reached. Under this rule, **any successful trajectory receives full credit**, and the policy optimal
under the shaped reward is also optimal under the original outcome reward. This is a different kind of
defence from the usual one: most dense-reward schemes are justified empirically, and this one is
justified by showing the optimum is unchanged.

**The measured benefit tracks the theory.** On synthetic tasks built from independent subtasks, the
speedup over [[Group Relative Policy Optimization]] **improves exponentially with the number of
subtasks** — the mirror image of the exponential signal-to-noise decay that motivates the method. On the
near-impossible math dataset it trains where GRPO cannot start, and beats the next-best method (POPE).

**A separate and highly transferable finding concerns training context length.** Training at **4K was
comparable to or better than training at 8K**, which inverts the usual assumption. The explanation given
is behavioural: the 8K policy collapses its output length and guesses early, while the 4K policy is
forced to optimise partial progress within its budget. A longer training budget can therefore teach a
policy to *waste* it, which connects directly to the length-collapse dynamics recorded under
[[Test-Time Scaling]] and [[Reasoning Compression]].

**The practical bottleneck has moved to point extraction.** Reasoning points are generated with an
off-the-shelf LLM, and this "required a significant amount of iteration." The method converts a
reward-design problem into a decomposition problem, and the decomposition is not yet automatic.

## State replay becomes part of policy correctness

[[Yifan Zhang - Recurrent Looped Transformer]] extends the credit-assignment problem into recurrent
serving state. Exact current-policy RL replay must rebuild hidden state, decoder KV, and encoder
memory after parameters change; reusing stale state means the replay no longer comes from the current
policy. Behavior log probabilities must also match the sampler that actually produced the trajectory.

The source specifies the contract but provides no evidence that full replay and backpropagation remain
tractable at the long sequence lengths the architecture targets.

## The clean identity covers terminal rewards only, and everything on this page lives past that line

[[Tyler Romero - Policy Gradient for LLMs, Explained Visually]] is useful here less for what it derives
than for where it stops. The derivation runs from the sequence probability through the log-derivative
trick to `grad J = E[R(y) grad log p_theta(y)]`, and on to the zero-mean score identity `E_p[s_yt] = 0`
that licenses subtracting a baseline — and it treats terminal sequence rewards throughout. It does not
address token-level credit assignment, KL regularization, clipping, importance ratios, or PPO's value
estimation. That boundary is the contribution to this page: it marks exactly where a result with a proof
ends and where the heuristics catalogued above begin.

The per-token decomposition shows why the boundary falls there. The sequence score is a sum of per-token
terms, and a terminal scalar reward multiplies that entire sum uniformly, so within a rewarded completion
the identity assigns identical credit to every token; the softmax gradient (`1 - p_v` for the sampled
token, `-p_u` otherwise) separates tokens by their current probability, not by their contribution to the
outcome. Long-horizon credit assignment is therefore not a gap the policy-gradient estimator failed to
close — it is a question the estimator never poses. Every method on this page that discriminates across a
trajectory is adding structure the identity does not supply, which is why each of them has to argue about
bias separately and from scratch.

This reframes the unbiasedness argument recorded above for Progressive Point Matching without weakening
it. PPM's guarantee — that shortcutting makes the policy optimal under the shaped reward also optimal
under the outcome reward — is a statement about which terminal-style reward to feed the same identity,
not an extension of the identity to per-step credit. It is strong precisely because it stays inside the
regime where the estimator is understood. Process rewards and learned value functions instead attach
signal to intermediate steps, where no comparable zero-mean result exists to say what the expected
gradient is, which is a more specific account of their bias than "they converge to a policy that is not
optimal for the outcome."

One caveat compounds with the state-replay problem recorded above. The baseline identity holds only under
on-policy sampling, and Romero warns that inference engines such as vLLM or SGLang may use different
numerical precision or stale weights, so the practical estimator is already approximate before recurrent
hidden state enters the picture. The requirement that behaviour log-probabilities match the sampler that
produced the trajectory is the same requirement arriving from a different direction. The source is a
pedagogical derivation and its worked numbers are explicitly illustrative rather than measured.

## Open questions

- The method needs a reference trajectory to extract points from. On genuinely novel tasks — the regime
  where long horizons matter most — where that reference comes from is unaddressed.
- If point extraction requires per-dataset manual tuning, the cost profile differs from GRPO's in a way
  the headline speedups do not capture.
- The exponential speedup is demonstrated on synthetic tasks with **independent** subtasks, the best case
  for a set-valued progress measure. Real reasoning chains are dependent — which is precisely what
  shortcutting handles — but the exponential claim is not shown to survive the dependent case.
- The 4K-beats-8K explanation is a plausible behavioural story, not a measured mechanism; no ablation
  isolating output-length collapse is reported.
- Whether an unbiased dense reward can be constructed for tasks with **no** verifiable outcome at all —
  where even the terminal signal is a judge — is untouched. Verifier's law (see
  [[Synthetic Data Flywheel]]) suggests that is where the frontier actually binds.
- Is there an analogue of the zero-mean score identity for token-level or step-level advantages, or is
  per-step credit assignment necessarily heuristic? Every method on this page assumes the latter without
  arguing for it.
- PPM's unbiasedness is established for a shaped terminal reward under on-policy sampling. Whether it
  survives the off-policy estimator that production stacks actually run — different serving precision,
  stale weights, truncated importance ratios — has not been tested by any source here.

## Related pages

- [[Reward Design for RL]]
- [[Group Relative Policy Optimization]]
- [[Reinforcement Learning]]
- [[Agentic Reinforcement Learning]]
- [[RL Environment Design]]
- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Staged Reinforcement Learning Curriculum]]
- [[Monte Carlo Tree Search]]
- [[Preston Fu - Progressive Point Matching]]
- [[Tyler Romero - Policy Gradient for LLMs, Explained Visually]]
- [[Inference Serving Engines]]
