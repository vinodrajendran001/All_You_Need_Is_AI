---
type: source-summary
created: 2026-11-27
updated: 2026-11-27
source_id: src-2026-11-24-zanichelli-swarms-raise-the-roof
source_title: Swarms do not yet raise the roof
source_author: Niccolò Zanichelli
source_url: https://www.paradigm3.org/research/swarms
tags:
  - source/summary
  - multi-agent
  - test-time-scaling
  - evaluation
source_ids:
  - src-2026-11-24-zanichelli-swarms-raise-the-roof
status: active
---

# Swarms Do Not Yet Raise the Roof

## Summary

Niccolò Zanichelli of Paradigm3 asks whether adding agents to a swarm raises the ceiling of what a
model can do or is "just a fast inefficient form of inference scaling". The study ran more than
**1,100** runs and compared more than **80** team configurations with a single agent given the same
total budget of weighted tokens. Teams of 2, 4 and 8 used Claude Opus 5.5, Claude Sonnet 5.5,
GPT-6.1 Sol and GPT-6.1 Terra, on four long-horizon tasks under three ways of organizing a team.
Teams finished about **6x** sooner but scored about **7%** lower. The one apparent swarm premium, on a
git-in-Zig porting task at 32M tokens, disappeared once the single agent was allowed to restart with
a fresh context. The author therefore argues that earlier swarm premiums are "explained by a single
agent going stale". For now a swarm buys speed at a token premium, which can still be worth paying
when time matters. The study is independent of the labs and unusually well controlled, but the
decisive restart baseline was post-hoc and run on one task.

## Key claims

### The design: matched budgets, three team shapes, and extra-tries controls

- The budget counts output tokens at **100%**, unique input at **23%** and total input at **2%**,
  following CAISI. Most comparisons used **8M** weighted tokens split evenly across a team; some were
  repeated at **32M**.
- Tasks: git-to-zig (reimplement git in Zig, from FrontierSWE v2, graded on **743** test scripts);
  AHC014 and AHC038 from ALE-Bench (AtCoder optimization problems); and Anthropic's performance
  take-home (cut clock cycles on a simulated chip).
- Protocol teams used a Park et al. (2026) prompt that assigns each agent a distinct approach and
  sharing rules. Self-organized teams shared a message board. Orchestrated teams used Codex's Ultra
  mode, with one orchestrator directing helpers from a shared budget. All models ran at high effort,
  each configuration normally three times (10 for some git-to-zig comparisons).
- A team scores its best agent's submission, so "no-talk" teams of independent agents measure how
  much of a team's result is just extra tries.
- The board for GPT teams is an undocumented Codex message board, disabled by default and absent from
  the /experimental menu. Source comments describe "Tree-owned message boards for training" and "A
  board held in memory for one training rollout", which the author reads as evidence that OpenAI
  trains with it.

### Teams trade quality for speed

