---
type: concept
created: 2026-06-04
updated: 2026-11-13
tags:
  - concept
  - llm
  - edge-ai
  - reasoning
  - deployment
source_ids:
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-06-04-efficient-reasoning-edge
  - src-2026-06-04-progressive-thought-encoding
  - src-2026-06-04-pace-efficient-reasoning
  - src-2026-06-04-extreme-ratio-cot-compression
  - src-2026-06-04-reasoncache
  - src-2026-06-04-difficulty-aware-entropy-regularization
  - src-2026-06-04-conpress
  - src-2026-06-04-dss-grpo-cot-compression
  - src-2026-06-17-prateek-singh-kv-cache-turboquant
  - src-2026-06-24-bytebytego-llm-vs-slm
  - src-2026-07-03-sebastian-raschka-local-coding-agents
  - src-2026-06-30-onur-sirin-local-llm-memory-hardware
  - src-2026-08-30-halo-research-sopro-v2
  - src-2026-10-27-bytebytego-apple-on-device
  - src-2026-11-11-pytorch-executorch-webgpu
status: active
---

# On-Device Reasoning

## Definition

On-device reasoning is the deployment of reasoning-capable language models directly on end-user hardware such as phones, laptops, or embedded devices under strict memory, latency, power, and privacy constraints.

## Why it matters

Reasoning is especially hard to bring to the edge because the same mechanisms that improve hard-task accuracy—explicit chain-of-thought, longer outputs, multiple test-time samples, larger KV caches—also amplify the exact costs that mobile hardware cannot hide.

## Current synthesis

- [[Liquid AI - LFM2.5-8B-A1B]] frames on-device assistants as an **architecture and runtime** problem. Sparse MoE design, multilingual tokenization efficiency, and broad runtime support are used to make local tool-calling assistants feel interactive on consumer hardware.
- [[Efficient Reasoning on the Edge]] frames the same deployment space as a **compute-control and systems-co-design** problem. Instead of changing the whole model family, it keeps a reusable base model and layers on LoRA reasoning adapters, budget-forced RL, dynamic routing, verifier-guided parallel test-time scaling, and quantization-aware training.
- Together, the two sources suggest that on-device reasoning is not one trick. It is a stack of controls:
  - activate expensive reasoning only when needed,
  - keep reasoning traces short,
  - reuse intermediate state such as KV caches,
  - quantize aggressively without destabilizing post-training,
  - and preserve privacy plus low latency by staying local.
- This also changes what "efficient reasoning" means. On-device settings care about **time-to-first-token, memory movement, battery/power, and bounded response length**, not just benchmark accuracy or theoretical FLOPs.
- The branch highlights two complementary strategies:
  - **Sparse activation** (Liquid AI) reduces active compute per token.
  - **Modular reasoning adapters plus routing** (Qualcomm) reduce how often explicit reasoning mode is invoked and how verbose it becomes when active.
- The newer compression papers broaden this page beyond explicitly mobile deployment. They suggest that token budget, cache size, and visible chain-of-thought length are becoming general optimisation targets across reasoning research, with on-device deployment acting as one especially demanding case. See [[Reasoning Compression]].
- A deeper lesson is that explicit reasoning itself is a deployment liability. The system must actively manage when to think, how long to think, and whether more test-time compute is worth the extra memory and latency.
- [[Prateek Singh - KV Cache and TurboQuant]] adds the long-context memory version of this lesson. On edge or single-GPU deployments, KV cache can become the limiting resource even before model weights or arithmetic do. This makes [[KV Cache]] optimization (GQA/MQA/MLA, PagedAttention, eviction, predictive skipping, and KV quantization such as TurboQuant) directly relevant to local assistants and long-context private agents.
- [[ByteByteGo - Large Language Models vs Small Language Models]] gives the device-model perspective. On-device systems are designed around single-digit gigabytes of memory, battery, thermal limits, and millisecond-scale latency. That pushes models toward [[Small Language Models]], quantization, grouped-query attention, sliding windows, hardware-specific mapping, and hybrid patterns where small local models handle common work while larger server models handle harder requests.
- The Apple-style split in that source is a durable product pattern: one small on-device model for privacy/latency/common cases, plus a larger server model for harder tasks. For this page, that means "on-device reasoning" is often a **routing architecture**, not a single local model doing everything.
- [[Sebastian Raschka - Using Local Coding Agents]] extends on-device deployment from phones to the developer workstation: an open-weight model served locally by Ollama/LM Studio/vLLM (an OpenAI-compatible endpoint) on a Mac Mini or DGX Spark, driving a [[Coding Agent Harness]]. Its constraints echo this page — sustained tokens/sec and bounded memory over *long* agentic contexts (~30 GB for 50k tokens) — and its privacy motivation (keeping data off third-party APIs) is the same one that pushes reasoning onto local hardware.
- [[Onur Sirin - How Local LLMs Run]] makes the local-deployment tradeoff concrete: Q4 weights may make a model *fit*, but local reasoning only feels usable if the active weights and KV cache sit in a sufficiently fast memory tier. The source's local-hardware comparison (5090, Mac Studio, GB300) is a practical checklist for on-device reasoning: capacity, bandwidth, topology (flat vs tiered), active-parameter count for MoE, and whether overflow drops to a slow tier.

## An on-device speech model, in numbers

