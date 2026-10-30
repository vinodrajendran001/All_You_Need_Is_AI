---
type: concept
created: 2026-06-29
updated: 2026-10-30
tags:
  - concept
  - nested-learning
  - inference-time-learning
  - continual-learning
  - memory
  - architecture
source_ids:
  - src-2026-06-29-siddhant-rai-nested-learning
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-10-27-behrouz-mirrokni-sleep-framework
status: active
---

# Nested Learning

## Definition

Nested Learning is a framework (Google, arXiv 2512.24695) for **continuous inference-time learning**: instead of treating training and inference as separate phases, a bounded part of the model keeps updating its own parameters as it processes a stream of new information. Its reference instantiation, **Hope**, combines a self-modifying sequence model with a Continuum Memory System. It generalizes the earlier Titans architecture from a single test-time update toward genuine continual learning.

## Why it matters

This page captures a distinct answer to the memory problem. [[Retrieval-Augmented Generation]]
adds knowledge by retrieving into context; the external-store designs in [[Agent Memory]]
retain explicit facts outside the model. Nested Learning instead folds adaptation into the
model's own computation, making memory a learnable structure. Agent Memory now also covers
these structural approaches; external storage is one design, not that page's entire scope.
Nested Learning is also a concrete example of the test-time-update idea that
[[Recursive Architectures]] gestures at.

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

## Why continual learning is a reasoning frontier

[[Akhil Arora et al - Current Advances in LLM Reasoning]] lists **continual learning** as one of the open pillars of reasoning, which gives this page's memory-as-structure agenda a concrete problem set with 2025–2026 evidence it is unsolved: **distribution drift** (Spurious Forgetting), **catastrophic forgetting** at post-training scale, **model collapse** from training on synthetic data, **"peak data"** (the field's biggest open question), and **reward hacking**. Nested Learning's inference-time, memory-as-structure approach is one proposed response to exactly these failures — a bridge from the vault's efficiency/memory branch into the broader [[LLM Reasoning]] map.

## Sleep schedules consolidation across the hierarchy rather than inventing the hierarchy

[[Ali Behrouz and Vahab Mirrokni - The Sleep Framework]] adds a concrete wake/sleep schedule.
Wake acquires information in fast memory; sleep pauses new input and uses on-policy generalized
distillation plus a learning-to-imitate reward to consolidate it into slower parameters.
Temporary high-frequency parameters are then reset. Low-rank mixture-of-experts memory blocks
are preallocated and progressively unlocked: capacity changes within a fixed design, not
through autonomous architecture invention.

Dreaming adds random expert activation, generated samples, gradient-based selection, and
refinement. The biological labels should not hide the specified update rules or the compute
spent between input-processing phases.

The Google Research blog reports near-zero forgetting on sequential unseen-language
translation and describes near-perfect BABILong scaling through **10 million tokens** of parametric
consolidation. That is not a native ten-million-token attention window or a lossless archive.
The linked paper was not separately read for this ingest, and the blog lacks the experimental
and compute detail needed to generalize its strong no-forgetting conclusion.

## Open questions

- Inference-time weight updates reintroduce stability/safety risk; is continuous self-modification robust enough for production?
- The inner-loop update has real cost at inference; what is the right fidelity/speed operating point for chunked approximations?
- The captured Hope and sleep accounts do not supply independent replication or matched
  production-cost comparisons; how much retention survives outside their evaluated settings?

## Related pages

- [[Ali Behrouz and Vahab Mirrokni - The Sleep Framework]]
- [[Continual Learning for Agents]]
- [[Knowledge Distillation]]
- [[Siddhant Rai - Nested Learning]]
- [[Agent Memory]]
- [[Retrieval-Augmented Generation]]
- [[Recursive Architectures]]
- [[On-Device Reasoning]]
- [[Transformer Architecture]]
- [[Latent-Space Reasoning]]
- [[LLM Reasoning]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[AI Knowledge Base Overview]]
