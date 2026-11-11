---
title: "What objective is reasoning solving?"
source: "https://alexwang.ai/posts/reasoning-as-pathfinding/?utm_source=tldrai"
author:
  - "[[Alex Wang]]"
published: 2026-11-08
created: 2026-11-11
description: "Reasoning as pathfinding in token space."
tags:
  - "clippings"
---
Contents

Reasoning as pathfinding. Each sample is an attempt to find a path from the starting context to a correct answer in .

There’s an intuitive but simplified picture of reasoning: let a model think for longer, and it’ll be more likely to be correct. This aligns well with our human intuition: spend more time and effort on thinking and it’s more likely that we’ll arrive at a correct answer.

But this picture doesn’t seem to explain everything. During RL training, models learn to write longer chains of thought, and they get more accurate as they do. Yet if you take a trained model and force any one chain to run longer, it helps for a while, then stops helping.[^1] Sometimes the answer even gets *worse*, as if it’s overthinking.[^2] If a chain of thought were truly converging toward some optimum, more steps shouldn’t make it worse. So is it really the length of each chain that helps at inference time? Or is it something more subtle?

This post is my attempt to clarify this confusion (mostly for myself) by looking at reasoning as pathfinding through token space. We’ll see that RL maximizes the probability of finding a path from to , but individual paths are not guaranteed to converge to the correct answer. As a bonus, this perspective clarifies some odd observations about reasoning models, like unfaithful chains of thought and reward hacking.

## Reasoning as pathfinding

Ask a reasoning model the same math problem ten times and you’ll get ten different chains of thought. Rather than thinking of reasoning as one mysterious process heading toward an answer, let’s think of it as pathfinding in token space. There are many paths from the problem to a correct answer, and the model traverses one of them with each sample.

Consider the problem: “what’s ”? One solution is to add the numbers one at a time: 1, 3, 6, 10, and so on up to 55. Another way is to pair them from the outside in: , , , and each make 11, and five pairs of 11 make 55. Both of these paths land on the correct answer, 55.

We can think about reasoning as following this general pattern. We are given a starting point, the prompt, which we’ll call . We want to find a path that starts from and ends at a correct answer . To tell whether a path lands in the right place, we assume we have a verifier that returns 1 if is correct and 0 if it isn’t.

So given a starting point , we want to find a path of tokens that lands in the set

