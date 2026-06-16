---
title: "KV Cache & TurboQuant — Prateek Singh PhD"
source: "https://prateeksinghphd.in/kvcache-full-blog.html"
author:
published:
created: 2026-06-16
description:
tags:
  - "clippings"
---
## KV Cache:Why Your GPU RunsOut of Memory

Step 1

## How a model actually writes text

Think of an LLM like an author who can only write **one word at a time**, and every new word depends on everything written before it. Press play to watch it happen.

Token Generation — one at a time

The

cat

sat

on

the

mat

and

purred

✓ 8 tokens written

Every token the model outputs becomes part of the input for the **next** prediction. The context window grows with every step — and so does the work attention has to do.

Step 2

## The problem: reading the whole book every time

Here's where it gets wasteful. Pick an analogy that clicks for you:

WITHOUT CACHE

Imagine you're reading a novel. Every time you finish a sentence, you close the book, go back to page 1, and re-read everything — just to write the next sentence. That's exactly what naive attention does.

WITH KV CACHE

KV Cache is like using a highlighter and sticky notes. You read each page once, mark the important bits, and just glance at your notes for context. You never re-read page 1 again.

In attention, the "re-reading" is computing **Keys** and **Values** for every past token — from scratch — every single generation step. Token 1001? Compute 1000 K,V pairs. Token 1002? Compute 1001. Again. And again.

Step 3

## Naive vs KV Cache, side by side

Watch both approaches generate the same sentence. Every row on the left is **wasted work** — the right computes each K,V exactly once.

✗ Naive — recompute everything

K,V(The)

K,V(The)K,V(cat)

K,V(The)K,V(cat)K,V(sat)

K,V(The)K,V(cat)K,V(sat)K,V(on)

K,V(The)K,V(cat)K,V(sat)K,V(on)K,V(the)

K,V(The)K,V(cat)K,V(sat)K,V(on)K,V(the)K,V(mat)

K,V(The)K,V(cat)K,V(sat)K,V(on)K,V(the)K,V(mat)K,V(and)

Total: 28 K,V ops

✓ KV Cache — compute once, reuse

K,V(The)cached ✓

K,V(cat)cached ✓

K,V(sat)cached ✓

K,V(on)cached ✓

K,V(the)cached ✓

K,V(mat)cached ✓

K,V(and)← new

Total: 7 K,V ops

Ops saved:

75%

75%

Step 4

## How much faster is it?

Short contexts: modest speedup. Long contexts: the difference is **enormous**. At 10k tokens the naive approach computes ~50 million K,V operations. KV Cache computes exactly 10,000.

Speed Race — generating 20 tokens

🐢 Naive (recompute) 20/20

🚀 KV Cache 20/20

🚀 KV Cache finished ~4× faster. At 10k tokens, this gap becomes 10–100×.

Step 5

## But storage isn't free

The cache stores K and V tensors for every token, every layer, every head. Drag the sliders — see how quickly it eats your GPU memory.

KV Cache Size Calculator

Context tokens

512

Layers

32

Head dim (d)

128

2 (K+V) × 512 tokens × 32 layers × 128 dim × 2 bytes (fp16) = 8.0 MB

% of a 24 GB GPU used by KV cache alone

✓ Manageable — try pushing tokens to 32k or 128k.

**This is why long contexts are expensive.** Double the tokens → double the cache. A 128k context on LLaMA-3-70B can demand 30–80 GB for the KV cache alone, before you've even loaded the model weights.

## The one-line summary

KV Cache trades repeated compute for memory storage — giving you speed at the cost of GPU RAM. The smarter the cache management, the longer the context your model can handle without running out of memory.

What researchers did next

## So people tried to fix the memory problem

KV Cache solved compute. But the memory wall remained. Over the next few years, five major research directions emerged — each attacking the problem from a different angle. None of them is perfect alone.

🗑️

Token Eviction H2O · StreamingLLM

Identify which cached tokens are "unimportant" using attention scores, then permanently delete them. Only the most-attended tokens survive.

