---
type: source-summary
created: 2026-06-02
updated: 2026-06-02
source_id: src-2026-06-02-dwarkesh-eric-jang-flashcards
source_title: Eric Jang Flashcards
source_author: Dwarkesh Patel
source_url: https://flashcards.dwarkesh.com/eric-jang/
tags:
  - source/summary
  - flashcards
  - alphago
  - mcts
  - retention
source_ids:
  - src-2026-06-02-dwarkesh-eric-jang-flashcards
status: active
---

# Dwarkesh Patel - Eric Jang Flashcards

## Summary

These flashcards distill the Eric Jang interview into explicit retrieval cues about MCTS, PUCT, AlphaGo's policy/value network roles, self-play training labels, alternate RL baselines, and why MCTS fails to transfer directly to LLM reasoning. Compared with the long-form interview, the flashcards are stronger on formulas, distinctions, and compact explanations.

## Key claims

- A single MCTS simulation consists of selection, leaf evaluation, and value backup.
- PUCT works because the exploration bonus decays with repeated visits while the running value estimate becomes more informative.
- AlphaGo's policy head prunes breadth and its value head prunes depth.
- AlphaZero's training targets are the MCTS visit distribution for the policy head and the terminal game outcome for the value head.
- Winner-imitation or sparse REINFORCE-style learning underuses the information available in self-play compared with MCTS distillation.
- MCTS struggles in LLMs because the search space has effectively unbounded breadth and partial-trajectory value modeling is weak.

## Why it matters

This is a high-signal retention companion to the interview. It makes the AlphaGo mechanics easier to re-derive later and provides compact statements that are useful when connecting classical game RL to LLM-era search and credit-assignment problems.

## Tensions / open questions

- Which parts of the AlphaGo training recipe are essential, and which are artifacts of Go's structure?
- Can flashcard-style structured retention become a standard ingest artifact for other complex technical interviews?

## Affected pages

- [[Monte Carlo Tree Search]]
- [[Reinforcement Learning]]
- [[Eric Jang]]

## Citations

- Raw capture note: [[2026-06-02 Dwarkesh Patel - Eric Jang Flashcards]]
- Readable flashcards: [markdown capture](../../raw/assets/2026-06-02%20Dwarkesh%20Patel%20-%20Eric%20Jang%20Flashcards.md)

## Related pages

- [[Monte Carlo Tree Search]]
- [[Reinforcement Learning]]
- [[Eric Jang]]
- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
