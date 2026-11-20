---
type: entity
created: 2026-06-03
updated: 2026-11-20
entity_kind: organization
tags:
  - entity
  - organization
  - llm
  - on-device
  - voice-ai
  - speech
source_ids:
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-08-20-liquid-ai-production-loops
  - src-2026-11-12-liquid-ai-liquidcodec
status: active
---

# Liquid AI

## What it is

AI company and model provider whose material in this vault focuses on sparse, on-device language models built for local/private assistants and fast tool calling.

## Why it matters here

Liquid AI matters because it adds a deployment-first perspective to the vault's LLM branch. Its source is not mainly about frontier-scale training; it is about making sparse MoE assistants practical on consumer hardware through runtime support, tokenizer efficiency, and targeted post-training.

## Notes

- The current source in the vault is [[Liquid AI - LFM2.5-8B-A1B]].
- [[Liquid AI - Designing Loops for Production-Grade Work]] adds a coding-agent experiment where real datasets and an external acceptance harness exposed requirements absent from the initial specification.
- In this knowledge base, Liquid AI mainly strengthens the overlap between efficiency, sparse architectures, and local/private agent deployment.
- The Localcowork demo is useful because it connects model architecture to a concrete MCP-heavy tool workflow rather than stopping at benchmark tables.
- [[Liquid AI - LiquidCodec High-Fidelity Audio Tokenization]] extends Liquid AI's on-device focus to
  audio. LiquidCodec is an in-house codec of about **74M** parameters, built from LFM3 blocks, that
  powers LFM3-Audio-2B and LFM3-Omni-2B. It replaces the third-party Mimi tokenizer used in
  LFM2-Audio-1.5B. LFM2.5-Audio-1.5B had already replaced Mimi's detokenizer for **8×** faster
  detokenization. Training ran on **264,000** hours in **107** languages, then **55,000** hours of
  clean full-band speech with adversarial critics, plus decoder-only QAT. The company reports about
  **87×** real-time decoding on one CPU thread, and GGUF builds (Q4_0, Q4_K_M, Q8_0) of LFM3-Audio-2B
  and LFM3-Omni-2B for llama.cpp. All results are first-party. See [[Neural Audio Codec]].

## Related pages

- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Mixture of Experts]]
- [[Model Quantization and Efficiency]]
- [[AI Agents in Production]]
- [[AI Knowledge Base Overview]]
- [[Liquid AI - Designing Loops for Production-Grade Work]]
- [[Loop Engineering]]
- [[Neural Audio Codec]]
- [[Liquid AI - LiquidCodec High-Fidelity Audio Tokenization]]
- [[Neural Text-to-Speech]]
- [[Real-Time Voice AI]]
