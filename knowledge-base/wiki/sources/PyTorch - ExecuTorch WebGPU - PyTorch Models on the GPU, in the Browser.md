---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-11-pytorch-executorch-webgpu
source_title: "ExecuTorch WebGPU: PyTorch Models on the GPU, in the Browser"
source_author: bsterling
source_url: https://pytorch.org/blog/executorch-webgpu-pytorch-models-on-the-gpu-in-the-browser/
tags:
  - source/summary
  - on-device
  - inference
  - pytorch
source_ids:
  - src-2026-11-11-pytorch-executorch-webgpu
status: active
---

# ExecuTorch WebGPU - PyTorch Models on the GPU, in the Browser

## Summary

This PyTorch blog post announces a WebGPU backend for ExecuTorch. A model exported with
`torch.export` becomes an ExecuTorch `.pte` file. The same file then runs on the GPU inside any
WebGPU-enabled browser, with no conversion to another framework's format such as GGUF, ONNX or
TFLite. The runtime compiles to WebAssembly, and the backend runs the model as WGSL compute
shaders. The post reports **4–7x** faster prefill and **2–10x** faster decode than ExecuTorch's
own WebAssembly CPU path, measured on one Apple M1 Pro machine. It lists LLMs, a
vision-language model, vision, speech and text-to-speech models validated on the backend, plus
on-device fine-tuning. The backend is described as "still in early development".

## Key claims

### One exported artifact, translated per platform

- Models export through `torch.export()` and a **WebGPUPartitioner**, and run as WGSL compute
  shaders. At runtime, the backend allocates GPU buffers and dispatches shaders into command buffers.
- **Dynamic shapes** use **allocate-at-max buffers** with per-dispatch workgroup recalculation, which
  enables batched prefill. The runtime also routes shapes to specialized WGSL kernels.
- One `.pte` file runs in WebGPU browsers such as Chrome and Safari, and natively on Metal (macOS),
  Vulkan (Linux/Android) and D3D12 (Windows). WGSL is translated to Metal Shading Language, SPIR-V or
  HLSL depending on the platform.
- For the browser, the C++ runtime compiles to WebAssembly via **Emscripten**, and `emdawnwebgpu`
  bridges its WebGPU calls to the browser's WebGPU JavaScript API. Deployment is a `.pte` file served
  over a CDN; data stays in GPU memory inside the tab.

### Why the browser

- The post calls the web the largest deployment surface, with billions of users on Chrome, Firefox
  and Safari. Keeping prompts, inputs and outputs on the device is presented as a privacy gain that
  also cuts network latency, enables offline use and lowers server inference cost.
- WebGPU, "the modern successor to WebGL", provides compute shaders, shared memory, storage buffers
  and barriers, which the post says make it viable for high-performance ML inference.

### Performance, under stated conditions

- Against ExecuTorch's WebAssembly CPU backend (XNNPACK, multi-threaded), WebGPU was **4–7x** faster
  on prefill and **2–10x** faster on decode.
- Conditions: quantized **Llama 3.2 1B** and **Qwen3-0.6B** in Google Chrome on an **Apple M1 Pro**;
  median of **5 runs after 3 warmups**; **128 to 8K** tokens of context; identical token IDs for both
  backends; wall-clock timing, because GPU timestamps are unavailable for CPU execution.
- The two paths are quantized differently. WebGPU uses **4-bit groupwise weights (group size 64)
  with fp32 activations**. The CPU path uses XNNPACK's **4-bit weights with 8-bit dynamic
  activations**.

### Models validated

- **LLMs:** Llama 3.2 1B, Qwen2.5-0.5B and Qwen3-0.6B (4-bit quantized), and Gemma 3 1B.
- **Vision-language:** SmolVLM (image question answering and captioning).
- **Vision:** Depth Anything V2, SAM 2.1 Hiera Tiny, D-FINE, Real-ESRGAN and MODNet background
  removal.
- **Voice:** Whisper base (speech-to-text) and Phonon-31M-EN (text-to-speech).
- **On-device training:** LoRA and DiReFT fine-tuning for Llama 3.2 1B, Qwen2.5 0.5B and Qwen3 0.6B,
  aimed at personalized assistants and domain adaptation.
- The post says this range shows operator coverage generalizing beyond autoregressive text
  generation. Each model's Hugging Face repo, under `executorch-community`, holds the `.pte` files, a
  model card and the exact export recipe. A Playground at executorch.ai runs many of the models.

## Why it matters

The post adds a browser tier to [[On-Device Reasoning]]: the browser tab becomes the device, and
the local GPU is reached through a web standard rather than a native install. It extends
[[PyTorch]]'s story beyond the datacenter: an export path that stays inside the PyTorch toolchain
instead of converting to GGUF or ONNX. Its dynamic-shape strategy echoes the bounded dynamism of
TorchTPU. For [[Model Quantization and Efficiency]], it is a
reminder that "4-bit" names a weight format, not a full numeric recipe; the two backends compared
differ in activation precision. [[Hugging Face]] is the distribution channel for the exported
artifacts.

## Tensions / open questions

- **First-party, self-referential benchmark.** The comparison is against ExecuTorch's own CPU
  backend, on one machine (Apple M1 Pro) in one browser (Chrome). No comparison with other browser
  runtimes, native GPU runtimes or other hardware is given.
- **Different quantization recipes.** WebGPU runs fp32 activations and the CPU path 8-bit dynamic
  activations, so the speedup mixes backend and numeric differences. The post reports no accuracy
  comparison between them.
- **Wide ranges, no breakdown in prose.** "2–10x" on decode spans a factor of five. The figure is not
  transcribed, so which model and context length produce each end is unknown here.
- **Coverage claims are listed, not measured.** The vision, speech and training examples are named
  as validated, but the post gives no speed or quality figures for them.
- **Early development.** The post says it will expand operator, data type and model coverage, so
  support beyond the listed models is not established.
- The byline "bsterling" is a username taken from the capture's frontmatter. The capture begins
  with a stray "Featured projects" heading from the site template.

## Affected pages

- [[On-Device Reasoning]]
- [[PyTorch]]
- [[Hugging Face]]
- [[Model Quantization and Efficiency]]

## Raw capture

- [[knowledge-base/raw/sources/ExecuTorch WebGPU PyTorch Models on the GPU, in the Browser]]

## Citations

- Canonical URL: https://pytorch.org/blog/executorch-webgpu-pytorch-models-on-the-gpu-in-the-browser/
  (tracking parameter removed).
- Byline: bsterling. Publisher: PyTorch (blog).
- Published: 2026-11-11. Captured: 2026-11-12.

## Related pages

- [[On-Device Reasoning]]
- [[PyTorch]]
- [[Hugging Face]]
- [[Model Quantization and Efficiency]]
- [[Small Language Models]]
- [[Ebba Simpson - Introducing TorchTPU]]
- [[Halo Research - Sopro V2 On-Device Text-to-Speech]]
- [[Ali Zahid Raja - Your Model Doesn't Have to Fit in Your GPU Anymore]]
- [[Meta]]
