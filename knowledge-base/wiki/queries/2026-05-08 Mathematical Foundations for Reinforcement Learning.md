---
type: query
created: 2026-05-08
updated: 2026-05-08
question: What mathematical concepts are fundamental for deeply understanding reinforcement learning if Kevin Murphy's survey is the starting point?
tags:
  - query
  - reinforcement-learning
  - mathematics
  - learning-roadmap
source_ids:
  - src-2026-05-08-murphy-reinforcement-learning-overview
status: active
---

# 2026-05-08 Mathematical Foundations for Reinforcement Learning

## Question

What are the fundamental mathematical concepts to know in order to fully understand and eventually become expert in reinforcement learning, assuming [[Kevin Murphy - Reinforcement Learning - An Overview]] is the place to start?

## Answer

To get from "I can follow Murphy's survey" to "I can read RL papers and design RL systems confidently," you need to master **three layers** of math:

### 1. Core math you cannot skip

These are the true foundations. Without them, most RL equations are just symbols.

| Area | What to know | Why it matters in RL |
| --- | --- | --- |
| **Probability** | random variables, conditional probability, expectation, variance, covariance, Bayes rule, law of total expectation | rewards, returns, uncertainty, transitions, exploration, stochastic policies |
| **Linear algebra** | vectors, matrices, dot products, norms, eigenvalues/eigenvectors, matrix calculus basics | function approximation, neural networks, value-function parameterization, state embeddings |
| **Multivariable calculus** | partial derivatives, gradients, Jacobians, Hessians, chain rule, Taylor expansion | policy gradients, backpropagation, sensitivity of objectives and updates |
| **Optimization** | gradient descent, stochastic gradient descent, constrained optimization, Lagrange multipliers, convex vs non-convex optimization | training policies and value functions, actor-critic methods, RLHF-style optimization |
| **Statistics / estimation** | bias-variance tradeoff, sampling error, estimators, regression, maximum likelihood | Monte Carlo estimates, bootstrapping, off-policy evaluation, noisy returns |

### 2. RL-specific mathematics you must internalize

This is what turns generic ML math into RL math.

| Area | What to know | Why it matters in RL |
| --- | --- | --- |
| **Markov processes** | Markov chains, transition matrices, stationary distributions, ergodicity intuition | MDPs are built on the Markov property |
| **Markov Decision Processes (MDPs)** | states, actions, rewards, transition kernels, policies, value functions | the formal language of almost all classical RL |
| **Dynamic programming** | recursion, Bellman equations, value iteration, policy iteration | the backbone of value-based RL and planning |
| **Fixed-point thinking** | contraction mappings, iterative convergence intuition | Bellman operators are solved as fixed-point problems |
| **Monte Carlo methods** | sampling, return estimation, variance reduction | first-principles RL estimation and policy evaluation |
| **Bootstrapping / temporal-difference learning** | partial target updates, target leakage intuition, stability issues | TD learning is central to practical RL |
| **Function approximation** | approximation error, generalization, regression under shifting targets | modern RL uses neural function approximators almost everywhere |

### 3. Mathematics that separates a practitioner from an expert

These are what you need to deeply understand advanced RL papers, theory, and edge cases.

| Area | What to know | Why it matters in RL |
| --- | --- | --- |
| **Information theory** | entropy, cross-entropy, KL divergence, mutual information | entropy regularization, trust-region methods, policy constraints, RLHF objectives |
| **Stochastic processes** | martingales intuition, stopping times, convergence of random processes | theoretical RL analysis and sequential uncertainty |
| **Numerical analysis** | stability, step-size effects, conditioning, approximation error propagation | RL is often fragile because learning targets move and errors compound |
| **Control theory** | optimal control, state estimation intuition, model predictive control, continuous-time systems | model-based RL and continuous control |
| **Game theory** | Nash equilibrium, zero-sum games, extensive-form games, regret | multi-agent RL and self-play |
| **Online learning / bandits** | exploration-exploitation, regret, upper confidence bounds, importance sampling intuition | exploration theory and data-efficient decision making |
| **Advanced probability / concentration** | law of large numbers, central limit theorem, concentration bounds | sample complexity and theoretical guarantees |

## Practical ordering

If Murphy's survey is your anchor, study in this order:

1. **Probability + linear algebra + multivariable calculus**
2. **Optimization + statistics**
3. **Markov chains + MDPs + Bellman equations**
4. **Dynamic programming + Monte Carlo + TD learning**
5. **Function approximation + deep learning math**
6. **Information theory + control theory + game theory**
7. **Advanced RL theory**: concentration bounds, stochastic approximation, regret, measure-theoretic probability if you want research-level depth

## Minimal expert checklist

If you can do the following comfortably, your math foundation is strong enough for serious RL work:

- Derive Bellman expectation and optimality equations
- Explain why value iteration converges
- Derive a policy gradient objective and apply the log-derivative trick
- Reason about bias vs variance in Monte Carlo, TD, and actor-critic estimates
- Understand why off-policy learning can become unstable
- Read entropy/KL-regularized objectives without getting lost
- Follow the math in modern RL-for-LLMs methods at least at the objective/optimization level

## Evidence

- [[Kevin Murphy - Reinforcement Learning - An Overview]] frames RL broadly across value-based, policy-based, model-based, multi-agent, offline, hierarchical, and LLM-related methods.
- That scope implies the prerequisite stack cannot stop at basic deep learning math; it must include the mathematics of sequential stochastic decision making, dynamic programming, optimization, and uncertainty.
- This note is therefore a synthesis of the survey's breadth plus the standard mathematical foundations that those RL branches rely on.

## Follow-ups

- Split this note into dedicated pages for `Probability for RL`, `MDPs and Bellman Equations`, `Optimization for RL`, and `Information Theory for RL`.
- Build a source-backed study sequence with one paper, one chapter, and one implementation resource per math topic.

## Related pages

- [[Reinforcement Learning]]
- [[Kevin Murphy - Reinforcement Learning - An Overview]]
- [[AI Knowledge Base Overview]]
