---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-08-alex-wang-reasoning-pathfinding
source_title: What objective is reasoning solving?
source_author: Alex Wang
source_url: https://alexwang.ai/posts/reasoning-as-pathfinding/
tags:
  - source/summary
  - reasoning
  - reinforcement-learning
  - reward-design
source_ids:
  - src-2026-11-08-alex-wang-reasoning-pathfinding
status: active
---

# What Objective Is Reasoning Solving

## Summary

Alex Wang treats reasoning as pathfinding through token space. Each sampled chain of thought is one
path from the prompt, and a verifier decides whether its final answer lands in the set of accepted
answers. Under that view, RL with a binary verifiable reward maximizes the *probability* that a
sampled path succeeds. It does not make any single path converge on the answer. Wang uses this to
explain four observations: chains of thought get longer during RL, forcing one chain to run longer
helps only for a while, chains of thought need not be faithful, and reward hacking grows as RL
scales. His answer to the title is that "Reasoning isn't actually solving any objective at all".
The post is a conceptual, teaching-style essay with no new experiments.

## Key claims

### Success is a sum over paths

- Many different paths can reach the same correct answer. Wang's example is adding the numbers one
  at a time versus pairing them from the outside in, both arriving at **55**.
- The **success probability** is the total probability of all sampled paths whose answers the
  verifier accepts. It can be raised by many low-probability paths or by one high-probability path;
  the objective does not distinguish them, though in practice one may want particular paths or
  diversity.

### Two ways to raise it

- **Best-of-n sampling** is "a guaranteed axis of compute-scaling". If any path can succeed,
  success rises monotonically with the number of samples (Brown et al. 2024). This scales the
  *number* of paths, not their length.
- **Training the sampler.** Rejection-sampling fine-tuning keeps successful samples and trains on
  them, round after round; STaR was an early reasoning version. Wang shows that RL with a binary
  verifiable reward does almost the same thing. The expected binary reward *is* the success
  probability. Its REINFORCE estimate drops failed paths, so **a REINFORCE step is a rejection-sampling
  fine-tuning step on the model's own successful paths, scaled by the current success rate**.
- That equivalence explains why chains of thought lengthen in RL. Each step pulls the model toward
  the paths that succeeded. If those tended to be longer, because of backtracking, more environment
  feedback, or "just dumb luck", the model learns to write longer paths.

### Amortization

- RL spends heavy compute searching for good paths and then trains the model to produce them
  directly, so that later queries need fewer samples. Wang calls this **amortizing** the search.
  A footnote links it to AlphaZero's tree search, expert iteration, and simulators that physicists
  and weather forecasters distill into networks.
- Because one model is trained on many prompts, it can generalize to unseen ones. The interactive
  figure, which is not captured, shows accuracy falling as a new prompt moves further from the
  training distribution.

### What the view explains

- **Faithfulness is not rewarded.** The verifier checks only the answer, so nothing requires the
  intermediate tokens to be true or to explain the answer. They often correlate with it because
  of pretraining. Wang says meaningful chains of thought need changed rewards or a changed
  objective.
- **Reward hacking has two causes.** An imperfect verifier accepts some wrong answers and rejects
  some right ones. An imperfect sampler fails to stay away from the shortcut regions that open up.
  Scaling RL with more and longer samples "fuzzes" the verifier more extensively, so it becomes more
  likely to find a misspecified region. Once a shortcut is found, training pushes the model toward
  it.
- **Longer thinking helps because training taught it.** "Thinking longer helps because training
  taught the model to use the extra tokens, not because generating more tokens is intrinsically
  better." The footnotes cite Muennighoff et al. 2025, where appending "Wait" made accuracy rise
  and then flatten, and Gema et al. 2025, which found tasks where longer reasoning lowered accuracy.

## Why it matters

[[Reward Design for RL]] already carries the claim that a 0/1 verifier reward makes the gradient
imitate successes. Wang reaches the same equivalence independently and adds the two-sided account
of reward hacking. [[Reinforcement Learning]] gains the amortization framing that links RL for LLMs
to expert iteration. [[LLM Reasoning]] gains a compact reason why traces are not faithful by
default and why forced extra thinking flattens out. [[Test-Time Scaling]] gains a clean separation
between sample-count scaling, which is guaranteed with a correct verifier, and length scaling,
which works only as far as training taught it. [[Chain-of-Thought Monitoring]] inherits the
faithfulness point.

## Tensions / open questions

- **Conceptual, not empirical.** The argument is a derivation and a set of illustrations. Its
  empirical support is borrowed from the cited papers.
- **The math did not survive capture.** The capture dropped the inline LaTeX symbols, leaving
  blanks where the prompt, answer set, path, probabilities, and gradient expressions should be. The
  prose meaning is clear, but the exact equations must be read from the original post. The two
  interactive figures are also missing.
- **The RL in the derivation is the simplest kind.** It uses a binary verifiable reward and plain
  REINFORCE. It does not address baselines, group normalization, KL terms, or PPO-style clipping,
  so it should not be read as a claim about every production RL recipe. The vault's covariance view
  in [[Reward Design for RL]] adds that, in expectation, the contrast with failures is already
  present.
- **Some explanations are hypotheses.** Whether successful paths were longer because of
  backtracking, environment feedback, or luck is offered as a possible reason, not measured.
- **Diversity is left open.** Wang says which paths to prefer, and how to keep samples diverse, may
  be a future post.

## Affected pages

- [[LLM Reasoning]]
- [[Reinforcement Learning]]
- [[Reward Design for RL]]
- [[Test-Time Scaling]]
- [[Chain-of-Thought Monitoring]]

## Raw capture

- [[knowledge-base/raw/sources/What objective is reasoning solving]]

## Citations

- Canonical URL: <https://alexwang.ai/posts/reasoning-as-pathfinding/> (the capture's URL carried a
  `utm_source=tldrai` parameter, removed here).
- By Alex Wang, published on alexwang.ai on November 8, 2026; captured November 11, 2026.

## Related pages

- [[LLM Reasoning]]
- [[Reinforcement Learning]]
- [[Reward Design for RL]]
- [[Test-Time Scaling]]
- [[Chain-of-Thought Monitoring]]
- [[James Tillman - Two Kinds of Test-Time Scaling]]
