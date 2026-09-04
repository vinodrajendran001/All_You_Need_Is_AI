---
type: source-summary
created: 2026-09-04
updated: 2026-09-04
source_id: src-2026-09-02-raschka-astra-looped-transformers
source_title: "OpenAI Astra and Looped Transformers"
source_author: Sebastian Raschka
source_url: https://sebastianraschka.com/blog/2026/openai-astra-looped-transformers.html
tags:
  - source/summary
  - topic/architecture
  - topic/reasoning
source_ids:
  - src-2026-09-02-raschka-astra-looped-transformers
status: active
---

# Sebastian Raschka - OpenAI Astra and Looped Transformers

## Summary

A short debunking note written against press coverage of OpenAI's Astra model. Raschka's position is that the
"recurrent depth / looped transformer" framing is being treated as a breakthrough when **"the looped transformer
idea is just reusing layers in the transformer block"** — a small architectural tweak with published prior art
and a known, unspectacular trade-off curve.

The second half addresses a stronger claim in the coverage: that the technique "works in a way that obscures some
or all of the AI's reasoning, otherwise known as 'chain-of-thought'." Raschka argues this does not follow from
looping, and offers a more careful account of when latent computation displaces legible reasoning tokens.

## Key claims

**Looping is layer reuse, and the arithmetic is simple.** Nanbeige4.2-3B "is pretrained from scratch on 28T
tokens with a Looped Transformer that reuses the layer stack to increase capacity without adding parameters." In
practice it reuses the same **22-layer stack twice, giving an effective 44 layers without duplicating weights**.
That roughly doubles model capacity while storage and RAM stay flat — and costs "almost 2x as expensive in terms
of compute, because we run the embedded text through almost 2x as many layers."

**The published trade-off is modest and saturates fast.** Per the Nanbeige 4.2 technical report, "two passes gave
the best trade-off and retained about **75% of the token efficiency** of a standard architecture. (More passes
gave barely any gains but made the training much slower and much more expensive.)" So looping buys parameter
efficiency at a measured cost in token efficiency, and adding loops past two is not worth it.

**Nanbeige 4.2 is, as far as Raschka knows, the first notable open-weight model to adopt the approach**, but the
idea predates it: the NeurIPS paper *Mixture-of-Recursions: Learning dynamic recursive depths for adaptive
token-level computation*. That paper is the more sophisticated version, adding **a learned router that decides
whether each token receives one, two, or more passes**, so "easy tokens can exit early while harder tokens
receive additional computation."

**Looping does not by itself suppress visible chain of thought.** Raschka rejects the coverage's claim directly:
"Reusing layers does not by itself suppress visible chain of thought. It adds computation in hidden states before
the next token is emitted, just as ordinary transformer layers do." He allows that the journalist may have been
referring to a different technique or misunderstood this one.

**The legible-reasoning shift is a capacity effect, not a looping effect.** The one plausible reading he grants:
"if a model uses more of these recurrent passes, it may need to generate fewer intermediate reasoning tokens. So
then more of its computation happens in latent activations that cannot be read as text." But the crucial
qualification is that this is not special to looping — **"we would get the same effect if we were scaling up the
model size, like GPT 5.6 Luna -> GPT 5.6 Sol."** Any capacity increase that lets a model do more work per token
shifts computation out of the readable trace.

**On Astra specifically:** "Astra may be a really good model, but this shouldn't be about this 'looped
transformer aspect,' which is just a tiny architectural tweak."

## Why it matters

This gives [[Recursive Architectures]] a second and third source and, more importantly, its first hard numbers: a
22×2 = 44 configuration, a ~75% token-efficiency retention figure, and an explicit finding that more than two
passes does not pay. The vault's existing coverage came from an explainer thread that described the mechanism
without a released model or a measured trade-off.

It also lands a correction the vault needs on [[Chain-of-Thought Monitoring]] and [[Latent-Space Reasoning]].
Those pages have carried the concern that architectures moving reasoning into latent space degrade monitorability.
Raschka's argument sharpens it in a way that cuts against the alarming version: **the mechanism that reduces
legible reasoning is added capacity per token, not recurrence as such**, and plain model scaling produces the same
effect. That means monitorability erosion is not something to be prevented by rejecting a particular architecture
— it is a general consequence of models getting more capable, which makes it both more serious and less
attributable.

Read against [[Linear Attention and Recurrent Memory]], rebuilt the previous day with Qwen3.8's 3:1 hybrid ratio,
the vault now holds two independent published operating points for architectures that trade parameter or memory
cost against something else: Qwen's three Gated DeltaNet blocks per Gated Attention block, and Nanbeige's two
passes over a 22-layer stack. Neither is accompanied by an ablation curve.

## Tensions / open questions

- **This is a short note, not an analysis of Astra.** Raschka is explicit that he is reasoning from press
  coverage and from published models with similar descriptions. He does not claim to know Astra's architecture,
  so the debunk is of the *reporting*, and the possibility that Astra uses some other technique is left open.
- **The 75% token-efficiency figure is relayed, not verified.** It comes from Nanbeige's own technical report and
  is not independently reproduced here.
- **"Roughly doubles the size of the model" is loose.** Raschka brackets embedding and output layers to make the
  claim, and capacity gained by weight reuse is not obviously equivalent to capacity gained from new parameters —
  the 75% token-efficiency retention is itself evidence that it is not.
- **The latent-computation argument is asserted, not measured.** That more recurrent passes may mean fewer
  reasoning tokens is offered as "the only plausible interpretation," with no experiment showing the trade.
- **Mixture-of-Recursions is described but not evaluated.** Whether token-level adaptive depth beats a fixed two
  passes in practice, and at what routing overhead, is not addressed.

## Affected pages

<!-- Pages this ingest actually changed, per ingest step 4. Every page listed here must cite this
     source's `source_id` or link back to this summary. Do not list pages that are merely relevant,
     and do not list the control pages (index, log, overview) — every ingest updates those by
     definition. Merely-relevant links belong under `## Related pages`. -->

- [[Recursive Architectures]]
- [[Linear Attention and Recurrent Memory]]
- [[Chain-of-Thought Monitoring]]
- [[Latent-Space Reasoning]]
- [[Reasoning Trace Privacy]]
- [[Sebastian Raschka]]

## Related pages

- [[Transformer Architecture]]
- [[Test-Time Scaling]]
- [[LLM Reasoning]]
- [[Reasoning Effort Control]]
- [[Small Language Models]]
- [[Open Model Ecosystems]]
- [[Mixture of Experts]]
- [[@neural_avb - What Are Looped Transformers?]]

## Citations

- Raw capture: [[2026-09-02 Sebastian Raschka - OpenAI Astra and Looped Transformers]]
- Source: <https://sebastianraschka.com/blog/2026/openai-astra-looped-transformers.html>
