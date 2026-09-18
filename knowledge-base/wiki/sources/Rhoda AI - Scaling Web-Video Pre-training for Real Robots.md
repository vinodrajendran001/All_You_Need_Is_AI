---
type: source-summary
created: 2026-09-18
updated: 2026-09-18
source_id: src-2026-09-14-rhoda-web-video-pretraining-robots
source_title: "Does Scaling Web-Video Pre-training Help Real Robots Do Real Work?"
source_author: Rhoda AI
source_url: https://www.rhoda.ai/research/scaling-web-video-pretraining
tags: [source/summary, robotics, video-models, scaling]
source_ids: [src-2026-09-14-rhoda-web-video-pretraining-robots]
status: active
---

# Rhoda AI - Scaling Web-Video Pre-training for Real Robots

## Summary

Rhoda AI tests whether larger video models and longer web-video pre-training improve an industrial
bearing-unpacking policy. Its Direct Video-Action pipeline predicts future frames and converts them
to robot actions through a fixed inverse-dynamics model. Model size and pre-training duration are
varied separately while the task, action decoder, post-training procedure, and strict 100-second
completion metric remain fixed.

## Key claims

- XS/S/M/L models achieved **4%/65%/75%/85%** at-speed completion.
- Fixed-M checkpoints at **0.08x/0.18x/0.37x/1x** pre-training compute reached
  **58%/67%/74%/75%**.
- The compute-budget spread was largest at 25% demonstration data, but the interaction result was
  only suggestive: coefficient **-0.09**, SE **0.05**, chi-square **3.2**, `p=0.07`.
- DINO Frechet distance over 400,000 predicted and 400,000 true frames ranked seven checkpoints in
  the same order as robot performance.
- Evaluation used generally 100-260 trials per policy and more than 200 robot-hours.

## Why it matters

The source links a pre-training proxy to physical task success rather than stopping at video quality.
Within this one setup, better web-video prediction correlates with better industrial manipulation.

## Tensions and caveats

This is self-reported vendor evidence from one task, embodiment, architecture family, and post-training
run per condition. Model sizes and absolute compute are undisclosed; size runs are not compute-matched;
DINO distance ignores temporal coherence; and the result does not establish a general robotics scaling law.

## Raw capture

- [[2026-09-14 Rhoda AI - Scaling Web-Video Pre-training for Real Robots]]

## Affected pages

- [[Video Pre-training for Robot Policies]]
- [[World Models]]
- [[Video Transformers]]

## Related pages

- [[Reinforcement Learning]]
- [[Autonomous Driving Systems]]

