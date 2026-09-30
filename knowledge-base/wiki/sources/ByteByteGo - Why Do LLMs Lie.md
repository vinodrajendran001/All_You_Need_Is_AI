---
type: source-summary
created: 2026-09-30
updated: 2026-09-30
source_id: src-2026-09-29-bytebytego-why-do-llms-lie
source_title: "Why Do LLMs Lie?"
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/why-do-llms-lie
tags: [source/summary, quality, rag, evaluation, tool-use, reasoning]
source_ids: [src-2026-09-29-bytebytego-why-do-llms-lie]
status: active
---

# ByteByteGo - Why Do LLMs Lie?

## Summary

ByteByteGo separates hallucination from lying and then separates hallucination into kinds that need
different defenses. Its central mechanism is plain: next-token generation optimizes for likely
continuations, and a likely continuation is not a verified claim, so fluent confidence language is
generated text rather than evidence. The recommended architecture routes deterministic conditions to
ordinary application code, grounds the rest in retrieval and tool lookups, and adds claim-level
verification plus an explicit abstention state. Every defense is presented as risk reduction, not a
guarantee.

## Key claims

- Hallucination is information that is **factually incorrect, invented, or inconsistent with the
  material the model is supposed to use**, and none of it establishes an intention to deceive.
- Three overlapping failure modes: **factual** hallucination contradicts reality, **faithfulness**
  hallucination contradicts supplied evidence, and **fabrication** invents policies, confirmation
  numbers, or papers. The distinction matters because a model can faithfully summarize an outdated
  document and still be wrong about the current policy.
- Words like "certainly" and "definitely" are generated language, not evidence, and an unvalidated
  "95% confidence" claim means nothing without calibration.
- The incentive argument: if a correct answer earns one point while an incorrect answer and an
  expression of uncertainty score the same, guessing has positive expected upside and abstention has
  zero.
- RAG is retrieval, augmentation, then generation - and its failure modes are enumerated: a retired
  policy retrieved, the wrong product's policy selected, an exception missed, the correct passage
  misread, an unsupported promise added, and related conditions split across passages so retrieval
  returns only part of the rule.
- Tools separate general conditions from customer-specific facts: a policy document supplies the
  former, an account lookup the latter. A generated claim that an account was checked is not evidence
  the lookup occurred, and confirming eligibility does not establish that a refund was issued.
- The recommended response space includes a third state such as **"needs review"** rather than forcing
  a binary eligible/ineligible answer.
- Verification is a separate stage: decompose the answer into individual claims, check each against
  applicable evidence, and validate citations for existence, applicability, and support. Chain-of-thought
  aids inspection but is not proof, since an explanation can contain false premises or fail to describe
  the causal process.
- Lowering temperature buys consistency, not accuracy; structured output buys parseability, not
  semantic correctness. Evaluation should include eligible purchases, used accounts, missing records,
  outdated policies, and questions containing false assumptions, and should measure correctness,
  support, appropriate abstention, and unnecessary refusal.

## Why it matters

The four-way measurement - correctness, support, appropriate abstention, and unnecessary refusal - is
the part worth keeping. Most of the vault's evaluation evidence scores answers as right or wrong,
which cannot distinguish a system that has learned to say "I don't know" from one that has learned to
refuse. The factuality-versus-faithfulness split matters for the same reason: a grounded system can be
perfectly faithful to stale evidence, and only a freshness check catches that.

## Tensions and caveats

This is a secondary explainer with sponsored sections, and it supplies no hallucination rates,
controlled comparisons, or ablations, so its recommendations are conceptual rather than sized. It does
not say how to calibrate confidence, choose retrieval thresholds, or adjudicate conflicting documents.
A verifier is itself a model and can be wrong, so claim checking reduces rather than removes error.
Placing fabrication under factuality is a reasonable taxonomy choice, not a standard one. The title's
"lie" is rhetorical and the article itself withdraws the implication.

## Raw capture

- [[2026-09-29 ByteByteGo - Why Do LLMs Lie]]

## Affected pages

- [[LLM Application Resilience]]
- [[Retrieval-Augmented Generation]]
- [[Tool Use and Function Calling]]
- [[LLM-as-a-Judge]]
- [[Chain-of-Thought Monitoring]]

## Related pages

- [[Agentic Testing]]
- [[Agent Observability]]
- [[Interpretability Evaluation]]
- [[Benchmark Optimization]]
- [[Multi-Turn Evaluation]]
