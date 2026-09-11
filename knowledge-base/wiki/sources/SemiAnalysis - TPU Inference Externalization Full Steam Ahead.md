---
type: source-summary
created: 2026-09-11
updated: 2026-09-11
source_id: src-2026-09-07-semianalysis-tpu-inferencex
source_title: "TPU Inference Externalization Full Steam Ahead"
source_author: SemiAnalysis
source_url: https://inferencex.semianalysis.com/blog/tpu-inferencex-full-steam
tags:
  - source/summary
  - hardware
  - inference
  - serving
source_ids:
  - src-2026-09-07-semianalysis-tpu-inferencex
status: active
---

# SemiAnalysis - TPU Inference Externalization Full Steam Ahead

## Summary

The first third-party inference benchmarks of Google's **TPUv7 Ironwood**, run on SemiAnalysis's
InferenceX Official Preview with **Qwen3.5 397B in FP8** as the bring-up model. The headline is that
Ironwood delivers **up to 50% better performance per dollar than B200 and B300** — but the article spends
much of its length establishing that this is a statement about specific points on a latency curve rather
than a general ranking, and the vault should hold it that way.

The more durable half is not the benchmark at all. It is the account of **externalization** — what it
takes to make a TPU usable by people who are not Google. Three things are documented: the software stack
being rebuilt (TorchAX replaced by **TorchTPU**), a long catalogue of kernel and memory optimisations
needed for one model, and the hardware's tile geometry quietly constraining which model architectures run
well. The last of these has the widest consequences, and the article names it: **"TPUs Are Picky."**

## Key claims

### The benchmark, with its qualifiers

**At 100 tok/s/user interactivity, Ironwood costs $0.181 per million tokens against B200's $0.222 and
B300's $0.276** — 19% and 34% lower.

**At 20 tok/s/user, Ironwood also leads on raw throughput**: **9,364 tok/s/chip versus 8,903 (B200) and
8,925 (B300)**, which combined with price gives **50.4% more tokens per dollar than B200 and 96.0% more
than B300**.

**At Google's internal TCO the gap widens but the latency does not survive.** At **$1.03/chip-hour** and
concurrency 256 the advantage rises to **76.7% and 130.2%** — but TPU mean TTFT is **5.41s against 3.75s
(B200) and 2.40s (B300)**. SemiAnalysis states the limit explicitly: the figure "applies to this datapoint
specifically, rather than every latency target."

**Normalising on end-to-end response time compresses the advantage sharply.** At a 20-second median
response time Ironwood is **$0.098/M against $0.106 and $0.132** — 8% and 25% lower, not 50%. **Around the
30-second median point B200 wins outright.**

**The most favourable NVIDIA comparison reverses the result.** An "apples-to-bananas" GB300 NVL72
disaggregated configuration against aggregated TPUv7 gives GB300 roughly a **30% perf/$ advantage in the
middle of the curve.**

**Anthropic has committed to over one million TPUs** — about 400k purchased directly and 600k rented via
GCP — and by 2029 surpasses DeepMind's own usage.

### The software stack

**TorchTPU replaces TorchAX**, the third stage of vLLM TPU support: PyTorch/XLA lazy tensor → the
`tpu-inference` backend using JAX with TorchAX → TorchTPU as a native PyTorch `PrivateUse1` device.
Crucially **XLA remains the compiler** — not Inductor or Triton — and existing Pallas kernels carry over.
It is in private beta with open-sourcing expected around mid-October at the PyTorch Conference.

### What one model's bring-up actually cost

The optimisation catalogue is the evidence for how much work externalization is. Selected items:

- **Collective restructuring:** combining two all-gathers saved **~80 µs per layer**, which across 58
  DeepSeek-V3 layers is **4.64 ms per forward pass**.
- **Offloading ReduceScatter to SparseCore** with double buffering gave **4.1–14.2%** higher throughput
  (8.5% at concurrency 256; 26.1% on the 1k8k shape at 512) — but offloading is not always a win, so a
  VMEM-derived threshold keeps small collectives on TensorCore, worth a further +2.7% and +5.7%.
- **MoE routing:** SparseCore rearrangement **+12%**; moving the top-k gather cut TensorCore overhead from
  **29 µs to 14 µs**; a packed sort key took a kernel from **106.6 µs to 21.7 µs**.
- **Gated DeltaNet:** algebraic rearrangement to overlap MXU and VPU (+2.79%/+4.48%); register-spill
  slicing made the decode-64 kernel ~20% faster; async state transfers **+11.3%**; **GDN v3 fuses Conv1D
  and GDN for 1.41× decode, 1.60× prefill and 2.14× mixed — but these are kernel-level figures, not
  end-to-end.**
- **Hybrid-model memory:** compact recurrent-state allocation reclaimed **~76 GiB of HBM**, growing the
  attention block pool **71%** and 1k8k throughput **18%**; BF16 recurrent state with FP32 arithmetic in
  VMEM added **15%**.
- **A layout change with a real trade-off:** sequence-on-lane doubles usable KV pages **5,141 → 10,283**
  and relaxes head dimension from a multiple of 128 to a multiple of 32, costing ~3% per-token latency at
  low concurrency but delivering **+16.5% throughput and −95% median TTFT at concurrency 128.**
