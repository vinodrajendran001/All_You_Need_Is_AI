---
type: concept
created: 2026-06-02
updated: 2026-06-02
tags:
  - concept
  - llm-evaluation
  - conversations
  - simulation
  - traces
source_ids:
  - src-2026-06-02-bytebytego-doordash-testing-system
  - src-2026-05-29-braintrust-multi-turn-scoring
status: active
---

# Multi-Turn Evaluation

## Definition

Multi-turn evaluation is the practice of measuring an AI system over an entire conversation or interaction trace, not just over isolated single responses. It usually combines turn-level checks with conversation-level outcome metrics such as resolution, consistency, policy compliance, or progress.

## Why it matters

Many conversational failures only emerge across turns: repeated questions, contradictions, circular dialogue, missed escalations, or a polite conversation that never actually solves the user's problem. If evaluation only scores individual responses, those failures remain invisible.

## Current synthesis

- The Braintrust article makes the base point explicit: turn-level and conversation-level scores answer different questions, and both are necessary.
- Turn-scoped metrics catch local issues such as tone, helpfulness, or policy alignment. Trace-scoped metrics catch global issues such as resolution, consistency, and whether the conversation made meaningful progress.
- Structured traces are a prerequisite. If turns are not grouped into a single conversation object, multi-turn evaluation becomes impossible or unreliable.
- [[LLM-as-a-Judge]] becomes especially useful here when the judging task is narrow and explicit: binary policy checks, resolution checks, or constrained rubric facets tend to be more calibratable than fuzzy holistic scoring.
- The DoorDash flywheel extends the pattern from passive scoring into active development. Human reviewers identify a failure mode, engineers write an evaluation, a simulator generates realistic multi-turn chats from historical scenarios, the system runs the assistant against those scenarios, and the resulting pass rate becomes a release gate.
- Simulation matters because production conversations are too expensive and risky to use as the only testing environment. Synthetic but transcript-grounded multi-turn chats let teams iterate on prompts, context shaping, and backend behavior offline.
- Aggregation closes the loop. Once turn and trace scores exist at volume, clustering and topic analysis can surface recurring failure modes instead of forcing humans to read every conversation manually.

## Open questions

- Which conversation-level outcomes can be safely reduced to binary or rubric-based checks?
- How much simulation fidelity is enough before offline metrics become misleading?
- What is the right balance between always-on online scoring and cheaper sampled evaluation?

## Related pages

- [[ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs]]
- [[Braintrust - How to evaluate multi-turn conversations]]
- [[LLM-as-a-Judge]]
- [[ML Systems at Scale]]
- [[DoorDash]]
- [[Braintrust]]
- [[AI Knowledge Base Overview]]
