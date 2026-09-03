---
type: entity
entity_kind: person
created: 2026-09-03
updated: 2026-09-03
tags: [entity, author, evaluation, testing, newsletter]
source_ids:
  - src-2026-09-02-paolo-perrone-agentic-testing
status: active
---

# Paolo Perrone

Author of *The AI Engineer* newsletter, writing on the engineering practice of building with language models.

## Why they matter to this vault

[[Paolo Perrone - What is Agentic Testing]] is the originating source for [[Agentic Testing]] and brings the
vault two things it did not have.

The first is **pass^k**. Where pass@k asks whether a system succeeded at least once in k attempts, pass^k asks
whether it succeeded **every** time — 0.6 versus 0.4 in the worked five-check, three-run example. Since most
agent capability numbers this vault holds are pass@k-shaped, the correction has wide reach; see
[[Multi-Turn Evaluation]].

The second is a disciplined reading of what agentic testing costs. The published case studies are presented as
funnels rather than headlines — Meta's 73% engineer acceptance applies only to tests that already survived
three filters — and the failure modes reported are the quiet ones: a repair agent whose give-up condition is
to **mark a test skipped**, and self-healing locators that go green over genuinely broken features.

The framing sentence the vault reuses is *"Agentic testing does not remove the check. It moves who writes
it."*

## Caveats

The three case studies — Meta TestGen-LLM, Uber AutoCover, the Airbnb Enzyme migration — are company blog
posts and conference talks reported secondhand, with no controlled comparisons; Airbnb's 1.5-year manual
baseline is an estimate rather than a measured control.

## Related pages

- [[Paolo Perrone - What is Agentic Testing]]
- [[Agentic Testing]]
- [[Multi-Turn Evaluation]]
- [[AI-Native Software Development Lifecycle]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
