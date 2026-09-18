---
type: concept
created: 2026-09-18
updated: 2026-09-18
tags: [concept, robotics, video-models, pre-training]
source_ids:
  - src-2026-09-14-rhoda-web-video-pretraining-robots
status: active
---

# Video Pre-training for Robot Policies

## Definition

Video pre-training for robot policies learns predictive visual representations from abundant
non-robot video, then adapts them to demonstrations from a physical robot. A separate action decoder
can translate predicted future frames into motor commands.

## Why it matters

Robot demonstrations are expensive and narrow; web video is plentiful but lacks action labels.
Transfer works only if better video prediction survives embodiment, action decoding, post-training,
and physical execution. Proxy quality therefore needs validation against real task completion.

## Current synthesis

[[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]] reports one controlled industrial case.
Its Direct Video-Action pipeline keeps the downstream task and inverse-dynamics decoder fixed while
varying pre-trained model size and training duration. Completion rises from **4% to 85%** across
XS-to-L models, while fixed-M checkpoints rise from **58% to 75%** across a 0.08x-to-1x compute sweep.

The strongest result is not simply "scale works." Seven checkpoints rank in the same order on
DINO-based held-out video prediction and real-robot completion. That makes video prediction a
candidate checkpoint-selection signal for this architecture.

The boundary is equally important. The study covers one bearing-unpacking task, one embodiment, one
architecture family, and one post-training run per condition. DINO Frechet distance ignores temporal
coherence, the size sweep is not compute-matched, and the data-scarcity interaction is suggestive
(`p=0.07`) rather than conventionally significant.

## Open questions

- Does the proxy-task relationship transfer across embodiments, action decoders, and task families?
- Which video qualities matter for control beyond frame-level feature distributions?
- Does scaling still help when model size, tokens, and post-training compute are jointly matched?
- How much trial and seed variance is hidden by one post-training run per condition?

## Related pages

- [[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]
- [[Video Transformers]]
- [[World Models]]
- [[Reinforcement Learning]]
- [[Autonomous Driving Systems]]

