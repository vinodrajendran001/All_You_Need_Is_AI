---
type: source-summary
source_id: src-2026-08-23-wafer-ai-performance-engineering-resources
source_title: "AI Performance Engineering"
source_author: Wafer
source_url: https://github.com/wafer-ai/gpu-perf-engineering-resources
created: 2026-08-26
updated: 2026-08-26
tags:
  - source/summary
  - gpu
  - kernels
  - inference
  - performance-engineering
  - reading-list
source_ids:
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-23-wafer-ai-perf-contributing-source-policy
status: active
---

# Wafer - AI Performance Engineering Resources

## Summary

A curated learning path for GPU performance engineering and production inference, maintained by [[Wafer]] and published as a GitHub repository (~2,000 stars at capture). It is deliberately ordered by *dependency* rather than by topic: from a single inference request, to a single GPU, to optimized kernels, to inference engines, to distributed systems, to current hardware.

Its distinguishing feature is not the topic list but the **evidence policy**. A core entry must be the paper that introduced a mechanism, the specification or official documentation that defines it, the repository that implements it, or a direct implementer report with code and measurements. Summaries, generic tutorials, marketing pages, broad surveys, and unhardened leaderboard claims are explicitly excluded. Fast-moving material is quarantined in a dated `Frontier` section that only graduates into the core path once a specification or original paper, a shipped implementation, *and* a reproducible measurement all exist.

For this vault the list functions less as new information than as a **provenance map**: it names the primary literature behind mechanisms the vault currently knows mostly through secondary explainers.

## Key claims

- **Dependency order beats topic order.** The recommended entry sequence is inference scaling → the transformer computation → the CUDA execution model → GPU programming → the roofline model → transformer inference arithmetic → scaling costs → serving SLOs. Optimization is presented as unintelligible until the request lifecycle and the memory hierarchy are both in view.
- **A performance number is meaningless without five attributes**: hardware and software versions, workload shapes or request distribution, precision and algorithm, baseline, and correctness method. If any is missing, the list omits the number rather than reporting it.
- **Vendor peak numbers are not performance measurements.** The hardware section instructs the reader to pair every architecture brief with its ISA or tuning guide.
- **Correctness is part of performance.** Kernel work is paired with Compute Sanitizer, CUTLASS's GEMM measurement methodology, and — for AI-generated kernels — benchmarks with hardened evaluators.
- **The kernel-optimization ladder is explicit**: coalescing and shared-memory tiling → bank conflicts and reduction/scan primitives → online softmax → register tiling and cuBLAS-class matmul → tensor cores and FP8/MX formats → the FlashAttention lineage through the Blackwell schedule.
- **Serving is a scheduling problem before it is a kernel problem.** Orca's iteration-level scheduling, PagedAttention's paged KV allocation, and Sarathi-Serve's chunked prefill are presented as the load-bearing ideas beneath current engines.
- **Prefill and decode are different workloads and increasingly different machines.** DistServe, Splitwise, and Mooncake separate the phases; NIXL and Dynamo are named as the transport and production implementations.
- **Goodput under per-request latency SLOs**, not raw throughput, is the serving metric the list endorses (Etalon, MLPerf Inference, MLPerf Endpoints), with ServeGen and BurstGPT supplying realistic workload shapes.
- **AI-generated kernels are explicitly probationary.** KernelBench, KernelBench-Verified, and SOL-ExecBench are listed under Frontier, with the standing caveat that individual kernel agents which have not been rerun on a hardened evaluator do not qualify.

## Why it matters

The vault's GPU, inference, and serving pages are largely built on secondary explainers — newsletters, visual guides, and vendor blogs. Those are useful for intuition but weak for provenance, and several vault claims currently trace only to a single explainer. This source supplies the primary citation for most of them: the Berkeley roofline technical report behind [[Arithmetic Intensity and the Roofline Model]], the GQA and DeepSeek-V2 papers behind [[KV Cache]], Leviathan and EAGLE behind [[Speculative Decoding]], GPTQ/SmoothQuant/AWQ behind [[Model Quantization and Efficiency]], and Megatron-LM behind [[Distributed Training Parallelism]].

