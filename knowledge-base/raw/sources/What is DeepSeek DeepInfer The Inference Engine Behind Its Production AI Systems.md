---
title: "What is DeepSeek DeepInfer? The Inference Engine Behind Its Production AI Systems"
source: "https://medium.com/data-science-in-your-pocket/what-is-deepseek-deepinfer-the-inference-engine-behind-its-production-ai-systems-c91c5070de38"
author:
  - "[[Mehul Gupta]]"
published: 2026-10-20
created: 2026-10-21
description: "DeepSeek open-sourced DeepInfer"
tags:
  - "clippings"
---
## DeepSeek open-sourced DeepInfer

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*ffTzXq3SEefqV6l2)

Photo by Saradasish Pradhan on Unsplash

Most AI developers spend their time choosing a model, quantizing it, and figuring out how to serve it. But when you start running an LLM at the scale of millions of requests, the model itself is only one part of the problem. GPU utilization, memory management, communication between accelerators, scheduling and decoding all start to matter just as much.

> DeepSeek has now open-sourced **DeepInfer**, its high-performance inference framework for large-scale production serving.

The initial release supports DeepSeek-V4.1-Flash and includes several optimizations designed for running models across multiple accelerators rather than on a single GPU.

The interesting part is that DeepSeek is exposing some of the infrastructure behind its own inference stack. This isn’t another chatbot interface or a wrapper around Transformers. It is a lower-level inference engine aimed at developers who need to execute models efficiently at scale.

