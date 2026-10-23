---
type: source-summary
created: 2026-10-23
updated: 2026-10-23
source_id: src-2026-10-23-why-decision-models-now
source_title: Why decision models, and why now
source_author: Unattributed in capture
source_url:
tags:
  - source/summary
  - decision-models
  - taxonomy
  - capture-quality
source_ids:
  - src-2026-10-23-why-decision-models-now
status: active
---

# Why Decision Models, and Why Now

## Summary

A newsletter essay placing the current decision-model wave inside the much older field of automated
decision-making. Its durable contribution is a **taxonomy**: rules and decision trees, classifiers and
structured judgments, probabilistic decision-making, optimization, learned policies, planning with a
world model, and language-model agents — presented as overlapping approaches rather than rival products.

Its sharpest point is that **a prediction is not a decision**. The same probability leads to opposite
actions once costs are attached.

**Capture-quality warning.** This capture is badly malformed. The article arrived as 26 enormous
pipe-delimited table rows with **no frontmatter, no title, no byline, no publication date, and no
canonical URL** — only opaque beehiiv tracking redirects. The body text is recoverable and is
summarized here, but no claim should treat this capture as complete.

## Key claims

- A coding agent reading an issue, finding files, and running a test is **making decisions at each
  step**: is this file relevant, did my change break the test, should I look elsewhere. A language model
  can answer in a structured format, but each turn adds material to process.
- Responding to the "isn't Jev just a classifier?" criticism, the author concedes: **"In an important
  sense, yes."** Choosing among labels is classification and zero-shot classifiers predate Jev. The
  claimed novelty is **the interface** — asking new questions, returning typed answers, and using the
  probabilities inside software.
- **"Older classifiers are still worth taking seriously."** A cited comparison reportedly found a
  classifier trained on labeled examples per task had the highest accuracy on all but **one** labeled
  benchmark.
- Judging evidence, choosing an action, and determining what an action changed **require different
  capabilities**, even when one model can be asked all three questions.
- The cost-sensitivity worked example, explicitly simplified: a **30%** chance of attack makes "benign"
  the more likely label, but with a missed attack costing **$100** and a false block costing **$10**,
  allowing has expected loss **$30** while blocking has expected loss **$7**. The same prediction yields
  a different choice once costs change.
- **Decision-focused learning** is credited to Bryan Wilder, Bistra Dilkina, and Milind Tambe in **2018**:
  training a predictor alongside an optimization problem so decision quality shapes what the model learns.
- A model can select an action, but **someone must supply the options**, the right action may be absent,
  and costs and constraints still need representing.
- Implementation routes differ within the new wave: **SemIf** reads scores from an existing language
  model without additional training; **Laya** and **GLiNER2.5-Decide** use encoders trained for
  classification; **Strands Decider**, **Clef**, and **Microsoft-Decision-1** adapt language models to
  score choices. Input modality differs too — Liquid's **d1-3B** takes text and images, experimental
  **d1-omni-600M** adds audio, and **H2O Lightning** accepts images.
- Fastino's **GLiDE** is described as first assessing the options and then using additional reasoning
  when the choice is uncertain.
- A cited study of **8 models on 500 coding tasks** reportedly found costs varied even when the same task
  was repeated, accumulated input drove much of one model's cost, and spending more did not reliably mean
  solving the problem. The study's identity is not recoverable from this capture.
- Roles overlap: reasoning models make decisions, some decision models reason before choosing, world
  models explore possible outcomes, and causal reasoning asks what an action changed.

## Why it matters

[[Typed Probabilistic Decision Models]] has grown largely through vendor announcements and commentary on
them. This source reframes the category as **one branch of a long-standing field**, which both deflates
the novelty claim and explains what is genuinely new — a usable interface for putting recurring
judgments into software where their behavior is visible.

The cost-sensitivity example supplies the missing link between the vault's calibration discussion and
actual deployment: [[Hamel Husain - How To Use Decision Models for Evals]] shows thresholds must be
tuned on labeled data, and this source shows **why the threshold cannot be read off the probability
alone** — it depends on the asymmetry between error costs.

## Tensions / open questions

- **Attribution is unresolved.** The author, publisher, title, and date are not recoverable. The body's
  closing reference to "AI Builds AI" suggests a newsletter series, and the capture is a beehiiv email
  like other newsletter captures in this vault, but no page here should assert a byline.
- The two cited studies — the 8-model/500-task cost study and the labeled-benchmark classifier
  comparison — are **not independently checkable** from this capture; their titles and authors are buried
  in tracking redirects.
- The **30%**, **$100**, and **$10** figures are explicitly illustrative. They say nothing about real
  attack rates or costs.
- Product capability descriptions (SemIf, Laya, GLiDE, d1-omni-600M, H2O Lightning) are **restatements of
  vendor positioning**, not benchmarks.
- The malformed table structure may have dropped headings, paragraphs, or a conclusion. A re-capture from
  a canonical URL would be worth doing if the source can be identified.

## Affected pages

- [[Typed Probabilistic Decision Models]]
- [[Hamel Husain - How To Use Decision Models for Evals]]

## Raw capture

- [[Why decision models, and why now]]

## Citations

- Raw capture: [[Why decision models, and why now]]
- **No citable permalink exists.** The capture contains only beehiiv tracking redirects
  (`link.mail.beehiiv.com/v2/c/...`) and no canonical article URL, so `source_url` is deliberately empty.
- Publication date unknown; captured 2026-10-23.
- References decision-focused learning by Wilder, Dilkina, and Tambe (2018), not read during this ingest.

## Related pages

- [[Microsoft-Decision-1]]
- [[TypeSafe AI]]
- [[Liquid AI]]
- [[Swapnil Talekar - The Decision Model Gold Rush]]
- [[Nandakishor M - Non-Autoregressive Decision Models and Laya]]
- [[World Models]]
- [[Agent Planning]]
