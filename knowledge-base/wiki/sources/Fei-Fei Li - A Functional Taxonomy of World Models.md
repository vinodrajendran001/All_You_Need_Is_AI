---
type: source-summary
created: 2026-06-05
updated: 2026-06-05
source_id: src-2026-06-05-fei-fei-li-taxonomy-world-models
source_title: A Functional Taxonomy of World Models
source_author: Fei-Fei Li et al. (World Labs)
source_url: https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models
tags:
  - source-summary
  - world-models
  - spatial-intelligence
  - robotics
  - generative-ai
source_ids:
  - src-2026-06-05-fei-fei-li-taxonomy-world-models
status: active
---

# Fei-Fei Li - A Functional Taxonomy of World Models

## Summary

A Substack essay by Fei-Fei Li and the World Labs team (published 2026-06-04) that cuts through the overloaded term "world model" by mapping all current systems back to the POMDP loop from RL theory. The essay proposes three functional categories — **Renderer**, **Simulator**, **Planner** — and argues that: (1) the simulator is the most consequential and most under-built category today; (2) the boundaries between the three are already collapsing; and (3) the logical endpoint is one unified foundation model that can switch between output modalities depending on what the consumer needs. The essay doubles as a product announcement for World Labs' Marble, their 3D environment generator that outputs both Gaussian splats and collision meshes from the same model.

## Key claims

- The correct frame for all "world models" is the **POMDP loop**: agent → action → state → observation → back. The three categories are three different projections of this same loop.
  - **Renderer** outputs observations (pixels for human eyes). Optimizes for visual fidelity. Cannot be trusted for physics accuracy. Most commercially mature (text-to-video, image generation).
  - **Simulator** outputs state (geometrically and physically accurate representation). Serves both human professionals and computer programs. Bridge between rendering and planning. Most consequential, least publicly visible.
  - **Planner** outputs actions (what the agent should do given observation + goal). Most intriguing, most nascent. Vision-Language-Action models and World Action Models are attempts at planners.
- "Simulation is the linchpin." Renderers optimize for plausibility; planners optimize for action; simulators operate at geometry + physics, the level from which both can be derived.
- The most important current trend is **convergence**: the same underlying world knowledge (geometry, materials, physics, dynamics) is required for all three, so the cleanest architecture would let one model switch output modality.
- Hard open problems live in simulation: 3D data is orders of magnitude scarcer than video; sim-to-real gap persists; AI-generated geometry can look correct while containing broken physics; multi-physics simulation at scale remains expensive.
- World Labs' **Marble** is their first simulator entry: text/image/video → explorable 3D environments (Gaussian splats + collision meshes).

## Why it matters

This source deepens the vault's `World Models` concept page with a clear functional taxonomy, ties the rendering/simulation/planning split back to the POMDP formalism from `Reinforcement Learning`, and adds `World Labs` and `Fei-Fei Li` as new entities. It also bridges to `Latent-Space Reasoning` (latent world state) and `AI Agents in Production` (simulators as training grounds for robots and autonomous systems).

## Tensions / open questions

- The essay is partly a product launch pitch (Marble). How much does World Labs' competitive position shape which problems are emphasized?
- The "unified world model" thesis is compelling but faces the data imbalance problem the essay itself identifies: video data for renderers vastly outweighs 3D+physics data for simulators.
- The essay barely mentions language/text as world model input/output — is text-world grounding treated as solved or just out of scope?

## Affected pages

- [[World Models]]
- [[Latent-Space Reasoning]]
- [[Reinforcement Learning]]
- [[AI Agents in Production]]
- [[World Labs]]
- [[Fei-Fei Li]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/A Functional Taxonomy of World Models.md`
- Source URL: [https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models](https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models)

## Related pages

- [[World Models]]
- [[Latent-Space Reasoning]]
- [[Reinforcement Learning]]
- [[AI Agents in Production]]
- [[World Labs]]
- [[Fei-Fei Li]]
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]]
- [[AI Knowledge Base Overview]]
