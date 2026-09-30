---
type: concept
created: 2026-09-18
updated: 2026-09-30
tags: [concept, decision-models, structured-output, inference]
source_ids:
  - src-2026-09-17-almeida-system-one-jev
  - src-2026-09-18-nandakishor-nonautoregressive-decisions
  - src-2026-09-18-0xmovez-jev-engineering
  - src-2026-09-22-canham-jev-explained
  - src-2026-09-23-kwok-contrastive-language-models
  - src-2026-09-25-rastogi-6-ways-jev-agents-reliable
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
end-to-end latency and very low input pricing, but provides no public architecture, calibration
curves, or independent benchmark.

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

[[Jacky Kwok et al - Contrastive Language Models]] is the first source in this thread written neither
by the vendor nor by a commentator on it. A Stanford and NVIDIA Research group proposes Contrastive
Language Models: a state encoder and an action encoder over **frozen LLM backbones**, scored by cosine
similarity, with only a **20M-parameter projection head** trained. A full pre-training run on Nemotron
DQA is reported at **about an hour on a single RTX 4090**. Jev is its baseline, which is the first
outside pressure this page has recorded on the category's numbers — but a competing architecture
benchmarking against its own baseline is not an independent replication of Jev's claims, and every CLM
figure is first-party too, published on a Notion page rather than at a peer-reviewed venue.

What CLM isolates is *why* a typed decision system can be fast, and the answer is not "smaller model".
Candidate action embeddings are **state-independent**, so they are computed once and reused: in the
Super Mario example **4 action embeddings** are precomputed and the per-step cost falls **from 5
forward passes to just 1**. That reframes the schema on this page as a precomputation boundary rather
than only an output contract — and it inherits the same limit, since the method presumes a defined
candidate action set and is not open-ended generation. The speed claims travel with different
conditions and must not be merged into one number: **up to 9x lower latency** overall, **4-6x faster
inference than Jev** in the benchmark section, and **13x** at around **1k candidates**. Only the last
matches the stated mechanism, because the cached side is the side that scales with candidate count.

[[Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]] approaches the category from
the opposite end, as an operations guide. It names three primitives — `Choice`, `Noul`, and `Score` —
and fixes a semantics worth carrying explicitly: a `Noul` of **0.5** means the model **cannot tell**,
not "medium". Read as a midpoint, it would silently corrupt every confidence gate built on it. The
durable contribution is the rollout sequence: **week 0** pick one simple decision, **week 1** run it
in shadow mode, **week 2** label **100 to 200 cases**, **week 3** automate only the measured paths.
Thresholds are chosen *after* labelling — the **0.6** escalation cut in the intent-routing example is
illustrative, not a recommended value. That is the first procedure in this thread for deciding when a
typed model has earned automation, as opposed to asserting that it has.

Neither source reconciles the performance claims. Rastogi restates about **100 milliseconds**,
**$0.042 per million input tokens** with output tokens free, and **40x to 200x faster** and **up to
400x cheaper** than frontier LLMs. Those sit alongside, and not in place of, the **70-500 ms**,
**20-200x**, **200x/400x**, and **444.6x cheaper** figures already recorded here; none of them travels
with a workload definition, so the set remains a pile of attributed vendor claims rather than a
converging estimate. His calibration statement — if the model says **0.9** it should be right about
**90%** of the time — is the right claim to make and is demonstrated nowhere in the source, and the
vendor cookbook results he cites are described only as having worked "pretty well", with no dataset or
confusion matrix. The "cannot hallucinate" framing still fails the schema-validity versus
semantic-validity split above: a schema-valid `Choice` can be the wrong one.

## Open questions

- Does the cached-action formulation generalize to candidate sets that change per state, or does it
  relocate the two-stage cascade above into cache invalidation?
- Are 100 to 200 labelled cases enough to set an escalation threshold whose two error directions carry
  very different costs?
- How is confidence calibrated under distribution shift?
- When does parallel decision sampling outperform a small autoregressive model plus constrained decoding?
- How should large or changing action spaces be represented without a two-stage error cascade?
- What independent ground truth should replace teacher-model averages in evaluation?

## Related pages

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
