---
type: concept
created: 2026-06-02
updated: 2026-08-26
tags:
  - concept
  - hardware
  - accelerators
  - gpu
  - tpu
source_ids:
  - src-2026-06-02-dwarkesh-reiner-pope-chip-design
  - src-2026-06-02-dwarkesh-reiner-pope-flashcards
  - src-2026-06-03-liquid-ai-lfm2-5-8b-a1b
  - src-2026-07-01-anastasiia-alekseeva-parallel-training
  - src-2026-07-02-alyona-vert-ai-concepts-2026
  - src-2026-07-03-fergus-finn-cuda-kernel
  - src-2026-06-30-onur-sirin-local-llm-memory-hardware
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-08-23-wafer-ai-performance-engineering-resources
status: active
---

# AI Accelerator Architecture

## Definition

AI accelerator architecture is the design of hardware systems specialized for neural-network workloads, spanning arithmetic units, memory hierarchy, data movement, precision formats, local compute tiles, and cluster-scale layout across devices and racks.

## Why it matters

Model capability is inseparable from hardware structure. Accelerator design determines which operations are cheap, which are bottlenecked by bandwidth, and how easily training and inference scale from one chip to an entire cluster.

## Current synthesis

- The most durable principle across both Reiner Pope sources is **compute versus communication**. The arithmetic you care about is often cheaper than the movement needed to feed it.
- At the chip level, the natural primitive for AI hardware is the **multiply-accumulate** because matrix multiplication is just repeated MACs. Lower precision helps twice: it reduces storage and also shrinks arithmetic circuitry roughly faster than linearly with bit width.
- The chip-design lecture makes the hidden cost concrete: muxes and register-file access can dominate the area around a logic unit, which is why accelerator designers keep trying to increase compute done per trip through the memory boundary.
- **Systolic arrays** are the canonical answer to that problem. They bake more of the matrix-multiply loop into fixed hardware, keep weights local, and stream activations through the array to reduce repeated data movement.
- **FPGA vs ASIC** is a classic tradeoff:
  - FPGA: reprogrammable, deterministic, fast to redeploy, but much less area- and energy-efficient.
  - ASIC: far more efficient, but expensive and slow to change because tape-out is costly.
- **Cache vs scratchpad** expresses a software/hardware control tradeoff. CPU-style caches optimize average performance but introduce nondeterminism; scratchpads and TPU-like memory systems expose locality management more explicitly.
- **GPU vs TPU** is partly a granularity decision:
  - GPU: many smaller repeated units with more local flexibility and higher internal movement bandwidth.
  - TPU: fewer coarser matrix units that amortize overhead better for very regular dense linear algebra.
- The flashcards show the same architecture story at cluster scale:
  - Batch size amortizes weight fetches until compute or KV-cache fetch dominates.
  - MoE layers fit naturally within a rack because expert routing is all-to-all and NVLink is the right topology for that boundary.
  - Pipeline parallelism can relieve weight placement pressure but introduces bubbles, model-architecture constraints, and weaker-than-expected relief for KV-heavy long-context workloads.
- The Liquid AI LFM2.5 source adds a deployment-facing MoE view: sparse models separate **total parameters** from **active parameters**, which can make explicit reasoning affordable on laptops and phones. But this only works if runtimes and kernels efficiently handle routing, memory layout, and sparse execution across frameworks such as `llama.cpp`, MLX, vLLM, and SGLang.
- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]] shows the same compute-vs-communication law at cluster scale from the software side: every distributed-training strategy is a different partition of the same GEMM, chosen to minimise coordination. See [[Distributed Training Parallelism]] — tensor parallelism reduces inter-device traffic to a few all-reduces per layer, MoE all-to-all wants a single NVLink rack (as the flashcards already note), and pipeline point-to-point tolerates slower inter-node links.
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]] complements this hardware-design page with the **software execution model** on top of the hardware — see [[GPU Execution Model]]. It makes the memory-vs-compute story concrete at the level of one kernel: a low-arithmetic-intensity vector add runs at ~80% of DRAM bandwidth but only ~5% issue activity, i.e. the chip is starved by data movement, not arithmetic — the micro-scale version of this page's central claim.
- [[Alyona Vert - AI Concepts and Techniques in 2026]] adds the **inference-hardware** frontier: as deployment shifts from training to serving billions of tokens, inference is fragmenting by workload. Three 2026 visions illustrate the spread — NVIDIA's rack-scale Vera Rubin, MatX's programmable LLM-first accelerator, and Taalas's radical "model-as-hardware" approach that bakes a specific model into silicon. This pushes accelerator design toward cost-per-token, latency, and power rather than raw training FLOPS.
- [[Onur Sirin - How Local LLMs Run]] adds a local-machine taxonomy that is useful beyond consumer buying advice. It distinguishes **GDDR/VRAM** (tiny but very fast, e.g. RTX 5090), **unified LPDDR-style memory** (flat pool, one speed, e.g. Mac Studio), and **coherent tiered memory** (HBM fast tier plus LPDDR slow tier, e.g. GB300). This reinforces the page's central point: hardware performance is not just arithmetic throughput; it is the shape, capacity, and bandwidth of the memory surface feeding the accelerator.
- [[Jacob Peake - AI Chip Architectures]] is now the page's most complete comparative source, covering all six architectures that have won real deployment on shared axes. Three additions matter most here:
  - **A reusable reading frame.** Understanding any chip reduces to four questions — where data *lives*, how it *moves* to the compute units, what the *compute units* look like, and how chips *talk to each other at scale*. Each architecture is a different strategy for the same data-movement game against the memory wall, and each is reducible to an explicit list of **bets**.
  - **The divergence has moved up a level.** Per-chip FP8 has converged — B200 (4.5 PF), TPU Ironwood (4.6 PF), and MI355X (10 PF) sit within roughly 2× of each other — so the architectures now differ at the rack and pod, not the die. The TPU's flat-rate-per-chip × massive-pod recipe (9,216-chip Ironwood pods at 42.5 ExaFLOPS FP8) yields more aggregate compute per system than any NVIDIA rack, at the cost of per-chip bandwidth, and its ICI message-passing torus is the deliberate inverse of NVLink's hardware-coherent address space.
  - **Two architectures that break the table's axes.** [[Cerebras]] has no HBM at all — 44 GB of on-wafer SRAM at ~21 PB/s, about **1.3 bytes per dense FLOP** where GPU rows sit near 0.002 — and executes as pure dataflow across a flat 900,000-core mesh where "the arrival of data is the schedule." [[Groq]] deletes every reactive component so the compiler owns each cycle, and extends that to a fabric that is *scheduled, not routed*, with forward error correction instead of retransmission because a retry would perturb the schedule. Both win per-user decode latency and lose an order of magnitude on throughput per dollar once you batch.
