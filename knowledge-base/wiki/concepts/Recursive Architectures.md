---
type: concept
created: 2026-05-18
updated: 2026-06-29
tags:
  - concept
  - architecture
  - reasoning
  - recursion
source_ids:
  - src-2026-05-18-alphasignal-return-of-recursion
  - src-2026-06-18-alyona-vert-recursive-self-improvement
  - src-2026-06-29-siddhant-rai-nested-learning
status: active
---

# Recursive Architectures

## Definition

Recursive architectures increase effective reasoning depth by repeatedly applying the same computational block or tightly coupled blocks over internal state, instead of relying only on a fixed stack of layers. In modern AI discussions, this usually means latent-space iterative computation rather than explicit token-by-token reasoning.

## Lineage

These models revive an older idea from recurrent neural networks and LSTMs: reuse parameters across time while updating a hidden state. Earlier recurrent systems struggled to train because unrolled loops made optimization unstable, but the core intuition remained powerful: if a model can revisit the same internal state multiple times, it can trade extra computation steps for stronger reasoning without needing a much larger network.

## Modern examples

### Hierarchical Reasoning Model (HRM)

HRM uses two coupled recursive modules: a slow high-level module for abstract planning and a fast low-level module for local computation. The L-module iterates on subproblems, then hands a stabilized result to the H-module, which updates the overall plan before sending back a refined objective. The reported result is a 27M-parameter system that reaches state-of-the-art ARC-AGI performance with only 1,000 training examples and up to 100× speedup over token-generating reasoning models on deterministic tasks.

### Tiny Recursive Model (TRM)

TRM strips HRM down to a single two-layer network with shared weights and full recursive looping. The key claim is that recursive depth matters more than hierarchical complexity. In the article's cited benchmarks, TRM outperforms HRM and larger frontier models with 87.4% on Sudoku-Extreme, 45% on ARC-AGI-1, and 85% on difficult maze navigation, despite using only about 5–7M parameters.

### RecursiveMAS

RecursiveMAS extends recursion beyond a single model into multi-agent coordination. Instead of exchanging text tokens at every step, agents pass latent representations to each other and only decode text at the end. The article reports up to 2.4× end-to-end speedup, 75.6% token reduction by the third recursion round, and 8.3% average accuracy improvement across code-generation and medical-reasoning tasks.

## Why recursive depth can beat layer stacking

Weight sharing lets a small model reuse the same learned transformation many times, so extra computation comes from more recursive steps rather than more parameters. For reasoning-heavy tasks, that can be more sample-efficient and computationally efficient than simply adding layers, especially when the problem benefits from iterative refinement. In effect, recursion turns time or loop depth into an additional reasoning resource.

## Relation to the broader vault

Recursive architectures matter here because they offer a different answer to the reasoning problem than token-heavy prompting or tool-driven loops. They do not replace general-purpose LLMs, but they suggest a complementary design space for specialized reasoning engines and agent systems. Their training and optimization questions also connect naturally to [[Reinforcement Learning]], especially when systems must learn how much computation to spend and how to improve multi-step behavior.

## Test-time updates as a recursive idea

[[Siddhant Rai - Nested Learning]] adds an adjacent variant of "reuse computation over evolving state": instead of looping the same block to deepen reasoning, the **Hope** architecture lets a bounded module update its own parameters during inference. The Titans lineage it builds on also revives the RNN-style "update a hidden state over time" intuition that this page traces — but here the state being updated is the *weights themselves*, via a learned update rule (self-modifying layers), not just an activation. The two ideas differ in what recurs (a fixed transformation over latent state vs a self-modified parameter state), but both trade extra inference-time computation for stronger adaptation. See [[Nested Learning]].

## Not recursive self-improvement

[[Alyona Vert - AI 101 - What is Recursive Self-Improvement]] makes a useful terminology distinction. Recursive architectures reuse computation over internal state to get more reasoning depth from a model. [[Recursive Self-Improvement]] is a broader research-loop idea where AI systems improve the process that creates future AI systems. The two ideas can interact, but they are not the same mechanism.

## Related pages

- [[Latent-Space Reasoning]]
- [[Reinforcement Learning]]
- [[Nested Learning]]
- [[Alpha Signal - The Return of Recursion]]
- [[Recursive Self-Improvement]]
- [[Alyona Vert - AI 101 - What is Recursive Self-Improvement]]
- [[Siddhant Rai - Nested Learning]]
- [[Agentic Loop]]
