---
type: concept
created: 2026-09-18
updated: 2026-10-23
tags: [concept, decision-models, structured-output, inference]
source_ids:
  - src-2026-09-17-almeida-system-one-jev
  - src-2026-09-18-nandakishor-nonautoregressive-decisions
  - src-2026-09-18-0xmovez-jev-engineering
  - src-2026-09-22-canham-jev-explained
  - src-2026-09-23-kwok-contrastive-language-models
  - src-2026-09-25-rastogi-6-ways-jev-agents-reliable
  - src-2026-09-29-raschka-text-classification-jev
  - src-2026-10-05-rai-jev-decision-models
  - src-2026-10-08-talekar-decision-model-gold-rush
  - src-2026-10-08-bytebytego-netflix-genrec
  - src-2026-10-10-jaloza-microsoft-decision-1
  - src-2026-10-20-husain-decision-model-evals
  - src-2026-10-23-why-decision-models-now
status: active
---

# Typed Probabilistic Decision Models

## Definition

Typed probabilistic decision models map unstructured or structured state directly to values from a
predeclared schema plus probabilities or confidence, rather than generating an arbitrary text string.

## Why it matters

Many software decisions are bounded: route to one queue, choose an action, rank candidates, or decide
whether a condition holds. Giving up free-form generation can make interface validity intrinsic,
enable parallel output, and expose uncertainty directly. It does not make the selected value true.

## Current synthesis

[[Diogo Almeida - Introducing System One Models and Jev]] is the first source in this vault for the
pattern. TypeSafe AI calls its implementation a "System One Model," but that is a vendor category;
this page uses a functional name.

Jev reportedly samples typed decisions in parallel and supports up to 255 native choices. Larger
sets use independent scoring followed by an explicit-choice stage. The vendor claims 70-500 ms
end-to-end latency and very low input pricing. That announcement provides no public architecture,
calibration curves, or independent benchmark; the October 7 evidence update below changes the
evaluation picture without disclosing the implementation.

Two validity layers must stay separate:

1. **Schema validity:** the output is one of the allowed types or values.
2. **Semantic validity:** the selected value is correct, calibrated, and useful.

Constrained construction can guarantee the first. It cannot guarantee the second, so "cannot
hallucinate" is too broad.

## A pattern, not one product category

[[Nandakishor M - Non-Autoregressive Decision Models and Laya]] supplies an open competing
implementation with a reported 421M-parameter total architecture, including a 395M bidirectional
ModernBERT-large encoder, typed questions, calibration-oriented RL, and an explicit escalation
action. Its benchmark and priority claims remain self-reported.

[[0xMovez - Jev Engineering]] contributes the deployment pattern—dynamic option menus, parallel
questions, confidence gates, and bounded middleware—while [[Matthew Canham - Jev Explained]] reduces
the interface to state, question, options, and probabilities. Their speed and cost ranges are
secondary claims with incompatible scopes, not independent replications of the vendor benchmark.

## An outside architecture and a rollout discipline arrive before the numbers reconcile

[[Jacky Kwok et al - Contrastive Language Models]] is the first source in this thread written
neither by the vendor nor by a commentator on it. A Stanford and NVIDIA Research group proposes
Contrastive Language Models: a state encoder and an action encoder over **frozen LLM backbones**,
scored by cosine similarity, with only a **20M-parameter projection head** trained. A full
pre-training run on Nemotron DQA is reported at **about an hour on a single RTX 4090**. Jev is its
baseline, which is the first outside pressure this page has recorded on the category's numbers — but
a competing architecture benchmarking against its own baseline is not an independent replication of
Jev's claims, and every CLM figure is first-party too, published on a Notion page rather than at a
peer-reviewed venue.

