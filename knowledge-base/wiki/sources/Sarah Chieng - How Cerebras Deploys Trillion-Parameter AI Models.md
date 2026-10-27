---
type: source-summary
created: 2026-10-27
updated: 2026-10-27
source_id: src-2026-10-26-cerebras-trillion-parameter
source_title: How Cerebras Deploys Trillion-Parameter AI Models
source_author: Sarah Chieng
source_url: https://www.cerebras.ai/blog/how-we-deploy-trillion-parameter-frontier-models-on-cerebras
tags: [source/summary, ai-hardware, inference, kv-cache, serving]
source_ids:
  - src-2026-10-26-cerebras-trillion-parameter
status: active
---

# Sarah Chieng - How Cerebras Deploys Trillion-Parameter AI Models

## Summary

A Cerebras blog explainer by Sarah Chieng, with no publication date in the capture (clipped 26 October
2026). It answers a common question: how does a model whose weights "need terabytes" run on wafers that
each hold 44 GB of on-chip memory? Using the open-source Kimi K3, with about 3 trillion parameters, "as an
illustrative example", it walks through mapping layers to wafers, a pipeline that passes only activations
between wafers, and how the memory left for the key-value (KV) cache limits concurrency.

The headline speed, multi-trillion-parameter models "at 1000-2000+ tokens per second", is a vendor claim
with no stated model, configuration, or measurement. The durable contributions are the placement
arithmetic and a proposed efficiency metric: throughput per megawatt at a fixed generation speed.

## Key claims

**Keep each layer whole and on-chip.** A WSE-3T wafer has 44 GB of on-chip SRAM. With 4-bit weights,
Kimi K3's weight payload divided across its 93 layers comes to about 16 GB per layer, so "we are typically
able to fit entire layers of the model directly on the chip". As a result, "in most cases, the model
weights never have to move".

**Layer type sets the packing.** A dense (full-attention) layer stores keys and values for every token of
every active request, so each dense layer gets its own wafer, and the rest of that wafer's SRAM holds its
KV cache. A linear-attention layer keeps "a small, fixed-size state per request, regardless of context
length", so two fit on one wafer (2 × 16 GB = 32 GB). Kimi K3's 69 linear and 24 dense layers therefore
need 35 + 24 = 59 wafers. The illustration assumes a 256k average request, 4-bit weights, and an 8-bit KV
cache.

**A pipeline, not a batch.** The compiler maps layers onto regions of wafers, and the runtime routes
tokens between wafers over RDMA over Ethernet, "roughly 2 microseconds per hop". "Only activations cross
from one wafer to the next." Each wafer acts as one stage of an assembly line. The pipeline stays full
because each stage works on a different request at the same time; with micro-batches, the number of
requests in flight is "roughly the number of stages times the micro-batch size". Smaller micro-batches
make each request faster, while larger ones raise total throughput. The example uses one layer per stage;
in production, Cerebras uses "much finer-grained stages, and many more of them."

**KV-cache memory caps concurrency.** Every request in flight needs its own KV cache on every dense-layer
wafer, so the SRAM left after one dense layer sets the ceiling on concurrent requests. The formulas and
resulting numbers are image-only in the capture.

**Compare systems by tokens per second per megawatt.** "Of course, neither concurrency nor batch size
tells you exactly how efficiently an inference system performs." The proposed metric is total token
throughput per unit of power, "when measured at the same output generation speed."

## Why it matters

[[AI Accelerator Architecture]] gets a worked example of the wafer-scale, SRAM-resident design. Capacity
grows by adding wafers, and the price is many chips joined by links that carry only activations.

[[KV Cache]] gets a consequence of hybrid attention: only dense layers carry a per-token cache, so the mix
of linear and dense layers sets both the wafer count and the concurrency ceiling.

[[Serving Benchmarks and Goodput]] gets a vendor proposal to normalize throughput by power at a matched
per-user speed, a goodput-style condition.

## Tensions / open questions

- **No measurements.** The 1000-2000+ tokens per second claim is not tied to Kimi K3 or any measured
  configuration. No throughput, latency, power, or concurrency figures appear in the text.
- **Simplified arithmetic.** Dividing the total payload evenly across 93 layers treats every layer as the
  same size, which the post does not justify.
- **The benchmark scores are the model maker's.** Kimi K3's 88.3% on Terminal-Bench 2.1 and 91.2% on
  BrowseComp, against GPT-5.6 Sol's 88.8% and 90.4%, link to Kimi's own blog.
- **Undated.** The capture has no publication date, so product details are point-in-time.
- **Capture artifact.** One paragraph appears twice in the capture.

## Affected pages

- [[AI Accelerator Architecture]]
- [[KV Cache]]
- [[Serving Benchmarks and Goodput]]
- [[Cerebras]]

## Raw capture

- [[How Cerebras Deploys Trillion-Parameter AI Models]]

## Citations

- Canonical URL: https://www.cerebras.ai/blog/how-we-deploy-trillion-parameter-frontier-models-on-cerebras
  (newsletter tracking parameter removed).
- No publication date; clipped 26 October 2026, which this vault uses for the source ID. Author from the
  clipping's frontmatter. Calculations are image-only.

## Related pages

- [[AI Accelerator Architecture]]
- [[KV Cache]]
- [[Serving Benchmarks and Goodput]]
- [[Linear Attention and Recurrent Memory]]
- [[Distributed Training Parallelism]]
- [[Inference Serving Engines]]
- [[Model Quantization and Efficiency]]
- [[Jacob Peake - AI Chip Architectures]]
- [[Cerebras]]
- [[AI Knowledge Base Overview]]
