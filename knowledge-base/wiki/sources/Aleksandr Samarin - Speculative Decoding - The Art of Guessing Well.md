---
type: source-summary
created: 2026-10-16
updated: 2026-10-16
source_id: src-2026-10-11-samarin-speculative-decoding
source_title: "Speculative Decoding: The Art of Guessing Well"
source_author: Aleksandr Samarin
source_url: https://astralord.github.io/posts/speculative-decoding-the-art-of-guessing-well/
tags: [source/summary, speculative-decoding, inference, distillation, kv-cache]
source_ids: [src-2026-10-11-samarin-speculative-decoding]
status: active
---

# Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well

## Summary

A derivation-led survey of drafters attached to a target model, connecting **verification rule,
draft architecture, cache ownership, training objective, and serving cost**. Samarin also discusses
LK losses from his own research. Most other empirical results are literature reports, not
experiments reproduced by this ingest.

The central distinction is that exact verification protects the target distribution, while
draft quality and cost decide speed. Neither high token accuracy nor a longer accepted prefix
alone establishes better wall-clock performance.

## Key claims

### Exactness and reproducibility are separate

For target distribution `p` and draft `q`, accept a proposed token with
`min(1, p(x)/q(x))`; on rejection sample from the normalized positive residual `(p-q)+`.
The one-position acceptance rate is

```
alpha = sum_x min(p(x), q(x)) = 1 - TV(p, q)
```

The accepted contribution plus residual reconstructs `p`. This preserves a **distribution**,
not necessarily the same sampled text under a fixed seed when the drafter changes.
Shared, position-consistent Gumbel noise can instead make verification exact matching against
the target's own sampled path; its coupling generally has a different acceptance rate.

Greedy matching is a distinct special case. "Typical acceptance" variants such as the discussed
Medusa-2 setting need not preserve the exact target distribution.

### Count committed tokens and actual work

With `K` guesses and a constant independent acceptance probability, the expected committed
tokens per round, including the correction/bonus token, are
`tau = (1-alpha^(K+1))/(1-alpha)`. Real drafts have position- and prefix-dependent survival;
the familiar geometric approximation is not a universal measured acceptance curve.

The illustrative example `alpha=0.8`, `K=5`, relative draft cost `c=0.05` gives `tau ~= 3.69`,
about **2.95x** for five serial draft passes and **3.51x** for one parallel pass, assuming
verification costs one ordinary target step. These are model calculations, not benchmarks.

With batch `B`, a draft tree of `N` nodes, and target-pass cost `T`, the wider accounting is
`tau(N) * T(B) / (T(B*(N+1)) + T_draft)`. Target attention, memory traffic, kernels,
scheduling, and cache compaction can invalidate the cheap-verification assumption.

### Architecture decides how proposals depend on one another

| Family | Mechanism and tradeoff |
| --- | --- |
| EAGLE / EAGLE-3 / MTP | Target-conditioned, sequential drafting; EAGLE-3 fuses multiple target layers and drops EAGLE's feature-regression objective |
| Medusa / P-EAGLE / DFlash | Parallel proposals reduce serial draft passes, but independent output marginals can combine incompatible continuations |
| DSpark / Domino | Parallel backbone plus a light causal head restores dependence on earlier sampled draft tokens |
| DFlash2 / editing approaches | Candidate selection, local mixing, or extra refinement passes improve coherence with their own compute costs |
| Cross-round methods | Accumulate drafts or reuse rejected states as proposal context; rejected tokens are not thereby committed to the target history |

DFlash is described as a **single-step masked block predictor at inference**, despite its
block-diffusion training terminology. D-Loop's two-pass block refinement and DLoop's
cross-block drafting are different cited methods, not interchangeable spellings.

Tree verification needs ancestor-only attention and depth-based positions. Block verification
uses a joint prefix rule rather than ordinary tokenwise stopping; any claimed optimality is
within that rule's stated proposal and lossless-verification setting, not a serving optimum.

