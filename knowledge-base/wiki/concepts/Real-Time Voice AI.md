---
type: concept
created: 2026-07-03
updated: 2026-11-20
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
  - src-2026-08-30-halo-research-sopro-v2
  - src-2026-09-22-bytebytego-openai-gpt-live
  - src-2026-08-12-alyona-vert-agent-frameworks-sdks
  - src-2026-11-12-liquid-ai-liquidcodec
  - src-2026-11-17-paul-kinlan-voice-harness
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

## The measurement problem underneath

Both branches above optimise a stack whose accuracy is reported by public speech benchmarks — and [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]] shows those numbers cannot be taken at face value. Testing 11 open ASR models on VoxPopuli and LibriSpeech, it finds that models reproduce erroneous benchmark reference transcripts 18–30% of the time, recover deliberately silenced numbers in 30–40% of LibriSpeech cases, and select the spelling convention a given benchmark expects at rates reaching ~90% where 50% would be chance.

The mechanism is specific to this page's domain and unsettling for it: **the cue is acoustic**. A model that reproduces a benchmark's wrong transcript on the original recording produces the audio-faithful transcript for a clone of a speaker recorded after its training cutoff, and appending ordinary conversational audio or trimming benchmark context restores fidelity — while appending benchmark audio degrades it. Models can transcribe the literal words correctly and are using surrounding audio to decide **whether to follow the signal or a benchmark-specific policy**.

Worst of all for model selection, the inverse correlation: the models with the *lowest* word error rate were the most likely to reproduce reference errors. Anyone choosing an STT component for the composed STT→LLM→TTS pipeline described above should use fully held-out sets (Real World VoiceEQ, the Open ASR Leaderboard's private data, the Far-field ASR Leaderboard) rather than a single public WER number. See [[Benchmark Optimization]].

## The synthesis side: small, local, and fast enough

[[Halo Research - Sopro V2 On-Device Text-to-Speech]] documents a **120M-parameter open voice-cloning
TTS** model that runs locally: **0.24 real-time factor on an M3 CPU** offline, **~300 ms
time-to-first-audio on M3** streaming, and **0.07 RTF on an H100 offline**. These are
**single-stream PyTorch runs at default settings, without batching**. A Vocos variant with
**causal three-frame lookahead** bounds the vocoder's future context; it does not by itself
determine the latency of the entire autoregressive/acoustic/vocoder pipeline.

That changes the shape of this page's latency argument. Where the vault's hosted voice-agent sources
treat network round-trips as a fixed cost to be engineered around, an on-device synthesizer removes
that leg entirely — and with it the privacy exposure of shipping voice to a server. See
[[Neural Text-to-Speech]] for the architecture and training recipe.

The measurement problem this page already records reappears from the synthesis side. Sopro V2 **beats
ground-truth WER** on Seed-TTS test-en — synthesized speech transcribed more accurately than the
original human recordings. That is a real result and also a trap: it reflects clarity *and* the
noisiness of the reference audio, while saying nothing about naturalness or speaker fidelity, which
WER cannot measure.

One governance note belongs here too. Sopro V2 ships **no watermark, deliberately** — the authors
argue that in an open pipeline a watermark is trivially removable and so provides false safety. Voice
cloning that runs offline on a laptop has no provenance mechanism at all, which is the unresolved cost
of moving this capability to the edge.

The codec is the last step on the synthesis side's latency path.
[[Liquid AI - LiquidCodec High-Fidelity Audio Tokenization]] reports a **74M**-parameter streaming
codec, behind LFM3-Audio-2B and LFM3-Omni-2B, that encodes at about **361×** and decodes at about
**87×** real time. It was measured in FP32 on a single CPU thread of an Apple M4 Max. Decode RTF is
**0.0115**, against **0.0329** for Mimi, **0.0379** for X-Codec 2 and **0.2543** for NanoCodec. The
design choices behind this are a fully causal encoder, a symmetric decoder, **12.5 Hz** frames
(**80 ms**), and direct prediction of spectral coefficients. A Q4_0 decoder build is **3.5×**
smaller "with minimal impact". These are vendor numbers from one laptop, single-stream. Like Sopro
V2's figures above, they cover one component, not end-to-end time-to-first-audio. See
[[Neural Audio Codec]].

## Full duplex needs two serving clocks

[[ByteByteGo - How OpenAI Built GPT-Live]] describes a continuously listening and speaking model
whose live path remains isolated from slower reasoning and tools. Warm handoff preserves session
state across instance changes, while WARP reportedly compresses WebRTC setup from six round trips to
one. These are secondary vendor-reported mechanisms without a public latency or reliability dataset.

## A live voice model in front of a general agent harness

[[Paul Kinlan - My Voice Harness Is My New Operating System]] uses a live voice model as the front
end of a general agent harness rather than as a conversational product. Voicebox has a browser page
as its interface, a local Node daemon that runs the agent loop, holds the API key, and executes every
tool call, and Gemini-3.8-live in the cloud, which Kinlan calls "a game-changer" because it responds
quickly, can be interrupted, and can write code. The model also takes screen-share video, so the
harness can co-work on what is on screen. He reports UI issues and a bug in continuous screen capture.

The problems this page tracks, transport and latency, are not the ones he dwells on. His are
authority (what a spoken request may cause on his machine) and cost: "this project can be pretty
expensive to run". He lists real-time **local** speech models as missing from the web platform, for
privacy and cost, which ties to the local-synthesis section above. It is a single-developer prototype
with no latency or reliability figures. See [[Coding Agent Harness]] and
[[Agent Security and Governance]].

## Open questions

- Do interaction models make the harness obsolete, or will the two layers co-evolve (in-model interactivity riding on relay-style transport)?
- How are long multi-hour audio/video sessions kept tractable as context accumulates every 200 ms?
- How does the 1:1 transport assumption interact with future multiparty or human-handoff interaction models?
- If ASR components inside a voice stack are benchmark-optimised, how much of a measured end-to-end quality gain is real?
- How should a voice-first agent confirm consequential tool calls without falling back to a
  screen-and-click step? Kinlan names per-action confirmation as the usual answer and has not worked
  out how to do it by voice.

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
- [[Neural Text-to-Speech]]
- [[On-Device Reasoning]]
- [[Small Language Models]]
- [[Halo Research - Sopro V2 On-Device Text-to-Speech]]
- [[Neural Audio Codec]]
- [[Liquid AI - LiquidCodec High-Fidelity Audio Tokenization]]
- [[Liquid AI]]
- [[Paul Kinlan - My Voice Harness Is My New Operating System]]
- [[Paul Kinlan]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
