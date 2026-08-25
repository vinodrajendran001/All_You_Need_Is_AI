---
type: concept
created: 2026-07-03
updated: 2026-08-25
tags:
  - concept
  - voice-ai
  - real-time
  - multimodal
  - systems
source_ids:
  - src-2026-07-03-bytebytego-openai-voice
  - src-2026-07-03-bytebytego-thinking-machines-interaction
  - src-2026-08-21-hume-ai-asr-benchmark-optimization
status: active
---

# Real-Time Voice AI

## Definition

Real-time voice AI is the class of systems that hold a spoken (and increasingly audio-visual) conversation with a human at the speed of speech. Making it feel natural requires solving two very different problems at once: a **transport/serving layer** that moves a continuous low-latency media stream to and from the model, and a **model/architecture layer** that can perceive and respond continuously rather than in discrete turns.

## Why it matters

The difference between "a conversation" and "a walkie-talkie" is measured in milliseconds. Two 2026 sources attack the ceiling from opposite ends, and together they frame the whole stack: [[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI|OpenAI]] optimises the *pipes* around a turn-based model, while [[ByteByteGo - Inside Thinking Machines Interaction Models|Thinking Machines]] argues the scaffolding *is* the ceiling and moves interactivity into the model itself.

## The two layers

### Transport / serving infrastructure (OpenAI)

- **Continuous stream, not upload.** Audio must arrive as a steady flow so the model can transcribe, reason, and call tools while the user is still speaking; if the stream breaks, the experience degrades to push-to-talk.
- **WebRTC vs the cloud.** WebRTC (ICE + DTLS + SRTP + RTCP) assumes stable server IPs/ports; Kubernetes treats addresses as disposable, causing **port exhaustion** and **state stickiness**.
- **Relay/transceiver split.** A stateless, geo-distributed relay forwards encrypted packets at the edge; a stateful transceiver owns ICE/DTLS/SRTP and the session lifecycle. First-packet routing rides the **ICE ufrag** the protocol already exchanges, avoiding a hot-path lookup — a locality lesson shared with [[ML Systems at Scale]].
- **Simple beats exotic.** Userspace Go with `SO_REUSEPORT`, thread pinning, and pre-allocated buffers handled 900M weekly users without kernel bypass. The design assumes overwhelmingly **1:1** sessions (user ↔ model), which is why it skips the multiparty-oriented SFU.

### Model architecture (Thinking Machines interaction models)

- **The turn is the bottleneck.** A turn-based LLM waits for finalised input and freezes perception while generating; helper systems (VAD, STT, TTS, dialog manager) simulate real-time around it but are simpler models than the LLM, capping proactive and visual behaviours.
- **The Bitter Lesson applied to interactivity.** Hand-crafted harness heuristics are exactly what general computation + learning eventually replace, so interactivity should live inside the model.
- **Time-aligned micro-turns.** Slicing time into 200 ms chunks makes *time* — not the turn — the unit of conversation, unlocking speaking-while-listening (live translation), watching-while-speaking (commentary), and mid-sentence visual interjection.
- **Fast/slow two-model coordination.** A fast interaction model handles live dialog and hands rich context to a slower background reasoning model whose results stream back — the fast-path/slow-path pattern applied to [[LLM Inference]] (served via 200 ms streaming sessions contributed to SGLang). The interaction model is a large [[Mixture of Experts|MoE]] (276B total / 12B active) built audio/video-first.

## The shared thesis

Both sources illustrate the same principle from different layers: **adding a capability through external scaffolding creates a ceiling, with the scaffolding becoming the bottleneck.** OpenAI accepts a turn-based core and invests everything in the transport around it; Thinking Machines bets the durable win is dissolving the harness into the model. The transport problem does not disappear in the interaction-model world — continuous audio/video still needs the low-latency, reliable-connection substrate OpenAI's infrastructure provides, and long sessions strain [[Context Engineering|context management]] and [[KV Cache|attention-state memory]].

[[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]] adds LiveKit Agents as a concrete framework option for this branch: programmable real-time participants, WebRTC, turn detection, telephony, tool use, and either composed STT→LLM→TTS or direct real-time models. This is an ecosystem example rather than a comparative performance result.

## Open questions

- Do interaction models make the harness obsolete, or will the two layers co-evolve (in-model interactivity riding on relay-style transport)?
- How are long multi-hour audio/video sessions kept tractable as context accumulates every 200 ms?
- How does the 1:1 transport assumption interact with future multiparty or human-handoff interaction models?
- If ASR components inside a voice stack are benchmark-optimised, how much of a measured end-to-end quality gain is real?

## The measurement problem underneath

Both branches above optimise a stack whose accuracy is reported by public speech benchmarks — and [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]] shows those numbers cannot be taken at face value. Testing 11 open ASR models on VoxPopuli and LibriSpeech, it finds that models reproduce erroneous benchmark reference transcripts 18–30% of the time, recover deliberately silenced numbers in 30–40% of LibriSpeech cases, and select the spelling convention a given benchmark expects at rates reaching ~90% where 50% would be chance.

The mechanism is specific to this page's domain and unsettling for it: **the cue is acoustic**. A model that reproduces a benchmark's wrong transcript on the original recording produces the audio-faithful transcript for a clone of a speaker recorded after its training cutoff, and appending ordinary conversational audio or trimming benchmark context restores fidelity — while appending benchmark audio degrades it. Models can transcribe the literal words correctly and are using surrounding audio to decide **whether to follow the signal or a benchmark-specific policy**.

Worst of all for model selection, the inverse correlation: the models with the *lowest* word error rate were the most likely to reproduce reference errors. Anyone choosing an STT component for the composed STT→LLM→TTS pipeline described above should use fully held-out sets (Real World VoiceEQ, the Open ASR Leaderboard's private data, the Far-field ASR Leaderboard) rather than a single public WER number. See [[Benchmark Optimization]].

## Related pages

- [[ByteByteGo - How OpenAI Delivers Low-Latency Voice AI]]
- [[ByteByteGo - Inside Thinking Machines Interaction Models]]
- [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]]
- [[Benchmark Optimization]]
- [[Hume AI]]
- [[LLM Inference]]
- [[Mixture of Experts]]
- [[ML Systems at Scale]]
- [[Context Engineering]]
- [[OpenAI]]
- [[Thinking Machines]]
- [[AI Knowledge Base Overview]]
- [[Agent Frameworks]]
- [[Alyona Vert - 13 Frameworks and SDKs for Building AI Agents]]
