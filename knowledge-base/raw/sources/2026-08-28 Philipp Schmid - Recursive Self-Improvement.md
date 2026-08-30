---
type: raw-source
source_id: src-2026-08-28-philipp-schmid-recursive-self-improvement
title: "Recursive Self-Improvement"
source: "https://www.philschmid.de/recursive-self-improvement?utm_source=substack&utm_medium=email"
author:
  - "[[Philipp Schmid]]"
published: 2026-08-21
created: 2026-08-28
description: "Agents can already edit their tools, skills, and harness. Recursive self-improvement still needs a system that can raise the verifier without capturing it."
tags:
  - "source/raw"
  - "clippings"
---
Earlier this week I [tweeted](https://x.com/_philschmid/status/2089987145020608740):

> The next iterations of agent harnesses will center on coded extensions that integrate automatically. Pi lead, others are following, and DeepSeek represents the extreme.
> 
> All powered and driven by autoresearch and recursive self-improvements.

For most of AI's history, recursive self-improvement belonged to theory and science fiction. I. J. Good described an ["intelligence explosion"](https://en.wikipedia.org/wiki/Technological_singularity#Intelligence_explosion) in 1965: a machine designs a better machine, which becomes better at designing the next one. The curve goes vertical.

We are surprisingly close to a narrow version of that loop. Agents can inspect failed runs, edit their tools and instructions, test the result, and keep what works. They are also beginning to run experiments that produce better models. The results are scrappy, but the pieces are starting to connect.

## What is recursive self-improvement?

Retrying a failed task is easy to mistake for learning. I use the following definition:

> Recursive self-improvement is a loop in which a system makes a persistent change that improves its future performance and its ability to produce subsequent improvements.

What a run leaves behind

### Iteration

Edit code, rerun the test.

Outputchanges

Systemfixed

Verifierfixed

The next task starts from the same agent.

### Self-improvement

Add a tool, record a skill.

Outputchanges

Systemchanges

Verifierfixed

Future tasks run through a different system.

### Recursive self-improvement

Raise the bar itself.

Outputchanges

Systemchanges

Verifierrises

Later rounds face a harder, still-honest test.

Each loop is defined by which layer persists after the run — and green marks what the loop is allowed to move.

**Iteration** improves an output while the system stays the same. An agent edits code, reruns a test, and the next task still starts with the same agent.

**Self-improvement** changes the system persistently. The agent adds a tool, records a skill, or changes how it compacts long conversations. Future tasks run through a different system. The ruler that says "better" does not move.

**Recursive self-improvement** also raises that ruler. The system gets better at judging, not only at scoring. Later rounds face a harder test that is still independent of the agent.

Current systems work best when an external evaluator stays fixed. A test passes, validation loss drops, or a benchmark score rises. The system can search because it has a ruler it doesn't control. A [recent survey](https://arxiv.org/abs/2607.07663) shows that agents can edit a prompt, tool, skill, or piece of harness code, but they can't redefine success.

Open-ended recursive self-improvement asks for more. The system would improve how it finds changes and how those changes are judged. It would strengthen the verifier without being able to game it. Public evidence for that remains thin.

A higher task score shows improvement. Recursion needs another measurement: did the next round face a harder bar that the system still could not cheat?

The missing half of the loop

### Today: bounded

Agent can edit

EditTestKeep

Evaluator

fixed · outside the loop

The agent can search because it is scored by a ruler it doesn't control.

### Missing: raise the bar

Agent can edit

EditTestKeep

raises the bar

Harder tests

stricter · still not gameable

The system strengthens the evaluator, and later rounds are judged against a signal it still cannot capture.

## Self-improving models

Models have long improved through their own outputs, [self-play](https://www.nature.com/articles/nature24270), [student-teacher training](https://arxiv.org/abs/1911.04252), or [successful reasoning traces](https://arxiv.org/abs/2203.14465). Later work lets a model [score its own training preferences](https://arxiv.org/abs/2401.10020) or [propose synthetic data and update directives](https://arxiv.org/abs/2506.10943). But researchers still set the objective, the update rule, and the tests. The model's output feeds the loop. The loop itself stays fixed.

Agents are now improving the code around that loop. [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) is the simple version. An agent propose a change, trains for a few minutes, keep it only if validation loss drops. On nanochat it ran about 700 experiments, found about 20 that transferred, and cut time-to-GPT-2 quality from 2.02 to 1.80 hours. Prime Intellect [scaled the same loop](https://www.primeintellect.ai/auto-nanogpt) to 10,000 trials and beat the human baseline.

Autoresearch

<svg viewBox="0 0 560 128" aria-hidden="true"><defs><marker id="rsi-auto-arrow" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1 6.5 4l-5 3" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></marker></defs><g><line x1="152" y1="33" x2="219" y2="33" stroke="currentColor" stroke-width="1.25" marker-end="url(#rsi-auto-arrow)"></line><line x1="337" y1="33" x2="404" y2="33" stroke="currentColor" stroke-width="1.25" marker-end="url(#rsi-auto-arrow)"></line><path d="M465 50v38a8 8 0 0 1-8 8H103a8 8 0 0 1-8-8V60" fill="none" stroke="currentColor" stroke-width="1.25" marker-end="url(#rsi-auto-arrow)"></path></g><g><rect x="40" y="16" width="110" height="34" rx="7" fill="Canvas" stroke="#ccc"></rect><text x="95" y="37.5" text-anchor="middle" font-size="12.5" font-weight="500" fill="currentColor">Propose</text> <rect x="225" y="16" width="110" height="34" rx="7" fill="Canvas" stroke="#ccc"></rect><text x="280" y="37.5" text-anchor="middle" font-size="12.5" font-weight="500" fill="currentColor">Train</text> <rect x="410" y="16" width="110" height="34" rx="7" fill="#888" stroke="#ccc"></rect><g transform="translate(441 26.5) scale(0.55)" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></g><text x="474" y="37.5" text-anchor="middle" font-size="12.5" font-weight="500" fill="currentColor">Eval</text></g> <g><rect x="278" y="84" width="154" height="24" rx="12" fill="Canvas" stroke="currentColor" stroke-opacity="0.4"></rect><text x="355" y="99.5" text-anchor="middle" font-size="10.5" font-weight="500" fill="currentColor">keep · metric improved</text></g> <g><rect x="122" y="84" width="112" height="24" rx="12" fill="Canvas" stroke="#ccc" stroke-dasharray="3 3"></rect><text x="178" y="99.5" text-anchor="middle" font-size="10.5" fill="#888">revert otherwise</text></g></svg>

~700

experiments, one GPU (nanochat)

~20

changes kept and transferred

2.02 → 1.80 h

time to GPT-2 quality

Prime Intellect scaled the same keep-or-revert loop to ~10,000 trials on H200s and beat the human baseline.

[AlphaEvolve](https://arxiv.org/abs/2506.13131) is the same idea aimed at algorithms. It mutates programs, scores them against an automatic evaluator, and keeps the winners. It found a way to multiply 4×4 complex matrices in 48 scalar multiplications, one fewer than Strassen's 49, and sped up a kernel used to train Gemini by 23%. A model improving the code that trains the model is the recursive loop in a single sentence.

Newer experiments connect both. [SIA](https://arxiv.org/abs/2605.27276) updates both a task agent's harness and its weights. [Recursive Harness Self-Improvement](https://arxiv.org/abs/2607.15524) edits a harness partly to produce better traces for training future models, and calls the result model–harness co-evolution.

Model–harness co-evolution

<svg viewBox="0 0 560 168" aria-hidden="true"><defs><marker id="rsi-coevo-arrow" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1.5 1 6.5 4l-5 3" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"></path></marker></defs><g><path d="M197 58C242 22 278 22 323 58" fill="none" stroke="currentColor" stroke-width="1.25" marker-end="url(#rsi-coevo-arrow)"></path><path d="M323 110c-45 36-81 36-126 0" fill="none" stroke="currentColor" stroke-width="1.25" marker-end="url(#rsi-coevo-arrow)"></path></g><text x="260" y="20" text-anchor="middle" font-size="11" fill="#888">better harness edits</text> <text x="260" y="156" text-anchor="middle" font-size="11" fill="#888">cleaner traces for the next model</text> <g><rect x="20" y="62" width="170" height="44" rx="8" fill="Canvas" stroke="#ccc"></rect><text x="105" y="81" text-anchor="middle" font-size="13" font-weight="600" fill="currentColor">Model</text> <text x="105" y="96" text-anchor="middle" font-size="10.5" fill="#888">weights</text> <rect x="370" y="62" width="170" height="44" rx="8" fill="Canvas" stroke="#ccc"></rect><text x="455" y="81" text-anchor="middle" font-size="13" font-weight="600" fill="currentColor">Harness</text> <text x="455" y="96" text-anchor="middle" font-size="10.5" fill="#888">the code around it</text></g></svg>

**Recursive self-improvement doesn't require a better model.** A frozen model with an honest verifier and a writable environment can climb on its own. The easier target is the [harness](https://www.philschmid.de/agent-harness-2026) around it.

## Agents editing their own harness

The idea is simple. Run a baseline, inspect the failures, change one part, and test again. Cline was able to [hill climb Opus 4.5 from 47% to 57%](https://cline.bot/blog/a-practical-guide-to-hill-climbing) in Terminal Bench manually and a few months later, an agent ran [the same method](https://cline.bot/blog/recursive-self-improvement-for-coding-agents) for 17 hours and about `$50` of compute. It moved Kimi K3 from 69 of 89 tasks to 79, with better retries, loop detection, and process handling.

Those improvements fall under bounded self-improvement. The agent changed its environment and kept the changes. The report does not show whether the updated system became better at finding its next change.

[HarnessOpt-Bench](https://arxiv.org/abs/2608.06301) asks whether such gains survive a stronger test. An agent edits its harness on development feedback; a separate system tests the candidate on hidden tasks. Across 111 runs, 5 optimizer models, and 4 tasks, results varied sharply by model and task. The benchmark measures whether an edit improves scores. RSI needs a second measure: whether later rounds face a harder bar the system still cannot cheat.

Measurement gap

### What we measure

<svg viewBox="0 0 240 126" aria-hidden="true"><g stroke="currentColor" stroke-opacity="0.07"><line x1="32" y1="44" x2="226" y2="44"></line><line x1="32" y1="73" x2="226" y2="73"></line></g><g stroke="currentColor" stroke-opacity="0.25" stroke-width="1"><line x1="32" y1="14" x2="32" y2="102"></line><line x1="32" y1="102" x2="226" y2="102"></line></g><g><path d="M36 94C90 84 130 68 218 26L218 102L36 102Z" fill="currentColor" fill-opacity="0.07" stroke="none"></path><path d="M36 94C90 84 130 68 218 26" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"></path><circle cx="218" cy="26" r="3" fill="currentColor" stroke="Canvas" stroke-width="1.5"></circle></g><text x="226" y="117" text-anchor="end" font-size="9.5" fill="#888">rounds →</text></svg>

Task score, rising over rounds.

### What recursion requires

<svg viewBox="0 0 240 126" aria-hidden="true"><g stroke="currentColor" stroke-opacity="0.07"><line x1="32" y1="44" x2="226" y2="44"></line><line x1="32" y1="73" x2="226" y2="73"></line></g><g stroke="currentColor" stroke-opacity="0.25" stroke-width="1"><line x1="32" y1="14" x2="32" y2="102"></line><line x1="32" y1="102" x2="226" y2="102"></line></g><path d="M36 94H84V76h48V58h48V40h38" fill="none" stroke="#888" stroke-width="1.25" stroke-dasharray="4 3.5" stroke-linecap="round" stroke-linejoin="round"></path><text x="223" y="33" text-anchor="middle" font-size="14" font-weight="600" fill="currentColor">?</text><text x="226" y="117" text-anchor="end" font-size="9.5" fill="#888">rounds →</text></svg>

Does the next round face a harder, still-honest bar?

A rising score proves self-improvement. Recursion is a claim about the other curve.

[PAST-Bench](https://arxiv.org/abs/2608.04003) asks whether stored experience actually helps later episodes. In many of its scenarios, turning memory on does not. A new [RSI Benchmark](https://rsi-benchmark.com/) proposes measuring AI systems doing AI research, which should show whether each round makes the next round faster or better.

So what should we count as recursion? [Hyperagents](https://arxiv.org/abs/2603.19461) comes close. The system can change an agent as well as the code that creates new agents, and improvements like better memory storage helped across later runs and tasks, but these are still bounded loops. The fitness function stayed outside the editable code.

Archive-based search

<svg viewBox="0 0 400 196" aria-hidden="true"><g font-size="9.5" fill="#888"><text x="8" y="34">gen 0</text> <text x="8" y="99">gen 1</text> <text x="8" y="164">gen 2</text></g> <g stroke="currentColor" stroke-opacity="0.3" stroke-width="1"><line x1="210" y1="37" x2="302" y2="88"></line><line x1="300" y1="103" x2="300" y2="152"></line></g><g stroke="currentColor" stroke-width="1.5"><line x1="210" y1="37" x2="122" y2="88"></line><line x1="120" y1="103" x2="120" y2="152"></line></g><circle cx="210" cy="30" r="4.5" fill="Canvas" stroke="currentColor" stroke-opacity="0.5"></circle><circle cx="300" cy="95" r="4.5" fill="Canvas" stroke="currentColor" stroke-opacity="0.5"></circle><circle cx="300" cy="160" r="4.5" fill="Canvas" stroke="currentColor" stroke-opacity="0.5"></circle><g><circle cx="120" cy="95" r="4.5" fill="Canvas" stroke="currentColor" stroke-width="1.5"></circle><circle cx="120" cy="160" r="5" fill="currentColor"></circle></g><g font-size="11" font-weight="500" fill="currentColor"><text x="222" y="34">62</text> <text x="132" y="99">58</text> <text x="312" y="99">71</text> <text x="312" y="164">73</text></g> <text x="134" y="164" font-size="11" font-weight="600">84</text> <text x="132" y="112" font-size="9.5" fill="#888">worse child</text> <text x="134" y="177" font-size="9.5" font-weight="500">best later agent</text></svg> Fitness function

Outside the tree. Every variant is scored by code no agent can edit.

Greedy selection would have pruned the 58. The archive kept it — and it parented the best agent.

## The agent takes control of its own setup

Early agents were a system prompt plus a handful of tools. We then added memory, compaction, hooks, skills, and control flow. Each addition made the harness more important and harder to change.

The next harness change will not be a bigger prompt. It is code the model can write, and that the runtime can load without a human rewriting the core. The harness will pick up the change without human intervention.

**Pi was first.** It ships 4 tools (`read`, `write`, `edit`, `bash`) and a system prompt under 1,000 tokens. Everything else is a TypeScript extension, auto-discovered from `.pi/extensions/`. An agent can write one, reload it, and continue with new tools. Others are following. [Amp](https://ampcode.com/manual/plugin-api) stores project plugins with the codebase.

**DeepSeek is the extreme.** [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) is built on the Cordis plugin kernel and treats almost every part as replaceable: models, tools, sessions, sandboxes, and the control loop itself. Plugin side effects unwind on unload, so the runtime can swap parts of itself without dying. Their shorthand is `Agent = Model + Harness`. An agent gets more code it can improve, and more ways to break compatibility or weaken a permission boundary.

Who can rewrite the harness

Fixed coreEverything is a plugin

### Conservative

Claude Code · Codex · Cursor

Skills, hooks, and plugins extend a fixed core.

### Pi

read · write · edit · bash

Four built-in tools; everything else is an extension the agent can write and reload.

### DeepSeek

deepseek-harness

Models, sandboxes, and the control loop itself are swappable plugins.

The green meter marks how much of the harness the agent can rewrite.

That shift matters for two reasons. The agent can build capabilities its developers didn't predict. And code can run a sequence of operations without filling the context window with every intermediate result. The same properties make failures persistent.

## The recursive part is still missing

An agent can overfit visible tasks, exploit bugs in the tests, or change a test so broken code passes. If it can edit evaluation, it can jailbreak itself. Reward hacking is the default behavior of a system asked to raise a number.

The agent and the system that verifies it have to stay apart for the moment. The agent may change prompts, skills, tools, memory, and harness code. A separate entity needs to own the evaluation. That's why are not at recursive self-improvement.

Recursive self-improvement needs the system to improve the verifier as well, harder tests, better judges, a higher bar. And it needs to do that without capturing the signal. Today the system does not know how to keep the verifier. Humans still set the objective and hide the real score.

Who owns the ruler

### Today: kept apart

Agent owns

promptsskillstoolsmemoryharness code

Humans own

held-out taskshidden score

If the agent can edit the evaluator, the score stops being evidence.

### What RSI needs

Agentraises the barVerifier · still hidden

The system strengthens the verifier without capturing it. No public system does this yet.

A [Princeton-led study](https://arxiv.org/abs/2608.13417) found that today's agents can execute much of the engineering of AI research while still struggling to choose original and useful directions. The loop is excellent at hill-climbing a verifiable metric. Taste is not a metric. Raising the bar without taste is a faster way to optimize the wrong thing.

These loops already deliver real things, faster training code, better tools, agents that fix their own retry logic overnight. What is still missing is the recursive part. Until the improver can raise the bar and still fail it, we are doing self-improvement. Not recursion.

## Three opinions loosely held

**The near future is local recursion.** Not a system redesigning its architecture in the dark. Agents writing the extensions the next session treats as native, and trajectories are used for training when they are good enough. Model–harness co-evolution is the least mystical description of where this is going. It is also the one the evidence supports.

**Verification is the bottleneck.** Every convincing result has a ruler the system does not own. The moment the system owns the ruler, it will get very good at looking improved. Bigger models will not fix that. A system that knows how to raise the bar, and keep it honest, might.

**Taste still lives outside the loop.** Agents will raise any number you give them. Recursive self-improvement without taste is a faster way to optimize the wrong thing. Deciding what counts as a win and that reward hacking does not is still our job.

Thanks for reading!