You can find the source code here: [DeepSeek-AI/DeepInfer on GitHub](https://github.com/deepseek-ai/DeepInfer).

## What exactly is DeepInfer?

> DeepInfer is an inference framework designed to execute DeepSeek models efficiently, particularly in multi-GPU production environments.

The current release supports **DeepSeek-V4.1-Flash** and provides an offline inference path, along with core runtime components for high-throughput serving. There are two important terms to understand here.

- **Prefill:** The stage where the model processes the input prompt and builds the information it needs to generate a response. Long prompts can make this stage computationally expensive.
- **Decode:** The stage where the model generates output tokens, usually one token at a time in an autoregressive generation process. At serving time, the system must balance the speed of each user’s response against the total number of requests it can handle.

These stages behave differently on hardware. Prefill can often take advantage of large parallel matrix operations, while decode is frequently constrained by memory bandwidth, kernel-launch overhead and the need to move data efficiently.

### A good inference engine cannot simply optimize one stage and expect everything else to improve.

DeepInfer includes optimized kernels, scheduling, parallel execution, speculative decoding and deterministic inference features to address different parts of this problem.

## The kernel optimizations are worth paying attention to

DeepInfer integrates several components from DeepSeek’s GPU and accelerator software stack, including FlashMLA, DeepGEMM, DeepEP, TileKernels and DeepSelect, alongside custom TileLang kernels.

These aren’t interchangeable libraries. Each addresses different parts of model execution.

- **FlashMLA** focuses on attention operations built around Multi-head Latent Attention (MLA), an attention architecture used by DeepSeek models. MLA reduces the size of the key-value representations that need to be stored and accessed compared with conventional multi-head attention designs. Efficient attention kernels are important because attention performance can become a bottleneck as context length increases.
- **DeepGEMM** provides optimized general matrix multiplication operations. Matrix multiplication is central to transformer inference, particularly in the linear layers that dominate much of the model’s computation. Improving these kernels can increase hardware utilization and reduce the time spent executing those operations.
- **DeepEP** handles communication for Mixture-of-Experts (MoE) models. In an MoE model, a router selects a subset of experts for each token. When those experts are distributed across GPUs, tokens and intermediate results must move between devices. That communication can become a significant bottleneck, even when the individual experts execute quickly.
- **TileKernels and TileLang** provide additional building blocks for specialized, tiled GPU computation. Rather than executing every operation through a general-purpose implementation, developers can build kernels tailored to the shapes and execution patterns of a particular model.

DeepSelect is another component in this optimized execution stack.

The broader point is that inference performance rarely comes from one magical kernel. It comes from reducing overhead across the entire execution path: attention, matrix multiplication, expert routing, memory movement and synchronization.

## DeepInfer supports multiple forms of parallelism

Running a large model across several accelerators introduces a different set of problems. Splitting computation across devices is useful only if the time spent communicating and synchronizing doesn’t eat up the performance gains. DeepInfer supports several forms of parallel execution.

- **Attention data parallelism (Attention DP)** distributes attention workloads across parallel execution paths. Data parallelism generally allows independent portions of a workload to be processed concurrently, although the precise behavior depends on the implementation and model architecture.
- **Balanced context parallelism (balanced CP)** addresses execution over context tokens. Context parallelism partitions sequence-related work across devices, which becomes particularly relevant for long inputs. Balancing that work matters because one device finishing much later than the others can leave expensive hardware underutilized.
- **Expert parallelism (MoE EP)** distributes experts across multiple accelerators. Instead of placing every expert on every device, the runtime can assign different experts to different devices and route tokens to the appropriate locations.

DeepInfer also supports **Expert Parallelism Load Balancing (EPLB)**. Expert workloads are not always evenly distributed: some experts receive more tokens than others. Load balancing helps avoid situations where one device becomes overloaded while other devices sit comparatively idle. These mechanisms address different bottlenecks, and they can work together.

For an MoE model, for example, expert parallelism distributes the expert computation, while load balancing addresses uneven expert demand. Meanwhile, the attention execution strategy determines how the context-processing workload is distributed.

This is the sort of engineering that becomes important when moving from a single-GPU experiment to a multi-accelerator inference deployment.

## DSpark: Generating tokens faster through speculative decoding

> One of the more interesting features in DeepInfer is its support for **DSpark and confidence-scheduled verification**.

To understand why this matters, consider ordinary autoregressive decoding. The model predicts the next token, adds it to the sequence, and then predicts the next one. Each step requires another pass through the relevant parts of the model.

Even when a model is highly optimized, this sequential dependency limits how quickly it can generate a response. Speculative decoding attempts to reduce that limitation by proposing multiple candidate tokens and checking them with the main model.

A simplified workflow looks like this:

1. A draft mechanism proposes several future tokens.
2. The main model verifies those proposals.
3. Tokens that pass verification can be accepted together.
4. If a proposal fails, generation continues from the appropriate point using the main model’s results.

The important detail is that speculative decoding does not have to sacrifice the target model’s output distribution. With a correctly implemented verification and sampling procedure, it can accelerate generation while preserving the intended sampling behavior.

DSpark adds confidence-scheduled verification to this process. Rather than treating every proposed token sequence identically, the system uses confidence estimates to help schedule verification work.

DeepInfer exposes configuration for variable-length speculative decoding. The repository documents `DEEPINFER_ENABLE_MTP_VARLEN=1` and the `DEEPINFER_USE_NEXTN_DECODE` setting, which controls the maximum draft length and defaults to five.

That doesn’t mean every request will become five times faster. Actual speedups depend on how many draft tokens are accepted, the cost of verification, the workload and the hardware.

Still, reducing the number of expensive sequential decoding steps is an important optimization for latency-sensitive LLM serving.

## Bounded replay: Avoiding unnecessary prefill work

Another feature in DeepInfer is bounded replay for the decoder’s sliding-window attention (SWA) path. This optimization deserves some explanation because it addresses a problem that is easy to overlook.

When a model processes a long sequence, it maintains information from earlier tokens so that subsequent computation can reuse it. In some architectures, attention is limited to a sliding window rather than covering the entire sequence in every operation.

Reprocessing an unnecessarily large portion of the context wastes compute.

DeepInfer supports a bounded replay strategy that replays only a limited suffix of the sequence under the relevant configuration. The repository documents the following settings for its default V4.1 configuration:

```hs
export DEEPINFER_YOCO_PREFILL_TRUNCATION_MODE=compact
export DEEPINFER_YOCO_PREFILL_KEEP_TOKENS=140
```

The retained suffix must cover the sliding-attention window plus the maximum backtracking length required by the implementation.

The distinction matters: this is not simply an instruction to discard arbitrary old tokens. The retained region must be sufficient for the model’s attention and replay requirements.

The potential benefit is less redundant prefill computation. The actual impact depends on the model’s execution path and workload.

## An asynchronous scheduler designed to reduce overhead

Another feature is asynchronous scheduling, which is enabled by default.

Inference serving involves more than GPU kernels. The runtime must decide which requests and token sequences should execute together, prepare batches, coordinate execution and manage the results. If the CPU spends too much time scheduling work while the GPU waits, the system loses performance even if its individual kernels are fast.

DeepInfer’s scheduler is designed to overlap CPU-side batch scheduling with device execution. The repository describes this as a zero-overhead batch scheduler.

That phrase should be interpreted as the project’s design goal, not a guarantee that scheduling has literally zero cost under every workload.

The underlying idea is straightforward: keep preparing the next batch while the accelerator is busy with the current one, reducing idle time between execution steps.

At high request volumes, small amounts of overhead can accumulate into a substantial loss of throughput. Removing those gaps can be just as important as optimizing the mathematical operations themselves.

## Batch-invariant inference and deterministic sampling

DeepInfer also provides batch-invariant inference, which is particularly interesting for evaluation and reproducibility.

In a typical inference server, requests are dynamically grouped into batches. The composition of a batch can change from one execution to another, depending on which requests arrive and when.

Depending on the numerical implementation, different batch compositions can lead to slightly different floating-point results. In an autoregressive model, a small difference at one step can eventually change the generated text.

Batch-invariant inference aims to keep a model’s results identical across different batch compositions. The repository documents the following setting for NVIDIA hardware:

```hs
export DEEPINFER_BATCH_INVARIANT=1
```

DeepInfer also supports deterministic sampling. With the documented configuration, a fixed sequence seed can produce identical outputs for identical inputs and sampling parameters.

For the NVIDIA path, the repository specifies:

```hs
export DEEPINFER_BATCH_INVARIANT=1
export DEEPINFER_ENABLE_MTP_VARLEN=0
```

The sampling configuration must also supply a fixed `seq_seed`.

This is useful for benchmarking, regression testing and debugging model-serving systems. If the same request produces different outputs simply because it was placed in a different batch, it becomes harder to determine whether a software change has introduced a real regression.

There is a trade-off, however. Reproducibility-oriented execution can impose constraints on the available optimizations. The documented settings also disable variable-length MTP decoding, so developers should measure the performance impact before enabling them in production.

These features are NVIDIA-specific in the current documentation.

## Structured outputs without relying entirely on prompting

Another useful feature is constrained structured generation.

If you’ve built an LLM application that expects valid JSON, you’ve probably seen the problem: asking a model to return JSON doesn’t guarantee that the output will be valid JSON.

The model might add an explanation before the object, omit a required field, or generate a value that violates the expected schema. DeepInfer supports structured outputs constrained by regular expressions, JSON Schema or EBNF grammars.

EBNF, or Extended Backus-Naur Form, is a notation for describing the grammar of a language. It can be used to specify which sequences of tokens are allowed in a generated output.

The repository exposes structured-output configuration through `SamplingParams`, using the `so_args` argument. For example, the general configuration pattern looks like this:

```hs
so_args = {
    "schema_type": "...",
    "schema": "...",
}
```

The actual values depend on the constraint type and schema you want to use.

Constrained generation is particularly useful when an LLM sits inside a larger application. A downstream service may expect a particular JSON structure, a tool invocation may require specific fields, or an automated workflow may reject anything that doesn’t follow a defined grammar.

It won’t automatically make the model’s answers factually correct. It helps control the shape of the output, which is a different problem.

## Hardware requirements: This is not a consumer GPU project

This is probably the most important limitation for developers who want to try DeepInfer.

The current release lists support for:

- NVIDIA SM100 GPUs.
- Huawei Ascend 950 NPUs.

The NVIDIA target is the Blackwell-generation SM100 GPU architecture. The repository does not list general support for every CUDA-capable NVIDIA GPU.

That means you should not assume DeepInfer will work on an RTX 4090, RTX 5090, or an older A100 or H100 system simply because those devices can run other LLM inference frameworks.

The documented software prerequisites are:

- Linux.
- GCC 13 or later.
- Python 3.12.
- CUDA 13 for NVIDIA hardware.
- CANN 9.2 for Huawei Ascend hardware.

CANN is Huawei’s software toolkit for its Ascend accelerators.

The project also needs a suitable software environment and the dependencies specified for the selected hardware platform. Given the compiler and accelerator requirements, setting it up is considerably more involved than installing a typical Python inference package.

## How to run DeepInfer

The repository provides an offline inference example, which is the simplest starting point for someone with supported hardware.

First, clone the repository and enter its directory:

```hs
git clone https://github.com/deepseek-ai/DeepInfer.git
cd DeepInfer
```

Create and activate an empty Python 3.12 environment before building.

For the NVIDIA platform, configure the accelerator and run the build script:

```hs
export DEEPINFER_ACCELERATOR=nvidia
./build.sh
```

For the supported Huawei platform, use `ascend` instead of `nvidia` in the environment variable. Once the build is complete, run the example:

```hs
python examples/offline_inference.py
```

By default, the example downloads the `deepseek-ai/DeepSeek-V4.1-Flash-1017` checkpoint into the Hugging Face cache on its first run.

If the model is already available locally, you can point DeepInfer to that directory:

```hs
export DEEPINFER_HF_MODEL_DIR=/path/to/DeepSeek-V4.1-Flash-1017
python examples/offline_inference.py
```

These commands follow the repository’s documented setup. They are not a promise that the build will succeed on arbitrary hardware: the supported accelerator and software versions are essential.

See the [official DeepInfer repository](https://github.com/deepseek-ai/DeepInfer) for the latest instructions, configuration options and examples.

## Does DeepInfer include everything required for production serving?

Not yet.

This is an important distinction because the project describes itself as infrastructure for large-scale inference, but the open-source release does not include every component needed to operate a complete inference service.

The README explicitly identifies several missing pieces.

- **A KV cache system:** The key-value cache stores intermediate attention representations that can be reused during autoregressive generation. Managing this cache is important for memory efficiency, long-context workloads and high request concurrency.
- **Complete prefill/decode disaggregation:** Prefill and decode have different performance characteristics, so production systems may run them on separate pools of accelerators. This is called prefill/decode disaggregation. DeepInfer states that most of the required engine functionality is implemented, but the complete arrangement is not included in the release.
- **Load balancing across data-parallel replicas:** A production deployment may run several copies of an inference engine. Requests need to be distributed across those replicas for both prefill and decode. Without appropriate load balancing, one replica can become overloaded while another has spare capacity.

In other words, DeepInfer provides important pieces of the execution engine, but a complete serving platform still requires additional infrastructure.

That doesn’t make the release less useful. It simply means developers should distinguish between an inference engine and a fully operational production serving stack.

## What do the benchmarks tell us?

DeepInfer includes performance benchmarks for both prefill and decode.

The repository states that its prefill measurements were collected on four SM100 GPUs, while its decode measurements used 64 SM100 GPUs. Each configuration was tested within a single scale-up domain.

These are two different experimental configurations, so their results should not be compared as if they were measurements from the same hardware setup. The project also provides a `run_sweep.sh` script for reproducing the benchmark sweeps.

One thing worth noting: benchmark graphs alone don’t establish how much faster DeepInfer will be than vLLM, SGLang or TensorRT-LLM on a particular deployment. A fair comparison needs the same model, accelerator configuration, precision, context lengths, batch sizes and latency constraints.

I would like to see more independently reproducible comparisons covering time to first token, inter-token latency, total throughput and memory consumption across different request distributions.

Those measurements would help answer a practical question: how much of DeepInfer’s advantage comes from its kernels, how much comes from scheduling, and how much depends on the hardware and model configuration?

For now, treat the repository’s benchmark results as measurements of its documented configurations rather than proof that it is universally faster than competing inference engines.

## DeepInfer builds on existing inference projects

DeepSeek acknowledges that DeepInfer was originally built primarily on vLLM, with additional inspiration from SGLang and TensorRT-LLM.

That is worth mentioning because modern inference systems rarely emerge from a completely isolated software stack. They build on existing execution engines, kernel implementations and scheduling ideas, then adapt them to specific models and deployment requirements.

DeepInfer’s focus is the DeepSeek model family and the execution patterns needed to serve those models efficiently.

The open-source release also makes it possible for developers to inspect the implementation, reproduce supported workloads and contribute improvements under the Apache 2.0 license.

It is not yet a general-purpose replacement for every inference framework. Its current model and hardware support are deliberately narrower.

## Final thoughts

DeepInfer is an interesting release because it shifts the conversation from model weights to the infrastructure required to serve those weights efficiently.

The project brings together optimized attention and matrix-multiplication kernels, expert-parallel execution, speculative decoding, asynchronous scheduling, reproducibility features and constrained generation. Each addresses a different source of overhead in an LLM inference system.

The hardware requirements are restrictive, and the open-source release still leaves several production-serving components to be supplied separately. Developers with consumer GPUs shouldn’t expect to install it and immediately replace their existing inference stack.

But for teams working with supported Blackwell GPUs or Huawei Ascend 950 accelerators, DeepInfer is worth examining. It provides a look at how DeepSeek approaches inference at production scale, including optimizations that go beyond simply making a model run.

**The bigger takeaway is that open-sourcing an AI model and open-sourcing the infrastructure needed to serve it are two different things. DeepInfer is DeepSeek opening up more of the second part.**

GitHub: [https://github.com/deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer)

License: Apache 2.0