---
type: concept
created: 2026-08-24
updated: 2026-10-19
tags: [concept, autonomous-driving, robotics, world-models]
source_ids:
  - src-2026-08-18-bytebytego-waymo-vs-tesla
  - src-2026-10-15-potter-how-to-train-your-robot
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

## Related pages

- [[World Models]]
- [[Vision-Language Grounding]]
- [[ML Systems at Scale]]
- [[AI Agents in Production]]
- [[ByteByteGo - Waymo vs Tesla - Two Ways to Build Self-Driving Cars]]
- [[Brian Potter - How to Train Your Robot]]
- [[Robot Training Data]]

