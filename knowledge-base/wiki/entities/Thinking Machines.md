---
type: entity
created: 2026-07-03
updated: 2026-11-13
entity_kind: organization
tags:
  - entity
  - organization
  - research-lab
  - voice-ai
  - human-ai-collaboration
source_ids:
  - src-2026-07-03-bytebytego-thinking-machines-interaction
  - src-2026-08-19-bytebytego-inkling
  - src-2026-11-06-nous-arete-27b
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
- [[ByteByteGo - The New American AI Model Designed to Be Customized]] adds Inkling, a 952B stored-parameter sparse MoE positioned for adaptation with mixed local/global attention and an exposed reasoning-effort control. These architecture details remain publication- and company-reported.
- [[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]] used Inkling as the teacher for Arete-27B, calling it "the best open model with a positive eval on what we were targeting". On Nous's 803-prompt evaluation, judged by Grok 4.7, Inkling has the highest fact score in the table (**3.96** of 5) and ties Mistral Large 4 for the lowest rate of answers adopting the official line (**0.3%**). The capture does not name Inkling's maker; the link to Thinking Machines rests on the ByteByteGo summary above. It is one judge on one evaluation, built by the downstream user.

## Related pages

- [[ByteByteGo - Inside Thinking Machines Interaction Models]]
- [[Real-Time Voice AI]]
- [[LLM Inference]]
- [[Mixture of Experts]]
- [[AI Knowledge Base Overview]]
- [[ByteByteGo - The New American AI Model Designed to Be Customized]]
- [[Open Model Ecosystems]]
- [[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]]
