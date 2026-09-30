---
type: entity
created: 2026-06-03
updated: 2026-09-30
entity_kind: organization
tags:
  - entity
  - organization
  - multimodal
  - vision
  - gpu
  - hardware
source_ids:
  - src-2026-06-03-nvidia-locateanything
  - src-2026-07-01-anastasiia-alekseeva-parallel-training
  - src-2026-07-02-alyona-vert-ai-concepts-2026
  - src-2026-07-03-fergus-finn-cuda-kernel
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
  - src-2026-09-05-lenz-nemoclaw-memory-agent
  - src-2026-09-10-lenz-epd-multimodal-serving
  - src-2026-09-23-kwok-contrastive-language-models
  - src-2026-09-28-inferact-tpu-megakernels-kimi-k3
status: active
---

# NVIDIA

## What it is

Technology company and research organization. In this vault it now spans three roles: high-throughput vision-language grounding research, the **GPU hardware and CUDA software stack** that virtually all modern training and inference runs on, and the **Megatron-LM** framework that formalized tensor parallelism.

## Why it matters here

NVIDIA matters because its LocateAnything source opens a branch around multimodal localization, showing that inference bottlenecks and interface design also matter for grounding models, not only for text LLMs. Beyond that vision work, NVIDIA is the hardware substrate under most other pages: the RTX 4090 whose warps [[Fergus Finn - What Happens When You Run a CUDA Kernel|execute a traced CUDA kernel]] ([[GPU Execution Model]]), the author of **Megatron-LM** whose column-then-row GEMM split underpins [[Distributed Training Parallelism|tensor parallelism]], and — via the rack-scale **Vera Rubin** platform — one pole of the [[AI Accelerator Architecture|inference-chip]] competition described in [[Alyona Vert - AI Concepts and Techniques in 2026]].

## Position in the accelerator landscape

[[Jacob Peake - AI Chip Architectures]] places NVIDIA inside a competitive frame rather than treating it as the default. Its reading of the 2024–25 period is that NVIDIA's decisive advantage was **rack-scale coherent memory**: NVLink turns a rack into one large coherent domain, which suits large mixture-of-experts models with high memory demand and lets the rack behave as a single accelerator rather than a network of them. The claim is architectural, not brand-based — the survey's four-question frame (memory system, precision, interconnect, and the workload being bet on) applies to NVIDIA the same way it applies to Cerebras or Groq.

The same source records two specific facts worth keeping:

- **NIC bandwidth is doubling per generation** — ConnectX-7 at 400 Gbps, ConnectX-8 at 800 Gbps, ConnectX-9 projected at 1.6 Tbps — which is why the survey treats interconnect as a first-class design axis rather than plumbing.
- NVIDIA's **acquihire of the Groq LPU team, with a non-exclusive license**, is offered as evidence that deterministic scheduled execution is being absorbed into the incumbent rather than left to competitors. See [[Groq]] and [[AI Accelerator Architecture]].

The survey also supplies the efficiency comparison that frames NVIDIA's trade-off: Cerebras claims roughly 1.3 bytes of memory bandwidth per FLOP against about 0.002 for a GPU, at the cost of yield, packaging, and model-size constraints. NVIDIA's design sits at the other end — far less bandwidth per FLOP, but far more generality and a mature software stack.

## Notes

- The current NVIDIA sources in the vault are [[NVIDIA - LocateAnything]] (vision), plus the CUDA-kernel and parallel-training explainers that use NVIDIA hardware/frameworks.
- Its DGX Spark also appears as local-inference hardware in [[Sebastian Raschka - Using Local Coding Agents]].
- H100 hardware is the reference point for the arithmetic-intensity analysis in [[Changyi Yang - Why MLA and MTP Fight Each Other]], whose ~295 FLOP/byte roofline ridge determines whether an inference optimization helps or hurts; see [[Arithmetic Intensity and the Roofline Model]].
- In this knowledge base, NVIDIA strengthens both the multimodal/perception side and the hardware/training-systems side of the graph.

## Documentation as a moat

