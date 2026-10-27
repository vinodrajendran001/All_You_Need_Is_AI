---
type: entity
created: 2026-08-25
updated: 2026-10-27
entity_kind: organization
tags:
  - entity
  - organization
  - hardware
  - accelerators
  - wafer-scale
source_ids:
  - src-2026-08-25-jacob-peake-ai-chip-architectures
  - src-2026-10-26-cerebras-trillion-parameter
status: active
---

# Cerebras

## What it is

The wafer-scale AI accelerator company. Its Wafer-Scale Engine abandons the reticle limit that constrains every conventional chip: 84 reticle-field dies are printed on one 300 mm wafer and stitched together with extra metal laid across the scribe lines, so software sees a single uniform fabric of ~900,000 cores with 44 GB of on-wafer SRAM and no HBM at all.

## Why it matters here

Cerebras is the vault's clearest example of an architecture that **changes the question rather than answering it faster**. Where the GPU is a hierarchy — threads in warps in SMs, dies in packages in racks, each boundary with its own bandwidth and programming construct — the WSE is a flat plane with no shared cache, no global memory, and no boundary. Execution is dataflow: a core idles until a *wavelet* arrives, control bits select the handler, and eight hardware microthreads switch cycle by cycle. As [[Jacob Peake - AI Chip Architectures]] puts it, **the arrival of data is the schedule**.

For [[Arithmetic Intensity and the Roofline Model]] it is the extreme data point. At roughly 1.3 bytes per dense FLOP — against ~0.002 for GPU rows — it sits so far on the bandwidth-rich side that the memory-bound decode problem largely disappears, which is why it produces the fastest independently measured decode in the industry (Artificial Analysis: 1,850 tok/s on Llama 3.1 8B, 2,522 on Llama 4 Maverick).

The cost is written into the same row of the table. Forty-four GB per wafer means a frontier-scale model consumes fleets; KV cache competes with weights for that same SRAM, so long context steals capacity and the API caps at 131K tokens while frontier providers serve 256K–1M; MoE is the format's worst case; and per-token pricing runs 3–5× GPU providers. The market has priced this as a **latency product**, and OpenAI's 750 MW CS-3 commitment through 2028 — reported above $10B at signing — is the largest endorsement wafer-scale has received.

## Notes

- Software is the binding constraint. The Cerebras compiler is a **kernel matcher**, not a general code generator: static graphs only, no dynamic shapes, no data-dependent control flow, no eager tensor access mid-step. SURF, the Dutch national compute centre, reports no 1:1 porting path from standard PyTorch.
- Cerebras has never published batch sizes or per-system throughput, so the throughput-per-dollar comparison rests on third-party analysis (SemiAnalysis).
- The 2024 pivot from training to inference — parking weights in SRAM rather than streaming them — is what now defines the company.
- [[Sarah Chieng - How Cerebras Deploys Trillion-Parameter AI Models]] is Cerebras's own worked example of parking weights in SRAM at frontier scale. Its illustrative Kimi K3 mapping (about 3 trillion parameters, 4-bit weights) spreads the model over 59 WSE-3T wafers of 44 GB each in a pipeline that passes only activations, and the SRAM left after each dense layer's weights caps concurrent requests: the vendor's own version of the capacity trade-off above. It proposes judging systems by token throughput per unit of power (e.g., tokens per second per megawatt) at a matched output generation speed. It is vendor material: its 1000-2000+ tokens per second headline names no model or setup, unlike the Artificial Analysis figures above, and it states no micro-batch size or measured per-system throughput, so the previous note still holds. Its assumed 256k average request exceeds the 131K API cap recorded from [[Jacob Peake - AI Chip Architectures]]; the cap may have changed since, but the undated post does not say.

## Related pages

- [[Jacob Peake - AI Chip Architectures]]
- [[Sarah Chieng - How Cerebras Deploys Trillion-Parameter AI Models]]
- [[AI Accelerator Architecture]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Inference Serving Engines]]
- [[LLM Inference]]
- [[Groq]]
- [[KV Cache]]
- [[AI Knowledge Base Overview]]
