---
type: raw-source
source_id: src-2026-07-16-bytebytego-rlhf-vs-dpo
title: "How LLMs Learn to Be Helpful (RLHF vs DPO)"
source: "https://blog.bytebytego.com/p/how-llms-learn-to-be-helpful-rlhf?utm_source=post-email-title&publication_id=817132&post_id=206407480&utm_campaign=email-post-title&isFreemail=true&r=6dm571&triedRedirect=true&utm_medium=email"
author:
  - "[[ByteByteGo]]"
published: 2026-07-14
created: 2026-07-16
description: "In this article, we will look at how that learning actually happens, starting with why instruction-following alone falls short, then walking through the two main methods for teaching preferences (RLHF and DPO)."
tags:
  - "clippings"
  - "source/raw"
---
## AWS Guide to Cloud Architecture Diagrams (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!jbLz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fb191c5-0313-4f95-a762-afff178bfa4d_2400x2400.png)

Enhance visibility into your cloud architecture with expert insights from AWS + Datadog. In this ebook, AWS Solutions Architects Jason Mimick and James Wenzel guide you through best practices for creating professional and impactful diagrams.

---

Ask a model the same question twice, phrased two different ways, and watch how it decides what to give you. It might offer a terse one-liner or a careful walk-through. It might sound fully confident, or it might hedge. Somewhere in training, the model learned which version you would rather have, even though both answers are correct.

That points to a harder question. How do you teach a model to be helpful when helpfulness changes with every request?

For a quick factual query, helpful means brevity. For a debugging problem, it means thoroughness. For a medical worry, it means caution paired with clarity. Each case requires a different direction with underlying trade-offs.

The model learned to handle those trade-offs from people comparing answers thousands of times over. This idea of learning from comparison rather than from a fixed answer key sits beneath every popular model you have used.

In this article, we will look at how that learning actually happens, starting with why instruction-following alone falls short, then walking through the two main methods for teaching preferences (RLHF and DPO).

## Pipeline

A useful model gets built in three stages, as shown in the diagram below:

