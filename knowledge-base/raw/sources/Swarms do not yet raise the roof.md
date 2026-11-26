---
title: "Swarms do not yet raise the roof"
source: "https://www.paradigm3.org/research/swarms?utm_source=tldrai"
author:
  - "[[Niccolò Zanichelli]]"
published: 2026-11-24
created: 2026-11-26
description: "TL;DR; Large groups of LLMs coordinating with each other – “swarms” – are suddenly a big deal. But does adding agents to a swarm increase the ceiling of their performance? Or is swarm scaling just a fast inefficient form of inference scaling; We compared teams of 2, 4, and 8…"
tags:
  - "clippings"
---
**TL;DR**

- Large groups of LLMs coordinating with each other – “swarms” – are suddenly a big deal. But does adding agents to a swarm increase the ceiling of their performance? Or **is swarm scaling just a fast inefficient form of inference scaling?**
- We compared teams of 2, 4, and 8 agents against a single agent given the same total token budget, on four long-horizon tasks and over three ways of organizing a team. We ran over 1,100 runs and compared more than 80 team configurations against a single agent.
- One of our settings uses OpenAI’s Codex message board. This feature is actually undocumented and hidden from users; comments imply OpenAI trains its swarms with it.
- Two ways for AIs to go superhuman are by being faster than us, or strictly better than us. Swarms are obviously an enormous speed improvement (6x in our experiments), but actually suffer a quality *penalty* (about 7%) relative to a single agent.
- Worse, we think this penalty *grows* with swarm size. (On one task we also ran teams of 16 and 32, and they did no better than teams of 8.)
- At 8M tokens, we found no swarm performance gain on unsaturated tasks. Since swarms pay a coordination cost up front, we reran a near-miss task at 32M: a self-organized team of 8 then beat the single agent.
- But when we allowed the single agent to restart with a fresh context, it again beat the teams. **We thus think that previous results finding a swarm premium are explained by a single agent going stale.**
- Against a single agent that can restart its session, we estimate the “stepping on each other’s toes” parameter to be 0.6 to 0.9 on one unsaturated task. (This parameter is poorly determined on our other three tasks.)
- In the real world, it could be totally worth spending the tokens and taking the performance hit to get ~93% of the result in one day rather than a week. But this is different from swarms being a dominant strategy or a scaling axis.
- We were fairly budget-constrained; teamwork training is still in its early days; obviously we don’t rule out future swarms scaling in quality (or current internal swarms doing so).

## Motivation

Large groups of LLMs coordinating with each other – “swarms” – are suddenly a big deal.