[The figure at the top of this post](#pathfinding-figure) sketches this picture. Each gray line is a sampled path: it starts from the prompt on the left, meanders in token space by sampling , with some of these paths landing in .

Since many paths land in , the success probability adds up over all of them. Let be the probability that the model generates the path given the prompt , and for the final answer at the end of . The probability of success is the probability of generating each path, times the probability that path lands in , summed over every path:

The second factor is just 1 if the path lands in and 0 if it doesn’t, so we sum only the probability of paths that land in :

We’ll call the **success probability**. Maximizing this probability means our model will be more likely to sample a path that lands in .

Note that there are two ways of increasing this probability. Either the model can sample multiple paths to the same answer, each with a small probability, or the model can sample a single path to the answer with a very high probability. The success probability doesn’t care which one we get, but in practice we might want to prioritize specific paths or ensure diversity in the samples [^3].

## How do we boost our success probability?

### Best-of- sampling

The simplest way to pathfind is to have the model keep sampling paths until one lands in .

Since we assumed we had a verifier, we can do best-of- sampling, which samples paths and looks for a success. Each path misses with probability , so all miss with probability , and the success probability rises from to

This is a guaranteed axis of compute-scaling. As long as , the success probability increases monotonically as we sample more paths, so spending more compute on more samples always helps, as seen early on by [Brown et al. 2024](https://arxiv.org/abs/2407.21787). However, the scaling here is over the number of samples rather than the length of the paths (thinking longer).

### Train the model to generate better samples

So far the model was fixed, so was fixed too. Can we change the model to increase itself?

Here’s a simple way to do this. Collect many prompts whose answers we can check. For each one, sample some paths from the model. We keep the paths that land in , and train the model on the ones we kept. Then repeat. Each round, we train the model to put more weight on the successful paths that it sampled. This loop is called rejection-sampling fine-tuning, and [STaR](https://arxiv.org/abs/2203.14465) was an early version of it for reasoning.

RL with a verifiable reward, which is how today’s reasoning models are trained, turns out to do almost the same thing. Let be the model with weights . Then since exactly when :

meaning the expected binary reward is exactly the success probability .

Computing the gradient of the success probability via the log-derivative trick, we arrive at

which is exactly the policy gradient, also called the REINFORCE estimator. Now estimate this gradient with sampled paths . The paths that failed have and disappear, while the paths that land in have . If of the paths succeed, the estimate is

This gradient involves two terms: the empirical success rate and the average log likelihood of the successful paths.

In other words, a step of REINFORCE with a binary reward is a step of rejection-sampling fine-tuning on the model’s own sampled paths, scaled by the current success rate .

This also explains the first observation from the intro, that chains of thought get longer during RL training. Each step pulls the model toward the paths that landed, so if the paths that succeeded tended to be longer than the ones that failed (e.g. because they include backtracking behavior, gather more feedback from the environment, or just dumb luck), the model will learn to write longer paths.

## Amortization and generalization

During RL training, we spend a lot of compute to search for good paths and then we train the model to generate those paths directly. Once trained, the model can produce the answer without spending all this extra compute on sampling multiple paths. This is called *amortizing* the search: we pay for it once during training, so we don’t have to pay for it every time we ask the model a question.[^4] Since we train a *single model* on many prompts, the model can potentially *generalize* to new prompts it has never seen.

The figure below shows this for four prompts, each with its own , and switches between the model before and after training. During training, we sample paths from every prompt, keep the ones that succeed, and SFT on them. The percentages show the empirical rate of success given each prompt. The hollow prompt is new and not seen before by the model, but the model generalizes to this new prompt after training. As the new prompt gets further from the training distribution, its accuracy drops (try dragging it!).

before trainingafter training

Try dragging the new prompt.

## Revisiting some observations about reasoning

Once we see a reasoning model as a distribution trained to land in given any , a few odd facts about these models become clear.

### Chains of thought are not guaranteed to be faithful

Our verifier above only checks whether the answer is correct. The reward is 1 if and 0 otherwise, so the intermediate tokens are just a way for the model to get to the answer. Nothing requires those tokens to be true, or to explain the answer that follows, though of course these are often correlated due to the model’s pretraining.

If we want meaningful chains of thought, we need to adjust the rewards or the training objective.

### Reward hacking comes from both the verifier and the sampler

We also assumed the verifier is never wrong, that if and only if is actually the correct answer to . But in practice the verifier can be imperfect. Then , the set of answers the verifier accepts, isn’t the same as the set of correct answers: it can include wrong answers and leave out correct ones. This misspecification opens up regions of that the model might learn to land in even though it’s not what we intended.

Thus reward-hacking comes from an imperfect verifier, which fails to capture what we truly want, as well as an imperfect sampling procedure which fails to stay away from these shortcut regions.

In the figure below, the dashed circle is the set of correct answers and the red ellipse is . The ellipse stretches back toward the prompt, so its wrong answers are the easiest to reach, and after training most paths land there.

before trainingafter training

This visualization also shows why scaling up RL (generating more samples and longer samples) makes reward hacking more likely. The more extensively we “fuzz” the verifier, the more likely we’ll find a path that lands in the misspecified region of . Once the model finds this shortcut, training pushes the model towards similar behavior.

## So what objective is reasoning solving?

Reasoning isn’t actually solving any objective at all. A path is not guaranteed to converge to the correct answer. It’s only in aggregate, over the distribution of paths, do we get a high probability of success.

RL training directly raises the success probability , by spending a lot of compute on searching for successful paths and then training the model to reproduce them. Thinking longer helps because training taught the model to use the extra tokens, not because generating more tokens is intrinsically better. The cost of sampling during RL is amortized into the weights. At inference time the model is likely to succeed with a single sample, but any individual sample is not guaranteed to succeed.

Cite this post

```
@article{wang2026reasoningaspathfinding,
  author = {Alex Wang},
  title = {What objective is reasoning solving?},
  journal = {alexwang.ai},
  year = {2026},
  month = {Nov},
  url = {https://alexwang.ai/posts/reasoning-as-pathfinding/}
}
```

[^1]: [Muennighoff et al. 2025](https://arxiv.org/abs/2501.19393) forced a model to keep thinking by appending “Wait” whenever it tried to stop. Accuracy rose at first, and then flattened.

[^2]: A neat example is [Gema et al. 2025](https://arxiv.org/abs/2507.14417) which found tasks where longer reasoning resulted in worse accuracy.

[^3]: We might revisit this in a future post.

[^4]: This idea of using expensive search to find a better answer and then training a network to output the answer cheaply, shows up outside language models too. [AlphaZero](https://arxiv.org/abs/1712.01815) runs a tree search at every move of self-play and trains its policy network to prefer the moves that were found ([expert iteration](https://arxiv.org/abs/1705.08439) is the same idea). Physicists and weather forecasters do it with simulators: they run an expensive hand-crafted simulation to get an answer, then train a neural network to predict that answer directly.