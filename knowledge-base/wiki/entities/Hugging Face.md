---
type: entity
created: 2026-08-25
updated: 2026-11-13
entity_kind: organization
tags:
  - entity
  - organization
  - open-models
  - platform
  - evaluation
source_ids:
  - src-2026-08-21-hume-ai-asr-benchmark-optimization
  - src-2026-08-18-hugging-face-state-open-models-summer-2026
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-11-05-huggingface-moe-training-handbook
  - src-2026-11-11-pytorch-executorch-webgpu
status: active
---

# Hugging Face

## What it is

The dominant open model and dataset hub, and increasingly a publisher of ecosystem research and leaderboards in its own right.

## Why it matters here

Hugging Face plays two distinct roles in this vault, and they pull in interesting directions.

**As infrastructure**, it is the substrate almost every open-model source assumes. Model cards, config files, and dataset pages are the citations used throughout — [[Changyi Yang - Why MLA and MTP Fight Each Other]] reads head counts straight out of `config.json` files on the hub to ground its arithmetic, and [[Open Model Ecosystems]] is largely a description of activity that happens there.

**As a measurement authority**, it operates the leaderboards that decide what "state of the art" means for open models — which makes [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]] notable. Rather than defending its leaderboard, Hugging Face co-authored the work showing that leading ASR models reproduce benchmark reference errors and detect which benchmark they are being tested on, then shipped the findings back into the product as a "Benchmark fitting" tab on the Open ASR Leaderboard with open-sourced scripts and un-normalised outputs. It also maintains the held-out private-data evaluations that the paper recommends as the remedy.

That combination — hosting the models, hosting the benchmarks, and publishing evidence that the benchmarks are being gamed — is what makes it a useful node rather than just a URL prefix. See [[Benchmark Optimization]].

## Notes

- [[Hugging Face - State of Open Models Summer 2026]] is the vault's ecosystem-survey source; its rankings inherit whatever measurement error [[Benchmark Optimization]] describes.
- Relevant properties: the Open ASR Leaderboard, the Far-field ASR Leaderboard, and the hosting of Real World VoiceEQ.

## The checkpoint format as an inter-stage interface

[[IBM Granite Team - Granite 4.2 LLMs How They're Built]] shows a role for the Hugging Face format
beyond distribution. In Granite's staged RL pipeline, each stage **exports its policy to Hugging Face
format when it finishes**, and that export becomes the base model for the next stage — with
Megatron-Bridge converting between Megatron and HF representations at every boundary.

The HF format is functioning here as an internal interchange standard inside a training pipeline, not
just as the way a finished model reaches the public. That is a quieter form of infrastructural
influence than the Hub: a serialization format that has become neutral enough that a team will
round-trip through it repeatedly during training, accepting conversion cost in exchange for clean,
inspectable, resumable stage boundaries.

The Granite 4.2 build report was itself published as a Hugging Face blog post rather than an arXiv
paper or a corporate release, which is the pattern several open-weight releases in this vault
follow.

## A training handbook published on the company's own platform

[[Nouamane Tazi et al - The Ultimate MoE Training Handbook]] follows the same pattern at book
length. Hugging Face researchers published it as a Space, presented as the sequel to their Smol
Training Playbook, which covered a dense model, and it links to the Ultrascale Playbook for each
parallelism technique. The handbook also sends readers to the company's own tools. Trackio,
Hugging Face's open-source experiment tracker, has an API that mirrors `wandb` and logs to a local
database that can be synced to a Space. Hugging Face Jobs runs a Docker image and a command on
Hugging Face's machines, billed by the minute; among its largest options is `h200x8`, eight H200s
of 141 GB each, and a job stops after 30 minutes unless a different timeout is set. The training
commands themselves are built on NVIDIA's Megatron-LM at a pinned commit, so the platform supplies
publishing, tracking and rented hardware rather than the training framework. See
[[Mixture of Experts]].

## Compiled artifacts from another framework

[[PyTorch - ExecuTorch WebGPU - PyTorch Models on the GPU, in the Browser]] shows the Hub carrying
artifacts that are not in Hugging Face's own format. ExecuTorch's browser-ready models are published
as `.pte` files in `executorch-community` repositories, each with a model card and the exact export
recipe. The infrastructure role described above therefore extends from checkpoints to compiled
runtime files for [[PyTorch]]'s ExecuTorch runtime. See [[On-Device Reasoning]].

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[IBM]]
- [[Hugging Face - State of Open Models Summer 2026]]
- [[Hume AI - Measuring Benchmark Optimization in Speech Recognition]]
- [[Benchmark Optimization]]
- [[Open Model Ecosystems]]
- [[Real-Time Voice AI]]
- [[Hume AI]]
- [[AI Knowledge Base Overview]]
- [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]]
- [[PyTorch - ExecuTorch WebGPU - PyTorch Models on the GPU, in the Browser]]
- [[Mixture of Experts]]
- [[PyTorch]]
- [[On-Device Reasoning]]
