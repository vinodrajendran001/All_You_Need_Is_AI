---
type: concept
created: 2026-06-02
updated: 2026-10-27
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
  - src-2026-09-07-semianalysis-tpu-inferencex
  - src-2026-09-28-inferact-tpu-megakernels-kimi-k3
  - src-2026-10-02-epoch-agent-population
  - src-2026-10-14-vllm-nixl-push-connector
  - src-2026-10-15-netflix-reliable-gpu-compute
  - src-2026-10-21-simpson-torchtpu
  - src-2026-10-26-cerebras-trillion-parameter
  - src-2026-04-19-karray-neuromorphic-guide
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

## The MXU grew to 256x256 and model architectures did not follow

[[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]] documents the first third-party benchmarks of **TPUv7 Ironwood**, and the most
consequential finding is a geometry constraint rather than a performance number.

**The matrix unit was 128x128 (16,384 MACs per cycle) through v5 and is 256x256 (65,536 MACs per cycle)
from v6e.** Model head dimensions did not scale with it. The consequence is arithmetic: **Llama 3 8B's
head dimension of 128 caps attention matmuls at 50% MXU utilisation, and a head dimension of 64 caps them
at 25%.** gpt-oss ships with 64; DeepSeek MLA splits 128+64=192. SemiAnalysis's summary of this is
**"TPUs Are Picky."**

This inverts the usual direction of influence. Head dimension is normally chosen for modelling reasons; on
a 256x256 MXU it becomes a hardware-utilisation decision, and **bring-up cost becomes uncorrelated with
model popularity** — a widely-used model with awkward dimensions is expensive to support while an obscure
one with friendly dimensions is cheap.

**Ironwood also breaks the MegaCore convention**: two separate compute dies, each an independent logical
device, joined by a die-to-die link, with **2 TensorCores and 4 third-generation SparseCores** per chip,
roughly **6x Trillium's HBM capacity**, and **native FP8** (the first TPU with it). There is no native FP4;
that arrives with TPUv8i.

