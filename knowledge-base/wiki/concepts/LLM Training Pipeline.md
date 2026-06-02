---
type: concept
created: 2026-05-18
updated: 2026-05-18
tags:
  - concept
  - llm
  - training
  - alignment
  - post-training
source_ids:
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-05-18-hanfang-pytorch-practice
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
status: active
---

# LLM Training Pipeline

## Definition

The LLM training pipeline is the staged process by which a base next-token predictor becomes a usable assistant: large-scale pretraining builds general language competence, supervised fine-tuning shapes instruction-following behavior, and preference-driven post-training further aligns outputs to human judgments or reward signals.

## Why it matters

This is one of the most overloaded topic clusters in modern AI discourse. The PocketFlow tutorials are valuable because they turn a messy pile of acronyms—pretrain, SFT, RLHF, PPO, DPO, LoRA—into one connected map.

## Current synthesis

- **Pretraining** is the foundation. The `pretrain` tutorial presents it as self-supervised next-token prediction over massive unlabeled corpora. The base model learns grammar, world knowledge, and long-range statistical structure by repeatedly minimizing cross-entropy on tokenized text.
- The YC Paper Club presentation on **Pretraining Under Infinite Compute** sharpens one frontier question inside this stage: if the dataset is fixed but compute keeps increasing, how much extra generalization can optimization still extract? That is a useful counterpoint to the usual "just scale data and parameters" story.
- Pretraining creates a capable but misaligned model: the collection repeatedly describes it as a powerful **text-completion engine** or "statistical parrot." It knows language, but it does not inherently know how to behave like an assistant.
- **Supervised Fine-Tuning (SFT)** is the first post-training correction. The `sft` tutorial shows the crucial engineering trick: convert prompt/response examples into a single chat-formatted sequence, then **mask the loss on user-side tokens** so the model is only penalized on the assistant response.
- SFT produces instruction following, but it still treats quality as if there were exactly one correct answer per prompt. That makes it strong at imitation, weaker at learning nuanced preference orderings.
- From here the pipeline splits into two main preference-learning branches:
  - **RLHF + PPO**: collect human rankings, train a reward model with a Bradley-Terry / logistic objective, then optimize the policy against that learned reward while constraining drift from the SFT/reference model.
  - **DPO**: use the same style of preference data, but skip the explicit reward-model-then-RL loop and directly adjust the policy through relative likelihoods of chosen versus rejected responses against a reference model.
- The collection's most durable alignment insight is economic as much as algorithmic: **judging is easier than creating**. Preference data scales better than expert-written ideal responses, which is why reward-modeling, PPO-style RL, and DPO all become attractive after SFT.
- **LoRA** belongs in this pipeline as an efficiency layer rather than a separate learning objective. It changes *how* post-training updates are parameterized by freezing the large base weights and learning a low-rank update, making SFT or preference tuning feasible on smaller hardware budgets.
- The policy-gradient material in `rl-policy.md` also helps place RLHF historically. PPO is not a mysterious LLM-only trick; it sits on top of REINFORCE, baselines, actor-critic methods, and KL-regularized policy optimization.
- A good mental model is:
  - **Pretraining** teaches language and latent world structure.
  - **SFT** teaches response format and instruction-following behavior.
  - **Preference optimization** teaches ranking-sensitive behavior under human or learned reward signals.
  - **LoRA / efficiency methods** make those updates cheaper to run.
- [[Han Fang - PyTorch Practice]] is useful here as a lower-level implementation companion: it covers step/exponential/cosine schedulers, warmup-plus-cosine decay, gradient clipping, weight initialization, multi-GPU wrapping, and `eval()`/`no_grad()` inference hygiene—the practical mechanics any real LLM training stack still depends on.

## Open questions

- When is PPO-style RLHF still worth the extra complexity versus simpler direct preference objectives such as DPO?
- Which future post-training recipes will replace the current SFT → preference-optimization default for frontier LLMs?

## Related pages

- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Han Fang - PyTorch Practice]]
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]]
- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]
- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Reward Design for RL]]
- [[Search-Augmented Language Models]]