[[Halo Research - Sopro V2 On-Device Text-to-Speech]] gives this page a concrete non-text data point.
A **120M-parameter open voice-cloning TTS** model reaches **0.24 real-time factor on an M3 CPU**
offline and **~300 ms time-to-first-audio on M3** when streaming. These are the vendor's
**single-stream PyTorch results at default settings, without batching**, not a universal
device-latency guarantee.

The design moves that made it fit are the ones this page keeps encountering: strip inherited
components sized for a different task (an 8,192-token SentencePiece vocabulary replacing a Llama 128k
one with a roughly 49M-parameter embedding table), distil from a larger teacher, and move work from
inference into training. Reflow reduces **acoustic-head** solver steps from 32 to two; the reported
16x head speedup is not a 16x improvement of the whole application. Quality parity remains a
first-party stage-specific claim rather than a matched base/Turbo comparison.

The motivation is also instructive about *why* on-device matters beyond latency: the author built it
because European Portuguese is poorly served by hosted TTS. Local execution is what makes a
long-tail language economically viable at all, since no vendor has to justify the market. Privacy
follows for free — no audio leaves the device. See [[Neural Text-to-Speech]].

## Local-first deployment has several memory budgets and a separate cloud trust boundary

[[ByteByteGo - How Apple Fits an LLM on Your iPhone]] turns the earlier Apple-style routing
pattern into a concrete, secondary account of the memory stack. Its roughly 3B model needs
almost **6 GB for 16-bit weights alone**; an earlier **3.7-bit average** reduces those weights
to about **1.39 GB**. A later **2-bit decoder / 4-bit embedding** recipe is a different
generation, not another description of that average.

Weight storage is only the first lever. Cross-layer sharing reportedly removes **37.5% of
KV-cache memory**, while task-specific rank-16 LoRA adapters reuse the base rather than
duplicating it. These savings concern different memory objects and do not establish total
runtime fit, battery life, thermal behavior, or sustained latency; none of those is measured
in the capture.

Harder requests may leave the phone for Private Cloud Compute. That is a change of trust
boundary, not an extension of the claim that data stays local: the account relies on verified
authorized software and encrypted delivery. See [[Confidential Computing]]. The closing
AFM 3 and cloud-platform claims remain unverified reporting, not device specifications adopted
by this page.

## The browser tab as a deployment target

[[PyTorch - ExecuTorch WebGPU - PyTorch Models on the GPU, in the Browser]] adds a deployment tier this
page had not covered: a web page. A PyTorch model is exported once with `torch.export` to an
ExecuTorch `.pte` file and runs in any WebGPU-enabled browser through a WebAssembly runtime. Its
compute is written as WGSL shaders, which are translated to Metal, Vulkan or D3D12 depending on the
platform. The post's case for the browser repeats this page's motives (prompts, inputs and outputs
stay on the user's device; offline use; lower server costs) and adds distribution: nothing is
installed, and the model is a file served from a CDN.

The reported speed comes from one comparison. On one Apple M1 Pro in Chrome, with quantized Llama
3.2 1B and Qwen3-0.6B across 128 to 8K tokens of context, WebGPU was **4-7x** faster than
ExecuTorch's own WebAssembly CPU backend (XNNPACK) on prefill and **2-10x** faster on decode, taking
the median of 5 runs after 3 warmups. The baseline is the same project's CPU path, not another
browser runtime, and the two paths use different activation precision (see
[[Model Quantization and Efficiency]]). No battery, thermal or mobile-browser figure is given, so
the result shows the GPU beating the CPU inside one laptop browser, not browser inference meeting
this page's phone constraints.

Two details connect to the memory budgets above. Dynamic shapes are handled with buffers allocated
at their maximum size and workgroups recalculated per dispatch, which enables batched prefill; this
implies the tab reserves memory for the largest shape, but the post gives no memory figure. The
models are small: the four LLMs listed run from 0.5B to 1B parameters, three of them marked 4-bit
quantized, alongside vision, speech-to-text and text-to-speech models, and the backend also supports
LoRA and DiReFT fine-tuning on the device for three of them. The post calls the backend "still in
early development".

## Open questions

- When will latent/internal reasoning become more edge-friendly than explicit chain-of-thought?
- What is the best combination of sparsity, quantization, routing, and verifier design for mobile assistants?
- Can parallel test-time scaling remain worthwhile on phones once power, thermal limits, and user-perceived latency are included?
- Which reasoning tasks should stay local for privacy/latency, and which should escalate to a larger cloud model?
- Can a browser tab hold a reasoning model's long traces? The ExecuTorch WebGPU benchmarks stop at
  8K tokens of context on one laptop and give no memory figure for its allocate-at-max buffers.

## Related pages

- [[ByteByteGo - How Apple Fits an LLM on Your iPhone]]
- [[Apple]]
- [[Confidential Computing]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Efficient Reasoning on the Edge]]
- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Prateek Singh - KV Cache and TurboQuant]]
- [[Small Language Models]]
- [[Coding Agent Harness]]
- [[Sebastian Raschka - Using Local Coding Agents]]
- [[Onur Sirin - How Local LLMs Run]]
- [[ByteByteGo - Large Language Models vs Small Language Models]]
- [[LLM Training Pipeline]]
- [[AI Agents in Production]]
- [[Reasoning Compression]]
- [[Mixture of Experts]]
- [[Qualcomm AI Research]]
- [[AI Knowledge Base Overview]]
- [[Neural Text-to-Speech]]
- [[Halo Research - Sopro V2 On-Device Text-to-Speech]]
- [[PyTorch - ExecuTorch WebGPU - PyTorch Models on the GPU, in the Browser]]
- [[PyTorch]]