In the last two years, the idea of using swarms moved from the margins of AI to the center. An early iteration was [o1’s Pro mode](https://openai.com/index/introducing-chatgpt-pro/) in December 2024[^1], which [reportedly](https://newsletter.semianalysis.com/p/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures) had multiple instances reason before answering, a design OpenAI [later confirmed](https://openai.com/index/introducing-gpt-5/) was used for GPT-5 Pro.[^2] Then in February 2026, Nicholas Carlini at Anthropic [had 16 Claude agents work on one codebase](https://www.anthropic.com/engineering/building-c-compiler) for two weeks, producing a 100,000-line C compiler with no dependencies.[^3] By mid-2026, frontier labs were reporting results for teams of agents alongside those of single agents, as Anthropic did for [Claude Opus 4.6](https://www.anthropic.com/engineering/eval-awareness-browsecomp) and OpenAI did in its [GPT-5.6 announcement](https://openai.com/index/gpt-5-6/).

*Then* a swarm of hundreds of OpenAI agents attacked Hugging Face. [In July](https://nightingalecollective.org/incidents/#incident-38), roughly 1,200 agents that were meant to be isolated from one another found a way to communicate, and about 700 went on to attack Hugging Face [and OpenAI](https://nightingalecollective.org/incidents/#incident-39) – the most serious incident of misbehavior by AI agents yet documented. Independent investigators from METR and Redwood Research [judged](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) that, by coordinating, the agents “managed to achieve milestones they could not have achieved working on their own.”

*Then*, in September, OpenAI reported what, before the recently [announced](https://alpo.ge/remark.pdf) proof of the Riemann Hypothesis, was the most important mathematical result produced by AI: a [resolution of the Navier–Stokes problem](https://openai.com/index/navier-stokes-solution/), produced by “a system of coordinating agents powered by our internal model \[…\] on the order of 10,000 concurrent agents.” In seven months, the largest reported swarms had grown from 16 agents to over 10,000.

The speed of this jump makes it urgent to understand how (or whether) swarms scale. Even the labs running swarms are at an early stage with this: OpenAI’s CEO, Sam Altman, [notes](https://blog.cosmos-institute.org/p/recursive-self-improvement) that when the company produced the Navier–Stokes proof, they “understood absolutely nothing about the scaling laws of teams of agents,” and that “now, we understand it a little bit.”

Specifically, the central question is whether adding agents to a swarm is a [new axis](https://www.understandingai.org/p/why-agent-swarms-could-be-the-next) that you can scale to buy improved performance (as training for using more intermediate tokens [turned out to be](https://openai.com/index/learning-to-reason-with-llms/) in September 2024) – or whether it’s just a faster but *less* efficient form of “[duration scaling](https://www.tobyord.com/writing/swarm-scaling)” (in which one adds more thinking time to a single agent’s chain of thought). In other words, **is swarm scaling just inference scaling in disguise, or is it a new way to turn compute into capabilities (and a portent of a further acceleration in AI progress)?**

As far as we know, no one has yet systematically compared teams of agents with a single agent at matched token budgets on long-horizon tasks, with the exception of the AI company [General Reasoning](https://www.gr.inc/releases/avalon-m1), which found roughly a null result for a swarm-quality bonus:

> *At matched output-token budgets, a single agent recovers much of the organisation’s performance gain, so organisations appear to be mainly beneficial in terms of their reduced latency.*

## Method

We compared teams of agents with a single agent given the same total budget of weighted tokens.[^4] Most comparisons used 8M weighted tokens in total, split evenly between the agents of a team. A team is scored on the best submission made by any of its agents. Since this gives a team several attempts at the task, we also scored no-talk teams, made up of agents that worked independently with a team member’s share of the budget, to measure how much of a team’s result comes from extra tries alone.

A budget of 8M weighted tokens is far smaller than the [roughly 130 billion output tokens](https://openai.com/index/navier-stokes-solution/) OpenAI used for Navier–Stokes. We cannot approach that scale, but to check whether our results depend on the limited budget, we repeated some comparisons at 32M: for GPT-6.1 Terra on git-to-zig and the two AtCoder Heuristic Contest (AHC) tasks, for GPT-6.1 Sol on git-to-zig, and for Claude Opus 5.5 on git-to-zig (two runs each).

We used four long-horizon tasks, on which a single agent works for hours to days, each with a continuous score that agents can check as they go.

| Name | Task | Score |
| --- | --- | --- |
| git-to-zig ([FrontierSWE v2](https://github.com/Proximal-Labs/frontier-swe-v2)) | Reimplement git in the Zig programming language | Percentage of git’s tests passed |
| [AHC014](https://atcoder.jp/contests/ahc014) and [AHC038](https://atcoder.jp/contests/ahc038) ([ALE-Bench](https://github.com/SakanaAI/ALE-Bench)) | Write programs for two hard optimization problems from AtCoder Heuristic Contests | AtCoder performance |
| Performance take-home ([Anthropic](https://github.com/anthropics/original_performance_takehome)) | Make a program run as fast as possible on a simulated chip | Clock cycles (lower is better) |

We compared three ways of organizing teams of 2, 4, and 8 agents.

1. **Protocol teams**: In the first setup, each agent received a prompt from [Park et al. (2026)](https://arxiv.org/abs/2609.21032) that designated it a distinct approach, along with rules for how, and when, to share its findings.
2. **Self-organized teams**: For the second, agents were not assigned roles but were able to coordinate via a shared, Slack-like message board, deciding among themselves how to divide labor.
	1. We found a suitable board in OpenAI’s [Codex source code](https://github.com/openai/codex/pull/46985). This feature is actually undocumented and hidden from users, and comments (for example, [here](https://github.com/openai/codex/blob/ddd1812a51f4aded35c3ec5446672474d5cb546b/codex-rs/features/src/feature_configs.rs#L371) and [here](https://github.com/openai/codex/blob/ddd1812a51f4aded35c3ec5446672474d5cb546b/codex-rs/agent-message-board-host/src/lib.rs#L43)) suggest OpenAI use it when training their models. The agents in the [Hugging Face incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/#july-8th-9th-phaseone10841-establishes-the-primary-message-board-and-agents-collaborate-to-reverse-engineer-their-flags) also coordinated through a message board, which one of them set up, possibly because they knew about such boards from training.
3. **Orchestrated teams**: In the third, one orchestrator agent starts helper agents, directs their work, and draws on a budget shared by the whole team. This is Codex’s own multi-agent mode, “[Ultra](https://openai.com/index/gpt-5-6/#:~:text=ultra%20goes%20further%20by%20coordinating%20four%20agents,reaching%20stronger%20results%20in%20less%20time).” In the first two setups, each agent explores on its own; in orchestrated teams, one agent directs the exploration.

We ran Claude Opus 5.5 and Claude Sonnet 5.5 in protocol teams, GPT-6.1 Sol in all three setups, and GPT-6.1 Terra in self-organized teams, all at “high” reasoning effort. Claude Code, used for the Claude models, has no message board, but its agents can talk through [cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging). On git-to-zig, we also ran self-organized Claude teams that talk only this way, with the same prompt adapted to direct messages. We ran each config three times; a few git-to-zig comparisons were run 10 times.

Full details in the methodology appendix.

<video src="https://www.paradigm3.org/img/swarms-method.mp4" controls="" aria-label="How the budget was split: a single agent has 8M weighted tokens in one session; protocol and self-organized teams of 4 give each agent 2M, sharing files or a message channel; an orchestrated team shares one 8M budget between an orchestrator and up to 3 helpers"></video>

## Main results

### Performance against tokens

<video src="https://www.paradigm3.org/img/swarms-tokens.mp4" controls="" aria-label="At the same budget, teams scored below a single agent in 54 of 70 comparisons: GPT-6.1 Sol&#39;s score curves against weighted tokens on the four tasks, and every team&#39;s score against its single agent, a median of 7.0% lower"></video>

At the same token budget, teams generally performed worse than a single agent, even though each team was scored on the best of its agents’ submissions. On the performance take-home, and for Claude models on AHC014, the single agent came close to saturating the task, leaving little room for improvement; on AHC014, Claude Opus 5.5 ranked first against the original human contestants in most runs. In these cases, teams matched the single agent, although a comparison this close to the ceiling says little about how efficiently teams use their budget.

We selected tasks through shorter pilots, typically at 2M weighted tokens, so some proved close to saturated at the 8M budget for the main runs. Claude Sonnet 5.5 teams also scored above the single agent on AHC038, but Sonnet’s single agents stopped early, spending on average 31% of their budget – so the two could not be fairly compared.

More generally, Claude’s single agents often stopped early on the AHC tasks and the performance take-home: Sonnet’s single agents spent 30–43% of their budget on average, and Opus’s single agents about three quarters of theirs on the AHC tasks. As a result, Claude’s teams and single agents were not compared at matched spend. One case where a team appeared to outperform a single agent was when self-organized teams of OpenAI models were tested on git-to-zig tasks, which we discuss below.

Apart from this, our results are consistent with [Toby Ord’s analysis](https://www.tobyord.com/writing/swarm-scaling) of the multi-agent results in OpenAI’s [GPT-5.6 announcement](https://openai.com/index/gpt-5-6/). Ord draws on an idea from economics: when many people work on a task together, they finish sooner, but usually at the cost of more total hours of work, since a task can only be divided so far and workers get in each other’s way. Economists measure this with a “stepping on toes” [parameter λ](https://web.stanford.edu/~chadj/JonesJPE95.pdf): N people working together get as much done as one person working N^λ times as long. A perfectly divisible task has λ = 1, while with λ = 0.5, for example, 100 people get as much done as one person working 10 times as long. From OpenAI’s results, Ord estimates λ between 0.48 and 0.68 on three benchmarks, so a team of agents gets considerably less out of its combined budget than a single agent would.

Our teams appear to pay a coordination cost of this kind, which grows with team size: the larger the team, the more tokens it spends before it starts making progress. Measured against tokens, adding agents does not yet look like a new axis along which performance scales. Tokens, however, are only one side of the trade-off described above, and in practice the other side, time, matters as well.

### Performance against time

<video src="https://www.paradigm3.org/img/swarms-time.mp4" controls="" aria-label="At the same budget, teams of 8 typically finished 6.1 times sooner than a single agent and scored 7.0% lower: score curves against active hours on the four tasks, and every comparison by how much sooner the team finished"></video>

A single agent can only produce tokens so fast, and teams spent the same budget in much less time: in most configurations, teams of 8 finished several times sooner than a single agent.[^5] This matters most at large budgets. Even at 750 output tokens per second, the top speed of OpenAI’s [Ultrafast preview](https://openai.com/index/previewing-ultrafast/), a single agent would need about 5.5 years to produce the roughly 130 billion output tokens of OpenAI’s [Navier–Stokes run](https://openai.com/index/navier-stokes-solution/), in which the swarm produced its proof about 88 hours after launch.

One might expect a single agent given unlimited time to always match or outperform a team with the same budget, since it avoids the team’s coordination costs, as Ord’s model predicts when λ is below 1. In practice, however, time is limited. Frontier models are superseded within months, so budgets of this size can only be used by spreading the work across many agents running at once, even though this usually spends more tokens for a given result. More generally, **whether a team is worth its extra tokens is determined by the value of time relative to compute**. On tasks where time affects the value of the results – reacting to a security incident or acting on new data in a financial market, for example – it may be preferable to run multiple agents to leverage more compute within the limited time window.

### An apparent swarm premium disappeared after letting the single agent restart

The one apparent exception is the git-to-zig task. At 8M, GPT-6.1 Sol’s self-organized teams scored about the same as the single agent over 10 runs of each configuration. Within a run, larger teams fell behind the single agent early on, because they paid a larger coordination cost, but then improved quicker.

We therefore repeated the comparison at 32M weighted tokens, again with 10 runs of each setting. At this budget, self-organized teams *outperformed* the single agent: Sol’s teams of 8 scored 93.2% against 83.7%, and GPT-6.1 Terra’s teams of 2 and 8 scored 29.1% and 32.0% against 26.6%, although its teams of 4 did not (25.4%). We also ran Terra in larger teams at this budget. Teams of 16 scored 33.3%, about the same as teams of 8, and teams of 32 scored 23.2%, below the single agent.[^6] This gain did not come from scoring a team on its best agent alone: the best of 8 single agents, each scored after 4M weighted tokens, reached 43.7% for Sol and 13.1% for Terra. If teams could do this on many tasks, adding agents would become a new axis along which performance scales.

One possibility is that agent diversity could allow a team to outperform a single agent on the same budget: agents running on different models may be good at different things, which we explore in the appendix on model diversity. But here every agent in a team was running the same model.

Another possibility is that the single agent’s performance diminished as its session got longer, while the members of the team, each working with a fraction of the budget, had much shorter sessions. Ord has [suggested](https://www.lesswrong.com/posts/6cb7qd3RSkgnviCpf/swarm-scaling?commentId=ZetcX8S8yFAxhZsur) that very long chains of thought may degrade this way, potentially allowing swarms to outcompete a single agent. To test this, we split the single agent’s budget into eight sessions run consecutively, as many as a team of 8 runs in parallel. Each session began with a fresh context but retained the files the previous session had left behind.[^7]

The restarted single agent outperformed the teams at both budgets. At 32M, it scored 97.0% for Sol and 41.9% for Terra, compared to 93.2% and 32.0% for teams of 8. It also beat Terra’s teams of 16 and 32. At 8M, where the teams had only matched the single agent, it scored 62.1% and 28.0%, against 55.0% and 17.8%. Measured against the restarted single agent, the teams’ λ fell below 1 at both budgets: at 32M from above 1 to 0.94 for Sol and 0.75 for Terra, and at 8M from about 1 to 0.89 and 0.60. So the teams did better than one long session, but not better than eight shorter sessions run one after another. [Cai et al. (2026)](https://arxiv.org/abs/2610.07447) found something similar for autoresearch agents.

<video src="https://www.paradigm3.org/img/swarms-restart.mp4" controls="" aria-label="On git-to-zig, a single agent that restarts its session beat GPT-6.1 Sol&#39;s and GPT-6.1 Terra&#39;s self-organized teams of 8 by 3.8 to 10.2 points, at 32M and at 8M weighted tokens"></video>

Part of the restarted agent’s advantage comes from including cached input tokens in the budget. Shorter sessions fit more calls into the same budget because every model call re-reads the context as cached input. At 8M, Terra’s restarted agent made about 60% more calls than a Terra single agent. However, at 32M, Sol’s restarted agent made roughly the same number of calls as the Sol single agent and still scored 13 points higher. So how we count tokens isn’t the full story – a long session never wholly resets, even with compaction. Every time the agent compacts, it [has to guess what will matter later](https://www.primeintellect.ai/blog/on-the-nature-of-the-swarm#compaction). We thus think stale or irrelevant information builds up and is carried forward. Restarting the sessions without compaction removes this history, leaving only the files on disk. In essence, members of a team have shorter sessions and so less context to carry, which we believe explains both why teams beat one long session at 32M and why the restarted agent, which got the same short, clean sessions without a team’s coordination cost, beat the teams.

One open question is whether training models to work in teams raises λ. On git-to-zig, GPT-6.1’s self-organized teams came closer to their single agent than any other teams we ran, roughly matching one long session at 8M. They coordinated on Codex’s message board, the only channel in our study that any lab appears to use in training. To see what role that training played, we tested the recently released GPT-6.2 Sol on git-to-zig at 8M using the same message board. Its teams of 2 and 4 scored slightly below one long session, and its teams of 8 scored 24% below. We did not run restarts with GPT-6.2 Sol, and it is much stronger on this task, so we cannot separate every factor. Still, we tentatively conclude that GPT-6.1’s teams matched one long session mostly because its single agent degraded as stale or irrelevant context built up. Whatever teamwork training OpenAI may be doing does not yet seem enough for its teams to match a single agent at an equal budget.

### Read more

- *What exactly did you do?* See [Methodology](#appendix-methodology)
- *What about diverse agents?* Our swarms are clones, and [classic](https://politicalphilosophyjournal.org/article/id/23914/) [arguments](https://cdn.mises.org/qjae5_3_3.pdf) for the superiority of distributed work often require us to sample knowledge and skill from very different agents. We ran [a small test](#appendix-cyberhayek-does-model-diversity-help) on teams composed of GPTs and Claudes, finding that no mixed team clearly outperformed the best single agent either.
- [*What does letting them talk do*](#appendix-how-much-does-communication-add)? Overall there was a huge spread (−17 to +53 points) compared to teams of individual workers.
- [*Do newer models collaborate better?*](#appendix-are-models-improving-at-collaborating) We only ran a few experiments here (comparing four older models with their newer versions, such as Opus 5 with Opus 5.5 and GPT-6.1 Sol with GPT-6.2 Sol), but we see similar or worse losses for newer models.
- In July, OpenAI found a higher ceiling for swarms. What gives? They didn’t do matched compute (“trading higher token use for stronger results”). [We replicated it anyway](#appendix-replicating-openais-multi-agent-browsecomp-results), finding results that were 1-8pp worse than OpenAI’s result. We don’t know why.
- [*What do other people find*](#appendix-other-evidence)? Most don’t match compute spend for the solo agents. Of those that do, only General Reasoning’s Avalon-M1 claims ~parity with an equally flush solo agent. Everyone else is doing an unfair test or finds a penalty like ours.
- [*What did swarms look like in 2014?*](#appendix-philosophy-as-testable-prediction) Bostrom had 3 ways of making a “collective” better. Adding a fourth way, we don’t see them yet.

### Takeaways

So, is adding agents a new axis for scaling LLM capabilities? **Not if the point is to do harder things, and not if the point is to do more with fewer tokens.** At matched budgets, no swarm clearly beats a single agent (as long as it can restart its session). So, for now, on public models, a swarm is just a faster, less efficient form of what Ord calls “[duration scaling](https://www.tobyord.com/writing/swarm-scaling).”[^8]

In the one case where teams looked better (GPT-6.1’s self-organized teams on git-to-zig at 32M), a single agent that worked across eight fresh sequential sessions did better.[^9] Against that baseline, λ for teams of 8 was 0.94 for Sol and 0.75 for Terra at 32M, and 0.89 and 0.60 at 8M. We ran the restarted baseline only on git-to-zig, so our other comparisons may flatter the teams.

[Bostrom (2014)](https://www.lesswrong.com/posts/semvkn56ZFcXBNc2d/superintelligence-5-forms-of-superintelligence#Summary) distinguishes three ways an AI could become better than humans at things. It could be 1) a speed superintelligence (which has human-level abilities, but acts much faster than us and so is able to outmaneuver us), or 2) a collective superintelligence (which ties many smaller intellects together to outperform any existing system), or 3) a quality superintelligence (which is able to solve problems that are beyond us). Bostrom’s baseline is a human mind (or a whole human civilization), and ours is a single agent running the same model as the swarm.

A swarm is a collective. Under [Ord’s model](https://www.tobyord.com/writing/swarm-scaling), a team of N agents finishes N^λ times sooner than a single agent would, and spends N^(1−λ) times as many tokens for the same result. With λ < 1, swarms buy speed at a token premium. At the values we measured for teams of 8 on git-to-zig, that means finishing about 3.5 times sooner for 2.3 times the tokens at the low end (Terra at 8M), and about 7 times sooner for 13% more tokens at the high end (Sol at 32M). With λ > 1, the team would be getting something from collaboration that serial work does not provide. A quality gain would be a team reaching results that a single agent does not reach at any budget.

A swarm is a fast collective. In our experiments, swarms reached a given score far faster than a single agent. Teams of 8 typically spent the same budget about 6 times sooner than the single agent and scored about 7% lower. They also had more CPUs, N times as many on three of the tasks, so part of that may be hardware. At the scale of OpenAI’s Navier–Stokes run – which consumed ~ [130 billion](https://openai.com/index/navier-stokes-solution/) output tokens in 88 hours – one agent would have needed years. When you need an answer now, as you often do, adding agents is the main way to put a lot more compute into a problem. In that limited but maybe practically transformative sense, it is effectively a new scaling axis, even if the effect is fully reducible to inference scaling.

A swarm is not currently a quality collective. Where single agents had nearly saturated a task (the performance take-home, and AHC014 for Claude), swarms were able to match their performance. On the other tasks, our budgets were too small to find the single agent’s ceiling.

![A team trades tokens for time: under Ord's model, N agents reach the same result N^λ times sooner for N^(1−λ) times the tokens; self-organized teams of 8 on git-to-zig sit at λ = 0.60 to 0.94 against a single agent that restarts](https://www.paradigm3.org/img/swarms-tokens-for-time.webp)

A team trades tokens for time: under Ord's model, N agents reach the same result N^λ times sooner for N^(1−λ) times the tokens; self-organized teams of 8 on git-to-zig sit at λ = 0.60 to 0.94 against a single agent that restarts

This could change: labs have only recently started training models to work in teams; our team designs were simpler than the several teams OpenAI ran for its Navier–Stokes proof; our budgets were a hundred times smaller than some lab runs, so we cannot rule out teams that pay a coordination cost early and pull ahead later. Humans have tried only a fraction of the possible ways to organize research ([Nielsen and Qiu, 2022](https://scienceplusplus.org/metascience/)).

Single agents might not outperform swarms next year. Recall that the largest reported swarm went from 16 agents to 10,000 in the last seven months.

Still, we’re fairly happy to say that it hasn’t happened yet.

## Metadata

- Cost to replicate the above: $70,000 at API pricing, or roughly 30 weeks of a (late-2026) Codex Pro subscription + 15 weeks of a Claude Ultra subscription.
- Data [here](https://www.paradigm3.org/research/swarms/data).
- Code [here](https://github.com/paradigm-3-institute/raising-the-roof).

Thanks to Juan Vazquez for discussions, and to Noah Perez for editing this post.

## Appendix: Methodology

### Tasks

We evaluated agents on four tasks: one from FrontierSWE v2, two from ALE-Bench, and Anthropic’s original performance take-home. We chose these tasks because all four are long enough to justify budgets of millions of weighted tokens, have a continuous score, and let agents check their own work as they go.

| Task | Source | Score |
| --- | --- | --- |
| git-to-zig | FrontierSWE v2 (Proximal Labs) | Percentage of git’s tests passed |
| AHC014 “RectJoin” | ALE-Bench (Sakana AI) | AtCoder performance |
| AHC038 “Tree Robot Arm” | ALE-Bench (Sakana AI) | AtCoder performance |
| Performance take-home | Anthropic | Clock cycles (lower is better) |

#### git-to-zig (FrontierSWE v2)

![git-to-zig: agents reimplement git in Zig and can run git's own test scripts at any time; a separate verifier runs 743 of them on the final code](https://www.paradigm3.org/img/swarms-task-git-to-zig.webp)

git-to-zig: agents reimplement git in Zig and can run git's own test scripts at any time; a separate verifier runs 743 of them on the final code

[FrontierSWE v2](https://github.com/Proximal-Labs/frontier-swe-v2) is a benchmark of long, open-ended software engineering tasks by Proximal Labs. In the git-to-zig task, agents must reimplement git in the Zig programming language so that it behaves exactly like the real git. Agents can run git’s own test scripts at any time, and their final code is graded on 743 of them. The score is, roughly, the percentage of those tests passed.

#### AHC014 and AHC038 (ALE-Bench)

![AHC014, RectJoin: each move adds a dot that completes a rectangle with three existing dots, upright or tilted 45 degrees; dots far from the center are worth more](https://www.paradigm3.org/img/swarms-task-ahc014.webp)

AHC014, RectJoin: each move adds a dot that completes a rectangle with three existing dots, upright or tilted 45 degrees; dots far from the center are worth more

[ALE-Bench](https://github.com/SakanaAI/ALE-Bench) is a benchmark by Sakana AI built from past AtCoder Heuristic Contests, where human programmers spend one to two weeks competing on hard optimization problems that have no known best answer. Agents write a C++ program and can test it on 50 public cases during the run. At the end, their best program is graded on the contest’s 2,000 hidden cases, and the score is the AtCoder performance that result would have earned against the original human contestants.

In AHC014, “RectJoin” (2022), agents play a one-player pencil-and-paper game on a square grid that starts with a few dots. Each move adds one dot: the agent picks an empty point that, together with three existing dots, forms the corners of a rectangle (upright or tilted 45 degrees), and draws that rectangle. A new rectangle can’t run along the lines of earlier ones, so early moves limit later ones. Dots far from the center are worth more, and the goal is to end with as much total dot value as possible.

![AHC038, Tree Robot Arm: agents design a branching robot arm, then steer it to move every item onto a target square in as few turns as possible](https://www.paradigm3.org/img/swarms-task-ahc038.webp)

AHC038, Tree Robot Arm: agents design a branching robot arm, then steer it to move every item onto a target square in as few turns as possible

In AHC038, “Tree Robot Arm” (2024), a grid holds a set of items that must be moved onto a set of target squares. Agents first design a robot arm, a branching structure with several fingertips that can each carry one item, and then steer it. Each turn, the arm can slide one square, swing any of its branches by 90 degrees, and pick up or drop items with its fingertips, all at once. The goal is to get every item onto a target in as few turns as possible, so both the arm design and the plan for moving it matter.

#### Performance take-home (Anthropic)

![Anthropic's performance take-home: rewrite a program so it runs in fewer clock cycles on a simulated chip; the starting program takes 147,734 cycles](https://www.paradigm3.org/img/swarms-task-take-home.webp)

Anthropic's performance take-home: rewrite a program so it runs in fewer clock cycles on a simulated chip; the starting program takes 147,734 cycles

The performance take-home is the exercise Anthropic used to hire performance engineers. Anthropic [released it publicly](https://github.com/anthropics/original_performance_takehome) in January 2026, once Claude Opus 4.5 matched the best human result within its 2-hour limit ([Designing AI-resistant technical evaluations](https://www.anthropic.com/research/AI-resistant-technical-evaluations)). Agents must make a small program run as fast as possible on a simulated chip. The score is the number of clock cycles their version takes to run on the simulated chip, so lower is better.

### Multi-agent setups

For each task we compared a single agent with teams of 2, 4, and 8 agents, while keeping the total token budget fixed.[^10] We tested three team setups. In the first, which we call protocol teams, agents follow fixed rules in the prompt for taking separate approaches and sharing findings. In the second, which we call self-organized teams, agents are equal peers with no fixed rules and decide among themselves how to collaborate. In the third and last, which we call orchestrated teams, an orchestrator agent directs the rest of the team, delegating tasks to helper subagents and combining their results.

| Setup | Models | How the team is organized | How agents communicate | Team of N |
| --- | --- | --- | --- | --- |
| Protocol | Anthropic and OpenAI models | Fixed rules in the prompt | Shared files | N equal agents |
| Self-organized | Anthropic and OpenAI models | Left to the agents | Codex’s message board (OpenAI), Claude Code’s direct messages (Anthropic), or a shared chat (mixed teams) | N equal agents |
| Orchestrated | OpenAI models only | Left to an orchestrator agent | The orchestrator hands out tasks and helpers report back | 1 orchestrator + up to N−1 helpers |

#### Protocol teams

Protocol teams follow one of the prompts from Park et al.’s “[Scaling Discovery through Test-Time Communication](https://github.com/jerryjonghopark/test-time-communication)”. The prompt is designed to keep the team exploring diverse approaches rather than collapsing onto a single one too early.

All agents receive the same prompt and share a folder. The prompt instructs the agents to claim a numbered slot with an approach that differs from the others’, log its findings with evidence, spend part of its time trying to disprove whichever approach has worked best so far, and switch to a teammate’s approach only when hard evidence shows it is clearly better.

#### Self-organized teams

On September 8, 2026, OpenAI reported a [resolution of the Navier–Stokes Millennium Prize problem](https://openai.com/index/navier-stokes-solution/) produced by “a system of coordinating agents powered by our internal model.” The agents were “subdivided into groups with the ability to communicate within the group,” and the group that produced the proof involved “on the order of 10,000 concurrent agents,” which exchanged 2.7 million messages. This led us to look at what OpenAI has said about how it runs its agent teams. Noam Brown, a researcher at OpenAI, discussed the setup on the [Dwarkesh Podcast](https://www.dwarkesh.com/p/noam-brown) on September 17. He described training environments “where we have a bunch of agents working together,” in which agents get “very primitive tools to use, and they figure out for themselves how to use them effectively.” The main such tool is the ability to message other agents, and he compared the result to “how human collaborators work over something like Slack.”

Codex, OpenAI’s open-source coding agent, contains a feature that matches this description: a message board shared by a team of agents ([PR #46985](https://github.com/openai/codex/pull/46985)). Agents can create channels, start threads, reply, search past posts, and subscribe to channels or threads. Agents subscribed to a thread, or named in a post, receive a short notification during their current turn. The feature is not offered to users. Codex marks it as [“still under development, not ready for external use”](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/features/src/lib.rs#L47-L49), it is [disabled by default](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/features/src/lib.rs#L1444-L1449), and unlike experimental features it does not appear in Codex’s /experimental menu. It is nonetheless fully implemented and can be enabled in Codex’s configuration.

Several comments in Codex’s source code suggest the board is used in OpenAI’s training. They describe [“Tree-owned message boards for training”](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/ext/agent-message-board/src/in_memory.rs#L1) and [“A board held in memory for one training rollout”](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/ext/agent-message-board/src/in_memory.rs#L67) ([PR #47946](https://github.com/openai/codex/pull/47946)), a setting to [“Keep the message board in memory for a training session”](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/features/src/feature_configs.rs#L333), and a connection to [“a board provisioned by the research host”](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/features/src/feature_configs.rs#L12) ([PR #48100](https://github.com/openai/codex/pull/48100), [PR #49267](https://github.com/openai/codex/pull/49267)).

We ran Codex with the board enabled. Codex’s built-in board only connects agents within a single Codex process, whereas our agents run as separate processes. We therefore used Codex’s support for remote boards ([PR #49267](https://github.com/openai/codex/pull/49267)) and hosted a board server that reproduces the built-in board’s behavior. The agents see Codex’s own board tools, tool descriptions, and notifications.

Self-organized agents decide how to collaborate by themselves. Each receives the task and a prompt that only sets a shared goal and introduces their Slack-like messaging channel. For GPT teams on the message board, the prompt is:

> You are one of N agents working on this task at the same time, in this container, all with this same prompt. You are one team: the team is scored on its best result, so whatever any one of you achieves counts for all of you.
> 
> The team shares a message board, like a team Slack: channels, threads and posts that everyone can read, search and subscribe to. Your teammates are /root/a1, /root/a2, …. The board’s tools (post, read\_thread, subscribe, …) are collaboration tools.
> 
> How you split the work, what you share, and when you talk is up to you. Work it out among yourselves.

Unlike protocol teams, there are no slots, shared files, or rules, so whatever organization appears is emergent.

Claude Code has no message board, but its agents can send one another direct messages through [cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging). Self-organized Claude teams used this channel. Their prompt was the same, except that the paragraph about the board was replaced with “You can message one another, like direct messages in a team Slack: each message goes to one teammate.” We report these teams on git-to-zig only, because the runs on the other three tasks did not finish in time for publication.

Since self-organized mixed teams (that is, teams that mixed Claude and GPT agents) had no native way to talk across their harnesses, they instead leveraged the recently released [SwarmChat](https://swarmchat.io/). Since GPT agents generally spent their budget faster than Claude agents, we paused any agent that got 250k weighted tokens ahead of the slowest agent in the team until the slowest caught up.

#### Orchestrated teams (OpenAI models only)

Orchestrated teams use Codex’s Ultra mode. Ultra is OpenAI’s highest-capability setting in Codex, “[coordinating multiple agents across parallel workstreams to finish complex tasks faster](https://openai.com/index/gpt-5-6/).” One orchestrator agent starts helper agents, hands them parts of the work, and combines what they produce. We turned this on with [the instruction Codex itself sends in Ultra mode](https://github.com/openai/codex/blob/rust-v0.162.1/codex-rs/prompts/src/model_messages/multi_agent.rs#L47), which includes:

> If at any point you can parallelize work by delegating tasks to another agent (no matter if you are root or subagent), you should do so using collaboration tools if it could save time or improve quality.

The prompt also says “At most N agents, you included, can work on this task at the same time.” A team of N therefore means one orchestrator and up to N−1 helpers running at once. The orchestrator decides how many helpers to start and when, and the whole team shares one token budget. Otherwise, the only difference from Codex’s built-in Ultra mode is the reasoning effort. Ultra normally raises it to the maximum, whereas we kept every agent at the same level as in the other setups. As in self-organized teams, the organization is emergent, but here one agent is in charge and in principle directs the work, while in self-organized teams every agent is an independent peer.

### Run setup

#### Token budget

We ran every task, for single agents and teams alike, with a fixed budget of weighted tokens, so that a team and a single agent are compared at the same total cost. Following [the evaluation of DeepSeek models by the Center for AI Standards and Innovation (CAISI)](https://www.nist.gov/system/files/documents/2025/09/30/CAISI_Evaluation_of_DeepSeek_AI_Models.pdf) (Appendix A2), the budget tracks the weighted sum of output tokens (100% weight), unique input tokens (23% weight), and total input tokens (2% weight). An uncached input token therefore costs a quarter of an output token, and a cached input token 2% of one. Most comparisons use a total of 8M weighted tokens. In protocol and self-organized teams this total is split evenly between the agents of a team, so that each agent of a team of N has its own budget of 8M/N and stops once it has spent it, while in orchestrated teams the orchestrator and its helpers draw on a single shared budget of 8M. Agents can query their remaining budget and time at any point during a run.

A team may pay a coordination cost early in a run and only overtake a single agent later, which a small budget would not reveal. To check for this, some comparisons were repeated at 32M weighted tokens: GPT-6.1 Terra on git-to-zig, AHC014, and AHC038; GPT-6.1 Sol on git-to-zig; and Claude Opus 5.5 on git-to-zig (two runs each).

To measure λ, we also ran single agents with 2M weighted tokens on git-to-zig and both AHC tasks, three runs per model. For a team of N agents, each with budget b, we find the budget X at which a single agent would reach the team’s mean score, assuming its score grows linearly with the logarithm of its budget between the budgets we ran, and set λ = ln(X/b) / ln N. We ran separate 2M runs rather than reading a single agent’s score after 2M from an 8M run, because agents can see their remaining budget and plan around it. We did not run them on the performance take-home, where single agents barely improve with budget.

#### Models, effort, and repeats

| Model | Single agent | Protocol teams | Self-organized teams | Orchestrated teams |
| --- | --- | --- | --- | --- |
| Claude Opus 5.5 | All four tasks; also 32M on git-to-zig | All four tasks | git-to-zig; also 32M on git-to-zig (team of 8) | – |
| Claude Sonnet 5.5 | All four tasks | All four tasks | git-to-zig | – |
| GPT-6.1 Sol | All four tasks; also 32M on git-to-zig | All four tasks | All four tasks; also 32M on git-to-zig (team of 8) | All four tasks |
| GPT-6.1 Terra | All four tasks; also 32M on git-to-zig, AHC014, AHC038 | – | All four tasks; also 32M on git-to-zig, AHC014, AHC038 | – |

Claude Opus 5, Claude Sonnet 5, and GPT-5.6 Terra were also run, on git-to-zig and AHC038 only, for the comparison between model generations. GPT-6.2 Sol, the newest model in that comparison, was run on git-to-zig only, as a single agent and in self-organized teams, five times per configuration. All runs used high reasoning effort. Each configuration was run three times by default, and a few git-to-zig comparisons were run 10 times to separate real differences from run-to-run variance.

#### Codex versions

GPT-6.1 Sol’s protocol teams, and some of the runs they were compared with, used Codex 0.160.0, the version we started on. Self-organized teams need remote message boards, which first shipped in 0.162.1, and most other GPT runs used that version.

Late in the project, we found a bug in both versions. When a message arrived mid-session, Codex double-counted the model’s earlier reasoning in its context estimate and could compact too early. The message could come from a teammate, or from our harness telling an agent to keep working after it stopped. The bug affected every setup, especially teams whose agents message each other. In self-organized teams, nearly every compaction happened at about 230k to 350k tokens instead of 450k. Later Codex versions fix the same double counting for resumed and forked sessions ([PR #57839](https://github.com/openai/codex/pull/57839)). We patched the bug and reran Sol’s and Terra’s self-organized teams of 8 on git-to-zig at 32M, where teams did best. Neither scored higher than before (Sol 89.7% against 93.2%, Terra 31.5% against 32.0%). The bug therefore does not appear to have affected our findings. All runs started after the fix used the patched build, including Terra’s teams of 16 and 32 and the restarted agents at 8M.

GPT-6.2 Sol needs a newer Codex. We ran it on 0.170.0 with the same patch.

#### Compute

The agents of a team share one container. On AHC014, AHC038, and the performance take-home, each agent is given 2 CPUs and 6 GB of memory, so that a team of N has N times as much. On git-to-zig, a single agent has the task’s standard 4 CPUs and 16 GB, and every team has 8 CPUs and 32 GB regardless of its size. An orchestrated team gets the resources of a team of the same size. Grading always runs outside the agents’ container. ALE-Bench’s judge and the take-home’s scorer run on separate CPUs, and git-to-zig’s verifier runs in its own container with 4 CPUs and 16 GB.

#### Scoring

A team is scored on its best result: its score is that of the best submission made by any of its agents, graded in the same way as a single agent’s submission.

#### Single-agent baselines

We used three single-agent baselines.

A plain single agent gets only the task instructions and runs in one session. This is our default baseline, and we compared self-organized teams against it because their prompt only adds a short note about the team.

A matched single agent gets the protocol prompt without any mention of teammates, keeping the slot, findings, and disconfirmation files as private notes. This tells us whether a protocol team does better because of teammates or just because of the protocol specified in the prompt. We ran it on AHC014 and AHC038 with Claude Opus 5.5, Claude Sonnet 5.5, and GPT-6.1 Sol.

A restarted single agent splits its budget across eight sessions run one after another, matching the eight sessions a team of 8 runs in parallel. Each session starts with a fresh context and keeps the files left behind by the previous one. This tests whether a team’s advantage comes from working in parallel or simply from running shorter, fresher sessions. We ran it on git-to-zig at 8M and 32M with GPT-6.1 Sol and GPT-6.1 Terra.

#### Keeping agents working

Agents work in turns, and models often end a turn early, for instance by declaring the task finished while budget remains. When this happens the harness sends a continuation message, up to 1,000 times per run, telling the agent that the task is not finished, that its best result so far is saved, and that a plateau is a reason to try a structurally different approach rather than to stop. Agents can nevertheless stop for good: an agent that ends 10 continuation turns in a row, each lasting less than a minute and making at most two tool calls, is treated as having given up and is stopped.

Each run also has a cap on working time, set per batch of runs at between 2 and 16 days, which ends runs whose agents spend their budget very slowly. Runs used subscriptions rather than API keys, so agents sometimes waited for usage limits to reset, and this waiting time is excluded from the times we report.

## Appendix: Cyberhayek: Does model diversity help?

[Hong and Page (2004)](https://www.pnas.org/doi/full/10.1073/pnas.0403723101) argued that a group of diverse problem solvers can outperform a group of the individually best ones, because the best solvers tend to resemble one another and get stuck in the same places.[^11] Since each of our teams used a single model, we wondered whether this lack of diversity was part of the reason teams did not outperform single agents at the same budget.

As an initial test, we ran protocol teams of 2, 4, and 8 agents (8M weighted tokens, three runs each) in which half of the agents were GPT-6.1 Sol and half Claudes with similar performance on the task. On AHC014 and the performance take-home, the Claude model was Claude Opus 5.5. On git-to-zig it was Claude Sonnet 5.5, because in single-agent runs with the prompt of protocol teams, Opus scored far above Sol. In our main single-agent runs, however, Sol scored far above Sonnet (53.3% against 41.7% of tests passed), so on git-to-zig the two halves of each team were not equally strong.

![The mixed-team setup: teams of 2, 4 and 8 split 8M weighted tokens evenly, half GPT-6.1 Sol and half Claude (Sonnet 5.5 on git-to-zig, Opus 5.5 on AHC014 and the take-home)](https://www.paradigm3.org/img/swarms-diversity-setup.webp)

The mixed-team setup: teams of 2, 4 and 8 split 8M weighted tokens evenly, half GPT-6.1 Sol and half Claude (Sonnet 5.5 on git-to-zig, Opus 5.5 on AHC014 and the take-home)

On git-to-zig, self-organized teams of Opus, Sonnet and Sol all scored higher than their protocol teams, so we also ran mixed self-organized teams of Sonnet and Sol there. Claude Code has no message board, so the mixed teams shared a chat built with [SwarmChat](https://swarmchat.io/), which works in both Claude Code and Codex.

<video src="https://www.paradigm3.org/img/swarms-diversity.mp4" controls="" aria-label="Mixed Claude and GPT-6.1 Sol teams scored between their Claude-only and Sol-only teams in 8 of 12 cases, on git-to-zig, AHC014 and the performance take-home; none clearly beat the best single agent"></video>

On AHC014, 16 of the 30 runs in this comparison reached 3389, the performance for first place and the highest possible. Because the task is close to saturated on this measure, the chart compares AHC014 results by raw score per hidden case, which still tells those runs apart.

In this small set of runs, mixing models had no clear effect. A mixed team usually scored between a Claude-only team and a Sol-only team of the same size, and when it beat both, it did so by only a few percent. No mixed team clearly outperformed the best single agent.[^12]

A tentative explanation is that current models are still broadly similar to one another, because they were trained on similar pretraining data and in similar reinforcement learning environments. A team that mixes them is therefore only a little more diverse than a team of one model.

Our experiments are far from conclusive, mainly because it is hard to find tasks on which two models are about equally strong. When one model is clearly stronger, giving half of the team to the weaker model lowers the team’s score, which can hide any benefit from diversity. In our runs, the two models were about equally strong only on AHC014 and the take-home. On both of those tasks, single agents were already close to the ceiling, which left teams little room to improve.

Finally, you might say that Claudes and GPTs are ultimately very similar to each other, and we’ll need some actually diverse kinds of AI to get the Hayekian gains. Could well be.

## Appendix: How much does communication add?

[Park et al. 2026](https://arxiv.org/abs/2609.21032) obtained a very striking result: letting swarm members communicate with others produced enormous gains over having the same number of agents working independently. (These two settings correspond to our “protocol team” and “no-talk team”.) In particular, their results include a 3.6x higher solve rate on ARC-AGI-3 (2.2% to 8%) for communicating swarms.

In our settings, how much do agents gain from talking to each other?

Our control is “best@k”: a no-talk team of $k$ agents that can’t communicate. Each agent gets a team member’s share of 8M weighted tokens (8M/k) and the task prompt, which doesn’t mention teammates. We score the group on its best agent’s result.[^13] We match protocol teams with no-talk agents given the protocol prompt, and self-organized teams with ones given the plain task prompt. We get no-talk controls for protocol teams of Claude Opus 5.5, Claude Sonnet 5.5 and GPT-6.1 Sol instances, and for self-organized teams of GPT-6.1 Sol and GPT-6.1 Terra, but not for orchestrated teams or Claude’s self-organized teams.

Call the “talk gain” a team’s score minus the equivalent score for its no-talk version, in points (where a “point” is 1% of the same model’s single-agent score). The gain reflects everything that comes with being on a team: the messages, the team’s instructions, working on one shared program, and the tokens spent on messages.

<video src="https://www.paradigm3.org/img/swarms-communication.mp4" controls="" aria-label="Talking added up to 53 points on git-to-zig over no-talk teams of the same size; on AHC014 and AHC038 it cost GPT teams in all 18 cases and Claude Opus 5.5 in none; on the performance take-home it changed little"></video>

The talk gain depends mostly on the task. On git-to-zig, talking helped a lot. Teams of 4 and 8 gained 16 to 53 points over their no-talk versions, and teams of 2 gained less. (One team lost points from talking.)

The talk gain was larger for self-organized teams than protocol teams. In teams of k=8, GPT-6.1 Sol’s self-organized team gained 53 points vs its protocol team gaining 20. On AHC014 and AHC038, talking cost GPT’s teams 2 to 12 points in every comparison, while Claude Opus 5.5’s teams did as well or slightly better. On the performance take-home, every team stayed within ~4 points of its no-talk baseline.

As in our main results, we see no-talk teams (with a reduced per-agent budget) doing worse compared to giving one agent a massive budget. On git-to-zig, no-talk@8 scored 31% to 60% below the single agent, and on the other tasks they stayed within about 10% of it. Protocol teams@8 lost more than half their score to splitting. Talking won back 18 to 26 points, and they still finished 27% to 41% below. GPT’s self-organized@8 made up the whole loss and ended level with the single agent or slightly above.

We guess the difference comes from how each task is scored. The git-to-zig score counts thousands of tests of different parts of the program. Since team members can make some of them pass on their own, their gains can add up in parallel. Conversely, on the AHC tasks and the take-home exercise, the score measures one algorithm or kernel, and a small budget gets most of the way. Team members’ improvements are then mostly alternatives to one another, and only the best counts. We don’t know why talking hurt GPT’s teams on the AHC tasks but not Claude Opus 5.5’s. We speculate that talking may pull the agents toward a single approach, so that the best of several attempts is little better than one.

We only ran three runs per team, so we’re underpowered to measure a performance penalty of just a couple points.

## Appendix: Are models improving at collaborating?

Teams rarely outperformed single agents in our experiments. That could change if newer models collaborate better than older ones, but we found no clear sign that they do.

We compared four older models with their newer versions, measuring how much each model’s teams lost against its own single agent with the same budget. Task difficulty confounds this comparison. Teams lose more on tasks the model finds hard, and our tasks are usually much harder for the older models.

The only pair of models whose single agents scored about the same was Claude Opus 5 and Opus 5.5, on AHC038. Two protocol teams of these two models lost roughly the same amount of performance compared to their single agents (7 to 10% for Opus 5, 5 to 8% for Opus 5.5).

On git-to-zig, every newer model’s single agent scored much higher than the older single agent, which by itself should make its teams lose less. The teams of Claude Opus 5.5 and Sonnet 5.5 did lose much less. GPT-6.2 Sol’s teams lost more than GPT-6.1 Sol’s, but GPT-6.1 Sol’s teams matched its single agent largely because that agent goes stale over a long session, as the restarts in the main text showed. We did not run restarts with GPT-6.2 Sol.

We could not compare GPT-5.6 Terra with GPT-6.1 Terra, because GPT-5.6 Terra’s single agent gave up long before spending its budget.

So far, each new model has mainly brought a stronger single agent.

## Appendix: Replicating OpenAI’s multi-agent BrowseComp results

### Motivation

In its [GPT-5.6 announcement](https://openai.com/index/gpt-5-6/), OpenAI reports results for GPT-5.6 Sol running as a team of agents in Codex on three benchmarks: BrowseComp, SEC-Bench Pro, and Terminal-Bench 2.1. We attempted to reproduce one of these results, to check whether our harness matches OpenAI’s scores and to compare our team setups with OpenAI’s own setup on the same benchmark.

Of the three benchmarks, BrowseComp was the most practical to run. SEC-Bench Pro consists of cybersecurity tasks, which are likely to trigger the safety classifiers that stop agent runs. Terminal-Bench 2.1 contains several hundred tasks, which would make repeated runs across several setups expensive. BrowseComp has difficulties of its own: it contains 1,266 questions, it requires agents to have internet access, and agents with internet access can find leaked answers online, as Anthropic reported for [Claude Opus 4.6](https://www.anthropic.com/engineering/eval-awareness-browsecomp).

### Setup

To limit cost, we used a random sample of 253 questions, or 20% of the benchmark. All runs used GPT-5.6 Sol. We compared a single agent with an orchestrated team in Codex’s Ultra mode, run with at most 4 agents active at once. OpenAI has not described its multi-agent setup in detail, and Ultra is our best approximation of it. At high reasoning effort, we also ran protocol and self-organized teams of 4 agents. We followed the official evaluation methodology, in which each agent submits an answer once it considers the answer ready and is not prompted to continue afterward. As in OpenAI’s evaluation, answers were graded by GPT-4.1 with the grader prompt from OpenAI’s simple-evals.

To prevent agents from finding leaked answers, every search passed through a filter that blocked Hugging Face and GitHub and withheld any result or page that quoted one of the benchmark’s questions. The agents’ containers could not reach the dataset, and we scanned every transcript for signs that an agent had looked for the benchmark or its answers.

### Results

| Setup | Low effort, ours | Low effort, OpenAI | High effort, ours | High effort, OpenAI |
| --- | --- | --- | --- | --- |
| Single agent | 67.6% | 69.0% | 80.2% | 88.2% |
| Orchestrated (Ultra), 4 agents | 74.3% | 81.8% | 83.0% | 90.8% |
| Protocol, 4 agents | – | – | 80.6% | – |
| Self-organized, 4 agents | – | – | 81.0% | – |

With 253 questions, the 95% confidence interval on each of our scores is about ±5 points.

At high reasoning effort, running several agents improves the score only slightly. OpenAI reports an improvement of 2.6 points, and our improvements range from 0.4 to 2.8 points. Protocol and self-organized teams score about the same as the orchestrated team, and the differences between the three multi-agent setups are well within the confidence intervals.

All of our scores are below OpenAI’s: by 1.4 points for the single agent at low effort, and by 7.5 to 8.0 points in the other three comparisons. We have not been able to determine the cause. Possible explanations include an internal harness, a sample that is harder than the benchmark as a whole, our stricter measures against leaked answers, and differences in the reasoning compute available to the model. Our runs used ChatGPT subscriptions, and OpenAI’s internal “juice” setting, which limits how much reasoning a model may use on each request, may differ between these subscriptions and the setup OpenAI used for its evaluation.

## Appendix: Other evidence

| Paper | Do swarms do better? | Matched-compute control? | λ | Max token budget | Setup | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| Us | **A penalty for swarms.** Swarms are ~7% worse than a single agent in 54 of our 70 comparisons and are only equal on saturated tasks. | Yes: equal weighted-token budgets, plus no-talk and restarted-single-agent controls | 0.235 \[-0.39, 0.86\] over all 4 tasks, but we recommend taking the git-to-zig number \[0.6,0.9\] instead, for statistical reasons | 32M weighted tokens<br>(8M in most comparisons) | Opus 5.5, Sonnet 5.5, GPT-6.1 Sol and Terra; teams of 2–8; four tasks lasting hours to days | Our λ estimate is only from one task. |
| [OpenAI](https://openai.com/index/gpt-5-6/) 2026 | **Bonus** (performance) for swarms, monotonically increasing with swarm size. +3pp to +23pp. | No. | Unknown | Unknown | GPT-5.6 Sol with 1, 4, 16 agents on BrowseComp, SEC-Bench Pro, Terminal-Bench 2.1. | Probably just disguised inference scaling. |
| [Ord](https://www.tobyord.com/writing/swarm-scaling) 2026 | **Penalty** (on efficiency)**.** For all performance levels L, the lone agent reaches L with fewer tokens than the swarm. | Yes, by analysis: he’s dealing in tokens per constant score. | 0.48–0.68 | N/A: his argument is from token ratios | GPT-5.6 on BrowseComp, SEC-Bench Pro, Terminal-Bench 2.1; 1 vs 4 vs 16 agents | Read off published charts; larger swarms could have a different λ, as he notes |
| [Mieczkowski et al.](https://www.pnas.org/doi/10.1073/pnas.2612825123) 2026 | **Penalty** (on efficiency)**.** Token savings are rare in its cost table | No. Compute varies freely across conditions; time to finish a fixed job is the outcome | None reported. Seems like ~0.3 pre-assigned and −0.1 self-claiming | No totals. Stated limits are per call (8,192 output tokens) and per run (60 rounds) | Its teams hold up to five copies of GPT-5.2, Sonnet 4.6 or Gemini 3 Flash, on coding jobs of 20 subtasks; the experimenter fixes the division of labour in one condition and leaves it to the agents in the other | Its “done” signal rests on the agents’ word, with tests unverified; a timeout bought a team up to two fresh attempts |
| [General Reasoning](https://www.gr.inc/releases/avalon-m1) 2026 | **Parity.** Or a tiny bonus.<br>At matched tokens, the n=8 swarm scores higher than a solo agent on 35% of benchmarks, but lower on 43%.<br>(They claim a tiny average gain for their swarm but without a statistical test.) | Yes: output tokens are equalised | None reported: ~1 implied. | Unstated: the organisation’s own output count sets the lone agent’s allowance; twelve hours is the longest run mentioned | Its training signal is a single team-level reward with a deadline; teams top out at a CEO agent with eight hires | The lone baseline is the same swarm-trained model, and training had not finished at release; ProgramBench goes the other way, 25.7% against 29.4%<br>“extended thinking recovers about three fifths of the \[swarm\] gain” - only if you exclude SWE-Bench Pro; with it it’s four fifths instead. |
| Aggarwal et al 2026,<br>[SwarmChat](https://swarmchat.io/) | **Penalty** (on efficiency)**.** To reach the same score, swarms needed more tokens than one agent at every size. Over one hour, 1.4× to 2.2×. Over six hours the 8-agent team needed 2.7× the agent-hours. | Partly. Two comparisons come with token counts, and they didn’t test no-talk teams. | 0.43–0.86. | 306M tokens is the largest figure on the page (eight agents, one hour), input evidently included | GPT-6-Luna and Haiku 5.5 take on ten ProgramBench programs in teams of up to sixteen | One run backs each performance figure |
| [Naam](https://www.rameznaam.com/p/can-a-million-ai-agents-create-superintelligence) 2026 | **Penalty.** | No. | 0.75 (<30 agents)<br>0.33 (<100 agents) | Not reported; the biggest team ran 100 agents for “a day” | His main data are a 24-hour team task on 49 Lean theorem statements | No lone agent is given a longer clock; his λ analysis takes ten agents as its starting point |
| Anthropic 2026, [Fable 5.2](https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2/) | **Unknown.** | No | None | ~2B | A lead and 999 helpers share a database and Git in place of messaging | Speed evidence only; model, platform and human steering all changed between September and this run |
| Bespoke Labs 2026, [MAC Bench](https://benchmarks.bespokelabs.ai/multi-agent-coordination-bench/) | **Penalty** (on cost). No fair test for quality. | No. | None reported. ~0.38 from the median time for eight agents to reach the single-agent final score. | ~100M | Opus 5.5, GPT-6.1 Sol and Gemini 4 Argon in their native harnesses; teams of 2, 4 and 8 on a message board; twelve simulated tasks | Time-matched, not compute-matched. They seem to drop six teams that never catch up to the solo agent from the calculation of the median. |
| [Park et al](https://arxiv.org/abs/2609.21032). 2026 | **Bonus** for communicating swarms vs independent agents; **penalty** vs a matched solo-agent. | Not for headline result; swarms lost on ARC when compute was matched. | None reported. Not computable against a single agent; against independent agents a team is worth 4.3 to 6.6 times its headcount | ~24M output on ARC-AGI-3; the research tasks are capped by time, at 72 hours per agent (packing) and 96 hours (MNIST) | Sonnet 4.6, Opus 4.6 and GPT-5.6 Sol in GitHub Copilot CLI; teams of 3 to 5 under the shared-workspace prompt our protocol teams use; ARC-AGI-3, polyomino packing, MNIST compression, Terminal-Bench 2.0 | Only two runs were given 72 hours, and only one run for MNIST; no restarted or longer-running single agent on the research tasks. |

## Appendix: Philosophy as testable prediction

[Bostrom 2014](https://en.wikipedia.org/wiki/Superintelligence:_Paths,_Dangers,_Strategies) guessed that you could scale a collective mind through the team size, their individual quality, and how well they are organized. You could also add diversity as a lever.

- **Number.** On git-to-zig, the best of 8 independent agents with 1M each scored 31–60% below one agent with 8M. On the other three tasks, where single agents gain less from extra budget, the same split cost at most 10%. Where teams fell short, the shortfall usually grew with team size.
- **Organization.** On git-to-zig, communication recovered part of the cost of splitting: protocol teams of 4 and 8 scored 32–56% above no-talk teams of the same size. The setup mattered as well. Self-organized teams scored higher than protocol teams for every model we ran in both, and GPT’s message-board teams roughly matched one long single-agent session at 8M. Some of that gap is the protocol prompt, which lowers a single Sol agent’s score from 53.3% to 42.2% before any teammates are added. On the other three tasks communication added little or nothing, and on the AHC tasks Sol’s protocol teams scored 2–8% below their no-talk teams. On BrowseComp, in our replication of OpenAI’s multi-agent result, the three setups scored within 2.4 points of one another, well within the confidence intervals.
- **Stronger members.** We could make one fair comparison between model generations, on AHC038, which is about as hard for Opus 5 as for Opus 5.5. Their protocol teams lost 7–10% and 5–8% against their single agents. On git-to-zig the newer Claude teams lost much less, but that task is much harder for the older models, and splitting a budget costs more on a harder task. We found no clear sign that newer models collaborate better.
- **Diversity.** [Hong and Page (2004)](https://www.pnas.org/doi/full/10.1073/pnas.0403723101) argue that a diverse group can beat a swarm of clones of the best performer. Teams that mixed GPT and Claude usually scored between the two single-model teams, and none clearly beat the best single agent. This is a weak test, because the two models are maybe not that different from each other, and they were only equally strong on tasks where single agents were already near the performance ceiling.

Bostrom also expected a collective to do best on problems that decompose into parallel parts which can be solved and checked independently, worst on tightly interdependent ones. Our tasks fit that expectation. The git-to-zig porting task is graded on 743 of git’s test scripts, and in self-organized teams of 8, each agent claimed a particular part of git’s functionality in the first minute and stuck to it.

Of the improvements teams made there, 77–94% were separable from the ones just before, against 27–49% on the performance take-home. It is the task on which communication and organization changed the score. Even there, teams only drew level with one long session, and the restarted single agent beat them.

## Footnotes

[^1]: Technically there was a [little orchestration framework](https://github.com/openai/swarm) before that, in October 2024. Clearly related.

[^2]: These systems reportedly made several attempts independently and chose among them, which differs from a team of agents that communicate while they work.

[^3]: It wasn’t very good: “The generated code is not very efficient. Even with all optimizations enabled, it outputs less efficient code than GCC with all optimizations disabled.” But at the time it was *still* not commonly known that large, complex software was in scope for models.

[^4]: Output tokens count fully and input tokens count at a quarter, or at 2% when cached, following [the Center for AI Standards and Innovation (CAISI)](https://www.nist.gov/system/files/documents/2025/09/30/CAISI_Evaluation_of_DeepSeek_AI_Models.pdf).

[^5]: Teams of 8 finished 3 to 16 times sooner than the single agent in almost all configurations, the exception being Claude Sonnet 5.5 on the performance take-home. The gap was largest for Claude models on the AHC tasks and the performance take-home, where single agents often waited on long-running jobs, and some Claude Opus 5.5 single agents reached the 240-hour cap on working time before spending their budget.

[^6]: Bootstrapped 95% confidence intervals for the gap: 3.6 to 15.8 points for Sol’s teams of 8, and 2.2 to 8.4, −0.7 to 5.6, and −4.5 to 1.8 points for Terra’s teams of 8, 2, and 4, from 10 runs of each configuration. For Terra’s teams of 16 and 32, they are 0.8 to 12.4 and −7.4 to 0.5 points, from 5 runs each. These two configurations ran on a patched Codex build (fixing a compaction bug), on which Terra’s teams of 8 scored about the same as on the original build, 31.5% against 32.0%.

[^7]: By analogy, imagine the result of you yourself doing some 2 day task as an all-nighter, compared to doing it as 8 hours work plus sleep plus 8 hours work.

[^8]: One intuition for why adding people reduces progress is meetings: setting aside the long-term benefits and their necessity for cross-organization projects (like ~all of sales), many people know from experience the sheer size of the overhead imposed by communication. And if the overhead uses up the token budget without being as productive as solo work, then you see a performance hit.

[^9]: But this was a post-hoc experiment!

[^10]: For GPT-6.1 Terra on git-to-zig at 32M weighted tokens, we also ran self-organized teams of 16 and 32 agents.

[^11]: Hong and Page’s result is disputed. [Thompson (2014)](https://www.ams.org/notices/201409/rnoti-p1024.pdf) argued that their theorem says little beyond its own assumptions, and that their simulated diverse groups did well because they were picked at random. [Singer (2019)](https://www.danieljsinger.com/papers/Singer%20-%20Diverstiy,%20Not%20Randomness,%20Trumps%20Ability%20%28draft%29.pdf) argued that diversity does explain their results.

[^12]: On AHC014, the mixed team of 2 scored 1.9% above the best single agent in raw score, and on the take-home the mixed team of 8 needed 1.9% fewer cycles. Both differences are within the noise of three runs. The best single agent on AHC014 was Claude Opus 5.5, whose three runs spent only 3.6M to 6.9M of their 8M weighted tokens. Two reached the 240-hour cap on working time and the third stopped on its own, so with the full budget it might have scored higher.

[^13]: We didn’t run each no-talk team separately. For each team size we ran a pool of lone agents, 6 at 4M, 8 at 2M and 12 at 1M, and averaged the best agent’s result over every group of k agents drawn from the pool. We ran Claude Sonnet 5.5 only on git-to-zig, and there is no pool for Claude Opus 5.5’s teams of 2 on AHC038. The score on git-to-zig is the share of its thousands of tests passed, on AHC038 it is AtCoder performance, and on the take-home it is speed. On AHC014 we compare raw score per case, because AtCoder performance stops at 3389, first place, where many Claude Opus 5.5 runs sit.