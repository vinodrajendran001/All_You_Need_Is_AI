---
type: concept
created: 2026-06-02
updated: 2026-06-02
tags:
  - concept
  - search
  - reinforcement-learning
  - planning
source_ids:
  - src-2026-06-02-dwarkesh-eric-jang-alphago
  - src-2026-06-02-dwarkesh-eric-jang-flashcards
status: active
---

# Monte Carlo Tree Search

## Definition

Monte Carlo Tree Search (MCTS) is a search-time planning procedure that incrementally grows a partial decision tree by repeatedly selecting promising nodes, expanding new leaves, evaluating them, and backing their value estimates up the tree.

## Why it matters

MCTS is one of the clearest bridges between classical search and modern learning-based AI. In AlphaGo and AlphaZero, it is not just a planner layered on top of a network; it is also the mechanism that generates better supervision targets for the policy.

## Current synthesis

- In AlphaGo-style systems, each simulation does three things: descend the tree by a selection rule such as PUCT, evaluate a newly expanded leaf with the neural network, and back the resulting value estimate up to the root.
- PUCT combines a running action-value estimate with a prior-weighted exploration bonus. Early in search, the bonus dominates because unvisited actions have tiny denominators; later, the learned search statistics dominate.
- The policy head and value head play different roles:
  - The **policy** prior prunes breadth by steering search away from obviously bad moves.
  - The **value** head prunes depth by letting the system stop rollouts at a leaf and still estimate downstream quality.
- The most durable learning insight from this source pair is that MCTS creates **dense per-state targets**. Instead of only learning from a terminal win/loss signal, the policy can imitate the improved MCTS visit distribution at every visited state.
- That dense supervision helps explain why naive winner-imitation or sparse policy-gradient learning can underperform: the useful signal is drowned out by many neutral or misleading moves.
- The same mechanism does not port cleanly to LLM reasoning today. The action space is effectively unbounded and partial-trajectory value estimation is much noisier than board-state evaluation in Go.

## Open questions

- Can LLM systems recover the benefits of MCTS-style dense supervision without literal tree search over token sequences?
- Which bounded-subproblem settings inside language or coding might still support useful search-style planners?

## Related pages

- [[Dwarkesh Patel - Eric Jang - Building AlphaGo from scratch]]
- [[Dwarkesh Patel - Eric Jang Flashcards]]
- [[Reinforcement Learning]]
- [[LLM Training Pipeline]]
- [[Automated AI Research]]