### Memory and scheduling can change the winner

A five-layer, eight-KV-head, 128-dimensional, BF16 DFlash-style cache at **32,768 tokens**
uses **671,088,640 bytes per request**: about **0.67 GB**, or **86 GB at 128 requests**.
This is cache arithmetic, excluding target weights/cache and other allocations.

H-Spec instead combines a summary initialized from target hidden states with direct reads of
selected target KV layers through a window. Its block state is rebuilt each round; it has
no context-growing private cache, not zero parameters or zero working memory.

The survey also cites long-context, cache-bound cases where speculation remains beneficial
at large batch sizes. Conversely, its cited Qwen3-8B/MATH500 AMD-vLLM example puts EAGLE-3
below ordinary decoding for all tested draft lengths, at **0.44-0.88x**. "Always disable
at high batch" and "always speed up" are both too strong.

For Qwen3-4B/GSM8K, a cited comparison gives both EAGLE-3 and DFlash `tau=4.2`, but
**2.1x versus 3.3x** speedups. DSpark's reported production comparisons separately fix
aggregate throughput or per-user generation speed; their improvements must not be added
or treated as one common configuration.

### Train for the verifier's objective

- For a capacity-limited drafter, minimizing KL need not maximize overlap `1-TV`.
  Small KL bounds TV but does not identify the best feasible drafter.
- Pure TV training can have weak gradients where the draft assigns little probability.
  LK losses use either an acceptance-dependent KL/TV blend or `-log(alpha)`.
- Per-position acceptance, per-round accepted length, and sequence-level verification rounds
  are different objectives. E2E-TV, block-verification-aware BV loss, and EDR address different
  versions of that distinction; a tokenwise surrogate is not automatically exact for every
  parallel drafter or verifier.
- Training must expose the drafter to the hidden states, proposed prefixes, rejected work,
  and round-start distribution it will encounter. Teacher-generated text alone does not
  necessarily cover these states.
- DSpark combines predicted conditional acceptance with the engine's profiled step rate
  to allocate draft lengths across a batch. This goes beyond batch-size-only switching.

## Why it matters

[[Speculative Decoding]] gains a sharper correctness contract and a richer optimization model.
[[Knowledge Distillation]] gains a concrete example where matching a teacher with a standard
loss is not identical to optimizing the downstream system objective.

## Tensions / open questions

- The introductory weight-bandwidth and H100 calculations are idealized ceilings that ignore
  cache reads and runtime overhead, not unconditional descriptions of every decode workload.
- The exactness statements assume a correct verifier, correct causal/cache bookkeeping, and
  the intended sampling transformations. They are not guarantees about implementation bugs,
  floating-point equivalence, or universal seed reproducibility.
- Benchmarks span different models, hardware, workloads, temperatures, and comparators.
  The survey's headline maxima and production-priority claims are not independently verified.
- Acceptance length sometimes counts only accepted draft tokens and sometimes includes the
  correction/bonus token in the literature; check the definition before combining numbers.
- The capture's SVG geometry is retained intact. Reading used the prose, equations, captions,
  and extracted SVG text labels, not measurements inferred from plotted curves.

## Affected pages

- [[Speculative Decoding]]
- [[KV Cache]]
- [[Knowledge Distillation]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[Inference Efficiency Frontier]]
- [[LLM Inference]]
- [[Linear Attention and Recurrent Memory]]

## Raw capture

- [[Speculative Decoding The Art of Guessing Well]]

## Citations

- Canonical tutorial: <https://astralord.github.io/posts/speculative-decoding-the-art-of-guessing-well/>
- Published October 11; captured October 13, 2026. This note describes the captured edition.
- The tutorial links the original verification, drafter, and training papers. Those links
  are a research map, not a claim that each paper was separately reviewed or reproduced.

## Related pages

- [[Speculative Decoding]]
- [[KV Cache]]
- [[Knowledge Distillation]]
- [[Linear Attention and Recurrent Memory]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
