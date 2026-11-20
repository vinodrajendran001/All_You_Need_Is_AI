---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-13-thinking-machines-end-to-end-4-bit-training
source_title: "End‑to‑End 4‑Bit Training"
source_author: "Jack Cook and Thinking Machines Lab"
source_url: "https://thinkingmachines.ai/blog/end-to-end-4-bit-training/"
tags:
  - source/summary
  - quantization
  - training
  - mixture-of-experts
  - distributed-training
  - kernels
source_ids:
  - src-2026-11-13-thinking-machines-end-to-end-4-bit-training
status: active
---

# End-to-End 4-Bit Training

## Summary

Thinking Machines Lab describes the numerics recipe it used to train **Inkling 2 Small** on NVIDIA
GB300 systems. The expert (MoE) layers run their forward passes in NVFP4, a 4-bit block-scaled
format. Backward passes run in MXFP8 after the forward tensors are re-quantized with stochastic
rounding. Expert-parallel communication is itself quantized, and a dedicated kernel stack (BBBK)
keeps the GPU's units busy. The same numerics run from the start of pretraining to the final RL
rollout, so no post-training calibration step is needed. The lab reports an **8%** wall-clock
speedup in pretraining and a **20%** speedup in RL "over full MXFP8 training" in its largest jobs,
at a cost of about **2%** compute efficiency in pretraining and "no discernible difference in reward"
in RL. All results are first-party. The post gives no model size, benchmark tables, or ablation data.

## Key claims

### The format tradeoff

- On GB300, NVFP4 stores **4.5** bits per value and runs at **15** PFLOPS. MXFP8 stores **8.25**
  bits at **5** PFLOPS, and BF16 stores **16** bits at **2.5** PFLOPS. In the post's words, NVFP4
  "is stored with 3.6x fewer bits than BF16, but it runs up to 6x faster on GB300s".
- NVFP4 groups FP4 values (±{0, 0.5, 1, 1.5, 2, 3, 4, 6}) in blocks of **16** with an FP8 (E4M3)
  scale, and MX formats use blocks of **32** with E8M0 scales. NVFP4 can represent magnitudes from
  2^-10 to **2688**. An extra FP32 scale over a whole tensor shifts that range.
- Different stages of training care about different errors. Forward passes and the RL sampler
  mostly need low *error*. Backward passes and the RL trainer need low *bias*, meaning values that
  consistently round one way. Random rounding errors average out over a batch. Bias compounds
  "across layers, samples, and training steps".

### Why only the experts

Earlier in the year the lab moved its MoE layers to full MXFP8 and found this "barely affected"
compute efficiency (CE). CE measures how a technique shifts training and evaluation loss. Full NVFP4
training instead caused "very large hits" to CE. The final recipe therefore applies NVFP4 only to
expert-layer forward passes.

### The transpose problem and stochastic rounding

The backward pass needs the transposed weight, which groups values into blocks along the other
axis, so the forward and backward copies get different scales and disagree. NVIDIA's suggested fix,
one scale per 16×16 tile, was "too coarse, hurting CE": one outlier can push a whole tile's small
values to zero. The lab instead de-quantizes, transposes in high precision, and re-quantizes with
**stochastic rounding (SR)**. SR rounds up or down at random, weighted by distance, so the backward
copy equals the forward copy *on average*. In the worked example, 4.5 at a new scale of 2 becomes
2.25. That rounds to 2 three quarters of the time and to 3 a quarter of the time, which preserves
4.5 in expectation. SR is "hardware-accelerated on Blackwell". Re-quantizing to MXFP8 and computing
gradients with MXFP8 GEMMs gave "the best tradeoff between accuracy and speed". The lab credits
TetraJet-v2 and Quartet II as inspiration.

### Communication became the bottleneck

With NVFP4 GEMMs, the MoE forward pass "should theoretically have gotten about three times faster"
than in MXFP8. Expert-parallel traffic then became the limit. NVLink moves **900** GB/s each way
while the GEMMs run at up to **15** PFLOPS, so a GPU can do about **16,000** FLOPs in the time one
byte arrives.

- *Dispatch*, which sends tokens to experts, goes in NVFP4.
- *Combine*, which returns expert outputs, normally stays in BF16. MXFP8 "impaired performance too
  much" because it represents outliers poorly. A 32-dimensional random Hadamard transform followed
  by block-scaled S2F6, an 8-bit fixed-point format, gave "no measurable accuracy degradation" and
  cut combine traffic from **16** to **8.25** bits per value. Blackwell has PTX conversion
  instructions for S2F6.

