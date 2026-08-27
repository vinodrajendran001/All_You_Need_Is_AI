---
type: source-summary
created: 2026-08-24
updated: 2026-08-26
source_id: src-2026-08-20-liquid-ai-production-loops
source_title: Designing Loops for Production-Grade Work
source_author: Liquid AI
source_url: https://www.liquid.ai/blog/agent-loops
tags: [source/summary, ai-agents, loop-engineering, evaluation]
source_ids: [src-2026-08-20-liquid-ai-production-loops]
status: active
---

# Liquid AI - Designing Loops for Production-Grade Work

## Summary

Liquid AI reports an experiment in which coding agents built a production-grade BPE tokenizer trainer through repeated execution against real datasets and external reference implementations. Zero-shot attempts failed; the loop exposed encoding, memory, parallelism, tokenization, ordering, and duplication issues that were absent from the initial specification.

## Key claims

- Production constraints are discovered through execution, not fully anticipated in prompts.
- Outcome-oriented specifications should state interfaces and invariants without over-prescribing mechanisms.
- Real-scale datasets reveal failures hidden by toy tests.
- An external harness that the agent cannot modify is essential to trustworthy convergence.
- Iteration, rather than a single generation, was the mechanism that closed the gap to production behavior.

## Why it matters

This is a concrete case study for [[Loop Engineering]]: the verifier and production workload supply missing specification detail while bounded iteration repairs the implementation.

## Tensions / open questions

- It is one project and does not isolate model, harness, and verifier contributions.
- The operator still selected tasks and interpreted progress despite the no-code-review framing.
- Comparative claims between model tracks are confounded by resource decisions.

## Affected pages

- [[Liquid AI]]
- [[Loop Engineering]]

## Citations

- Raw capture: [[2026-08-20 Liquid AI - Designing Loops for Production-Grade Work]]

## Raw capture

- [[2026-08-20 Liquid AI - Designing Loops for Production-Grade Work]]

## Related pages

- [[Liquid AI]]
- [[Agentic Loop]]
- [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- [[AI Agents in Production]]
- [[Coding Agent Harness]]
- [[Multi-Turn Evaluation]]