[[Wafer - AI Performance Engineering Resources]] shows a dimension of NVIDIA's position that hardware comparisons miss: the depth of its public documentation. That learning path can cite the CUDA programming and best-practices guides, the PTX ISA, per-architecture tuning guides for Hopper and Blackwell, and a full profiling toolchain (Nsight Systems, Nsight Compute, Compute Sanitizer) — while its AMD, TPU, and Trainium sections are markedly shorter, a gap the curator attributes to documentation availability rather than deployment share.

The asymmetry is self-reinforcing: engineers learn performance work on the stack that documents itself, and the resulting expertise is stack-specific. The same list keeps **Rubin** on a dated frontier watchlist rather than the core path, on the principle that an announced architecture does not qualify until a specification, a shipped implementation, and a reproducible measurement all exist. See [[Wafer]].

## NeMo-RL and NeMo-Gym as the RL training stack

[[IBM Granite Team - Granite 4.2 LLMs How They're Built]] documents an NVIDIA software stack this
vault had not recorded, used end to end for a third party's model family.

**NeMo-RL** drives the training side: Megatron-Core as the training backend, vLLM for rollout
generation, and **Megatron-Bridge** converting weights between Megatron and Hugging Face formats so
each RL stage can export a clean checkpoint for the next one. **NeMo-Gym** handles rollouts, exposing
every environment — verifiers, tools, sandboxes, reward models — as pluggable **Resources** behind
one uniform interface.

This is worth noting for what it says about NVIDIA's position. The company's leverage in this vault
is usually described through silicon and CUDA. Here it also supplies the orchestration layer for
agentic RL, on hardware it designed (GB200 NVL72), with generation running on vLLM. Granite 4.2 was
trained on NVIDIA hardware, with NVIDIA training software, using NVIDIA's environment abstraction —
a full-stack dependency, and the same kind of vertical position that makes NVIDIA hard to displace.

See [[Staged Reinforcement Learning Curriculum]] for why the Resource abstraction is the load-bearing
piece.

## Memory agents and policy separation

[[Tanya Lenz - Building a Memory-Driven Agent with NVIDIA NemoClaw]] adds a fourth NVIDIA role to the
vault: an agent-memory recipe built on NemoClaw and isolated with OpenShell. The benchmark reports an
8.1-point overall gain on 186 questions but regressions on corpus faithfulness and single-hop lookup.
The source is NVIDIA-authored, uses invented workplace data, and performs no live external actions.

## Multimodal serving

[[Tanya Lenz - EPD Disaggregation for Multimodal Model Serving]] adds a Dynamo benchmark for
independently scaling vision encoding and prefill/decode. It is useful as a topology study while
remaining vendor-authored and specific to NVIDIA hardware, NIXL, and the tested Qwen configuration.

## Nemotron data and a single RTX 4090 underwrite someone else's decision model

[[Jacky Kwok et al - Contrastive Language Models]] adds a role this page has not recorded: NVIDIA as
the **data asset** inside an outside group's architecture. The paper is co-authored by NVIDIA
Research with Stanford, and its pre-training corpus is **~60M Nemotron DQA question-answer pairs**.
Mid-training then layers on **~30M synthetic hard negatives generated by Gemini 2.5 Flash-Lite** — a
competitor's model supplying the negatives against NVIDIA's positives — and post-training adds
**~1M** ADP agent trajectories. Elsewhere on this page NVIDIA's leverage is silicon, CUDA, and the
NeMo training stack; here it is a corpus that a third party can build a competing decision model on.

The hardware span is the other detail worth keeping, because it covers both ends of NVIDIA's own
product line in one paper. A full pre-training run on Nemotron DQA is reported at **about an hour on
a single RTX 4090** — only a **20M-parameter projection head** is trained, over frozen LLM backbones
— while the reward-model results (**81.6% on DeepSWE** over **38 held-out tasks**, **87.6% on
Terminal-Bench 2.1** over **30**) have their latency measured on an **H100 GPU**. Those two accuracies
are best-of-N *selection* scores over candidate solutions sampled with **Opus 5** for DeepSWE and
**Fable 5** for Terminal-Bench 2.1, so the generator sets the ceiling and the figure is not a property
of the verifier alone. The consumer card
is the training budget and the datacenter part is the measurement instrument, in work NVIDIA did not
have to fund to benefit from.

Provenance limits apply to all of it. Every figure is first-party and self-reported, "SOTA" is the
authors' own characterization, the venue is a **Notion page rather than a peer-reviewed paper**, and
the capture's frontmatter carried **no author at all** — the author list was recovered from the body
and its BibTeX entry. The three speed claims describe three different conditions and must not be
merged into one: **up to 9x lower latency** overall, **4-6x faster inference than Jev** in the
benchmark section, and **13x** at roughly **1k candidates**. See
[[Typed Probabilistic Decision Models]].

## GB200's SRAM is split 152 ways, and a competitor built its case on exactly that

[[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]] is the vault's first third-party
argument *against* NVIDIA at a named operating point, and it is notable because the argument is not
about peak numbers — which GB200 largely wins. By Inferact's own comparison, **GB200, per GPU, leads
on 2.5 PFLOPS BF16 / 5 PFLOPS FP8, 8,000 GB/s of HBM bandwidth, and 1,800 GB/s of NVLink 5**, against
TPU v7's **2.31 / 4.61 PFLOPS, 7,380 GB/s HBM and 1,200 GB/s ICI**; GB200 trails only on HBM capacity
(**186 GB against 206 GB**). Inferact's table is per-GPU, and its baseline is 16 GB200 GPUs, not 16
superchips.

The claimed weakness is granularity of on-chip memory. Inferact puts **GB200's ~111 MiB of SRAM split
152 ways** — **256 KB of Tensor Memory and 228 KB of shared memory per SM across 152 SMs**, roughly
**38 MiB** of Tensor Memory per GPU — against TPU v7's **64 MiB of VMEM per TensorCore and 128 MiB per
chip addressed as two pools**. Nearly equal totals, very different shapes, and the shape is what a
single persistent decoder program needs. The reported consequence, with conditions: on **Kimi K3
(92 MoE layers, 16 TPU v7 chips, 2x2x4 topology, TP4 x EP8)**, decode **without speculation** runs
**249 vs 127 tokens/s at batch 1 (1.96x)**, narrowing monotonically to **865 vs 636 (1.36x) at batch
8**; with **speculative decoding at acceptance length 6**, **709 vs 452 (1.57x)**; and on **Qwen 3.8
27B at acceptance length 6, 1,515 tokens/s on 4x TPU v7 against 695 on 4x GB200 (2.18x)**.

The asymmetry matters more on an entity page than the ratios do. Inferact compares its **own
hand-written TPU megakernel against a published vLLM GB200 recipe**, so this is a software-effort
comparison as much as a hardware one — and it points in the opposite direction from the moat this
page records above. Both readings can hold at once: NVIDIA's documentation and tooling depth make
competent GPU performance broadly reachable, while a specialist willing to hand-write a single-kernel
decoder on another vendor's chip can beat the published recipe at one narrow operating point. The
claim is also scoped away from where [[Jacob Peake - AI Chip Architectures]] locates NVIDIA's
structural advantage: rack-scale coherent memory for large MoE serving is a throughput-regime
argument, and Inferact's margin is largest at batch 1 and fading by batch 8.

Everything here is vendor-reported by a party selling TPU inference work: no independent reproduction,
no confidence intervals, and no energy or cost-per-token figures.

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[Staged Reinforcement Learning Curriculum]]
- [[IBM]]
- [[Jacob Peake - AI Chip Architectures]]
- [[NVIDIA - LocateAnything]]
- [[Vision-Language Grounding]]
- [[GPU Execution Model]]
- [[Distributed Training Parallelism]]
- [[AI Accelerator Architecture]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Cerebras]]
- [[Groq]]
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]]
- [[AI Agents in Production]]
- [[AI Knowledge Base Overview]]
- Wafer - AI Performance Engineering Resources
- Wafer
- GPU Kernel Optimization
- [[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]
- [[Megakernels]]
- [[Jacky Kwok et al - Contrastive Language Models]]
- [[Typed Probabilistic Decision Models]]
- [[Embedding Model Selection]]
- [[Inference Efficiency Frontier]]
