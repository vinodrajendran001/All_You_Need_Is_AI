---
type: concept
created: 2026-08-30
updated: 2026-09-04
tags:
  - concept
  - speech
  - on-device
  - open-models
source_ids:
  - src-2026-08-30-halo-research-sopro-v2
  - src-2026-08-31-docmilanfar-lagrangian-flow-matching
status: active
---

# Neural Text-to-Speech

## Definition

Neural text-to-speech (TTS) converts text into a waveform using learned models, typically in three
stages: a text encoder, an acoustic model that predicts an intermediate audio representation such as
a mel spectrogram, and a vocoder that renders that representation as audio. Voice cloning conditions
the acoustic stage on a short reference sample of a target speaker.

## Why it matters

TTS is the output half of any voice interface, and it is where the latency budget in
[[Real-Time Voice AI]] is usually spent. It is also one of the clearest cases where a small,
locally-run model is genuinely competitive with a hosted one — which makes privacy and offline
operation available rather than aspirational.

## Current synthesis

### A modern small TTS stack, component by component

[[Halo Research - Sopro V2 On-Device Text-to-Speech]] documents a 120M-parameter open voice-cloning
model and, unusually, records what was *replaced* and why.

| Component | Earlier choice | Replacement | Reason |
| --- | --- | --- | --- |
| Text vocabulary | Llama 128k | SentencePiece 8,192 | The Llama vocabulary consumed ~49M parameters — roughly 40% of V1's budget — on embeddings a TTS model does not need |
| Backbone | Convolutional | Transformer decoder | Long-range consistency |
| Acoustic head | Discrete codebooks | Mel-based flow matching | A continuous target avoids codebook quantization artifacts |
| Speech tokenizer | WavLM-distilled Mimi | ASR-aligned FSQ warm-started from Whisper large-v3 | Removed a **7% WER floor** imposed by the distilled tokenizer |
| Vocoder | — | Vocos, plus a causal 3-frame-lookahead variant | Streaming with bounded latency |

The vocabulary finding is the sharpest lesson for small models generally: inheriting an LLM's
tokenizer can spend half the parameter budget on capability the task does not use. See
[[Small Language Models]].

### Training recipe: teacher, preference optimization, distillation, reflow

1. Train a **0.5B teacher**.
2. Run **three rounds of DPO**. GRPO **destabilized the model**, so preference optimization was used
   instead — a data point against [[Group Relative Policy Optimization]] in continuous-output domains,
   though the mechanism is not diagnosed.
3. **Distil to 120M.** The student was reported as **more stable than its teacher**, which cuts
   against the usual assumption that distillation only loses.
4. **Reflow the flow-matching solver from 32 steps to 2** — a **16x speedup with no measurable
   quality loss**.

The reflow step is the structural analogue of the token-budget reductions in
[[Reasoning Effort Control]]: a large inference saving obtained entirely during training, by changing
what the model needs to compute rather than how fast it computes.

### Performance and the limits of the quality claim

Reported: **0.24 real-time factor on an M3 CPU** offline, **~300 ms time-to-first-audio** streaming,
**0.07 RTF on an H100**. On Seed-TTS test-en the model **beats ground-truth WER** — synthesized speech
transcribed more accurately than the original human recordings.

That last number is easy to over-read. Beating ground-truth WER reflects clarity *and* the noisiness
of the reference audio; it says nothing about naturalness or speaker fidelity, which WER cannot
measure. The vault's [[Real-Time Voice AI]] page already records that voice quality lacks a good
single metric, and this is the same gap seen from the synthesis side.

### The watermarking refusal

Sopro V2 ships **no watermark, deliberately**. The argument: in an open pipeline a watermark is
trivially removable, so shipping one provides **false safety** rather than real provenance. This is an
honest position and worth recording as such — but it leaves voice-cloning misuse entirely
unaddressed, and the source offers no alternative mitigation.

## Why flow-matching vocoders can take few steps

This page records flow-matching vocoders reaching acceptable quality in very few solver steps, which is what makes
streaming synthesis viable at all. [[@docmilanfar - A Lagrangian View of Flow Matching]] explains the mechanism.

In standard diffusion the sampling path curves, so the denoiser's estimate of the clean output shifts every step
and the solver must take tiny ones. Flow matching forces **straight trajectories**, which makes the target static
and lets the solver take large strides — and the straightness is not a convenience but the solution of the
governing advection PDE, so the speedup is structural rather than incidental.

It also explains why baseline flow matching alone is not enough for the lowest step counts. Independently drawn
straight paths **cross** in high dimensions, and a crossing forces the model to average conflicting targets,
bending the flow and restoring the need for tens of steps. Reflow removes the crossings, driving the posterior
covariance toward zero — which is why the fastest vocoders are typically reflowed or distilled rather than plain
flow-matching models. For real-time speech, where sequential solver steps are latency that cannot be batched
away, that is the difference between shipping and not. See [[Flow Matching]].

## Open questions

- What metric should replace WER for TTS quality? Naturalness and speaker fidelity are the properties
  that matter and neither is captured.
- Why did GRPO destabilize training where DPO worked? If this generalizes to continuous-output
  domains it matters well beyond speech.
- Why was the distilled student more stable than its teacher? If distillation is acting as a
  regularizer, that is a general result being reported as an aside.
- Is there any provenance mechanism for open-weight voice cloning that is not trivially defeated?
- How do these latency figures hold up across device thermal states and longer utterances? Single
  configuration numbers with no variance are reported.

## Related pages

- [[Real-Time Voice AI]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[Knowledge Distillation]]
- [[Diffusion Models]]
- [[Direct Preference Optimization]]
- [[Model Quantization and Efficiency]]
- [[Open Model Ecosystems]]
- [[Halo Research - Sopro V2 On-Device Text-to-Speech]]
- [[Flow Matching]]
- [[@docmilanfar - A Lagrangian View of Flow Matching]]
- [[@docmilanfar]]
