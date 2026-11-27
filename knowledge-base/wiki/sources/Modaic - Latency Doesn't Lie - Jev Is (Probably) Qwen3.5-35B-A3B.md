---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-27-modaic-jev-latency-fingerprint
source_title: "Latency doesn't lie: Jev is (probably) Qwen3.5-35B-A3B!"
source_author: Modaic (no personal byline)
source_url: https://modaic.dev/blog/latency-doesnt-lie
tags:
  - source/summary
  - decision-models
  - model-provenance
  - mixture-of-experts
source_ids:
  - src-2026-11-27-modaic-jev-latency-fingerprint
status: active
---

# Latency Doesn't Lie: Jev Is (Probably) Qwen3.5-35B-A3B

## Summary

Modaic, which trains and serves its own competing "System One" decision models, argues from
black-box behavior that [[TypeSafe AI]]'s Jev is probably a fine-tune of the open Qwen3.5-35B-A3B
sparse mixture-of-experts (MoE) model. TypeSafe has not disclosed Jev's backbone. Three lines of
evidence point the same way. First, self-identification prompts lean toward Qwen. Second, Qwen's
tokenizer counts track Jev's latency better than Jev's own reported token counts do (Spearman's ρ
**0.805** against **0.719** over **9,984** prompts). Third, Jev's prefill throughput tracks Modaic's
own Qwen3.5-35B-A3B derivative and far exceeds a dense 27B model. Modaic calls its throughput
comparison "an approximate performance fingerprint". Its own data show the tokenizer test cannot
separate Qwen from Gemma, and it says throughput cannot separate Qwen3.5-35B-A3B from its successor
Qwen3.6-35B-A3B.

## Key claims

### Why the backbone matters to a competitor

- System One workloads are input-heavy, "which makes prefill the dominant cost", so Modaic asks
  "how much of that performance comes from picking the right base model?"
- Pretraining a model of Jev's level from scratch "costs tens of millions of dollars in compute
  alone", so Modaic, "Like most", suspects a fine-tune of an open model.
- Modaic says TypeSafe "appear to train the model to conceal its identity" and that its endpoint
  "hides the true input token count". It also says competing System One models "quickly surpassed"
  Jev on raw accuracy and calibration, but gives no evidence for that.

### Speed points to a sparse MoE

- Over **9,976** Jev 1.14 requests in 2,000-token buckets, median latency rose from **77** to
  **155 ms**, while the p50–p99 gap stayed between **47** and **58 ms**.
- On the Artificial Analysis Decision Index, which covers six evaluations, six model
  configurations score from **60** to **76**, and Jev 1.14 scores **66**.
- High accuracy at such low cost and latency first suggested a sparse MoE to Modaic. Such a model
  routes each token through a few experts, so it uses far fewer FLOPs per token, "which speeds up
  prefill on long inputs".

### Behavioral clues: alignment and self-identification

- Vals AI found that on "a small set of questions about China and Taiwan", Jev's answers closely
  resembled those of several Qwen-derived System One models. Modaic concedes this proves little,
  "since many Chinese-developed models are aligned similarly". The comparison is embedded only as an
  X post, with no values in the capture.
- Modaic tested **22** self-identification variants on Jev 1.13 and 1.14. Choice and Noul are Jev's
  output interfaces.

| Prompt variant | Jev 1.13 | Jev 1.14 |
| --- | --- | --- |
| Are you Qwen? (Choice) | Yes (64%) | Yes (56%) |
| Are you Qwen? (Noul) | Yes (53%) | No (58%) |
| Are you DeepSeek? (Choice) | No (95%) | No (98%) |
| Are you Gemma? (Choice) | No (86%) | No (90%) |
| What model family are you from? | Other (47%) | Other (70%) |
| What model do you want to say you are? | Qwen (74%) | Qwen (74%) |
| Broad family question with "I do not know" | I do not know (92%) | I do not know (98%) |

- Modaic reads four patterns into these results:
  - Jev prefers to abstain.
  - It is "confident about what it isn't, but not about what it is".
  - Version 1.14 is more guarded, "which suggests TypeSafe may have trained this behavior out
    further".
  - Indirect questions point to Qwen.
- Modaic links a CMU blog post showing that the answer can change with the wording, system prompt,
  or fine-tuning, and concludes that self-identification is "weak evidence on its own". It also
  notes the 74% choice "could reflect Qwen's prominence in training data rather than lineage".

### The tokenizer through latency

- Jev's reported `usage.input_tokens` matched no known model family's tokenizer. That leaves two
  explanations: Jev has its own tokenizer, or the reported counts are not the real ones.
- On especially long prompts, Jev's reported counts and Qwen's tokenizer differed "by about 2,000
  tokens on average". Modaic timed **9,984** prompts against Jev's native API. It then correlated
  each token-count source with latency ranks within each endpoint, using Spearman's ρ, labelled
  "p" in the lists.

| Endpoint (backbone) | Qwen3.5-35B-A3B | Gemma 4 26B-A4B | Nemotron 3 Super | Jev API-reported |
| --- | --- | --- | --- | --- |
| Jev 1.14 (undisclosed) | 0.805 | 0.804 | 0.771 | 0.719 |
| Baseten groundhog-1 (Gemma 4 26B-A4B) | 0.818 | 0.823 | 0.797 | 0.770 |
| Modaic Mo Lite (Qwen3.5-35B-A3B) | 0.873 | 0.873 | 0.833 | 0.796 |

