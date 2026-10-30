---
type: source-summary
created: 2026-10-30
updated: 2026-10-30
source_id: src-2026-10-27-behrouz-mirrokni-sleep-framework
source_title: "The sleep framework: A new way for LLMs to retain knowledge in continual learning"
source_author: Ali Behrouz and Vahab Mirrokni
source_url: https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning/
tags:
  - source/summary
  - continual-learning
  - memory
  - distillation
source_ids:
  - src-2026-10-27-behrouz-mirrokni-sleep-framework
status: active
---

# The Sleep Framework

## Summary

Google Research presents scheduled wake, sleep, and dreaming phases for continual learning.
Fast memory acquires information while awake; sleep pauses new inputs and consolidates that
information into slower parametric memory. The framework extends the Hope/continuum-memory
line rather than replacing external memory files with another name. Its architecture and
training rules remain human defined.

## Key claims

- **Wake and sleep have different update jobs.** Wake uses fast short-term memory. Sleep
  transfers information into slower parameters with on-policy generalized distillation and a
  learning-to-imitate reward, using semantic and Levenshtein similarity signals.
- **Capacity grows within a predetermined design.** The system unlocks preallocated low-rank
  mixture-of-experts memory blocks. This is not autonomous invention of a new architecture.
  Temporary high-frequency parameters are reset after consolidation.
- **Dreaming creates a further training loop.** Random expert activation generates synthetic
  samples, gradient-based selection chooses samples, and subsequent fine-tuning/refinement
  uses them. Self-generated material is not automatically independent supervision.
- **Reported retention is task-specific.** The post describes near-zero forgetting on
  sequential unseen-language translation involving Manchu and Kalamang, and near-perfect
  BABILong scaling to **10 million tokens through parametric consolidation**, not a native
  ten-million-token attention window or guaranteed verbatim storage.
- **Other figures remain separate experiments.** Reported factual incorporation is **48.9%**
  in the single-task setting and **46.2%** in continual pretraining. Reported AIME 2024,
  AIME 2025, and HMMT 2025 scores are **79.2%, 69.0%, and 46.1%**, respectively; the blog
  does not supply enough surrounding experimental detail to rank these as general capability.

## Why it matters

[[Nested Learning]] gains a concrete schedule for moving information between update frequencies.
[[Agent Memory]] and [[Continual Learning for Agents]] need to distinguish three operations:
writing explicit records, consolidating representations through training, and expanding usable
capacity inside an existing architecture. [[Knowledge Distillation]] supplies the transfer
mechanism, while [[Synthetic Data Flywheel]] supplies the risk that internally generated samples
can repeat errors. [[Recursive Self-Improvement]] should classify this by what changes, not by
the biological metaphor.

## Tensions / open questions

- This is a first-party research blog; the linked paper is not separately captured or read in
  this ingest. Base-model, compute-budget, full-table, and independent-replication detail is
  insufficient for broad comparison.
- The concluding language about avoiding catastrophic forgetting is stronger than the bounded
  translation and long-context evidence. Retention outside those tasks remains open.
- Sleep requires pausing new inputs and spending consolidation compute. The post does not
  establish a production latency/cost budget or unlimited expansion of preallocated capacity.
- Parameter consolidation is neither a lossless archive nor the same operation as offline
  Markdown-memory maintenance. A large processed stream does not become an equally large
  simultaneously addressable attention context.

## Affected pages

- [[Nested Learning]]
- [[Continual Learning for Agents]]
- [[Agent Memory]]
- [[Knowledge Distillation]]
- [[Synthetic Data Flywheel]]
- [[Recursive Self-Improvement]]

## Raw capture

- [[knowledge-base/raw/sources/The sleep framework A new way for LLMs to retain knowledge in continual learning]]

## Citations

- Canonical URL: <https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning/>
- Byline: Ali Behrouz and Vahab Mirrokni, Google Research. Published October 27, 2026;
  captured October 29, 2026.
- The research acknowledgments also name Farnoosh Hashemi and Adel Javanmard; that is not
  the blog's byline. Linked paper: <https://arxiv.org/abs/2606.03979> (not separately ingested).

## Related pages

- [[Nested Learning]]
- [[Continual Learning for Agents]]
- [[Agent Memory]]
- [[Knowledge Distillation]]
- [[Synthetic Data Flywheel]]
- [[Recursive Self-Improvement]]
- [[Mixture of Experts]]
- [[Leon Sick et al - On-Policy Self-Training]]
- [[Divyansh Agrawal - Qwenputer - A Deterministic RISC-V CPU Inside Qwen3.5]]
