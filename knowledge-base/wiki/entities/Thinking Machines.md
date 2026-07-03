---
type: entity
created: 2026-07-03
updated: 2026-07-03
entity_kind: organization
tags:
  - entity
  - organization
  - research-lab
  - voice-ai
  - human-ai-collaboration
source_ids:
  - src-2026-07-03-bytebytego-thinking-machines-interaction
status: active
---

# Thinking Machines

## What it is

Thinking Machines is a relatively new AI research lab focused on human-AI collaboration. It publishes research under the name **Connectionism** and offers developer-facing products. Its distinguishing bet is that most labs over-index on *autonomous* capability (a model that takes a task and returns a result alone), while real work benefits from continuous, interruptive collaboration where the human clarifies and redirects as the model goes.

## Why it matters here

Thinking Machines is the subject of [[ByteByteGo - Inside Thinking Machines Interaction Models]] and the source of the vault's **interaction model** thesis: real-time voice AI built from turn-based models plus helper harnesses has a ceiling, and the way past it is to move interactivity inside the model. Its **TML-Interaction-Small** (276B-parameter [[Mixture of Experts|MoE]], 12B active) demonstrates **time-aligned micro-turns** and **fast/slow two-model coordination**, forming the model-architecture half of the [[Real-Time Voice AI]] concept. It also contributed a streaming-session feature to open-source SGLang, touching [[LLM Inference]].

## Notes

- Built its own benchmarks (TimeSpeak, CueSpeak, RepCount-A, ProactiveVideoQA) because existing voice benchmarks miss proactive, time-aware, and visual behaviours.
- Explicitly grounds its design philosophy in Rich Sutton's "Bitter Lesson."

## Related pages

- [[ByteByteGo - Inside Thinking Machines Interaction Models]]
- [[Real-Time Voice AI]]
- [[LLM Inference]]
- [[Mixture of Experts]]
- [[AI Knowledge Base Overview]]
