---
type: entity
created: 2026-08-25
updated: 2026-08-25
entity_kind: person
tags:
  - entity
  - person
  - hardware
  - accelerators
  - writing
source_ids:
  - src-2026-08-25-jacob-peake-ai-chip-architectures
status: active
---

# Jacob Peake

## What it is

Independent technical writer on AI hardware, author of the comparative accelerator survey at `jacobpeake.com`.

## Why it matters here

[[Jacob Peake - AI Chip Architectures]] is the vault's most complete single treatment of [[AI Accelerator Architecture]], and its value is methodological as much as informational. Three habits make it durable:

- **A fixed comparison frame.** Every architecture is examined through the same four lenses — genealogy, architecture, scaling, software — so NVIDIA, TPU, AMD, Cerebras, Trainium, and Groq become comparable rather than six separate marketing narratives.
- **Design commitments stated as bets.** Reducing each architecture to an explicit list ("systolic array," "software scratchpads," "compiler scheduling," "MAC-only silicon," "determinism over tolerance") turns hardware comparison into a set of falsifiable choices instead of a spec-sheet contest.
- **Explicit epistemic marking.** Analyst-derived, era-inferred, and vendor-aggregate figures carry an asterisk; undisclosed specs are marked `n/d`; and the tables state upfront that memory-bandwidth and scale-up columns are *not* directly comparable across vendors. That is the standard this knowledge base tries to hold sources to.

The survey's framing question — where data lives, how it moves, what the compute units look like, and how chips talk at scale — is a reusable checklist for reading any future accelerator announcement.

## Notes

- The article carries no publication date; the vault capture is dated to 2026-08-25 and its most recent cited events are mid-2026.
- Its problem statement (matmul shape decides the compute/bandwidth regime) is the hardware-side twin of the analysis in [[Changyi Yang - Why MLA and MTP Fight Each Other]]; the two anchor [[Arithmetic Intensity and the Roofline Model]] together.

## Related pages

- [[Jacob Peake - AI Chip Architectures]]
- [[AI Accelerator Architecture]]
- [[Arithmetic Intensity and the Roofline Model]]
- [[Cerebras]]
- [[Groq]]
- [[NVIDIA]]
- [[AI Knowledge Base Overview]]