- Teams scored below the single agent in **54 of 70** comparisons, by a median of **7.0%** (figures
  from the post's chart captions). Teams of 8 finished **3 to 16** times sooner in almost all
  configurations.
- Where a single agent nearly saturated the task (the take-home, and Claude on AHC014, where Opus 5.5
  ranked first against the human contestants in most runs), teams matched it.
- Claude single agents often stopped early: Sonnet spent **30-43%** of its budget on average and Opus
  about three quarters on the AHC tasks. Claude teams and single agents were therefore not compared at
  matched spend.
- The results fit Toby Ord's reading of OpenAI's GPT-5.6 swarm numbers, which put the "stepping on
  toes" exponent λ at **0.48-0.68**. Under Ord's model, N agents finish N^λ times sooner and spend
  N^(1-λ) times the tokens. With λ below 1, swarms buy speed at a token premium.

### The one premium, and the restart that erased it

- At 8M, GPT-6.1 Sol's self-organized teams roughly matched the single agent on git-to-zig. At 32M
  they beat it: Sol teams of 8 scored **93.2%** against **83.7%**, and Terra teams of 2 and 8 scored
  **29.1%** and **32.0%** against **26.6%** (teams of 4: **25.4%**). Terra teams of 16 scored
  **33.3%**, and teams of 32 scored **23.2%**, below the single agent. The best of 8 independent 4M
  agents reached only **43.7%** (Sol) and **13.1%** (Terra), so the gain was not extra tries.
- A single agent whose budget was split into eight consecutive fresh sessions, each keeping the files
  on disk, beat the teams at both budgets. At 32M it scored **97.0%** (Sol) and **41.9%** (Terra)
  against **93.2%** and **32.0%**. At 8M it scored **62.1%** and **28.0%** against **55.0%** and
  **17.8%**. Against this baseline, λ fell to **0.94** (Sol) and **0.75** (Terra) at 32M, and to
  **0.89** and **0.60** at 8M.
- Part of the advantage is accounting: at 8M, Terra's restarted agent made about **60%** more calls,
  because short sessions re-read less cached context. At 32M, Sol's restarted agent made roughly the
  same number of calls and still scored **13** points higher. The author concludes that "a long
  session never wholly resets, even with compaction", and that stale context builds up. Cai et al.
  (2026) is cited as finding something similar for autoresearch agents.
- GPT-6.2 Sol teams on the same board scored slightly below one long session (teams of 2 and 4) and
  **24%** below it (teams of 8); no restarts were run. The author concludes that whatever teamwork
  training OpenAI does "does not yet seem enough".

### Speed is still worth buying

- At these λ values, a team of 8 finishes about **3.5** times sooner for **2.3** times the tokens
  (Terra at 8M), or about **7** times sooner for **13%** more tokens (Sol at 32M). At 750 output tokens
  per second, a single agent would need about **5.5 years** to produce the roughly 130 billion output
  tokens of OpenAI's Navier–Stokes run, which the swarm finished in about **88 hours**.
- "Whether a team is worth its extra tokens is determined by the value of time relative to compute."
  Getting "~93% of the result in one day rather than a week" can be worth it. The author calls swarms
  "effectively a new scaling axis" in that limited sense, "even if the effect is fully reducible to
  inference scaling".

### Communication, diversity and newer models do not change the picture

- Talking helped on git-to-zig, where **77-94%** of improvements were separable, against **27-49%** on
  the take-home. Teams of 4 and 8 gained 16 to 53 points over their no-talk versions, but talking cost
  GPT teams 2 to 12 points on the AHC tasks in every comparison, and not Claude Opus 5.5's. The protocol
  prompt alone lowers a single Sol agent from **53.3%** to **42.2%**.
- Teams mixing GPT and Claude usually scored between the two single-model teams, and none clearly beat
  the best single agent. The author calls this a weak test of Hong and Page's diversity argument, which
  is itself disputed.
- Between model generations, the one fair pair (Opus 5 and Opus 5.5 on AHC038) lost **7-10%** and
  **5-8%** in teams. "So far, each new model has mainly brought a stronger single agent."

### Replicating OpenAI's multi-agent BrowseComp result

On a **253**-question sample (20% of **1,266**; about ±5 points), GPT-5.6 Sol scored **80.2%** alone
and **83.0%** in a 4-agent Ultra team at high effort. OpenAI reports **88.2%** and **90.8%**. OpenAI's
team gain at high effort is **2.6** points, and the replication's gains ranged from **0.4** to **2.8**.
The replication ran **1.4** points below OpenAI for the single agent at low effort and **7.5 to 8.0**
points below in the other three comparisons. The author could not determine why; candidates include an
internal harness, a harder sample, stricter leak filtering, and the reasoning-compute "juice" setting.

### How other evidence was rated

In the author's table, OpenAI's GPT-5.6 swarm bonus (**+3pp to +23pp**) had no matched-compute control
and is "Probably just disguised inference scaling". General Reasoning's Avalon-M1 is the only matched
comparison claiming about parity: its n=8 swarm beat a solo agent on **35%** of benchmarks and lost on
**43%**, and its solo baseline is the same swarm-trained model. On ProgramBench it went the other way,
**25.7%** against **29.4%**, and its claim that extended thinking "recovers about three fifths" of the
swarm gain holds only if SWE-Bench Pro is excluded; with it, four fifths. Ramez Naam's λ values
(**0.75** under 30 agents, **0.33** under 100) have no matched-compute control, because "No lone agent
is given a longer clock". Aggarwal et al. (SwarmChat), Mieczkowski et al. and Bespoke Labs' MAC Bench
also show penalties on efficiency or cost. Park et al. find a bonus against independent agents but a
penalty against a matched solo agent.

## Why it matters

This is the first matched-budget test in the vault that adds a restarted single agent as a baseline.
It answers the depth-versus-width question left open on [[Test-Time Scaling]] for one task, and it
challenges the speed-not-intelligence split and the trained-swarm claims on
[[Multi-Agent Coordination]]. It recasts trained coordination in [[Agentic Reinforcement Learning]] as
not yet enough to beat a fresh single agent, and it offers a baseline that vendor swarm comparisons
in [[Benchmark Optimization]] have not run. It tests [[Ramez Naam]]'s λ framing, rereads
[[General Reasoning]]'s Avalon-M1 parity claim and [[OpenAI]]'s swarm numbers, and turns context
staleness, a [[Context Engineering]] problem, into the main confound in swarm results.

## Tensions / open questions

- The restarted-single-agent experiment was post-hoc (footnote 9) and run only on git-to-zig, so
  "our other comparisons may flatter the teams". The recommended λ range, **0.6 to 0.9**, comes from
  that one task; pooled over all four, λ is **0.235** [−0.39, 0.86].
- Hardware differed: on three tasks a team of N had N times the CPUs, and on git-to-zig every team had
  8 CPUs and 32 GB against the single agent's 4 CPUs and 16 GB.
- A Codex compaction bug triggered compaction at about 230k to 350k tokens instead of 450k. Patched
  reruns did not score higher (Sol **89.7%** vs **93.2%**, Terra **31.5%** vs **32.0%**).
- Most configurations ran three times, which the author says is underpowered for a penalty of a couple
  of points. Even at 10 runs, the bootstrapped 95% intervals for Terra's teams of 2 and 4 include zero.
  λ assumes score grows linearly with log budget between the budgets run, using added 2M runs.
- Claude single agents underspent, some Opus single agents hit the **240**-hour working-time cap, and
  subscription waits are excluded from timings, so Claude comparisons are not at matched spend.
- Context figures are relayed, not checked here: about 1,200 agents in OpenAI's Hugging Face incident
  (about 700 attacked), about 10,000 agents for Navier–Stokes, and Carlini's 16 Claude agents building a
  100,000-line C compiler. The claim that Terminal-Bench 2.1 "contains several hundred tasks" conflicts
  with **89** tasks in [[Hugging Face - Introducing Harness Adapters]].
- The reading of Codex source comments as evidence of OpenAI's training practice is an inference from
  code, not a disclosure by OpenAI.

## Affected pages

- [[Multi-Agent Coordination]]
- [[Test-Time Scaling]]
- [[Agentic Reinforcement Learning]]
- [[Benchmark Optimization]]
- [[Ramez Naam]]
- [[General Reasoning]]
- [[OpenAI]]
- [[Context Engineering]]

## Raw capture

- [[knowledge-base/raw/sources/Swarms do not yet raise the roof]]

## Citations

- Canonical URL: <https://www.paradigm3.org/research/swarms> (the capture's `utm_source` parameter
  removed).
