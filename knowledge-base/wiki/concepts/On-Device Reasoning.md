---
type: concept
created: 2026-06-04
updated: 2026-06-04
tags:
  - concept
  - llm
  - edge-ai
  - reasoning
  - deployment
source_ids:
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-06-04-efficient-reasoning-edge
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
- A deeper lesson is that explicit reasoning itself is a deployment liability. The system must actively manage when to think, how long to think, and whether more test-time compute is worth the extra memory and latency.

## Open questions

- When will latent/internal reasoning become more edge-friendly than explicit chain-of-thought?
- What is the best combination of sparsity, quantization, routing, and verifier design for mobile assistants?
- Can parallel test-time scaling remain worthwhile on phones once power, thermal limits, and user-perceived latency are included?

## Related pages

- [[Efficient Reasoning on the Edge]]
- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Model Quantization and Efficiency]]
- [[LLM Training Pipeline]]
- [[AI Agents in Production]]
- [[Mixture of Experts]]
- [[Qualcomm AI Research]]
- [[AI Knowledge Base Overview]]
