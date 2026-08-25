---
type: entity
created: 2026-08-25
updated: 2026-08-25
entity_kind: organization
tags:
  - entity
  - organization
  - voice-ai
  - evaluation
  - speech
source_ids:
  - src-2026-08-21-hume-ai-asr-benchmark-optimization
status: active
---

# Hume AI

## What it is

A voice AI research company whose vault contribution is evaluation methodology rather than models: it builds benchmarks and probes for measuring how speech systems behave under real-world conditions.

## Why it matters here

Hume AI is the vault's example of an organisation that treats **measurement itself as the research contribution**. [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]], written with [[Hugging Face]], converts "benchmaxxing" from a widely shared suspicion into three reproducible probes — consensus disagreement, masked entity retrieval, and orthographic switching — with controls (post-cutoff fresh recordings, same-speaker voice clones, silenced spans, phonetically neutral spelling pairs) designed to separate genuine capability from benchmark-specific behaviour.

The result that matters beyond speech: models appear to use surrounding acoustic context to **identify which benchmark they are being tested on** and then apply that benchmark's transcription policy even when it contradicts the audio, and the models with the lowest word error rate were the most likely to do so. That is a general warning about leaderboard rank order, not a speech-specific curiosity. See [[Benchmark Optimization]].

Hume also maintains Real World VoiceEQ, one of the held-out evaluations the paper recommends over single public-benchmark scores — relevant to [[Real-Time Voice AI]], where the vault's other sources optimise latency and interaction quality without addressing whether the underlying transcription numbers are trustworthy.

## Notes

- The probe design is the transferable asset: construct inputs where the benchmark's answer and the correct answer disagree, then see which one the model produces.
- Evidence is limited to 11 open-source ASR models on VoxPopuli and LibriSpeech; closed frontier systems were not tested.

## Related pages

- [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]]
- [[Benchmark Optimization]]
- [[Real-Time Voice AI]]
- [[Multi-Turn Evaluation]]
- [[Hugging Face]]
- [[AI Knowledge Base Overview]]
