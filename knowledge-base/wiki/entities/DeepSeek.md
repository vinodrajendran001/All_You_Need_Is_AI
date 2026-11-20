---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-11-20
tags: [entity, organization, models, inference, ai-agents, open-models]
source_ids:
  - src-2026-09-14-alphasignal-deepseek-v4-1-flash
  - src-2026-09-27-fd-agent-muse-compute-demand
  - src-2026-10-20-gupta-deepseek-deepinfer
  - src-2026-11-06-doubleai-llms-redesign-themselves
  - src-2026-11-05-huggingface-moe-training-handbook
  - src-2026-11-15-anshuman-mishra-baseten-2000tps
  - src-2026-11-12-will-depue-checkpoint-forensics
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

## DeepSeek's own deployment notes, relayed by a training handbook

[[Nouamane Tazi et al - The Ultimate MoE Training Handbook]] cites two DeepSeek documents, the
DeepInfer release post on Zhihu and the deployment Q&A in the DeepInfer repository, and calls
DeepInfer "DeepSeek's production serving engine". It relays how DeepSeek serves V4.1-Flash: prefill
at expert-parallel sizes **EP2 to EP8**, the smallest whose GPUs have enough memory, and decode at
**EP64 to EP128**, the largest the GPUs allow, with data-parallel attention and no tensor or context
parallelism. At 64 requests per GPU, EP64 decodes about **15,700** tokens per second per GPU against
about **12,600** at EP8, about 25% more. Prefill and decode get roughly equal GPU counts, so the
smallest deployment worth running is **64 GPUs for prefill plus 64 for decode**. One failed GPU
takes a whole expert-parallel instance down, and on restart DeepSeek re-sizes the group to the
healthy GPUs.

Separate prefill and decode pools in DeepSeek's own deployment fit Gupta's account that the public
release lacks complete prefill-decode disaggregation: the fleet layer stays in-house. This narrows
the open questions below without closing them. The vault has read neither DeepSeek document
directly, the relayed passage names no GPU type, and no relayed figure measures memory or cache, so
nothing yet connects to the **890 bytes per token** claim. See [[Inference Serving Engines]] and
[[Prefill-Decode Disaggregation]].

## A third-party engine for V4.1-Flash, and an approximate prefill

[[Anshuman Mishra - I Reverse Engineered Baseten's 2000TPS Inference Engine]] documents a non-DeepSeek
engine for **DeepSeek-V4.1-Flash** that uses the model's own features. DSpark drafting reads target
features from layers 37-39, and a rank-256 "Markov" correction conditions each draft token on the
previous one. The engine's Blackwell Ultra profile allows **six** draft tokens, where DeepInfer's
default maximum is five, so the draft budget is an engine choice rather than a model constant. The
relayed throughput (**2,060 tokens/s on 8 × B300**) is Baseten's, on Baseten's engine. It does not
bridge the gap noted above between the model's cache claim and DeepInfer, because it is a different
engine and reports no memory figure.

The new point is about the model. V4.1-Flash is described as a 20-layer encoder plus 20-layer decoder
whose global KV comes from the encoder side. A long prompt can therefore stream through the first 20
layers and replay the decoder only over the last **128** tokens: **20,002,560** layer-token evaluations
against **40,000,000**, a ratio of about **0.500064**. The author says this does not prove a twofold
FLOP or time reduction. The source cites DeepSeek's paper (Section 3.2.2) as calling bounded replay
an **approximation**, with "little quality degradation" in DeepSeek's evaluations. Million-token
prefill figures for this model may therefore not be like-for-like with a full decoder pass.

## A model that built a verifier on its own activations

In [[DoubleAI - Can LLMs Redesign Themselves as They Train]], **DeepSeek-V4.1-Flash** (described as
a 763B mixture-of-experts model, run without thinking mode) acts as the agent on itself. From its
own graded solutions to **243** problems from the 2024 and 2025 contests, it chose a linear probe at
seven deep blocks of its residual stream. From held-out older problems, DeepSeek predicted the probe
would add about eight points; the hidden AIME 2026 and HMMT February 2026 sets gave seven
(**64%→71%**). First-party blog, single run reported.

## An outside reading of DeepSeek's initialization hardware

[[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]] reports that DeepSeek
reuses one initialization seed (**953049583**) across generations. That lets an outside analyst
compare layouts. DeepSeek V3 and V3.2 read as Hopper (**132** SMs), consistent with DeepSeek's
disclosed H800 use, though the method cannot separate H800 from H100 or H200. V4-Flash reads as
B200/B300 (**148**) and V4-Pro as GB200/GB300 (**152**). V4-Flash was reproduced on a physical B300,
with **445** of **469** selected rows matching bit for bit, and an AMD alternative was excluded for
that model only. V4-Pro rests on statistics alone, with no physical reproduction. No fingerprint was
found in V4.1-Flash. The report says this supports, "without proving", Blackwell training. It does
not establish chip location or ownership, or any export-control violation. It also cites a June 2025
DeepSeek engineer comment, "we don't have SM100 GPUs", which predates V4's release and so neither
confirms nor refutes the reading. DeepInfer's SM100 support, above, is software support and is not
evidence of possession. No DeepSeek response is reported. See [[Checkpoint Forensics]].

## Open questions

- Nothing in the vault verifies that DeepInfer powers DeepSeek's production systems, or that every
  component the article lists is implemented in the released code rather than planned, integrated, or
  repository-adjacent.
- There is no measured link between V4.1-Flash's reported cache compression and any serving result on
  any engine, DeepInfer included.
- Both DeepSeek sources on this page are secondary — a newsletter and a Medium walkthrough. The vault
  holds no first-party DeepSeek technical document, so every figure attributed to DeepSeek here has
  passed through an interpreter. Mishra's write-up cites DeepSeek's paper (Section 3.2.2), but only
  secondhand; the paper itself is not in the vault.
- What does DeepSeek run internally that DeepInfer does not contain? The omissions are named but their
  in-house replacements are not described anywhere the vault can see.
- Does the Ascend 950 support reflect a durable multi-vendor strategy or a procurement constraint?
  Nothing in the source distinguishes them.
- Does the V4-generation Blackwell initialization reading hold under independent replication? Did
  training stay on the initializing hardware? The forensic report cannot see either.

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
- [[DoubleAI - Can LLMs Redesign Themselves as They Train]]
- [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]]
- [[Anshuman Mishra - I Reverse Engineered Baseten's 2000TPS Inference Engine]]
- [[Baseten]]
- [[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]]
- [[Checkpoint Forensics]]
- [[NVIDIA]]
- [[Open Model Ecosystems]]
