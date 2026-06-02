---
type: source-summary
created: 2026-06-02
updated: 2026-06-02
source_id: src-2026-06-02-dwarkesh-eric-jang-alphago
source_title: Eric Jang - Building AlphaGo from scratch
source_author: Dwarkesh Patel
source_url: https://www.dwarkesh.com/p/eric-jang
tags:
  - source/summary
  - interview
  - alphago
  - mcts
  - research-automation
source_ids:
  - src-2026-06-02-dwarkesh-eric-jang-alphago
status: active
---

# Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch

## Summary

This interview uses AlphaGo as a clean worked example of intelligence primitives: search, learning from experience, and self-play. Eric Jang uses the AlphaGo reconstruction not just to explain classical game AI, but to illuminate why dense search-derived supervision can outperform sparse policy-gradient credit assignment and what that implies for RL in LLMs. The later part of the conversation extends that lens to automated AI research, arguing that LLMs are already useful for executing experiments and tuning hyperparameters even when they still struggle with choosing the best next question.

## Key claims

- AlphaGo remains a particularly crisp example of how search, learning, and self-play compose into a strong system.
- MCTS plus network distillation produces dense per-state training targets, which can sidestep part of the credit-assignment problem that plagues naive policy-gradient RL.
- The policy head prunes breadth while the value head prunes depth, which is why AlphaGo's network is useful even before the full search is complete.
- MCTS does not transfer cleanly to current LLM reasoning because language/action branching is effectively unbounded and partial-trajectory value estimation is much harder than board-state evaluation.
- Autoresearch loops are promising but uneven: LLMs can already help with experiment implementation, execution, and hyperparameter optimization more reliably than they can choose the next question or escape conceptual dead ends.

## Why it matters

This source connects several branches of the vault at once. It strengthens the RL branch with a concrete, mechanistic example of dense improvement targets through search. It also strengthens the agents branch by grounding a realistic view of automated research loops rather than treating them as pure speculation.

## Tensions / open questions

- How much of AlphaGo's advantage comes from bounded action spaces and well-shaped environments rather than from search itself?
- Can LLM systems recover AlphaGo-like dense supervision without literal MCTS over token sequences?
- How far can research automation go before the bottleneck becomes question selection, not experiment execution?

## Affected pages

- [[Monte Carlo Tree Search]]
- [[Reinforcement Learning]]
- [[Automated AI Research]]
- [[Agentic Loop]]
- [[Eric Jang]]

## Citations

- Raw capture note: [[2026-06-02 Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
- Readable transcript: [transcript markdown](../../raw/assets/2026-06-02%20Dwarkesh%20Patel%20-%20Eric%20Jang%20-%20Building%20AlphaGo%20from%20scratch%20transcript.md)

## Related pages

- [[Monte Carlo Tree Search]]
- [[Reinforcement Learning]]
- [[Automated AI Research]]
- [[Agentic Loop]]
- [[Eric Jang]]
- [[Dwarkesh Patel - Eric Jang Flashcards]]
