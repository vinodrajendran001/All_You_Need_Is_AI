---
type: concept
created: 2026-06-04
updated: 2026-06-17
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

## Open questions

- When will latent/internal reasoning become more edge-friendly than explicit chain-of-thought?
- What is the best combination of sparsity, quantization, routing, and verifier design for mobile assistants?
- Can parallel test-time scaling remain worthwhile on phones once power, thermal limits, and user-perceived latency are included?

## Related pages

- [[Efficient Reasoning on the Edge]]
- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Prateek Singh - KV Cache and TurboQuant]]
- [[LLM Training Pipeline]]
- [[AI Agents in Production]]
- [[Reasoning Compression]]
- [[Mixture of Experts]]
- [[Qualcomm AI Research]]
- [[AI Knowledge Base Overview]]
