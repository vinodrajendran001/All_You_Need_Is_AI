---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-10-23
tags: [entity, organization, models, inference, ai-agents]
source_ids:
  - src-2026-09-14-alphasignal-deepseek-v4-1-flash
  - src-2026-09-27-fd-agent-muse-compute-demand
  - src-2026-10-20-gupta-deepseek-deepinfer
status: active
---

# DeepSeek

## What it is

DeepSeek is an AI model developer represented in this vault through architecture, distillation,
speculative decoding, attention, and inference-efficiency discussions.

## Why it matters here

[[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]] makes DeepSeek relevant as an
example of separating total capacity from active serving cost. V4.1-Flash is described as combining
sparse experts, asymmetric prefill/decode activity, local-state replay, compressed sparse
long-context retrieval, and FP4 cache storage.

The source is secondary and contains no measured serving benchmark, so the architecture figures are
useful as a systems hypothesis rather than independent proof of cost or latency.

## Roughly 0.23 physical cores per live sandbox is the density other estimates borrow

DeepSeek appears here in a second role, outside model architecture: as a published infrastructure
reference point that other people compute with. [[FD - Agent Muse Compute Demand]] anchors its CPU
oversubscription assumption on DeepSeek's **DSec** paper - **~30,000 physical CPU cores**, **250 TB of
DRAM**, **~160 nodes**, peak concurrency above **380,000 sandboxes**, stable at about **800 microVMs
per node** on roughly **188 physical cores per node**, which works out to about **0.23 physical cores
per live VM**.

The way that number is used is as important as the number. FD treats it as a floor rather than a
target: Muse is assumed *less* efficient, with a sensitivity range of **0.3-0.75** and a base case of
**0.5** physical cores per live VM. So DSec does not enter the analysis as a prediction about anyone
else's fleet; it enters as the most efficient published behaviour available, with the estimate
deliberately parked above it. The whole exercise is a **scenario estimate built on assumptions**, not
a measurement, and FD flags directly that DSec's sandbox workload and implementation may differ
materially from Muse's.

For this page that extends DeepSeek's existing role rather than changing it. The vault's other
DeepSeek material is about doing more with less at the model layer - sparse experts, asymmetric
prefill/decode, FP4 cache storage, conditional memory via Engram. DSec places the same reputation one
layer out, in the sandbox fabric that hosts agent execution, and in a form specific enough to be
reused as an input elsewhere. The limit is the usual one for a borrowed density figure: it is only as
good as the workload behind it, and this vault has no independent detail on what those 380,000
sandboxes were doing.

## The serving layer it publishes, and the part it keeps

[[Mehul Gupta - What is DeepSeek DeepInfer]] adds a third role to the two above. DeepSeek appears here
not as a model architect and not as a borrowed infrastructure datapoint, but as a publisher of serving
software — and the shape of what it published is the interesting part.

**DeepInfer is reported as built primarily on vLLM**, with inspiration from SGLang and TensorRT-LLM.
The author attributes this to DeepSeek rather than claiming it independently, and it inverts the usual
direction of this page's material: on architecture DeepSeek is upstream of everyone else's
implementations, while on serving it is downstream of the open ecosystem. The release adds kernels
(FlashMLA, DeepGEMM, DeepEP, TileKernels/TileLang), parallelism including Expert Parallelism Load
Balancing, **DSpark** speculative decoding, an asynchronous scheduler, batch-invariant determinism, and
structured output. It omits, by the same account, complete **KV-cache management**, complete
**prefill-decode disaggregation**, and **replica load balancing** — so the fleet layer stays in-house.
See [[Inference Serving Engines]].

**Hardware support is narrow and notable**: NVIDIA **SM100** and Huawei **Ascend 950** NPUs, with
Linux, GCC **13+**, Python **3.12**, and CUDA **13** or CANN **9.2**. RTX 4090, RTX 5090, A100, and
H100 are named as not covered. Shipping an Ascend path alongside the NVIDIA one is a second-source
accelerator commitment expressed in code rather than in a statement; see
[[Accelerator Software Externalization]] for what that usually costs.

The gap worth recording is between this page's two DeepSeek sources. The section above reports
**V4.1-Flash** compressing global cache growth to **890 bytes per token**; DeepInfer's initial release
is said to support **DeepSeek-V4.1-Flash**, with the offline example using the
**DeepSeek-V4.1-Flash-1017** checkpoint. The obvious inference — that the engine demonstrates the
model's serving economics — is exactly what the vault cannot make. Both sources are secondary, neither
reports a throughput, latency, cost, or memory figure, and the engine is described as lacking a
complete KV-cache management system, which is the subsystem the model's headline claim lives in. Two
adjacent artifacts, no bridge between them.

## Open questions

- Nothing in the vault verifies that DeepInfer powers DeepSeek's production systems, or that every
  component the article lists is implemented in the released code rather than planned, integrated, or
  repository-adjacent.
- There is no measured link between V4.1-Flash's reported cache compression and any serving result on
  any engine, DeepInfer included.
- Both DeepSeek sources on this page are secondary — a newsletter and a Medium walkthrough. The vault
  holds no first-party DeepSeek technical document, so every figure attributed to DeepSeek here has
  passed through an interpreter.
- What does DeepSeek run internally that DeepInfer does not contain? The omissions are named but their
  in-house replacements are not described anywhere the vault can see.
- Does the Ascend 950 support reflect a durable multi-vendor strategy or a procurement constraint?
  Nothing in the source distinguishes them.

## Related pages

- [[Mehul Gupta - What is DeepSeek DeepInfer]]
- [[Inference Serving Engines]]
- [[Prefill-Decode Disaggregation]]
- [[Speculative Decoding]]
- [[Accelerator Software Externalization]]
- [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]
- [[KV Cache]]
- [[Mixture of Experts]]
- [[Inference Efficiency Frontier]]
- [[Transformer Architecture]]
- [[FD - Agent Muse Compute Demand]]
- [[Multi-Tenant Agent Architecture]]
- [[AI Agents in Production]]
- [[Meta]]

