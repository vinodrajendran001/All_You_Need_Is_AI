---
type: concept
created: 2026-08-30
updated: 2026-10-09
tags:
  - concept
  - ai-agents
  - self-improvement
  - optimization
source_ids:
  - src-2026-07-16-lilian-weng-harness-engineering
  - src-2026-08-28-philipp-schmid-recursive-self-improvement
  - src-2026-08-30-adlrocha-base-models-bottleneck
  - src-2026-09-02-can-boluk-harness-playbook
  - src-2026-09-03-github-ai-coding-cost-efficient
  - src-2026-09-01-iusztin-scoped-subagents
  - src-2026-09-28-martin-automating-eval-design-hillclimbing
  - src-2026-09-30-replit-free-models-harness-design
  - src-2026-10-09-dickson-agent-stack-optimization
status: active
---

# Harness Optimization

## Definition

Harness optimization is the automated search for a better *harness* — the code, prompts, context
files, tools, workflows, and control logic surrounding a model — with the model's weights held fixed.
It treats the scaffolding as a search space rather than as configuration, and it asks a machine to
explore that space against a scored objective.

## Why it matters

If the model is frozen, everything left that determines agent behaviour lives in the harness. That
makes the harness the only surface most teams can actually optimize: it needs no training access, no
GPUs, and no model provider cooperation. It is also the surface an agent can modify *about itself*,
which is why this page is the mechanical core of [[Recursive Self-Improvement]].

## Current synthesis

### The optimization ladder

[[Lilian Weng - Harness Engineering for Self-Improvement]] supplies the organizing structure this
vault previously lacked: five rungs, ordered by how much of the system the optimizer may rewrite.

| Rung | What is optimized | Representative systems |
| --- | --- | --- |
| 1 | **Prompts** — instructions, few-shot examples | classic prompt optimization |
| 2 | **Structured context** — playbooks, memory, skills | ACE, MCE |
| 3 | **Workflow** — the graph of steps and roles | AFlow (MCTS over workflow graphs), ADAS |
| 4 | **Harness code** — the executable scaffolding | STOP, Self-Harness, AHE, Darwin Godel Machine |
| 5 | **Optimizer code** — the search procedure itself | Meta-Harness |

Each rung subsumes the ones below and enlarges the search space. Higher rungs promise more headroom
while making evaluation, credit attribution, and safety harder — a trade this page keeps returning to.

### Context optimization has to be itemized, not rewritten

ACE (Agentic Context Engineering) splits the work across a *generator*, a *reflector*, and a
*curator*, and stores the evolving playbook as **itemized bullets** that are added, edited, or retired
one at a time. The reason is a specific failure mode Weng names **context collapse**: when a whole
context document is regenerated each round by a model with a brevity bias, accumulated detail erodes
round after round until the playbook is shorter and worse than where it started. Itemization makes
each update local, attributable, and reversible. See [[Context Engineering]].

### The search only works if the base model is strong enough

This is the most important negative result on the page. **STOP improved when driven by GPT-4 but
degraded with GPT-3.5 and Mixtral.** The recursive structure contributes nothing on its own; the gain
comes from the proposer's ability to generate good candidates. Recursive scaffolding applied to a
weak model makes it worse.

### Harness-writing ability and harness-benefit scale differently

Weng cites Lin et al. for a finding that reshapes where harness investment pays off:

- **Harness-updating capability is roughly flat** from around 9B parameters to frontier models. Small
  models write skill files that are procedurally similar to those written by much larger ones.
- **Harness-benefit is non-monotonic**, peaking for mid-tier models. Weak models cannot exploit a good
  harness; the strongest models already know most of what the harness would tell them.

The practical reading: elaborate scaffolding is worth the most in the middle of the capability range,
and its marginal value declines as base models improve. This is consistent with Weng's own forecast
that harness techniques get absorbed into model behaviour the way prompt-engineering tricks were — but,
she notes, the need to specify goals, constraints, context, and evaluation does not disappear.

