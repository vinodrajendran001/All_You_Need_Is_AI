---
type: concept
created: 2026-11-13
updated: 2026-11-13
tags:
  - concept
  - attention
  - long-context
  - inference
source_ids:
  - src-2026-11-10-alphasignal-latent-sparse-attention
  - src-2026-08-14-changyi-yang-mla-mtp-arithmetic-intensity
  - src-2026-09-14-alphasignal-deepseek-v4-1-flash
  - src-2026-10-13-zancato-model-priming
status: active
---

# Sparse Attention

## Definition

Sparse attention lets each query attend to a **selected subset** of earlier keys instead of all of
them, and then runs ordinary attention over that subset. The subset can be fixed by
position, as with a sliding window of recent tokens plus a few initial tokens. Or it can be chosen
by content: a cheap indexer scores tokens or blocks and keeps the top-k, or a search over clustered
keys retrieves promising groups. This separates it from [[Linear Attention and Recurrent Memory]].
Those designs replace exact attention with a fixed-size state. Sparse attention keeps exact
attention but reads less.

## Why it matters

Full attention's cost grows with the square of context length.
[[Alpha Signal - How Latent Sparse Attention Tackles the Search Bottleneck in Long-Context AI]] puts
it as doubling context roughly quadrupling the computation, and notes that coding agents accumulate
millions of tokens of context. The cost shows most in prefill, though decode also slows as every new
token consults the whole context (see [[LLM Inference]]). Sparse attention is one way the vault's
sources keep token-addressable access to very long histories without paying for every key. It also
changes the hardware picture: [[Arithmetic Intensity and the Roofline Model]] shows that selecting k
keys instead of L changes which kernel path wins.

## Current synthesis

### Four selection styles in the vault

1. **Fixed windows.** A recent-token window, sometimes with a few retained initial tokens. LSA keeps
   both alongside its retrieved keys. [[KV Cache]] lists sliding windows among its optimization
   families, and [[Small Language Models]] treats them as a runtime saving that trades away
   long-range memory. [[Luca Zancato - Priming Hybrid Models from Pretrained Transformers]] uses
   sliding-window substitution as a probe: layers that tolerate it are candidates for conversion to
   fixed-state layers.
2. **Indexer top-k.** DeepSeek Sparse Attention (DSA) scores candidates with a smaller, cheaper
   indexer. In [[Changyi Yang - Why MLA and MTP Fight Each Other]], a DeepSeek-V3.2-style DSA keeps
   `index_topk = 2048` cached tokens.
3. **Block and hierarchical retrieval.** Methods that score blocks of neighboring keys instead of
   single keys. [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]] reports
   DeepSeek V4.1-Flash narrowing history to at most **2,048 blocks** and then selecting up to **512
   compressed positions**.
4. **Clustered search.** Latent Sparse Attention (LSA) groups keys into clusters in a learned
   latent space and compares queries with cluster centroids. Flat search checks every centroid;
   tree search follows a hierarchy of clusters.

### The selector can become the new quadratic cost

Sparse attention removes the dense score matrix but not the work of choosing. If the indexer still
looks at every earlier key or block, its prefill cost keeps growing quadratically. In the LSA
account, selection took **98%** of an attention layer's prefill time in a 10-million-token
experiment with GLM-5.3-Flash, which uses a variant of DSA. LSA's answer is to search centroids
rather than keys, although flat search still grows with the number of clusters. On one NVIDIA H200
at 10 million tokens, it reports a **22.7x** prefill and **4.6x** decode speedup for one GLM
attention layer against that sparse baseline. In end-to-end serving across eight H200 GPUs, the
reported gains fall to **2.2x** time to first token and **2.1x** time per output token. The gap
between layer and system numbers is the usual caution: attention is only part of a serving step.

DeepSeek V4.1-Flash's two-stage narrowing (blocks, then compressed positions) and LSA's tree
search both use hierarchy to bound selection cost. The vault has no source comparing them, and the
DeepSeek account reports no hardware, throughput or latency figures.