What CLM isolates is *why* a typed decision system can be fast, and the answer is not "smaller
model". Candidate action embeddings are **state-independent**, so they are computed once and reused:
in the Super Mario example **4 action embeddings** are precomputed and the per-step cost falls
**from 5 forward passes to just 1**. That reframes the schema on this page as a precomputation
boundary rather than only an output contract — and it inherits the same limit, since the method
presumes a defined candidate action set and is not open-ended generation. The speed claims travel
with different conditions and must not be merged into one number: **up to 9x lower latency**
overall, **4-6x faster inference than Jev** in the benchmark section, and **13x** at around **1k
candidates**. Only the last matches the stated mechanism, because the cached side is the side that
scales with candidate count.

[[Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]] approaches the category from
the opposite end, as an operations guide. It names three primitives — `Choice`, `Noul`, and
`Score` — and fixes a semantics worth carrying explicitly: a `Noul` of **0.5** represents
uncertainty about a binary statement, not a middle category on a utility scale. A low truth
probability can instead mean a confident negative answer. The durable contribution is the rollout sequence: **week 0** pick one simple decision,
**week 1** run it in shadow mode, **week 2** label **100 to 200 cases**, **week 3** automate only
the measured paths. Thresholds are chosen *after* labelling — the **0.6** escalation cut in the
intent-routing example is illustrative, not a recommended value. That is the first procedure in this
thread for deciding when a typed model has earned automation, as opposed to asserting that it has.

Neither source reconciles the performance claims. Rastogi restates about **100 milliseconds**,
**$0.042 per million input tokens** with output tokens free, and **40x to 200x faster** and **up to
400x cheaper** than frontier LLMs. Those sit alongside, and not in place of, the **70-500 ms**,
**20-200x**, **200x/400x**, **193.6x faster**, and **444.6x cheaper** figures already recorded here;
none of them travels with a workload definition, so the set remains a pile of attributed vendor
claims rather
than a converging estimate. For predicted-event probabilities, his calibration statement — if the
model says **0.9** it should be right about **90%** of the time — is the property to evaluate and is
demonstrated nowhere in the source,
and the vendor cookbook results he cites are described only as having worked "pretty well", with no
dataset or confusion matrix. The "cannot hallucinate" framing still fails the schema-validity versus
semantic-validity split above: a schema-valid `Choice` can be the wrong one.

## October 7 evidence update: task accuracy and calibration are now separate observations

[[Sebastian Raschka - Language Models for Text Classification - From Bag-of-Words to Jev]] adds an
independent, unaffiliated run on **25,000 IMDb test reviews** with **jev-1.13.0**. Choice achieved
**96.47%** and Noul **96.20%**; the runs were nondeterministic, contamination was unknown, and the
small gap was not shown to be significant. This supplies task evidence, not a general validation
of the vendor's speed multipliers or calibration claims.

[[Siddhant Rai - Jev - Models Built for Decisions Rather Than Text]] reports broader evaluations
secondhand. Its Bonn summary gives Choice expected calibration error of **0.028 pooled across
22 datasets**, but **0.074 as the mean dataset ECE**, with individual tasks ranging
**0.003-0.279**. Low aggregate error does not validate a particular workflow's threshold. In the
reported radiology study, ECE falls **0.1235 to 0.0077 after held-out-half isotonic calibration**,
not from the raw API alone. These linked studies were not independently read in this ingest.

## Interface semantics, learning objective, and action policy must not collapse together

Raschka clarifies that Choice's `confidence` is **distribution concentration**, not the winning
option's probability. Noul returns independent statement probabilities, not one categorical
distribution across questions. Calibration tests and gates must first identify which quantity
they are using.

Both cross-entropy and Brier loss are proper scoring rules: in expectation their ideal predictions
match the conditional probabilities, even when each training example has a single hard label.
Rai's claim that hard-label supervised learning cannot calibrate, or that RL is necessary, is
therefore too strong. Finite data, model misspecification, and optimization can still produce poor
calibration. Raschka's discussion of published **RLCR** is not a disclosure of Jev's proprietary
**RLCD**.