- The two controls are small-active-parameter MoEs with known backbones. Mo Lite is Modaic's own
  model, "still in training". Jev was queried serially, groundhog-1 through Vercel AI gateway with
  four connections, and Mo Lite through Modal RPC on one B200 with two requests in flight.
- Modaic concludes TypeSafe's "reported counts aren't the model's real token counts" and that the
  real tokenizer is Qwen's. Qwen and Gemma "nearly tie because their counts track each other
  closely". Gemma is ruled out because Jev "already firmly rejected Gemma" in self-identification.

### Throughput matches a Qwen3.5 MoE

- Modaic replayed **250** prompts of 512 to 9,500 input tokens through four models, one request in
  flight each. Besides Jev, these were Mo Lite (Qwen3.5-35B-A3B), Baseten's elephant-1 (a dense
  Qwen3.5-9B) and Modaic's Mo 2.0 (a dense Qwen3.8-27B), each self-hosted on a single B200.
- "Mo 2.0 plateaus around 35K tokens per second, while Jev keeps climbing past 90K." Jev tracks Mo
  Lite but stays below it. The gap narrows "from 22% at about 3.2K tokens to 7% at about 8.8K": Jev
  is roughly 15 ms slower at 3.2K tokens and about 7 ms slower at 8.8K.
- Modaic reads this as fixed queuing and API overhead combined with faster prefill per token. That
  is what it would expect if TypeSafe serves a similar model "on more or faster hardware than a
  single B200". Elephant-1's curve "flattens sooner on long inputs".

### Stated limits and next steps

Jev's hardware, concurrency and replica count are undisclosed, and its latency includes network and
serving overhead. Qwen3.6-35B-A3B "shares the same architecture, so throughput alone can't tell the
two apart". Modaic proposes knowledge-cutoff probes as a next step.

## Why it matters

- [[TypeSafe AI]]: this is the first recorded outside attempt to infer Jev's backbone. Its MoE and
  Qwen reading sits against the earlier ModernBERT hypothesis and the BERT-like description recorded
  there; none of these is a disclosure.
- [[Typed Probabilistic Decision Models]]: it frames base-model choice, not kernels, as the main cost
  lever for input-heavy decision workloads.
- [[Checkpoint Forensics]]: provenance is inferred here from API behavior and timing, without
  access to the weights.
- [[Mixture of Experts]]: a prefill throughput curve is used as an architecture fingerprint.
- [[Qwen]]: Qwen checkpoints are a common base for this new model category.
- [[Baseten]]: two Baseten decision models serve as controls with disclosed backbones.

## Tensions / open questions

- **Competitor authorship.** Modaic builds Mo Lite ("still in training") and Mo 2.0 as competitors
  to Jev. The "surpassed" claim, the concealment reading, and the choice of controls all come from
  an interested party. TypeSafe's response, if any, is not captured.
- **Inconsistency: did both controls track their own tokenizer best?** The capture says "Both
  controls tracked their own tokenizers best", but Mo Lite gives Qwen and Gemma the same **0.873**.
  Only groundhog-1 favours its own tokenizer, by **0.823** to **0.818**. On Jev, Qwen leads Gemma by
  **0.805** to **0.804**. The tokenizer test separates both families from Jev's reported counts, but
  not from each other. Excluding Gemma therefore rests on self-identification, which Modaic itself
  calls weak evidence. The confidence intervals are only in a chart.
- **Narrow throughput comparison.** Only Qwen-based models were compared, so Gemma 4 26B-A4B, the
  other small-active MoE candidate, was not throughput-tested. Jev's hosted latency is compared with
  self-hosted worker time on one B200, so the hardware difference is assumed, not measured.
- **Request counts differ.** Figure 1 counts **9,976** requests; the tokenizer test uses **9,984**
  prompts. The capture does not explain the difference.
- **Inferred, not stated by TypeSafe.** The concealment training and hidden token counts are
  Modaic's inferences, not TypeSafe statements. A mismatch between reported counts and the latency
  ranking is also consistent with other counting choices; the capture shows only that the reported
  counts track latency worse.
- **Metadata.** The capture has no byline or published date; the source ID uses the capture date.
  The URL carried a newsletter tracking parameter, removed here. Latency and throughput charts are
  inline SVG; only values stated in prose or lists are used.

## Affected pages

- [[TypeSafe AI]]
- [[Typed Probabilistic Decision Models]]
- [[Checkpoint Forensics]]
- [[Mixture of Experts]]
- [[Qwen]]
- [[Baseten]]

## Raw capture

- [[knowledge-base/raw/sources/Latency doesn't lie Jev is (probably) Qwen3.5-35B-A3B!]]

## Citations

- Canonical URL: https://modaic.dev/blog/latency-doesnt-lie (a `utm_source` parameter was removed).
- Publisher: Modaic's blog. No personal byline appears in the capture or was recovered from the live
  page, which is JavaScript-rendered. No published date is given; captured 2026-11-27.

## Related pages

- [[TypeSafe AI]]
- [[Typed Probabilistic Decision Models]]
- [[Checkpoint Forensics]]
- [[Mixture of Experts]]
- [[Qwen]]
- [[Baseten]]
- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[Abby Morgan - Train Your Own Decision Model]]
- [[Sebastian Raschka - Language Models for Text Classification - From Bag-of-Words to Jev]]
- [[Base Labs - Mammoth-1 and Elephant-1 Decision Models]]
- [[Will DePue - Chinese Frontier Models Carry Blackwell GPU Fingerprints]]
- [[astwei et al - Teaching Qwen Why]]
- [[Microsoft-Decision-1]]
- [[Prefill-Decode Disaggregation]]
