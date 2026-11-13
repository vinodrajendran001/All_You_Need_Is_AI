---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-05-huggingface-moe-training-handbook
source_title: The Ultimate MoE Training Handbook
source_author: Nouamane Tazi, Leandro von Werra, and Thomas Wolf
source_url: https://huggingface.co/spaces/huggingface/moe-blogpost
tags:
  - source/summary
  - mixture-of-experts
  - llm-training
  - distributed-training
  - inference
source_ids:
  - src-2026-11-05-huggingface-moe-training-handbook
status: active
---

# The Ultimate MoE Training Handbook

## Summary

Hugging Face's handbook is a long, hands-on guide to training mixture-of-experts (MoE) models with
Megatron-LM. It runs from cluster validation through a dense baseline and a first MoE, then through
the router, load balancing, expert shape, block layout, training choices, systems, precision, serving
and reinforcement learning (RL). Each topic sets the authors' own small Megatron experiments beside
the published choices of current open MoEs, and ends in a "Recommendation" and a "Watch" callout. The
durable lesson is that an MoE adds three problems a dense model does not have: a router that must
learn, a load that must stay balanced, and an all-to-all token exchange that can dominate the step.
Matching a dense model's active parameters does not match its step time. The authors are unusually
explicit about the evidence: many recommendations rest on one ablation in one lab's setup.

## Key claims

### The frontier is sparse, and matched active parameters are not matched cost

- On the Artificial Analysis index, **18 of the 20** highest-scoring open-weights models are MoEs;
  the two dense exceptions are Nanbeige4.3-33B and Qwen3.8 27B.
- The first MoE replaces a ~1.22B dense model's feed-forward layers with **64 experts, top-8**, each
  one-eighth of the dense width, so the eight active experts equal one dense FFN. The result has
  **6.86B total and 1.221B active** parameters against the dense model's **1.219B**, yet matching
  active parameters does not give equal step time.

### Validate the cluster and make runs comparable before tuning

- DCGM level 2 found thermal violations and failed PCIe and memory tests on **three GPUs in one
  node**. nccl-tests all-to-all at 8 GiB per rank gave **77.14 GB/s** bus bandwidth on a two-node
  baseline but **39.84 GB/s** on another two-node allocation with NCCL tuning variables. Default and
  tuned ran on different node pairs, so the tuning's effect cannot be isolated. The policy adopted is
  to accept **90%** of a same-size baseline (~69 GB/s) rather than one fixed threshold.
- When NCCL fell back to TCP sockets, an EP16 proxy ran about **25 times slower** (**1.7 vs 42.0
  TFLOP/s**). Checking that the log says the intended transport is cheap insurance.
- With deterministic mode, two runs were identical. Without it, losses differed from iteration 1 by
  up to **0.00063**. Deterministic mode comes before comparing runs or chasing a NaN.

### The router: precision is the choice that changes winners

- Of four router choices (gating function, output scale, sharpness, precision), precision is the
  one that changes which experts win, because bf16 ties flip the top-k. Always use
  `--moe-router-dtype fp32`, with a **1e-3** z-loss for softmax routers whose logits drift. Only
  **2 of 10** model reports mention training router precision.
- The routed scaling factor "has no settled value", and shipped models disagree. Token choice is
  the recommended routing scheme.

### Load balance is a throughput problem first

- With routing forced even, the same model ran **1.5x** faster at initialization (**149.4 TFLOP/s**
  best case), which sets the target every balancer is judged against.
- In a five-way comparison (one seed, median of the last 20 of 120 iterations), quantile balancing
  reached **139** TFLOP/s, an auxiliary loss **125** and a bias-only scheme **99**. But quantile
  ended with the *highest* training loss of the five, so its throughput lead "does not establish"
  faster training to the same quality. The recommendation is an auxiliary loss near **1e-3**.

### Expert shape and layout

- Finer experts help up to a point. Liew et al. saw loss fall **2.334 → 2.297** up to 128 experts of
  d/4 at top-8 (fixed total and active), and finer splits gave no further gain. Stop when small GEMMs
  and token copies dominate.
- LatentMoE projects tokens to a smaller dimension before dispatch. NVIDIA's 73B-A8B ablation scored
  **4.6 points** higher on MMLU-Pro than a standard MoE at equal total and active parameters.
  Serving throughput ranged from **12% lower** at concurrency 1 to slightly higher at some
  concurrencies.
- Leading dense layers mean fewer all-to-alls, but they should not be relied on to fix imbalance.
  LongCat's shortcut-connected block cut exposed dispatch and combine from **25.3%** to **8.4%**.
- A "rogue" expert in Step 3.5 Flash grew from about **14** to about **5,700 times** the layer's
  median output norm while training loss barely moved. The max-to-median norm ratio is the canary.

### Training choices

- **Upcycling** from a dense checkpoint pays when the MoE run is short. OLMoE trained from scratch
  caught up after about **500B tokens** (25% of 2T), and Komatsuzaki et al. after about **120%** of
  the dense model's compute.
