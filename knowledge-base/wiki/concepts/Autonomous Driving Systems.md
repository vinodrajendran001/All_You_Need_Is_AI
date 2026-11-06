---
type: concept
created: 2026-08-24
updated: 2026-11-06
tags: [concept, autonomous-driving, robotics, world-models]
source_ids:
  - src-2026-08-18-bytebytego-waymo-vs-tesla
  - src-2026-10-15-potter-how-to-train-your-robot
  - src-2026-11-03-nvidia-cosmos-interactive-world-models
status: active
---

# Autonomous Driving Systems

## Definition

Autonomous driving systems combine sensing, scene representation, prediction, planning, control, validation, and training to drive within a defined operational domain.

## Two architecture tendencies

[[ByteByteGo - Waymo vs Tesla - Two Ways to Build Self-Driving Cars]] contrasts two tendencies rather than two pure implementations:

- a structured, geofenced stack using multiple sensor modalities, HD maps, explicit intermediate representations, and simulation;
- a camera-centered, fleet-scaled stack that learns more of the internal representation and control policy end to end.

Structured representations expose objects, lanes, and predicted trajectories for inspection and targeted testing. Learned representations can retain visual nuance and reduce dependence on hand-designed schemas. Sensor redundancy can improve observability, while simpler hardware and broad data collection can improve scale. Each choice changes the validation problem downstream.

## Evaluation caution

Fleet mileage is meaningful only with operating-domain and supervision context. Driverless miles inside a constrained domain, supervised assistance miles, interventions, and simulated scenarios are not interchangeable denominators. Public accounts also lag changing production systems.

## Simulated mileage is volume, not validation

[[Brian Potter - How to Train Your Robot]] cites one scale comparison: by 2019 Waymo had driven
**10 million** miles in the real world and **10 billion** in simulation. Potter also notes that
synthetic data generation appears to be widely used for training autonomous vehicles. The
thousandfold ratio is the case the caution above anticipates. Simulated miles are cheap to produce
at scale, but what they are worth depends on how faithfully the simulator reproduces sensors, other
road users, and physics, and the 2019 figure carries no evidence on that fidelity. The broader
robotics comparison, including the sim-to-real gap for manipulation, is on [[Robot Training Data]].

## Generated sensors can close the loop around a driving policy

[[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]] describes
a learned sensor simulator rather than a mileage figure. Both of NVIDIA's AV checkpoints are
conditioned on **World Scenario Map** controls: lanes, objects, road markings, traffic signs and
road boundaries. Joint RGB-LiDAR generation adds HD-map rangemap controls. The structured scene
representation from the first architecture tendency above thus becomes the control input to a
generative model.

- **Cosmos3-Nano-Transfer-Auto** produces synchronized multi-camera video and LiDAR offline. Its
  four-GPU reference run yields **seven 720p videos (297 frames at 30 FPS) and 99 LiDAR sweeps**.
  Prompt edits re-render the same layout and trajectories in other weather and lighting, to "train
  and evaluate perception and driving models across weather and lighting conditions".
- **Cosmos3-Nano-Sim-Auto**, a causal, few-step distilled variant, streams observations while an AV
  policy or a human driver acts. Generated camera and LiDAR frames return to the policy, which
  enables **closed-loop evaluation**. The post's figure places it inside the AlpaSim runtime, with
  Alpamayo as an example policy.

This addresses one weakness of open-loop replay: the scene now reacts to the policy's own
actions. It does not answer the fidelity question raised above. The post's output checks confirm
finite LiDAR values and alignment across views, not that generated sensors match real ones. It
reports no closed-loop metric, no comparison with real driving or classical simulation, and no
measurement of what few-step distillation costs in quality. It is vendor documentation.

## Related pages

- [[World Models]]
- [[Elizabeth Goodman - Build World Models for Interactive Simulation with NVIDIA Cosmos]]
- [[NVIDIA]]
- [[Diffusion Models]]
- [[Vision-Language Grounding]]
- [[ML Systems at Scale]]
- [[AI Agents in Production]]
- [[ByteByteGo - Waymo vs Tesla - Two Ways to Build Self-Driving Cars]]
- [[Brian Potter - How to Train Your Robot]]
- [[Robot Training Data]]

