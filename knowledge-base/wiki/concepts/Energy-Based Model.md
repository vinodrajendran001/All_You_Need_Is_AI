---
type: concept
created: 2026-10-16
updated: 2026-10-19
tags: [concept, energy-based-models, reasoning, verification]
source_ids:
  - src-2026-09-07-rai-lejepa
  - src-2026-10-12-bytebytego-energy-based-reasoning
  - src-2026-10-19-alphasignal-next-concept-modeling
status: active
---

# Energy-Based Model

## Definition

An energy-based model learns a scalar compatibility function, often written `E(x, y)`, over
an input and a candidate output or latent state. Lower energy is intended to identify more
compatible configurations. Producing an answer requires an additional search, optimization,
or sampling procedure; the score is not itself a proof of correctness.

## Why it matters

This separates three jobs often compressed into "the model reasons": learning a useful
landscape, finding a candidate in it, and checking the result. It gives [[Latent-Space Reasoning]]
and [[Test-Time Scaling]] an inference mechanism other than extending a visible token trace.
A scoring network can therefore be part of a generative system without itself emitting
tokens autoregressively.

## Current synthesis

### Search and checking have different contracts

[[ByteByteGo - How to Build Models Without Language]] illustrates optimizing continuous
candidate representations with fixed model weights, then decoding and checking the result.
The search can converge to a local minimum, exploit errors in the learned score, or produce
an invalid discrete result. Decreasing energy is progress under a learned objective, not a
certificate that the task is solved.

A Sudoku checker or formal proof checker supplies a separate validity test. That test only
certifies its encoded constraints under its own assumptions; it does not establish that the
specification captures the user's intent. Search still needs a budget and an explicit
failure or escalation outcome.

### Contrastive negatives are a recipe, not the definition

ByteByteGo teaches a contrastive example that lowers correct-answer energy relative to
incorrect candidates. [[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]]
provides a complementary representation-learning case: predictive matching is paired with
noncontrastive anti-collapse regularization.

The shared question is how to prevent an uninformative learned solution, not whether every
useful objective must enumerate wrong answers. LeJEPA concerns vision representations and
has its own assumptions about downstream tasks and isotropy. It is neither Kona's disclosed
recipe nor evidence that the two systems solve the same problem.

### A vendor puzzle result does not establish general reasoning superiority

The ByteByteGo account reports [[Logical Intelligence]]'s Kona solving **96.2%** of the
demonstration's Sudoku puzzles versus **2%** across the LLM panel and **6.9%** for its best
LLM. The technical walkthrough explicitly does not describe Kona's implementation.

The **$4 GPU-time** and **$11,000 API-charge** figures have different accounting boundaries;
**313 ms mean** versus **up to 90 seconds** mixes a mean and a maximum. These do not support
general cost or speed ratios. Nor does the demonstration show that language models cannot
use search, tools, or formal checkers. A plausible division of labor is language for the
interface and a specialist for constrained search, with independent checks at the boundary.

### Sudoku is becoming a shared demonstration, not a shared benchmark

[[Alpha Signal - How Next-Concept Modeling Rethinks AI Text Generation]] reports a second
non-autoregressive approach tested on hard Sudoku. Stanford's Next-Concept Modeling generates a
coarse-to-fine hierarchy of discrete codes rather than optimizing an energy. It reportedly
"outperformed the strongest competing method while requiring fewer model evaluations." The
article treats whole-board constraint satisfaction as a natural test of coarse-to-fine
refinement.

The two Sudoku claims cannot be placed on one scale. NCM's result has no accuracy figure and no
named competitor. Kona's **96.2%** comes from a vendor demonstration against an LLM panel. The
protocols, puzzle sets, and checkers are undocumented in both captures.

What the pair does show is a family resemblance. Both are presented as alternatives to
committing to an answer left to right. NCM refines coarse codes for the whole sequence, and the
generic energy walkthrough optimizes a whole candidate (though that walkthrough is explicitly not
Kona's implementation). Neither result is evidence about language-model systems that use search,
tools, or formal checkers.

## Open questions

- Which optimization and stopping rules preserve useful performance under a fixed budget?
- What changes when constraints are incomplete, ambiguous, or expensive to check?
- How would Kona compare with strong task-specific solvers under matched hardware, data,
  accounting, and independent evaluation?

## Related pages

- [[ByteByteGo - How to Build Models Without Language]]
- [[Alpha Signal - How Next-Concept Modeling Rethinks AI Text Generation]]
- [[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]]
- [[Logical Intelligence]]
- [[Joint-Embedding Predictive Architecture]]
- [[Latent-Space Reasoning]]
- [[LLM Reasoning]]
- [[Test-Time Scaling]]