**The interconnect is being redesigned away from the torus.** ICI went 2D torus (v2/v3) → 3D torus from
v4/v5p — 4x4x4 = 64 chips per rack, twisted, with Optical Circuit Switches rewiring around failures in
seconds, scaling to the **9,216-chip Ironwood superpod at 42.5 FP8 exaflops**. **TPUv8i "Boardfly"
replaces it with a high-radix dragonfly-style fabric**, cutting network diameter **more than 50%** (~16
hops to ~7 at 1,024-1,152 chips), doubling ICI bandwidth to **19.2 Tb/s**, and tripling on-chip SRAM to
**384 MB** — sized specifically to hold reasoning and agentic KV cache on-chip. (Unit caveat added
2026-10-23: [[Ebba Simpson - Introducing TorchTPU]] states the same 19.2 figure for TPU 8t/8i ICI as
**19.2 TBps** — bytes, not bits, an eightfold difference. Both are first-party statements from
different vendors' write-ups; the vault records both and resolves neither.)

**Google has split its training and inference architectures for the first time** (8t versus 8i), with the
target workload named explicitly: multi-turn, long context, high prefix reuse, and sub-agent bursts. This
is the vault's first instance of agent workloads driving a hardware design decision rather than a
serving-software one.

Commercially, **Anthropic has committed to over one million TPUs** — about 400k purchased directly and
600k rented via GCP — surpassing DeepMind's own usage by 2029.

## Behind on peak FLOPS and on HBM bandwidth, and still ahead at batch-one decode

[[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]] is a useful stress test of the spec
tables this page keeps, because it reports a win by the chip that loses on both headline numbers.
Inferact's own comparison: **TPU v7 at 2.31 PFLOPS BF16 / 4.61 PFLOPS FP8, 206 GB of HBM at
7,380 GB/s, 1,200 GB/s ICI**, against **GB200, per GPU, at 2.5 PFLOPS BF16 / 5 PFLOPS FP8, 186 GB of
HBM at 8,000 GB/s, 1,800 GB/s NVLink 5** — Inferact's table is per-GPU, and its baseline is 16 GB200
GPUs, not 16 superchips. The TPU trails on arithmetic throughput, on memory bandwidth and on
interconnect, and leads only on HBM capacity.

The claimed explanation sits one level above HBM, on the memory surface this page's cache-versus-
scratchpad section is about. Inferact reports **64 MiB of VMEM per TensorCore and 128 MiB per chip,
addressed as two pools**, against **GB200's ~111 MiB of SRAM split 152 ways** — 256 KB of Tensor
Memory and 228 KB of shared memory per SM across 152 SMs, roughly 38 MiB of Tensor Memory per GPU.
Nearly equal totals, radically different granularity. A single persistent program that wants to hold
a decoder's working set and prefetch the next layer's weights while computing the current one can use
the first shape and not the second, which is the [[Megakernels]] argument in hardware terms.

The reported result, with its conditions: on **Kimi K3, 92 MoE layers across 16 TPU v7 chips in a
2x2x4 topology (TP4 x EP8 for routed experts, attention across 32 ranks)**, decode **without
speculation** runs at **249 vs 127 tokens/s at batch 1 (1.96x)** and **865 vs 636 at batch 8
(1.36x)**. The advantage is therefore a small-batch, memory-bandwidth-bound phenomenon that erodes as
vector arithmetic and inter-device traffic take over — narrow enough that it does not generalise to
the throughput regime the rest of this page compares.

Two tensions with existing material on this page should stay open rather than be resolved. First, the
[[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]] section above shows the same
silicon family yielding results from +96% to −30% depending on the normalisation axis, and describes
TPU serving software as largely catching up to GPU practice; Inferact's figure is one more point on
that spread, not a verdict. Second, the comparison is asymmetric in a way the hardware numbers hide:
a **hand-written TPU megakernel against a published vLLM GB200 recipe**, vendor-reported, with no
independent reproduction and no energy or cost-per-token accounting. It is evidence about what a
memory system permits a specialist to build, and only indirectly about the chips.

## HBM supply can anchor a capacity scenario, not count running agents

[[Jason Li - How Many AI Agents Could We Run]] normalizes HBM shipments into GB300 equivalents
using **288 GB per GPU**, not per superchip. It assumes **1-4x effective capacity uplift per GB**
for HBM4/4E relative to HBM3E, with 2x central. The resulting central effective supply is
**24.03 million GB300 equivalents through 2026** and **60.36 million through 2027**.
These are nested horizons for eventual deployment of hardware associated with 2025 onward
shipments, not two additive supplies or an observed installed fleet.

Mapping that hardware to agent sessions still requires a model, service target, allocation,
utilization, and economic assumptions; see [[Serving Benchmarks and Goodput]]. Memory supply is a
useful bottleneck proxy, not a complete performance model or evidence that every session performs
human-equivalent work.

## Inside the node, placement is topology too

This page's interconnect discussion has mostly lived at the rack and pod. Two October 2026 sources
show the same compute-versus-communication law inside one server. On the test nodes in
[[Sunita Nadampalli and Nicolò Lucchesi - Push-Based KV Transfer in vLLM]] (`p5en.48xlarge`, 8x H200),
16 EFA interfaces at 200 Gb/s each provide 3.2 Tb/s; eight sit on each NUMA node, and each GPU shares a
PCIe switch with two of them. NIXL's default LIBFABRIC backend registers each GPU's KV cache only on
those two rails, so every transfer stays PCIe-local without manual device overrides.
[[Netflix - Reliable GPU Compute for Training and Inference]] states the cost of getting this wrong: a
GPU paired with a network adapter or CPU on the wrong PCIe root incurs a bandwidth penalty. Netflix
plans topology-aware allocation (Compute/IMEX domains, PCIe roots, NUMA nodes) through Kubernetes
Dynamic Resource Allocation once Karpenter supports it.

Netflix also treats the device as divisible. MIG partitions give memory-level isolation between small
inference tenants and are reconfigured without restarting the machine, which changes the unit of
capacity. Device-level allocation could also change the unit of failure, since one faulty GPU need not
remove the whole machine, but the source makes that conditional on future DRA support. Neither source
quantifies these placement effects. See [[GPU Fleet Reliability]].

## A TPU TensorCore is effectively single-threaded, and the shapes are an input to compilation

[[Ebba Simpson - Introducing TorchTPU]] is a framework announcement, but its most durable content for
this page is its list of ways TPU execution declines to behave like a GPU. All of it is first-party
Google/Meta/PyTorch description, with no independent verification in the post.

- **TensorCores are described as effectively single-threaded execution processors.** TPU Streams exist,
  but the post says GPU-equivalent parallel execution cannot always be achieved on them. SparseCores
  take sparse and collective work; DMA engines carry asynchronous host/device transfers. Concurrency
  here is a property of the compiled program rather than of a warp scheduler, which is the
  cache-versus-scratchpad tradeoff above restated at the level of the execution unit.
- **One user-space process per device is enforced.** The post names the consequence: reinforcement-
  learning colocation, which puts generation and training on the same device, does not work out of the
  box. See [[Distributed Training Parallelism]].
- **Shapes are a compile-time input.** XLA and PjRT traditionally require compile-time-known shapes.
  *Bounded dynamism* allocates buffers to a compile-time maximum bound while tracking the runtime
  logical dimension, padding and slicing rather than recompiling — described as active development,
  with `torch.compile` currently forcing `dynamic=False`.
- **The ISA is not addressable.** "The actual TPU ISA is proprietary," so the lowest level available
  outside Google is Mosaic or Pallas. There is no TPU equivalent of inspecting the emitted machine code.

Three hardware figures extend or corroborate what this page holds, all first-party and all presented by
the post as generation-specific examples rather than universal TPU properties. The **256x256
multiply-accumulator MXU** matches the geometry the SemiAnalysis section above records from v6e onward,
so the two independent write-ups agree on the number that makes TPUs "picky" about head dimension.
**TPU 8i is given as 288 GB of HBM at 8.6 TB/s** and **TPU 8t DCN as 400 GBps**, adding a memory and
scale-out surface the vault did not have for that generation.

Precision above the MXU's native format is bought in passes through it: `high` uses a **3-pass**
algorithm at roughly **3x** MXU compute and `highest` a **6-pass** algorithm at roughly **6x**, both
relative to the default `medium` mode. No benchmark or workload accompanies those multipliers; they are
the post's description of the algorithms, not a measured slowdown.

The padding cost of lane geometry gets a worked number for the first time here: in the post's KV-cache
example **each core occupied 1,024 bytes per token to hold 512 bytes of data**, the remainder being
padding, and a *sequence-on-lane* layout is said to halve both KV memory and KV bytes read. The model,
hardware generation, and baseline for that example are not stated. It is the 256x256 head-dimension
finding one level down: tile and lane geometry decide what fraction of an allocated byte is useful.

## Wafer-scale capacity is bought in wafers, and the links between them carry only activations

[[Sarah Chieng - How Cerebras Deploys Trillion-Parameter AI Models]] shows how Cerebras fits a model
whose weights need terabytes onto WSE-3T wafers, each with the 44 GB of SRAM recorded from
[[Jacob Peake - AI Chip Architectures]] above. Its Kimi K3 example (about 3 trillion parameters, 4-bit
weights) divides the payload evenly over 93 layers, about 16 GB each. Each of the 24 dense
(full-attention) layers gets a wafer, with the remaining SRAM kept for that layer's KV cache, and the 69
linear-attention layers pack two per wafer: 35 + 24 = 59 wafers. Whole layers typically fit on one
wafer, so "in most cases, the model weights never have to move", and "Only activations cross from one
wafer to the next" over RDMA over Ethernet, at what the post gives as "roughly 2 microseconds per hop".
The compute-versus-communication principle is taken to its limit: weights stay put, and the price is
paid in wafers.

The post also tests the pipeline-parallelism bullet from [[Dwarkesh Patel - Reiner Pope Flashcards]]
above: bubbles, architecture constraints, and less KV relief than expected. Cerebras fills the pipeline
with a different request in each stage, so "the number of requests in flight is roughly the number of
stages times the micro-batch size". Each of those requests needs its own cache on every dense-layer
wafer, so the cache caps how full the pipeline can be, and at a fixed micro-batch a deeper pipeline
needs more cache on each dense wafer. The post does not state that depth effect; its two statements imply
it. The architecture constraint shows up too: attention type decides how layers pack.

[[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]] runs the same model on 16 TPU v7 chips,
prefetching weights from HBM. Chips and wafers are different units, and neither source reports a power
or cost figure, so the two placements cannot be ranked. Inferact counts 92 MoE layers; this post counts
93 by attention type and never mentions experts.

This is a vendor explainer. Its arithmetic is illustrative, its formulas are images in the capture, and
it reports no measured throughput or cost, so the throughput-per-dollar gap recorded above is
untouched. The headline promise "to run multi-trillion parameter models at 1000-2000+ tokens per second"
names no model, configuration, or measurement, and the post is undated.

## Neuromorphic chips attack the memory wall by skipping work, but their efficiency figures are uncited

[[Yasmine Karray - Neuromorphic Computing - A Complete Guide]] adds a branch this page has not covered:
event-driven, spiking hardware. Its diagnosis is this page's compute-versus-communication principle: in
a classical processor "the limiting factor is generally not the speed of computation — it is the time
spent transferring data between memory and the processor". Its answers to the four questions from
[[Jacob Peake - AI Chip Architectures]] above are distinctive. Weights are "stored locally" beside the
compute in each neuromorphic node. Data moves as spike events over an asynchronous network with no
global clock. Nodes act only when a spike arrives: "If there is no spike, there is no computation."
Chip-to-chip scaling is not discussed. Two of those answers overlap with [[Cerebras]], which keeps
weights in on-wafer SRAM and leaves each core idle until data arrives; what the guide adds is sparsity,
with binary spikes and most neurons silent at any moment.

Two existing claims meet it. The [[Dwarkesh Patel - Reiner Pope Flashcards]] bullet above says batching
amortizes weight fetches, and the guide says "A neuromorphic chip does not need batching", which fits a
design whose weights do not move, though the guide does not argue it that way. Its 300 to 700 watts for
a data-center GPU stops at Hopper in the power bullet above, where [[Jacob Peake - AI Chip Architectures]]
puts Blackwell at 1,000 W and B300 at 1,400 W. Peake and the guide also disagree on deployment: Peake
counts neuromorphic designs among architectures in development, not among those that have won
deployment, while the guide describes a 2026 division of labor, with GPUs training and converted models
running on neuromorphic edge chips, and names no deployed conversion.

The numbers are the weak point. The over-99% energy saving, the 100× to 1000× efficiency factors, the
ANYmal robot's AI computation using "up to 100× less energy" with Loihi 2 than a GPU-based solution
such as an Nvidia Jetson, and a 90% cut in overall processor consumption in certain walking-control
tests come without workload, configuration, or citation. By the guide's own figure of 1–5% active
neurons, proportional savings top out near a hundredfold, short of the upper end it says sparsity
"largely explains". No comparison holds accuracy or latency fixed.

## Open questions

- Which future model architectures will favor larger TPU-like units versus more GPU-like flexible tiles?
- How much of future accelerator progress will come from arithmetic innovation versus memory and interconnect innovation?
- When do software-managed locality strategies become too hard to use effectively, even if they are theoretically more efficient?
- As bytes-per-FLOP ratios diverge by three orders of magnitude across deployed architectures, does a single comparison frame remain meaningful, or does each architecture now need its own?
- Should comparison tables carry on-chip memory *per independent scheduling unit* alongside totals? 128 MiB in two pools and ~111 MiB split 152 ways are nearly the same number and support completely different programs.
- TPUv8i triples on-chip SRAM to 384 MB, sized for agentic KV cache. Does that capacity widen the single-program megakernel advantage, or does the cache claim it first?
- Is TPU 8t/8i ICI bandwidth **19.2 Tb/s** or **19.2 TBps**? Two first-party write-ups in this vault state the same number in units that differ by a factor of eight, and neither shows its derivation.
- The TorchTPU post supplies no GPU-side measurements of its own, no energy figures, and no cost-per-token accounting, so none of its MFU or tokens-per-second results can be read as a cross-vendor hardware comparison. What would a matched-workload comparison even hold fixed, given the shape constraints above?
- If TensorCores are effectively single-threaded and shapes must be bounded at compile time, which workloads — data-dependent routing, variable-length agent traffic, reinforcement-learning rollouts — are *structurally* expensive on this hardware rather than merely untuned?
- Does the 1,024-bytes-for-512 padding ratio in the TorchTPU KV example generalize beyond that unnamed configuration, or is it an artifact of one head dimension meeting one lane width?
- Kimi K3 now has two placements here, 16 TPU v7 chips ([[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]) and 59 WSE-3T wafers ([[Sarah Chieng - How Cerebras Deploys Trillion-Parameter AI Models]]), and two layer counts, 92 MoE layers versus 69 linear-attention plus 24 dense. Neither source gives power or cost; would tokens per second per megawatt at a matched per-user speed, the Cerebras post's proposal, be enough to rank them?
- Would any of the efficiency factors in [[Yasmine Karray - Neuromorphic Computing - A Complete Guide]] survive a matched comparison at equal task accuracy and latency, with idle leakage, memory retention, and sensor power inside the energy boundary? The vault has no primary measurement of neuromorphic hardware.

## Related pages

- [[Ebba Simpson - Introducing TorchTPU]]
- [[PyTorch]]
- [[Sunita Nadampalli and Nicolò Lucchesi - Push-Based KV Transfer in vLLM]]
- [[Netflix - Reliable GPU Compute for Training and Inference]]
- [[GPU Fleet Reliability]]
- [[Jason Li - How Many AI Agents Could We Run]]
- [[Epoch AI]]
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
- [[Wafer - AI Performance Engineering Resources]]
- [[Wafer]]
- [[GPU Kernel Optimization]]
- [[SemiAnalysis - TPU Inference Externalization Full Steam Ahead]]
- [[Accelerator Software Externalization]]
- [[SemiAnalysis]]
- [[Inferact - 700 TPS on Kimi K3 - A Case for TPU Megakernels]]
- [[Megakernels]]
- [[Sarah Chieng - How Cerebras Deploys Trillion-Parameter AI Models]]
- [[Yasmine Karray - Neuromorphic Computing - A Complete Guide]]
