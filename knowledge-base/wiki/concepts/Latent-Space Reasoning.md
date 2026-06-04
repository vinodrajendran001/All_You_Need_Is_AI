---
type: concept
created: 2026-05-18
updated: 2026-06-04
tags:
  - concept
  - reasoning
  - architecture
source_ids:
  - src-2026-05-18-alphasignal-return-of-recursion
  - src-2026-06-04-progressive-thought-encoding
  - src-2026-06-04-reasoncache
status: active
---

# Latent-Space Reasoning

## Definition

Latent-space reasoning is the use of continuous internal representations for intermediate computation instead of generating explicit natural-language tokens for every reasoning step. Rather than “thinking out loud” in text, a model iterates over compressed hidden states and produces language only when it needs to expose a final answer.

## Why it matters

Reasoning in latent space can be faster, cheaper, and more compact than token-space reasoning because the model avoids repeatedly decoding long intermediate chains of text. That reduces token costs, lowers memory pressure, and lets the system spend compute on recursive internal updates instead of serial text generation. It is especially attractive for deterministic tasks where the main bottleneck is structured computation rather than broad world knowledge.

## Token-space contrast

In a standard [[Agentic Loop]] or chain-of-thought workflow, the model often externalizes intermediate reasoning as text tokens, then rereads those tokens to continue. That can improve performance, but it is slow and inefficient because every extra reasoning step expands the visible sequence. Latent-space reasoning keeps those intermediate steps compressed inside the model's state, trading inspectability for speed and compute efficiency.

## Representative implementations

- **HRM** uses coupled recurrent modules so a high-level planner can guide a fast low-level solver in latent space.
- **TRM** simplifies the idea to a tiny weight-sharing recursive network, suggesting that the recursive loop itself is the key ingredient.
- **RecursiveMAS** applies the same principle to multi-agent systems, with agents exchanging latent representations instead of text messages until final output time.

## Training implications

Making latent recursive systems work well still depends on training, optimization, and evaluation choices that overlap with [[Reinforcement Learning]] and related post-training methods. Even when these models are not trained with RL directly, the broader problem is similar: how to allocate computation over multiple steps, assign credit across reasoning trajectories, and optimize for accuracy under latency and cost constraints.

## Compression-oriented bridges

The newer efficient-reasoning batch adds two adjacent examples that are not full recursive latent reasoners but still push in the same direction:

- [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]] progressively compresses intermediate reasoning into fixed-size vectors so RL training and inference can run under bounded cache budgets.
- [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]] distills demonstrations into a reusable key-value cache, letting the model learn reasoning skills without storing every step as long visible text or modifying the base weights in the usual way.

These methods reinforce the same general lesson: useful reasoning state does not always need to survive as a long explicit token trace.

## Related pages

- [[Recursive Architectures]]
- [[Agentic Loop]]
- [[Reinforcement Learning]]
- [[Reasoning Compression]]
- [[On-Device Reasoning]]
- [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]]
- [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]]
- [[Alpha Signal - The Return of Recursion]]
