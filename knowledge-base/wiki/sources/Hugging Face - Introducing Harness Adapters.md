---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-20-huggingface-harness-adapters
source_title: "Introducing harness adapters: adapt your favorite model to your harness to improve performance and cost"
source_author: Younes B, ben burtenshaw, Nathan Habib, Lysandre, Amine Dirhoussi, Adithya S K, shaun smith, Sergio Paniego, Joel Niklaus, and Lewis Tunstall
source_url: https://huggingface.co/blog/harness-adapters-at-scale
tags:
  - source/summary
  - reinforcement-learning
  - fine-tuning
  - coding-agents
  - harness-engineering
source_ids:
  - src-2026-11-20-huggingface-harness-adapters
status: active
---

# Introducing Harness Adapters

## Summary

Hugging Face trains one LoRA adapter per coding-agent harness (Pi 1.5.2, OpenCode 2.2.7 and Hermes
Agent v0.22.6) on top of a frozen Qwen3.8-27B. It uses RL inside the real harness rather than a
re-implementation of its agent loop. The headline: with the pi harness on Terminal-Bench 2.1, the base
model scores **39%** at about **2.9K** tokens per task, and the adapted model scores **55%** pass@1 at
**1.5K**. The authors attribute most of this to "the model reasoning less, calling less tools, and
performing better first time." The post also covers how the RL tasks were found, validated and
filtered for difficulty, and the training setup. It then shows that the three nearly orthogonal adapters
can be concatenated into one "super-adapter" that improves on the base model under every harness. The
evidence is first-party, single-attempt, and internally inconsistent in several counts, but it is the
vault's most detailed public recipe for post-training a model into the harness it will be deployed in.

## Key claims

### Train through the real harness

- Most RL frameworks train against their own agent interface (verl's AgentLoop, SkyRL-Gym, rLLM, slime,
  ART). Here the deployed harness runs unchanged, and a proxy between it and vLLM records the exact
  tokens for training. Agent Lightning v1.0 ("harnessed agentic RL") and SkyRL's Harbor integration are
  cited as moving the same way.
- The stack is TRL's `AsyncGRPOTrainer`, which does not wait for every rollout before an optimization
  step, plus OpenEnv, Harbor-format tasks, and Hugging Face Jobs and sandboxes.

### A task is useful only if its verifier is right and its difficulty is mid-range

- A Hub search for Harbor environments returned about **59,000** tasks, including duplicates, eval sets
  and not-for-training tasks. The authors kept two training sources, SWE-smith (injected bugs in Python
  and Go; "It adds volume") and SWE-Gym via TaskTrove (real GitHub issues). They added Tasksmith, which
  generates tasks from merged pull requests and requires the reference and a valid alternative to pass
  while the unfixed code and a known-wrong solution fail. From **30** pull requests it produced **24**
  tasks in **10** Python repositories.
- A metadata screen drops the **253** tasks in the target benchmarks and any task from their
  repositories. `openenv validate` then checks that the reference earns maximum reward, doing nothing
  scores clearly lower, no canary beats doing nothing, and replay is deterministic. **858** of **1,127**
  Hub candidates passed. Wrong-answer controls caught a Tasksmith task that accepted an incomplete
  implementation and a Terminal-Bench 2.1 verifier (regex-log) that accepted known-wrong answers. Most
  failures were infrastructure problems, and rejected tasks are kept in a separate split.
- Because GRPO learns nothing from a group where every attempt passes or every attempt fails, the base
  model attempted each task 4 times (8 for a stratified sample). Of **442** scored tasks it solved
  **151** every time and **120** never; the **171** in between form the qualified set.
- The released dataset holds **871** tasks from **35** repositories (SWE-smith **717**, SWE-Gym
  **130**, Tasksmith **24**). Four short runs on unvalidated, validated, unqualified and qualified sets
  tested the filters, but their results appear only in charts.

### Training recipe

- LoRA on all linear layers, with thinking off during rollouts. The reward is verifier correctness plus
  a **0.1** tool-efficiency bonus. Each adapter trains on two B200s (one for vLLM, one for the trainer).
  A 50-step learning-rate sweep found 1e-4 collapsing rollouts (turns from 18 to 6, entropy rising),
  1e-5 barely moving, and 5e-5 improving but unstable over longer runs, so the final runs used
  **2e-5**. The mixture is **750** harness-adapters tasks plus **300** termgrade tasks, interleaved by
  family.
- Across the three runs, **598** steps trained **78,114** samples (**167M** tokens). Training
  correctness stayed roughly flat while trajectories shortened, so more groups fit in each step's token
  budget. The safeagents tool checked **1.3M** tool calls and blocked **647**; the authors read the
  falling block rate as the model getting "safer and safer".

### In-harness results

- On the 51 hardest SWE-bench Pro tasks the specialists move pi from **39.2%** to **64.7%** (15 newly
  solved vs 2 lost, p = 0.002), hermes from **29.4%** to **43.1%**, and opencode from **35.3%** to
  **51.0%**. On all 89 Terminal-Bench 2.1 tasks, pi gains **+16.3** points and hermes **+14.1**.
  Opencode gains **+6.0** overall and **+13.6** on the 66 tasks not used to choose its checkpoint.
- On tasks both solve, the specialists make **56-72%** fewer tool calls on SWE-bench Pro and **53-70%**
  fewer on Terminal-Bench 2.1.
- Each run is one attempt per task at temperature 0.8 with default harness settings. Pi compacts
  context and the others do not, so the authors warn that results cannot be compared across harnesses,
  only within one.

### One merged adapter for every harness