- Two structural constraints from the same source are worth recording because they bound everything above. **Power per chip is rising fast** — 700 W (Hopper) → 1,000 W (Blackwell) → 1,400 W (B300, MI355X) → ~1,800 W (analyst-estimated Rubin Ultra) — and liquid cooling becomes mandatory above ~1,000 W, so air cooling effectively ends with Hopper. And **software remains the asymmetry the spec tables cannot show**: the Cerebras compiler is a kernel matcher requiring static graphs with no dynamic shapes or data-dependent control flow, which is a different kind of cost from any number in the comparison.
- [[Changyi Yang - Why MLA and MTP Fight Each Other]] supplies the analytic complement to the hardware survey and is developed in [[Arithmetic Intensity and the Roofline Model]]. The connecting claim: the *shape* of the matmul, not the chip, decides the regime. Training and prefill stack many tokens against the same weights and are compute-bound GEMMs; decode emits one token at a time so every matmul degenerates to a GEMV, and arithmetic intensity drops by orders of magnitude. Batching, speculative decoding, and multi-token prediction all exist to promote those GEMVs back to GEMMs — but under continuous batching each user still reads their own KV cache, so long-context decode shifts from weight-bandwidth-bound to **KV-bandwidth-bound**. That is the hardware reason [[KV Cache]] optimisation is an accelerator concern and not just a memory-capacity one.

## The non-NVIDIA stacks have primary documentation too

[[Wafer - AI Performance Engineering Resources]] documents the alternatives at the same level as the incumbent, which is unusual and useful. **AMD CDNA 4** covers the MI350-series architecture with matching ROCm and Composable Kernel material; **Google TPU** is documented from the TPU v4 paper through the Ironwood generation, with JAX and XLA as the programming surface; **AWS Trainium** appears via Trainium3 and the Neuron SDK.

The list is candid that its coverage is NVIDIA-weighted, and equally candid about why: public architectural documentation is unevenly available, and depth of documentation is not a proxy for deployment share. The practical reading is that the *concepts* on this page — memory hierarchy, tensor units, interconnect topology, precision support — port across vendors, while tooling maturity does not. See [[Wafer]] for the curation's own disclosure of this bias, and [[Distributed Training Parallelism]] for the open interconnect standards that would make portability real.

## Open questions

- Which future model architectures will favor larger TPU-like units versus more GPU-like flexible tiles?
- How much of future accelerator progress will come from arithmetic innovation versus memory and interconnect innovation?
- When do software-managed locality strategies become too hard to use effectively, even if they are theoretically more efficient?
- As bytes-per-FLOP ratios diverge by three orders of magnitude across deployed architectures, does a single comparison frame remain meaningful, or does each architecture now need its own?

## Related pages

- [[Dwarkesh Patel - Reiner Pope - Chip design from the bottom up]]
- [[Dwarkesh Patel - Reiner Pope Flashcards]]
- [[Liquid AI - LFM2.5-8B-A1B]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Cerebras]]
- [[Groq]]
- [[NVIDIA]]
- [[Jacob Peake]]
- [[Mixture of Experts]]
- [[Model Quantization and Efficiency]]
- [[ML Systems at Scale]]
- [[LLM Training Pipeline]]
- [[Distributed Training Parallelism]]
- [[GPU Execution Model]]
- [[Anastasiia Alekseeva - The Simple Maths Behind Parallel Training]]
- [[Fergus Finn - What Happens When You Run a CUDA Kernel]]
- [[Alyona Vert - AI Concepts and Techniques in 2026]]
- [[Onur Sirin - How Local LLMs Run]]
- [[Reiner Pope]]
- Wafer - AI Performance Engineering Resources
- Wafer
- GPU Kernel Optimization