### Make the scoreboard unwritable

Every system on rung 4 that works does the same defensive thing: it puts the evaluator outside the
agent's reach. AHE (Automated Harness Engineering) is the clearest instance — it makes the **runs
directory, the tracer, the verifier, and the LLM configuration read-only to the agent**. That single
constraint removes the three cheapest reward hacks: disabling the verifier, swapping in a stronger
model, and raising the reasoning budget. Self-Harness reaches the same place differently, by mining
weaknesses from failure traces, bounding each proposal, and validating on held-in *and* held-out
splits.

[[Philipp Schmid - Recursive Self-Improvement]] states the principle in one line: **"If it can edit
evaluation, it can jailbreak itself. Reward hacking is the default behavior of a system asked to raise
a number."** See [[Benchmark Optimization]].

### Does an optimized harness transfer, or does it overfit?

One encouraging data point: AHE's evolved harness, **frozen**, still transfers to SWE-bench Verified,
suggesting it encoded engineering practice rather than benchmark-specific tricks. One discouraging
one: HarnessOpt-Bench, which separates the editing agent from the tester and scores candidates on
hidden tasks, found results **varying sharply by model and by task** across 111 runs, 5 optimizer
models, and 4 tasks. Transfer is possible, not reliable.

### Keep the archive, not just the winner

Greedy selection is the wrong search policy here. Schmid's illustration makes the case concretely: a
generation-1 variant scoring 58 — worse than its 62-scoring parent — is the one that goes on to parent
the best agent at 84. Greedy selection would have pruned it. Archive-based evolutionary search
(AlphaEvolve, ShinkaEvolve, the Darwin Godel Machine) keeps the losers because they carry structure
the winners lack. Weng lists **diversity collapse** among the field's open challenges for exactly this
reason.

### How much of the harness should be rewritable?

Schmid ranks three postures, and the ordering doubles as a risk ladder:

- **Conservative** (Claude Code, Codex, Cursor) — skills, hooks, and plugins extend a fixed core.
- **Pi** — four built-in tools (`read`, `write`, `edit`, `bash`) and a system prompt under 1,000
  tokens; everything else is a TypeScript extension auto-discovered from `.pi/extensions/`, which an
  agent can write and reload mid-session.
- **DeepSeek Harness** — built on the Cordis plugin kernel, where models, tools, sessions, sandboxes,
  and the control loop itself are swappable, and plugin side effects unwind on unload so the runtime
  can replace parts of itself without dying. Shorthand: `Agent = Model + Harness`.

More rewritable surface means more capability the developers did not anticipate — and more ways to
break compatibility or quietly weaken a permission boundary. See [[Agent Plugin Architecture]].

### The counter-evidence nobody should skip

[[Addy Osmani - Audit your Agent files]] is the sceptical companion to this page. Optimizing rung 1
and rung 2 artifacts assumes those artifacts matter; a study of 288 runs across 17 tasks found that
the presence of `AGENTS.md` / `CLAUDE.md` made **no clear difference to correctness**, and Anthropic
removed more than 80% of Claude Code's system prompt with no measurable eval loss. Before searching a
space, confirm the space has gradient in it.

## Post-training inside the harness you will deploy into

[[adlrocha - Base Models Stopped Being the Bottleneck]] records a release-time practice that makes the harness
effect explicit rather than incidental. Under a heading reading "Downstream Compatibility: broader support for
popular harnesses", **all of Qwen3.8's coding benchmarks were run through the Claude Code harness**.

The reading offered is *"if you want a model to work inside a real agent loop, you post-train it inside a real
agent loop."*

Two things follow. The benchmark numbers describe a **model-plus-harness pair**, not the weights — so
cross-family comparison requires the harness to be held fixed, and it usually is not reported at all. And the
harness has moved upstream of evaluation into training itself, which means harness choice is now a
post-training decision with the same standing as environment choice; see [[RL Environment Design]] and
[[Coding Agent Harness]].

