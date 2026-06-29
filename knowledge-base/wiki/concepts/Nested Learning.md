---
type: concept
created: 2026-06-29
updated: 2026-06-29
tags:
  - concept
  - nested-learning
  - inference-time-learning
  - continual-learning
  - memory
  - architecture
source_ids:
  - src-2026-06-29-siddhant-rai-nested-learning
status: active
---

# Nested Learning

## Definition

Nested Learning is a framework (Google, arXiv 2512.24695) for **continuous inference-time learning**: instead of treating training and inference as separate phases, a bounded part of the model keeps updating its own parameters as it processes a stream of new information. Its reference instantiation, **Hope**, combines a self-modifying sequence model with a Continuum Memory System. It generalizes the earlier Titans architecture from a single test-time update toward genuine continual learning.

## Why it matters

This page captures a distinct answer to the memory problem from the rest of the vault. [[Retrieval-Augmented Generation]] adds knowledge by *retrieving into context*; [[Agent Memory]] adds it by *storing facts externally*. Nested Learning instead folds adaptation *into the model's own computation*, making memory a learnable structure rather than external storage. It is also a concrete example of the test-time-update idea that [[Recursive Architectures]] gestures at.

## The learning spectrum

[[Siddhant Rai - Nested Learning]] frames adaptation along one axis — how much the model may change in response to new information — with three regimes between fully frozen and fully dynamic:

1. **In-context learning** — weights never change; the model conditions on examples in the context window, using attention as ephemeral memory. Powerful but bounded by sequence length and erased when context clears. "Adaptation without memory."
2. **Continual learning** — the model accumulates knowledge across a stream of tasks over time. Its core failure mode is **catastrophic forgetting**: gradient updates that help a new task overwrite the weights that encoded old ones.
3. **Inference-time learning** — the forward pass becomes a write operation; designated parameters update *during* inference. This needs a bounded updatable module plus a cheap update rule (not full backprop).

Hope lives at the inference-time end but pushes toward true continual learning.

## The central obstacle: plasticity vs stability

The **plasticity-stability tradeoff** is the unsolved tension underneath continual learning. Update too readily and the model is plastic but unstable (learns fast, forgets fast); update too conservatively and it is stable but rigid (retains old knowledge, resists new). The two requirements pull in opposite directions and there is no free solution.

## Why RAG isn't enough (in this frame)

RAG appears to solve memory without touching the model, but the source argues it treats **memory as storage** (retrieve documents into context) rather than **memory as structure** (knowledge integrated into the model's computation). It inherits the context-window ceiling of in-context learning and never changes what the model *is*. This is the gap Nested Learning targets — see [[Retrieval-Augmented Generation]].

## Architecture

### Titans (the predecessor)

Titans showed the train/inference boundary is not fixed: a small MLP **neural memory module** can be updated at test time via a self-supervised objective. Its three memories are short-term attention, a long-term updatable state, and a persistent fixed memory. Limitation: it handles a single test-time update, not a continuous stream.

### Continuum Memory System (CMS)

CMS organizes memory as a **chain of modules updated at different frequencies**: fast levels hold volatile, recent detail; slow levels hold stable, consolidated knowledge. This frequency hierarchy is how Hope decides what to remember vs overwrite — a structural answer to plasticity-stability.

### Self-Modifying Titans and Hope

**Self-Modifying Titans** learn their own update rule (meta-learning the write mechanism) instead of using a fixed one. This differs from fine-tuning because updates are local, bounded, and happen at inference. **Hope** = self-modifying sequence model + CMS, trained with a **two-loop structure** (inner-loop parameter updates, outer-loop objective), with inference-time gradients approximated by chunked, amortized updates to keep cost tractable.

## Open questions

- Inference-time weight updates reintroduce stability/safety risk; is continuous self-modification robust enough for production?
- The inner-loop update has real cost at inference; what is the right fidelity/speed operating point for chunked approximations?
- These claims come from one recent paper's own evaluation; independent replication and benchmarking are still missing.

## Related pages

- [[Siddhant Rai - Nested Learning]]
- [[Agent Memory]]
- [[Retrieval-Augmented Generation]]
- [[Recursive Architectures]]
- [[On-Device Reasoning]]
- [[Transformer Architecture]]
- [[Latent-Space Reasoning]]
- [[AI Knowledge Base Overview]]
