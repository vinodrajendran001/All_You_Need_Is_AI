---
type: source-summary
created: 2026-10-16
updated: 2026-10-16
source_id: src-2026-10-12-bytebytego-energy-based-reasoning
source_title: "How to Build Models Without Language, with Logical Intelligence"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-to-build-models-without-language
tags: [source/summary, energy-based-models, reasoning, verification]
source_ids: [src-2026-10-12-bytebytego-energy-based-reasoning]
status: active
---

# ByteByteGo - How to Build Models Without Language

## Summary

A ByteByteGo interview/explainer with Logical Intelligence founder Eve Bodnia, using the
company's Kona Sudoku demonstration to motivate energy-based reasoning. An energy network
scores candidate answers or latent states; inference searches for low-energy candidates,
and a separate checker can verify task constraints.

The article explicitly says its technical walkthrough is **not a disclosure of Kona's
implementation**. Treat the benchmark as a vendor demonstration reported secondhand and the
energy-landscape discussion as an illustrative model, not a reproduced training recipe.
The unrelated CI sponsorship is not evidence for this ingest.

## Key claims

- An energy function `E(x, y)` scores compatibility between a problem and candidate answer.
  The tutorial illustrates contrastive training that lowers correct-answer energy relative
  to incorrect examples, followed by inference-time optimization of continuous candidates
  while model weights remain fixed.
- For discrete outputs, continuous representations can be optimized and then decoded.
  A latent reasoning variant optimizes intermediate states before reading out the result.
  The actual relaxation, losses, optimizer, and stopping rules are implementation choices.
- Logical Intelligence reportedly trained Kona on partially hidden Sudoku solutions, with
  **half of each grid hidden and no reinforcement learning**. This is a claim about Kona's
  training, not a requirement or prohibition for the entire model family.
- The company's demonstration reportedly achieved **96.2% solved puzzles** for Kona versus
  **2% across the LLM panel**, with the best LLM at **6.9%**. The cited models include
  GPT-5.2, Claude Opus/Sonnet 4.5, Gemini 3 Pro, and DeepSeek V3.2.
- The reported **$4 in Kona GPU time** and about **$11,000 in LLM API calls** use different
  accounting boundaries. Likewise, **313 ms average Kona time** and **up to 90 seconds** for
  an LLM compare a mean with a maximum. Neither licenses a general price or speed multiplier.
- The proposed division of labor gives constrained search to a specialist and uses a
  language model to interpret requests and express results.
- The final check matters independently of the learned energy. A Sudoku rule checker or,
  for formal proofs, Lean 4 can reject an invalid candidate. Repeated search still requires
  a practical budget and failure/escalation path.

## Why it matters

[[Energy-Based Model]] separates **learning a compatibility function**, **searching with it**,
and **checking the selected result**. This adds a different form of [[Latent-Space Reasoning]]
and [[Test-Time Scaling]], rather than simply renaming a language model with a shorter answer.

It also sharpens a recurring vault distinction: an output's formal validity is not proof
that the problem specification captures the user's intent.

## Tensions / open questions

- The prose initially equates lowest energy with the correct answer and later explicitly
  says energy is only an approximation. The latter qualification governs this summary:
  local convergence, continuity, or decreasing energy does not guarantee a global optimum
  or a valid answer after decoding.
- Negative-example contrastive training is the illustrated recipe, not the only possible
  anti-collapse strategy. [[Joint-Embedding Predictive Architecture]] provides a separate
  noncontrastive representation-learning example; it does not disclose Kona's internals.
- Saying the energy network "does not generate" describes its scoring role. A system using
  it can produce outputs by search or sampling; energy-based modeling is not categorically
  non-generative.
- The article's broad claims that language models cannot revise, extrapolate, or verify are
  too strong. Search, tools, formal checkers, and alternative output interfaces can surround
  an autoregressive model. The Sudoku result does not establish a universal reasoning limit.
- Exact checking only certifies the encoded constraints under the checker's assumptions.
  It does not certify user intent, practical safety, successful search termination, or a
  company's broader deployment claims.
- Training data, solver baselines, hardware, full harness details, and independent replication
  are missing from this capture. Proposed cross-domain and hardware/business shifts remain
  Bodnia's outlook, not measured generalization.

## Affected pages

- [[Energy-Based Model]]
- [[Latent-Space Reasoning]]
- [[LLM Reasoning]]
- [[Test-Time Scaling]]
- [[Joint-Embedding Predictive Architecture]]
- [[Logical Intelligence]]
- [[ByteByteGo]]

## Raw capture

- [[How to Build Models Without Language, with Logical Intelligence]]

## Citations

- Canonical article: <https://blog.bytebytego.com/p/how-to-build-models-without-language>
- Published October 12; captured October 13, 2026.
- Linked vendor demonstration, not independently reviewed:
  <https://logicalintelligence.com/blog/energy-based-model-sudoku-demo>.
- The source also links LeCun's energy-based learning tutorial and Lean documentation; these
  are references in the article, not additional independently ingested sources.

## Related pages

- [[Energy-Based Model]]
- [[Logical Intelligence]]
- [[Latent-Space Reasoning]]
- [[Test-Time Scaling]]
- [[Joint-Embedding Predictive Architecture]]
- [[LLM Reasoning]]