### Sparsity pays only past a threshold

[[Changyi Yang - Why MLA and MTP Fight Each Other]] shows that sparsity changes kernel choice. With
top-k selection, MLA's gather-by-index path drops from L to k, while the dense path still expands
the whole history. sglang's DSA backend therefore uses a threshold of exactly 2048, the same as
`index_topk`. Below it, top-k selects everything and the dense kernel is preferable. The LSA
account gives a matching caution: its gains "become much smaller in shorter context
tasks". The common reading, inferred here rather than stated by either source, is that sparse
attention is a long-context tool. Below some length, the bookkeeping costs more than it saves.

### Selection is not storage

Reading fewer keys does not by itself store fewer. This separates sparse attention from the
token-eviction family in [[KV Cache]], which deletes low-importance tokens and so risks losing one
that matters later. A sparse selector keeps every token and chooses again for each query. LSA still
retrieves "the original keys" from the chosen clusters, so the full [[KV Cache]] must remain
addressable; the capture gives no memory figures for the cache, the centroids or the index. DeepSeek
V4.1-Flash pairs its sparse retrieval with a separately compressed global cache stored in FP4. In
the vault's sources, cutting reads and cutting bytes stored are separate design choices.

### Fixed windows are a weak stand-in for long-range retrieval

Two independent sources point the same way. Zancato reports that state-space hybrids beat
sliding-window hybrids even when the window receives **two to four times** the state-memory budget.
In the LSA account, natively trained LSA retained more long-context accuracy than baselines such as
sliding-window attention, in a **500-million-parameter** hybrid trained at up to 128,000 tokens.
Both are tested configurations reported by the methods' own authors. Neither supports treating a
local window as an adequate substitute for long-range memory, whether that memory is a recurrent
state or retrieved keys.

### Quality depends on the model

LSA's reported quality effect differs by model. On RULER, Qwen-3.8-27B with distilled LSA scored
**63.9** at 10 million tokens against **59.9** for full attention, while GLM-5.3-Flash lost up to
eight points at 2–5 million tokens against its own sparse baseline. A selector can help or hurt
retrieval depending on the model it is attached to. Both results are the researchers' own, relayed
by a newsletter.

### Relation to hybrids

Sparse attention and linear/recurrent hybrids answer the same pressure from opposite ends: read
fewer exact keys, or replace some attention layers with constant-size state. The LSA work suggests
the two can be combined: native LSA was tested inside a hybrid model, though the capture does not
say what the other layers were. The LSA account describes Qwen-3.8-27B as using "full attention",
but the vault records Qwen3.8-27B as a 3:1 hybrid of Gated DeltaNet and Gated Attention blocks (see
[[Linear Attention and Recurrent Memory]]). The likely reading is that its attention layers are
dense rather than sparse. The capture does not say whether LSA replaced all of them.

## Open questions

- Does sparse selection keep its quality at 10 million tokens across model families? The one
  two-model comparison in the vault is split.
- How much memory do cluster centroids, indexers and block summaries add on top of the KV cache? No
  source here reports it.
- Where is the crossover length for clustered search on real serving stacks? sglang's 2048-token
  threshold is for DSA kernels, not LSA.
- Can a natively trained sparse model at frontier scale match full attention? The only native
  result is a 500M model.

## Related pages

- [[Alpha Signal - How Latent Sparse Attention Tackles the Search Bottleneck in Long-Context AI]]
- [[Changyi Yang - Why MLA and MTP Fight Each Other]]
- [[Alpha Signal - How DeepSeek Made a Bigger Model Cheaper to Run]]
- [[Luca Zancato - Priming Hybrid Models from Pretrained Transformers]]
- [[Linear Attention and Recurrent Memory]]
- [[KV Cache]]
- [[LLM Inference]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Transformer Architecture]]
- [[Small Language Models]]
- [[Inference Serving Engines]]
- [[Prefill-Decode Disaggregation]]
- [[DeepSeek]]
- [[Alpha Signal]]
