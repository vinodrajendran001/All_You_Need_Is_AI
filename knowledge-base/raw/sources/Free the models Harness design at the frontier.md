---
title: "Free the models: Harness design at the frontier"
source: "https://replit.com/blog/free-the-models?utm_source=substack&utm_medium=email"
author:
  - "[[Daniel Furman]]"
  - "[[Jacky Zhao]]"
  - "[[Vaibhav Kumar]]"
  - "[[Ed Sioufi]]"
  - "[[Michele Catasta]]"
published: 2026-09-30
created: 2026-10-05
description: "Model routers are everywhere right now, but they have a fundamental limitation. No matter if based on advanced heuristics or a small model that reads each..."
tags:
  - "clippings"
---
Model routers are everywhere right now, but they have a fundamental limitation. No matter if based on advanced heuristics or a small model that reads each turn and picks which LLM to use, a router will always be less capable than the model it’s choosing for. Replit Agent lets the model decide instead.

The main agent, or core loop, chooses its subagents’ tier and effort, and adjusts its own as the task unfolds. Given that freedom, GPT-6 Astra hands routine implementation to less costly subagents and decides for itself where its tokens are worth spending. On both DeepSWE and Terminal-Bench, Replit Agent is Pareto-efficient against Astra on its own: no published Astra baseline costs less and scores higher. It also beats a sidekick architecture, the same setup with one long-lived worker, by 11 and 16 points.

## Why we scaffold less

Every model release invalidates assumptions baked into the harness.

