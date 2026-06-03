---
type: source-summary
created: 2026-06-03
updated: 2026-06-03
source_id: src-2026-06-03-nvidia-locateanything
source_title: LocateAnything
source_author: NVIDIA Research
source_url: https://research.nvidia.com/labs/lpr/locate-anything/
tags:
  - source-summary
  - vision-language
  - grounding
  - multimodal
  - detection
source_ids:
  - src-2026-06-03-nvidia-locateanything
status: active
---

# NVIDIA - LocateAnything

## Summary

LocateAnything is a unified visual grounding and detection framework that treats bounding boxes as **atomic prediction units** instead of serializing coordinates token by token. The main idea, **Parallel Box Decoding (PBD)**, is to break the autoregressive bottleneck that slows many vision-language grounding systems while improving high-IoU localization quality.

The source matters because it frames grounding efficiency as both an architectural and an interface problem. Fast grounding is not just a computer-vision benchmark concern; it affects embodied agents, GUI agents, OCR-heavy systems, and document-understanding assistants that need precise spatial references rather than only fluent language output.

## Key claims

- Standard coordinate-token autoregression mismatches the coupled geometry of boxes and creates a practical decoding bottleneck.
- Parallel Box Decoding predicts full box coordinates in one step, preserving intra-box coherence while unlocking parallelism.
- The model uses a Moon-ViT vision encoder, Qwen2.5 language decoder, and MLP projector in a unified grounding/detection stack.
- Hybrid inference combines a fast parallel mode with fallback autoregressive re-decoding when format irregularity or spatial ambiguity appears.
- The training recipe includes **LocateAnything-Data**, a large-scale dataset with 138M language queries and 785M boxes spanning detection, GUI grounding, OCR, layout grounding, referring comprehension, and point localization.
- The reported result is a better speed/accuracy frontier, including substantially higher throughput and stronger high-IoU localization than comparable methods.

## Why it matters

This source opens a new multimodal branch in the vault around **vision-language grounding**. It is a useful reminder that many agents need a perception interface to images, screens, or documents, and that this interface has its own decoding bottlenecks analogous to token generation in text LLMs.

## Tensions / open questions

- How broadly does PBD generalize beyond box prediction to richer spatial outputs such as masks, trajectories, or 3D grounding?
- When is hybrid fallback worth the added implementation complexity compared with staying fully autoregressive?
- How much of the gain comes from box-aligned decoding versus the sheer scale and diversity of LocateAnything-Data?

## Affected pages

- [[Vision-Language Grounding]]
- [[AI Agents in Production]]
- [[NVIDIA]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/LocateAnything.md`

## Related pages

- [[Vision-Language Grounding]]
- [[AI Agents in Production]]
- [[NVIDIA]]
- [[World Models]]
- [[AI Knowledge Base Overview]]
