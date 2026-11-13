---
type: concept
created: 2026-06-03
updated: 2026-11-13
tags:
  - concept
  - multimodal
  - vision-language
  - grounding
  - detection
  - robotics
source_ids:
  - src-2026-06-03-nvidia-locateanything
  - src-2026-09-21-liu-just-in-time-agentic-ocr
  - src-2026-11-11-nvidia-gr00t-2
status: active
---

# Vision-Language Grounding

## Definition

Vision-language grounding is the task of linking natural-language intent to specific spatial regions in an image, screen, document, or scene, often by predicting bounding boxes, points, or other localized outputs.

## Why it matters

Many multimodal systems do not just need to describe images; they need to **point** precisely. GUI agents need to identify clickable elements, document assistants need to localize layout regions or text spans, and embodied agents need to ground instructions in the physical world.

## Current synthesis

- LocateAnything frames grounding as a decoding problem as much as a representation problem. If box coordinates are generated token by token, inference becomes unnecessarily sequential.
- Parallel Box Decoding (PBD) treats a box as one atomic prediction unit, which better matches the geometry of the task and unlocks more parallelism.
- The source suggests a useful task unification: object detection, referring expression comprehension, GUI grounding, OCR, layout grounding, and point localization can all be viewed as variations of text-conditioned spatial prediction.
- Hybrid inference is a practical compromise. Fast parallel decoding handles the common case, while fallback autoregressive decoding handles malformed or ambiguous cases.
- The training-data story matters almost as much as the decoder. LocateAnything-Data broadens supervision across many grounding modalities, which is likely part of why the model generalizes well across benchmarks.
- This makes grounding analogous to tool use in language agents: the quality of the system depends heavily on the fidelity of the interface between the model and the world it needs to act on.

## Visual grounding as an escalation tier

[[Jerry Liu - Just-in-Time Agentic OCR]] applies visual parsing only after retrieval identifies a
candidate page. The design reduces visual inference cost but makes first-pass extraction a recall
bottleneck; layout complexity is useful routing evidence, not a substitute for task relevance.

## Points on a camera view as a planner-to-policy interface

[[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
uses grounding in the opposite direction from LocateAnything. Instead of a model predicting where
language refers to, a planner writes spatial marks for a motor policy to read. In "visual steering",
a reasoning model marks a grasp point on the target object and a release point at its destination on
GR00T 2's camera view, coloured by the arm that should act. GR00T 2 generates the approach, grasp,
transport, and release. The planner then looks again and decides whether to continue, retry, or
stop. The marks are extracted from gripper and hand states in existing demonstrations, so "training
needs no new data", and the same model still follows language alone.

The gain comes from settling what language leaves ambiguous, especially in clutter: which object,
where it goes, and which arm acts.

| Short "what and where" instructions | YAM | Dexter |
| --- | --- | --- |
| Task instruction only | 40% | 30% |
| Planner step instructions | 66% | 33% |
| Step instructions plus marks | 92% | 70% |

YAM ran **90** trials per setting and Dexter **64**. For instructions about *how* to move, such as
action or grasp type, the gain is smaller: **44%** to **59%** on YAM. Over long horizons on YAM,
nothing completes without marks, even with step instructions. With marks, trash sorting completes
**17 of 20** episodes and board disassembly **3 of 10**. On Dexter, full tasks are still rarely
completed.

The limits bear on the open question below about output interfaces. Two points carry a target and a
destination, but "neither an object's final orientation nor the motion between grasp and release,
such as pouring or wiping", which still come from language. The results are first-party, from one
planner-policy pair, and the reasoning model is not named.

## Open questions

- What is the right output interface beyond boxes: points, masks, polygons, or mixed spatial primitives?
- How transferable are grounding gains across GUIs, documents, robotics, and natural-image tasks?
- Can grounding models be made both more precise and more interactive without sacrificing robustness?
- Could richer marks, such as orientation arrows or motion paths, carry what GR00T 2's grasp and
  release points leave to language?

## Related pages

- [[NVIDIA - LocateAnything]]
- [[AI Agents in Production]]
- [[NVIDIA]]
- [[World Models]]
- [[AI Knowledge Base Overview]]
- [[NVIDIA - GR00T 2 - Scaling Robot Foundation Models for Generalization, Dexterity, and Adaptation]]
- [[Robot Training Data]]
- [[Agent Planning]]
