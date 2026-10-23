---
type: social-post
created: 2026-10-23
updated: 2026-10-23
tags:
  - post
platforms:
  - linkedin
  - x
pages_used:
  - Chain-of-Thought Monitoring
  - Nikita Kezin et al - Messages in Rendered Images
topics:
  - messages in images
  - visual information channels
  - multimodal evaluation
covers_from: 2026-10-16
covers_through: 2026-10-23
status: ready
---

# The Skyline Was the Message

## LinkedIn post

The AI drew a city skyline. The buildings were the message.

If an AI assistant can read images, a picture is more than decoration. It can carry information even when the code that drew it is gone.

A small experiment by Nikita Kezin and colleagues makes that idea wonderfully concrete.

The researchers supplied 50 short messages and asked Fable, an AI model, to hide each one in a drawing. Then they opened a fresh session and gave it only the rendered image. No drawing code. No explanation of the encoding. The reader was asked to look for a message without assuming one existed, and could use image-analysis tools.

One recurring design was a skyline. Different building heights represented different letters. The reader could measure the shapes and look for a pattern.

Think of a chart dressed up for a night out: the bars became buildings, but they still carried information.

That explains why removing the drawing code was not enough to remove the message. The information was in the visible geometry, which survived rendering. The picture itself was doing the communicating.

Across the 50 messages, the authors report 78% recovery. An important detail: "recovered" meant at least 90% string similarity after lowercasing and keeping only letters and digits. It did not mean every character was copied perfectly. And this was tool-assisted decoding, not a model simply glancing at the picture.

Before we give the skyline a spy-movie soundtrack: the models were explicitly asked to do this. Every test image deliberately contained a message; there was no clean-image control to measure how often the reader invented one. The experiment did not show spontaneous secrecy, obedience to hidden instructions, or a successful monitoring bypass. The authors say the decoding remained visible in tool calls.

The practical lesson is smaller, and useful: if your AI accepts images, test what it reads from them, not just what it reads from text. Include ordinary images with no planted message, and inspect the tools it uses to interpret them.

A screenshot can remove the drawing's code without removing what the drawing says.

When you test an image-reading assistant, do you check only what it misses, or also what it imagines is there?

Source: Nikita Kezin, 13ryanC, hronir, and James Chua:
https://www.lesswrong.com/posts/WHEQps5PK8LrrcTAb/how-does-fable-5-1-hide-messages-in-images

#MultimodalAI #AIEvaluation #ComputerVision #AIAgents

## X post

**A) Standalone** (249 chars):

In a prompted experiment, AI model Fable hid messages in images; a fresh session used tools to read them without the drawing code. The pixels carried the message. Test images as AI inputs, not decoration. Nikita Kezin et al.: https://www.lesswrong.com/posts/WHEQps5PK8LrrcTAb/how-does-fable-5-1-hide-messages-in-images

**B) Thread:**

1. (243 chars)
The AI drew a skyline. The buildings were the message.

In a prompted experiment, Fable put messages in images that a fresh session could read with tools. Removing the drawing code did not remove the message. Test the image, not just its text.

2. (264 chars)
The setup: researchers supplied 50 short messages and asked Fable to hide each in a drawing. A fresh session received only the rendered image, not the drawing code or an explanation of the encoding. It was asked to look for a message, without assuming one existed.

3. (246 chars)
One recurring trick was building height: different heights represented different letters. The decoder used image-analysis tools to measure shapes and look for a pattern. Think of a chart dressed as a city skyline: the meaning was in the geometry.

4. (237 chars)
The authors report 78% recovery across the 50 messages. That meant at least 90% string similarity after lowercasing and keeping only letters and digits, NOT exact transcription. The decoder had tools; this was not unaided visual reading.

5. (236 chars)
Why could it work without the drawing code? Rendering preserved the visible shapes carrying the information. Removing the code changed the format, not necessarily the message. An image can be both a picture and something an AI can read.

6. (247 chars)
The limits: every test image deliberately carried a message; no clean-image control was reported. This was not a test of spontaneous secrecy, obeying hidden commands, or bypassing a monitor. The authors say decoding remained visible in tool calls.

7. (252 chars)
For image-taking AI, test what it reads from pictures, not just text. Include clean images to check for invented messages, and inspect its tool use. A new format is not a blank slate.

Nikita Kezin, 13ryanC, hronir & James Chua: https://www.lesswrong.com/posts/WHEQps5PK8LrrcTAb/how-does-fable-5-1-hide-messages-in-images

**Ship:** Thread. The skyline mechanism makes the idea memorable, and the connected explanation
keeps the scoring rule and experimental limits next to the result. The standalone is a complete,
nonnumeric alternative, not a teaser. Counts include spaces and line breaks, with each URL
counted as 23 characters under X's link weighting; numbered labels are not part of the copy.

## Hook variants

1. **Visual reveal:** "The AI drew a city skyline. The buildings were the message."
2. **Analogy:** "A chart dressed as a city skyline is still carrying data."
3. **Format surprise:** "The drawing code was gone. The message was still readable."

**Recommended:** 1 for both platforms. It gives a cold reader something concrete to picture,
then the body explains the result without turning it into a claim about secret intent.

## Why this topic

Editorial replacement for [[2026-10-23 A Safe Query Is Not a Correct Answer]], not another
weekly slot. Reused **2026-10-16 through 2026-10-23**, reread the October 16, 19, and 23
ingest entries, and included the supplemental five-source October 23 ingest added after
the rejected draft. Recent wiki commits corroborate those updates and the later lint repairs.

ByteByteGo was excluded before selection, including its inherited evidence in shared concepts
and its archived candidates. These three eligible angles come from the supplemental ingest:

| Angle | Clarity | Completeness | Surprise | Concreteness | Reach | Freshness | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **The skyline was the message** | 5 | 5 | 5 | 5 | 4 | 5 | **29** |
| An AI supervisor can spend the attention it is meant to save | 5 | 4 | 4 | 5 | 5 | 5 | 28 |
| Teach a decision model that the correct answer may be absent | 4 | 4 | 4 | 4 | 4 | 5 | 25 |

The runner-up comes from Dan McAteer's account: 99 of 111 turns triggered his supervisor,
and he reports starting to skim its output. It is relatable, but anecdotal; trigger frequency
does not measure false positives or useful interventions. The third comes from Base Labs'
abstention-training recipe. It is teachable, but the report does not isolate that ingredient's
effect on reliability. Neither candidate supplies evidence to the selected post.

The selected angle has one visual example, an explainable mechanism, and a bounded reported
result. It is not another "safe is not correct" argument or a product-release recap.
[[Chain-of-Thought Monitoring]] is not in cooldown; the selected image-channel section has
not been used in an active post. Its six-week cooldown ends **2026-12-04**.

## Reader check

Reading only the public copy:

1. **Situation:** An image-reading AI can receive a message through a drawing, not just text.
2. **Single claim:** Rendering can remove drawing code while retaining information in visible shapes.
3. **Example:** In a deliberately prompted experiment, Fable created message-bearing drawings;
   a fresh session decoded images with tools and without the source code or supplied scheme.
4. **Mechanism:** Building heights represented letters, so the visible geometry carried the message.
5. **Limits:** The reported recovery threshold is approximate; all images contained messages;
   neither spontaneous concealment nor successful evasion nor following instructions was demonstrated.
6. **Action:** Evaluate images as information-bearing inputs, add clean controls, and inspect tool use.

LinkedIn and the thread complete that progression before the closing question or attribution.
The standalone omits the rate and skyline detail but retains the prompted setup, tool assistance,
information surviving code removal, and practical action. It claims no monitoring failure.
Drawing formats and library names are omitted rather than left as unexplained acronyms.
The chart analogy explains the mechanism; it is not a second experimental result.

## Fact check

Evidence: [[Nikita Kezin et al - Messages in Rendered Images]], checked against its raw capture,
especially Introduction, Height encoding, Method, Results, and Implications. The only spine
section used is **Image-message recovery is a channel test, not a monitor-evasion result** in
[[Chain-of-Thought Monitoring]].

| Public claim | Evidence and boundary |
| --- | --- |
| 50 supplied messages; explicitly prompted creation | Raw Method and Introduction; not autonomous behavior. |
| Fresh session, image only, no drawing code or supplied encoding scheme | Raw Introduction and Method. The decoder was told not to assume a message existed. |
| Building heights represent letters; tools measure shapes | Raw Height encoding and decoding examples; paraphrased, not a claim about all images. |
| Information survives rendering in visible geometry | Demonstrated by these examples and recorded in the source summary; "can" does not imply robustness to every transformation. |
| 78% recovery | Authors' reported result over 50 messages, not independently replicated here. |
| At least 90% similarity after lowercasing and keeping letters/digits | Raw Method; explicitly preferred over the inconsistent "exactly" figure caption. Both long-form bodies retain this qualifier. |
| Tool-assisted rather than unaided vision | Raw Method supplies Python and image-analysis libraries. |
| Every evaluated image carried a message; no clean-image control | Source summary's evaluation boundary and raw construction method. No false-positive rate is inferred. |
| No demonstrated spontaneous secrecy, obedience, or monitor bypass | Source summary and spine section distinguish decoding from those unevaluated behaviors. |
| Decoding visible in tool calls | Raw Implications, explicitly attributed to the authors. |
| Add clean controls and inspect image/tool inputs | Editorial recommendation derived from the recorded evaluation gaps, not a proven defense. |

**Source-exclusion check:** The primary source is the LessWrong article by Nikita Kezin,
13ryanC, hronir, and James Chua, not ByteByteGo. The mixed-source spine contains unrelated
ByteByteGo material, but none of it supplies this post's topic, example, claims, or attribution.
Every empirical claim above is independently supported by the primary article read directly.

**Compression check:** The standalone drops the numerical result rather than its scoring
qualifier. Both X openings retain deliberate prompting and tool assistance. Thread post 4
keeps the threshold and normalization; post 6 keeps the missing control and no-evasion boundary.
No copy turns recovery into obedience or a measured safety failure.

**Comprehension check:** Picture -> experiment -> geometry -> result -> limits -> evaluation
action. The conclusion follows from retained visual information, not a leap from a benchmark
score to a security claim.

**Cut:** Cross-model recovery counts, language counts, encoding taxonomies, and decoding code.
They distract from the one-example explanation. Also excluded exact-transcription language,
claims of covert intent, undetectability, production prevalence, and proven mitigation.
The source's byline/BibTeX discrepancy is retained in the summary; public attribution follows
its `source_author` rather than guessing mappings between handles and names.

## Attribution

- **Nikita Kezin, 13ryanC, hronir, and James Chua**, "How does Fable 5.1 hide messages in images?"
  <https://www.lesswrong.com/posts/WHEQps5PK8LrrcTAb/how-does-fable-5-1-hide-messages-in-images>.
  Published 2026-10-22; captured and ingested 2026-10-23. Small author-run experiment,
  not a production incident or an independently reproduced evaluation.

## Hashtags

LinkedIn: #MultimodalAI #AIEvaluation #ComputerVision #AIAgents

X: none.

## Related pages

- [[Chain-of-Thought Monitoring]] - spine; only the primary-source-backed image-channel section is used
- [[Nikita Kezin et al - Messages in Rendered Images]] - experimental setup, result, and evidence limits
- [[Post Archive]] - active draft and cooldown ledger
