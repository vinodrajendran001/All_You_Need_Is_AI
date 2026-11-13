---
type: entity
created: 2026-10-23
updated: 2026-11-13
entity_kind: open-source project
tags:
  - entity
  - frameworks
  - accelerators
source_ids:
  - src-2026-10-21-simpson-torchtpu
  - src-2026-11-11-pytorch-executorch-webgpu
status: active
---

# PyTorch

## What it is

The dominant open-source deep-learning framework, and — more relevantly for this vault — a **dispatcher
architecture that other hardware vendors can attach to**. Its `PrivateUse1` dispatcher key, `at::Tensor`
/ `StorageImpl` storage model, Dynamo FX graphs, `torch.compile()`, and Process Group collectives are
the extension points that make a new accelerator backend possible without forking the framework.

## Why it matters here

PyTorch enters the vault through [[Ebba Simpson - Introducing TorchTPU]], and the reason it deserves its
own page is that the announcement makes the framework's role visible: **PyTorch is the compatibility
surface that determines whether an accelerator is usable**.

TorchTPU's stated goal — that `.to("tpu")` should be the only change an existing program needs — is a
claim about **PyTorch's abstraction boundary holding** across a radically different hardware target with
a proprietary instruction set. Registering as a native dispatcher backend rather than sitting outside
the dispatcher is what buys eager execution, standard tensor semantics, and `torch.compile` support;
the contrast drawn with the earlier lazy-tensor integration (explicitly marked compilable regions, high
compile latency, no native eager mode, lagging distributed features) is a direct argument that **where
you attach to the framework determines what you can offer**.

This is the practical content of [[Accelerator Software Externalization]]: hardware differentiation is
real, but adoption runs through the framework, and the framework's abstractions are what a vendor must
satisfy. See also [[AI Accelerator Architecture]] and [[Open Model Ecosystems]].

## Notes

### Coverage as the unit of compatibility

The vault's source measures backend readiness in **framework terms rather than hardware terms**: roughly
**450 ATen ops**, the **5,000 most-downloaded Hugging Face models**, and a validation corpus of
**4,917 models across 500+ architecture families** with a 98% Tier 1 pass rate and 97% numerical parity
with GPU on the Tier 2 subset. Operator coverage and model-corpus pass rates are the currency, which is
itself a statement about where the ecosystem's gravity sits.

### The abstraction leaks under distribution

Three details show the boundary is not free:

- **One process per device** is enforced, a constraint the framework does not otherwise impose.
- **Skinny Collectives**, which isolate collectives into separate modules to prevent cross-rank graph
  inconsistency, are reported to cost **30–40% end-to-end** performance — with no stated configuration.
- Dynamic shapes require **bounded dynamism** (compile-time maximum buffers with runtime logical
  dimensions), still in development, with `torch.compile` currently forcing `dynamic=False`.

Portability and performance are therefore separate achievements, and the vault's source is candid about
it: moving a workload is not the same as making it fast. Several of its comparisons show the PyTorch
path slightly **behind** a JAX baseline on the same hardware.

### The same strategy in the browser

[[PyTorch - ExecuTorch WebGPU - PyTorch Models on the GPU, in the Browser]] shows the compatibility
argument at the other end of the hardware range. PyTorch's ExecuTorch gains a WebGPU backend: a
model is exported once with `torch.export` and a `WebGPUPartitioner` to a `.pte` file that runs in
WebGPU-enabled browsers. The post makes the same case as TorchTPU. Running a PyTorch model in a
browser usually meant converting it to another framework's format, such as GGUF, ONNX or TFLite,
and the new backend lets models "reach the browser without leaving the PyTorch toolchain".
Compatibility is again stated as model coverage: LLMs, a vision-language model, segmentation,
depth, object detection, super-resolution, speech-to-text and text-to-speech, published as `.pte`
files on [[Hugging Face]].

The dynamic-shape solution resembles TorchTPU's. TorchTPU's bounded dynamism compiles maximum
buffers with runtime logical dimensions; ExecuTorch WebGPU allocates buffers at their maximum size
and recalculates workgroups per dispatch. Two backends on very different hardware handle variable
shapes by reserving the worst case, which is a pattern across two sources rather than a framework
rule. The performance evidence is narrower than TorchTPU's: one Apple M1 Pro in Chrome, measured
only against ExecuTorch's own WebAssembly CPU path (**4-7x** faster prefill, **2-10x** faster
decode), and the post calls the backend "still in early development". See
[[On-Device Reasoning]].

## Related pages

- [[Accelerator Software Externalization]]
- [[AI Accelerator Architecture]]
- [[Distributed Training Parallelism]]
- [[GPU Kernel Optimization]]
- [[Open Model Ecosystems]]
- [[ML Systems at Scale]]
- [[Ebba Simpson - Introducing TorchTPU]]
- [[Google Cloud]]
- [[Meta]]
- [[PyTorch - ExecuTorch WebGPU - PyTorch Models on the GPU, in the Browser]]
- [[On-Device Reasoning]]
- [[Hugging Face]]
- [[Model Quantization and Efficiency]]
