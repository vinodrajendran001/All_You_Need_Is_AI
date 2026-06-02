---
type: source-summary
created: 2026-06-02
updated: 2026-06-02
source_id: src-2026-06-02-bytebytego-doordash-testing-system
source_title: How DoorDash Built a Testing System to Evaluate LLMs
source_author: ByteByteGo
source_url: https://blog.bytebytego.com/p/how-doordash-built-a-testing-system
tags:
  - source/summary
  - llm-evaluation
  - chatbot
  - simulation
  - doordash
source_ids:
  - src-2026-06-02-bytebytego-doordash-testing-system
status: active
---

# ByteByteGo - How DoorDash Built a Testing System to Evaluate LLMs

## Summary

This ByteByteGo article distills DoorDash's simulation-and-evaluation flywheel for support chatbots. The central pattern is to stop treating prompt changes like ad hoc experiments and instead build an offline loop: generate realistic multi-turn customer conversations from transcript-derived scenarios, run the chatbot against those simulations, evaluate the full traces with binary LLM-based checks, and ship only after the pass rate clears a release bar.

The article's most durable insight is that evaluation needs its own architecture. DoorDash's system combines an LLM customer simulator, calibrated LLM-as-a-judge evaluators, realistic mock backend state, and a structured "case state" representation that reduces raw context noise before the chatbot generates a reply. The result is a faster improvement loop that can catch regressions before production while still staying grounded in real failure modes from live support traffic.

## Key claims

- LLM chatbots need a different testing paradigm from deterministic software because prompt and context changes can fix one failure mode while creating another.
- Historical transcript mining is a better source of test scenarios than hand-written examples because it captures real customer behavior and escalation patterns.
- Multi-turn conversation simulation is necessary because single-message test cases miss pushback, clarifications, and circular dialogue failures.
- LLM-as-a-judge works better as a narrow verifier than as a general generator, especially when framed as binary policy checks over a full trace.
- Calibration against human judgment is required before trusting the evaluator in production.
- Reducing raw context into a structured intermediate representation ("case state") can lower hallucination rates more effectively than simply giving the model more information.
- The full evaluation suite becomes a release gate, not just a debugging aid.

## Why it matters

This source deepens the vault's evaluation branch by moving from search relevance judging into full chatbot-development infrastructure. It shows how simulation, evaluation, and context-shaping become one system when teams need to iterate on multi-turn assistants safely and quickly.

## Tensions / open questions

- The flywheel only catches failure modes that are already represented in the evaluation suite.
- Simulation quality still depends on how faithfully transcript-derived scenarios and mock data represent production reality.
- Running large numbers of LLM-to-LLM conversations plus judge calls can be expensive for smaller teams.

## Affected pages

- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[ML Systems at Scale]]
- [[DoorDash]]
- [[AI Knowledge Base Overview]]

## Citations

- Raw capture: `knowledge-base/raw/sources/How DoorDash Built a Testing System to Evaluate LLMs.md`

## Related pages

- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[ML Systems at Scale]]
- [[DoorDash]]
- [[Braintrust - How to evaluate multi-turn conversations]]
- [[AI Knowledge Base Overview]]