## Four measured reductions, and the trap underneath them

[[GitHub - How We Make AI Coding More Cost Efficient]] is this page's first source reporting **A/B results from
production rather than design reasoning**. Four changes, each measured against an internal AI-credit cost metric:
removing `view` line-number prefixes (**3.1%**), selective output compaction (**5.5%**), a shortened task-tool
prompt (**2.9%**), and batching notification roundtrips (**2.3%**). The source states plainly that these are
**not additive** — a caveat that tends to be lost the moment the numbers travel.

Three findings matter more than the percentages.

**The local metric trap.** An aggressive output compressor reduced per-response tokens and increased total cost,
because agents reopened files and re-ran commands to recover what was removed: *"We saved tokens locally and
spent more globally."* Optimising a component metric is not the same as optimising the loop. The useful
corollary is that **the recovery path doubles as an evaluation signal** — if the agent re-reads what you
compressed, the compression was wrong, and no human judgement is needed to see it.

**Shortening a prompt can silently delete a behaviour.** A meta-prompting loop halved a task-tool prompt and, in
the process, rewrote cautious parallelism guidance into a hard scheduling policy that serialised independent
agents. Offline evaluation did not catch it; production did. The fix was one restored sentence. The stated
lesson: *"Prompt behavior needs tests. If a behavior is not tested, a shorter prompt can remove it without anyone
noticing."*

**Some overhead is archaeology.** The `view` line-number prefixes existed to serve an edit tool that had stopped
needing them. Nobody had removed them. Worth ~5% offline and ~3% online per user.

[[Can Bölük - The Harness Playbook]] adds two optimisation results from the other end of the stack. A terminal
render path measured at **267 seconds was reduced to 90ms**, with **98.7s of the original spent in `wrapAnsi`**
alone — and the profile contained an internal contradiction the author flags himself, since an image-line
`.includes` check accounted for 13% of one panel and 20% of prose rendering in a session that contained **zero
images**. And **compaction should be scheduled, not triggered**: firing at the context limit blocks the user at
the least convenient moment, so fire roughly 10% early, branch, and splice, rather than treating compaction as an
exception handler. His remark that *"even the frontier lab ships the naive design"* is a reminder that
prevalence is not validation.

The overall boundary of this practice is best stated by GitHub: *"None of these changes made the model smarter.
They removed work the model never needed to do."*

## Bounding delegation is a harness optimization with knobs but no published measurements

[[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]] supplies a full set of delegation knobs — fan-out width (6), concurrency
(`Semaphore(4)`), per-child request limit (25), shared result budget (16,000 bytes divided by fan-out
width), retry policy (one nudge, then a "no usable report" note), and output truncation (2,000 lines) —
and grounds them in the same evidence this page already carries, that a harness change alone moved a
coding agent from ~30th to top 5 on Terminal-Bench.

The honest reading is that these are **budgets, not results**. The source reports no before/after on token
spend, latency, or answer quality for the six-subagent research setup that motivates it, so the numbers
are a starting configuration rather than a tuned optimum. Two of them are in visible tension: dividing a
fixed result budget across the fan-out means six children get roughly 2.7 KB each, and nothing establishes
that a useful report fits.

One structural gap is named by the author: Decode has no in-flight queue letting a parent communicate with
a running subagent, so a fan-out is fire-and-forget and a child that misreads its prompt burns its full
25-request budget before anyone finds out. Closing that gap is an observability problem as much as a
harness one — see [[Agent Observability]].

A related generalisation from outside the agent loop: a 100-document serial pipeline rewritten under
`asyncio.gather()` with a `Semaphore(5)` turned an hours-long run into a bounded one. Bounded parallelism
is the same optimization whether the work is a subagent or a document.

## One patch per round is what makes a harness edit attributable

