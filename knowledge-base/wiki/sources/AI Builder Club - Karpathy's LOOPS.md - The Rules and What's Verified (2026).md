---
type: source-summary
created: 2026-08-05
updated: 2026-08-26
source_id: src-2026-08-05-aibuilderclub-loops-md-karpathy
source_title: "Karpathy's LOOPS.md: The Rules and What's Verified (2026)"
source_author: AI Builder Club
source_url: https://www.aibuilderclub.com/blog/loops-md-karpathy
tags:
  - source/summary
  - ai-agents
  - ai-builder-club
source_ids:
  - src-2026-08-05-aibuilderclub-loops-md-karpathy
status: active
---

# AI Builder Club - Karpathy's LOOPS.md: The Rules and What's Verified (2026)

## Summary

This source separates the practical value of a circulating “LOOPS.md” document from its uncertain attribution to Andrej Karpathy. The document’s roughly nine rules advocate designing loops rather than prompts, separating planner/generator/evaluator roles, defining a completion contract, persisting state outside context, supporting clean restarts, grading subjective quality with rubrics, reading raw traces, removing obsolete scaffolding, and continuously finding the next bottleneck.

AI Builder Club reports that it found no primary copy on Karpathy’s website, GitHub repositories, or public gists as of July 17, 2026. It therefore labels the authorship unverified rather than false and recommends using the rules on their merits.

## Key claims

- Long-running agents depend on durable state, explicit contracts, restartability, and readable traces more than on a single clever prompt.
- Planner, generator, and evaluator should occupy separate contexts so the producer does not control its own stop condition.
- State that must survive hours or days belongs in files or other durable storage, not only in a degrading context window.
- Subjective quality must be translated into explicit rubrics if it is to participate in a closed loop.
- Harness scaffolding should be removed when stronger models or better tools make it unnecessary; optimization targets move over time.
- Provenance matters: useful advice should not inherit authority from a famous but unsupported byline.

## Why it matters

The source contributes both loop-design guidance and an example of disciplined uncertainty handling. It reinforces [[Agentic Loop]], [[Agent Memory]], [[Multi-Turn Evaluation]], and [[Coding Agent Harness]] while modeling how the vault should preserve unresolved attribution instead of collapsing it into certainty.

## Tensions / open questions

- The document may exist privately, but a private artifact cannot presently support public attribution.
- The rules are presented through secondary copies, so wording and grouping may have drifted.
- “Delete the harness” can conflict with safety, governance, or reproducibility requirements even when models improve.
- Explicit rubrics help subjective evaluation but can narrow behavior toward what is easiest to score.

## Affected pages

- [[Agentic Loop]]
- [[Agent Memory]]
- [[Multi-Turn Evaluation]]
- [[Coding Agent Harness]]
- [[Andrej Karpathy]]
- [[Context Engineering]]

## Citations

- Raw capture: [[2026-08-05 AI Builder Club - Karpathy's LOOPS.md - The Rules and What's Verified (2026)]]
- Canonical URL: https://www.aibuilderclub.com/blog/loops-md-karpathy

## Raw capture

- [[2026-08-05 AI Builder Club - Karpathy's LOOPS.md - The Rules and What's Verified (2026)]]

## Related pages

- [[Agent Planning]]
- [[LLM-as-a-Judge]]
- [[AI Agents in Production]]
- [[AI Knowledge Base Overview]]
