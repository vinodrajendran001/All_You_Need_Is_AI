---
type: entity
created: 2026-09-11
updated: 2026-09-11
entity_kind: organization
tags:
  - entity
  - inference
  - gpu
  - models
source_ids:
  - src-2026-09-08-cohere-megakernel-serving
status: active
---

# Cohere

## What it is

AI company building enterprise-focused models and the North platform. Publishes engineering detail on its
own serving infrastructure.

## Why it matters here

Cohere built what it describes as the **first fully fledged serving system around a decode megakernel** —
as distinct from a compiler that auto-generates megakernels or a batch-size-1 research demonstration. It
is the source behind [[Megakernels]], and the engineering report is unusually complete: a full task ABI,
16 opcodes, counter-based global-memory barriers, a four-step porting recipe, and a scheduler ablation.

Two of its findings are more instructive than the headline speedup. **Dependency-affinity placement made
the system 1–2% slower** — the intuitively correct optimisation is wrong here, and the authors say a
causal model "remains open," which is a candid marker of how immature megakernel scheduling is. And
**real expert distributions give more speedup than synthetic uniform routing** (1.32× versus 1.14× at
batch 8), because real requests concentrate on the same experts and leave more bubbles to fill — meaning
the conventional way to benchmark MoE serving **understates** the technique.

## Notes

- **North Mini Code** is 30B total with 3.3B active, using **parallel transformer layers** — attention and
  MoE computed from the same normalised input — which is what makes wave-quantisation backfill effective.
- Measured 292 tok/s at batch 1 against vLLM's 185 (62% versus 39% of a 470 tok/s speed-of-light ceiling
  on H100), and 1.25×–1.41× end-to-end, holding to 256K context with accuracy preserved.
- Builds explicitly on Hazy Research's "Look Ma, No Bubbles!", departing from it by using `wgmma`
  tensor-core instructions even at batch 1 and by abandoning shared-memory paging as buggy and
  high-overhead.
- States its limitations plainly: decode only, no mixed prefill/decode, maximum batch size 8.

## Related pages

- [[Megakernels]]
- [[GPU Kernel Optimization]]
- [[Inference Serving Engines]]
- [[LLM Inference]]
- [[Mixture of Experts]]
- [[Serving Benchmarks and Goodput]]
- [[Cohere - North Mini Code Megakernel Serving Engine]]
