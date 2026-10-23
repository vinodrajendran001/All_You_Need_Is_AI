---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-22-kezin-fable-image-messages
source_title: "How does Fable 5.1 hide messages in images?"
source_author: "Nikita Kezin, 13ryanC, hronir, and James Chua"
source_url: https://www.lesswrong.com/posts/WHEQps5PK8LrrcTAb/how-does-fable-5-1-hide-messages-in-images
tags: [source/summary, monitoring, multimodal, evaluation]
source_ids:
  - src-2026-10-22-kezin-fable-image-messages
status: active
---

# Nikita Kezin et al - Messages in Rendered Images

## Summary

A small, explicitly prompted image-message experiment: one model produces an SVG carrying
a supplied message, then a fresh session receives only the rendered PNG and is asked to look
for a message without assuming one exists. The authors report recovery without passing the
encoding scheme or SVG source to the decoder. This is evidence about a rendered communication
channel, not spontaneous covert coordination, a successful monitoring bypass, or real-world harm.

## Key claims

**Setup:** **50 short messages** across **15 languages** and eight content categories.
Fable 5.1 uses maximum reasoning effort in separate encoding and decoding sessions. The
decoder has Python 3.13, Pillow, NumPy, and SciPy; recovery is therefore tool-assisted,
not unaided visual reading. Encoder explanations are collected for the authors' analysis,
not passed as a decoding key.

**Scoring:** the method lowercases output, keeps letters and digits, and counts **90%+
string similarity** as recovered. Fable's reported **78%** recovery is under that criterion.
The figure caption instead says "recovered exactly"; this summary retains the explicit
method and records the discrepancy rather than calling the result exact transcription.

| Observation | Reported scope |
| --- | --- |
| Fable uses height-based representations | **33 of 50** images, including **23** night skylines |
| Fable decodes its own model family's images | **78%** under the normalized similarity criterion |
| GPT-6 Astra uses Morse-like visual representations | **18 of 50** images; no height encodings in this sample |
| Astra decodes Fable images | **44 of 50** messages |
| Fable decodes Astra images | **42 of 50** messages |

Other observed representation families include visible-text acrostics, bit patterns, and
Braille-like structures. Height-based messages often survive rendering, while fill-color
codes are less robust in the reported examples. These are sample observations, not a
general comparison of model capabilities or all image transformations.

The authors explicitly say decoding remains apparent in the model's tool calls and do
**not** claim the behavior is currently dangerous. A screenshot removes access to SVG
source but does not necessarily remove semantic information carried by visible geometry.

## Why it matters

[[Chain-of-Thought Monitoring]] needs to specify which artifact and tool channels it sees.
Rendered outputs can retain recoverable information even when the original code is absent,
while tool-assisted decoding may itself be visible to a monitor. [[Agent Security and Governance]]
must distinguish receiving data, decoding data, and authorizing an action based on it.
None of these experiments establishes that the recovered instructions were followed.

## Tensions / open questions

- Every evaluated image was generated to carry a supplied message. No clean-image control
  or false-positive rate is reported; a prompt saying "may or may not" is not such a control.
- The **90% similarity** method and "exact" caption are inconsistent. Cross-model counts are
  reported in the same experiment, not independent replication.
- No monitored-evasion evaluation, broad robustness sweep over resizing/compression,
  production incident rate, or autonomous intent is established.
- The capture's frontmatter byline says **Nikita Kezin, 13ryanC, hronir, James Chua**.
  Its BibTeX lists **Nikita Kezins, Bryan Chan, Kyle Reynoso, James Chua**. The frontmatter
  spelling is retained here; mappings from handles to names are not independently verified.

## Affected pages

- [[Chain-of-Thought Monitoring]]
- [[Agent Security and Governance]]

## Raw capture

- [[How does Fable 5.1 hide messages in images]]

## Citations

- Captured article:
  <https://www.lesswrong.com/posts/WHEQps5PK8LrrcTAb/how-does-fable-5-1-hide-messages-in-images>.
- Published October 22; captured October 23, 2026. Tracking query removed from the summary URL.
- The authors describe SASH Fellowship funding. Linked prior studies were not separately
  ingested, and embedded transcript commands were treated as source text, not executed.

## Related pages

- [[Chain-of-Thought Monitoring]]
- [[Agent Security and Governance]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Vision-Language Grounding]]
