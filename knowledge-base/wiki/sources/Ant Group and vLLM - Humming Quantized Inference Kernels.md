---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-21-ant-vllm-humming
source_title: "Announcing Humming: Fast, Flexible Kernels for Quantized Inference"
source_author: "Ant Group and the vLLM Community"
source_url: https://vllm.ai/blog/2026-10-21-humming
tags: [source/summary, quantization, kernels, inference, serving]
source_ids:
  - src-2026-10-21-ant-vllm-humming
status: active
---

# Ant Group and vLLM - Humming Quantized Inference Kernels

## Summary

A first-party release account of Humming, a CUDA kernel library that separates quantization
semantics from hardware- and workload-specific execution. Its common representation, weight
preprocessing, configuration system, and reusable components target the maintenance cost of
supporting many precisions across dense and mixture-of-experts workloads. The article reports
both isolated matrix-multiplication benchmarks and one end-to-end serving sweep; these are
different evidence and must not share a headline multiplier.

## Key claims

**Representation and execution are separate.** The standard format describes weights,
scales, zero points, secondary scales, and activation types. Preprocessing validates, pads,
and repacks tensors. Layer Config captures shapes and quantization; Compute Config captures
the operation and options; Tuning Config chooses tiles, pipelines, instructions, and scheduling.
Device-specific heuristics select variants by input size, and NVCC/NVRTC compile and cache
specialized kernels. Automatic benchmarking-based tuning is a future plan, not the default.

**Newer hardware paths do not always win.** Small batches can favor asynchronous-copy/MMA
pipelines over TMA/UMMA; larger batches can reverse that ordering. MXFP4 weights can be
dequantized inside the kernel into INT8/FP8 compute formats on pre-Blackwell hardware such as
H200. Low-bit storage does not require the device to compute natively in the stored format.

**Reported support:** NVIDIA Turing onward and T-Head Zhenwu 810E, subject to format/hardware
constraints. Executability differs from peak-performance support: B300 INT8 can use older
MMA instructions but not its UMMA path. The reported hidden Blackwell formats `float4e0m3`
and `float8e3m4` do not extend to Rubin. Support matrices are images in the clipping, so this
summary does not reconstruct an exhaustive compatibility table.

| Measurement | Reported result and boundary |
| --- | --- |
| One W4A16 kernel compilation, H200, CUDA 13.4, caches disabled | CUTLASS/NVCC **23.35 s**; Humming/NVCC **1.82 s**; Humming/NVRTC **1.88 s** |
| Compile and load all supported M sizes for one layer's GEMM | About **2-4 s** with parallel warmup compilation; not full-model cold-start time |
| Kernel microbenchmarks | M powers of two from **1 to 8192**, warmed kernels, cold L2, samples separated by pauses; MoE measures Gateup plus Down GEMM |
| DeepSeek-V4.1-Flash, **8 H20**, **TP=8**, concurrency **1-64** | Reported throughput gain **14%-43%**, mean time-to-first-token reduction **25%-32%** |
| Same serving test, concurrency **64** | Output **442.37 to 633.94 tokens/s**; mean time per output token **123.25 to 85.70 ms** |

The serving comparison keeps MXFP4 weights but changes **both backend and activation
precision**: Marlin W4A16/BF16 activations versus Humming W4A8/tokenwise FP8 activations.
It is not a backend-only ablation. The clipping supplies no accompanying task-quality
evaluation establishing that this activation change is behaviorally neutral.

Starting with vLLM **0.29.0**, CUDA installs reportedly include Humming. `--linear-backend`
and `--moe-backend` select execution; `--quantization humming` is a compatibility-loading
path for otherwise unsupported formats, not the general enablement flag. Unsupported
activation compute can fall back to a higher precision. The approximately **500 KB** wheel
does not include every compiled kernel or remove the CUDA compiler/runtime requirements.

## Why it matters

[[Model Quantization and Efficiency]] needs three separate contracts: stored format, execution
precision, and measured quality. [[GPU Kernel Optimization]] gains a compositional alternative
to a separate kernel per format. [[Inference Serving Engines]] must account for preprocessing,
compilation, dispatch, and fallback, while [[Serving Benchmarks and Goodput]] keeps kernel,
startup, and serving numbers separate.

## Tensions / open questions

- All results are developer/community reports, not independently reproduced here.
- The multi-fold kernel gains against Marlin, FlashInfer, DeepGEMM, or cuBLAS use different
  shapes, precisions, devices, and baselines; none is a whole-model multiplier.
- The serving table reports means and throughput, not tail-latency goodput or accuracy parity.
  Prompt/output distributions and a task-quality method are not specified in the captured prose.
- Heuristic defaults, native support, fallback execution, and planned autotuning are distinct.
  General CUDA compatibility does not establish arbitrary-device support.

## Affected pages

- [[Model Quantization and Efficiency]]
- [[GPU Kernel Optimization]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]

## Raw capture

- [[Announcing Humming Fast, Flexible Kernels for Quantized Inference]]

## Citations

- Captured article: <https://vllm.ai/blog/2026-10-21-humming>.
- Published October 21; captured October 23, 2026. Tracking query removed from the summary URL.
- Linked implementation, not executed or independently inspected:
  <https://github.com/vllm-project/humming>.

## Related pages

- [[Model Quantization and Efficiency]]
- [[GPU Kernel Optimization]]
- [[Inference Serving Engines]]
- [[Serving Benchmarks and Goodput]]
- [[Mixture of Experts]]
- [[Arithmetic Intensity and the Roofline Model]]
