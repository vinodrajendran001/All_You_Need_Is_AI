---
title: "Agentic kernels in production"
source: "https://www.baseten.co/blog/agentic-kernels-in-production/#future-direction"
author:
  - "[[Brian Li]]"
  - "[[Faraz Shahsavan]]"
  - "[[Pankaj Gupta]]"
published: 2026-08-29
created: 2026-09-03
description: "Baseten's agentic kernel optimization framework cuts latency by 42.3% on Qwen-Image and by 15.2% on FLUX.2."
tags:
  - "clippings"
---
![Agentic kernels in production](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787661078-baseten-blog-2026-thumbnails-16.png%3Fauto%3Dformat%26fit%3Dcrop%26h%3D630%26w%3D1200&w=3840&q=100) TL;DR

We’ve built an agentic kernel development framework that identifies model-level optimization opportunities, generates improved kernels, and validates them in our serving stack. On our current models, we’ve improved end-to-end latency by 42.3% on Qwen-Image, 15.2% on FLUX.2, and a 5.5% increase in tok/s on MiniMax M3.

We’ve seen in recent years that agents have become surprisingly capable at kernel development, from ideation to generating kernels from scratch. Existing benchmarks such as [KernelBench](https://github.com/ScalingIntelligence/KernelBench) have made it easier to evaluate how well agents can optimize kernels on isolated general-purpose problems.

However, there’s a gap between winning a kernel benchmark and shipping optimizations into production.

A few reasons why:

1. **The best kernel configuration depends on the production workload.** The kernel that wins on a general benchmark may lose on a specific deployment. Optimizations such as tile shapes, warp-specialization strategy, and CTA configurations respond differently to changes in tensor shape, batch size, sequence length, etc. Kernels like MoE and Attention make this especially visible.
2. **A faster microbenchmark doesn’t necessarily translate to a faster model.** Once your changes are integrated, interactions with downstream dependencies like CUDA graph capture and multi-stream execution can wipe out kernel-level gains or even result in a regression.
3. **Optimizing kernels individually can miss higher-level opportunities.** End-to-end traces often show that only a small subset of kernels have headroom for improvement. The lower-effort wins may come from restructuring the computation around them: fusing operations, eliminating redundant work, or removing pipeline bubbles.
4. **Integrating a new kernel into a production serving engine is nontrivial.** Unlike modifying a standalone torch model, serving engines have interconnected execution paths and dependencies. New kernels must be wired into the correct path, replace existing computation cleanly, and remain compatible with the surrounding runtime.

With this in mind, we’ve created a solution that bridges the gap between benchmarks and production. Given a model and serving engine, our framework can profile the full workload, reason about the best optimizations, and then generate and ship those kernels straight to production.

## The stack: model-level + kernel-level optimizations

The optimization stack divides into two layers:

![Agentic kernel architecture diagram](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787957861-diagram_1_update-2.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Two-track optimization pipeline: model-level work profiles, ranks, and tests candidate changes for end-to-end latency improvements, and kernel-level work benchmarks kernels across variants. Both feed into engine integration and production. The dotted testing loop (microbenchmark, correctness check, ablation tests) determines whether a candidate gets archived or recorded as a dead end.

1. **Model-level optimization:** Understands the full model workload, profiles where time is spent, and proposes changes such as fusion and redundant work elimination.
2. **Per-kernel optimization:** Takes generated and other performance-critical kernels identified in the trace, explores several implementations in parallel, and iterates on the strongest candidate.

The first layer helps expand the search space beyond one-for-one kernel improvements. Rather than only optimizing kernels in isolation, the framework can restructure the execution graph by removing redundant work, reducing intermediate materialization, or combining operations before generating and improving the underlying kernels.

### Learning across optimization runs

Our framework also has a self-improving mechanism: kernels that pass correctness and end-to-end performance checks are retained as reusable candidates, while lessons from both successful and failed attempts are added to an evolving knowledge base alongside workload constraints and integration findings.

This creates a self-improvement loop where each optimization iteration starts from accumulated experience, enabling the agent to generate stronger candidates and converge faster over time.

![Persistent knowledge architecture](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787953994-diagram_2.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Persistent knowledge architecture: successful optimizations get stored in the kernel database with their patch, test cases, benchmarks, and workload data, then feed into the next optimization loop. Both successful and unsuccessful optimizations get summarized into the knowledge base, with successes captured as reusable patterns and failures captured as caveats and root causes.

## Results + case studies

Our initial experiment targeted **diffusion models**, namely **Qwen-Image** and **FLUX.2** served with SGLang on B300 GPUs. The optimizations highlighted below were **identified, proposed, and implemented entirely by our agentic framework.**

![Median per-step denoising time across four model configurations (FLUX.2 FP8, FLUX.2 NVFP4, Qwen-Image FP8, Qwen-Image NVFP4). Every model gets faster moving left to right, with Qwen FP8 showing the largest drop, from 245.6 ms to 141.8 ms.](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787958561-graph_1_update-1.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Median per-step denoising time across four model configurations (FLUX.2 FP8, FLUX.2 NVFP4, Qwen-Image FP8, Qwen-Image NVFP4). Every model gets faster moving left to right, with Qwen FP8 showing the largest drop, from 245.6 ms to 141.8 ms.

## Optimizations on both models

### Optimization #1: Pre-packed FP8 scales

The FP8 paths in Qwen-Image and FLUX.2 were wasting launches converting scale metadata into DeepGEMM’s required format before matrix multiplications. Constant weight scales were repeatedly repacked through sequences of small kernel launches.

We eliminate this overhead by changing the main FP8 activation producers to emit packed scales directly while also moving weight-scale packing to model load time. The numerical computation is unchanged, so outputs remain bit-identical.

For example, at FLUX.2 attention projections:

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787954157-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Baseline

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787954217-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Optimized

Another example at the Qwen-Image feed-forward layer:

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787954268-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Baseline

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787954301-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Optimized

The optimization reduced end-to-end latency by **7.3% on Qwen-Image** and **6.1% on FLUX.2**, with these gains persisting throughout the subsequent FP8 optimizations.

### Optimization #2: Fused QKV projection and epilogue

Both models’ original attention paths compute the image query, key, and value projections independently, despite them all using the same input. This resulted in repeated activation quantization and GEMM setup throughout every attention block.

The optimization merges the three FP8 projections into one GEMM, then fuses bias addition, QK normalization, RoPE, and writes to the joint image-text attention buffers in a single Triton epilogue. NVFP4 still uses separate Q, K, and V GEMMs, as each projection uses a different scale.

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787954336-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Baseline

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787954438-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Optimized

### Optimization #3: Normalization + quantization kernel fusion

In both models, normalization previously produced a large BF16 tensor that the following quantization kernel immediately reads back. Thus, the fix was to simply fuse these together, eliminating the intermediate BF16 write-and-read round trip.

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955110-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Baseline

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955145-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Optimized

On Qwen-Image, the fused kernel emits both the original BF16 result and pre-quantized FP8 activations for the QKV and feed-forward GEMMs. This reduces latency by **4.3%** and creates the producer path used by the packed-scale optimization.

On FLUX.2’s residual path, the fused kernel emits the normalized output, updated residual, packed E2M1 values, and swizzled E4M3 scales in one pass. This improves end-to-end latency by **0.7%.**

## Qwen-Image

### Optimization #1: Bias absorption

After the previous optimization, there are two standalone bias additions remaining after the attention and feed-forward output projections, which account for roughly 11% of Qwen’s FP8 step time. To address this, we fold each bias into the next fused operation (residual normalization scale and residual update), reducing latency by **5.2%**.

### Optimization #2: CFG modulation cache

Classifier-free guidance runs two denoiser passes at the same timestep. Each pass uses different conditioning (one receives the prompt $c$, while the other receives an empty or negative prompt $\varnothing$). The previous implementation recomputed the same timestep-only image and text modulation branches in both passes:

$$
\epsilon_{\text{cond}} = F(x_t, t, c), \qquad \epsilon_{\text{uncond}} = F(x_t, t, \varnothing)
$$
 
$$
\epsilon_{\text{CFG}} = \epsilon_{\text{uncond}} + w\left(\epsilon_{\text{cond}} - \epsilon_{\text{uncond}}\right)
$$

The noisy latent $x_t$ and timestep $t$ are shared by both passes. The image and text modulation branches are functions only of the timestep embedding and fixed model parameters, not the prompt:

$$
e_t = \text{Embed}(t)
$$

and so:

$$
m_{\text{image}} = W_{\text{image}} e_t + b_{\text{image}}, \qquad m_{\text{text}} = W_{\text{text}} e_t + b_{\text{text}}
$$

Because these modulation branches depend only on $e_t$ and fixed weights, their outputs are identical across the conditional and unconditional passes at the same timestep, making it cacheable. Prompt-dependent outputs like hidden states and attention are computed separately.

**Create cache key at DiT entry** (the same `timestep` object is passed to both CFG branches):

```python
def _cfg_cache_optimization_enabled(active) -> bool:
    return active

# QwenImageTransformer2DModel.forward
if _cfg_cache_optimization_enabled() and isinstance(timestep, torch.Tensor):
    # Both CFG branches receive the same timestep tensor.
        # Keep a reference to it so tensor identity can be used safely.
        cache_key = {
        "timestep": timestep,
        "version": version_if_available(timestep), 
        }
```

**Cache the image and text modulation outputs in each block:**

```python
# QwenImageTransformerBlock.forward
cached = getattr(self, "modulation_cache", None)

cache_hit = (
    cache_key is not None
    and cached is not None
    and cached["timestep"] is cache_key["timestep"]
    and cached["version"] == cache_key["version"]
)

if cache_hit:
    # Second CFG pass: reuse the cached outputs.
    image_modulation = cached["image_modulation"]
    text_modulation = cached["text_modulation"]

else:
    # First CFG pass: compute the modulation outputs.
    image_modulation = image_modulation_GEMM(timestep_embedding)
    text_modulation = text_modulation_GEMM(timestep_embedding)

    # Cache them for the second CFG pass.
    if cache_key is not None:
        self.modulation_cache = {
            "timestep": cache_key["timestep"],
            "version": cache_key["version"],
            "image_modulation": image_modulation,
            "text_modulation": text_modulation,
        }
```

This contributes to a reduction in latency of **2.1% for FP8** and **3.1% for NVFP4**.

### Optimization #3: Per-kernel optimization

We then run an optimization pass on performance-critical and previously fused kernels, producing the following improvements:

These per-kernel optimizations improve latency by **7.6%** for FP8 and **13.4%** for NVFP4.

![Qwen-Image, cumulative ms/step saved](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955583-graph_3-1.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75)

## FLUX.2

### Optimization #1: Single-block QK normalization + RoPE

FLUX.2’s single-stream transformer block didn’t use the production fused QK-normalization and RoPE kernel because of a Python contiguity guard that rejected the merged-GEMM views. The fallback ran QK RMSNorm and interleaved RoPE as separate passes, which repeatedly concatenated the cosine and sine caches.

The new replacement is a per-token-CTA kernel that loads each contiguous 12 KB Q/K head tile, performs RMSNorm in FP32, rounds the result to BF16, and applies interleaved RoPE in the same pass. It reads the cosine and sine tensors directly, eliminating 48 of 60 cache concatenations per step.

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955634-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Baseline

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955665-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Optimized

The fused kernel offers a **2× speedup**, resulting in end-to-end latency improvements of **2.3% for FP8** and **4.0% for NVFP4**.

### Optimization #2: Fused SwiGLU + FP8/NVFP4 quantization

Each invocation of SwiGLU previously produced a large BF16 intermediate that a separate FP8 or NVFP4 quantization kernel read for the output projection. Some single blocks also launched another operation to join attention features with the SwiGLU output.

This optimization replaces those multi-stage paths with a single fused kernel that performs the aforementioned steps in one pass:

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955697-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Baseline

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955722-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Optimized

For FP8, matching production exactly requires preserving the original operation order: compute SiLU using division, round to BF16, multiply in BF16, and derive the FP8 scale from the stored BF16 result.

For NVFP4, the same fused path directly emits the packed E2M1 values and swizzled E4M3 scales required by the downstream FP4 GEMM. This eliminates the intermediate BF16 write-and-read round trip, contiguous copy, and multiple standalone kernel launches.

The fused kernel reduces latency by **2.3% for FP8** and **3.8% for NVFP4**.

### Optimization #3: Gated residual normalization

FLUX.2’s residual path previously ran the gated residual update and layer normalization as two separate operations. The previous production stack didn’t support FLUX.2’s gate, leaving the model on the unfused path.

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955750-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Baseline

![GPU profiler trace](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787955770-image.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75) Optimized

The new kernel fuses the gate multiplication, residual update, normalization, and scale/shift into one operation, reducing latency by **1.2% for FP8** and **2.3% for NVFP4**.

### Optimization #4: Per-kernel optimization

Similar to Qwen-Image, we run another per-kernel optimization loop that identifies the following improvements:

Together, these kernels reduced NVFP4 latency by **2.8%** and FP8 latency by **1.9%**.

![FLUX.2 cumulative ms/step saved](https://www.baseten.co/_next/image/?url=https%3A%2F%2Fwww.datocms-assets.com%2F104802%2F1787956154-graph_2-2.png%3Fauto%3Dformat%26w%3D1200&w=3840&q=75)

## Future direction

The framework is designed to be model- and engine-agnostic, allowing the same optimization loop to be applied across various serving stacks. We have already begun expanding into LLM optimization, where kernel implementations are considerably more mature and leave less headroom for improvement. Despite this, early results show up to **5.5% tok/s improvements** on models such as MiniMax M3 and GLM-5.2 on vLLM (Stay tuned!).

As the harness and production integration continue to improve, we see a path toward automatically generating kernels that are specialized for the workloads that actually matter given a specific model, hardware platform, tensor shapes, and serving patterns. Rather than relying solely on generic kernels, each deployment could continuously evolve toward the implementation best suited to its real traffic.