- **A tuning parameter worth 49%:** splitting RPA v3 block size into fetch-16k and compute-4k took decode
  from **64.9k to 96.3k tok/s**, on an inverted-U curve. The tuned-parameter table could only store one
  block size, so it shipped as an environment override.

### The hardware

**Ironwood breaks the MegaCore convention**: two separate compute dies, each an independent logical
device, joined by a die-to-die link. Each chip has **2 TensorCores and 4 third-generation SparseCores**,
roughly **6× Trillium's HBM capacity**, and is the **first TPU with native FP8** — but has no native FP4,
which arrives with TPUv8i.

**The MXU grew and model architectures did not follow.** The matrix unit was **128×128 (16,384 MACs per
cycle) through v5** and is **256×256 (65,536 MACs per cycle) from v6e**. The consequence is direct:
**Llama 3 8B's head dimension of 128 caps attention matmuls at 50% MXU utilisation, and a head dimension
of 64 caps them at 25%.** gpt-oss ships with 64; DeepSeek MLA splits 128+64=192.

**This makes bring-up cost uncorrelated with model popularity.** Architectural hyperparameters now need to
be chosen with TPU tile geometry in mind, and a widely-used model with awkward dimensions is expensive to
support while an obscure one with friendly dimensions is cheap.

**The interconnect is being redesigned.** ICI went from a 2D torus (v2/v3) to a 3D torus from v4/v5p —
4×4×4 = 64 chips per rack, twisted torus, Optical Circuit Switches rewiring around failures in seconds and
scaling to the **9,216-chip Ironwood superpod at 42.5 FP8 exaflops**. **TPUv8i "Boardfly" replaces the
torus with a high-radix dragonfly-style fabric**, cutting network diameter **more than 50%** (~16 hops to
~7 at 1,024–1,152 chips), doubling ICI bandwidth to **19.2 Tb/s**, and tripling on-chip SRAM to **384 MB**
— sized specifically to hold reasoning and agentic KV cache on-chip.

**Google has split its training and inference architectures for the first time** (8t versus 8i). The
target workload is named: multi-turn, long context, high prefix reuse, and sub-agent bursts.

**The roadmap is mostly catching up to GPU serving practice**: speculative decoding and MTP, prefill-decode
disaggregation via **TPU-Sync** (formerly TPU-raiden, zero-copy through native PJRTBuffer descriptors), KV
cache offloading to DRAM, Mooncake Store P2P pooling, and AgentX.

## Why it matters

This is the vault's first hard data on a non-NVIDIA accelerator at inference, and the useful lesson is
methodological. The same hardware is **50% better, 8% better, or 30% worse** depending on whether you
normalise by chip-hour, by interactivity, by end-to-end response time, or against a disaggregated
competitor. Any single number pulled from this article is misleading. That belongs on
[[Serving Benchmarks and Goodput]] as a worked example of why the normalisation axis has to travel with
the result.

The **tile-geometry** finding is the most consequential item and the least obvious. Head dimension is
usually chosen for modelling reasons; on a 256×256 MXU it becomes a hardware-utilisation decision, with
head dim 64 leaving three quarters of the unit idle. This is hardware constraining model architecture
rather than the reverse, and it is why a second accelerator vendor is not simply a procurement choice —
the topic [[Accelerator Software Externalization]] now covers.

The optimisation catalogue is also the clearest available answer to "why doesn't everyone just use TPUs."
The gap between a chip that is competitive on paper and one that serves a specific model well is dozens of
kernel-level changes, and that gap has to be re-crossed per model family.

Finally, **TPUv8i's 384 MB of SRAM sized to hold agentic KV cache** is the first instance in the vault of
agent workloads driving a hardware design decision rather than a serving-software one.

## Tensions / open questions

- The 50–96% figure and the −30% figure come from the same article. Which is "true" depends entirely on
  the comparison chosen, and SemiAnalysis is careful about this in a way that downstream citation will
  not be.
- TTFT is materially worse on TPU (5.41s vs 2.40s on B300), which matters for exactly the interactive
  agentic workloads TPUv8i is being designed for.
- Results are from an **Official Preview** on one model (Qwen3.5 397B, FP8). Google was presumably
  involved in tuning; NVIDIA configurations may not have received equivalent attention.
- The GDN v3 numbers (1.41×/1.60×/2.14×) are kernel-level only. No end-to-end figure is given for them.
- The RPA v3 block-size win of 49% shipped as an environment variable because the tuning table could not
  represent it — a reminder that these gains are not automatically available to other users.
- TorchTPU is in private beta and unreleased at time of writing, so its portability claims are unverified.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Accelerator Software Externalization]]
- [[AI Accelerator Architecture]]
- [[Inference Serving Engines]]
- [[Prefill-Decode Disaggregation]]
- [[Serving Benchmarks and Goodput]]
- [[Linear Attention and Recurrent Memory]]
- [[KV Cache]]
- [[SemiAnalysis]]

## Related pages

- [[GPU Kernel Optimization]]
- [[Speculative Decoding]]
- [[ML Systems at Scale]]
- [[Distributed Training Parallelism]]
- [[Mixture of Experts]]
- [[Inference Efficiency Frontier]]
- [[NVIDIA]]
- [[Megakernels]]

## Citations

- Raw capture: [[2026-09-07 SemiAnalysis - TPU Inference Externalization Full Steam Ahead]]
- Source: <https://inferencex.semianalysis.com/blog/tpu-inferencex-full-steam>
