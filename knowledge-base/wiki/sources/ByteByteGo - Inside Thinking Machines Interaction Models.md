---
type: source-summary
created: 2026-07-03
updated: 2026-07-03
source_id: src-2026-07-03-bytebytego-thinking-machines-interaction
source_title: "Inside Thinking Machines' Interaction Models"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/inside-thinking-machines-interaction
tags:
  - source-summary
  - voice-ai
  - multimodal
  - real-time
  - architecture
source_ids:
  - src-2026-07-03-bytebytego-thinking-machines-interaction
status: active
---

# ByteByteGo - Inside Thinking Machines Interaction Models

## Summary

This ByteByteGo article explains Thinking Machines' research preview of an **interaction model** — an argument that today's real-time voice AI has a ceiling because it wraps a turn-based language model in a **harness** of simpler helper systems (voice activity detection, speech-to-text, text-to-speech, a dialog manager). Because the helpers are lighter models than the LLM they surround, whole categories of behaviour (proactive interjection, visual reactions) stay out of reach. Invoking Rich Sutton's "Bitter Lesson," Thinking Machines argues that hand-crafted harness heuristics are exactly what scale eventually pushes out; the way past the ceiling is to **put interactivity inside the model itself.**

Their answer, TML-Interaction-Small, is a 276B-parameter [[Mixture of Experts|MoE]] model (12B active) built **audio/video-first** rather than text-first. Three design choices carry it: **time-aligned micro-turns** (slice time into 200 ms chunks instead of discrete turns), **lightweight from-scratch audio/video encoders** (skipping heavy pretrained encoders like Whisper), and a **two-model split** pairing a fast interaction model with a slower background reasoning model that share context. They contributed a streaming-session feature to open-source SGLang to serve 200 ms chunks efficiently.

## Key claims

- **The bottleneck is the turn.** A typical LLM works in a single thread: it waits for a finalised input, and once it starts generating its perception freezes and new input is queued. This narrows the human-AI channel to "prompting and waiting" and forces the human to think like a model.
- **Today's voice AI is a harness**, not real-time cognition: VAD + STT + LLM + TTS + dialog manager simulate conversation around a turn-based core. The helpers are simpler than the LLM, which caps behaviours like "interrupt me when I say something wrong" or "tell me when I've written a bug."
- **The Bitter Lesson applied to interactivity:** general computation + learning beat hand-designed heuristics, so harness components should be absorbed into the model.
- **Micro-turns make time the unit of conversation.** Every 200 ms the model ingests whatever arrived across audio/video/text and decides what to emit across audio/text — enabling speaking while listening (live translation), watching while speaking (sports commentary), and mid-sentence visual interjection (counting pushups).
- **Two-model coordination** resolves fast-vs-deep: the interaction model handles real-time dialog; when deeper reasoning/tool use/browsing is needed it hands a rich full-conversation context to an asynchronous background model whose results stream back and are woven in when the moment fits — the classic fast-path/slow-path OS pattern applied to inference.
- **New capabilities need new benchmarks.** Existing voice benchmarks miss these jumps, so Thinking Machines built **TimeSpeak** (initiate speech at user-specified times), **CueSpeak** (speak at the right moment while the user talks), **RepCount-A** (count reps from video), and **ProactiveVideoQA** (answers depend on what happens visually at specific moments); existing models mostly stay silent or answer wrong.
- **Limitations:** long sessions accumulate audio/video context fast and strain context management; low-latency streaming demands a reliable connection; and model size is capped by latency targets (their larger pretrained models are currently too slow to serve this way).

## Why it matters

This is the model-architecture half of the new [[Real-Time Voice AI]] concept, complementing the transport-infrastructure half in [[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]]: OpenAI keeps a turn-based model responsive with external scaffolding, while Thinking Machines argues the scaffolding is the ceiling. It gives [[LLM Inference]] a concrete streaming-session pattern (200 ms chunks, fast/slow two-model serving via SGLang) and adds a large sparse example to [[Mixture of Experts]] (276B total / 12B active). The "external scaffolding creates a ceiling" thesis echoes the [[Agent Skill|skills-as-scaffolding]] and harness debates elsewhere in the vault, and introduces the [[Thinking Machines]] entity.

## Tensions / open questions

- It is a research preview reconstructed by ByteByteGo; the benchmarks are Thinking-Machines-built and self-reported, with no independent replication yet.
- The "harness has a ceiling" argument is a strong bet, not a settled result — turn-based systems with better helpers may close some gaps the paper highlights.
- Long-session context management, the load-bearing limitation, is acknowledged but unsolved; it connects to the same long-context memory pressure discussed under [[KV Cache]] and [[Context Engineering]].

## Affected pages

- [[Real-Time Voice AI]]
- [[LLM Inference]]
- [[Mixture of Experts]]
- [[Thinking Machines]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/Inside Thinking Machines’ Interaction Models.md`
- Source URL: [https://blog.bytebytego.com/p/inside-thinking-machines-interaction](https://blog.bytebytego.com/p/inside-thinking-machines-interaction)
- Primary source: [Interaction Models: A Scalable Approach to Human-AI Collaboration](https://thinkingmachines.ai/blog/interaction-models/)

## Related pages

- [[Real-Time Voice AI]]
- [[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]]
- [[LLM Inference]]
- [[Mixture of Experts]]
- [[Thinking Machines]]
- [[ByteByteGo]]
- [[AI Knowledge Base Overview]]
