---
type: concept
created: 2026-06-02
updated: 2026-06-23
tags:
  - concept
  - world-models
  - planning
  - robotics
  - spatial-intelligence
source_ids:
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
  - src-2026-06-05-fei-fei-li-taxonomy-world-models
  - src-2026-06-23-mayank-pratap-singh-diffusion-visual-breakdown
status: active
---

# World Models

## Definition

World models are learned predictive models of how an environment evolves over time. Instead of mapping observations directly to actions, they model future states, observations, or latent dynamics so an agent can imagine consequences before acting.

## Why it matters

World models sit at the boundary between generative modeling, planning, robotics, and reinforcement learning. They matter because they promise a more general route to control: learn a model of the world well enough, then use that model for planning, policy learning, or simulation.

## Current synthesis

- The YC Paper Club session frames world models as a resurgent research direction rather than a niche curiosity. The presenter explicitly treats them as a hot area again and ties them to current large funding and product interest.
- In the robotics framing from the video, world models connect naturally to **model predictive control**: if a model can predict future trajectories or observations, it can be used inside a planning loop instead of only as an offline simulator.
- The discussion also ties world models to **video models** and broader predictive modeling, suggesting that progress in generative sequence modeling may transfer into control and embodied-policy settings.
- World models overlap with [[Latent-Space Reasoning]] in that both rely on learned internal predictive structure, but the emphasis is different: latent reasoning is about internal computation steps, while world models are about predicting external environment dynamics.

### Fei-Fei Li functional taxonomy (2026)

[[Fei-Fei Li - A Functional Taxonomy of World Models]] provides the sharpest conceptual map in this vault. The unifying frame is the **POMDP loop** (agent → action → state → observation → back), and all world model systems are projections of that loop:

| Category | Output | Optimizes for | Maturity |
|----------|--------|--------------|---------|
| **Renderer** | Observations (pixels) | Visual plausibility | Commercially mature (text-to-video, image gen) |
| **Simulator** | State (geometry, physics) | Physical accuracy | Consequential but under-built |
| **Planner** | Actions | Decision quality | Most nascent |

Key claim: **simulation is the linchpin.** Renderers optimize for plausibility; planners optimize for action; only the simulator operates at the geometry/physics level from which both can be derived. This makes simulators a strategic capability node — they are the bridge between the other two categories.

The hard problems cluster in simulation: 3D data is orders of magnitude scarcer than video, AI-generated geometry can look correct while violating physics constraints, and full multi-physics simulation at scale remains expensive. Data scarcity is worst precisely where capability leverage is highest.

**Convergence thesis:** The essay argues that the renderer/simulator/planner distinction is already dissolving. All three require the same underlying world knowledge (geometry, materials, physics, dynamics), so the logical endpoint is one unified foundation model that switches output format depending on what the downstream consumer needs. [[World Labs]]' **Marble** product — text/image/video → explorable 3D environment outputting both Gaussian splats and collision meshes — illustrates this convergence: one system spans renderer and simulator outputs from the same representation.

### Diffusion as renderer and trajectory mechanism

[[Mayank Pratap Singh - Diffusion Model Visual Breakdown]] adds the mechanism behind many renderer-style world-model outputs. [[Diffusion Models]] learn a path from Gaussian noise to structured data by repeatedly denoising, often in latent space and often conditioned on text or other control signals.

For world models, the useful distinction is:

- diffusion is a **generative path** from a simple distribution to data;
- a world model is a **predictive model of environment dynamics**.

Diffusion can implement renderer-like world-model components and can be adapted to video, trajectory, or control settings, as the YC Paper Club source notes. But visual plausibility is not the same as physical simulation. A diffusion renderer can make believable pixels while still violating geometry, causality, or physics unless the broader system grounds it in state and dynamics.

### Open questions

- What representation is best for scalable world models: pixels, tokens, latent states, or hybrid forms?
- Can world models generalize robustly enough for open-ended real-world environments, or will they remain strongest in constrained domains?
- The unified world model thesis faces a data imbalance problem the essay itself identifies: video data for renderers vastly outweighs 3D+physics data for simulators. Can this gap be closed synthetically?

## Related pages

- [[Fei-Fei Li - A Functional Taxonomy of World Models]]
- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]]
- [[Diffusion Models]]
- [[Mayank Pratap Singh - Diffusion Model Visual Breakdown]]
- [[Latent-Space Reasoning]]
- [[Reinforcement Learning]]
- [[AI Agents in Production]]
- [[World Labs]]
- [[Fei-Fei Li]]
- [[AI Knowledge Base Overview]]
