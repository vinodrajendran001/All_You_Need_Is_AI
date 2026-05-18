---
type: source-summary
created: 2026-05-18
updated: 2026-05-18
tags:
  - source
  - reasoning
  - architecture
  - recursion
source_id: src-2026-05-18-alphasignal-return-of-recursion
source_title: "The return of recursion - How AI is rethinking complex reasoning"
source_author: Alpha Signal
source_url: ""
status: active
---

# Alpha Signal - The Return of Recursion

## Summary

This Alpha Signal newsletter argues that complex reasoning is exposing a core limit of standard autoregressive LLMs: a fixed-depth Transformer eventually runs out of computation steps on tasks that cannot be solved in one pass. Chain-of-thought partly compensates by moving reasoning into token generation, but this workaround is slow, memory-hungry, and inefficient because the model must externalize intermediate steps as text. The article presents recursive architectures as an alternative: instead of “thinking” in tokens, they iterate over compact latent states, increasing effective reasoning depth without scaling parameter count in the usual way.

The main example is the **Hierarchical Reasoning Model (HRM)**, which uses a slow high-level planning module and a fast low-level computation module that recurse together. According to the article, a 27M-parameter HRM achieved state-of-the-art ARC-AGI performance with only 1,000 training examples and can deliver up to 100× speedups over token-generating reasoning models on deterministic tasks. The newsletter then highlights Samsung's Tiny Recursive Model as an even more stripped-down design: a single weight-sharing two-layer network with recursive depth instead of hierarchical modules. TRM reportedly beats HRM and frontier LLM baselines on Sudoku-Extreme, ARC-AGI-1, and maze navigation, suggesting that recursive looping and weight sharing matter more than architectural complexity.

The article frames these systems as specialized reasoning engines rather than general-purpose LLM replacements. HRM and TRM are well-suited to deterministic, latency-sensitive, or data-scarce tasks, while language-heavy work still favors LLMs. It extends the same idea to multi-agent systems through RecursiveMAS, where agents exchange latent representations instead of text tokens. That design reportedly reduces token usage, speeds inference, and improves accuracy. The durable thesis is that latent-space recursion offers a scalable, lower-cost path for reasoning systems, especially when paired with LLMs rather than used in isolation.

## Key Claims

- Standard autoregressive LLMs have a fixed computation depth per forward pass, which limits performance on tasks that need more reasoning steps than the architecture natively provides.
- Chain-of-thought improves reasoning by externalizing intermediate steps as tokens, but token-space reasoning is slow and memory-intensive.
- Recursive models revisit ideas from recurrent architectures by iterating over internal state rather than expanding token output.
- The article presents HRM as a dual-module latent reasoning system with a slow planner (H-module) and fast solver (L-module).
- HRM is reported to achieve state-of-the-art ARC-AGI results with 27M parameters and only 1,000 training examples, while delivering up to 100× faster reasoning on deterministic tasks.
- Samsung's TRM reduces the design to a single weight-sharing two-layer recursive network with roughly 5–7M parameters.
- TRM is reported to outperform HRM and larger frontier models on Sudoku-Extreme (87.4%), ARC-AGI-1 (45%), and maze navigation (85%).
- Weight sharing plus more recursive steps can be a stronger path to generalization than simply stacking more layers.
- Recursive models are positioned as complements to LLMs: strong on structured reasoning, weak on open-ended language tasks.
- RecursiveMAS extends latent-space recursion to multi-agent systems, reporting 2.4× speedup, 75.6% token reduction, and 8.3% average accuracy gains.

## Affected Pages

- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[Alpha Signal]]
- [[AI Knowledge Base Overview]]
- [[knowledge-base/wiki/index|Knowledge Base Index]]
- [[knowledge-base/wiki/log|Knowledge Base Log]]

## Related pages

- [[Latent-Space Reasoning]]
- [[Recursive Architectures]]
- [[Reinforcement Learning]]
- [[Agentic Loop]]
- [[Alpha Signal]]
- [[AI Knowledge Base Overview]]
