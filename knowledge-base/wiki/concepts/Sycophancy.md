---
type: concept
created: 2026-10-07
updated: 2026-11-06
tags: [concept, alignment, evaluation, reliability]
source_ids:
  - src-2026-07-16-bytebytego-rlhf-vs-dpo
  - src-2026-09-29-bytebytego-why-do-llms-lie
  - src-2026-10-06-bytebytego-sycophancy
  - src-2026-10-27-anthropic-agents-judgment-calls
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

## The same failure runs in the other direction

[[Anthropic - How AI Agents Shape Experts' Judgment Calls]] measures the mirror image of this page's
subject: the human bending toward the model. In a randomized trial, 50 professional analysts using
Claude Code chose the option their agent had been secretly assigned to favor **86%** of the time on
four judgment calls, against about **50%** if it had no effect. When an analyst had stated a
preference first, they switched away from it **60%** of the time if the agent disagreed versus
**6%** if it agreed (a **54**-point gap, 95% interval **24 to 82**, from only **38** cases).

Two details connect the directions. First, the agent was instructed to argue its lean honestly,
change its mind if the evidence turned, and never mislead, so the influence did not depend on
dishonesty. The authors' diagnosis is one-sidedness: the agents rarely made a strong case for the
other option. Second, the post says the full paper shows agents without an assigned lean have
weaker preferences and sometimes push back against users, so the study does not show a sycophantic
default either way. A system can therefore be non-sycophantic by this page's paired-prompt test and
still pull its user's choices toward its own. Evaluating the pair — model updates on user pressure,
user updates on model framing — requires measuring the human as well as the model; see
[[Human Deferral to AI]].

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
- [[Anthropic - How AI Agents Shape Experts' Judgment Calls]]
- [[Human Deferral to AI]]
