---
type: concept
created: 2026-07-03
updated: 2026-08-30
tags:
  - concept
  - reasoning
  - test-time-scaling
  - inference
  - search
source_ids:
  - src-2026-07-02-arora-llm-reasoning-advances
  - src-2026-08-12-yoko-li-loop-convergence
  - src-2026-08-25-ibm-granite-4-2-how-they-are-built
  - src-2026-07-20-raschka-reasoning-effort
status: active
---

# Test-Time Scaling

## Definition

Test-time scaling (inference-time reasoning) is spending **more compute at inference** — longer traces, more samples, explicit search, verification, or tool calls — to get better answers from a *fixed* model, without any weight update. It treats inference compute as a first-class scaling axis alongside parameters and data.

## Why it matters

It is one of the two levers for improving reasoning (the other being post-training). Under the [[LLM Reasoning|frozen-θ view]], a model already stores latent reasoning structure; test-time scaling is how you *surface* it. It is the deliberate opposite of [[Reasoning Compression]] — spend more to reason better, rather than spend less without losing accuracy — and it sits above the serving mechanics of [[LLM Inference]].

## Current synthesis

[[Akhil Arora et al - Current Advances in LLM Reasoning]] frames the whole area around one split.

### Verifier-free vs verifier-based

- **Verifier-free** methods explore the model's internal space and select by self-agreement: self-consistency / majority voting, Tree-of-Thoughts, [[Monte Carlo Tree Search|MCTS]], beam search, multi-sample decoding, Fleet of Agents. "Surface a latent path."
- **Verifier-based** methods anchor to an external signal: process reward models (PRM, judge the *process*), generative reward models (GenRM), code execution, retrieval, formal checkers, human/AI feedback. "Anchor to ground truth." The core move is that **verifiers separate generation from evaluation** — see [[LLM-as-a-Judge]] and [[Reward Design for RL]].

### Search & sieve

- Without a pruning/verification function, purely sequential generation suffers **exponentially compounding errors** from autoregressive drift. That is the mathematical reason inference pipelines separate into verifier-free (VF) and verifier-based (VB) regimes, and why adding a "sieve" (a verifier or value function) is what makes deeper search pay off.

### From prompting to structured reasoning to control

- The progression: plain prompting → CoT ("let's think step by step," emulated deduction) → **structured reasoning** that models the process as a *tree* with branching/pruning (BFS/DFS, Monte-Carlo, genetic algorithms). Structured scaffolds are powerful but require careful prompting, segmented steps, a good value function, and brittle parsers.
- **Reasoning as a scaling axis** exposes many knobs: how many thoughts to discover, how many heuristic values to sample, backtracking, and exploration-vs-exploitation. But **"just thinking more is not enough"** — more tokens can cause *overthinking*, so scaling needs **control**. The frontier "is no longer a better prompt; it's a controller that decides whether to answer, think longer, branch, retrieve, verify, or call tools." This is where [[Reasoning Compression|budget forcing]] and adaptive halting meet test-time scaling: the goal is *right-sized* compute, not maximal compute.

### Tool-mediated reasoning

- Increasingly, reasoning *is* interaction with external systems — code executors, APIs, databases, compilers, theorem provers, simulators. This connects test-time scaling to [[Tool Use and Function Calling]], [[Retrieval-Augmented Generation]] (retrieval as a test-time tool, sometimes invoked even when unnecessary), and [[Agentic Reinforcement Learning]] (agentic reasoning with verifier-based control, e.g. reflective MCTS).

### Relationship to training

- Test-time scaling and training are complementary: RL "enters the picture only when you want to use the verifier's feedback to permanently train the base model" so it reasons better *before* test-time scaling is applied. The same verifier can score candidates at inference (VB sampling) or supply the reward signal during RL — and test-time RL (TTRL) blurs the line further.

### Stop when marginal value disappears

[[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]] adds the systems-level stopping problem. Returns can plateau or turn negative while token cost continues rising with the transcript. A controller therefore needs more than a fixed sample budget: it should observe progress, detect unreachable targets, meter evaluator cost, and stop when expected improvement no longer justifies another iteration.

## A third rung between thinking and not thinking

[[IBM Granite Team - Granite 4.2 LLMs How They're Built]] ships every Granite 4.2 model with a
thinking / non-thinking switch **plus a low-effort mode that spends a short reasoning budget on easy
questions**.

The three-way split is a small but meaningful change to how test-time compute gets allocated. A
binary switch forces a routing decision with only bad options for the middle of the difficulty
distribution: questions that benefit from some deliberation but do not justify a full reasoning trace
either get overspent or get nothing. A short-budget mode makes the allocation continuous enough to
match the actual shape of incoming traffic.

It also relocates the decision. With a binary switch, a router upstream of the model picks the mode
(see [[Model Routing]]); with a budget parameter, the amount of test-time compute becomes a dial the
caller sets per request. Granite does not report how the low-effort budget is enforced or what it
costs in accuracy, so whether this beats routing between two modes is untested.

## Effort and parameters are substitutes

[[Sebastian Raschka - Controlling Reasoning Effort in LLMs]] makes the connection this page needs to
the economics of serving: training scaling and inference scaling are **two knobs whose curves
overlap**, so **a smaller model at high effort can match a larger model at low effort**.

The practical consequence is that comparing models at their default settings compares two arbitrary
points on two curves. The meaningful comparison is **cost at matched quality**, with effort level
treated as a deployment variable rather than a model property.

The user-facing effort selectors that make this possible are trained behaviours, not inference
plumbing — installed either by conditioning the RLVR run on an effort level with an effort-dependent
length penalty, or by a post-RLVR supervised stage on effort-labelled targets. Qwen3's soft switch
(`/think` flag) and hard switch (`enable_thinking=False`, which prefills an empty `<think></think>`
block) are the two ends of how firmly that setting binds. See [[Reasoning Effort Control]].

## Open questions

- **Sufficiency detection:** when has a model gathered/thought enough to answer, without a verifier? (CALM, DeepConf, DEER, early-exit methods.)
- **Reward-model reliability:** verifier-based scaling is only as good as the verifier; a flawed reward model can rank wrong answers higher.
- **Budget allocation:** how to size samples/search per problem difficulty, especially for smaller models (s1, Fleet of Agents), and how to make it self-tuning.

## Related pages

- [[IBM Granite Team - Granite 4.2 LLMs How They're Built]]
- [[Akhil Arora et al - Current Advances in LLM Reasoning]]
- [[LLM Reasoning]]
- [[Reasoning Compression]]
- [[Monte Carlo Tree Search]]
- [[LLM-as-a-Judge]]
- [[Reward Design for RL]]
- [[LLM Inference]]
- [[Retrieval-Augmented Generation]]
- [[Tool Use and Function Calling]]
- [[Agentic Reinforcement Learning]]
- [[Latent-Space Reasoning]]
- [[Reinforcement Learning]]
- [[LLM Training Pipeline]]
- [[Speculative Decoding]]
- [[AI Knowledge Base Overview]]
- [[Loop Engineering]]
- [[Yoko Li - Knowing When to Stop - The Art of Making a Loop Converge]]
- [[Reasoning Effort Control]]
- [[Sebastian Raschka - Controlling Reasoning Effort in LLMs]]
