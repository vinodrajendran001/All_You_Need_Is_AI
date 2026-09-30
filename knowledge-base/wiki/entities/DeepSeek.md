---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-09-30
tags: [entity, organization, models, inference, ai-agents]
source_ids:
  - src-2026-09-14-alphasignal-deepseek-v4-1-flash
  - src-2026-09-27-fd-agent-muse-compute-demand
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

## Related pages

- [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]
- [[KV Cache]]
- [[Mixture of Experts]]
- [[Inference Efficiency Frontier]]
- [[Transformer Architecture]]
- [[FD - Agent Muse Compute Demand]]
- [[Multi-Tenant Agent Architecture]]
- [[AI Agents in Production]]
- [[Meta]]