- For **Muon**, use `--muon-extra-scale-factor 0.2`; the default 1.0 diverged on a dense 7B in Mellum2
  tests.
- **Multi-token prediction (MTP)** is not free: one MTP layer made early steps about **37%** longer
  on the authors' 256-node runs, against **7%** reported for Mellum2. In Ling 2.0 an MTP layer costs
  about **1.7x** an MoE layer's compute, and repartitioning the pipeline around it gained **40%** end
  to end.

### Systems: the all-to-all is the bill

- In one traced single-node step, **half** the time was exposed all-to-all while the router was
  still unbalanced.
- EP16 across two nodes ran **59%** below EP8 in one node. The two runs also differ in nodes and
  micro-batch accumulation, so the comparison is confounded. The rule is to keep EP inside a node
  and add nodes as data-parallel replicas.
- Overlapping one micro-batch's all-to-all with another's compute gave up to **35%** more
  throughput on two nodes, for **5–10 GB** more reserved memory on rank 0. Full recomputation cost
  **24%** of throughput. In NVIDIA's measurement, activation offloading cut peak reserved memory by
  **18%** for a **2%** throughput loss.
- **Dropless is the default.** In Vavre et al., capacity factor 1 without tensor parallelism ran at
  **463** TFLOP/s/GPU against **392** for dropless with TP2, and MMLU stayed within a point. Pangu's
  capacity factor 1.5 dropped about **6%** of tokens at 20B and **8%** at 718B, and in the 20B
  comparison the dropless run kept a lower loss throughout. UltraEP, which re-plans replicas per
  micro-batch and layer, cut the busiest rank from **1.30–2.86x** the mean to **1.01–1.03x**.

### Precision

- FP8 gives about **10–25%** end-to-end throughput on a large MoE, per the Megatron Core team.
  DeepSeek's 16B and 230B FP8 runs stayed within **0.25%** relative error of BF16. Ling-1T was within
  about **0.1%**, with MFU up about **15%**. The router, norms and attention core stay in higher
  precision.
- Nemotron 3 Super (**120B total, 12B active**) trained in NVFP4 on **25T** tokens, with the last 15%
  of the network, attention projections, embeddings and MTP kept in BF16.

### Serving

- **Fewer experts at serving time saves compute, not memory, and the renormalization denominator
  decides the cost.** For Qwen3.6-35B-A3B at top-4, dividing by the top-16 routing mass cost
  **0.35** MMLU points (not significant, p = 0.66). Renormalizing over the surviving experts cost
  **4.65**. With no renormalization, top-6 cost **27.45**.
- **Low-bit experts shrink storage more than they shrink reads.** For gpt-oss-20b, 4-bit experts take
  the model from **39.0 to 12.8 GiB** (3x smaller). Bytes read per decoded token only fall from
  **6.72 to 3.45 GiB** (about half): a batch-1 token reads only 4 of 32 experts per layer but all
  of attention and the unembedding, which stay in bf16. The
  recommendation is 4-bit routed experts in post-training.
- **DeepSeek sizes expert parallelism in opposite directions by phase.** Relayed from DeepSeek's
  DeepInfer documentation, DeepSeek-V4.1-Flash runs prefill at **EP2–EP8** and decode at
  **EP64–EP128**. At 64 requests per GPU, EP64 decodes about **15,700** tokens/s per GPU (~246 per
  user) against EP8's **12,600** (198), both about **25%** higher. At 256 requests per GPU the two
  nearly meet (**26,300 vs 24,900**). The price is a **64 + 64 GPU** minimum deployment, and one
  failed GPU takes the instance down. Load imbalance (`moe_lb`) is held at **1.090** in decode with
  redundant hot-expert copies.
- **Attention-FFN disaggregation (AFD)** is unsettled. MegaScale-Infer reports up to **1.90x**
  per-GPU throughput, and FastAFD **1.41x** over colocated EP4. Qiu et al.'s analytical model puts
  FastAFD at **0.99x** on the same 72-GPU budget, with homogeneous AFD helping only in a minority of
  modelled settings.

### RL: rollout and trainer route differently

- On Qwen3-30B-A3B, about 10% of routers chose different experts between SGLang rollouts and
  Megatron, and **94%** of tokens differed in at least one layer. Routing replay (R3) cut
  train-inference KL from **1.5e-3 to 7.5e-4**, near dense Qwen3-8B's **6.4e-4**. Whether replay pays
  off in reward is "still contested".
- In Zhuge et al.'s runs at Qwen, NVFP4 rollouts against a BF16 trainer collapsed after about
  **150 steps**; the collapse was traced to quantized activations, not weights.

## Why it matters