Finally, small output entropy does not make the underlying decision easy, and schema validity is
not a correctness verifier. A sound deployment separately evaluates valid output, task accuracy,
probability calibration, and the acceptance/escalation policy. Jev's architecture and detailed
training recipe remain undisclosed; ModernBERT hypotheses, GLiNER tutorials, and Laya's open design
do not fill that gap. The vendor's "100% synthetic" data statement is an attributed claim, not an
independent audit.

## October 9 selection update: reported benchmark evidence is not interchangeability

[[Swapnil Talekar - The Decision Model Gold Rush]] reports DecideBench's **400 multiple-choice
decisions across eight task families**: Jev at **98% accuracy and $32 per million tasks**,
small encoder models including Laya in a **35-59% group range**, and image-capable Imajev-4B
at **95%**. This is a secondary account of a benchmark the author calls independent, without
the primary protocol, exact versions, or uncertainty estimates in the capture.

It adds an adverse comparison for the small-encoder category without directly refuting earlier
Laya self-reports on different tasks and metrics. Accuracy also says nothing by itself about
calibration. The source's confidence-binning recipe must use the relevant event or selected-option
probability, not silently substitute Jev Choice's concentration field.

The durable selection criteria are deployment location, modality, local quality and calibration,
latency, full cost, and replacement effort. The cited **$32 per million tasks** and **$0.042 per
million input tokens** are different units, not contradictory prices. GPU-only, per-question,
and hosted end-to-end latency claims likewise need a common boundary. A drop-in API replacement
can still require new thresholds and behavioral evaluation.

## Closed-catalog ranking shares a boundary, not necessarily the vendor category

[[ByteByteGo - How Netflix Taught an LLM to Recommend Movies]] describes GenRec's LLM-plus-ranking
head scoring finite catalog embeddings without autoregressive recommendation text. It shares the
idea of making the output set explicit, but is a domain-specific recommender, not evidence that
Netflix uses Jev or its proprietary recipe. Softmax makes a normalized ranking distribution;
it does not make scores calibrated probabilities of satisfaction. The output contract prevents
invented catalog IDs, not wrong choices among valid items.

## Microsoft adds a disclosed backbone, not a common benchmark

[[Lisa Brown Jaloza - Microsoft-Decision-1]] describes single-pass fixed-option scoring
adapted from **Qwen3.5-9B**. That separates this release from vendors whose architecture is
undisclosed, without revealing its complete scoring head or training recipe. Microsoft AI
and OpenAI backbones are planned replacements, not the announced model's base.

The developer reports leading accuracy on **36 benchmarks** and nearly **150,000 questions**,
with the suite blind to training. This is not the vault's DecideBench or IMDb evaluation.
The capture asserts calibration but supplies no numerical curve, and its editor's note
adds Jev comparisons without captured margins.

Across eight perturbation types, the reported average flip rate is **1.3%**; zero flips
in particular paraphrase/order categories do not prove general invariance. Listed
**$0.042 per million input tokens**, output tokens free, is also distinct from price per
task. [[Microsoft-Decision-1]] extends the category while retaining the existing boundaries:
valid options are not correct decisions, probabilities are not validated thresholds,
and classification is not authorization.

## The first same-task, same-protocol comparison, and the latency figures it will not settle

This page's standing complaint is that its speed and price claims are a pile of attributed vendor claims
rather than a converging estimate, because none of them travels with a workload definition.
[[Hamel Husain - How To Use Decision Models for Evals]] is the first source here to run several of these
systems **on one task under one protocol**: **Jev 1.13**, **Perplexity Decider 1.1 27B**, **Liquid d1**
and **d1-ultra**, **Cloudflare Clef Flash**, and **OpenAI Decisions on GPT-6 Luna**, each asked for a
failure probability over **98** masked apartment-leasing agent traces (**61** known failures, **37** with
no labeled failure, after excluding **2** internal QA examples). The original conversations are private,
so it is not independently reproducible.

