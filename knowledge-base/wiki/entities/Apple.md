---
type: entity
created: 2026-10-30
updated: 2026-10-30
entity_kind: organization
tags:
  - entity
  - edge-ai
  - privacy
source_ids:
  - src-2026-10-27-bytebytego-apple-on-device
status: active
---

# Apple

## What it is

Apple is represented here through a secondary account of its on-device foundation-model stack
and Private Cloud Compute (PCC), [[ByteByteGo - How Apple Fits an LLM on Your iPhone]].

## Why it matters here

The case links five deployment decisions that are often discussed separately: a small shared
base, low-bit weight storage, cross-layer KV sharing, task-specific LoRA adapters, and routing
to a remote service when local capability is insufficient.

The memory numbers refer to different objects. The earlier approximately 3B model's **3.7-bit
average** gives about **1.39 GB of weights**, not a whole-application footprint. A later recipe
uses **2-bit decoder weights / 4-bit embeddings**; the reported **37.5% saving** instead
concerns KV-cache memory. Adapter storage and operating-system requirements remain separate.

## Evidence boundary

This capture supplies mechanisms, not measured battery, thermal, or sustained-latency outcomes.
Its closing AFM 3 specifications and PCC placement on NVIDIA/Google Cloud lack claim-specific
supporting references and are not treated here as verified product facts. PCC also changes the
trust boundary rather than making cloud processing on-device: the account relies on verified
authorized software and encrypted delivery.

## Related pages

- [[ByteByteGo - How Apple Fits an LLM on Your iPhone]]
- [[ByteByteGo]]
- [[On-Device Reasoning]]
- [[Small Language Models]]
- [[Model Quantization and Efficiency]]
- [[KV Cache]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Confidential Computing]]