As models become stronger at long-horizon tasks, they don’t need as much scaffolding at the harness layer. In practice, we’ve observed them lean more towards delegation on their own: using subagents for context management and parallelism. Recent breakthroughs, Navier–Stokes among them, came in part from coordinating swarms of agents powered by frontier models [\[1\]](https://openai.com/index/navier-stokes-solution/).

But the frontier is jagged. The strongest coding model is not necessarily the strongest at designing UIs or making slides, nor the best at writing emails.

Coding agents write in a compressed, jargon-heavy register nicknamed “Claudish”; each frontier model’s prose is distinct enough to identify from text alone [\[7\]](https://arxiv.org/abs/2502.12150).

So we design our harness to let each model work its own way, with the guardrails it still needs and quality at minimum cost as the goal.

Each new model sends us back to re-test what we held firmly, and to experiment *fast* with techniques that build on emergent behaviors. Freeing the model, then, means letting it decide how hard to think, when to hand work off, and who to hand it to.

### Freeing the model

The harness offers the options and keeps the guardrails; at every step, the core loop decides.

#### 1How hard to think

<svg viewBox="0 0 200 110" role="img" aria-label="An effort scale from low to max with high selected, and an arrow showing it can move either way mid-turn" style="font-size:10.5px"><line x1="44" x2="156" y1="40" y2="40" stroke="currentColor" stroke-opacity="0.2"></line><path d="M40,40 l7,-3.5 v7 z" fill="none"></path><path d="M160,40 l-7,-3.5 v7 z" fill="none"></path><text x="100" y="30" text-anchor="middle" style="font-size:10px" fill="currentColor">adjusted mid-turn</text> <line x1="22" x2="178" y1="66" y2="66" stroke="currentColor" stroke-opacity="0.2"></line><g><rect x="18" y="62" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="22" y="88" text-anchor="middle" style="font-size:10px" fill="currentColor">low</text></g> <g><rect x="57" y="62" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="61" y="88" text-anchor="middle" style="font-size:10px" fill="currentColor">med</text></g> <g><rect x="95" y="61" width="10" height="10" fill="none" stroke="currentColor"></rect><text x="100" y="88" text-anchor="middle" style="font-size:10px" fill="currentColor">high</text></g> <g><rect x="135" y="62" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="139" y="88" text-anchor="middle" style="font-size:10px" fill="currentColor">xhigh</text></g> <g><rect x="174" y="62" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="178" y="88" text-anchor="middle" style="font-size:10px" fill="currentColor">max</text></g></svg>

Effort is set step by step and, on the latest models, changes mid-turn without a cache miss.

#### 2When to hand work off

<svg viewBox="0 0 200 110" role="img" aria-label="A core loop line that works on its own, briefs two subagents at once, takes their replies, and continues" style="font-size:10.5px"><line x1="50" x2="50" y1="6" y2="104" stroke="currentColor" stroke-opacity="0.2"></line><rect x="46" y="18" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="62" y="26" style="font-size:10.5px" fill="currentColor">does it itself</text> <g><line x1="54" x2="113" y1="44" y2="44" stroke="currentColor" stroke-opacity="0.2"></line><path d="M119,44 l-6,-3.5 v7 z" fill="none"></path><line x1="120" x2="120" y1="44" y2="78" stroke="currentColor" stroke-opacity="0.2"></line><line x1="120" x2="61" y1="78" y2="78" stroke="currentColor" stroke-opacity="0.2"></line></g><g><line x1="54" x2="163" y1="44" y2="44" stroke="currentColor" stroke-opacity="0.2"></line><path d="M169,44 l-6,-3.5 v7 z" fill="none"></path><line x1="170" x2="170" y1="44" y2="78" stroke="currentColor" stroke-opacity="0.2"></line><line x1="170" x2="61" y1="78" y2="78" stroke="currentColor" stroke-opacity="0.2"></line></g><path d="M55,78 l6,-3.5 v7 z" fill="none"></path><rect x="46" y="40" width="8" height="8" fill="none" stroke="currentColor"></rect><rect x="46" y="74" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="196" y="96" text-anchor="end" style="font-size:10.5px" fill="currentColor">or hands off, two at once</text></svg>

Hand-offs buy context management and parallelism; a small task spawns nothing at all.

#### 3Who to hand it to

<svg viewBox="0 0 200 110" role="img" aria-label="Four kinds of work against three frontier models, with a different model strongest at each, joined by a jagged line" style="font-size:10.5px"><text x="112" y="12" text-anchor="middle" style="font-size:10px" fill="currentColor">A</text> <text x="146" y="12" text-anchor="middle" style="font-size:10px" fill="currentColor">B</text> <text x="180" y="12" text-anchor="middle" style="font-size:10px" fill="currentColor">C</text> <polyline points="112,30 180,52 146,74 180,96" stroke="currentColor" stroke-opacity="0.2"></polyline><g><text x="92" y="34" text-anchor="end" style="font-size:10.5px" fill="currentColor">coding</text> <rect x="107" y="25" width="10" height="10" fill="none" stroke="currentColor"></rect><rect x="142" y="26" width="8" height="8" fill="none" stroke="currentColor"></rect><rect x="176" y="26" width="8" height="8" fill="none" stroke="currentColor"></rect></g><g><text x="92" y="56" text-anchor="end" style="font-size:10.5px" fill="currentColor">UI design</text> <rect x="108" y="48" width="8" height="8" fill="none" stroke="currentColor"></rect><rect x="142" y="48" width="8" height="8" fill="none" stroke="currentColor"></rect><rect x="175" y="47" width="10" height="10" fill="none" stroke="currentColor"></rect></g><g><text x="92" y="78" text-anchor="end" style="font-size:10.5px" fill="currentColor">slides</text> <rect x="108" y="70" width="8" height="8" fill="none" stroke="currentColor"></rect><rect x="141" y="69" width="10" height="10" fill="none" stroke="currentColor"></rect><rect x="176" y="70" width="8" height="8" fill="none" stroke="currentColor"></rect></g><g><text x="92" y="100" text-anchor="end" style="font-size:10.5px" fill="currentColor">writing</text><rect x="108" y="92" width="8" height="8" fill="none" stroke="currentColor"></rect><rect x="142" y="92" width="8" height="8" fill="none" stroke="currentColor"></rect><rect x="175" y="91" width="10" height="10" fill="none" stroke="currentColor"></rect></g></svg>

The frontier is jagged, so each specialist runs on the model strongest at its job.

Figure 1: Freeing the model: the three decisions the core loop makes at every step.

## Composable primitives for delegation

When we started experimenting with GPT-6 Astra [\[2\]](https://openai.com/index/gpt-6-astra), we found that the model delegates well. The GPT-6 family is also the first from OpenAI to support effort changes mid-turn without breaking the cache.

To use these capabilities, we refined four harness primitives. They give the core loop a small set of choices at each step: what kind of subagent to dispatch, at what size and effort, whether to return to one it has already briefed, and how hard to think:

- **Domain-aware subagents.** Alongside a general worker, the harness offers specialists: read-only explorers, browser testers, reviewers, and a design subagent for slides and UI,
	As of September 2026, Replit Design leads the Builders leaderboard on Design Arena [\[8\]](https://www.designarena.ai/leaderboard?tab=builders).
	each with its own model and tooling. For now, the harness still decides which specialists exist; the core loop decides when and how to use them.
- **Subagent tiers and effort.** Small, standard, and large, each a step up in cost and capability, and an effort level within the tier. Both apply to every subagent, and the core loop picks them at each dispatch. For example, a mechanical rename goes to small at low effort, while generating hypotheses for a stubborn bug goes to large at high effort.
- **Reusable subagents.** The core loop can return to a subagent it has already briefed instead of starting over. There is no single sidekick kept alive for the session: any number of subagents stay warm across kinds and tiers, and it picks which to wake. A longer cache lifetime on OpenAI’s newer models keeps the cost of doing so down.
- **Dynamic effort tuning.** Now that changing effort mid-turn preserves the cache on some models
	Effort changes preserve cache on the GPT-6 family [\[2\]](https://openai.com/index/gpt-6-astra), Fable 5.1 [\[3\]](https://www.anthropic.com/claude-fable-and-mythos-5-1), and these providers’ models released since. Elsewhere, effort changes and model switches rebuild the cache.
	, we trained an escalation system that checks the trajectory at each step and matches effort to task difficulty. Unlike a router, it acts mid-turn on the work in progress, not once on the request.

The code quality of Astra and Fable 5.1 [\[3\]](https://www.anthropic.com/claude-fable-and-mythos-5-1) also let us use our code-review subagent less, with no drop in our eval scores. We’ve not seen this level of engineering quality from any model before.

### Newer models delegate on their own

Frontier models like Astra and Fable cost more per token, which makes them look uneconomical next to smaller ones. We’ve observed them naturally delegate to less costly subagents, keeping their own tokens for the decisions that need them.

Replit Agent never forces the core loop to spawn subagents. Table 1

Replit Agent production, one week per model: Fable 5 in August 2026, Fable 5.1 and Astra in September.

shows how three models handle that decision in production:

|  | Fable 5 | Fable 5.1 | GPT-6 Astra |
| --- | --- | --- | --- |
| Turns that dispatch a subagent | 32% | 21% | 36% |
| Turns that hand work to a general worker | 0.9% | 2.3% | 20% |
| Dispatches that return to an existing subagent | 17% | 29% | 42% |

Table 1: Delegation in Replit Agent production, each model at medium reasoning effort.

All three models delegate, but each in its own way. At medium effort, Fable models rarely hand work to a general worker: they send out read-only explorers and reviewers and keep the implementation for themselves. Astra is the first model we’ve seen routinely delegate to general workers without being told to, and once it has briefed one it tends to go back to it rather than start over. This return rate has risen with every model generation.

When I add a service from a vendor's page, it never brings me back to the vendor. Can we fix this?

Agent

Explorer

Worker A

Worker B

Tester

0:00

Confirms the plan

find where it drops

Reads the flagged files

Scans the save flow

Reads the handler

found the handler

fix the return path

update the spec

Tags vendor links

Drafts the spec

Adds a return helper

spec drafted; needs evidence

Runs the suite

23 pass; type errors

1:43

which are real?

none; stale types

Rebuilds stale types

Restarts the app

run the journey

Figure 2: A production turn on September 17, 2026, drawn from the trace. The core loop dispatched an explorer, two workers, and a tester; of its five worker dispatches, three were returns to a worker it had already briefed.

## Results

We evaluated Replit Agent in Max mode, our highest-quality setting with Astra as the core loop, on two software engineering benchmarks: DeepSWE and Terminal-Bench.

Our runs are means of four repetitions; whiskers are 95% intervals, mean ± 1.96 SE, as on the DeepSWE leaderboard [\[4\]](https://deepswe.datacurve.ai/). Astra’s figures are the published mini-swe-agent baselines [\[4\]](https://deepswe.datacurve.ai/) [\[9\]](https://artificialanalysis.ai/evaluations/terminalbench-4-0), with intervals where the leaderboard reports them.

We compare against two baselines: Astra on its own in mini-swe-agent, as published on each leaderboard, and a sidekick architecture, the same configuration with one change: its subagent primitives replaced by a single long-lived worker. Each chart plots score against cost per task, so the most efficient configurations sit toward the top left.

On **DeepSWE v1.1** [\[4\]](https://deepswe.datacurve.ai/), which tests long-horizon changes to active open-source repositories, Replit Agent scores 72% at $2.11 per task. Astra in mini-swe-agent at low effort scores 67% at $1.60, and at xhigh effort 74% at $4.43; the sidekick architecture scores 61% at $1.34. **Terminal-Bench 4.0** [\[5\]](https://www.tbench.ai/) tests multi-step work done entirely from a shell.

Three GPU tasks are excluded from our runs.

Replit Agent reaches 49% at $2.53 per task, against 42% at $2.25 for Astra at low effort and 60% at $5.86 at xhigh. The sidekick architecture manages 33% at $1.84.

### DeepSWE: score against cost per task

Mean of 4 repetitions over 113 tasks. GPT-6 Astra alone in mini-swe-agent, public v1.1 leaderboard.

<svg viewBox="0 0 640 300" role="img" aria-label="DeepSWE: score against cost per task" style="font-size:11.5px"><g><line x1="48" x2="616" y1="256" y2="256" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="256" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">50%</text></g> <g><line x1="48" x2="616" y1="177.33333333333334" y2="177.33333333333334" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="177.33333333333334" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">60%</text></g> <g><line x1="48" x2="616" y1="98.66666666666667" y2="98.66666666666667" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="98.66666666666667" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">70%</text></g> <g><line x1="48" x2="616" y1="20" y2="20" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="20" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">80%</text></g> <polyline points="138.88,122.26666666666667 222.944,75.06666666666666 270.656,75.06666666666666 299.62399999999997,67.19999999999999 474,75.06666666666666" stroke="currentColor" stroke-opacity="0.2"></polyline><text x="48" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$0</text> <text x="161.60000000000002" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$2</text> <text x="275.20000000000005" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$4</text> <text x="388.8" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$6</text> <text x="502.40000000000003" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$8</text> <text x="616" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$10</text> <line x1="48" x2="616" y1="256" y2="256" stroke="currentColor" stroke-opacity="0.2"></line><text x="332" y="294" text-anchor="middle" style="font-size:11px" fill="currentColor">Cost per task</text> <text transform="translate(14 138) rotate(-90)" text-anchor="middle" style="font-size:11px" fill="currentColor">Score</text> <g><g><line x1="138.88" x2="138.88" y1="114.4" y2="130.13333333333333"></line><line x1="135.88" x2="141.88" y1="114.4" y2="114.4"></line><line x1="135.88" x2="141.88" y1="130.13333333333333" y2="130.13333333333333"></line></g><rect x="134.88" y="118.26666666666667" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="146.88" y="122.26666666666667" text-anchor="start" dy="4" style="font-size:10px" fill="currentColor">low</text> <rect x="129.88" y="113.26666666666667" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (low): 67.0% score, $1.60 per task, 95% interval 66.0% to 68.0%, as published" fill="transparent"></rect></g><g><g><line x1="222.944" x2="222.944" y1="51.46666666666666" y2="98.66666666666667"></line><line x1="219.944" x2="225.944" y1="51.46666666666666" y2="51.46666666666666"></line><line x1="219.944" x2="225.944" y1="98.66666666666667" y2="98.66666666666667"></line></g><rect x="218.944" y="71.06666666666666" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="214.944" y="75.06666666666666" text-anchor="end" dy="4" style="font-size:10px" fill="currentColor">med</text> <rect x="213.944" y="66.06666666666666" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (medium): 73.0% score, $3.08 per task, 95% interval 70.0% to 76.0%, as published" fill="transparent"></rect></g><g><g><line x1="270.656" x2="270.656" y1="51.46666666666666" y2="98.66666666666667"></line><line x1="267.656" x2="273.656" y1="51.46666666666666" y2="51.46666666666666"></line><line x1="267.656" x2="273.656" y1="98.66666666666667" y2="98.66666666666667"></line></g><rect x="266.656" y="71.06666666666666" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="262.656" y="75.06666666666666" text-anchor="end" dy="4" style="font-size:10px" fill="currentColor">high</text> <rect x="261.656" y="66.06666666666666" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (high): 73.0% score, $3.92 per task, 95% interval 70.0% to 76.0%, as published" fill="transparent"></rect></g><g><g><line x1="299.62399999999997" x2="299.62399999999997" y1="43.599999999999994" y2="90.80000000000001"></line><line x1="296.62399999999997" x2="302.62399999999997" y1="43.599999999999994" y2="43.599999999999994"></line><line x1="296.62399999999997" x2="302.62399999999997" y1="90.80000000000001" y2="90.80000000000001"></line></g><rect x="295.62399999999997" y="63.19999999999999" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="307.62399999999997" y="67.19999999999999" text-anchor="start" dy="4" style="font-size:10px" fill="currentColor">xhigh</text> <rect x="290.62399999999997" y="58.19999999999999" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (xhigh): 74.0% score, $4.43 per task, 95% interval 71.0% to 77.0%, as published" fill="transparent"></rect></g><g><g><line x1="474" x2="474" y1="67.19999999999999" y2="82.93333333333334"></line><line x1="471" x2="477" y1="67.19999999999999" y2="67.19999999999999"></line><line x1="471" x2="477" y1="82.93333333333334" y2="82.93333333333334"></line></g><rect x="470" y="71.06666666666666" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="474" y="59.19999999999999" text-anchor="middle" dy="0" style="font-size:10px" fill="currentColor">max</text> <rect x="465" y="66.06666666666666" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (max): 73.0% score, $7.50 per task, 95% interval 72.0% to 74.0%, as published" fill="transparent"></rect></g><text x="484" y="75.06666666666666" text-anchor="start" dy="4" style="font-weight:500" fill="currentColor">GPT-6 Astra</text> <g><g><line x1="167.848" x2="167.848" y1="67.8720226112329" y2="103.10797738876714"></line><line x1="164.848" x2="170.848" y1="67.8720226112329" y2="67.8720226112329"></line><line x1="164.848" x2="170.848" y1="103.10797738876714" y2="103.10797738876714"></line></g><rect x="162.848" y="80.29333333333332" width="10" height="10" fill="none" stroke="currentColor"></rect><text x="156.848" y="85.29333333333332" text-anchor="end" dy="4" style="font-weight:500" fill="currentColor">Replit Agent</text> <rect x="158.848" y="76.29333333333332" width="18" height="18" tabindex="0" aria-label="Replit Agent: 71.7% score, $2.11 per task, 95% interval 69.4% to 73.9%" fill="transparent"></rect></g><g><g><line x1="124.11200000000001" x2="124.11200000000001" y1="159.7285177826623" y2="185.49814888400445"></line><line x1="121.11200000000001" x2="127.11200000000001" y1="159.7285177826623" y2="159.7285177826623"></line><line x1="121.11200000000001" x2="127.11200000000001" y1="185.49814888400445" y2="185.49814888400445"></line></g><rect x="119.11200000000001" y="167.61333333333332" width="10" height="10" fill="none" stroke="currentColor"></rect><text x="135.11200000000002" y="172.61333333333332" text-anchor="start" dy="4" style="font-weight:500" fill="currentColor">Sidekick architecture</text><rect x="115.11200000000001" y="163.61333333333332" width="18" height="18" tabindex="0" aria-label="Sidekick architecture: 60.6% score, $1.34 per task, 95% interval 59.0% to 62.2%" fill="transparent"></rect></g></svg>

### Terminal-Bench 4.0: score against cost per task

Mean of 4 repetitions over 63 tasks, GPU tasks excluded. GPT-6 Astra alone in mini-swe-agent, Artificial Analysis leaderboard.

<svg viewBox="0 0 640 300" role="img" aria-label="Terminal-Bench 4.0: score against cost per task" style="font-size:11.5px"><g><line x1="48" x2="616" y1="256" y2="256" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="256" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">20%</text></g> <g><line x1="48" x2="616" y1="208.8" y2="208.8" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="208.8" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">30%</text></g> <g><line x1="48" x2="616" y1="161.6" y2="161.6" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="161.6" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">40%</text></g> <g><line x1="48" x2="616" y1="114.4" y2="114.4" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="114.4" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">50%</text></g> <g><line x1="48" x2="616" y1="67.19999999999999" y2="67.19999999999999" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="67.19999999999999" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">60%</text></g> <g><line x1="48" x2="616" y1="20" y2="20" stroke="currentColor" stroke-opacity="0.2"></line><text x="40" y="20" dy="4" text-anchor="end" style="font-size:10.5px" fill="currentColor">70%</text></g> <polyline points="175.8,152.632 278.03999999999996,95.51999999999998 299.62399999999997,116.76 380.84800000000007,69.088 530.8,71.448" stroke="currentColor" stroke-opacity="0.2"></polyline><text x="48" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$0</text> <text x="161.60000000000002" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$2</text> <text x="275.20000000000005" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$4</text> <text x="388.8" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$6</text> <text x="502.40000000000003" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$8</text> <text x="616" y="272" text-anchor="middle" style="font-size:10.5px" fill="currentColor">$10</text> <line x1="48" x2="616" y1="256" y2="256" stroke="currentColor" stroke-opacity="0.2"></line><text x="332" y="294" text-anchor="middle" style="font-size:11px" fill="currentColor">Cost per task</text> <text transform="translate(14 138) rotate(-90)" text-anchor="middle" style="font-size:11px" fill="currentColor">Score</text> <g><rect x="171.8" y="148.632" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="183.8" y="152.632" text-anchor="start" dy="4" style="font-size:10px" fill="currentColor">low</text> <rect x="166.8" y="143.632" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (low): 41.9% score, $2.25 per task" fill="transparent"></rect></g><g><rect x="274.03999999999996" y="91.51999999999998" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="286.03999999999996" y="95.51999999999998" text-anchor="start" dy="4" style="font-size:10px" fill="currentColor">high</text> <rect x="269.03999999999996" y="86.51999999999998" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (high): 54.0% score, $4.05 per task" fill="transparent"></rect></g><g><rect x="295.62399999999997" y="112.76" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="307.62399999999997" y="116.76" text-anchor="start" dy="4" style="font-size:10px" fill="currentColor">med</text> <rect x="290.62399999999997" y="107.76" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (medium): 49.5% score, $4.43 per task" fill="transparent"></rect></g><g><rect x="376.84800000000007" y="65.088" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="388.84800000000007" y="69.088" text-anchor="start" dy="4" style="font-size:10px" fill="currentColor">xhigh</text> <rect x="371.84800000000007" y="60.087999999999994" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (xhigh): 59.6% score, $5.86 per task" fill="transparent"></rect></g><g><rect x="526.8" y="67.448" width="8" height="8" fill="none" stroke="currentColor"></rect><text x="530.8" y="63.44799999999999" text-anchor="middle" dy="0" style="font-size:10px" fill="currentColor">max</text> <rect x="521.8" y="62.44799999999999" width="18" height="18" tabindex="0" aria-label="GPT-6 Astra (max): 59.1% score, $8.50 per task" fill="transparent"></rect></g><text x="540.8" y="71.448" text-anchor="start" dy="4" style="font-weight:500" fill="currentColor">GPT-6 Astra</text> <g><g><line x1="191.704" x2="191.704" y1="96.26087243369395" y2="140.091127566306"></line><line x1="188.704" x2="194.704" y1="96.26087243369395" y2="96.26087243369395"></line><line x1="188.704" x2="194.704" y1="140.091127566306" y2="140.091127566306"></line></g><rect x="186.704" y="113.17599999999999" width="10" height="10" fill="none" stroke="currentColor"></rect><text x="180.704" y="118.17599999999999" text-anchor="end" dy="4" style="font-weight:500" fill="currentColor">Replit Agent</text> <rect x="182.704" y="109.17599999999999" width="18" height="18" tabindex="0" aria-label="Replit Agent: 49.2% score, $2.53 per task, 95% interval 44.6% to 53.8%" fill="transparent"></rect></g><g><g><line x1="152.512" x2="152.512" y1="178.54005002985474" y2="215.45994997014526"></line><line x1="149.512" x2="155.512" y1="178.54005002985474" y2="178.54005002985474"></line><line x1="149.512" x2="155.512" y1="215.45994997014526" y2="215.45994997014526"></line></g><rect x="147.512" y="192" width="10" height="10" fill="none" stroke="currentColor"></rect><text x="163.512" y="197" text-anchor="start" dy="4" style="font-weight:500" fill="currentColor">Sidekick architecture</text><rect x="143.512" y="188" width="18" height="18" tabindex="0" aria-label="Sidekick architecture: 32.5% score, $1.84 per task, 95% interval 28.6% to 36.4%" fill="transparent"></rect></g></svg>

Replit Agent beats the sidekick architecture on both benchmarks, by 11 and 16 points. The sidekick costs less, and gives up a sixth to a third of the score for it. Astra on its own scores higher only by spending more: its best settings sit 2 and 11 points above Replit Agent at more than twice the cost. Neither baseline wins on both cost and score. We ran Replit Agent exactly as it ships to users, with no changes to the prompting or harness.

## The bitter lesson of harness design

We read these results as an instance of Sutton’s bitter lesson [\[6\]](http://www.incompleteideas.net/IncIdeas/BitterLesson.html). Baking human knowledge into an agent helps in the short term, plateaus in the long run, and is eventually overtaken by general methods that scale with computation. A rigid harness forces the model into one way of working; a composable one lets it choose. The smarter models get, the less the harness should decide for them.

Compared with a more prescribed architecture, this approach buys us three things:

- **It bets on model scaling laws.** Delegation that relies on the taste of the model improves with every release. Early previews of next-generation models continue the trend.
- **It fits the task.** The model spawns nothing for a small task, one explorer for a search, and a team when a build breaks into independent pieces.
- **It reuses without persisting.** A subagent keeps its context in case the model wants it back, and nothing persists unless it does.

In Sutton’s terms, the harness should let the model discover how to execute the work, not prescribe how we would have done it. Free the models.

## Acknowledgements

Written by Daniel Furman, Jacky Zhao, Vaibhav Kumar, Ed Sioufi, and Michele Catasta. Thanks to James Austin, Toby Ho, Preeya Kirani, Zhen Li, Robin Newhouse, Devanshu Sen Pandey, Ibrahim Sheikh, Samuel Spitz, Peter Zhong, and the rest of the AI team at Replit for their contributions to this work. If you want to work on Replit Agent, our team is hiring; reach out to [pirroh@repl.it](mailto:pirroh@repl.it).

## References

1. [On the Navier–Stokes Millennium Prize Problem](https://openai.com/index/navier-stokes-solution/)
2. [Introducing GPT-6 Astra](https://openai.com/index/gpt-6-astra)
3. [Introducing Claude Fable 5.1 and Claude Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)
4. [DeepSWE v1.1](https://deepswe.datacurve.ai/)
5. [Terminal-Bench 4.0](https://www.tbench.ai/)
6. [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)
7. [Idiosyncrasies in Large Language Models](https://arxiv.org/abs/2502.12150)
8. [Design Arena](https://www.designarena.ai/leaderboard?tab=builders)
9. [Terminal-Bench 4.0 results, Artificial Analysis](https://artificialanalysis.ai/evaluations/terminalbench-4-0)

### Footnotes

1. [1](#1c4422762960-ref)
	Coding agents write in a compressed, jargon-heavy register nicknamed “Claudish”; each frontier model’s prose is distinct enough to identify from text alone [\[7\]](https://arxiv.org/abs/2502.12150).
2. [2](#fn_designarena-ref)
	As of September 2026, Replit Design leads the Builders leaderboard on Design Arena [\[8\]](https://www.designarena.ai/leaderboard?tab=builders).
3. [3](#3c3a641eacb3-ref)
	Effort changes preserve cache on the GPT-6 family [\[2\]](https://openai.com/index/gpt-6-astra), Fable 5.1 [\[3\]](https://www.anthropic.com/claude-fable-and-mythos-5-1), and these providers’ models released since. Elsewhere, effort changes and model switches rebuild the cache.
4. [4](#e9bd0580c72f-ref)
	Replit Agent production, one week per model: Fable 5 in August 2026, Fable 5.1 and Astra in September.
5. [5](#c9b7f8a519f3-ref)
	Our runs are means of four repetitions; whiskers are 95% intervals, mean ± 1.96 SE, as on the DeepSWE leaderboard [\[4\]](https://deepswe.datacurve.ai/). Astra’s figures are the published mini-swe-agent baselines [\[4\]](https://deepswe.datacurve.ai/) [\[9\]](https://artificialanalysis.ai/evaluations/terminalbench-4-0), with intervals where the leaderboard reports them.
6. [6](#fn_tbench_gpu-ref)
	Three GPU tasks are excluded from our runs.