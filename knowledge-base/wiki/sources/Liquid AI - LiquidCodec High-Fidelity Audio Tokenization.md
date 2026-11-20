---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-12-liquid-ai-liquidcodec
source_title: "LiquidCodec: High-Fidelity Audio Tokenization Optimized for Speed"
source_author: "Liquid AI"
source_url: "https://www.liquid.ai/blog/liquidcodec"
tags:
  - source/summary
  - voice-ai
  - on-device
  - quantization
  - vector-quantization
source_ids:
  - src-2026-11-12-liquid-ai-liquidcodec
status: active
---

# LiquidCodec: High-Fidelity Audio Tokenization Optimized for Speed

## Summary

Liquid AI introduces **LiquidCodec**, an in-house streaming audio codec of about **74M** parameters
that sits behind its LFM3-Audio-2B and LFM3-Omni-2B models, released at the end of October. A codec
has two halves. The *tokenizer* turns audio into discrete tokens that a language model can predict,
and the *detokenizer* turns predicted tokens back into sound. Liquid AI built its own codec for two
reasons: so its speech models can predict the tokens easily, and so decoding is very fast on-device.
The main design changes are grouped finite scalar quantization (GFSQ) instead of residual vector
quantization (RVQ), a symmetric encoder and decoder with a causal encoder, and direct prediction of
spectral coefficients. In the company's tests it leads on two reconstruction metrics, ViSQOL and mel
distance, and on TTS naturalness across eight test sets. It is also much faster than three external
codecs on one CPU. Every result is first-party.

## Key claims

### Why not keep Mimi

- Liquid AI's first audio model, LFM2-Audio-1.5B, used the third-party Mimi codec, with a 1.1 kbps
  bitrate and about **96M** parameters. LFM2.5-Audio-1.5B replaced only the detokenizer and got
  **8×** faster detokenization.
- Keeping Mimi's tokenizer limited both token quality and architecture. Mimi uses RVQ, in which each
  codebook encodes the error left by the previous one. That chain creates strong sequential
  dependencies between codebooks.

### Design

- **GFSQ** rounds each feature dimension to a fixed set of values, in independent groups, and
  concatenates the results. Because codebooks are not chained the way they are in RVQ, they can be
  predicted in parallel. Liquid AI adopts MaskGIT-style iterative parallel prediction.
- The codec keeps the earlier **12.5 Hz** frame rate (one frame every **80 ms**) and models **24 kHz**
  audio. The encoder and decoder are symmetric, the encoder is fully causal, and both use LFM3
  architecture blocks. That makes the tokenizer as light as the detokenizer, which suits streaming.
- Predicting spectral coefficients directly avoids "progressive upsampling with learned transposed
  convolutions" during decoding. Liquid AI credits this choice and the edge-optimized LFM3 blocks for
  the codec's speed.

### Training

- **Stage 1:** **264,000** hours across **107** languages (web speech, audiobooks, crowd-sourced,
  parliamentary and meeting recordings), trained with waveform and spectral losses and no GAN losses.
  This left "metallic" artifacts. The team *hypothesized* the losses were "averaging out" fine
  perceptual detail.
- **Stage 2:** **55,000** hours of cleaner full-band speech (sources natively at 24 kHz or above),
  trained with adversarial critics on waveform, spectrum and speech features. The artifacts
  "gradually disappeared".
- Decoder-only quantization-aware training (QAT) prepares the decoder for low-bit edge inference.

### Evaluation setup

- The TTS comparison holds fixed the data (**101,000** hours, six languages), the architecture and
  the compute budget. Each TTS model starts from LFM3-1.7B and adds a six-layer, 1,024-dim
  autoregressive depth decoder. All codecs see identical batches in identical order, and only the
  token embeddings and output heads change. Evaluation uses no reference speech prompt and three
  seeds.
- There are eight test sets: LibriSpeech test-clean, Seed-TTS English and Mandarin, and FLEURS German,
  French, Mandarin, Japanese and Korean.

### Results (vendor-reported)

- **Reconstruction:** LiquidCodec BF16 has the best ViSQOL and lowest mel distance on all eight sets.
  On LibriSpeech, for example, ViSQOL is **4.319** against NanoCodec's **4.219**, and mel distance is
  **0.120**. NanoCodec leads PESQ and reconstruction character error rate (CER) on seven of the eight sets each;
  LiquidCodec BF16 leads PESQ only on FLEURS Korean and CER only on FLEURS German.
  Decoder QAT shrinks the decoder **3.5×** in Q4_0 "with minimal impact", and the Q4_0 build keeps the
  ViSQOL and mel-distance lead.
