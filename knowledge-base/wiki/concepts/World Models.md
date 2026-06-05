---
type: concept
created: 2026-06-02
updated: 2026-06-05
tags:
  - concept
  - world-models
  - planning
  - robotics
  - spatial-intelligence
source_ids:
  - src-2026-06-02-ycombinator-yc-paper-club-inference-diffusion-world-models
  - src-2026-06-05-fei-fei-li-taxonomy-world-models
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

## Open questions

- What representation is best for scalable world models: pixels, tokens, latent states, or hybrid forms?
- Can world models generalize robustly enough for open-ended real-world environments, or will they remain strongest in constrained domains?

## Related pages

- [[Y Combinator - Inference, Diffusion, World Models, and More - YC Paper Club]]
- [[Latent-Space Reasoning]]
- [[Reinforcement Learning]]
- [[AI Knowledge Base Overview]]
