---
type: concept
created: 2026-07-03
updated: 2026-10-27
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
  - src-2026-10-12-bytebytego-energy-based-reasoning
  - src-2026-10-19-alphasignal-next-concept-modeling
  - src-2026-10-19-naam-million-agents-superintelligence
  - src-2026-10-15-cohere-agent-teams
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

The source's **learned effort modes** are shaped by effort-conditioned RLVR with length penalties
or a supervised stage on effort-labelled targets. They are distinct from external stopping
budgets and architectural iteration controls. Qwen3's soft `/think` flag selects a trained
behavior; its hard switch (`enable_thinking=False`) prefills an empty `<think></think>` block
to close the explicit trace phase, not eliminate internal computation. See
[[Reasoning Effort Control]].

## Extra search need not be extra text

[[ByteByteGo - How to Build Models Without Language]] adds inference-time optimization over
continuous candidate or latent states against a fixed learned energy function. Iterations,
restarts, decoding, and independent constraint checks consume a budget even when no reasoning
trace is generated. This extends the search/verification distinction beyond token sampling.

More search does not guarantee the global minimum, a valid discrete output, or termination
within budget. A checker can reject a candidate but only certifies the constraints it encodes;
the system still needs a failure/escalation path. The source's Kona Sudoku figures are a
vendor demonstration, not a measured general scaling curve, and its illustrative energy
walkthrough is not a disclosure of Kona's algorithm.

## Cheaper samples buy more candidates per budget

[[Alpha Signal - How Next-Concept Modeling Rethinks AI Text Generation]] adds a verifier-free
selection case in which the lever is sample cost rather than a better selector. **Minimum Bayes
risk (MBR) decoding** generates several candidates and keeps the one with the highest average
similarity to the others. It is a consensus rule in the same family as self-consistency.

Because Next-Concept Modeling samples quickly, it fits more candidates into the same time budget.
On summarization this is reported as "an approximately **7%** higher ROUGE-L" than the strongest
baseline. The capture does not say whether that is relative or absolute. The article notes that
the selection method itself works with other architectures; what faster generation changes is
"how many candidates an application can afford to examine."

The result therefore mixes model quality with a budget allocation. Reporting a fixed-time
comparison without also reporting a fixed-sample-count comparison would credit the generator
with gains owed to the number of samples. ROUGE-L measures overlap with reference summaries, not
factual support, so consensus selection under this metric is not verification. The figures are
secondhand research results at small model scale.

## The width axis has a measured shape, and speed and score scale differently

Everything above treats test-time compute as something spent *within* one model — longer traces, more samples,
deeper search, a verifier. [[Ramez Naam - Can a Million AI Agents Create Superintelligence]] collects what
happens on the other axis: spending the budget on **more agents working in parallel**. It is a synthesis of
other people's results rather than an experiment, and the author's own position is
**"We're all operating on far too little real world data."** Treat the curves below as a well-sourced argument
about where measurement currently stands.

The finding that matters for this page is that **adding agents moves two different curves, and they do not
move together**. Speed — how fast a solvable task finishes — scales reasonably. Score on harder problems
saturates early.

| Reported result | Agents | Effect | Cost basis |
| --- | --- | --- | --- |
| Terminal-Bench (Toby Ord) | 4 vs 1 | ~1.9x faster to the same result | ~2.1x token cost |
| BrowseComp (Toby Ord) | 4 vs 1 | ~2.6x faster to the same result | ~1.6x cost |
| Lean formal math | 10→30, then 30→100 | speed exponent **λ** fell ~0.75 → ~0.33 | agent runtime as proxy |
| SEC-Bench Pro | 1 → 4 → 16 | peak scores ~71.2 → 74.3 → 76.4 (+3.1 then +2.1 points) | best score at each budget |
| Opus 5.5 formal math, 49 weighted theorem statements, 24h per team | 10 → 100, then beyond | +27 score points, then +2 | 100-agent team could spend ~10x aggregate runtime |
| Persona/model diversity study | up to 8, then more | substantial gains to 8; average performance then barely moved | not stated |
| Molecular exploration | 1 → 128 | logarithmic diminishing returns | not stated |

Two things follow for the allocation question this page keeps returning to.

**The width axis saturates, and the saturation point is a measurable quantity.** The open question below asks
how to size samples and search per problem difficulty; the Lean and Opus 5.5 rows say the same question has a
*team-size* form, and that the answer arrives early — the 10→100 expansion bought 27 points and the next
expansion bought 2. Naam's proposed reporting protocol makes this visible by construction: report **G** (gain
per multiplication of agents), **λ** (speed scaling), and **N** (where gains saturate) separately for 1→10,
10→100, and 100→1,000, rather than quoting a single total. Gains per multiplication, not per total, is the
whole point.

