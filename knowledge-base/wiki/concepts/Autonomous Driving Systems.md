---
type: concept
created: 2026-08-24
updated: 2026-08-24
tags: [concept, autonomous-driving, robotics, world-models]
source_ids:
  - src-2026-08-18-bytebytego-waymo-vs-tesla
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

## Related pages

- [[World Models]]
- [[Vision-Language Grounding]]
- [[ML Systems at Scale]]
- [[AI Agents in Production]]
- [[ByteByteGo - Waymo vs Tesla - Two Ways to Build Self-Driving Cars]]