- By Niccolò Zanichelli, published as Paradigm3 research on November 24, 2026; captured November 26,
  2026. The post thanks Juan Vazquez for discussions and Noah Perez for editing, states a replication
  cost of $70,000 at API pricing, and links code at paradigm-3-institute/raising-the-roof.

## Related pages

- [[Multi-Agent Coordination]]
- [[Test-Time Scaling]]
- [[Agentic Reinforcement Learning]]
- [[Benchmark Optimization]]
- [[Ramez Naam]]
- [[General Reasoning]]
- [[OpenAI]]
- [[Context Engineering]]
- [[General Reasoning - How to Train a Swarm]]
- [[Ramez Naam - Can a Million AI Agents Create Superintelligence]]
- [[Cohere - Scaling Agent Teams - Reach the Frontier at 30% of the Cost]]
- [[James Tillman - Two Kinds of Test-Time Scaling]]
- [[OpenAI - The Hugging Face Incident and the Road Ahead]]
- [[Ethan Mollick - Fable 5.2 and Jagged AGI]]
- [[Yun Chi et al - The Surprising Leadership Dynamics in Agent Swarms]]
- [[Hugging Face - Introducing Harness Adapters]]
- [[Uber Engineering - How Uber Evals 1 Million Agent Skill Invocations a Month]]
