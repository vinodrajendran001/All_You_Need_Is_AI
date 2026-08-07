---
title: "RL Environments are all you need"
source: "https://x.com/madiator/status/2084657077637746957"
author:
  - "[[@madiator]]"
published: 2026-07-26
created: 2026-08-07
description: "Recently I tweeted RL Environments are you need for RSI.Mahesh Sathiamoorthy@madiator·Jul 27Data curation (RL envs) is all you need for RSIQ..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HO4wSP2awAAzYc_?format=jpg&name=large)

Recently I tweeted RL Environments are you need for RSI.

> Jul 27
> 
> Data curation (RL envs) is all you need for RSI

In fact, I wanted to share my perspective today that RL environments are all you need, which holds beyond RSI. RL environments are all you need when you build agents!

## What we learned from Deep Learning

Remember the 60s and the 70s? I guess not, but anyhow, people at the time thought AGI is around the corner. They were building expert systems which were hand crafted if/else kind of heuristics and rules. Eliza was an expert-system chat bot built in 1966, and people thought it was great, until they figured it doesn't work, at all. The whole field collapsed and we went into AI winter.

![Image](https://pbs.twimg.com/media/HOxbTXCaMAABXuV?format=png&name=large)

The illusion of Eliza, a hand-crafted chatbot

Then neural networks happened. It invented a systematic way of solving problems. Rather than hand crafting heuristics, the model learns to approximate the distribution of what you are trying to learn. You have to **curate data and use compute** to train the model.

The models got better with scale. This got us deep learning, but also a good understanding of the importance of scaling compute. [The bitter lesson](https://www.cs.utexas.edu/~eunsol/courses/data/bitter_lesson.pdf) is by now very well understood.

Anyway, the community converged on to a recipe: we curated data**,** split it into train and test, and trained a model on the train set and tested if it generalizes on the test set. This we learned in the school and we applied well at work. Legions of ML engineers used this recipe to transform the world.

![Image](https://pbs.twimg.com/media/HOw_F1YasAAaZZl?format=jpg&name=large)

But the equivalent thing for agents is missing. What we need is to **figure out how to leverage compute to build agents.**

![Image](https://pbs.twimg.com/media/HOw_XZhbMAA2PNo?format=jpg&name=large)

So key questions:

- What's the data for agents?
- What constitutes an agent and how to leverage compute?

## Agent Data: RL Environments

The equivalent thing to data for agents is RL environments. We are expanding from from models that know things to agents that can do things.. in an environment. The agents are trained in these environments, and so that is now the new data.

The term "RL" in "RL Environment" is superfluous: it's just that people were using these environments for RL, but it's not necessary that RL needs to be used.

## What constitutes an agent?

Agent is essentially a LLM put in a harness along with a system prompt.

![Image](https://pbs.twimg.com/media/HOw5RCIakAAOphf?format=jpg&name=large)

Any of these can be tuned/updated. For example, the frontier labs heavily invest into updating the LLMs, while the rest of the population is mostly focused on updating the prompts. Harness engineering is now picking up.

Going back, let's see how we can leverage compute to update these components.

## Leveraging compute to update the LLM

This one is obvious. You can use RL to update the LLM's weights. Or SFT or even midtrain with the trajectories generated from the environment. This is what the labs use, and there are a number of success stories now outside the lab as well where people are able to train LLMs to customize for their agentic use cases.

This is a clear use of leveraging compute to update the LLM parameters. And **you need RL Environments** for that!

## Leveraging compute to update the system prompt

Most people have been writing prompts themselves but this doesn't work well for complex agents. Instead we are going to drift towards systems which use tools like [GEPA](https://arxiv.org/abs/2507.19457) or autoresearch to find the best system prompt that works for you.

Ultimately you and me are worse than powerful LLMs that can inspect, reflect, and write the system prompts. This is just the bitter lesson surfacing again.

For GEPA or autoresearch or evolutionary algorithms, you need to systematically have a way to get the score of how well a prompt is doing, and curate train/test splits (you want to iterate on the the train split, and see if you generalize on the test split).

So ultimately this is achieved by **having good RL environments!**

## Leveraging compute to update the harness

This is a bit of a new field!

People are iterating on harness manually, but like everything else, I believe, we will have mechanisms to automate building of harness (it's essentially a piece of software).

The closest paper I know of is [Meta-Harness](https://arxiv.org/pdf/2603.28052) work.

![Image](https://pbs.twimg.com/media/HOxa3TYaEAA2yAc?format=jpg&name=large)

We are going to see a lot more work come out next year perhaps! At any rate, the best way to iterate over the harnesses is to have **a set of RL environments for your use case**.

## RL Environments are all you need for Evals

Beyond training the agents, you can use RL environments to do systematic evals (rather than the vibe evals that people do now).

For example Snowflake CEO compared GLM-5.2 with Opus 4.7 and he did that by having access to 103 RL environments for dbt (guess who curated this data?).

> Jun 24
> 
> Early results from the @snowflake's coco team on GLM-5.2 vs Opus-4.7 on dbt-bench — what the trajectories actually show

## RL Environments are all you need!

Gist of what I have said:

- ML recipe means you curate data, and leverage compute to train a model on the data.
- The new agent recipe is to curate RL environments, and leverage compute to do one or more of: (1) updating the weights, (2) updating the system prompt, and (3) updating the harness.
- Even if you are not doing any of these, you should at least use them to do evals.
- And so RL environments are critical for building agents, and you are probably not investing enough into curating them.

This is why [@bespokelabsai](https://x.com/@bespokelabsai) is razor focused on doing research and shipping RL environments. Whether you are a lab or an enterprise building/evaluating agents, RL environments are all you need.

Next time, I will talk about what RL envs mean for software and for RSI.