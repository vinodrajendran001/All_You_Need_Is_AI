---
type: concept
created: 2026-06-17
updated: 2026-06-17
tags:
  - concept
  - post-training
  - distillation
  - rl
  - frontier-models
source_ids:
  - src-2026-06-17-nathan-lambert-frontier-post-training-recipe-review
status: active
---

# Multi-Teacher On-Policy Distillation

## Definition

Multi-Teacher On-Policy Distillation (MOPD) is a frontier post-training pattern where a general student model samples its own trajectories, each trajectory is routed to a relevant domain-specialist teacher, and the student is trained to match the teacher's token distribution (often via reverse KL) while remaining inside an RL-style on-policy training loop.

## Why it matters

MOPD is one of the clearest 2026 signs that frontier post-training has moved beyond a single SFT -> preference -> RL recipe. It decomposes capability building into domain-specialist teachers, then consolidates those capabilities into one deployable general model. This is both a technical pattern and an organizational scaling pattern.

## Current synthesis

[[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]] frames MOPD as the new recipe shape emerging across MiMo Flash V2, DeepSeek V4, and Nemotron 3 Ultra:

1. Train multiple domain-specialist teachers. Each teacher may have its own SFT, RLVR, agentic RL, safety RL, or code/math recipe.
2. Train one general student by sampling from the student's own policy, not just replaying fixed teacher traces.
3. Route each rollout to the relevant teacher.
4. Apply a token-level distillation loss, often reverse KL to the teacher output distribution, and optionally combine it with other RL losses such as verifiable rewards.

## Why it emerged

- **Mixed-domain RL is conflict-prone.** Math, code, agentic tool use, safety, and general chat can trade off when optimized inside one monolithic RL run.
- **Specialists are organizationally scalable.** Separate teams can improve domain teachers in parallel, then a consolidation stage merges them.
- **On-policy distillation matured.** The RLVR renaissance made labs better at running on-policy loops and combining distillation with RL-style objectives.
- **Frontier post-training became industrial.** The source repeatedly emphasizes that recipe complexity now maps onto organizational capacity: modern post-training is partly "wrangling an org chart."

## Relationship to other post-training stages

- Compared with **SFT**, MOPD is not just imitation of fixed demonstrations. The student samples its own trajectories, so the supervision is on-policy.
- Compared with **DPO**, MOPD does not rely on chosen/rejected pairs. It transfers full teacher distributions token by token.
- Compared with **RLVR**, MOPD can be combined with verifiable rewards, but its supervision comes from specialist teachers rather than only scalar correctness signals.
- Compared with **trace distillation SFT**, MOPD avoids some off-policy mismatch by training on the current student's rollouts.

## Failure modes and open problems

- **Teacher/student mismatch:** Nemotron 3 Ultra reports that teachers trained with substantially different pipelines cannot be naively combined; the student's rollouts may be out-of-distribution for the teacher.
- **Cross-teacher alignment:** if teachers learn incompatible reasoning styles, the student receives inconsistent distributional targets.
- **Consolidation schedule:** one open question is whether to use final converged teachers or gradually distill from intermediate checkpoints as teachers improve.
- **Magnitude of benefit:** the source treats the relative gain of MOPD versus trace-distillation SFT as still unclear.
- **Transparency:** even when a frontier lab publishes a recipe, the recipe may be too complex to reproduce without the org chart, teacher checkpoints, data mixtures, and implementation details.

## Related pages

- [[Nathan Lambert - Frontier post-training recipe review with Finbarr Timbers]]
- [[LLM Training Pipeline]]
- [[Reward Design for RL]]
- [[Direct Preference Optimization]]
- [[Group Relative Policy Optimization]]
- [[Automated AI Research]]
- [[AI Knowledge Base Overview]]