✓ Up to 10× compression ✗ Permanently loses context — risky for retrieval tasks

📄

Paged Allocation vLLM · PagedAttention

Don't change what's stored — change how memory is allocated. Instead of pre-reserving huge contiguous blocks, allocate small pages on demand. Eliminates fragmentation entirely.

✓ Memory utilization 33% → 99% ✗ Values still stored at full FP16 precision

🏗️

Architecture-Level Sharing GQA · MQA · MLA

Redesign the model itself to need fewer K,V heads. Grouped Query Attention (used in LLaMA 3) shares KV heads across query groups, giving a 4–8× reduction. DeepSeek's MLA projects into a latent space for 64× compression.

✓ 4–64× reduction, no quality loss ✗ Must be baked in at training time — can't apply post-hoc

🔮

Predictive Skipping SnapKV · PyramidKV

Use early-layer attention patterns to predict which tokens will matter in later layers. Skip computing or storing the ones predicted as unimportant.

✓ Moderate compression, task-adaptive ✗ Prediction errors compound — depends heavily on task type

🗜️

Simple INT8 Quantization Naive Quant

Store each K,V value in 8 bits instead of 16. No architecture changes, no retraining, drop-in replacement. Gets you a free 2× memory reduction with acceptable quality.

✓ Easy, safe, works everywhere ✗ Only 2×. Goes bad fast below 4 bits

ICLR 2026 · Google

Coming up in Part 2

### TurboQuant: the missing piece

All five methods above leave something on the table. What if you could compress KV values to **3 bits** — 5× smaller than INT8, 5.3× smaller than FP16 — without losing any tokens, without retraining, and with less than 0.6 point quality drop on every benchmark?

That's what TurboQuant does. It's a three-step mathematical pipeline — random rotation, optimal scalar quantization, and bias correction — that pushes into bit-depth territory where all previous approaches fail. Google published it at ICLR 2026. We break it down completely in Part 2.

6×

memory reduction

<0.3pt

quality drop at 4-bit

0

retraining required

5×

more concurrent users

## TurboQuant:Shrink the Cache6× Without Losing Quality

The Problem

## Real numbers on a real problem

We know the KV cache grows linearly with context. Now let's see the actual GB numbers that motivate compression.

KV Cache Memory (FP16) per request — hover rows

| Model | 4K tokens | 32K tokens | 100K tokens | 1M tokens |
| --- | --- | --- | --- | --- |
| LLaMA 3 8B | 537 MB | 4.3 GB | 13.1 GB | 131 GB 💥 |
| LLaMA 3 70B | 1.3 GB | 10.7 GB | 32.8 GB ⚠ | 327 GB 💥 |
| Mistral 7B | 537 MB | 4.3 GB | 13.1 GB | 131 GB 💥 |

An A100 80GB GPU has ~30–40 GB left after loading 70B weights. At 100K context, you can *barely serve one user* before OOM.

With TurboQuant (3-bit, ~5× reduction)

| Model | 4K tokens | 32K tokens | 100K tokens | 1M tokens |
| --- | --- | --- | --- | --- |
| LLaMA 3 8B | 107 MB | 859 MB | 2.6 GB | 26.2 GB |
| LLaMA 3 70B | 268 MB | 2.1 GB | 6.6 GB | 65.5 GB |
| Mistral 7B | 107 MB | 859 MB | 2.6 GB | 26.2 GB |

LLaMA 3 70B at 100K drops from 32.8 GB to 6.6 GB. Same GPU now serves **5 concurrent users** instead of 1.

The Algorithm

## TurboQuant's 3-step pipeline

Each step solves a specific problem the previous step reveals. You can't skip any of them.

STEP 1

🌀 Random Rotation

Spreads lopsided KV values evenly across all dimensions using a Hadamard transform.

Result: balanced distribution

›

STEP 2

📦 Scalar Quantization

Maps rotated FP16 values to 3-bit centroids using Lloyd-Max Gaussian codebooks.

Result: 5.3× smaller storage

›

STEP 3

🔧 QJL Bias Correction

