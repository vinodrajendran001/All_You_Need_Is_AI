---
type: concept
created: 2026-06-04
updated: 2026-08-27
tags:
  - concept
  - reasoning
  - compression
  - efficiency
  - cot
source_ids:
  - src-2026-06-04-efficient-reasoning-edge
  - src-2026-06-04-progressive-thought-encoding
  - src-2026-06-04-pace-efficient-reasoning
  - src-2026-06-04-extreme-ratio-cot-compression
  - src-2026-06-04-reasoncache
  - src-2026-06-04-difficulty-aware-entropy-regularization
  - src-2026-06-04-conpress
  - src-2026-06-04-dss-grpo-cot-compression
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
status: active
---

# Reasoning Compression

## Definition

Reasoning compression is the family of methods that reduce the token, memory, or training cost of explicit reasoning while trying to preserve answer quality. It includes shortening visible chain-of-thought traces, protecting only the most important steps, replacing long traces with fixed-size internal state, and learning when to spend more or less reasoning budget.

## Why it matters

The usefulness of reasoning models is increasingly bounded not only by accuracy but by **how expensive each extra thought is**. Long traces inflate latency, KV-cache size, training memory, and deployment cost. Reasoning compression tries to keep the benefits of deliberate reasoning without paying the full chain-of-thought tax every time.

## Current synthesis

- A first split in the literature is **where compression happens**:
  - **Token-space compression** shortens or restructures visible CoT traces. This is the dominant family in PACE, Extra-CoT, CEEH, ConPress, DSS-GRPO, and the Qualcomm edge paper.
  - **State-space compression** replaces long visible traces with compact internal representations. [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]] uses fixed-size vector encodings of intermediate thought, while [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]] distills demonstrations into reusable key-value caches.
- A second split is **how the compression policy is learned**:
  - **RL-based control** — [[Efficient Reasoning on the Edge]], [[PACE - Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning]], [[Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning]], and [[Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression]] all shape rewards so models become shorter without becoming wrong.
  - **SFT / supervised compression** — [[Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression]] uses compressed supervision plus mixed-ratio SFT before RL.
  - **Self-supervision from model behaviour** — [[ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure]] mines concise traces from the model's own self-compression behaviour under multi-question prompts.
  - **Prefix/cache learning** — [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]] avoids conventional weight updates and stores reasoning skill in attention-state scaffolding instead.
- A recurring lesson is that **uniform pressure is brittle**. Several papers independently argue that not all prompts and not all reasoning segments should be compressed equally:
  - PACE protects prefixes and scales penalties by difficulty.
  - CEEH preserves exploration on hard questions with entropy regularization.
  - DSS-GRPO separates think and answer segments so the final answer is not accidentally compressed.
  - Extra-CoT trains across a range of compression ratios rather than one fixed target.
- Another durable pattern is that compression can sometimes **improve** accuracy rather than merely preserve it. The shared intuition is that many reasoning models waste tokens on hesitation, redundant verification, or diffuse exploration. Compression helps when it removes that waste without cutting away the critical logical spine.
- The branch also shows that efficient reasoning is as much a **systems problem** as a model problem. Token reduction matters because decoding is memory-bound, KV caches grow with trace length, and RL rollout memory scales badly with long visible thoughts.
- This page is the **"spend less"** dual of [[Test-Time Scaling]]'s "spend more." [[Akhil Arora et al - Current Advances in LLM Reasoning]] unifies the two: "just thinking more is not enough" because more tokens can cause *overthinking*, so the frontier is a **controller** that decides right-sized compute — whether to answer now, think longer, branch, retrieve, or verify. Compression, budget forcing, and adaptive early-exit are the mechanisms that keep that controller from defaulting to maximal-compute, and they connect the efficiency branch directly to the broader [[LLM Reasoning]] map.

## Verbosity as a side effect to be removed later

[[IBM Granite Team - Granite 4.2 LLMs How They're Built]] adds a pipeline-level view of the problem
this page addresses. Granite's final RLHF stage applies a **reasoning-length penalty specifically to
discourage the overly verbose reasoning behavior acquired during earlier stages**.

The framing matters. Most compression work on this page treats length as a property to optimize
directly — budget forcing, difficulty-scaled rewards, segment-wise compression. Granite treats it as
**iatrogenic**: the earlier capability stages, optimizing verifiable rewards on math, code, and
long-horizon agentic tasks, taught the model to think longer because longer thinking scored better,
and the alignment stage then has to undo it.

That suggests reasoning bloat is partly a predictable consequence of multi-stage post-training rather
than an intrinsic property of reasoning models, and that where the correction is applied is a design
choice. Granite applies it last, at the highest KL in the pipeline, bundled with preference and
safety — which keeps capability stages unconstrained but means the model spends the whole pipeline
learning a habit that must then be trained away.

Granite also ships **three inference-time settings rather than two**: thinking, non-thinking, and a
**low-effort** mode that spends a short reasoning budget on easy questions. The middle rung is the
interesting one, since the usual binary forces a routing decision between "cheap and shallow" and
"expensive and deep." See [[Test-Time Scaling]] and [[Model Routing]].

## Open questions

- What is the right balance between interpretability and efficiency once compressed traces become very short or entirely internal?
- How should systems estimate prompt difficulty online before deciding how much reasoning budget to spend?
- Which compression strategies generalize beyond math-heavy benchmarks into open-ended, tool-using, or multimodal settings?

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[Efficient Reasoning on the Edge]]
- [[On-Device Reasoning]]
- [[Model Quantization and Efficiency]]
- [[LLM Training Pipeline]]
- [[Reward Design for RL]]
- [[Group Relative Policy Optimization]]
- [[Latent-Space Reasoning]]
- [[Training Large Reasoning Models Efficiently via Progressive Thought Encoding]]
- [[PACE - Prefix-Protected and Difficulty-Aware Compression for Efficient Reasoning]]
- [[Towards Efficient Large Language Reasoning Models via Extreme-Ratio Chain-of-Thought Compression]]
- [[ReasonCACHE - Teaching LLMs To Reason Without Weight Updates]]
- [[Compress the Easy, Explore the Hard - Difficulty-Aware Entropy Regularization for Efficient LLM Reasoning]]
- [[ConPress - Learning Efficient Reasoning from Multi-Question Contextual Pressure]]
- [[Shorter Thoughts, Same Answers - Difficulty-Scaled Segment-Wise RL for CoT Compression]]
- [[Test-Time Scaling]]
- [[LLM Reasoning]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
