---
type: source-summary
created: 2026-08-30
updated: 2026-10-07
source_id: src-2026-07-16-bytebytego-rlhf-vs-dpo
source_title: "How LLMs Learn to Be Helpful: RLHF vs DPO"
source_author: "ByteByteGo"
source_url: "https://blog.bytebytego.com/p/how-llms-learn-to-be-helpful-rlhf"
tags:
  - source/summary
  - post-training
  - alignment
  - rlhf
source_ids:
  - src-2026-07-16-bytebytego-rlhf-vs-dpo
status: active
---

# ByteByteGo - How LLMs Learn to Be Helpful (RLHF vs DPO)

## Summary

An explainer on post-training that contrasts reference-answer imitation with explicit preference
comparisons. Standard SFT has no pairwise preference term, while RLHF and DPO use comparisons
between candidate answers. The article's motivating argument should not be read as a proof that
SFT cannot learn trade-offs encoded in curated demonstrations.

## Key claims

**RLHF and DPO differ in machinery, not in objective.** RLHF trains a separate reward model on human
comparisons, then optimizes the policy with PPO against it, holding a frozen reference model for a KL
penalty and a value model for advantage estimation — four models in play. DPO folds the reward into
the policy itself ("your language model is secretly a reward model"), so **the reward is implicit,
not absent**.

**Alignment beats scale on human preference.** InstructGPT raters preferred a 1.3B aligned model over
175B GPT-3. Zephyr-7B, trained with DPO, beat Llama 2 Chat 70B on the evaluated comparisons.

**Reward hacking is Goodhart's law with a training loop.** True quality rises, peaks, and then
declines while the proxy reward keeps climbing — the optimizer is still succeeding by its own
measure. The explainer illustrates the risk with Anthropic findings in which human raters and reward
models favored agreeable answers over correct ones. This is a reported failure mode, not a universal
ordering of truth and agreement across every rater, model, and task.

**The trouble follows the data, not the algorithm.** Because DPO learns from the same human
comparisons, it can inherit their biases. Switching from PPO to DPO does not by itself repair a
biased signal; that does not imply identical outcomes under every optimizer and dataset.

**Verifiable rewards sidestep the proxy only where a program can check the answer.** DeepSeek's
approach is instructive: RLVR drove reasoning, while reward models were retained for helpfulness and
safety, where no checker exists. The rule the source lands on is **"the method follows the signal"** —
choose the alignment machinery to match what kind of feedback is actually available.

## Why it matters

This is the vault's clearest statement of *why* preference learning exists, which the existing
[[Direct Preference Optimization]] page assumed rather than argued. It also supplies the missing
comparison axis: DPO is not "RLHF without the reward" but "RLHF with the reward re-parameterized into
the policy," which explains its simpler machinery and its continued exposure to biased preferences.

The durable warning is that efficiency and a simpler optimizer are not evidence of a better
preference signal. Data construction, objectives, and evaluation still need to distinguish useful
agreement from unsupported endorsement.

## Tensions / open questions

- If the pathology lives in the data, what does a preference dataset that does not reward
  agreeableness look like, and can humans produce it at scale?
- The InstructGPT and Zephyr results are preference-win-rate comparisons. They show alignment buys
  perceived helpfulness, not that a 1.3B model is otherwise competitive with 175B.
- The "method follows the signal" rule leaves the large middle ground — tasks that are partly
  checkable — without guidance.
- Reward hacking is described as detectable in hindsight (the divergence between true and proxy
  quality). How a team notices it *during* a run is not addressed.

## Affected pages

- [[Direct Preference Optimization]]
- [[Reward Design for RL]]
- [[LLM Training Pipeline]]
- [[ByteByteGo]]

## Citations

- Raw capture: [[2026-07-16 ByteByteGo - How LLMs Learn to Be Helpful (RLHF vs DPO)]]
- Original: <https://blog.bytebytego.com/p/how-llms-learn-to-be-helpful-rlhf> (published 2026-07-14)

## Related pages

- [[Sycophancy]]
- [[ByteByteGo - Why LLMs Agree With You Even When You Are Wrong]]
- [[Reinforcement Learning]]
- [[Group Relative Policy Optimization]]
- [[Agentic Reinforcement Learning]]
- [[LLM-as-a-Judge]]
- [[Benchmark Optimization]]
