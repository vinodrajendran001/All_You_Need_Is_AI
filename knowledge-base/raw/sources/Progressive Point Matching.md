---
title: "Progressive Point Matching"
source: "https://www.prestonfu.com/notes/ppm/?utm_source=tldrai"
author:
published:
created: 2026-09-10
description: "Assigning partial credit to improve reinforcement learning for long-horizon reasoning tasks."
tags:
  - "clippings"
---
Today’s LLMs tackle extremely long-horizon tasks that may run continuously for hours or days. Tasks that take humans days or weeks may require language model trajectories containing millions, or eventually billions, of tokens.

These capabilities have been enabled by large-scale reinforcement learning (RL). The standard approach is to sample full trajectories and to assign a sparse outcome reward to the full trajectory – a 0 or 1 based on whether the trajectory was successful. Empirically, this simple approach has demonstrated stable performance improvements at scale, since the optimal policy has an *unbiased* objective: it is trained to maximize the likelihood of task success.

But as we continue to scale to longer-running tasks, sparse outcome rewards become increasingly inefficient. For example, a trajectory that makes progress on dozens of subtasks but fails at the final one receives the same reward as a trajectory that makes no progress at all. Theoretically, we show that sparse outcome rewards produce policy gradients that degrade *exponentially* in signal-to-noise with the task horizon.