This page's fourth open question asks what the unit of credit assignment should be when an optimizer
changes several rungs at once.
[[Lance Martin - Automating Eval Design and Hillclimbing with Claude]] answers by refusing the premise.
Candidate changes may target prompts, skills, tool descriptions, model choice, effort, API parameters,
or harness code — rungs 1 through 4 of the ladder above — but the loop proposes **one patch per round**.
The evaluation is split into a search set and a held-out test set; a patch is kept only when **train and
test both improve**, and reverted when only train improves or when either regresses. Attribution is
bought by narrowing the step rather than by analysing a wide one after the fact.

Two stopping rules bound the loop, and the second is a discipline this page's other sources lack. If
progress stalls for **two or three rounds**, remaining failures are bucketed by cause rather than
attacked individually. If an expected gain falls **below evaluation noise**, the response is to add
repetitions or cases — to improve the instrument — rather than make an edit nobody can measure.
Grader determinism is checked up front by running **the grader twice on the same output** and reporting
whether the verdict changed; separately, before the first round the eval's own noise — how far the score
can move by chance alone — is checked against the smallest improvement worth acting on. Results carry a
confidence interval with one full transcript per case. There is also an input-side version of this
page's unwritable-scoreboard rule: failures are never pasted into prompts, so evaluation answers stay
structurally inaccessible to the thing being optimized.

The reported numbers need every condition carried with them. On an internal benchmark of **44 tickets**
(**30** for search, **14** held out), on the **30 search (train) tickets** the baseline Opus 4.8 at high
effort scored **74.4% decision accuracy at 4.6 cents per ticket**; Opus 5.5 at low effort **87.8% at 1.9
cents**; Sonnet 5 at low effort **88.9% at 1 cent**; prompt work took Sonnet 5 to **98.9%** at about the
same cost. On the **14 held-out tickets** — a different split, which is why the original baseline reads
differently there — the final configuration scored **90.5%** against the original setup's **78.6%**, at
roughly **one fifth of the cost**. That before-and-after is **not a clean measurement of hillclimbing**:
it bundles a model change, an effort
change, a prompt change, and a pricing change, since Opus 5.5 is stated to price input and output **20%
less** than Opus 4.8 and cache reads **60% less**. This is the same attribution discipline the page
already applies to GitHub's four measured reductions, and here it bites harder — part of the cost win is
a price list. Everything is Anthropic-reported on an Anthropic workflow with no independent reproduction
and no released evaluation data; see [[Anthropic]].

The capability example is the more interesting one for this page because it is a rung-2 artifact under
optimization: the Claude API skill began at **66%**, reached **74%** after eight features were covered
and **77%** after C# and Java type tables were fixed, ending near **88%**, with the figure caption
reporting **66.1%** baseline and **87.9% at round 24**. Martin's own limits complicate this page's
rung-4 optimism rather than overturning it. He concedes that leakage and overfitting persist, **including
harness additions that solve benchmark quirks rather than production problems**, and that the method
suits cheap, attributable surfaces such as prompts and skills better than open-ended harness rewrites
where a single patch is hard to isolate. AHE's frozen harness transferring to SWE-bench Verified remains
the page's evidence that rung-4 search can encode practice; this is a first-hand report that it can also
encode the benchmark, from a practitioner who was looking for it.

## Optimize the available primitives, not necessarily a fixed topology

[[Replit - Free the Models - Harness Design at the Frontier]] changes the object being optimized:
the harness supplies specialists, worker tier/effort, reusable subagents, and dynamic effort, while
the core chooses the execution pattern. This is not autonomous rewriting of harness code; it is
model-selected use of a designed action space.

Its four-repeat Max/Astra comparison reports **72% at $2.11 per task** versus a one-worker
sidekick's **61% at $1.34** on **113 DeepSWE v1.1 tasks**. On **63 Terminal-Bench 4.0 tasks,
excluding three GPU tasks**, the rounded figures are **49% at $2.53** versus **33% at $1.84**.
The gain costs more; public xhigh baselines cost still more and score higher. The outcome therefore
supports a reported nondominated operating point, not superiority on both axes.