It also fills genuine gaps. Before this ingest the vault had **no mention at all** of FlashAttention, CUTLASS, KernelBench, goodput, Orca, or NCCL, despite having pages on attention, kernels, serving, and parallelism. Kernel programming models and prefill/decode disaggregation were similarly absent — the latter existed only as an open question on [[LLM Inference]], which [[Prefill-Decode Disaggregation]] now answers.

Finally, its `CONTRIBUTING.md` is a reusable **evidence standard**. The five required attributes of a performance claim are a sharper, more checkable version of the caution that [[Benchmark Optimization]] argues for, and they apply well beyond GPU work.

## Tensions / open questions

- **It is a curation, not a result.** Every technical claim here is a claim about *someone else's* source. Nothing in the list is independently verified by the maintainer, and the vault should cite the underlying papers rather than the list for any specific mechanism.
- **Commercial context.** The repository is published by a company that is hiring for exactly this skill set and links its careers page from the README. The evidence policy is strict and the list contains no Wafer product placement, but the selection is not disinterested.
- **Authorship is thin.** The only attribution is the organization and a maintainer email (`emilio@wafer.ai`); no individual author is named in the repository, so this vault attributes it to the organization.
- **Recency is asserted, not continuously verified.** The `Frontier` section is stamped "Verified on 2026-08-23" and the README states external links are checked separately because some primary sources block automated requests — so link rot in the core list is possible between verification passes.
- **The list is Western-vendor and NVIDIA-weighted.** AMD, TPU, and Trainium each get a short section against a much deeper NVIDIA treatment. This reflects available public documentation more than relative deployment, but it does skew the reader's mental model.
- Several entries point to 2026 publications (FlashAttention-4, KernelBench-Verified, ServeGen, Ultra Ethernet 1.0.3) whose durability is not yet established.

## Affected pages

- [[Arithmetic Intensity and the Roofline Model]] - primary citation for the roofline model and transformer inference arithmetic
- [[GPU Kernel Optimization]] - new concept seeded by this source
- [[Prefill-Decode Disaggregation]] - new concept seeded by this source
- [[Serving Benchmarks and Goodput]] - new concept seeded by this source
- [[AI-Generated Kernels]] - new concept seeded by this source
- [[Wafer]] - new entity
- [[LLM Inference]], [[Inference Serving Engines]], [[KV Cache]], [[Speculative Decoding]], [[Model Quantization and Efficiency]], [[Distributed Training Parallelism]], [[Mixture of Experts]], [[Transformer Architecture]], [[GPU Execution Model]], [[AI Accelerator Architecture]], [[Benchmark Optimization]], [[NVIDIA]]

## Raw capture

- `knowledge-base/raw/sources/2026-08-23 Wafer - AI Performance Engineering.md`
- `knowledge-base/raw/sources/2026-08-23 Wafer - Contributing Source Policy.md`

## Citations

- Canonical URL: [https://github.com/wafer-ai/gpu-perf-engineering-resources](https://github.com/wafer-ai/gpu-perf-engineering-resources)
- Repository description: "A curated resource list for learning AI performance engineering, from GPU fundamentals to production inference."
- Repository created 2026-01-12; last push 2026-08-23; ~2,011 stars at capture. No license file is set on the repository, though the README states MIT.
- Maintainer contact given in the README as `emilio@wafer.ai`; no individual author is named, so this vault attributes the work to the organization.
- The `Frontier` section is self-dated "Verified on 2026-08-23"; the capture preserves that stamp.

## Related pages

- [[Wafer]]
- [[GPU Kernel Optimization]]
- [[Prefill-Decode Disaggregation]]
- [[Serving Benchmarks and Goodput]]
- [[AI-Generated Kernels]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[LLM Inference]]
- [[Inference Serving Engines]]
- [[Benchmark Optimization]]
- [[AI Knowledge Base Overview]]