- **TTS:** LiquidCodec models score the highest UTMOSv2 naturalness on all eight sets. The text claims
  the best WER/CER on four of eight. Examples: LibriSpeech **3.15**, Seed-TTS English **3.50**,
  Seed-TTS Mandarin **1.19**, FLEURS German **5.30**. A Qwen3-1.7B backbone gave "consistent
  results", but no numbers are shown.
- **Speed:** measured in FP32, single-threaded, on an Apple M4 Max CPU. LiquidCodec encodes at about
  **361×** and decodes at about **87×** real time.

| Codec | Codebooks | Enc. RTF | Dec. RTF |
| --- | --- | --- | --- |
| LiquidCodec | 12 | 0.0028 | 0.0115 |
| X-Codec 2 | 1 | 0.7359 | 0.0379 |
| NanoCodec | 13 | 0.2145 | 0.2543 |
| Mimi | 12 (truncated) | 0.0361 | 0.0329 |

- **Release:** the codec is on Hugging Face and loads with Transformers. The LFM3-Audio-2B and
  LFM3-Omni-2B GGUFs include Q4_0, Q4_K_M and Q8_0 builds for llama.cpp.

## Why it matters

The codec sets both the vocabulary a speech model predicts and the final latency step before the
user hears audio. This source argues that the two goals interact. A codec that reconstructs audio
well is not automatically easy for a language model to learn. So the comparison trains TTS models on
each codec's tokens under matched conditions, rather than only measuring reconstruction. It is the
second source in the vault to replace a Mimi-family tokenizer with FSQ, after
[[Halo Research - Sopro V2 On-Device Text-to-Speech]]. It also adds a concrete small-model data point
for on-device voice: a 74M codec that decodes far faster than real time on one CPU thread.

## Tensions / open questions

- **Count mismatch.** The text claims the best WER/CER on "four out of the eight" sets. The table
  bolds a LiquidCodec row on five: BF16 on four, plus Q4_0 on FLEURS French (**5.26**, against
  BF16's **6.91**). The caption also mentions underlined second-best scores, but no underlines
  survived in the capture.
- **Quantized beats full precision on some TTS sets.** Q4_0's WER/CER is lower than BF16's on FLEURS
  French, Mandarin (**7.84** vs **8.82**) and Korean (**6.71** vs **8.36**). The post does not explain
  this. With three seeds, it may partly be noise.
- **Losses on intelligibility.** On FLEURS Mandarin and Korean, NanoCodec has the best WER/CER, and
  on FLEURS Japanese, X-Codec 2 has it.
- **Compression claim not quantified.** The codec "matches similarly sized models" in compression,
  but no LiquidCodec bitrate is stated.
- **Single-platform speed.** Speeds are FP32 on one CPU thread on one laptop. No GPU or mobile-SoC
  numbers are given, and Mimi was run truncated to 12 codebooks.
- The cause of the metallic artifacts is a hypothesis, supported only by the observation that the
  artifacts disappeared after adversarial fine-tuning. No ablation isolates the cause.

## Affected pages

- [[Neural Audio Codec]]
- [[Neural Text-to-Speech]]
- [[Real-Time Voice AI]]
- [[Liquid AI]]

## Raw capture

- [[knowledge-base/raw/sources/LiquidCodec High-Fidelity Audio Tokenization Optimized for Speed]]

## Citations

- Canonical URL: <https://www.liquid.ai/blog/liquidcodec>. A `utm_source=tldrai` tracking parameter
  was removed.
- Liquid AI Blog, published 2026-11-12 (capture `published` field); captured 2026-11-20. The in-page
  citation names "Liquid AI" as author. The acknowledgements credit Anna Piunova and Calder Katyal
  with leading research and development.
- This is a first-party vendor post. All comparisons are the company's own.

## Related pages

- [[Neural Audio Codec]]
- [[Neural Text-to-Speech]]
- [[Real-Time Voice AI]]
- [[Liquid AI]]
- [[Model Quantization and Efficiency]]
- [[Halo Research - Sopro V2 On-Device Text-to-Speech]]
- [[Liquid AI - LFM2.5-8B-A1B]]
