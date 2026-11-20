---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-19-shankar-husain-evals-three-gulfs
source_title: "Evals for AI Engineers"
source_author: "Shreya Shankar and Hamel Husain (book excerpt published by ByteByteGo)"
source_url: "https://blog.bytebytego.com/p/evals-for-ai-engineers"
tags:
  - source/summary
  - evaluation
  - llm-as-a-judge
  - error-analysis
source_ids:
  - src-2026-11-19-shankar-husain-evals-three-gulfs
status: active
---

# Shreya Shankar and Hamel Husain - Evals for AI Engineers

## Summary

A ByteByteGo newsletter issue that reprints, with permission, an excerpt from the opening chapter of
the O'Reilly book *Evals for AI Engineers* by Shreya Shankar and [[Hamel Husain]]. The excerpt
introduces two organising ideas for the book. The **Three Gulfs** model names three places where LLM
application development breaks down: comprehension, specification, and generalization. The
**Analyze-Measure-Improve** lifecycle is the loop the book uses to close them. Its most useful
practical rule is a routing decision. Read traces first, then fix failures caused by unclear
instructions in the prompt. Build automated evaluators only for the failures that remain once the
prompt is clear.

This is a textbook framework illustrated with hypothetical examples (an email-processing agent, a
support chatbot, a coding assistant, a personal stylist). It reports no study, dataset, or measured
result. The single number in the excerpt, a boilerplate failure found "in 8% of cases", belongs to an
imagined example.

## Key claims

### The Three Gulfs

The model is "adapted from Shankar et al. (2025) and inspired by Norman (1988)".

- **Gulf of Comprehension (developer and data).** You need to know what real inputs look like and
  how the system behaves on them. A prompt drafted against a few clean emails will meet forwards,
  long quoted threads, multilingual signatures, and text pasted from PDFs. The gulf "applies to
  outputs too": without characterising outputs at scale, a few good examples can mislead you, and
  recurring failures (the wrong name when several appear, dropped details, confidentiality notices
  copied into summaries) go unseen.
- **Gulf of Specification (developer and agent).** Intent is only loosely captured by the prompt.
  "Extract the sender's name and summarize the key requests in this email" leaves the format, the
  sender representation, implicit requests, and length unstated, so the model guesses. That is why
  two runs of the same agent can differ in format and edge-case handling.
- **Gulf of Generalization (data and agent).** Even with good comprehension and a clear prompt, the
  model misapplies instructions. In the email example it occasionally returns a public figure named
  in the body instead of the sender. The authors call these errors "unavoidable: no matter how
  advanced the models become, there will always be cases where they produce the wrong output."

The same split is applied to other domains. A support bot that apologises when it should escalate
has a specification failure. A coding assistant that "produces correct Python but fails on less
common languages or complex multi-file changes" has a generalization failure. "The evaluation
strategy for each application depends on which gulf is the primary source of failure."

### Who can bridge the gulfs

How much rigour is needed depends on whether users can catch mistakes. Programmers using a coding
assistant can perhaps be assumed to specify precisely, read the code, and run tests. Users of an LLM
personal stylist may not know how to specify requirements, and cannot easily tell that good
casual-winter advice may not carry over to winter weddings. Where users cannot catch errors, or
errors are costly, more rigorous processes are needed.

### Analyze-Measure-Improve

- **Analyze:** read traces ("the full record of what the agent did for each request"), talk to users
  or domain experts about what correct looks like, and list failure modes without counting them yet.
  All three gulfs tend to surface in the same trace-reading sessions (Chapter 3).
- **Measure:** quantify the **generalization** failures with evaluators that score traces without
  human review, as code-based rules or an LLM judge (Chapter 5). The key question is "how often does
  each failure mode actually occur, and is the rate low enough that the system is usable?" In the
  hypothetical, a rule that flags boilerplate phrases finds the failure "in 8% of cases".
- **Improve:** specification gaps are fixed by tightening the prompt or agent logic. Generalization
  failures need stronger interventions: more examples, better retrieval, fine-tuning on labelled data,
  or a redesign, such as extracting the sender from email metadata instead of asking the model to
  parse the body. Chapter 12 orders fixes "by effort level from quick prompt edits to model-level
  changes".

The tip box presents the gulfs as shared vocabulary. A team can then argue about whether a failure is
a "specification failure" or a "generalization failure" instead of about the model "not working".

## Why it matters

The vault's [[LLM-as-a-Judge]] page is mostly about whether a judge can be trusted. This excerpt sits
one step earlier and asks which failures deserve a judge at all. Its answer is that evaluators measure
the generalization residue left after the prompt has been fixed. A specification gap should be closed
in the prompt, not counted. This matches the trace-first, error-analysis-first method already
associated with [[Hamel Husain]] in the vault, and it makes the routing rule explicit. It also links
to [[Agent Observability]], since the Analyze step assumes complete traces are available to read.

## Tensions / open questions

- The specification/generalization boundary is a judgement call. A failure that persists after "a
  clear prompt" may still be a specification gap nobody has noticed. The excerpt gives no test for
  when a prompt counts as clear enough to start measuring.
- Calling generalization errors "unavoidable" is a design stance, not a measured result. The excerpt
  does not say what residual rate is acceptable. It leaves that to the stakes analysis.
- The excerpt mentions LLM judges only by forward reference to Chapter 5, so it says nothing about
  judge validation. The vault's judge-calibration material fills that gap from other sources.
- Only the first chapter's framing is covered. The book's later chapters (3, 5 and 12) are cited but
  not reproduced, so their methods are not ingested here.

## Affected pages

- [[LLM-as-a-Judge]]
- [[Hamel Husain]]
- [[Agent Observability]]

## Raw capture

- [[knowledge-base/raw/sources/Evals for AI Engineers]]

## Citations

- Raw capture: ByteByteGo newsletter issue "Evals for AI Engineers", published 2026-11-19 (source ID
  date). The canonical URL drops the email tracking parameters.
- Authorship: the clipping's author field is ByteByteGo, but the substantive text is marked "Excerpted
  from Evals for AI Engineers by Shreya Shankar and Hamel Husain ... Published by O'Reilly Media,
  Inc. Used with permission." The summary credits the book authors and notes ByteByteGo as publisher
  of the excerpt. The excerpt line reads "Copyright © 2027", a year after the capture date. It is
  recorded as printed.
- Biographical claims come from ByteByteGo's introduction, not the excerpt. Husain is described as "an
  ML engineer at OpenAI with 20 years of experience", previously at Airbnb and GitHub, having helped
  "more than 35 companies". Shankar is described as an ML systems researcher and PhD candidate at UC
  Berkeley. Together they "trained more than 4,500 engineers and product managers" through their
  course. These are unverified, publisher-supplied bio claims.
- Two sponsor blocks (GlobalFoundries/Redpanda; Teleport Beams) were excluded.

## Related pages

- [[Hamel Husain]]
- [[Hamel Husain - How To Use Decision Models for Evals]]
- [[LLM-as-a-Judge]]
- [[Agent Observability]]
- [[Multi-Turn Evaluation]]
- [[ByteByteGo]]