Read against the ladder above, the lesson is to re-evaluate whether a stronger model needs a
prescribed workflow at all before optimizing its details. Keep the same external evaluator and
authority constraints either way. The source does not isolate each primitive's contribution,
and published baselines are not controlled reruns.

## Choose the smallest editable surface that contains the bottleneck

[[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]] supplies a
complementary map: skills, harness code, model-harness co-evolution, environment wrappers,
and orchestration. These are overlapping intervention choices, not stages every project should
climb. Weng's ladder measures how much scaffold code may change; this map asks where the
observed failure lives.

WikiSkill's experience wiki retains successes, failures, and rejected fixes upstream of skill
edits, addressing the negative-result-memory gap previously listed below. EnvHarness changes
the learning experience while keeping core environment logic and the verifier fixed. Raven
makes specialist coordination another optimization target. Weight training in HarnessX is
outside this page's strict frozen-model definition and belongs to a separately evaluated
model-harness pair.

The newer Self-Harness maximum also needs a specific denominator: the matched public article
locates **132% relative improvement** at **22.5% to 52.2% for Qwen3.5-35B-A3B on AppWorld**,
not a 132-point gain across all agents. It is a secondary report, not a controlled comparison
with the earlier newsletter's Terminal-Bench figures or an ablation proving that verification
gates alone caused the improvement.

## Open questions

- Does climbing the ladder add capability, or only variance that a strong model can exploit and a weak
  one cannot? Every rung-4 and rung-5 result cited here is gated on base-model strength.
- If harness-benefit peaks for mid-tier models, harness research has a moving target. How should a
  technique be validated so it survives the next model generation?
- How do you keep an evaluator both unreachable *and* improving? Read-only evaluators cap the system
  at self-improvement rather than recursion.
- What is the right unit of credit assignment when an optimizer changes several rungs at once?
- WikiSkill now explicitly targets memory of rejected fixes. What evidence shows that retained
  negative results reduce repeated search rather than preserve stale explanations?
- One patch per round with an immediate revert *is* greedy selection, which this page argues against
  elsewhere: Schmid's generation-1 variant scoring 58 went on to parent the best agent at 84. Does the
  attributability gained justify pruning exactly the candidates archive-based search keeps?
- Does a two-or-three-round stall indicate exhausted headroom, or only exhausted proposals from one
  proposer? STOP's base-model dependence suggests the second reading is available and untested.

## Related pages

- [[Ben Dickson - How AI Agents Are Learning to Optimize Their Own Stack]]
- [[Persistent Wiki]]
- [[RL Environment Design]]
- [[Graph Engineering]]
- [[Replit - Free the Models - Harness Design at the Frontier]]
- [[Replit]]
- [[Inference Efficiency Frontier]]
- [[Recursive Self-Improvement]]
- [[Coding Agent Harness]]
- [[Context Engineering]]
- [[Automated AI Research]]
- [[Benchmark Optimization]]
- [[Agent Plugin Architecture]]
- [[Agent Skill]]
- [[Loop Engineering]]
- [[Lilian Weng - Harness Engineering for Self-Improvement]]
- [[Philipp Schmid - Recursive Self-Improvement]]
- [[Addy Osmani - Audit your Agent files]]
- [[adlrocha - Base Models Stopped Being the Bottleneck]]
- [[Qwen]]
- [[Tool Roster Economics]]
- [[Harness State Authority]]
- [[GitHub - How We Make AI Coding More Cost Efficient]]
- [[Can Bölük - The Harness Playbook]]
- [[GitHub]]
- [[Can Bölük]]
- [[Paul Iusztin - From 1 Bloated Context Window to 6 Scoped Subagents]]
- [[Paul Iusztin]]
- [[Agent Delegation]]
- [[Agent Observability]]
- [[Lance Martin - Automating Eval Design and Hillclimbing with Claude]]
- [[Anthropic]]
- [[Agentic Testing]]
- [[Multi-Turn Evaluation]]
