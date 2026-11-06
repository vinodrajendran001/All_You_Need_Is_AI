---
type: source-summary
created: 2026-11-06
updated: 2026-11-06
source_id: src-2026-11-04-general-reasoning-train-swarm
source_title: How to Train a Swarm
source_author: General Reasoning team
source_url: https://www.gr.inc/blog/how-to-train-a-swarm
tags:
  - source/summary
  - reinforcement-learning
  - multi-agent
  - test-time-scaling
source_ids:
  - src-2026-11-04-general-reasoning-train-swarm
status: active
---

# How to Train a Swarm

## Summary

General Reasoning describes how it trains agent collectives with reinforcement learning. The
recipe, RLCR ("reinforcement learning from collective rewards"), is illustrated by its Avalon-M1
model. The core is deliberately simple: one shared policy, a policy-gradient update, one flat
collective advantage applied to every agent, and latency pressure from wall-clock time limits.
The post argues that a task reward alone gives no reason to work in parallel, so the training setup
must "make faster work pay". With that pressure and simple communication primitives, agents
should learn to divide work and coordinate. The post reports early "signs of life" from Avalon-M1
and names three unsolved problems: collectives are much smaller in training than in deployment, a
flat advantage gives weak credit assignment, and contributions to shared environments go
unrewarded. Every result is first-party, the charts were not captured as data, and the full paper
is still pending.

## Key claims

### The reasoning paradigm worked because the incentives were right

- The goal is **collective inference-time scaling**: agents scale the useful work done in parallel
  and the communication needed to achieve it. The post frames this as the reasoning paradigm
  extended with latency constraints or penalties.
- In reasoning models (o1's train- and test-compute graph; DeepSeek-R1-Zero's response length
  rising with accuracy), longer thinking needed little handcrafting *if* the RL setup was right.
  But "a naive reinforcement learning setup is not guaranteed to get this scaling pattern". With a
  standard PPO recipe using γ<1 and/or λ<1, "you would likely not have seen" it. In
  Open-Reasoner-Zero's ablation, PPO with **GAE λ = 1** keeps lengthening its responses, while
  with **λ = 0.95** response length collapses within about **50 steps**.
- Base-model priors also matter. Weaker base models with less exposure to high-quality mathematics
  explore less well, and OpenAI was "well-positioned by having a GPT-4 level base model before
  anyone else".

### Making parallel work pay

- An illustrative diagram spends about the same inference compute three ways:
  - extended reasoning takes **100** minutes;
  - independent attempts followed by selection take **28**;
  - a communicating organisation takes **46**.

  When independent attempts suffice, communication "may just add unnecessary overhead".
  Coordination pays when a task can be parallelised only imperfectly.
- A shared reward can reinforce coordination that improves the answer. When returns are equal,
  however, an objective that ignores time gives no preference for the faster approach.
- **Latency penalty.** The post gives "one possible" form, modelled on an adaptive reasoning-length
  penalty ("Just enough thinking"): `R(τ) = R_task(τ) − β · p̄(q) · T(τ) / T_max`. Here p̄(q) is the
  task's average pass rate across rollouts. DeepSeek-V4.1-Flash's agent teams used a latency
  penalty, but its functional form was not shared. The post calls the penalty principled but says
  it has "some disadvantages"; the list is missing from the capture.
- **Time limits, the Avalon-M1 choice.** A wall-clock cap, T_max, is the sole latency pressure. A
  rollout that hits the cap scores the return earned so far. The cap rises over training, giving
  collectives time to recover coordination costs, because single agents usually make more progress
  early. A deadline does not reward every reduction in time: two rollouts with equal returns
  before the deadline get the same score.
- Time limits need **"anytime-return"** environments, in which progress can be measured
  mid-rollout. Examples are tests passed in long-horizon software engineering or returns in a
  financial trading environment. A group of rollouts is stopped at the limit, and those with
  relatively higher returns are rewarded.

### Communication primitives are priors

- The core primitives are direct messages and public channels ("message boards"). Issue boards
  and knowledge archives are optional surfaces. The post urges keeping primitives simple so that
  agents discover how to work together "without excessive bias from a harness".
- It compares three current structures:
  - **Kimi K2.5 Agent Swarm** trains only the orchestrator; its sub-agents are frozen, and K2.6
    runs up to **300** sub-agents.
  - **Avalon-M1** trains every agent on one collective reward. Anyone can talk through channels,
    direct messages and an archive, and a CEO that can hire and fire leads up to **8** specialists.
  - **OpenAI's Navier–Stokes system**, "as described", split agents into islands, prompting each
    group with a different version of the problem. About **10,000** agents were in the group that
    found the solution. Its training is "not described", and the board is GR's own assumption.

  "Each is a prior about how to divide the work."

### Signs of life (Avalon-M1, first-party)

- **Useful work.** The proxy is the output and reasoning tokens of turns that act on the
  environment. A collective with **5-8 hires** starts below the average rollout and does "nearly
  twice the average amount by step 200".
- **Communication.** Communication compute per rollout-hour rises over training, together with
  normalised performance and total inference-time compute; these are z-scored charts whose values
  were not captured. The post concedes that this is "consistent with" coordination, not proof that
  the communication is useful.
