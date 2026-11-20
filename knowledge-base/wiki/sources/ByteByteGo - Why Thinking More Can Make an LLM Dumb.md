---
type: source-summary
created: 2026-11-20
updated: 2026-11-20
source_id: src-2026-11-18-bytebytego-thinking-more-dumb
source_title: "Why Thinking More Can Make an LLM Dumb"
source_author: "ByteByteGo"
source_url: "https://blog.bytebytego.com/p/why-thinking-more-can-make-an-llm"
tags:
  - source/summary
  - reasoning
  - test-time-scaling
  - explainer
source_ids:
  - src-2026-11-18-bytebytego-thinking-more-dumb
status: active
---

# Why Thinking More Can Make an LLM Dumb

## Summary

A [[ByteByteGo]] explainer on why extra reasoning can help or hurt a reasoning model. Its core
mechanism is plain autoregression: each new token is conditioned on the question *and* on everything the
model has already written, so an early written idea shapes later computation. That lets an intermediate
result (a $120 price before a 20% discount) carry a calculation forward. It also lets a later, spurious
idea displace a correct early answer.

The article walks through what reasoning models do before replying, the difference between
training-time and inference-time compute, how DeepSeek's R1-Zero learned to revisit its own steps with
reinforcement learning and GRPO, and then two forms of **overthinking**: continuing long after a correct
answer, and talking itself out of a correct answer. It ends with a methodological point: comparing
length with error rates across questions is confounded by difficulty, so the better test gives the same
model the same questions with different reasoning budgets.