### The kernel and the recipe

- **BBBK** ("Big Beautiful Blackwell Kernel") is described as "fully deterministic". It uses the
  GB300-only 2SM UMMA instruction (K=96), a 6-stage multiplicand pipeline, and a 7-stage scale-factor
  pipeline. It fuses the Hadamard transform and S2F6 quantization into the w2 GEMM epilogue. The lab
  claims it saturates NVLink, the ALUs and the Tensor Cores together in training, and reaches the
  NVLink/HBM latency floor in RL sampling. Overlap uses expert waves "as in DeepSeek-V4".
- The last **16.6%** of layers stay in higher precision, computed in MXFP8 rather than BF16.
- Four Over Six (4/6) is used when quantizing activations but not weights.
- Following Composer 2, weights get per-expert outer scales and activations get per-token outer
  scales, which the lab says gives "batch-invariance" and avoids "causality leakage".
- Inkling 2 Small was pretrained in **68 hours** on GB300 NVL72 racks. A similar-size run "months
  ago" took "several weeks". The post says numerics are "just one piece" of that improvement.
- Next steps named: an FP4 backward pass, and how the recipe changes on Vera Rubin.

## Why it matters

The vault's quantization material mostly concerns compressing a finished model. This post treats
precision as part of the training recipe. It explains *where* 4-bit arithmetic is safe, using the
bias-versus-error split, and *what breaks next* when it is applied. Once the MoE forward GEMMs get
(theoretically) about three times faster, the bottleneck moves to the interconnect, so numerics,
communication and kernel design have to be co-designed. Because sampler and trainer share one
precision recipe, the post also bears on the train-inference mismatch problem in MoE reinforcement
learning.

## Tensions / open questions

- **Unverified scale and benefit.** "The largest model we are aware of" trained end to end with a
  native 4-bit forward pass is a self-assessment, and no parameter count is given. The 8%, 20% and
  2% figures cover the lab's "largest jobs" and come with no tables or ablations.
- **Speedup vs. theory.** The theoretical MoE forward gain is about 3×, but the measured end-to-end
  pretraining gain is 8%. The post does not break down where the difference goes.
- **Which layers stay higher-precision.** Nemotron 3 Super, as relayed in
  [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]], keeps its last **15%** in BF16. This
  lab keeps the last **16.6%** in MXFP8. Neither source ablates the choice.
- **RL with low-precision rollouts.** The same handbook relays a Qwen study where NVFP4 rollouts
  against a BF16 trainer collapsed after about **150** steps. This post reports no discernible reward
  difference. One possible explanation, which is our inference and not the post's claim, is that
  sampler and trainer share the same numerics here.
- **Hardware specificity.** The recipe depends on GB300 features (the K=96 UMMA, SR and S2F6
  instructions), and it is unclear how much carries over to other accelerators.

## Affected pages

- [[Low-Precision Training]]
- [[Model Quantization and Efficiency]]
- [[Distributed Training Parallelism]]
- [[LLM Training Pipeline]]
- [[Thinking Machines]]

## Raw capture

- [[knowledge-base/raw/sources/End‑to‑End 4‑Bit Training]]

## Citations

- Canonical URL: <https://thinkingmachines.ai/blog/end-to-end-4-bit-training/>. The captured link
  carried a `utm_source=tldrai` parameter, which is removed here.
- The capture's `published` field is empty, and its in-page citation says only "Cook, Jack and
  Thinking Machines Lab … Thinking Machines Lab: Connectionism, Nov 2026". A read-only fetch of the
  canonical page recovered the byline "Jack Cook in collaboration with others at Thinking Machines"
  and the date **Nov 13, 2026**, which is used for the source ID. No figures were taken from the
  fetch. Captured 2026-11-17.
- The raw filename uses non-breaking hyphens (U+2011). The summary stem uses ASCII hyphens.

## Related pages

- [[Low-Precision Training]]
- [[Model Quantization and Efficiency]]
- [[Distributed Training Parallelism]]
- [[LLM Training Pipeline]]
- [[Mixture of Experts]]
- [[Thinking Machines]]
- [[NVIDIA]]
- [[GPU Kernel Optimization]]
- [[Nouamane Tazi et al - The Ultimate MoE Training Handbook]]
- [[ByteByteGo - The New American AI Model Designed to Be Customized]]