A variety of methods such as learned value functions, process rewards, or self-distillation have introduced asymptotic *bias*. Here, by bias we mean that optimal policies under the surrogate objective may not be optimal under outcome rewards. For example, process rewards (which reward [logical correctness](https://arxiv.org/abs/2501.07301) at each segment of a trajectory) can incentivize saying logically correct statements that are unrelated to eventual task success.

We propose **progressive point matching (PPM)**, a simple and asymptotically unbiased framework for assigning partial credit.

![Partial credit methods for long-horizon reasoning](https://www.prestonfu.com/notes/ppm/teaser.png)

Figure 1. Sparse outcome rewards converge exponentially more slowly than methods that assign partial credit. Biased partial credit methods such as process rewards may converge to suboptimal policies.

### Framework

Our key insight is that solving reasoning problems can be regarded as discovering paths through a *Markovian state space*.

Reasoning trajectories are long, and previous reasoning can be compressed into intermediate results. For example, consider the task of theorem proving, which may additionally involve proving intermediate lemmas. Once a trajectory has stated a lemma and proved it, subsequent reasoning can simply condition on the lemma without referring to its proof. We call such intermediate results **reasoning points**. In practice, we obtain reasoning points from a reference trajectory, like a human-written proof.⁠ <sup aria-label="Footnote 1: By nature of compression, it’s cheap to extract reasoning points from a reference trajectory, but the other direction is nontrivial and may involve proving some lemmas. This also means that we do not require full language model reasoning traces.">[1] <span role="tooltip">By nature of compression, it’s cheap to extract reasoning points from a reference trajectory, but the other direction is nontrivial and may involve proving some lemmas. This also means that we do not require full language model reasoning traces.</span></sup>

Reasoning trajectories therefore admit compact state representations: the *set of reasoning points* visited by the current trajectory prefix. We can view reasoning trajectories as paths through the state space of a goal-reaching **reasoning MDP**, where the goal state must contain the goal point (e.g., the final answer). Each action represents adding new reasoning point(s) to this set. One corollary of this setup is that the set can never shrink over time. That is, by construction *progress can never be undone*, where progress is the size of this set. For example, if the trajectory then takes an incorrect turn, its reasoning state remains unchanged, and it can still backtrack to the lemma.

However, there’s a problem. Consider a successful trajectory, which reaches the goal following a totally different strategy from the reference trajectory. According to our definition, it attains very low progress. On the other hand, a failed trajectory, which does not reach the goal but closely follows the reference trajectory may achieve high progress. As a result, naively optimizing for progress is *biased*.

We can solve this by introducing a **shortcutting** mechanism: a point is considered reached if all points that depend on this point have already been reached. In particular, any successful trajectory gets full credit.⁠ <sup aria-label="Footnote 2: As we suggest in Figure 1, shortcutting also enables learning strategies that differ from the reference trajectory! This is critical toward improving pass@$k$.">[2] <span role="tooltip">As we suggest in Figure 1, shortcutting also enables learning strategies that differ from the reference trajectory! This is critical toward improving pass@ <math xmlns="http://www.w3.org/1998/Math/MathML" display="inline" data-latex="k"><semantics><mrow><mi>k</mi></mrow> <annotation>k</annotation></semantics></math>.</span></sup> In [our paper](https://arxiv.org/abs/2609.07303), we show that shortcutting results in learned policies that are optimal under outcome rewards!

![Progressive point matching shortcutting mechanism](https://www.prestonfu.com/notes/ppm/method.png)

Figure 2. In RL with sparse outcome rewards, trajectories that fail to reach the goal g get no partial credit. In progressive point matching, the shortcutting mechanism provides partial progress rewards that (in a special case) correspond to the farthest point along the reference trajectory.

### PPM scales to long-horizon reasoning tasks

To isolate the effect of task horizon, we consider synthetic tasks, which allows us to control (i) the number of subtasks, (ii) the “shape” of the reasoning MDP.

Intuitively, credit assignment methods like PPM perform the best when each subproblem is independent, or equivalently there are no dependencies between reasoning points. This allows us to get independent policy gradients on each subtask. In this setting, it turns out that as we increase the number of subproblems $n$, the empirical training speedup over standard GRPO improves *exponentially* with $n$!

![PPM performance as the task horizon grows](https://www.prestonfu.com/notes/ppm/multicountdown.png)

Figure 3. In a synthetic task where each subtask is independent, PPM improves training efficiency exponentially over sparse outcome rewards as the task horizon grows.

The paper includes many additional experiments to explore axis (ii). For example, we consider the much more difficult MDP where each subproblem can only be solved given a correct answer to the previous subproblem. In this case, reaching points is highly correlated, which we show theoretically degrades the signal-to-noise of the policy gradient. We also consider synthetic reasoning tasks that lie between these two extremes. If you’re interested, check out [our paper](https://arxiv.org/abs/2609.07303)!

### PPM enables training on near-impossible math reasoning tasks

As we continue to scale our algorithms to longer-horizon tasks, it is not feasible to directly train on trajectories that are millions of tokens long. Instead, [practical RL systems](https://openai.com/index/learning-to-reason-with-llms/) train on “simulated” versions of these tasks at small token budgets, with the objective of improving performance at a much larger test-time token budget.

Recent work, such as Claude Code’s `/effort ultracode` mode, has aimed to resolve this by designing harnesses and multi-agent workflows to improve performance at extremely large test-time budgets. But such approaches are insufficient, and have led to [inconsistent performance gains](https://cognition.com/blog/frontier-code-1.1) with larger budgets in frontier models. Thus, today’s RL algorithms remain bottlenecked by their ability to scale with test-time budget.

In this setting, the task may rarely be solved within the training token budget. One proxy for this setting is a dataset of extremely hard math problems, where the base policy sees outcome rewards that are almost always zero. It is nearly impossible to train via GRPO with sparse outcome rewards in this environment – after 24 hours, we were unable to sample enough trajectories to fill even a single training batch.

When training on this dataset, PPM significantly outperforms the next-best method. But perhaps more surprisingly, we found that training at length 4K is *comparable to or better* than training at length 8K!

![PPM performance at larger test-time token budgets](https://www.prestonfu.com/notes/ppm/pope.png)

Figure 4. When training on an extremely challenging math reasoning dataset, PPM significantly outperforms the next-best method (POPE) at a larger test-time token budget, measured in terms of either success rate or pass@8. Due to data filtering, GRPO was unable to make any progress.

Why does this happen? We found that this is due to a collapse in output length – the policy trained at length 8K may greedily guess at the answer and end its reasoning process early, while the policy trained at length 4K is never able to succeed within the training token budget and thus optimizes for partial progress. So, there is a regime of tasks like these where training at lower sequence lengths can be *beneficial*. Check out [our paper](https://arxiv.org/abs/2609.07303) for an extended discussion!

### What’s next?

We designed our method around two key desiderata:

1. The method is unbiased, in that the optimal policy under PPM matches the optimal policy under outcome rewards.
2. Rewards are assigned proportionally to partial progress toward the goal. By partial progress, we mean the expected terminal return conditioned on starting from the current (reasoning) state.

As we show in the paper, PPM satisfies desiderata (1). And in minimal settings like Figures 2 or 3, when we can trivially define reasoning points as reaching nodes along the reference trajectory or solving clearly-scoped intermediate subproblems, our method satisfies desiderata (2).

However, general reasoning tasks do not come with clean partitions into subproblems for free. Practically, we generate our reasoning points with an off-the-shelf LLM, and this generation procedure required a significant amount of iteration to produce a strong correlation between predicted progress and Monte Carlo returns. As we show in the paper, our approach outperforms naive rubric grading baselines according to our proposed reasoning point evaluations.

This opens up a variety of exciting directions:

- PPM extends well to settings with multiple given reference trajectories, as we can simply construct reasoning graphs as the union of the per-trajectory graphs. But with larger graphs, we incur more cost and variance in judging sampled trajectories. Can we efficiently construct “meta-graphs” or design new rewards?
- PPM can be viewed as an approximation to imitation learning, where we now have the freedom to visit reasoning points from the reference trajectory in any order. One nice resulting property is that *any* goal-reaching task can be determined entirely by a reference trajectory and a sufficiently good judge. So, this framework may enjoy the same benefits on non-verifiable environments.
- In practice, understanding the training dynamics of PPM and the relation between the data distributions, training token budget, trajectory segmenting procedure, and other factors may be critical to scaling imitation-based approaches to extremely long-horizon tasks. To ensure simplicity of the method, we reused our hyperparameters from standard GRPO, but there may be additional tricks to further stabilize training.

We’re very excited about this new space of methods that bridge imitation learning and RL, and hope to see new methods to tackle challenging, long-horizon domains!

### Acknowledgements

I'd like to thank [Aviral](https://aviralkumar2907.github.io/), [Kevin](https://kvfrans.com/), and [Oleg](https://olehrybkin.com/) for their helpful feedback on this post.

### Citation

```
@misc{fu2026longhorizonlanguagemodelreinforcement,
      title={Long-Horizon Language Model Reinforcement Learning via Progressive Point Matching},
      author={Preston Fu and Kevin Frans and Oleh Rybkin and Sergey Levine and Aviral Kumar},
      year={2026},
      eprint={2609.07303},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2609.07303},
}
```