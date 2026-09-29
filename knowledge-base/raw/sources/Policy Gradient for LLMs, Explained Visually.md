---
title: "Policy Gradient for LLMs, Explained Visually"
source: "https://www.tylerromero.com/posts/2026-09-policy-gradient/?utm_source=tldrai"
author:
  - "[[Tyler Romero]]"
published: 2026-09-27
created: 2026-09-29
description: "A from-scratch derivation of REINFORCE for language models"
tags:
  - "clippings"
---
Most RL algorithms used to train language models, from PPO to GRPO, are elaborations of one idea: the policy gradient. This post derives it from scratch for an LLM solving a problem with a checkable answer. It follows one prompt, “What is 17 × 24?”, from next-token probabilities to the gradient that makes correct answers more likely.

## Language models as policies

Given a prompt $x$, a language model generates a completion $y = (y_1, \dots, y_T)$ one token at a time. In RL terms, the model is a *policy*: at each step it looks at the prefix it has produced so far and outputs a distribution over the next token, from which one token is sampled.

![The prompt "What is 17 × 24? Show your work, then give a final answer." and a completion in progress, "17 × 24 = 17 × 20 + 17 × 4 = 340 +", followed by an empty slot. Below it, the model's probabilities for the next token: 68 at 0.82, the slip 58 at 0.07, and small amounts for other tokens. One token is sampled, appended, and the process repeats.](https://www.tylerromero.com/assets/img/BEWlv0FZ3U-1265.webp)

The probability of the full completion is the [product of the per-token probabilities](https://www.tylerromero.com/posts/2024-04-dpo/#the-probability-of-a-completion):$\theta$ is the model’s parameters: its weights, which training adjusts.

$$
p_\theta(y \mid x) = \prod_{t=1}^{T} p_\theta(y_t \mid x, y_{<t})
$$

Generating a completion traces one path through a tree of possible continuations.Each $p(\cdot)$ in the tree is conditioned on the prompt and on every token before it on the path, so $p(24)$ means $p(24 \mid x, 17, \times)$. The slot from the previous figure is one branch point: 68 leads to the correct answer, and the 58 slip to a wrong one. Once the model emits a stop token, a reward function grades the finished completion.

![A tree of possible completions for "What is 17 × 24?". The sampled path starts 17, ×, 24, and its probability is the product 0.6 × 0.9 × 0.7. At "340 +", it branches to 68 with probability 0.82 or 58 with 0.07. The completion reaching 408 gets reward 1 from the verifier, and the one reaching 398 gets reward 0.](https://www.tylerromero.com/assets/img/ahhRWygIoF-1344.webp)

For reasoning tasks, the reward function is often a verifier that returns $R(x, y) = 1$ if the final answer is correct and $0$ otherwise. Our goal is to find the parameters $\theta$ that maximize the expected reward, which we call the objective $J(\theta)$:

$$
J(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \; y \sim p_\theta(\cdot \mid x)}\big[R(x, y)\big]
$$

This is the standard reinforcement learning objective.

From here on, I’ll drop the prompt $x$ from the notation; everything is conditioned on it.

## The policy gradient

To improve the model, we want to follow the gradient of the objective, $\nabla_\theta J(\theta)$: the direction in parameter space that most increases the expected reward. This gradient is the **policy gradient**, and methods that train by estimating and following it are called policy gradient methods. REINFORCE, [PPO](https://arxiv.org/abs/1707.06347), and GRPO are all examples. They share this expected-reward goal, but PPO and GRPO also change the update itself, clipping or reweighting it to keep training stable.

The hard part is computing it. Written out, the objective is a sum over every possible completion:

$$
J(\theta) = \sum_y p_\theta(y) \, R(y)
$$

$\theta$ appears only in $p_\theta(y)$, how likely each completion is, and not in the reward $R(y)$. If we could evaluate this sum, we could differentiate it directly, but there are far too many completions to enumerate.With a vocabulary of about 150,000 tokens, even a 100-token completion has more than $10^{500}$ possibilities.

The usual fix for an expectation we can’t enumerate is to estimate it by sampling: generate $N$ completions, compute their rewards, and average them. That gives a fine estimate of $J$, but not one we can differentiate. The completions are discrete token sequences, and their rewards come from a verifier, a unit test, or a person, none of which we can backpropagate through. There is no path for autograd to follow from the reward back to $\theta$.

Compare supervised fine-tuning, where the completion $y$ is fixed training data and $\theta$ appears directly in the loss $-\log p_\theta(y)$. Here, $\theta$ decides *which* completions we get, not how any one of them is graded. What we need is a way to rewrite $\nabla_\theta J$ as an average, over sampled completions, of something we *can* differentiate.

## The log-derivative trick

The workaround is a one-line identity, $\nabla_\theta p_\theta = p_\theta \nabla_\theta \log p_\theta$,By the chain rule, $\nabla_\theta \log p_\theta = \nabla_\theta p_\theta / p_\theta$. Multiply both sides by $p_\theta$. which moves the gradient inside the expectation:

$$
\begin{aligned}
\nabla_\theta J(\theta)
&= \nabla_\theta \, \mathbb{E}_{y \sim p_\theta}\big[R(y)\big] \\
&= \nabla_\theta \sum_y p_\theta(y) \, R(y) \\
&= \sum_y \underbrace{\nabla_\theta p_\theta(y)}_{\mathclap{\text{depends on } \theta}} \, R(y) \\
&= \sum_y \underbrace{p_\theta(y) \, \nabla_\theta \log p_\theta(y)}_{\mathclap{\text{the identity}}} \, R(y) \\
&= \mathbb{E}_{y \sim p_\theta}\big[R(y) \, \underbrace{\nabla_\theta \log p_\theta(y)}_{\mathclap{\text{the score}}}\big]
\end{aligned}
$$

This derivation is a special case of the *policy gradient theorem* ([Sutton et al., 2000](https://papers.nips.cc/paper/1713-policy-gradient-methods-for-reinforcement-learning-with-function-approximation)), and the third line is its key step. In general RL, a policy’s actions change which states it ends up in, so you might expect the gradient of the objective to include a term for how the distribution of visited states changes with $\theta$. That term would be hard to compute, because it depends on the environment’s dynamics. The point of the theorem is that it never appears: the gradient needs only the gradients of the policy’s own probabilities, weighted by how much reward each choice leads to. For language models, this is easy to see. Appending a token always produces the same next prefix, so there are no environment dynamics, and the only way $\theta$ affects which completions we get is through $p_\theta$ itself.

The quantity $\nabla_\theta \log p_\theta(y)$ is called the **score**. It points in the direction in parameter space that most increases the log-probability of the completion $y$. The final line is an expectation over completions sampled from the policy $p_\theta$ itself, so we can estimate it by sampling. Perform $N$ *rollouts* (that is, draw $N$ completions from the policy), score each one, and average:

$$
\nabla_\theta J(\theta) \approx \frac{1}{N} \sum_{i=1}^{N} R(y_i) \, \nabla_\theta \log p_\theta(y_i), \qquad y_i \sim p_\theta
$$

This is the REINFORCE estimator, also known as the *Monte Carlo policy gradient*: it estimates the gradient by averaging over complete sampled rollouts, using each one’s actual reward rather than a learned estimate of how good it was. Each term pairs a direction with a weight: the score points toward making that rollout’s completion more likely, and the reward sets how much that direction counts.

![Four rollouts for "What is 17 × 24?": A (an arithmetic slip) and D (an estimate) earn reward 0, while B and C reach 408 and earn 1. A bar holding all the probability for this prompt shows B rising from 0.22 to 0.27 and C from 0.03 to 0.05 after one update, A and D barely changing, and unsampled completions shrinking.](https://www.tylerromero.com/assets/img/3FHlCcUqnt-1608.webp)

Four rollouts for "What is 17 × 24?": A (an arithmetic slip) and D (an estimate) earn reward 0, while B and C reach 408 and earn 1. A bar holding all the probability for this prompt shows B rising from 0.22 to 0.27 and C from 0.03 to 0.05 after one update, A and D barely changing, and unsampled completions shrinking.

Because all completions share a total probability of 1, B’s and C’s gains come from elsewhere, here mostly from completions nobody sampled. A barely changes, because it shares everything up to “340 +” with B, so reinforcing B also lifts most of A’s path. The numbers are only illustrative: B and C are pushed up, but how every other completion moves depends on how the model’s parameters are shared.

With the reward held fixed, $R \, \nabla_\theta \log p_\theta(y)$ is exactly the gradient of $R \log p_\theta(y)$: a log-likelihood on one of the model’s own samples, weighted by its reward. So **policy gradient is supervised fine-tuning on your own samples, weighted by reward.** With $+1/0$ rewards, as in the figure above, it is literally SFT on the correct completions, so incorrect completions are never pushed down directly; they only lose share.

## From sequences to tokens

A completion’s log-probability is a sum of per-token log-probabilities, so its score breaks into one term per token:

$$
\nabla_\theta \log p_\theta(y) = \sum_{t=1}^{T} \nabla_\theta \log p_\theta(y_t \mid y_{<t})
$$

Each term is the score of a single token: the direction that most increases the probability of choosing $y_t$, given everything generated before it. So we can study the update one position at a time. Pick a single position, such as the slot right after “340 +” in the 17 × 24 example, and hold its prefix $y_{<t}$ fixed. For each token $v$ in the vocabulary, write

$$
p_v = p_\theta(v \mid y_{<t}) \qquad \text{and} \qquad s_v = \nabla_\theta \log p_v
$$

for the model’s probability of choosing $v$ at this position and that token’s score. In the example, $p_{68} = 0.82$ and $p_{58} = 0.07$.

Only one token is actually sampled at each position. Its contribution to the update is $R \, s_{y_t}$: that token’s score, multiplied by the reward the whole completion earned.

To see what a token’s score looks like, look at the last layer. At one position, the network outputs a logit $z_u$ for every token $u$ in the vocabulary, and $p = \operatorname{softmax}(z)$. Differentiating the log-softmax gives the **logit gradient** of the chosen token $v$:

$$
\log p_v = z_v - \log \sum_u e^{z_u}
\qquad\Longrightarrow\qquad
\frac{\partial \log p_v}{\partial z_u} =
\begin{cases}
1 - p_v & u = v \\
-p_u & u \neq v
\end{cases}
$$

It is positive on the chosen token’s own logit, negative on every other logit in proportion to that token’s probability, and sums to zero. The score is this vector carried back through the network to the parameters by the chain rule:

$$
s_v = \sum_u \big(\mathbb{1}[u = v] - p_u\big) \, \nabla_\theta z_u
$$

As $p_v \to 1$, every coefficient in this sum goes to zero, so the score does too. Across completions A and B from the figure above:

![Completions A (reward 0) and B (reward 1) as rows of tokens, each labeled with its probability and its own-logit gradient, 1 − p, with an arrow of that length. In A, every score is multiplied by 0, so nothing updates, not even the unlikely slip 58. In B, uncertain tokens like 17, 24, and 68 get large gradients and confident filler almost none. Zoom-ins below B show the full logit gradient summing to zero.](https://www.tylerromero.com/assets/img/b1CUApi4fR-1728.webp)

Completions A (reward 0) and B (reward 1) as rows of tokens, each labeled with its probability and its own-logit gradient, 1 − p, with an arrow of that length. In A, every score is multiplied by 0, so nothing updates, not even the unlikely slip 58. In B, uncertain tokens like 17, 24, and 68 get large gradients and confident filler almost none. Zoom-ins below B show the full logit gradient summing to zero.

The reward only says whether the finished completion was right, so every position gets the same $R$, whatever its token did: A’s correct opening steps get nothing, and B’s filler tokens get the full reward. What differs from token to token is the score, which is tiny for tokens the model was already sure of.

## The score has zero mean

The score has a simple but important property. On-policy, when the token is sampled from the same distribution $p$ whose score we compute, the expected score is exactly zero:

$$
\begin{aligned}
\mathbb{E}_{y_t \sim p}[s_{y_t}] &= \sum_v p_v \, \nabla_\theta \log p_v = \sum_v \nabla_\theta p_v \\
&= \nabla_\theta \sum_v p_v = \nabla_\theta 1 = 0
\end{aligned}
$$

Intuitively, probability is conserved. Any change to $\theta$ that makes some tokens more likely must make others less likely by the same total amount. Weighted by how often each token is sampled, the pushes cancel.

We can check this at the logits. In vector form, the logit gradient from the previous section is $e_v - p$, where $e_v$ is the one-hot vector for $v$; the zoom-ins in the figure above show it for 68 and for “=”. Averaging these vectors over which token gets sampled, weighted by $p$, gives $\sum_v p_v (e_v - p) = p - p = 0$.

## Baselines and group centering

Nothing so far required the rewards to be $+1/0$. What if we use $+1/-1$ instead? That doubles every reward and then subtracts 1. Doubling just doubles the gradient. For the shift, the zero-mean identity is the answer: we can subtract any baseline $b$ from the reward without changing the expected gradient, as long as $b$ does not depend on the sampled token:

$$
\mathbb{E}_{p}\big[(R - b) \, s_{y_t}\big] = \mathbb{E}_{p}[R \, s_{y_t}] - b \, \underbrace{\mathbb{E}_{p}[s_{y_t}]}_{=\,0} = \mathbb{E}_{p}[R \, s_{y_t}]
$$

The quantity $A = R - b$ is called the **advantage**. Subtracting a baseline adds no bias: REINFORCE stays unbiased, with exactly the same expected gradient. What it can change is the variance, and a well-chosen baseline reduces it dramatically. To see why, split each rollout’s term in two:

$$
R \, s_{y_t} = \underbrace{b \, s_{y_t}}_{\text{mean zero, but noisy}} + \underbrace{(R - b) \, s_{y_t}}_{\text{the advantage-weighted part}}
$$

The first part contributes nothing to the expected gradient, but each sample of it is a large vector pointing somewhere different. In the extreme case where every completion earns $R = 1$, the true gradient is zero, yet each sample still pushes its own log-probabilities up at random. With $b = 1$, every term vanishes. How much a baseline helps depends on $b$. The standard choice is the prompt’s expected reward. It isn’t exactly optimal, but it is simple to estimate, and because some prompts are far easier than others, estimating it per prompt removes a large source of noise.

GRPO popularized a simple, critic-free baseline for LLMs: sample a group of $G$ completions for each prompt and use the group’s mean reward as the baseline for each of them:

$$
A_i = R_i - \frac{1}{G} \sum_{j=1}^{G} R_j
$$

Correct completions now get a positive advantage and are reinforced. Incorrect completions get a negative advantage and are suppressed. Prompts where every completion succeeds, or every completion fails, contribute nothing. For the four rollouts from earlier:

![The same four rollouts with group-centered advantages. The group mean reward is 0.5, so B and C get advantage +0.5 and are pushed up, while A and D get −0.5 and are pushed down. Along the prefix A and B share, their pushes cancel.](https://www.tylerromero.com/assets/img/IJECdtISgt-1267.webp)

REINFORCE with group-centered advantages fits in a few lines of PyTorch:

```python
def reinforce_loss(logprobs, rewards, mask, group_size):
    # logprobs: (B, T) per-token log p_θ(y_t | y_<t)
    # rewards:  (B,)   one per completion, grouped by prompt
    # mask:     (B, T) 1 on completion tokens, else 0
    r = rewards.view(-1, group_size)
    advantages = (r - r.mean(dim=1, keepdim=True)).view(-1)
    seq_logprobs = (logprobs * mask).sum(dim=1)  # log p_θ(y)
    return -(advantages * seq_logprobs).mean()
```

The advantages are constants that carry no gradient, so differentiating this loss gives exactly the estimator from the previous sections, with advantages in place of rewards. PPO, GRPO, [DAPO](https://arxiv.org/abs/2503.14476), and most other RL algorithms used for LLMs start from this loss and add clipping, masking, or reweighting.

## The on-policy assumption

Both identities in this post, the log-derivative rewrite and the zero-mean score, assume that **the completions are sampled from the same distribution $p_\theta$ that we differentiate**. In the rewrite, $p_\theta$ is both the distribution we average over and the model we differentiate. In the zero-mean identity, averaging over $p$ itself is what makes the pushes cancel. If the samples come from even a slightly different distribution, the expected score is no longer guaranteed to be zero, and subtracting a baseline shifts the expected gradient instead of leaving it unchanged.

In practice, this assumption rarely holds exactly. In the `reinforce_loss` above, `logprobs` comes from the training framework’s forward pass, but the completions were generated by a separate inference engine, such as [vLLM](https://github.com/vllm-project/vllm) or [SGLang](https://github.com/sgl-project/sglang). The two are supposed to compute the same distribution, but they seldom do. They can run at different numerical precisions, and in asynchronous setups the inference engine may still be serving weights from a few updates ago. Either way, the completions come from a slightly different model than the one being trained. That gap is where the trouble starts.