The headline comparison is cost against F1, with its unit attached: **Perplexity** at **0.82 cents per
100 eval runs** with **F1 0.79**, and **OpenAI Decisions** at **F1 0.87** for **3.72 cents per 100 eval
runs**, about **4.5 times** the cost, at one eval run per trace. Liquid list prices are given as **$0.02
per million input tokens** (d1) and **$0.042 per million input tokens** (d1-ultra) as of October 17,
2026 — worth noting because **$0.042 per million input tokens** now appears in this vault attached to
three different products, which makes it a list-price convention rather than a distinguishing fact.

The calibration figures are the first third-party probability-quality measurements this page holds for
Jev. Brier scores on saved out-of-fold probabilities, **before → after Platt scaling**: Jev **0.187 →
0.188**, Liquid d1-ultra **0.173 → 0.172**, OpenAI **0.159 → 0.164**, with an exploratory
direct-probability refit giving OpenAI **0.154**. Brier is **not** an ECE and mixes discrimination with
calibration, so these neither replace nor contradict the **0.028 pooled / 0.074 mean-dataset** Choice ECE
figures recorded above; they are a different statistic on a different task. What they do show is that
recalibration is not automatic — Platt scaling made OpenAI's main-fit score **worse**, and the author
states that neither Platt scaling nor isotonic regression guarantees improvement on new examples.

The latency means are the interesting friction, and they must not be merged into this page's existing
numbers: **Jev 4.33 s**, **Perplexity 7.85 s**, **Liquid d1 7.38 s**, **Liquid d1-ultra 1.56 s**, **Clef
Flash 2.09 s**, **OpenAI 2.77 s**. Those are seconds, where this page records **70-500 ms** and **about
100 milliseconds** for Jev. They do not refute the vendor figures, because the boundary differs: these
are mean end-to-end response times from **separate runs**, which Husain deliberately kept out of his main
comparison and says establish nothing about throughput or tail latency, since batching, parallelization,
vendor arrangement, infrastructure distance, and concurrency dominate. The lesson is the one already on
this page — GPU-only, per-question, and hosted end-to-end claims need a common boundary — now with an
observation from the far side of that boundary, on inputs long enough to be whole agent conversations.

The task was also deliberately broad, a single "does this trace contain a failure" question chosen to
make model differences visible. The author says it may exaggerate the gaps, recommends separate judges
per failure mode, and tells readers to measure on their own data.

## A prediction is not a decision: the cutoff comes from error costs, not from the probability

[[Why Decision Models, and Why Now - A Taxonomy of Automated Decision-Making|Why Decision Models, and Why Now]] places this category inside the much older field of automated
decision-making — rules and decision trees, classifiers and structured judgments, probabilistic
decision-making, optimization, learned policies, planning with a world model, and language-model agents,
presented as overlapping approaches rather than rival products. It concedes the obvious criticism
directly: asked whether Jev is "just a classifier", the author answers **"In an important sense, yes"**,
and locates the novelty in the **interface** — asking new questions, getting typed answers back, and
using the probabilities inside software. It also records that **"older classifiers are still worth taking
seriously"**, citing a comparison in which a classifier trained on labeled examples per task had the
highest accuracy on all but **one** labeled benchmark. That citation's identity is **not recoverable**
from the capture.

The durable addition is the cost-asymmetry argument, which supplies what the threshold discussion above
is missing. Its worked example is **explicitly simplified**: a **30%** chance that activity is an attack
makes "benign" the more likely label, but with a missed attack costing **$100** and a false block costing
**$10**, allowing carries expected loss **$30** while blocking carries **$7**. The **30%**, **$100**, and
**$10** are illustrative figures, not evidence about real attack rates or costs. The structural point
stands on its own, and it is the one this page needs: the same probability supports opposite actions once
the two error directions are priced, so a confidence gate cannot be read off the probability alone. The
article credits **decision-focused learning** to Bryan Wilder, Bistra Dilkina, and Milind Tambe in
**2018** — training a predictor alongside an optimization problem so decision quality shapes what the
model learns — and notes that a model can select only from options someone supplies, with costs and
constraints still needing representation.

