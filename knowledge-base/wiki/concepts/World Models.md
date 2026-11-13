---
type: concept
created: 2026-06-02
updated: 2026-11-13
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
  - src-2026-07-21-bytebytego-roblox-world-models
  - src-2026-09-07-rai-lejepa
  - src-2026-09-14-rhoda-web-video-pretraining-robots
  - src-2026-10-15-potter-how-to-train-your-robot
  - src-2026-11-03-nvidia-cosmos-interactive-world-models
  - src-2026-11-11-nvidia-gr00t-2
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

## Engine-authoritative hybrids

[[ByteByteGo - Inside Roblox's Bet on World Models]] describes a deployment shape that sidesteps most of this page's hard problems by refusing the strong version of the goal. Deterministic game state, rules, and physics stay in the engine as the authoritative shared-world substrate; a learned model acts as a **video upsampler** conditioned on that state. The generated image is *presentation*, never the authoritative multiplayer state.

The move is worth generalizing, within limits. Conditioning generation on engine state constrains the model with geometry and rules instead of asking it to learn a whole consistent world. The engine stays the authority on what exists, and a retrieval step supplies the objects relevant to the current view, which keeps the world from drifting frame to frame. It does not dissolve this page's two main failure modes. Consistency across many frames still needs a longer context window, which Roblox is extending after acquiring Morpheus AI. Rendering multiplayer actions for thousands of players at once is described as "an active research area, not a solved feature." Each frame is conditioned on engine-derived inputs, which constrains the image without supplying a ground truth for it.

The caveat travels with it: the video model "is still in the lab, not yet running in real time," and 2K/60fps delivery, long-context visual consistency, and multiplayer scale are stated as **targets and open work**, not shipped capability.

## A JEPA objective with the anti-collapse heuristics removed

[[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]] matters to the JEPA line because it removes the scaffolding that made
joint-embedding prediction hard to reason about. **Predictor, teacher–student asymmetry and register
tokens can all be dropped** — significant because prior work found that removing predictors yields
chance-level encoders. The tutorial's gloss is that the heuristics **"were never wrong, they were
unnamed"**: they were doing the work of an anti-collapse term that is now written down explicitly as
SIGReg. See [[Joint-Embedding Predictive Architecture]].

**Architecture-independence is the strongest empirical claim**: **50 timm architectures under 20M
parameters from 8 families all land between 91.5% and 95% top-1** on ImageNet-10 with a single λ, stable
across two orders of magnitude, and still competitive at **batch size 128**.

**Emergent PCA object–background separation and unsupervised video object tracking** are reported, which
is the behaviour the world-model framing predicts.

Two limits belong with this: it is **vision only**, and **no matched-compute comparison against DINOv2 or
DINOv3 has been run** — the headline Galaxy10 result compares a from-scratch model against transferred
features, which is a different question from whether LeJEPA is a better pretraining objective at equal
compute.

## A predictive video model crossed into physical control

[[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]] adapts a causal video predictor to an
industrial bearing-unpacking policy through a fixed inverse-dynamics decoder. Completion rises from
4% to 85% across model sizes and 58% to 75% across a fixed-model compute sweep. Seven checkpoints
rank in the same order on DINO video-prediction distance and physical completion.

The scope remains narrow: one vendor, task, embodiment, architecture family, and post-training run
per condition. The result supports transfer within that setup, not a universal robotics scaling law.

## Simulation as a source of robot data

[[Brian Potter - How to Train Your Robot]] adds the data-production view of the simulator category.
Simulated RL is cheap and massively parallel — Figure AI trained humanoid walking on thousands of
simulated robots — but its data is only as good as the simulation. Locomotion is characterized well
enough to simulate; soft or deformable manipulation is not, the sim-to-real gap that the Fei-Fei Li
taxonomy also lists among simulation's open problems. Domain randomization trades accurate modeling
for coverage: OpenAI's Rubik's Cube hand needed about **13,000 simulated years** and reached **20%**
success on maximally difficult starting arrangements. Potter reports randomization as fairly standard
for locomotion but not widely used for manipulation.

That qualifies the "simulation is the linchpin" thesis in practice: a simulator is the linchpin only
where its physics holds, and for robot control the missing physics is concentrated in contact-rich
manipulation. Potter also cites NVIDIA's Cosmos, a video-trained foundation model usable as a
robot-policy backbone, without performance evidence. See [[Robot Training Data]].

## Offline generation and closed-loop simulation need different generators

[[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]] turns
Potter's passing mention of Cosmos into a product description. It also splits generation by
**how the output will be consumed**:

- **Offline synthetic data** can use a **bidirectional** generator. Cosmos3-Nano-Transfer-Auto
  denoises "an entire multi-view clip at once", up to **400 frames** at **30 fps**. A prompt edit
  turns a daytime drive into a rainy night "while keeping the same road layout and vehicle
  trajectories".
- **Closed-loop simulation** needs a **causal**, few-step distilled variant. Cosmos3-Nano-Sim-Auto
  streams camera and LiDAR observations autoregressively while a driving policy or human changes
  the scenario, and the outputs return to the policy. Cosmos3-H-Dreams does the same for surgical
  robots, generating frames from live kinematics.

The reason is structural: the next frame in a closed loop depends on an action that has not yet
been taken, so the clip cannot be denoised as a whole. In the Fei-Fei Li taxonomy, these
checkpoints are renderers conditioned on state or actions, and they differ in who holds the
state. Sim-Transfer paints RGB over depth or segmentation video "while the simulator maintains
physical state". Sim-Auto's figure has the AlpaSim runtime update the scenario and pass it to
the generator through World Scenario Map controls. Both are engine-authoritative hybrids like
Roblox's. Sim-Bimanual and Cosmos3-H-Embodied-Nano instead predict observations directly from
actions. For surgery this is pitched as "a complementary approach" to classical simulators,
which struggle with "complex multi-physics", so the learned model carries the dynamics itself.

This is vendor documentation. It shows reference runs and output checks (finite LiDAR values,
alignment across views) but **no measure of physical fidelity, sim-to-real transfer or policy
improvement**. The "simulation is the linchpin" thesis therefore gains infrastructure here, not
evidence.

## A world-action model, and a simulator checked against real rankings

[[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
calls GR00T 2 a "world-action model" (WAM). One diffusion transformer predicts future video and
robot actions together, and small per-robot heads turn the plan into motor commands. In the Fei-Fei
Li taxonomy, its outputs span two categories: the renderer's observations and the planner's actions.
That makes it a second example for the convergence thesis, after World Labs' Marble, which spans
renderer and simulator. Here the joint output is the design from the start. NVIDIA says that
predicting how the scene should change "lets GR00T 2 learn physics from human video". That physics
stays implicit in predicted pixels, and GR00T 2 does not output simulator state. It is therefore not
evidence that a learned model can replace the simulator.

The same page uses a conventional simulator in two ways and reports results for both:

- **As a data source.** With the same real data, adding simulated episodes raised GR00T 2 Turbo's
  out-of-distribution success on the G1 humanoid from **6.7%** to **63.3%**; GR00T 1.7 rose to
  **40.0%**. That is one comparison in one setting, but it is a positive manipulation result for a
  route that Potter reports as weaker for manipulation than for locomotion.
- **As an evaluator.** An agent-assisted workflow builds digital twins of real tasks from robot
  videos, 3D scans, and photographs. The twins are validated by replaying demonstrations, stability
  tests, and human expert feedback. Across **14** GR00T 2 policies on a **25**-task YAM benchmark,
  simulated and real success rates correlate at Pearson **0.92** and Spearman **0.89**, and Elo
  scores at **0.93** and **0.90**. NVIDIA reports screening data-pipeline changes and inference
  settings in simulation before robot tests.

This qualifies the Cosmos 3 verdict above of "infrastructure, not evidence". GR00T 2 is the vault's
first report of a simulator ranking policies roughly as real robots do. The result is first-party
and narrow: one robot, one benchmark, and **14** policies from one model family. Close agreement
within one family does not show that the simulator would rank a different architecture correctly.
The third reported metric, MMRV **0.055**, is not defined in the capture.

## Open questions

- What representation is best for scalable world models: pixels, tokens, latent states, or hybrid forms?
- Can world models generalize robustly enough for open-ended real-world environments, or will they remain strongest in constrained domains?
- How much fidelity do causal, few-step distilled world models lose relative to their bidirectional
  teachers, and is it enough to change a policy evaluation's verdict?
- Does a digital-twin evaluator that ranks one model family's policies correctly also rank other
  architectures, or policies with different failure modes, correctly?
- The unified world model thesis faces a data imbalance problem the essay itself identifies: video data for renderers vastly outweighs 3D+physics data for simulators. Can this gap be closed synthetically?

## Related pages

- [[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]]
- [[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
- [[NVIDIA]]
- [[Autonomous Driving Systems]]
- [[Brian Potter - How to Train Your Robot]]
- [[Robot Training Data]]
- [[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]
- [[Video Pre-training for Robot Policies]]
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
- [[ByteByteGo - Inside Roblox's Bet on World Models]]
- [[ML Systems at Scale]]
- [[Siddhant Rai - LeJEPA Provable and Scalable Self-Supervised Learning]]
- [[Joint-Embedding Predictive Architecture]]
- [[Siddhant Rai]]
