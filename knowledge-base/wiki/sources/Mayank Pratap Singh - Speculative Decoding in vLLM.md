---
type: source-summary
created: 2026-07-06
updated: 2026-10-16
source_id: src-2026-07-06-mayank-pratap-singh-speculative-decoding
source_title: "Speculative Decoding: Theory and Implementation in vLLM"
source_author: Mayank Pratap Singh
source_url: https://vizuara.substack.com/p/speculative-decoding-theory-and-implementation
tags:
  - source/summary
  - inference
  - speculative-decoding
  - serving
  - vllm
source_ids:
  - src-2026-07-06-mayank-pratap-singh-speculative-decoding
status: active
---

# Mayank Pratap Singh - Speculative Decoding in vLLM

## Summary

This Vizuara post builds speculative decoding from first principles and then deploys it, ending with an EAGLE3-on-vLLM run where speculation was **slower** than baseline. It motivates the technique through low-batch, bandwidth-bound decode, explains distribution-preserving rejection sampling, works through the economics (α, τ, K), catalogues draft-source families, and reports an actual GPU experiment separately from its illustrative timing diagrams.

Its motivating example is a dense 70B model at 16-bit precision: roughly **140 GB of weights**. At low batch, repeated weight reads can leave arithmetic headroom for verifying several positions together. Batching amortizes those reads and sharding changes the per-device boundary; this is not universal per-token traffic. The durable lesson is that speculation is a **bet** on committed tokens per unit of total serving work, not a guaranteed speedup.

## Key claims

- **Bandwidth-bound decode provides an opportunity, not a phase-wide rule.** The low-batch dense example can verify multiple positions for a cost close to one target step. Actual verification cost depends on batch, context, kernels, and hardware; see [[LLM Inference]].
- **Draft, then verify.** A small `M_q` proposes K tokens and target `M_p` scores them in parallel. Under **greedy matching**, keep the matching prefix and the target's correction at the first mismatch. Stochastic rejection sampling instead needs the acceptance and residual rules below. A round can advance by one token while costing more than plain decoding; progress is not a latency guarantee.
- **Exactness is distributional.** Rejection sampling (Leviathan 2023, arXiv:2211.17192; Chen 2023, arXiv:2302.01318) accepts with `min(1, p(x)/q(x))` and resamples a rejection from normalized `(p-q)+`. Correct implementation preserves the target distribution, not seed-identical sampled wording or factual correctness.
- **Three economics knobs.** **α** describes acceptance; **τ** in `τ = (1−α^{K+1})/(1−α)` counts expected **committed tokens including the correction/bonus**, under constant conditional acceptance. For the figure's **K=5**, α=0.30 gives ~1.43 and α=0.85 ~4.15 tokens per round; the α=1 limit is K+1. The article proposes adapting **K** to predictability, but entropy alone does not determine draft agreement or serving cost.
- **System limitations are implementation-specific.** The described serial draft/verify loop has waiting time; the direct tokenwise algorithm needs a common token space; and auxiliary weights, cache, and workspace compete for memory. A rejection ends the committed prefix. The article recommends load-aware switching, not a measured universal batch-size cutoff.
- **Draft families:** separate draft-target models; **n-gram prompt lookup** without a draft model; **Medusa** heads with tree verification; and original **EAGLE** feature prediction. That EAGLE explanation is not the training objective of every successor; the deployment experiment uses EAGLE3.
- **The system-tax diagrams are illustrative.** The 2.5× token-math versus ~1.8× effective speedup and the verification/draft time shares (52%→74% and 24%→10%) are explicitly labeled illustrative. The batch-128 −5% to +10% range is part of that pedagogical discussion, not the actual run below. These figures explain possible overheads and stragglers; they are not measured production results.
- **The reported benchmark:** Llama-3.1-8B on a single **48 GB Ada GPU**, baseline versus EAGLE3, was **slower in both tested regimes**: greedy batch 1 and a non-greedy load test with 500 prompts at infinite request rate, approximately 500 concurrent. The article reports acceptance length **τ=1.81**. Small-target cost, acceptance, and saturation are its explanations, not separately ablated causes; proposed tuning is not a measured successful rerun.

## Why it matters

This early foundation for [[Speculative Decoding]] pairs a mechanism tutorial with a useful negative serving result. It connects [[LLM Inference]], [[KV Cache]], and [[Arithmetic Intensity and the Roofline Model]]: accepted history, drafter memory, and verification cost must be accounted for together. Unlike [[Model Quantization and Efficiency|directly serving a compressed model]], exact speculation preserves the target distribution; unlike [[Test-Time Scaling]], its aim is efficiency rather than a different answer-generation policy. The later [[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]] extends the account with newer architectures and workload-dependent exceptions.

## Tensions / open questions

- The headline "2–3× faster" is not reproduced by the author's own run. The opening "exact same text" wording is also stronger than the distributional proof under sampling.
- The October 16 lint corrects this summary's earlier promotion of illustrative timings to measurements and its conflation of one-token progress with never being slower. The raw source retains both its simplified framing and its negative benchmark.
- The raw calls τ "accepted tokens" even though its geometric formula includes the correction/bonus. Preserve the reported 1.81 diagnostic without assuming all papers or runtime metrics use the same convention.
- The article's low-load-only framing is qualified even by its later acknowledgment of gains in other high-concurrency studies. Samarin adds cache-bound large-batch cases and acceptance-aware scheduling; neither account establishes a universal on/off rule.
- Direct tokenwise comparison requires compatible tokenization, not necessarily common model ancestry. Cross-tokenizer machinery is outside this tutorial's scope.

## Affected pages

- [[Arithmetic Intensity and the Roofline Model]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Mayank Pratap Singh]]
- [[Speculative Decoding]]

## Citations
- Source URL: [vizuara.substack.com](https://vizuara.substack.com/p/speculative-decoding-theory-and-implementation)
- Code: [LLM-Inference-Playbook](https://github.com/Mayankpratapsingh022/LLM-Inference-Playbook)
- Foundational: Leviathan et al. 2023 (arXiv:2211.17192); Chen et al. 2023 (arXiv:2302.01318).

## Raw capture

- [[2026-07-06 Mayank Pratap Singh - Speculative Decoding Theory and Implementation in vLLM|Speculative Decoding Theory and Implementation in vLLM]]

## Related pages

- [[Aleksandr Samarin - Speculative Decoding - The Art of Guessing Well]]
- [[Speculative Decoding]]
- [[LLM Inference]]
- [[KV Cache]]
- [[Model Quantization and Efficiency]]
- [[GPU Execution Model]]
- [[Test-Time Scaling]]
- [[Mayank Pratap Singh]]
- [[Vizuara]]
- [[AI Knowledge Base Overview]]