It also separates implementation routes this page has been treating as one category: **SemIf** reads
scores from an existing language model with no additional training; **Laya** and **GLiNER2.5-Decide** use
encoders trained for classification; **Strands Decider**, **Clef**, and **Microsoft-Decision-1** adapt
language models to score choices; and Fastino's **GLiDE** assesses the options first, using additional
reasoning only when the choice is uncertain. Modality differs too — Liquid's **d1-3B** takes text and
images, experimental **d1-omni-600M** adds audio, and **H2O Lightning** accepts images. These are
**restatements of vendor positioning inside the captured article**, not benchmarks.

**Capture-quality warning.** This source arrived as 26 malformed pipe-delimited table rows with no title,
byline, publication date, or canonical URL — only beehiiv tracking redirects. The body is recoverable and
summarized in the source page, but headings, paragraphs, or a conclusion may be missing, and no page here
should attach a byline to it.

## Open questions

- Does the cached-action formulation generalize to candidate sets that change per state, or does it
  relocate the two-stage cascade above into cache invalidation?
- Are 100 to 200 labelled cases enough to set an escalation threshold whose two error directions carry
  very different costs? **Partially answered 2026-10-23, and only as method.**
  [[Hamel Husain - How To Use Decision Models for Evals]] tunes thresholds on **98** labeled traces with
  stratified five-fold cross-validation and reports how often a stated precision/recall floor was
  infeasible on training splits, while [[Why Decision Models, and Why Now - A Taxonomy of Automated Decision-Making|Why Decision Models, and Why Now]] supplies the argument that
  the floor should be derived from error costs rather than from F1. Neither establishes a sample size at
  which a cost-weighted threshold becomes stable, and Husain does not claim his tuned cutoffs transfer
  to another dataset.
- What per-question boundary sits behind the category's millisecond latency claims, given that mean
  end-to-end response times over whole agent traces came in at seconds for every system measured?
- Brier scores, ECE figures, and accuracy numbers in this thread come from different tasks and different
  statistics. Does any system here have a calibration measurement on a workload a reader would actually
  deploy?
- If a classifier trained per task is competitive on labeled benchmarks, what does the typed interface
  buy where labeled data already exists? The comparison cited for that claim is not recoverable from its
  capture.
- How is confidence calibrated under distribution shift?
- When does parallel decision sampling outperform a small autoregressive model plus constrained decoding?
- How should large or changing action spaces be represented without a two-stage error cascade?
- What independent ground truth should replace teacher-model averages in evaluation?

## Related pages

- [[Hamel Husain - How To Use Decision Models for Evals]]
- [[Hamel Husain]]
- [[Why Decision Models, and Why Now - A Taxonomy of Automated Decision-Making|Why Decision Models, and Why Now]]
- [[Liquid AI]]
- [[Perplexity]]
- [[Multi-Turn Evaluation]]
- [[World Models]]
- [[Agent Planning]]

- [[Lisa Brown Jaloza - Microsoft-Decision-1]]
- [[Microsoft-Decision-1]]
- [[Swapnil Talekar - The Decision Model Gold Rush]]
- [[ByteByteGo - How Netflix Taught an LLM to Recommend Movies]]
- [[Semantic Recommendation Systems]]
- [[Netflix]]
- [[Sebastian Raschka - Language Models for Text Classification - From Bag-of-Words to Jev]]
- [[Siddhant Rai - Jev - Models Built for Decisions Rather Than Text]]
- [[Reward Design for RL]]
- [[Agent Delegation]]
- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[TypeSafe AI]]
- [[Tool Use and Function Calling]]
- [[LLM-as-a-Judge]]
- [[Inference Efficiency Frontier]]
- [[Jacky Kwok et al - Contrastive Language Models]]
- [[Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]]
- [[Sarthak Rastogi]]
- [[Embedding Model Selection]]
- [[Model Routing]]
- [[Agent Security and Governance]]
- [[NVIDIA]]