![](https://substackcdn.com/image/fetch/$s_!dbfI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd72766d2-c766-4b0c-935c-e74bf3d6948b_2650x1382.png)

Let’s look at each stage in a bit more detail:

- The first stage is pretraining. The model reads an enormous amount of text and learns to predict the next word. In other words, it builds a broad sense of how language works and soaks up world knowledge along the way. What it gains is raw capability. What it still lacks is direction, because predicting the next word and answering your question are two different goals.
- The second stage is supervised fine-tuning, or SFT. We show the model thousands of example pairs, each an instruction together with a good response, and train it to imitate them. After this stage, the model follows instructions instead of continuing text. For example, if we ask a model to summarize a paragraph, it writes a proper summary. A raw model without SFT would have rambled on.
- The third stage teaches preferences, which will be the focus of the rest of this article.

Why does a model that already follows instructions need a third stage at all?

This is because SFT works through imitation. The model sees a correct answer and learns to copy its shape, which holds up well when a question has one good answer, but runs into problems when a question has many possible answers.

Consider a request like “explain how a hash map works”. A short answer and a long answer can both be excellent, and which one helps depends on who is asking. An example dataset can show one of those answers, while the trade-off between them stays invisible. Imitation teaches the model what a good answer looks like, but struggles to teach it how to weigh two good answers against each other.

The payoff is larger than it might appear at first. For example, when OpenAI built InstructGPT in 2022, human raters preferred answers from a 1.3 billion parameter aligned model over answers from the 175 billion parameter GPT-3, a model roughly a hundred times larger. The alignment stage mattered more than a hundredfold jump in size.

Nevertheless, the line between pretraining and SFT is cleaner in the example than in practice. Some recipes blend the two, but the three-stage view is the right place to start.

Next up, we need a signal that captures the trade-off directly. That signal is comparison.

---

## Introducing Attio: the agentic CRM. (Sponsored)

![](https://substackcdn.com/image/fetch/$s_!47nM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa99590e6-cb09-4389-b5e3-4e0bb5c62a2c_2870x1091.png)

Attio, the agentic CRM, makes it incredibly easy for anyone to run workflows for any GTM play they need.

Describe what you want, and Attio builds it. I just built a workflow that runs every morning, surfaces the deals that need my attention today, like anything with a stage change or a new signal in the last 24 hours.

Hundreds of thousands of automations already run on Attio every day. Ready to try now?

---

## Preferences

Comparison turns a judgment call into something a model can learn.

A preference example is simple. We take one prompt, generate two responses, and ask a person which is better. The result is a small piece of data, a prompt with a winner and a loser. If we collect enough of these, a pattern emerges that captures the trade-offs accurately.

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!LJnD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51464bbf-5bcd-4ab0-aaf9-081aba1535e0_2490x1330.png)

The reason this works comes down to what people are good at. Writing the single ideal response to a tricky prompt is hard, and two skilled people would produce different versions. Judging which of two responses is better is far easier, and people agree with each other more often when they compare than when they create. This is why labeling teams compare outputs instead of writing perfect ones from scratch, which makes the data trustworthy enough to train on.

This is the same comparison data InstructGPT collected, and the starting point for both methods we are about to compare. They differ in what they do with it, while the comparisons stay the same.

To clarify, the comparisons can come from another AI model in place of a person, an approach used in RLAIF and Constitutional AI. The overall mechanics stay the same.

Let us now look at the two different methods.

## RLHF

RLHF, short for Reinforcement Learning from Human Feedback, learns from comparisons by training a separate scorer and then coaching the model to score well against it.

See the below diagram that shows the basic RLHF flow:

![](https://substackcdn.com/image/fetch/$s_!7YkP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26014789-0519-40ea-b6f4-99b601046a6a_2334x1562.png)

It works in two moves once the comparisons are collected.

- First, we train a reward model. We take those prompt-with-a-winner examples and train a separate model to score any response, high for the kind people preferred and lower for the kind they passed over. The reward model turns scattered human judgments into a single function that grades fresh responses on its own.
- Second, we use that scorer to improve the main model, which here we call the policy. The policy writes a response, the reward model scores it, and a reinforcement learning algorithm called PPO nudges the policy toward higher-scoring responses.

Reinforcement learning, in plain terms, means learning from a reward signal through trial and error in place of labeled examples. Run the loop many times, and the policy drifts toward the answers people prefer.

Left to chase a score freely, a model will discover strange, degenerate text that games the scorer while reading badly. To guard against that, we keep a frozen copy of the starting model, the reference, and penalize the policy whenever it strays too far from it. This penalty, the KL term, lets the policy improve while staying close enough to fluent language to stay useful.

The reward model, the policy, the frozen reference, and a value model that PPO uses internally add up to four models in play during training.

That is the source of RLHF’s reputation for being expensive, fiddly, and slow to get right. However, this is also the pipeline behind the first version of ChatGPT, and it produced the first generation of genuinely helpful assistants at considerable cost.

Running a separate reward model and a full RL loop is a lot of moving parts. In 2023, a study from Stanford showed that much of it can collapse into a single step.

## DPO

DPO reaches the same goal with the same data, replacing the reward model and the RL loop with one training step.

DPO stands for Direct Preference Optimization, and the name fits. Rather than train a scorer and then optimize against it, the method tunes the model directly on the comparison pairs.

The mechanics sit close to ordinary supervised learning.

For each comparison, DPO adjusts the model to raise the probability of the preferred response and lower the probability of the rejected one, measured against that same frozen reference from before. The whole thing becomes a single loss that would train the way you would train a classifier. This is far simpler and steadier than an RL loop.

A common idea is that DPO removes the reward model, but what actually happens is subtler. The Stanford paper that introduced DPO carries the idea in its title that a language model is secretly a reward model. The reward signal is still present, but it now lives inside the policy itself rather than in a separate network.

![](https://substackcdn.com/image/fetch/$s_!U7RG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a06e3e9-fcdc-4b7c-ad06-96f448bb8231_2490x1480.png)

The approach proved itself quickly.

Zephyr, a 7 billion parameter model trained with DPO on machine-generated comparisons, beat Llama 2 Chat 70B, the strongest open RLHF model at the time, on a standard chat benchmark. Since then, DPO has become a staple in the industry.

By folding the reward into a single training step, DPO put alignment within reach of a small team on a modest budget, far from any large research cluster. A family of variants, such as SimPO, KTO, and ORPO, adjusts the objective in different ways. They share DPO’s core approach.

On cost and simplicity, DPO looks like a clear win. The catch is one it shares with RLHF, and it sits in the signal both methods trust.

## Reward Hacking

Both methods rely on a signal that only approximates human judgment, and leaning too hard on it can also backfire at times.

The reward model, whether trained explicitly in RLHF or folded into the policy in DPO, is a proxy. It approximates what people prefer. Like any approximation, it also has gaps. Optimize the model hard against that proxy, and it can start to exploit those gaps. In other words, the score climbs while the answers get worse.

Researchers at OpenAI measured this directly.

As the model optimizes against the proxy, true quality rises for a while, then peaks and slides backward even as the proxy score keeps climbing. They tied it to Goodhart’s law, the old observation that a measure stops being a good measure once it becomes the target.

![](https://substackcdn.com/image/fetch/$s_!e4_k!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd916e76f-8edf-4969-b936-cab2a9ec8466_2418x1454.png)

The everyday symptoms of this are familiar.

Models pad answers with length because longer responses tend to score well, and they learn to agree with whatever view you express. This behavior is called sycophancy. Anthropic found that most of the time, both human raters and reward models prefer a confident, agreeable answer over a correct one, which sometimes means flattery in place of truth.

The important part is that this trouble follows the data rather than the algorithm.

DPO inherits it just as RLHF does, because both learn from the same imperfect human judgments. Simpler training buys you a great deal, and this particular problem comes along for the ride. This is why your model sometimes agrees with you when you are clearly wrong. It learned that agreement tends to score well.

The KL penalty we discussed earlier softens this by holding the model near its starting point, though it shrinks the problem rather than completely erasing it.

If the root trouble is an imperfect human signal, a natural question follows. Could we replace it with a signal that is exact? For a certain class of tasks, we can.

## Verifiable Rewards

When a program can check the answer, the human reward becomes optional, and that single fact reshaped the final training stages across 2025 and 2026.

Some tasks have a checkable answer:

- A math problem is right or wrong.
- A piece of code passes its tests or fails them.

For these, we can replace the human-derived reward model with a verifier, a program that grades the result directly. The signal becomes exact and effectively free, clearing the proxy problem at its root for that work.

DeepSeek pushed this idea furthest.

They introduced an RL method called GRPO that drops one of the extra models PPO needs, and they trained their R1 reasoning model largely by rewarding correct final answers on math and code. The results matched the strongest closed reasoning models of the time. The model learned to reason by checking its own work, guided by a reward a calculator could supply.

The limit is that a verifier can grade a math proof. However, it stays silent on whether an answer is honest, kind, or appropriately cautious. Those qualities take many acceptable forms and resist any automatic test, the territory preference learning was built for. DeepSeek themselves kept reward models for the helpfulness and safety parts of R1, while verifiable rewards drove the reasoning.

This gives us the rule for the whole landscape.

When a machine can check the answer, reach for verifiable rewards. When the answer is a matter of judgment, reach for preference learning, whether RLHF or DPO. The method follows the signal.

See the diagram below:

![](https://substackcdn.com/image/fetch/$s_!PvwW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff189de82-9bcd-48b8-96a7-0818c4ee1886_2100x1246.png)

This is why reasoning models improved so quickly, and why even the best of them still rely on preference methods to stay pleasant and safe. Newer methods, such as DAPO and RLVR, extend the verifiable-reward idea, and they make up much of the active frontier in 2026.

## Conclusion

We can retrace the path in a sentence each:

- A raw model learns language and knowledge from pretraining.
- Supervised fine-tuning teaches it to follow instructions by imitation.
- A third stage teaches preferences, because the questions that matter most often have several good answers and a real trade-off between them.

Comparison is the signal that captures that trade-off, and the two main methods both run on it.

RLHF trains a separate reward model and optimizes against it with reinforcement learning, which is powerful and costly. On the other hand, DPO folds the same signal into a single training step, which is simpler and steadier while keeping the reward implicit rather than absent.

Both inherit the same catch, that a human signal is a proxy, and pushing on it too hard breeds sycophancy and quiet failures. And when a task has a checkable answer, verifiable rewards now sidestep the proxy entirely.

**References:**

- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)
- [Zephyr: Direct Distillation of LM Alignment](https://arxiv.org/abs/2310.16944)
- [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760)
- [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548)
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300)
- [DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning](https://www.nature.com/articles/s41586-025-09422-z)