It is a teaching piece. It reports no measurements of its own, lists two references (OpenAI's "Learning
to reason with LLMs" and the DeepSeek-R1 paper), and carries the publisher's disclaimer that it is based
on "publicly shared details from various sources". The capture opens with a sponsored block for
Unblocked, which is excluded here.

## Key claims

### Written steps act as a scratchpad

- Worked example: raise $100 by 20% and then cut by 20%. The tempting answer is $100; writing the
  intermediate $120 makes the correct $96 easy. "In this example, the most useful part of the chain is a
  single number."
- Reasoning models such as OpenAI's o1 "were specifically trained to generate intermediate work before
  generating a final answer". The tokens used are "often called reasoning tokens or thinking tokens", and
  many providers keep raw reasoning private and show a summary.
- Compute can be spent at training or at inference; spending more per request "is called
  inference-time scaling. Also known as test-time scaling."

### Sequential versus parallel extra compute

A debugging example (a loop that stops when position is "less than" the item count skips the last
item) shows a single attempt that can "have each step build on what the previous step found out". The
alternative is several separate solutions compared by final answer. The article says separate attempts
help most when each can make different mistakes, and a longer single attempt helps most when the model
must follow a promising idea long enough to verify it. The sentence carrying the first half is garbled
in the capture ("separate attempts can help more each attempt can make different mistakes").

### How R1-Zero learned to check its work (secondhand)

- DeepSeek started from a pretrained model and applied reinforcement learning on problems with
  automatically checkable answers (math answer keys, code tests).
- **GRPO** samples a group of attempts per question, scores each, and compares each score with the
  group's rather than with a separate critic model's estimate. R1-Zero used rules to grade correctness and
  format.
- The relayed "aha moment": partway through a square-root equation, an intermediate R1-Zero stopped,
  returned to the original equation and reconsidered its steps. The article stresses that the strategy
  choice was left to the model. Because feedback scores whole attempts, a lucky guess can also earn credit,
  but across many problems reconsidering a doubtful step pays.
- R1-Zero "sometimes switched languages or produced solutions that were hard to follow", so the released
  DeepSeek-R1 began with supervised fine-tuning.

### Overthinking, form 1: continuing after the answer is right

- From an unnamed "study of reasoning models": one model asked "2 + 3" reached five in its first
  solution, then continued until its response held **thirteen** solutions. "Nearly all of that text appeared after the calculation
  had already been done correctly."
- The proposed reason is the reward: two correctly formatted responses ending in 5 get the same score
  from a correctness checker, so "The score offers little guidance about which response made better use
  of the user’s time."
- A second check is valuable only if it "tests something the first one could have missed", for example
  comparing a total with the original order form rather than re-adding one's own list.
- Knowing when to stop "is a separate skill". The model must decide whether another check is worth it
  before it knows how the answer will be judged; stopping early is costly on hard problems, checking
  again is wasted wait time on easy ones.

### Overthinking, form 2: an extra step changes a right answer

- An illustrative scenario, not a reported case: asked for a train's timetabled departure (9:00) when
  the train "usually leaves 10 minutes late", a model finds 9:00 but continues because the delay detail
  "sounds too deliberate to ignore", and answers 9:10. Each step is sensible; the response "drifts away
  from what was intended".
- The question stays in context throughout. What changes is the set of candidate answers the model has
  now written for itself.

### How to measure it

"If longer answers contain more errors, one possibility is that the model wrote longer because those
questions were harder to begin with." A better comparison gives "the same model the same questions with
different amounts of reasoning". On hard questions extra steps may catch mistakes; on easy ones they may
repeat a conclusion or add an irrelevant detail that changes the answer.

## Why it matters

The vault's [[Test-Time Scaling]] page records, via [[Akhil Arora et al - Current Advances in LLM Reasoning]],
that "just thinking more is not enough" because of overthinking, but not what overthinking is. This
article separates two failure forms with different costs (latency versus correctness) and attaches a
plausible cause to the first: an outcome-only reward gives no credit for stopping. That matches the
vault's [[Alex Wang - What Objective Is Reasoning Solving]] frame, in which binary verifiable rewards
select whatever paths happened to succeed. Its measurement point, matched questions at varied budgets,
is the same design the vault asks of [[Reasoning Effort Control]] claims.

## Tensions / open questions

- **No measurements; the title is rhetorical.** "Dumb" is not measured, and no accuracy-versus-length
  curve is given. The article's own methodological advice is not applied to any data.
- **The "2 + 3" study is uncited.** It is not in the two-item reference list, and the model, prompt and
  frequency of the behaviour are not given. Treat it as a single secondhand anecdote.
- **The timetable case is constructed.** It illustrates a mechanism; it is not evidence that models do
  this at any particular rate.
- **The reward explanation is argued, not shown.** No reward ablation or length penalty comparison is
  reported. Other vault sources attribute length growth to reward shaping or advantage estimation (see
  [[LLM Reasoning]]); the article names only the correctness checker.
- **R1-Zero details are relayed** from the DeepSeek-R1 paper; the "aha moment" is DeepSeek's own
  interpretation of one intermediate checkpoint.
- **Capture slips.** Beyond the garbled sentence above, the R1-Zero passage states the reconsideration
  twice in a row. In the timetable case, "the calculation is correct" means the 9:10 estimate is sound;
  the error is that it answers a different question from the one asked.

## Affected pages

- [[Test-Time Scaling]]
- [[ByteByteGo]]

## Raw capture

- [[knowledge-base/raw/sources/Why Thinking More Can Make an LLM Dumb]]

## Citations

- Canonical URL: <https://blog.bytebytego.com/p/why-thinking-more-can-make-an-llm> (Substack email
  tracking parameters in the captured link removed).
- Publisher/author: ByteByteGo, as captured. Published and captured 2026-11-18; the `source_id` date is
  the publication date.
- The article's references: OpenAI, "Learning to reason with LLMs"; DeepSeek, "DeepSeek-R1:
  Incentivizing Reasoning Capability in LLMs via Reinforcement Learning".
- The sponsored section ("How much of your week is spent answering questions?", for Unblocked) is not
  part of the article and is not summarized.

## Related pages

- [[Test-Time Scaling]]
- [[ByteByteGo]]
- [[Reasoning Effort Control]]
- [[Reasoning Compression]]
- [[LLM Reasoning]]
- [[Group Relative Policy Optimization]]
- [[Reward Design for RL]]
- [[Alex Wang - What Objective Is Reasoning Solving]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- [[Chain-of-Thought Monitoring]]