Uses 1-bit sign sketches (Johnson-Lindenstrauss) to cancel systematic quantization error.

Result: attention scores preserved

Deep Dive — Step 1

## The lopsided distribution problem

Raw KV vectors are not evenly distributed. A few dimensions dominate with huge values. If you try to quantize this directly to 3 bits, you waste all your resolution on those outliers — the small dimensions lose all precision.

Raw KV vector vs After Rotation — click to rotate

7.7

0

6.5

1

0.1

2

4.9

3

0.1

4

0.3

5

0.1

6

0.3

7

0.1

8

0.1

9

0.2

10

0.2

11

0.3

12

0.2

13

0.0

14

0.1

15

**The key insight:** A random orthogonal rotation preserves all inner products (the geometric structure stays identical) but spreads the energy evenly across all dimensions. After rotation, no single dimension dominates — the uniform quantizer can work efficiently.

Deep Dive — Step 2

## How 3-bit quantization actually works

After rotation, values follow a near-Gaussian distribution. Instead of 16 bits (65,536 levels), we only need 3 bits (8 levels). We store the *index* of the nearest centroid, not the value itself.

Quantization Error vs Bit Depth — interactive

| Bits | Levels | Avg Error | Compression | Quality |
| --- | --- | --- | --- | --- |
| 16 (FP16) | 65,536 | ~0 | 1× (baseline) | ████████ Perfect |
| 8 | 256 | 0.005 | 2× smaller | ███████░ Excellent |
| **4 (TurboQuant)** | 16 | 0.094 | **4× smaller** | █████░░░ Great ✓ |
| **3 (sweet spot)** | 8 | 0.177 | **5.3× smaller** | ████░░░░ Good ✓ |
| 2 | 4 | 0.494 | 8× smaller | ██░░░░░░ Risky |
| 1 | 2 | 1.700 | 16× smaller | █░░░░░░░ Broken |

// FP16 vs 3-bit storage for a single value FP16: 3.14159 → stored as 0100001001001000 (16 bits, 2 bytes) 3-bit: 3.14159 → centroid index 5 → stored as 101 (3 bits, 0.375 bytes) Compression: 5.3×

Deep Dive — Step 3

## The hidden danger: quantization bias

Even after rotation, 3-bit quantization introduces a **systematic bias** in attention scores. A 25% error in one attention score can shift which token the model "looks at" — causing hallucinations in long contexts.

Attention score error before and after QJL correction

| Bits | True Score | Quantized Score | Error | After QJL |
| --- | --- | --- | --- | --- |
| 8-bit | \-8.57 | \-8.62 | 0.5% | ~0 ✓ |
| 4-bit | \-8.57 | \-8.97 | 4.7% | 0.1 ✓ |
| 3-bit (no fix) | \-8.57 | \-6.42 | 25.1% ✗ | 0.54 ✓ |
| 2-bit | \-8.57 | \-8.76 | 2.2% | 0.05 ✓ |

Token ranking recovery — watch QJL fix the wrong rankings

Press ▶ to animate the ranking recovery.

**Johnson-Lindenstrauss insight:** Store just 1 bit per random projection of each Key vector (sign: +1 or -1). These 64 bits form an *unbiased estimator* of the true attention score. Across thousands of tokens, individual sign-bit errors cancel out statistically. The attention ranking is fully recovered.

The Math

## What actually gets stored

For one attention head with 128 dimensions, here's the complete storage breakdown after TurboQuant:

Original FP16 — 4,096 bits per head (512 bytes)

4,096 bits

TurboQuant compressed — 928 bits per head (116 bytes)

K: 384b

V: 384b

■ K values (3-bit × 128) ■ V values (3-bit × 128) ■ QJL sketch K (64 × 1-bit) ■ QJL sketch V (64 × 1-bit) ■ Scale factors (2 × 16-bit)

4.41× compression

928 bits vs 4,096 bits per head · No quality loss at 4-bit

Results

## Quality benchmarks vs FP16

The 3-bit setting is the sweet spot: 5× compression with quality drops that remain within benchmark noise on most tasks.

