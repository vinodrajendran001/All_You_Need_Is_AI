---
type: entity
entity_kind: organization
created: 2026-09-18
updated: 2026-09-30
tags: [entity, organization, decision-models]
source_ids:
  - src-2026-09-17-almeida-system-one-jev
  - src-2026-09-18-nandakishor-nonautoregressive-decisions
  - src-2026-09-18-0xmovez-jev-engineering
  - src-2026-09-22-canham-jev-explained
  - src-2026-09-23-kwok-contrastive-language-models
  - src-2026-09-25-rastogi-6-ways-jev-agents-reliable
status: active
---

# TypeSafe AI

## What it is

TypeSafe AI is an AI lab building models that return typed probabilistic decisions for software
automation. Its first public product is Jev.

## Why it matters here

[[Diogo Almeida - Introducing System One Models and Jev]] introduces a model interface that gives up
open-ended string generation for predefined values, probabilities, and confidence. The design is a
useful counterpoint to constrained decoding around general-purpose LLMs.

All available evidence is vendor-authored and early-access. Claims about latency, price, calibration,
and "no hallucinations" require independent evaluation; schema validity should not be confused with
semantic correctness.

## External explanations and dispute

[[0xMovez - Jev Engineering]] and [[Matthew Canham - Jev Explained]] broaden the use cases but repeat
incompatible performance ranges without controlled baselines. [[Nandakishor M - Non-Autoregressive Decision Models and Laya]]
claims prior work and reports an open alternative; it does not establish copying or an independently
controlled comparison with Jev.

## An academic group makes Jev a baseline while an adoption guide restates its numbers

[[Jacky Kwok et al - Contrastive Language Models]] is the first entry in this thread authored
neither by TypeSafe nor by a commentator on TypeSafe. A Stanford and NVIDIA Research group builds a
competing architecture — a state encoder and an action encoder over **frozen LLM backbones** scored
by cosine similarity, with only a **20M-parameter projection head** trained — and publishes **Jev as
its baseline**. That is the first outside pressure on this company's numbers recorded here. It is
also not an audit: a competitor benchmarking against its chosen baseline is not an independent
replication of Jev's vendor claims, every CLM figure is first-party as well, and the venue is a
Notion page rather than a peer-reviewed paper.

What the comparison establishes is structural rather than evaluative. CLM-8B is reported comparable
to Jev across computer-use, gaming, and tool-calling tasks at lower latency, and the mechanism is
**caching rather than a smaller model**: candidate action embeddings are state-independent, so the
expensive side of the comparison is computed once. The speed claims carry three separate conditions
and must not be merged — **up to 9x lower latency** overall, **4-6x faster inference than Jev** in
the benchmark section, and **13x** at roughly **1k candidates**. None of this speaks to Jev's
calibration, which remains the property with no public evidence behind it.

[[Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]] is the first source here
written as an operations guide rather than an announcement or an explanation. It restates the vendor
line: launched **September 15, 2026**, about **100 milliseconds** response time, **$0.042 per
million input tokens** with **output tokens free**, and **40x to 200x faster** and **up to 400x
cheaper** than frontier LLMs on decision-shaped work. Those figures **join rather than reconcile**
the incompatible ranges this page already carries — **70-500 ms**, **20-200x**, **200x/400x**,
**193.6x faster**, **444.6x cheaper** — because not one of them travels with a workload definition.
The company's own guardrail cookbook, cited for `Noul` screening questions on **`jev-1.12`**, is
described only as having worked **"pretty well"**, with no dataset, denominator, or confusion matrix.

The durable product detail from the same source: Jev returns typed answers with probabilities and
**generates no text**; the three primitives are `Choice`, `Noul`, and `Score`; a **`Noul` of 0.5
means the model cannot tell, not "medium"**; the weaknesses listed in TypeSafe's own jaggedness
notes for **`jev-1.13`** are arithmetic, counting, date logic, images, audio, and video, with text
only; and the named open-source alternatives are Kev, openjev, NanoJev, and Laya. Rastogi draws the
operational conclusion from those same **`jev-1.13`** jaggedness notes, which state that adversarial
content in the state can move the answer: the screen is a **filter, not a security boundary**, and
least-privilege tool access stays underneath. Note the cookbook results he cites were run on
**`jev-1.12`** — a different version from the jaggedness notes. He also states the calibration
property the company would need to demonstrate: if the model says **0.9**, it should be right about
**90%** of the time. See [[Agent Security and Governance]].

## Related pages

- [[Diogo Almeida - Introducing System One Models and Jev]]
- [[Typed Probabilistic Decision Models]]
- [[Inference Efficiency Frontier]]
- [[LLM-as-a-Judge]]
- [[Jacky Kwok et al - Contrastive Language Models]]
- [[Sarthak Rastogi - 6 Ways to Use Jev to Make AI Agents More Reliable]]
- [[Sarthak Rastogi]]
- [[Embedding Model Selection]]
- [[Model Routing]]
- [[Agent Delegation]]
- [[Agent Security and Governance]]
- [[NVIDIA]]

