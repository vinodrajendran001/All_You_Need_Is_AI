---
type: concept
created: 2026-05-08
updated: 2026-06-02
tags:
  - concept
  - reinforcement-learning
  - sequential-decision-making
source_ids:
  - src-2026-05-08-murphy-reinforcement-learning-overview
  - src-2026-04-22-perplexity-search-augmented-lm
  - src-2026-05-18-pocketflow-tutorial-docs
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-02-dwarkesh-eric-jang-flashcards
status: active
---

# Reinforcement Learning

## Definition

Reinforcement learning is the part of AI concerned with sequential decision making, where an agent improves behavior through interaction, feedback, and optimization over time.

## Why it matters

RL is one of the major domains already represented in the broader vault, and this paper gives the knowledge base its first structured anchor for that domain.

## Current synthesis

- A useful top-level map of RL should span value-based, policy-based, and model-based approaches rather than treating any one of them as the whole field.
- The field also extends into multi-agent RL, offline RL, hierarchical RL, and intrinsic reward.
- LLM training now intersects directly with RL, which makes RL relevant to this vault's LLM focus rather than a separate side topic.
- Perplexity's search-agent pipeline demonstrates a concrete production use of RL for LLMs: [[Group Relative Policy Optimization|GRPO]] with gated reward aggregation, anchored efficiency penalties, and rubric-based rewards. See [[Search-Augmented Language Models]] and [[Reward Design for RL]].
- [[The Pocket - PocketFlow Tutorial Docs]] adds a much more tutorialized RL ladder to this vault: multi-armed bandits, finite MDPs, Monte Carlo methods, temporal-difference learning, policy gradients/PPO, and n-step bootstrapping.
- That collection also sharpens one of this page's open questions: the bridge between classic RL and RL-for-LLMs is not incidental. Policy-gradient methods for alignment sit naturally on top of the same foundations as bandits, value functions, Bellman-style reasoning, and model-free control.
- The Eric Jang sources add AlphaGo/AlphaZero as the clearest concrete example of an alternative RL regime: **search plus self-play** can turn a sparse terminal reward into dense per-state supervision by making the policy imitate the MCTS-improved move distribution at every state. See [[Monte Carlo Tree Search]].
- Those same sources sharpen the contrast with RL for LLMs: token-level policy gradients face a much uglier credit-assignment problem, and MCTS does not transfer cleanly because language has unbounded branching and weak partial-trajectory value models.
- This page should remain a hub page until narrower RL subtopic pages are added.

## Open questions

- Which RL branches deserve their own pages first as more sources are ingested?
- How should the vault distinguish classic RL background from modern RL-for-LLMs workflows?

## Related pages

- [[Kevin Murphy - Reinforcement Learning - An Overview]]
- [[The Pocket - PocketFlow Tutorial Docs]]
- [[Perplexity - Advancing Search-Augmented Language Models]]
- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
- [[Dwarkesh Patel - Eric Jang Flashcards]]
- [[Perplexity]]
- [[Eric Jang]]
- [[Monte Carlo Tree Search]]
- [[Search-Augmented Language Models]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[AI Knowledge Base Overview]]
- [[2026-05-08 Mathematical Foundations for Reinforcement Learning]]
