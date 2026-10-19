---
type: source-summary
created: 2026-09-25
updated: 2026-10-19
source_id: src-2026-09-22-canham-jev-explained
source_title: "Jev Explained for Normies"
source_author: Matthew Canham
source_url: https://x.com/matthewcanham/status/2102077098756280413
tags: [source/summary, decision-models, structured-output]
source_ids: [src-2026-09-22-canham-jev-explained]
status: active
---

# Matthew Canham - Jev Explained

## Summary

Matthew Canham's long X post explains Jev to non-technical product builders. Jev is the decision
model the vault attributes to [[TypeSafe AI]]; the post itself does not name the developer. Its
frame is historical. Rules handle simple decisions. Trained classifiers handle complex ones but do
not generalize beyond their domain. LLMs generalize but are slow and expensive per decision. Jev is
presented as "a classifier that generalizes": it takes a question, a set of possible answers, and
context ("state"), and returns a selected answer with a probability instead of generated text.

The author is an enthusiastic independent explainer ("I really do believe the hype is real"), not
the vendor. The post runs no benchmark of its own. Its speed and cost ranges are relayed claims, and
its example outputs illustrate the response format, not measured accuracy.

## Key claims

- **Interface.** The input is the question, the possible answers, and the state. The output is the
  chosen answer and "the probability that answer is correct." There is no chat.
- **Three decision types.** A yes/no **Noul** returns the estimated probability that a statement is
  true. **Choice** selects from up to **255** options with a probability for each. **Score** rates
  against a scale of **2 to 10** levels.
- **Request shape.** The JSON examples name a model (`jev-latest`), pass the state text, and define
  each named question with a type, instructions, and per-answer criteria. The criteria prose is
  therefore part of the decision contract.
- **Worked examples** use one hotdog-stand review. The Noul gives **0.04** that it is a food
  complaint. Choice picks "queue" at **0.80** (food 0.15, service 0.03, other 0.02) alongside a
  separate confidence field of **0.60**. Score returns **2.1** on a five-level scale indexed 0–4,
  which equals the expected value of the returned distribution (the vault's arithmetic).
- **Speed and cost.** "The claims are that Jev is 20-200x faster and 40-400x cheaper than comparable
  LLMs," explained by returning a decision instead of generating token by token. An embedded video
  compares 60 reviews against gpt-5.6 Luna; the capture contains no figures from it.
- **Suggested uses.** Yes/no for churn signals, missed shipment deadlines, student misconceptions,
  unowned meeting commitments, and stuck game players. Choice for routing a request to a specialist
  team, matching tutorials, choosing a responding game character, picking an audio-guide segment,
  or choosing an ingredient substitute. Score for bug disruption, itinerary fit, support for a
  product hypothesis, dialogue voice drift, and how much a hint reveals.

## Why it matters

The post reduces the [[Typed Probabilistic Decision Models]] interface to its essentials: state, a
typed question, criteria-defined options, and probabilities. It also shows that the option criteria
are written prose the model has to interpret. Its use-case list is a reminder that many product
decisions are classification or rating problems that need no generated answer, which is the cost
argument developed on [[Inference Efficiency Frontier]] and [[Model Routing]].

## Tensions / open questions

- The speed and cost ranges are unattributed in the capture ("The claims are that..."). They do not
  match the vendor announcement in [[Diogo Almeida - Introducing System One Models and Jev]], which
  frames latency as **40x-200x** faster and reports workflow headlines of **193.6x** faster and
  **444.6x** cheaper. The vault treats these as incompatible secondary figures, not one range.
- "The probability that answer is correct" is a calibration claim the post does not test. Its own
  Choice output carries both a 0.80 top probability and a 0.60 "confidence" without explaining the
  difference, so this source supports no deployment threshold on either number.
- Token-free output explains lower generation cost, not accuracy or generalization. The post does
  not describe the architecture.
- Each example is a single illustrative output on one review. No error rates, sensitivity to
  criteria wording, or out-of-domain behavior are shown.
- This is an independent explainer, not a technical specification or evaluation. The vault keeps
  [[Typed Probabilistic Decision Models]] as its neutral term rather than adopting the vendor's
  category.

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[TypeSafe AI]]

## Raw capture

- [[2026-09-22 Matthew Canham - Jev Explained]]

## Citations

- Canonical post: <https://x.com/matthewcanham/status/2102077098756280413>
- Published September 22, 2026; captured September 23, 2026.

## Related pages

- [[Typed Probabilistic Decision Models]]
- [[TypeSafe AI]]
- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[0xMovez - Jev Engineering]]
- [[Siddhant Rai - Jev - Models Built for Decisions Rather Than Text]]
- [[Sebastian Raschka - Language Models for Text Classification - From Bag-of-Words to Jev]]
- [[Inference Efficiency Frontier]]
- [[Model Routing]]