The handbook is the vault's most complete practitioner account of [[Mixture of Experts]]. Its
mechanics run through [[Distributed Training Parallelism]] (expert parallelism kept in-node,
overlap, capacity) and the [[LLM Training Pipeline]] (upcycling, Muon, MTP, routing replay in RL).
It extends [[GPU Fleet Reliability]] with pre-flight validation and baseline-relative acceptance. On
the serving side it adds the phase-split EP sizing to [[Prefill-Decode Disaggregation]],
storage-versus-reads arithmetic to [[LLM Inference]], and the expert-only low-bit recipe to
[[Model Quantization and Efficiency]]. It is also a long-form [[Hugging Face]] Space.

## Tensions / open questions

- **Thin evidence, stated as such.** Many experiments use one seed, 120 iterations and one cluster.
  The authors' conclusion says many recommendations rest on one ablation in one lab's setup.
- **Throughput is not quality.** The router comparison ranks speed over the first 120 iterations,
  and the fastest scheme had the highest loss.
- **Confounded comparisons, acknowledged.** The NCCL-tuning and EP16-vs-EP8 comparisons changed
  node allocation along with the variable under study.
- **Relayed vendor numbers.** DeepSeek serving figures, NVIDIA's LatentMoE ablation, the AFD
  speedups and the FP8 gains come from the cited parties. The handbook relays them, and in places
  redraws them, but did not reproduce them. FastAFD's 1.41x and Qiu et al.'s 0.99x disagree under
  different assumptions.
- **Serving versus released code.** DeepSeek's documented phase-split deployment sits beside
  [[Mehul Gupta - What is DeepSeek DeepInfer]], which reports that DeepInfer's initial release lacks
  complete prefill-decode disaggregation. Running such a deployment and shipping it are not the
  same claim.
- **Capture artifacts.** The HTML conversion turned some numbers into section links. Examples are
  `[2.5](#s-2-5) at k = 8`, `Step [3.5](#s-3-5) Flash`, a load-balancing loss of `[3.2]`, and a
  permute-fusion step-time drop of `[3.3]%`. Values that are also section numbers are not cited
  here unless the prose confirms them.
- **Figures are interactive.** Values plotted in the 62 figures appear only where prose or captions
  state them.

## Affected pages

- [[Mixture of Experts]]
- [[Distributed Training Parallelism]]
- [[LLM Training Pipeline]]
- [[GPU Fleet Reliability]]
- [[LLM Inference]]
- [[Prefill-Decode Disaggregation]]
- [[Model Quantization and Efficiency]]
- [[Hugging Face]]
- [[Inference Serving Engines]]
- [[DeepSeek]]
- [[NVIDIA]]
- [[Speculative Decoding]]

## Raw capture

- [[knowledge-base/raw/sources/2026-11-05 Nouamane Tazi, Leandro von Werra, and Thomas Wolf - The Ultimate MoE Training Handbook]]
- [[knowledge-base/raw/sources/The Ultimate MoE Training Handbook - a Hugging Face Space by huggingface]].
  This is the original November 10 clipping. It holds only the Space's "Refreshing" placeholder and
  an embedded iframe, and lists no author. It is kept for provenance and is not cited as evidence
  here.

## Citations

- Canonical URL: https://huggingface.co/spaces/huggingface/moe-blogpost (fragment removed).
- Byline: Nouamane Tazi, Leandro von Werra, and Thomas Wolf. Publisher: Hugging Face. The page
  description is "A hands-on guide to training Mixture-of-Experts models with Megatron-LM"; a margin
  note gives the reading time as 1-2 days.
- Published: 2026-11-05.
- Recaptured: 2026-11-13, at the user's request, from the server-rendered HTML of the Space's iframe
  address (`https://huggingface-moe-blogpost.hf.space/`). The 62 interactive figures were reproduced
  as links to static posters with their captions; plotted values were not transcribed. The original
  clipping was captured 2026-11-10.
- Software pins stated in the source: Megatron-LM commit `d6316eb45` and the NGC PyTorch image
  `26.06-py3`.

## Related pages

- [[Mixture of Experts]]
- [[Distributed Training Parallelism]]
- [[LLM Training Pipeline]]
- [[GPU Fleet Reliability]]
- [[LLM Inference]]
- [[Prefill-Decode Disaggregation]]
- [[Model Quantization and Efficiency]]
- [[Hugging Face]]
- [[Inference Serving Engines]]
- [[Xuewen Yang - Parallelism for LLM Training, with Numbers You Can Check by Hand]]
- [[Mehul Gupta - What is DeepSeek DeepInfer]]
- [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]
- [[Wafer - AI Performance Engineering Resources]]
- [[Rohan Anil - The Hitchhiker's Guide to Training on Compute Islands]]
- [[Netflix - Reliable GPU Compute for Training and Inference]]
- [[Ali Zahid Raja - Your Model Doesn't Have to Fit in Your GPU Anymore]]
- [[ByteByteGo - How Nvidia's New Nemotron Model Works]]
- [[DeepSeek]]
- [[NVIDIA]]
- [[Speculative Decoding]]