Benchmark scores — click a row to highlight

| Benchmark | FP16 | 4-bit TQ | 3-bit TQ | 2-bit TQ | Task |
| --- | --- | --- | --- | --- | --- |
| MMLU (5-shot) | 85.1 | 84.9 | 84.7 | 83.2 | Knowledge |
| HumanEval (code) | 62.2 | 62.0 | 61.8 | 59.1 | Coding |
| GSM8K (math) | 78.4 | 78.1 | 77.8 | 74.2 | Math |
| Needle-in-Haystack | 97.2 | 96.8 | 96.3 | 88.4 | Retrieval |

4-bit TurboQuant: <0.3 point drop — within benchmark noise. 3-bit: <0.6 point drop — the recommended sweet spot for production.

Concurrent users per GPU (LLaMA 3 8B, 30 GB KV budget)

4K context (short chat)

FP16 baseline 55 users

55

TurboQuant 279 users (5.1×)

279

32K context (medium)

FP16 baseline 6 users

6

TurboQuant 34 users (5.7×)

34

100K context (long)

FP16 baseline 2 users

TurboQuant 11 users (5.5×)

11

System Design

## What happens if you skip a step?

The three steps are interdependent. Removing any one causes a specific failure.

✗ Skip rotation, keep quantization

Mathematical failure: outlier dimensions dictate step size. The quantizer wastes all resolution on 3 huge values — 90% of dimensions lose all precision.

→ Complete output degradation at ≤3 bits.

✗ Rotate, but skip QJL correction

Mathematical failure: residual quantization bias systematically skews inner products. Some tokens get consistently over-attended, others ignored.

→ Attention ranking drift. Bias accumulates over long contexts, causing hallucination.

✗ QJL correction without rotation

Mathematical failure: quantization error remains concentrated in massive outlier dimensions. QJL spreads correction effort uniformly — it cannot compensate for concentrated lopsided error.

→ QJL sketch mathematically cannot correct for lopsided error distribution.

Landscape

## TurboQuant vs other KV compression approaches

TurboQuant is **uniquely positioned**: the most aggressive compression available for already-trained models, without permanently losing any tokens.

| Technique | Mechanism | Compression | Loses tokens? | Needs retraining? |
| --- | --- | --- | --- | --- |
| **TurboQuant** | Precision (rotation + quant) | 4–6× | No ✓ | No ✓ |
| H2O / StreamingLLM | Token eviction | Up to 10× | Yes ✗ | No |
| SnapKV / PyramidKV | Layer prediction | Moderate | Partial | No |
| DeepSeek MLA | Latent projection | 64× | No ✓ | Yes ✗ |
| Simple INT8 | 8-bit quant | 2× | No ✓ | No ✓ |

Honest Assessment

## What TurboQuant does NOT do

**1\. No weight compression.** TurboQuant only compresses the KV cache — not the model weights themselves. A LLaMA 3 70B still needs ~140 GB for weights. Use GPTQ/AWQ alongside TurboQuant.

**2\. Minimal benefit below 8K tokens.** The rotation overhead isn't worth it for short contexts. Best value at 16K+ tokens.

**3\. Research stage (ICLR 2026).** Not yet a first-class feature in vLLM or TensorRT-LLM. Requires custom CUDA kernels today.

**4\. The "8× faster" headline uses FP32 baseline, not FP16.** Against a well-optimized FP16 system, the attention speedup is ~2–3×. Memory reduction (6×) is valid regardless of baseline.

## The conclusion

TurboQuant achieves 5× memory compression with under 0.6 point quality loss — turning a service that served 2 concurrent users into one that serves 11, on the same hardware. Long-context AI isn't held back by model intelligence. It's held back by the cost of memory. TurboQuant is one of the techniques that makes those applications economically viable.

Next up: **KurboQuant** — a channel-aware extension to TurboQuant that exploits kurtosis structure in K weights, with per-head heterogeneity and self-calibrating thresholds. Coming soon on [prateeksinghphd.in](https://prateeksinghphd.in/).