**Parallel breadth and sequential depth are not interchangeable.** The essay's mechanism — *"A million
independent searches can run at once. A sequential investigation can't."* — is the same constraint this page
records under *Search & sieve*, where purely sequential generation compounds errors and a verifier is what
makes depth pay. Width has the mirror-image failure: it buys independent attempts without buying the next step
of a dependent chain, and homogeneous agents share their blind spots, so breadth does not supply diversity
automatically. That is a direct caution for self-consistency and MBR-style consensus selection above, where
**n** cheaper samples are assumed to behave like **n** independent ones.

**The evidence is weaker than the table looks.** Every row is third-party. The SEC-Bench Pro figures compare
**best reported scores at different budgets**, not equal-compute runs. Several rows use **total agent runtime
as a cost proxy**, which need not track tokens or dollars. OpenAI's ~10,000-agent, 88-hour Navier-Stokes run
is excluded from the table precisely because it **had no single-agent control**; Noam Brown is quoted saying
he would attribute **"not even 10%"** of that result to multi-agent scaling, which is an expert judgment
rather than a measurement. And benchmark score is a task-specific proxy, not a measure of capability.

## A team is a test-time budget whose return depends on where the agents go

[[Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost]] opens with the claim that
"Teams of agents unlock a new axis of inference-time scaling", and tests it in a single controlled
testbed rather than the collected third-party curves of
[[Ramez Naam - Can a Million AI Agents Create Superintelligence]]: one design choice changed at a time,
each configuration normally run three times on all 200 ProgramBench tasks, and paired 95% intervals
against a solo baseline. The exchange rate it measures is steep. A blocking all-Sol team with the
minimal prompt scored **61.8%** against **52.1%** for a solo Sol agent, and with the PIV prompt **63.1%**
against **57.7%**, yet "All four Sol teams cost between 4 and 7 times as much as the corresponding solo
agent." The key takeaways instead say the gains "come at 3–7× higher cost"; the source does not
reconcile the two ranges.

What this page gains is that the return on width depends on allocation more than on count. With
asynchronous leads, delegating only exploration and planning gained **3.4** points per **$100** of added
cost against **1.7** for the next-best stage (**3.8** against **2.4** with blocking leads). Fixed teams
of Luna planners under a Sol lead rose from **59.6%** with two to **61.8%** with sixteen, and the stated
mechanism is information: each planner ran the reference program about seven times whatever the team
size, so more planners showed the lead more of the program's behavior. That refines Naam's caution that
breadth does not supply diversity automatically: here the planners shared one model, and the breadth
came from the lead's split of the task, "each probing a different part of the program's interface".

Naam's split between speed and score also reappears. With the PIV prompt, an asynchronous lead finished
in **19.5%** less time than a blocking one at about the same reward; with the minimal prompt, it finished
in **60%** less time but did more of the work itself, and the team fell to **55.9%**, below the
PIV-prompted solo agent.

This does not settle the depth-versus-width question below: costs are reported beside results, not
matched, so no run gives one agent the team's budget. Fixed-size teams ran once, the results are
vendor-reported on one benchmark, and pairing cheap workers with a strong lead makes width a
[[Model Routing]] decision as well.

## Open questions

- **Sufficiency detection:** when has a model gathered/thought enough to answer, without a verifier? (CALM, DeepConf, DEER, early-exit methods.)
- **Reward-model reliability:** verifier-based scaling is only as good as the verifier; a flawed reward model can rank wrong answers higher.
- **Budget allocation:** how to size samples/search per problem difficulty, especially for smaller models (s1, Fleet of Agents), and how to make it self-tuning.
- **Depth versus width at a fixed budget is unmeasured.** No source on this page compares spending a token
  budget on a longer trace, more samples from one model, or more parallel agents on the same task. The
  collected agent curves report speed and score against agent count, never against an equal-compute
  single-agent alternative. [[Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost]]
  does not fill the gap: it reports each team's cost beside its score but never gives one agent the
  same budget.
- **What determines N?** The saturation points above range from 8 agents in the diversity study to beyond 100
  in formal math, and nothing in the evidence explains the spread — the formal-math results in particular do
  not distinguish a sequential bottleneck from a missing insight.
- **Does parallel scaling on benchmarks transfer to anything else?** Every curve is a benchmark result, and
  the source does not establish that the shapes hold on open-ended work.
## Related pages

- [[Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost]]
- [[Cohere]]
- [[Model Routing]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[Ramez Naam]]
- [[Agent Delegation]]
- [[Automated AI Research]]
- [[Recursive Self-Improvement]]
- [[Benchmark Optimization]]

- [[Alpha Signal - How Next-Concept Modeling Rethinks AI Text Generation]]
- [[ByteByteGo - How to Build Models Without Language]]
- [[Energy-Based Model]]
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
