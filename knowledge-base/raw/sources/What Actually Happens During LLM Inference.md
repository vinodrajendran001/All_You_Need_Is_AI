---
title: "What Actually Happens During LLM Inference?"
source: "https://medium.com/@nithinellanki/what-actually-happens-during-llm-inference-e9e756715fc8"
author:
  - "[[Nithin]]"
published: 2026-06-25
created: 2026-06-26
description: "More"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*e7BNZPQkm-y5GGhZQaz_IQ.png)

When you run a Large Language Model (LLM), the process is just a long series of math steps. The system reads the model files to generate text without changing any of the underlying data.

Running a model is not a single, uniform task. The moment a user submits a prompt, the workload immediately splits into two completely different steps. Each step hits a totally different performance bottleneck.

First, the system has to process the entire input prompt at the same time. It runs a massive matrix multiplication across thousands of tensor cores at the same time. This workload pushes the execution engines to their absolute limit, meaning your speed is dictated entirely by how fast the processors can run the math.

Second, the system has to switch to generating the output text one token at a time. To create just one single word, the system has to read the entire multi gigabyte model file from VRAM and pass it through the processors. The processor cores end up sitting idle because they are waiting on slow memory bandwidth to deliver the data.

Because the system switches from a heavy math task to a strict memory bottleneck in less than a second, you cannot optimize your code as a single loop. If you want to choose the right serving engines or make your setup run faster, you have to understand exactly how these two phases move data through the processors and memory layers.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*OJdUpowP9RhvV7_NP8dNAQ.png)

## Phase 1: Processing the Input Prompt

This opening step is known as the prefill phase. Because the engine handles the entire input text at once, the mathematical work takes the form of a massive matrix-matrix multiplication (GEMM).

During this time, execution speed is strictly compute bound. Your speed depends entirely on how many floating point operations per second (FLOPS) your GPUs can run.

The main systems goal of this phase is setup. The engine processes the incoming words to calculate the internal attention states of the prompt. It saves these completed states directly into memory as the Key-Value (KV) Cache. By storing these states immediately, the engine ensures it never has to waste time recalculating the prompt words during the rest of the run.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*4IdiDPiiAgceSUrQEDqH-A.png)

## Phase 2: Generating Text Token by Token

Once the KV cache is set up, the engine shifts to the decode phase. The mathematical work changes completely from a wide matrix-matrix layout to a narrow matrix-vector multiplication (GEMV).

To output a single new token, the engine must look at the last generated token, read the entire multi gigabyte model weight file from the storage layer, and load the growing KV cache. This structural shift alters the execution state entirely. The processor cores finish their math instantly and spend the rest of their cycles starved for data, waiting on the physical limits of your High Bandwidth Memory (HBM) lanes.

This creates the core loop bottleneck. The system is entirely memory bandwidth bound, and it must complete this full memory round trip over and over for every single word it outputs.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*lGqDS7j4Me9bNTyVfCn7Lw.png)

## File Loading and Storage Formats

Because memory bandwidth dictates decoding speed, how a model is loaded and stored directly controls performance.

**File Mapping vs Standard RAM Loading  
**Traditional loading allocates a massive block of RAM and reads the entire weight file from disk into memory at boot time, causing long startup delays.

Using ⁠mmap⁠ (memory mapping) fixes this by mapping the weight file directly into the OS virtual memory space. The OS lazily loads pages from storage only when the processor actually calls them during a forward pass. This drops startup times to near-zero and allows multiple processes to share the same physical memory space.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*PxkV4RrM3ys5rmcaT8jhKw.png)

## Weight Compression Formats

Reducing the model file size cuts down the total data moving through the memory lanes during the decode phase:

- **AWQ and EXL2:** These are 4-bit compression methods used for dedicated GPU serving. They speed up the decode phase by keeping important model weights at higher precision while shrinking the rest, dropping the total gigabytes that must travel through the memory lanes for every token.
- **FP8 and NVFP4:** These are native low-precision formats supported directly by modern hardware. FP8 is the current data-center default for Hopper GPUs, while NVFP4 is the newer 4-bit standard for Blackwell chips. They let the processors run math on compressed data natively inside the cores, skipping slow decompression steps.
- **GGUF:** Built specifically for consumer hardware and split CPU/GPU running. If a model is too big for your graphics memory lanes, GGUF lets you spill parts of the model onto standard system RAM so the system can still run.

## Multiple Users and Serving Engines

In production, an inference engine cannot just run a single loop; it must handle hundreds of users simultaneously. Different engines handle this execution pipeline using distinct strategies:

- **vLLM and SGLang:** Focus on dynamic memory management. They use PagedAttention to slice up the KV cache into small blocks, treating VRAM exactly like operating system virtual memory to stop fragmentation.
- **TensorRT-LLM and TGI:** Rely on deep graph compilations and custom kernels to maximize raw token throughput at the silicon layer.

To keep utilization high, these production engines use Continuous Batching. Instead of waiting for a full batch of users to finish generation before starting a new request, they inject new incoming prefill tasks directly into the ongoing decoding loops of existing users.

This introduces a physical conflict on the GPU. Processing a new user prompt requires massive compute power for matrix math. When a new prompt is injected into the active batch, it takes over execution cycles on the tensor cores. Because the math units are fully saturated processing the new prompt, the ongoing text generation loops for existing users are forced to pause, causing a brief drop in their output speed until the new prefill finishes.