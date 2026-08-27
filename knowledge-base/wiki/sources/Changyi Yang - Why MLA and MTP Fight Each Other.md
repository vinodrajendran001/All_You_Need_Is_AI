---
type: source-summary
created: 2026-08-25
updated: 2026-08-26
source_id: src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
source_title: 'Why MLA and MTP Fight Each Other: Attention Through Arithmetic Intensity'
source_author: Changyi Yang
source_url: https://www.linkedin.com/pulse/why-mla-mtp-fight-each-other-attention-through-arithmetic-yang-npr9c/
tags: [source/summary, attention, arithmetic-intensity, mla, speculative-decoding, inference]
source_ids: [src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity]
status: active
---

# Changyi Yang - Why MLA and MTP Fight Each Other

## Summary

A first-principles derivation that reframes the entire MHA → GQA → MQA → MLA lineage as a single story about **arithmetic intensity** — FLOPs per byte moved — rather than about KV-cache size. Starting from a remark by Su Jianlin that "MLA+MTP tends to lose out," the author counts FLOPs and HBM bytes for the attention core during single-token decode and finds that all four attention variants collapse into one formula with a sliding KV-head count. The conclusion is that MLA and multi-token prediction are competing for the *same* scarce resource: the compute headroom that a memory-bound decode leaves idle.

## Key claims

- **One formula, four structures.** For BF16 single-token decode, the arithmetic intensity of the attention core is `1 → H_q/H_kv → H_q → ~2H_q` for MHA, GQA, MQA, and MLA respectively. Context length and head dimension cancel out entirely; only head counts survive.
- **Removing KV heads does not reduce FLOPs**, it reduces the history read from HBM, because one KV is reused by more query heads. That is the first layer of data reuse.
- **MQA's arithmetic intensity ceiling is the query head count, and that number does not grow.** Typical models have 32, 64, or 128 query heads (Falcon-7B's 71 is already high), and head count is fixed by the architecture — so piling on query heads alone cannot reach the few-hundred FLOP/byte balance point of modern GPUs.
- **MLA's contribution is making one latent serve as both K and V**, which is where the extra factor of just under 2 comes from — not from the latent dimension, which also cancels.
- **The whole lineage is a decode story.** In prefill, `AI ≈ (H_q/H_kv)·(L/b)`, i.e. decode AI multiplied by input length, so even plain MHA is compute-bound past roughly six hundred tokens. GQA and MQA do not change prefill FLOPs at all. These structures exist because decode has exactly one query token and therefore no reuse.
- **One MLA, two algorithms.** The same product can be bracketed two ways — expand the latent into K/V and run a dense GEMM (the "MHA algorithm"), or score directly against the wide latent (the "MLA algorithm"). Decode favours the MLA algorithm outright; prefill favours the other; the crossover sits around **S ≈ 171** query tokens, and sglang's dispatch logic follows exactly this split.
- **Sparse attention reverses the direction.** With DeepSeek-V3.2-style DSA selecting `index_topk = 2048` cached tokens, the MLA algorithm gathers latents by index and its cost goes from L to k, while the MHA algorithm must still expand the whole history for a dense GEMM. sglang's DSA backend threshold defaults to exactly 2048 — below it top-k selects everything so the dense kernel is preferable; above it sparsity finally pays.
- **The central result.** MTP raises the query count from 1 to S, and because HBM traffic barely grows while QK/PV compute scales nearly linearly, `AI(S) ≈ S · AI(S=1)`. DeepSeek-style MLA already reaches ~256 FLOP/B at S=1 and Kimi K3's MLA layer ~192 FLOP/B, against roofline balance points of ~206 FLOP/B on H200 and the two-to-three-hundred range on H100/B200. At S=2 these become 512 and 384 — past the knee. **MTP's extra arithmetic stops using idle compute and starts costing real latency.**
- Speculation windows are typically 2–8 and at most a few dozen, nowhere near 171, so MTP **stays on the MLA-algorithm side** of the crossover.
- **Appendix — RoPE.** The clean `AI = 2H` result ignores RoPE, which breaks the associativity that absorption relies on because query and key are rotated by different angles. DeepSeek's answer is a division of labour: a RoPE-free absorbed latent plus a small shared RoPE-carrying key segment of width `d_s` that participates in scoring but not the weighted sum, giving `F = 2HL(2d_c + d_s)` and `B = bL(d_c + d_s)`.

## Why it matters

This is the vault's clearest demonstration that attention-variant design is **data-reuse engineering**, and it supplies the analytical half of [[Arithmetic Intensity and the Roofline Model]] that [[Jacob Peake - AI Chip Architectures]] supplies from the hardware side. It also reframes two pages that previously treated their subjects independently: [[KV Cache]] has catalogued MLA as an architecture-level sharing technique, and [[Speculative Decoding]] has treated speculation as a low-batch latency play. This source shows they are coupled — an architecture that already saturates the roofline removes the headroom speculation depends on.

## Tensions / open questions

- **Byline caveat.** The capture carries no author field. "Changyi Yang" is inferred from the LinkedIn article slug (`…-arithmetic-yang-npr9c`) and the canonical version hosted at `changyi.fun`; it is not independently confirmed, and the personal site was unreachable from this network at ingest time.
- The derivation counts only the attention core's single pass over the cached KV, assuming a fused kernel and ignoring softmax, projections, and output projection as lower-order terms — real kernels will not hit the clean constants.
- The author flags that **arithmetic intensity itself misleads** near the crossover (section 5.7): a higher AI does not automatically mean a faster kernel.
- The independently arrived-at Zyphra Compressed Convolutional Attention paper (arXiv:2510.04476) agrees on `AI = 2n_heads`, the 295 FLOP/B H100 ridge, and the claim that DeepSeek chose head count against the roofline — and adds a mechanism this post does not cover: **MLA also loses under tensor parallelism**, because the shared KV must be replicated per TP rank, giving back the reuse MQA bought.
- The same paper's caution applies to the whole analysis: "model quality and latency, not SM utilization, is the end goal." Higher compute utilisation is not the objective function.
- Whether the MLA/MTP conflict is a hard architectural limit or merely a current-generation hardware coincidence is unresolved — the balance points quoted are H100/H200/B200 specific, and a bandwidth-heavier future part would move the knee.

## Affected pages

- [[AI Accelerator Architecture]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[GPU Execution Model]]
- [[Hugging Face]]
- [[Inference Serving Engines]]
- [[Jacob Peake]]
- [[KV Cache]]
- [[LLM Inference]]
- [[NVIDIA]]
- [[Speculative Decoding]]
- [[Transformer Architecture]]

## Citations

- Raw capture: [[2026-08-14 Changyi Yang - Why MLA and MTP Fight Each Other]]
- Canonical URL: https://www.linkedin.com/pulse/why-mla-mtp-fight-each-other-attention-through-arithmetic-yang-npr9c/
- Originally published at https://changyi.fun/posts/attention-arithmetic-intensity/
- Prompted by Su Jianlin, https://kexue.fm/archives/11848
- Converging independent result: Zyphra, *Compressed Convolutional Attention*, arXiv:2510.04476
- Implementation evidence: sglang `dsa_backend.py` dispatch thresholds

## Raw capture

- [[2026-08-14 Changyi Yang - Why MLA and MTP Fight Each Other]]

## Related pages

- [[GPU Execution Model]]
- [[Inference Serving Engines]]
- [[Model Quantization and Efficiency]]
- [[AI Accelerator Architecture]]
- [[Jacob Peake - AI Chip Architectures]]
