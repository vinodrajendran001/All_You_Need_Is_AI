---
type: concept
created: 2026-05-18
updated: 2026-06-04
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
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-06-03-fareed-khan-train-llm-from-scratch
  - src-2026-06-04-efficient-reasoning-edge
  - src-2026-06-04-progressive-thought-encoding
  - src-2026-06-04-pace-efficient-reasoning
  - src-2026-06-04-extreme-ratio-cot-compression
  - src-2026-06-04-reasoncache
  - src-2026-06-04-difficulty-aware-entropy-regularization
  - src-2026-06-04-conpress
  - src-2026-06-04-dss-grpo-cot-compression
  - src-2026-06-05-dharma-ai-dpo-beyond-chatbots
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
- The Reiner Pope flashcards add a deployment-economics perspective to the same stage: once you count **pretraining + RL + inference** together, it can become rational to pretrain far beyond Chinchilla-optimal data scales if heavy downstream RL and long-lived inference dominate lifetime cost.
- Pretraining creates a capable but misaligned model: the collection repeatedly describes it as a powerful **text-completion engine** or "statistical parrot." It knows language, but it does not inherently know how to behave like an assistant.
- **Supervised Fine-Tuning (SFT)** is the first post-training correction. The `sft` tutorial shows the crucial engineering trick: convert prompt/response examples into a single chat-formatted sequence, then **mask the loss on user-side tokens** so the model is only penalized on the assistant response.
- SFT produces instruction following, but it still treats quality as if there were exactly one correct answer per prompt. That makes it strong at imitation, weaker at learning nuanced preference orderings.
- From here the pipeline splits into two main preference-learning branches:
  - **RLHF + PPO**: collect human rankings, train a reward model with a Bradley-Terry / logistic objective, then optimize the policy against that learned reward while constraining drift from the SFT/reference model.
  - **DPO**: use the same style of preference data, but skip the explicit reward-model-then-RL loop and directly adjust the policy through relative likelihoods of chosen versus rejected responses against a reference model. See [[Direct Preference Optimization]] for a full treatment.
- The collection's most durable alignment insight is economic as much as algorithmic: **judging is easier than creating**. Preference data scales better than expert-written ideal responses, which is why reward-modeling, PPO-style RL, and DPO all become attractive after SFT.
- [[Dharma-AI - Direct Preference Optimization Beyond Chatbots]] sharpens what SFT and DPO actually fix at a mechanistic level: SFT closes the *distance* between a generalist model and the task domain; DPO explicitly moves the distribution *away* from identifiable failure geometries (attractor regions). These are orthogonal operations — more SFT data cannot substitute for DPO's completion-level signal. The DharmaOCR system demonstrated this by using the model's own degenerate outputs (repetition loops) as self-generated rejection pairs, achieving 59.4% average degeneration reduction across five model families with no human annotation. This is a practically important generalisation: DPO is not only a chat-alignment tool but a reliability improvement mechanism wherever failure modes are categorically identifiable and automatically scoreable.
- **LoRA** belongs in this pipeline as an efficiency layer rather than a separate learning objective. It changes *how* post-training updates are parameterized by freezing the large base weights and learning a low-rank update, making SFT or preference tuning feasible on smaller hardware budgets.
- [[Efficient Reasoning on the Edge]] adds a deployment-aware post-training recipe for small reasoning models: SFT on high-quality reasoning traces first unlocks explicit reasoning, then GRPO-based RL applies a budget-aware reward to compress those traces, and separate switcher / verifier heads shape how the model behaves at inference time. This is a useful reminder that post-training objectives may target **shorter reasoning and hardware viability**, not only generic helpfulness or preference alignment.
- The same paper also weakens the clean separation between "training" and "deployment." Its Quantization-Aware Modular Reasoning setup trains reasoning adapters directly on top of a quantized base model, suggesting that quantization can be part of the post-training recipe itself rather than only a final export step.
- The newer efficient-reasoning batch makes this even clearer: a growing post-training subfield now optimizes **how much visible reasoning a model emits**. Some approaches use difficulty-aware RL penalties (PACE, CEEH, DSS-GRPO, the Qualcomm paper), some use compressed supervision plus ratio-aware optimisation (Extra-CoT), some exploit self-supervised contextual pressure (ConPress), and some replace long traces with fixed-size vectors or KV caches (Progressive Thought Encoding, ReasonCACHE). See [[Reasoning Compression]].
- The policy-gradient material in `rl-policy.md` also helps place RLHF historically. PPO is not a mysterious LLM-only trick; it sits on top of REINFORCE, baselines, actor-critic methods, and KL-regularized policy optimization.
- A good mental model is:
  - **Pretraining** teaches language and latent world structure.
  - **SFT** teaches response format and instruction-following behavior.
  - **Preference optimization** teaches ranking-sensitive behavior under human or learned reward signals.
  - **LoRA / efficiency methods** make those updates cheaper to run.
- [[Han Fang - PyTorch Practice]] is useful here as a lower-level implementation companion: it covers step/exponential/cosine schedulers, warmup-plus-cosine decay, gradient clipping, weight initialization, multi-GPU wrapping, and `eval()`/`no_grad()` inference hygiene—the practical mechanics any real LLM training stack still depends on.
- [[Fareed Khan - Train LLM From Scratch]] adds an end-to-end pretraining implementation path: download shards of The Pile, tokenize them with `tiktoken` `r50k_base`, append `<|endoftext|>` separators, pack tokens into HDF5, train a decoder-only model with AdamW and periodic dev evaluation, then sample from the saved checkpoint. It is a strong code-first bridge between the conceptual pipeline and an actual runnable GPT-style pretraining stack.
- The same repository also contains a separate `sft_rlhf_guide.ipynb`, which signals that the author's mental model of the pipeline extends past base pretraining into post-training stages rather than stopping at next-token prediction.

## Open questions

- When is PPO-style RLHF still worth the extra complexity versus simpler direct preference objectives such as DPO?
- Which future post-training recipes will replace the current SFT → preference-optimization default for frontier LLMs?

## Related pages

- [[The Pocket - PocketFlow Tutorial Docs]]
- [[The Pocket]]
- [[Han Fang - PyTorch Practice]]
- [[Fareed Khan - Train LLM From Scratch]]
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[AI Accelerator Architecture]]
- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]
- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Dharma-AI - Direct Preference Optimization Beyond Chatbots]]
- [[Direct Preference Optimization]]
- [[Reward Design for RL]]
- [[Search-Augmented Language Models]]
- [[Efficient Reasoning on the Edge]]
- [[On-Device Reasoning]]
- [[Reasoning Compression]]
