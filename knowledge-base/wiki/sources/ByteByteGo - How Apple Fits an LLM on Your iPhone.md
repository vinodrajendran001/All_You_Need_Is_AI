---
type: source-summary
created: 2026-10-30
updated: 2026-10-30
source_id: src-2026-10-27-bytebytego-apple-on-device
source_title: How Apple Fits an LLM on Your iPhone
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-apple-fits-an-llm-on-your-iphone
tags:
  - source/summary
  - edge-ai
  - efficiency
  - privacy
source_ids:
  - src-2026-10-27-bytebytego-apple-on-device
status: active
---

# How Apple Fits an LLM on Your iPhone

## Summary

ByteByteGo explains Apple's on-device model as a coordinated memory-budget design: compress
weights, share attention state across layers, reuse a frozen base through task adapters, and
route harder requests to Private Cloud Compute (PCC). It is a secondary account, not a device
benchmark. Its most useful contribution is separating the objects competing for phone memory
rather than treating a small parameter count as sufficient.

## Key claims

- **Weight storage is only one budget.** A roughly 3B model at 16 bits needs almost 6 GB for
  weights alone. The earlier mixed 2-/4-bit palettization averages **3.7 bits per weight**,
  about **1.39 GB**. Cache, activations, operating-system use, and other apps remain additional.
- **The quantization recipes describe different generations.** The later account uses
  **2-bit decoder weights and 4-bit embeddings**, with quantization-aware training. It should
  not be folded into the earlier 3.7-bit average as one configuration.
- **Cross-layer sharing attacks another memory object.** A **5:3** depth split lets the later
  block reuse keys and values from the final layer of the first block. The reported saving is
  **37.5% of KV-cache memory**, not 37.5% of total application memory.
- **Specialization need not duplicate the base.** Rank-16 LoRA adapters stored at 16 bits occupy
  tens of megabytes and select task-specific behavior around shared frozen weights.
- **Local-first is not local-only.** Bounded tasks stay on-device; more demanding requests may
  use PCC. The described privacy mechanism combines verification of an authorized server image
  with encrypted request delivery, rather than asking users to trust the provider's name alone.

## Why it matters

The source joins [[On-Device Reasoning]], [[Model Quantization and Efficiency]], [[KV Cache]],
and [[Parameter-Efficient Fine-Tuning]] into a deployment stack. [[Small Language Models]]
therefore need a full runtime budget and a routing policy, not merely compressed weights.
The PCC discussion also supplies a comparison for [[Confidential Computing]]: moving a request
off-device changes the trust boundary even if the remote service uses attestation.

## Tensions / open questions

- The opening implies little battery or thermal impact, but the capture provides no measured
  power, temperature, latency, or sustained workload results.
- The conclusion reports **AFM 3 Core at 3B**, **Core Advanced at 20B total / 1-4B active** with
  prompt-level expert loading from flash, and PCC on NVIDIA GPUs in Google Cloud. These closing
  release/platform claims lack claim-specific supporting references in the capture; they are
  retained as unverified reporting, not established product specifications.
- Memory arithmetic is not proof of quality preservation or usable performance on every phone.
  Task mix, context length, runtime overhead, and supported hardware still matter.
- The linked Apple material is supporting material named by the explainer, not a separately
  captured and verified primary-source chain in this ingest. The sponsored opening is excluded.

## Affected pages

- [[On-Device Reasoning]]
- [[Small Language Models]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Confidential Computing]]
- [[Apple]]
- [[ByteByteGo]]

## Raw capture

- [[knowledge-base/raw/sources/How Apple Fits an LLM on Your iPhone]]

## Citations

- Canonical URL: <https://blog.bytebytego.com/p/how-apple-fits-an-llm-on-your-iphone>
- Published October 27, 2026; captured October 28, 2026. Tracking parameters are omitted from
  the summary URL; the raw capture is unchanged.

## Related pages

- [[Apple]]
- [[ByteByteGo]]
- [[On-Device Reasoning]]
- [[Small Language Models]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Confidential Computing]]
- [[Model Routing]]
