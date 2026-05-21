---
type: concept
created: 2026-05-21
updated: 2026-05-21
tags:
  - concept
  - algorithms
  - data-structures
  - interview-prep
source_ids:
  - src-2026-05-21-leetcode-templates
  - src-2026-05-18-hanfang-pytorch-practice
status: active
---

# Algorithm Templates for Interviews

The template-based approach to interview preparation treats coding problems as **recognition tasks before they become implementation tasks**. Instead of deriving every solution from first principles under time pressure, the candidate learns to classify the prompt, select the right reusable pattern, and then customize the pattern's invariants, state, and stopping conditions.

## Core workflow

A durable interview loop emerges across both DSA and ML-engineering coding rounds:

1. **Recognize the signal** — contiguous range, sorted input, monotonic predicate, graph traversal, reversible search, overlapping subproblems, top-`k`, or stateful design prompt.
2. **Select the template** — sliding window, two pointers, binary search, BFS/DFS, backtracking, DP, heap, trie, Union-Find, and so on.
3. **Customize the moving parts** — validity condition, update rule, recurrence, comparator, node state, or class API.
4. **State complexity clearly** — good interview performance depends not just on passing code, but on explaining why the chosen template has the right time/space profile.

[[Universal LeetCode Templates]] makes this workflow explicit for algorithmic coding rounds, while [[Han Fang - PyTorch Practice]] applies a similar pattern in ML-oriented rounds by turning common PyTorch interview tasks into repeatable implementation drills.

## How the 20 categories map to common interview problem types

- **Sliding Window** — contiguous subarray and substring optimization problems.
- **Two Pointers** — sorted-array pairing, palindrome checks, and in-place compaction or partitioning.
- **Binary Search** — exact lookup, boundary finding, and answer-space optimization with monotonic feasibility.
- **BFS** — shortest path in unweighted graphs, level-order traversal, and minimum-step state search.
- **DFS** — reachability, component counting, recursive tree logic, and exhaustive graph exploration.
- **Backtracking** — combinations, permutations, subsets, Sudoku-style constraints, and search with undo steps.
- **Dynamic Programming** — optimization/counting problems with repeated substructure and choice-dependent state.
- **Monotonic Stack** — next greater/smaller element, histogram area, and span/boundary problems.
- **Heap / Priority Queue** — top-`k`, merge-`k` lists, streaming maxima/minima, and scheduling.
- **Linked List** — pointer rewiring, reversal, cycle detection, and merge/split routines.
- **Trie** — prefix queries, autocomplete, dictionary membership, and character-by-character pruning.
- **Union-Find** — connectivity, component merging, redundant-edge detection, and equivalence classes.
- **Prefix Sum** — range aggregation and subarray counting with cumulative-state lookups.
- **Topological Sort** — dependency ordering, course-schedule style validation, and DAG cycle checks.
- **Greedy (Interval Problems)** — merge/erase/select interval tasks where a local ordering rule is sufficient.
- **Bit Manipulation** — parity, mask-based state compression, xor tricks, and constant-factor optimization.
- **Graph — Dijkstra's** — weighted shortest-path problems with non-negative edge costs.
- **Deque / Monotonic Deque** — sliding-window extrema and queue problems needing both ends.
- **Math Patterns** — number theory, digit manipulation, modular arithmetic, and closed-form shortcuts.
- **Design / Data Structure Problems** — cache, iterator, randomized set, and API-design questions that test state management over pure algorithmics.

## Why this matters for interviews

Algorithm interviews reward **fast pattern recognition under ambiguity**. The strongest candidates usually do three things well:

- infer the hidden structural signal in the prompt,
- pick a template whose invariant matches that signal, and
- explain the tradeoff between alternative templates before coding.

That is why template study is more than memorization. It is a way to internalize which invariants matter: window validity, pointer movement rules, BFS frontier levels, DP state definitions, monotonic stack ordering, or heap size constraints.

## DSA templates vs. ML interview implementations

The new LeetCode source and the existing Han Fang source cover **complementary halves of technical interview preparation**:

- [[Universal LeetCode Templates]] emphasizes abstract algorithm families, asymptotic complexity, and problem classification.
- [[Han Fang - PyTorch Practice]] emphasizes hands-on PyTorch mechanics such as autograd, normalization, attention, optimizers, and training loops.

For ML-engineering interviews, both matter. DSA rounds often test whether the candidate can quickly map a prompt to a canonical algorithmic skeleton; ML rounds often test whether the candidate can implement or explain model-training components inside a concrete framework. The two study modes reinforce each other because both reward reusable mental templates rather than ad hoc coding.

## Meta-strategies

- **Listen for trigger phrases** such as “contiguous,” “shortest path,” “at most `k`,” “minimum feasible,” “top `k`,” or “design a class.”
- **Name the invariant before writing code**: what must stay true about the window, stack, heap, graph frontier, or DP table?
- **Identify customization points** early: predicate, recurrence, merge rule, state update, or data-structure API.
- **Say the complexity out loud** before and after implementation; interviewers use this to judge whether the template choice was principled.
- **Practice paired coverage**: algorithm templates for general coding rounds, and framework-specific drills for ML rounds.

## Related pages

- [[Universal LeetCode Templates]]
- [[Han Fang - PyTorch Practice]]
- [[Neural Network Fundamentals]]
- [[AI Knowledge Base Overview]]
- [[index|Knowledge Base Index]]
