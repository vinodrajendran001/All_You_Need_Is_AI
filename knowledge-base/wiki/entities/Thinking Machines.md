---
type: entity
created: 2026-07-03
updated: 2026-11-20
entity_kind: organization
tags:
  - entity
  - organization
  - research-lab
  - voice-ai
  - human-ai-collaboration
  - training
  - quantization
  - inference
  - determinism
source_ids:
  - src-2026-07-03-bytebytego-thinking-machines-interaction
  - src-2026-08-19-bytebytego-inkling
  - src-2026-11-06-nous-arete-27b
  - src-2026-11-13-thinking-machines-end-to-end-4-bit-training
  - src-2026-11-12-nathan-barry-detllm-integer-inference
status: active
---

# Thinking Machines

## What it is

Thinking Machines is a relatively new AI research lab focused on human-AI collaboration. It publishes research under the name **Connectionism** and offers developer-facing products. Its distinguishing bet is that most labs over-index on *autonomous* capability (a model that takes a task and returns a result alone), while real work benefits from continuous, interruptive collaboration where the human clarifies and redirects as the model goes.

## Why it matters here

Thinking Machines is the subject of [[ByteByteGo - Inside Thinking Machines Interaction Models]] and the source of the vault's **interaction model** thesis: real-time voice AI built from turn-based models plus helper harnesses has a ceiling, and the way past it is to move interactivity inside the model. Its **TML-Interaction-Small** (276B-parameter [[Mixture of Experts|MoE]], 12B active) demonstrates **time-aligned micro-turns** and **fast/slow two-model coordination**, forming the model-architecture half of the [[Real-Time Voice AI]] concept. It also contributed a streaming-session feature to open-source SGLang, touching [[LLM Inference]].

Two later sources add a training and numerics side to that profile. A first-party post describes a
4-bit training recipe for its own Inkling 2 Small, and a third-party post credits the lab with a
widely cited diagnosis of inference nondeterminism. See [[Low-Precision Training]] and
[[Inference Determinism]].

## Notes

- Built its own benchmarks (TimeSpeak, CueSpeak, RepCount-A, ProactiveVideoQA) because existing voice benchmarks miss proactive, time-aware, and visual behaviours.
- Explicitly grounds its design philosophy in Rich Sutton's "Bitter Lesson."
- [[ByteByteGo - The New American AI Model Designed to Be Customized]] adds Inkling, a 952B stored-parameter sparse MoE positioned for adaptation with mixed local/global attention and an exposed reasoning-effort control. These architecture details remain publication- and company-reported.
- [[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]] used Inkling as the teacher for Arete-27B, calling it "the best open model with a positive eval on what we were targeting". On Nous's 803-prompt evaluation, judged by Grok 4.7, Inkling has the highest fact score in the table (**3.96** of 5) and ties Mistral Large 4 for the lowest rate of answers adopting the official line (**0.3%**). The capture does not name Inkling's maker; the link to Thinking Machines rests on the ByteByteGo summary above. It is one judge on one evaluation, built by the downstream user.
- [[Thinking Machines - End-to-End 4-Bit Training]] (Jack Cook and the lab, Connectionism, Nov 13,
  2026) is the vault's first first-party Thinking Machines training document. It describes
  **Inkling 2 Small**, a lab-trained MoE, pretrained in **68 hours** on GB300 NVL72 racks with NVFP4
  expert forward passes, MXFP8 backward passes and quantized expert-parallel communication. It also
  describes a kernel stack, BBBK, as "fully deterministic", and says per-token outer scales give
  "batch-invariance". Reported results in its largest jobs are an **8%** pretraining and **20%** RL
  speedup over full MXFP8, at about **2%** compute-efficiency cost in pretraining and no discernible
  reward difference in RL. The post confirms the lab trains a model in the Inkling line. That
  supports, but does not settle, the attribution of "Inkling" in the Nous Arete note above, since
  that capture does not name a variant. See [[Low-Precision Training]].
- [[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]] credits
  Thinking Machines (Horace He et al., *Defeating Nondeterminism in LLM Inference*, 2025) with the
  diagnosis of why temperature-0 decoding is not deterministic: sending one prompt 1,000 times gave
  **80** different answers, because kernel choice and reduction order depend on batch size. Their fix,
  **batch-invariant kernels**, reportedly made all 1,000 completions identical "at about a 20% matmul
  slowdown", and Barry relays their argument that a bitwise-identical sampler and trainer makes RL
  truly on-policy. The vault previously carried the ~80-completions figure on [[LLM Inference]] and
  [[Multi-Turn Evaluation]] without this attribution; this is its likely origin. All of it is
  secondhand through Barry; the original post is not in the vault. See [[Inference Determinism]].

## Related pages

- [[ByteByteGo - Inside Thinking Machines Interaction Models]]
- [[Real-Time Voice AI]]
- [[LLM Inference]]
- [[Mixture of Experts]]
- [[AI Knowledge Base Overview]]
- [[ByteByteGo - The New American AI Model Designed to Be Customized]]
- [[Open Model Ecosystems]]
- [[Nous Research - Introducing Arete-27B - Qwen3.8-27B Post-Trained to Reinforce Western Values]]
- [[Low-Precision Training]]
- [[Inference Determinism]]
- [[Thinking Machines - End-to-End 4-Bit Training]]
- [[Nathan Barry - Eliminating Nondeterminism in LLM Inference with Integer-Only Arithmetic]]
- [[Model Quantization and Efficiency]]
- [[Distributed Training Parallelism]]
- [[LLM Training Pipeline]]
