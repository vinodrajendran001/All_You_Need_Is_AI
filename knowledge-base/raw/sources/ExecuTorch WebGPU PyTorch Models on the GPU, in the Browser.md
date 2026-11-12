---
title: "ExecuTorch WebGPU: PyTorch Models on the GPU, in the Browser"
source: "https://pytorch.org/blog/executorch-webgpu-pytorch-models-on-the-gpu-in-the-browser/?utm_source=tldrai"
author:
  - "[[bsterling]]"
published: 2026-11-11
created: 2026-11-12
description: "TL;DR PyTorch models now run in the web browser on the GPU through ExecuTorch, with no conversion to another framework’s format. You export with torch.export to an ExecuTorch .pte file,..."
tags:
  - "clippings"
---
### Featured projects

### TL;DR

- PyTorch models now run in the web browser on the GPU through ExecuTorch, with no conversion to another framework’s format. You export with torch.export to an ExecuTorch.pte file, and the same file runs in any [WebGPU](https://webgpu.org/) browser via ExecuTorch’s new [WebGPU backend](https://github.com/pytorch/executorch/tree/main/backends/webgpu).
- It works across a broad range of models: LLMs (e.g. Llama 3.2, Qwen3, Gemma 3), vision-language (e.g. SmolVLM), segmentation, depth, object detection, super-resolution and speech-to-text (e.g. Whisper). Everything runs locally in the tab, and no data leaves the device. Try it in the ExecuTorch WebGPU [Playground](https://executorch.ai/playground).
- On the same machine, WebGPU is 4–7× faster than ExecuTorch’s CPU path (Webassembly + XNNPACK) on prefill and 2–10× faster on decode.

### Why the Browser?

The web is the largest deployment surface with billions of users on Chrome, Firefox and Safari. Browser inference ensures privacy by keeping users’ prompts, model inputs, and outputs on the user’s device rather than the server. This reduces network latency, enables offline use-cases, and lowers server-side inference costs. With the ExecuTorch WebGPU backend, PyTorch models get a native path to GPU-accelerated inference in WebGPU-enabled browsers on desktop, laptop and mobile.

WebGPU, the modern successor to WebGL, provides native compute shaders, shared memory, storage buffers, and barriers, making it viable for high-performance ML inference directly in the browser. Today, running a PyTorch model in the browser usually means first converting it to another framework’s format, such as GGUF, ONNX or TFLite. The ExecuTorch WebGPU backend lets PyTorch models reach the browser without leaving the PyTorch toolchain.

### Backend Design

![](https://pytorch.org/wp-content/uploads/2026/11/pytorch-model-1.jpg)

*\[Figure 1: ExecuTorch WebGPU backend design: a PyTorch model is exported once to a.pte file and runs in any WebGPU browser through the ExecuTorch Wasm runtime\]*

Three principles guided the WebGPU backend’s design:

- Architecture, export, and dynamic runtime. Models export through ExecuTorch’s `torch.export()` and WebGPUPartitioner and run via WGSL compute shaders. At runtime, the WebGPU runtime allocates GPU buffers and dispatches compute shaders into command buffers. Dynamic shapes are handled via allocate-at-max buffers with per-dispatch workgroup recalculation to enable batched prefill, and the runtime routes shapes to specialized WGSL kernels at runtime.
- Same artifact across multiple devices and browsers. One model (.pte file) runs in WebGPU browsers such as Chrome and Safari, natively on Metal (macOS), Vulkan (Linux/Android) and D3D12 (Windows), translating WGSL to Metal Shading Language, SPIR-V or HLSL depending on the platform. For browser deployment, the dynamic C++ runtime compiles to Webassembly via Emscripten and `emdawnwebgpu` bridges its WebGPU API calls to any browser’s WebGPU JavaScript API.
- Zero friction for the end user. With WebGPU, models run in the browser sandbox with no native installation, backend server, and no data leaving the device. For developers, deployment is a.pte file served over CDN on a web page. Pipeline compilation, memory management, and dispatch scheduling are all handled through the WebGPU backend, with all data staying in GPU device memory within the browser tab.

### Performance

We benchmarked ExecuTorch WebGPU against ExecuTorch’s own Webassembly (wasm) CPU backend (XNNPACK, multi-threaded) on the same machine, using quantized Llama 3.2 1B and Qwen3-0.6B in Google Chrome on Apple M1 Pro. Each data point is the median of 5 runs after 3 warmups, across 128 to 8K tokens of context, with identical token IDs for both backends. Both are timed with wall-clock time, since GPU timestamps aren’t available for CPU execution. WebGPU uses 4-bit groupwise weights (group size 64) with fp32 activations; the CPU uses XNNPACK’s 4-bit weights with 8-bit dynamic activations.

![](https://pytorch.org/wp-content/uploads/2026/11/2.png)

*\[Figure 2: ExecuTorch WebGPU is 4–7× faster than ExecuTorch Wasm (XNNPACK) on prefill and 2–10× faster on decode, measured in Chrome on Apple M1 Pro\]*

### Models in Practice

We’ve validated the WebGPU backend across models with very different architectures, demonstrating that the operator coverage generalizes beyond autoregressive text generation:

LLM Inference

- [Llama 3.2 1B (4-bit quantized)](https://huggingface.co/executorch-community/Llama-3.2-1B-Instruct-ExecuTorch-WebGPU)
- [Qwen2.5-0.5B (4-bit quantized)](https://huggingface.co/executorch-community/Qwen2.5-0.5B-Instruct-ExecuTorch-WebGPU)
- [Qwen3-0.6B (4-bit quantized)](https://huggingface.co/executorch-community/Qwen3-0.6B-ExecuTorch-WebGPU)
- [Gemma 3 1B](https://huggingface.co/executorch-community/Gemma-3-1B-IT-ExecuTorch-WebGPU)

Vision-Language Understanding

- [SmolVLM](https://huggingface.co/executorch-community/SmolVLM-500M-Instruct-ExecuTorch-WebGPU): image question answering and captioning

Vision

- [Depth Anything V2](https://huggingface.co/executorch-community/Depth-Anything-V2-Small-ExecuTorch-WebGPU): monocular depth estimation
- [SAM 2 (SAM 2.1 Hiera Tiny)](https://huggingface.co/executorch-community/SAM2-Hiera-Tiny-ExecuTorch-WebGPU): promptable image segmentation
- [D-FINE](https://huggingface.co/executorch-community/D-FINE-Small-COCO-ExecuTorch-WebGPU): object detection
- [Real-ESRGAN](https://huggingface.co/executorch-community/Real-ESRGAN-General-x4v3-ExecuTorch-WebGPU): super-resolution
- [Background Removal (MODNet)](https://huggingface.co/executorch-community/MODNet-ExecuTorch-WebGPU): foreground segmentation

Voice

- [Whisper (base)](https://huggingface.co/executorch-community/Whisper-Base-ExecuTorch-WebGPU): speech-to-text
- [Phonon-31M-EN](https://huggingface.co/executorch-community/Phonon-31M-EN-ExecuTorch-WebGPU): text-to-speech

On-Device Training

- [LoRA and DiReFT fine-tuning](https://github.com/pytorch/executorch/blob/main/backends/webgpu/README.md) for Llama 3.2 1B, Qwen2.5 0.5B and Qwen3 0.6B, aimed at personalized assistants and domain adaptation on-device

*![](https://pytorch.org/wp-content/uploads/2026/11/executorch-webgpu-four-demos-1.gif)*

*\[Figure 3: ExecuTorch WebGPU demonstration\]*

### Try it: ExecuTorch WebGPU Playground

The ExecuTorch WebGPU [Playground](https://executorch.ai/playground/) runs many of the models above, all on the same WebAssembly + WebGPU runtime. All the prompts, photos, camera frames and audio never leave your device. Each model’s Hugging Face repo includes the.pte files, a model card, and the exact export recipe.

### What’s Next

The backend is still in early development. We’ll keep making the backend faster and more stable, and expand operator, data type, and model coverage.

### Contributions / Feedback

ExecuTorch is open source, and we’d love your contributions to the WebGPU backend. If something breaks or a model you care about isn’t supported, open an [issue](https://github.com/pytorch/executorch/issues) or reach us on the [ExecuTorch Discord](https://discord.com/invite/Dh43CKSAdc). Contributions are welcome too, whether that’s new operators, new models or performance improvements.

Learn more at [ExecuTorch Documentation](https://docs.pytorch.org/executorch/main/index.html) | [ExecuTorch repo](https://github.com/pytorch/executorch) | [WebGPU Backend](https://github.com/pytorch/executorch/tree/main/backends/webgpu)