- **Latency.** The post grants that a single agent given as many output tokens as the collective
  "will recover much of the performance gain, but take longer to do it". Its claim is about time:
  "At a matched-token budget, a single-agent baseline takes **4x** as long compared
  to agent collectives." On EdgeBench, an 8-hire organisation overtakes the single-agent baseline
  at about **2.4 hours** of derived latency. Twelve per-benchmark latency charts compare three
  setups: a single agent, a single agent with extended thinking given the organisation's token
  count, and an organisation of up to 8 hires. The benchmarks include SWE-Bench Pro V2 (Hard),
  Terminal-Bench 2.1, GPQA and AIME 2026. The chart values were not captured.

### Outstanding problems

- **The village problem.** Avalon-M1 trained organisations of at most **9** agents, while swarms
  are deployed with hundreds or thousands. "We are training agents in villages but deploying them
  in cities", and what generalises upward is unknown.
- **The uneasy triangle.** Long-horizon, multi-agent and multi-environment training each weaken
  the learning signal. Episodes "last hours and sometimes millions of tokens", so a flat advantage
  also credits the many tokens that did not affect the outcome.
- **Shared environments.** Rollouts are currently isolated. A contribution to a public good, such
  as a paper or a code library, might help later episodes. Under a per-episode return, the rollout
  that made it gets no credit for those later benefits.

## Why it matters

This is the vault's first source on *training* a collective rather than prompting or orchestrating
one. That axis has lacked evidence in [[Multi-Agent Coordination]] and [[Agent Delegation]]. The
source recasts [[Test-Time Scaling]] as a latency problem: a team spends compute in parallel to
finish sooner, so the training signal has to price time.

It also feeds several other pages:

- [[Reward Design for RL]]: a continuous latency penalty set against a deadline that is
  indifferent to time saved before it.
- [[RL Environment Design]]: anytime-return as a required environment property.
- [[Long-Horizon Credit Assignment]] and [[Reinforcement Learning]]: a flat collective advantage
  stretched across agents and millions of tokens, plus credit for public goods across episodes.
- [[Staged Reinforcement Learning Curriculum]]: a deadline that rises within one run as a
  within-run curriculum.
- [[LLM Reasoning]]: a hyperparameter route to length collapse, from the GAE λ background.
- [[Agentic Reinforcement Learning]]: RL applied to the collective.

[[General Reasoning]] is the publisher.

## Tensions / open questions

- **Self-reported, not peer-reviewed.** Every Avalon-M1 number comes from the lab that trained it.
  Detail is deferred to a technical report and to a full paper due "in the coming weeks once
  training finishes".
- **Charts not captured.** The z-scored curves, the useful-work curve, the EdgeBench curve and the
  twelve per-benchmark latency charts survive only as titles and axis ticks. No benchmark score
  can be read from the capture.
- **The 4x claim lacks detail.** The capture gives no benchmark set, token budget, seed count or
  variance for the matched-token claim. It partly answers the vault's token-matched question
  rather than settling it; the per-benchmark charts may differ.
- **Communication's contribution is unmeasured.** No ablation separates communication from extra
  parallel compute. The post concedes that communication volume does not establish usefulness, and
  the useful-work proxy counts tokens, not quality.
- **Training is small-scale.** No collective had more than 9 agents in training; the village
  problem is the authors' own caveat.
- **The comparisons are second-hand readings.** The penalty's "disadvantages" list is missing from
  the capture. The OpenAI comparison is GR's reading of another lab's description, and the
  message board in it is GR's assumption.
- **Capture metadata is thin.** The capture has no published date and lists only a team as author.
  Footnotes [^2] (Quanta) and [^4] (METR) are listed but not cited in the captured prose.
- **Background claims agree with other sources.** The opening context (Navier–Stokes in 88 hours;
  agents coordinating through an unauthorised message board) matches
  [[Ramez Naam - Can a Million AI Agents Create Superintelligence]] and
  [[OpenAI - The Hugging Face Incident and the Road Ahead]].

## Affected pages

- [[Agentic Reinforcement Learning]]
- [[Reinforcement Learning]]
- [[Reward Design for RL]]
- [[Long-Horizon Credit Assignment]]
- [[RL Environment Design]]
- [[Test-Time Scaling]]
- [[Staged Reinforcement Learning Curriculum]]
- [[LLM Reasoning]]
- [[General Reasoning]]
- [[Multi-Agent Coordination]]
- [[Agent Delegation]]

## Raw capture

- [[knowledge-base/raw/sources/How to Train a Swarm]]

## Citations

- Canonical URL: https://www.gr.inc/blog/how-to-train-a-swarm
- Byline: General Reasoning team; the post names no individual authors. Its suggested citation for
  RLCR and Avalon-M1 lists Iliyan Zarov, Henry Course, Anthony Hartshorn, Ran Achiron, Louis Roche,
  Akshit Sinha, Chengxi Taylor and Ross Taylor, with General Reasoning as publisher (2026).
- Published: not stated in the capture. Captured: 2026-11-04.
- Publisher: General Reasoning (gr.inc). Technical report: https://www.gr.inc/avalonm1.pdf, cited
  as October 2026.

## Related pages

- [[General Reasoning]]
- [[Multi-Agent Coordination]]
- [[Agent Delegation]]
- [[Test-Time Scaling]]
- [[Agentic Reinforcement Learning]]
- [[Reinforcement Learning]]
- [[Reward Design for RL]]
- [[Long-Horizon Credit Assignment]]
- [[RL Environment Design]]
- [[Staged Reinforcement Learning Curriculum]]
- [[LLM Reasoning]]
- [[Reasoning Compression]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[Ethan Mollick - The Dot and the Swarm]]
- [[Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[astwei et al - Teaching Qwen Why]]
