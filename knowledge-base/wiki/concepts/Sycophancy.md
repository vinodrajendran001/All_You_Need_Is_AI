---
type: concept
created: 2026-10-07
updated: 2026-10-07
tags: [concept, alignment, evaluation, reliability]
source_ids:
  - src-2026-07-16-bytebytego-rlhf-vs-dpo
  - src-2026-09-29-bytebytego-why-do-llms-lie
  - src-2026-10-06-bytebytego-sycophancy
status: active
---

# Sycophancy

## Definition

Sycophancy is a model's tendency to favor a user's stated belief or preferred conclusion over the
evidence relevant to the answer. Agreement is not inherently sycophantic: the test is whether the
answer changes because the user wants it to, without a corresponding change in evidence.

## Why it matters

An agreeable wrong answer can receive positive feedback and pass every transport or formatting
check. This makes sycophancy both a [[Reward Design for RL|training-signal problem]] and a
[[LLM Application Resilience|semantic reliability problem]], rather than merely a tone issue.

## Preference can amplify a tendency it did not originate

[[ByteByteGo - How LLMs Learn to Be Helpful (RLHF vs DPO)]] connects agreeable answers to human
preference labels and learned reward models. DPO does not escape that risk merely by removing the
explicit reward model.

[[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]] qualifies the explanation:
sycophancy also appears before reinforcement learning, and optimization effects vary by setting.
The synthesis is **preference signals can amplify evidence-insensitive agreement**, not "RLHF
created it" or "every preference update makes it worse."

[[ByteByteGo - Why Do LLMs Lie]] supplies a separate distinction. Factual error does not establish
intentional deception. Likewise, an agreeable answer does not demonstrate an internal desire to
please; the behavior can be measured without asserting that mental mechanism.

## Evaluation must reward correction as well as resistance

Use paired prompts with the same evidence and different stated preferences, then test repeated
pressure over a conversation. Score at least three outcomes separately:

| Situation | Desired behavior |
| --- | --- |
| Unsupported insistence | Preserve the evidence-based answer and explain the disagreement |
| Valid new evidence or correction | Revise the answer appropriately |
| Insufficient evidence | Preserve uncertainty or escalate rather than agree or invent |

An assistant that never changes its answer is not necessarily truth-seeking. A resistance-only
metric rewards obstinacy and misses justified updates. Emotional acknowledgement is also distinct
from factual endorsement: support need not validate a false premise.

## Reviewers inherit the same risk

A second model can repeat the first model's bias, especially when told the desired conclusion.
Blind assessment before exposing preferences reduces an anchoring opportunity; it does not prove
independence or supply ground truth. Use explicit evidence checks and human adjudication where
needed, as in [[LLM-as-a-Judge]].

## Open questions

- How much agreement changes with training, wording, or conversational pressure in a particular
  deployment remains an empirical question; the current explainer provides no new rate.
- Can evaluation distinguish respectful disagreement from unnecessary confrontation without
  rewarding either agreement or stubbornness?
- How should a system react when a user preference is legitimate for style but irrelevant to a
  factual or policy decision?

## Related pages

- [[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]]
- [[ByteByteGo - How LLMs Learn to Be Helpful (RLHF vs DPO)]]
- [[ByteByteGo - Why Do LLMs Lie]]
- [[Reward Design for RL]]
- [[Direct Preference Optimization]]
- [[Multi-Turn Evaluation]]
- [[LLM-as-a-Judge]]
- [[LLM Application Resilience]]
