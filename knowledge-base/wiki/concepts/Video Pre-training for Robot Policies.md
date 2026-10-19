---
type: concept
created: 2026-09-18
updated: 2026-10-19
tags: [concept, robotics, video-models, pre-training]
source_ids:
  - src-2026-09-14-rhoda-web-video-pretraining-robots
  - src-2026-10-15-potter-how-to-train-your-robot
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

### Web video is one route among several

[[Brian Potter - How to Train Your Robot]] places this approach in a wider map of robot data.
Interest in generic web video comes from its ubiquity, and NVIDIA's Cosmos is cited as a
video-trained foundation model usable as a policy backbone. In Potter's survey, though, web video is
the cheapest and least action-specific route: it is not task-completion data, and human egocentric
video adds a human-to-robot mapping problem that teleoperation and UMI data largely avoid. Video is
also highly correlated from frame to frame. Chris Paxton's estimate of about **3,600** useful tokens
per hour of video, after a tenfold discount, is an order-of-magnitude guess rather than a measured
training signal.

The two sources answer different questions. Rhoda shows that, for one task and one decoder, more
web-video pre-training moved physical completion. Potter's figures are collection volumes and
prices. Neither establishes how many video hours a policy needs, or what an hour of web video is
worth against an hour of teleoperation at matched cost. See [[Robot Training Data]].

## Open questions

- Does the proxy-task relationship transfer across embodiments, action decoders, and task families?
- Which video qualities matter for control beyond frame-level feature distributions?
- Does scaling still help when model size, tokens, and post-training compute are jointly matched?
- How much trial and seed variance is hidden by one post-training run per condition?
- What is an hour of web video worth against an hour of teleoperation, UMI, or simulated data at
  matched cost?

## Related pages

- [[Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]
- [[Brian Potter - How to Train Your Robot]]
- [[Robot Training Data]]
- [[NVIDIA]]
- [[Video Transformers]]
- [[World Models]]
- [[Reinforcement Learning]]
- [[Autonomous Driving Systems]]

