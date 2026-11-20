---
type: concept
created: 2026-11-20
updated: 2026-11-20
tags:
  - concept
  - speech
  - voice-ai
  - on-device
  - vector-quantization
source_ids:
  - src-2026-11-12-liquid-ai-liquidcodec
  - src-2026-08-30-halo-research-sopro-v2
status: active
---

# Neural Audio Codec

## Definition

A neural audio codec is a learned encoder-quantizer-decoder for audio. The *tokenizer* encodes a
waveform into feature vectors and quantizes them into discrete tokens. The *detokenizer* decodes
tokens, including ones predicted by a language model, back into audio. In speech-LLM and TTS stacks,
the codec defines both the target vocabulary and the last step before the user hears sound.

## Why it matters

A codec is judged twice. Reconstruction asks whether audio encoded and decoded through it sounds like
the original. Generation asks whether a language model can learn to predict its tokens. The two can
disagree, as [[Liquid AI - LiquidCodec High-Fidelity Audio Tokenization]] argues. Decode speed also
sits directly on the latency path that [[Real-Time Voice AI]] budgets for.

## Current synthesis

- **Quantizer choice shapes prediction.** In residual vector quantization (RVQ), used by Mimi, each
  codebook encodes the error left by the previous one, which chains the codebooks. Finite scalar
  quantization (FSQ), and its grouped form GFSQ, rounds each dimension independently, so codebooks
  can be predicted in parallel. LiquidCodec adopts MaskGIT-style parallel prediction for this reason.
- **Two sources moved off Mimi-family tokenizers toward FSQ.**
  [[Halo Research - Sopro V2 On-Device Text-to-Speech]] replaced a WavLM-distilled Mimi with an
  ASR-aligned FSQ tokenizer and removed a **7% WER floor**. LiquidCodec (about **74M** parameters)
  replaced Mimi (about **96M**) with GFSQ at **12.5 Hz** and **24 kHz**. Sopro also moved its acoustic
  *head* off discrete codebooks to mel-based flow matching, so the sources differ on whether the
  generation target stays discrete. See [[Flow Matching]].
- **Speed comes from architecture.** LiquidCodec predicts spectral coefficients directly, avoiding
  transposed-convolution upsampling, and uses a symmetric encoder and decoder with a causal encoder. It
  reports about **361×** real-time encoding and **87×** decoding in FP32 on one M4 Max CPU thread.
  Mimi was run truncated to 12 codebooks in that comparison, and no GPU or mobile numbers are given.
- **Evaluate generation under matched training.** LiquidCodec trains a TTS model on each codec with
  identical data, batches and compute, and scores each over three generation seeds. It reports the
  highest UTMOSv2 on all eight test sets but not the best WER everywhere: NanoCodec and X-Codec 2
  win some languages. The text claims the best WER/CER on four of eight, while its table bolds a
  LiquidCodec row on five.
- **Codecs quantize too.** Decoder-only QAT shrank LiquidCodec's decoder **3.5×** in Q4_0 "with
  minimal impact". See [[Model Quantization and Efficiency]].

All results are first-party.

## Open questions

- Is token predictability a stable property of a codec, or does it depend on the backbone and the
  amount of data? LiquidCodec says a Qwen3 backbone gave "consistent results" but shows no numbers.
- Should generation targets stay discrete (LiquidCodec) or move to continuous heads (Sopro V2)?
- Which reconstruction metrics track human preference? ViSQOL, mel distance and PESQ crown different
  codecs on the same sets.
- Why does LiquidCodec's Q4_0 build beat its BF16 build on TTS WER/CER for FLEURS French, Mandarin and
  Korean? The post does not explain it, and with three seeds it may partly be noise.
- What bitrate does LiquidCodec run at? It is said to match "similarly sized models" in compression,
  but no bitrate is stated, while Mimi's is given as 1.1 kbps.

## Related pages

- [[Neural Text-to-Speech]]
- [[Real-Time Voice AI]]
- [[Model Quantization and Efficiency]]
- [[Flow Matching]]
- [[Liquid AI]]
- [[Liquid AI - LiquidCodec High-Fidelity Audio Tokenization]]
- [[Halo Research - Sopro V2 On-Device Text-to-Speech]]
