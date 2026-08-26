---
type: entity
entity_kind: organization
created: 2026-08-26
updated: 2026-08-26
tags:
  - entity
  - organization
  - gpu
  - performance-engineering
source_ids:
  - src-2026-08-23-wafer-ai-performance-engineering-resources
  - src-2026-08-23-wafer-ai-perf-contributing-source-policy
status: active
---

# Wafer

## What it is

An AI company working on GPU performance engineering and production inference, publishing at `wafer.ai`. In this vault it is represented by a single artifact: the curated learning path [[Wafer - AI Performance Engineering Resources]], maintained as a public GitHub repository that had accumulated roughly 2,000 stars by the time of capture.

## Why it matters here

Wafer matters to this knowledge base for its **editorial method** more than for any technical claim of its own.

The repository publishes an explicit evidence policy: a core entry must be the paper that introduced a mechanism, an official specification, the implementing repository, or a direct implementer report with code and measurements — and a performance number must carry hardware, workload, precision, baseline, and correctness method or be omitted entirely. Fast-moving material is quarantined in a dated frontier section and only graduates once a specification, a shipped implementation, and a reproducible measurement all exist.

That standard is directly useful to this vault, which relies heavily on secondary explainers for its GPU and inference pages. The list supplies primary citations for mechanisms the vault previously knew only through newsletters and visual guides, and it introduced four topics the vault had no coverage of at all: kernel optimization as a discipline, prefill/decode disaggregation, serving goodput, and AI-generated kernels.

## Notes

- No individual author is named in the repository. The only attribution is the organization plus a maintainer email (`emilio@wafer.ai`), so this vault attributes the work to Wafer rather than to a person.
- The repository is a **curation, not original research**. Every technical claim in it is a claim about someone else's source, and specific mechanisms should be cited to the underlying papers rather than to the list.
- **Commercial interest is disclosed but real.** The README links Wafer's hiring page, and the company recruits for exactly the skill set the list teaches. The list contains no product placement and its evidence policy is strict, but the selection is not disinterested.
- Coverage is NVIDIA-weighted, with shorter AMD, Google TPU, and AWS Trainium sections. This tracks the availability of public documentation more than relative deployment.
- The repository states an MIT license in the README, though no license file is set on the repository itself.

## Related pages

- [[Wafer - AI Performance Engineering Resources]]
- [[GPU Kernel Optimization]]
- [[Prefill-Decode Disaggregation]]
- [[Serving Benchmarks and Goodput]]
- [[AI-Generated Kernels]]
- [[Benchmark Optimization]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[NVIDIA]]
- [[AI Knowledge Base Overview]]
