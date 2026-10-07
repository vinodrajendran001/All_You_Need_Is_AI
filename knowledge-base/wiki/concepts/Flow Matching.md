---
type: concept
created: 2026-09-04
updated: 2026-10-07
tags:
  - concept
  - generative-models
  - diffusion
  - theory
source_ids:
  - src-2026-08-31-docmilanfar-lagrangian-flow-matching
  - src-2026-08-30-halo-research-sopro-v2
status: active
---

# Flow Matching

## Definition

Flow matching learns a time-dependent generative flow between simple and target distributions.
Straight-line conditional paths between noise and data are an important training choice, not a
guarantee that the learned flow is straight or that one numerical step will suffice.

## Why it matters

Sequential model evaluations can dominate generation latency, so changing the learned path and
training for fewer evaluations can be useful. The vault has two different evidence grades:
[[@docmilanfar - A Lagrangian View of Flow Matching]] offers a geometric intuition, while
[[Halo Research - Sopro V2 On-Device Text-to-Speech]] reports a specific acoustic-head result.
The latter does not prove the former's mathematical explanation.

## Current synthesis

### Conditional training paths and learned trajectories are different

The geometric source emphasizes straight noise/data interpolation. Learning a velocity field from
conditional targets need not preserve each pair's straight path. Reflow can change the coupling
used for training and make low-step generation easier, but this does not establish zero residual
uncertainty or remove model-capacity and approximation limits.

### An advection identity is not a straight-path theorem

If `f` is constant along a flow, the chain rule gives `partial_t f + J_f v = 0`.
It does not require straight characteristics or `partial_t f = 0`. A rotating flow with
`f(x,t) = R(-t)x` preserves its initial label along circular trajectories; the partial-time and
transport terms cancel. The source summary records this counterexample and a Gaussian denoiser
whose posterior covariance shrinks rather than explodes as noise vanishes.

The October 7 correction therefore narrows this page's earlier claim that straightness and
few-step sampling follow from the PDE alone. **Jacobian Penalty** remains the author's framing,
not a generally established law equating step count with uncertainty.

### A bounded engineering result

[[Halo Research - Sopro V2 On-Device Text-to-Speech]] reports self-distillation with reflow from
**32 to two acoustic solver steps**, described as a **16x speedup of the acoustic head**.
The head generates mel spectrograms; a separate Vocos vocoder produces audio. This is neither a
16x end-to-end TTS result nor a flow-matching vocoder.

The authors report near-parity after reflow. Their published comparisons also change model size
from a 0.5B base to 120M Turbo, so those tables are not a matched reflow-only ablation. The useful
synthesis is to evaluate path/training changes on a specified subsystem and quality target,
not to infer a universal mechanism from a successful application.

## Open questions

- Which probability paths, training objectives, and solvers give the best quality at a fixed
  latency budget?
- When does a target-drift diagnostic add predictive value beyond direct quality/latency
  measurements?
- How much of a reflow gain comes from the changed coupling, distillation recipe, model capacity,
  or solver configuration?
- Which conclusions survive matched ablations rather than comparisons that change several
  components at once?

## Related pages

- [[Halo Research - Sopro V2 On-Device Text-to-Speech]]
- [[@docmilanfar - A Lagrangian View of Flow Matching]]
- [[Diffusion Models]]
- [[Knowledge Distillation]]
- [[Neural Text-to-Speech]]
- [[Video Transformers]]
- [[On-Device Reasoning]]
- [[Test-Time Scaling]]
- [[Speculative Decoding]]
- [[@docmilanfar]]