- The three adapters' weight updates have pairwise cosine similarity of about **0.01-0.02**. They are
  concatenated along the rank dimension (rank **96**) and scaled by a weight w. On Terminal-Bench 2.1,
  w = 1 over-applied the updates (13.4 tool calls per task; pi fell back to base level), ⅓ diluted
  them, and **½** gave the best mean (**52.5%** against **43.3%** for the base).
- With thinking off, the super-adapter beats the base on all six harness-benchmark pairs (mean
  **39.5%** to **49.0%**; 71 tasks newly solved vs 34 lost, p < 0.001), but each specialist is ahead
  on four of six pairs. With thinking on (default xhigh effort), though never trained that way, it
  wins five pairs and ties pi on SWE-bench Pro at **74%** (mean **55.5%** to **63.5%**, p = 0.004).
- Because ½ was chosen on Terminal-Bench 2.1, the authors call those numbers "slightly optimistic";
  SWE-bench Pro played no part in the choice.

### Transfer and out-of-distribution checks

- The pi adapter run under OpenCode matches OpenCode's specialist on Terminal-Bench 2.1 (**44.8%** to
  **54.0%**, against **46.4%** to **52.4%**). Under Hermes it keeps about two-thirds of the
  specialist's gain (**46.3%** to **56.1%**, against **44.7%** to **58.8%**), with a ~45% cut in tool
  calls in both.
- On **300** AutomationBench business-automation tasks with that benchmark's own loop, the base scores
  **23.0** pass@1; pi 160 scores **27.0**, and hermes 160 drops to **17.7**. The authors call this
  "within noise, except perhaps Hermes", and say RL "neither transfers clearly" to this domain "nor
  breaks the model".
- With thinking off, the trained models emit short reasoning-like text before tool calls ("..wait?..let
  me see"), which the authors call "reasoning leakage" and do not think invalidates the results.

## Why it matters

This is a measured case of [[Harness Optimization]] moving into the weights: the harness becomes the
training environment, and the adapter is specific to it. It applies [[Parameter-Efficient Fine-Tuning]]
to deployment, with one adapter per harness and a concatenated merge instead of a full fine-tune. Its
task pipeline is concrete [[RL Environment Design]]: verifier gates, wrong-answer controls and benchmark
decontamination. Its difficulty filter is the practical form of the silent-group problem in
[[Group Relative Policy Optimization]], and the setup is [[Agentic Reinforcement Learning]] for
[[Coding Agent Harness]] use. It shows [[Hugging Face]] publishing a full recipe on its own stack, for a
[[Qwen]] model. Its single-attempt, within-harness evaluation discipline bears on
[[Benchmark Optimization]], and safeagents is a training-time control relevant to
[[Agent Security and Governance]].

## Tensions / open questions

- First-party and single-attempt (one run per task at temperature 0.8). Paired p-values are given for
  some comparisons but no repeated-run variance.
- Base pi on Terminal-Bench 2.1 appears as **39%** (introduction), **39.1%** (weight table) and
  **40.0%** (results table). On SWE-bench Pro the prose says 39.2% to 64.7% while the table says 40.0%
  to 64.0%, and pi's Terminal-Bench gain is +16.3 in prose against 40.0% to 56.5% in the table. The
  table covers only tasks every run graded (50-51 and 82-85), which may explain part of the gap.
- Task counts do not reconcile: 858 of 1,127 candidates passed validation, yet "1,127 tasks to 278"
  were included directly and "the remaining 522" were repaired, and 278 plus 522 is not 1,127
  (derived). The dataset's qualified column (144, 27, 22) sums to 193 against a stated total of
  **171** (derived).
- The transfer section's base scores (44.8%, 46.4%, 46.3%, 44.7%) differ from the main tables, so they
  come from separate runs.
- The filter-ablation and safeagents-trend results are chart-only and are not reported here. "Safer
  and safer" is the authors' reading of a falling block rate, not a separate safety evaluation.
- The closing line, that in-harness RL "leads to more efficient and therefore more accurate final
  models", asserts a causal link the post does not test; reasoning leakage and checkpoint selection on
  the eval benchmark are uncontrolled.
- Terminal-Bench 2.1 has **89** tasks here; [[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]]
  says it "contains several hundred tasks". The reports of adapters working on Qwen3.8 derivatives such
  as Swift-1.5 are community anecdotes.

## Affected pages

- [[Harness Optimization]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Agentic Reinforcement Learning]]
- [[RL Environment Design]]
- [[Group Relative Policy Optimization]]
- [[Benchmark Optimization]]
- [[Hugging Face]]
- [[Qwen]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]

## Raw capture

- [[knowledge-base/raw/sources/Introducing harness adapters adapt your favorite model to your harness to improve performance and cost]]

## Citations

- Canonical URL: <https://huggingface.co/blog/harness-adapters-at-scale> (the capture's `utm_source`
  parameter removed).
- Hugging Face blog post by Younes B, ben burtenshaw, Nathan Habib, Lysandre, Amine Dirhoussi, Adithya
  S K, shaun smith, Sergio Paniego, Joel Niklaus, and Lewis Tunstall (Hugging Face display names),
  published November 20, 2026; captured November 24, 2026.

## Related pages

- [[Harness Optimization]]
- [[Parameter-Efficient Fine-Tuning]]
- [[Agentic Reinforcement Learning]]
- [[RL Environment Design]]
- [[Group Relative Policy Optimization]]
- [[Benchmark Optimization]]
- [[Hugging Face]]
- [[Qwen]]
- [[Coding Agent Harness]]
- [[Agent Security and Governance]]
- [[adlrocha - Base Models Stopped Being the Bottleneck]]
- [[Factory Research - Droid 1.0 - Building a Frontier Harness]]
- [[@zafstojano - Recursive Synthetic Improvement]]
- [[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]]
- [[Niccolò Zanichelli - Swarms Do Not Yet Raise the Roof]]
