---
type: source-summary
created: 2026-08-30
updated: 2026-10-07
source_id: src-2026-08-30-halo-research-sopro-v2
source_title: "Sopro V2: private, fast, on-device text-to-speech"
source_author: "Halo Research (Halo NeuroAI)"
source_url: "https://research.haloneuro.ai/posts/sopro-v2"
tags:
  - source/summary
  - speech
  - on-device
  - open-models
source_ids:
  - src-2026-08-30-halo-research-sopro-v2
status: active
---

# Halo Research - Sopro V2 On-Device Text-to-Speech

## Summary

An engineering write-up for the Sopro V2 family, including the open **120M-parameter Sopro V2
Turbo** voice-cloning model. Reported Turbo performance: **0.24 real-time factor on an M3 CPU**
offline, **~300 ms time-to-first-audio on M3** streaming, and **0.07 RTF on an H100 offline**.
These are **single-stream PyTorch runs at default settings, without batching**. The stated motivation is
personal and unusual — European Portuguese is poorly served by hosted TTS — which shapes the design
toward small, open, and locally runnable rather than maximally capable.

The post is most valuable as a record of what was *replaced* between V1 and V2, and why.

## Key claims

**Every major component was swapped, each for a specific reason.**

| Component | V1 | V2 | Reason |
| --- | --- | --- | --- |
| Tokenizer vocab | Llama 128k | SentencePiece 8,192 | The 384-dimensional Llama embedding table consumed ~49M parameters; the smaller vocabulary reduces that overhead |
| Backbone | Convolutional | Transformer decoder | Better long-range consistency |
| Acoustic head | Discrete codebooks | Mel-based flow matching | Continuous target avoids codebook quantization artifacts |
| Speech tokenizer | WavLM-distilled Mimi | ASR-aligned FSQ, warm-started from Whisper large-v3 | Fixed a **7% WER floor** that the distilled tokenizer imposed |
| Vocoder | — | Vocos, plus a causal 3-frame-lookahead variant | Streaming with bounded latency |

**Training sequence: teacher, preference optimization, distillation, reflow.** Train a 0.5B teacher;
run **three rounds of DPO** (the post notes **GRPO destabilized the model**, so DPO was used
instead); distill to the 120M student — which was **more stable than its teacher**; then **reflow the
flow-matching solver from 32 steps to 2**. The authors report a **16x speedup of the acoustic
head**, with near-parity in quality, similarity, and intelligibility. This is not a 16x
end-to-end TTS result, and the flow-matching head is separate from the Vocos vocoder.

**Quality claim:** on Seed-TTS test-en, Sopro V2 **beats ground-truth WER** — that is, the
synthesized speech is transcribed more accurately than the original human recordings, which reflects
both model clarity and the noisiness of the reference audio.

**No watermarking, deliberately.** The authors argue that in an open pipeline a watermark is trivially
removable, so shipping one would provide **false safety** rather than real provenance.

## Why it matters

This is the vault's first end-to-end account of a modern TTS stack, and it lands on the same theme as
the [[Small Language Models]] and [[On-Device Reasoning]] material: capability at the edge can come
from reducing components sized for a different problem. The 49M-parameter embedding table is the
concrete example; it should not be divided by the later 120M Turbo total to invent a V1 percentage.

Two training details generalize beyond speech. **The distilled student being more stable than its
teacher** is a counterexample to the assumption that distillation only loses; and **reflow cutting
acoustic solver steps from 32 to two** is a reported subsystem saving obtained during training.
The authors' quality-parity claim is not a matched end-to-end ablation. This is structurally
similar to the token-budget reductions in
[[Sebastian Raschka - Controlling Reasoning Effort in LLMs]].

The watermarking refusal is an honest position worth recording: it trades a visible safety artifact
for not misleading downstream users about provenance guarantees.

## Tensions / open questions

- "Beats ground-truth WER" is a statement about the test set as much as the model; it does not
  establish naturalness or speaker fidelity, which WER cannot measure.
- GRPO destabilizing the model where DPO worked is reported without diagnosis. This is a data point
  against GRPO in continuous-output domains, but the mechanism is unexplained.
- The student being more stable than the teacher is asserted, not analysed. If distillation is acting
  as a regularizer here, it would matter well beyond speech.
- The no-watermark argument is sound for open weights but leaves voice-cloning misuse entirely
  unaddressed; the post offers no alternative mitigation.
- Latency numbers are single-configuration reports without variance or a comparison baseline.
- The published tables compare a **0.5B, 32-step base model** with **120M, two-step Turbo**,
  changing size and training as well as step count. For example, Seed-TTS test-en WER improves
  **1.77 to 1.65** while similarity changes **0.685 to 0.651**. Those rows cannot isolate
  reflow's effect or establish universal quality parity; retain the near-parity statement as
  the authors' claim about the reflow stage.

## Affected pages

- [[Neural Text-to-Speech]]
- [[Real-Time Voice AI]]
- [[Small Language Models]]
- [[On-Device Reasoning]]
- [[Flow Matching]]

## Citations

- Raw capture: [[2026-08-30 Halo Research - Sopro V2 - private, fast, on-device text-to-speech]]
- Original: <https://research.haloneuro.ai/posts/sopro-v2>

## Related pages

- [[Knowledge Distillation]]
- [[Direct Preference Optimization]]
- [[Diffusion Models]]
- [[Model Quantization and Efficiency]]
- [[Open Model Ecosystems]]
- [[Group Relative Policy Optimization]]
